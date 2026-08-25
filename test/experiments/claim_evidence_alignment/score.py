"""Blind scorer for article-level claim/evidence alignment predictions.

Gold cards are never passed to the system under test.  This scorer consumes
them only after predictions have been written under repeat_XX/<case_id>.json.
Only manifest cases explicitly marked ``gold`` are scored; machine drafts and
unreviewed annotations cannot silently become ground truth.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.claim_evidence import ArticleResultCard, audit_result_card  # noqa: E402


def _load_card(path: Path) -> ArticleResultCard:
    return ArticleResultCard.model_validate_json(path.read_text(encoding="utf-8"))


def _link_map(card: ArticleResultCard) -> dict[tuple[str, str | None], str]:
    return {(x.claim_id, x.evidence_id): x.relation for x in card.links}


def score_card(gold: ArticleResultCard, predicted: ArticleResultCard) -> dict:
    if gold.annotation_status != "gold":
        raise ValueError("Gold card must have annotation_status='gold'.")
    gold_audit = audit_result_card(gold, verify_artifacts=False)
    if gold_audit["verdict"] != "pass":
        raise ValueError(f"Gold card failed deterministic audit: {gold_audit['blocking']}")

    gold_links = _link_map(gold)
    predicted_links = _link_map(predicted)
    correct = sum(predicted_links.get(key) == relation for key, relation in gold_links.items())
    false_direct = sum(
        relation == "direct_support" and gold_links.get(key) != "direct_support"
        for key, relation in predicted_links.items()
    )

    gold_primary = {x.claim_id for x in gold.claims if x.importance == "primary"}
    predicted_linked = {x.claim_id for x in predicted.links}
    primary_covered = len(gold_primary & predicted_linked)

    placeholder = lambda s: not s or "SOURCE REQUIRED" in s or "TODO" in s
    predicted_claims = {x.claim_id: x for x in predicted.claims}
    predicted_evidence = {x.evidence_id: x for x in predicted.evidence}
    links_by_claim: dict[str, list] = {}
    for link in predicted.links:
        links_by_claim.setdefault(link.claim_id, []).append(link)

    def _claim_is_grounded(claim_id: str) -> bool:
        claim = predicted_claims.get(claim_id)
        if claim is None or placeholder(claim.source_quote) or placeholder(claim.source_locator):
            return False
        links = links_by_claim.get(claim_id, [])
        if not links:
            return False
        for link in links:
            if link.relation == "not_evaluable":
                continue
            evidence = predicted_evidence.get(link.evidence_id)
            if evidence is None or not (evidence.artifact_paths or evidence.source_locator):
                return False
        return True

    sourced_primary = sum(_claim_is_grounded(claim_id) for claim_id in gold_primary)

    return {
        "article_id": gold.article_id,
        "relation_total": len(gold_links),
        "relation_correct": correct,
        "relation_accuracy": correct / len(gold_links) if gold_links else 0.0,
        "false_direct_support": false_direct,
        "primary_claim_total": len(gold_primary),
        "primary_claim_covered": primary_covered,
        "primary_claim_coverage": primary_covered / len(gold_primary) if gold_primary else 0.0,
        "sourced_primary_claims": sourced_primary,
        "provenance_completeness": sourced_primary / len(gold_primary) if gold_primary else 0.0,
        "has_deliverable": bool(predicted.claims and predicted.links),
        "deliverable_level": predicted.deliverable_level,
        "prediction_relations": {
            f"{claim_id}|{evidence_id or ''}": relation
            for (claim_id, evidence_id), relation in sorted(predicted_links.items())
        },
    }


def score_benchmark(manifest_path: Path, predictions_root: Path, repeats: int = 3) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    base = manifest_path.parent
    gold_cases = [x for x in manifest.get("cases", []) if x.get("annotation_status") == "gold"]
    if len(gold_cases) < 6:
        return {
            "verdict": "insufficient_gold",
            "gold_case_count": len(gold_cases),
            "required_gold_cases": 6,
            "blocking": ["fewer_than_6_human_reviewed_gold_cases"],
        }

    rows, missing = [], []
    relations_by_case: dict[str, list[dict]] = {}
    for repeat in range(1, repeats + 1):
        repeat_dir = predictions_root / f"repeat_{repeat:02d}"
        for case in gold_cases:
            case_id = case["case_id"]
            gold_path = base / case["gold_card"]
            predicted_path = repeat_dir / f"{case_id}.json"
            if not predicted_path.is_file():
                missing.append(str(predicted_path))
                continue
            gold = _load_card(gold_path)
            predicted = _load_card(predicted_path)
            row = score_card(gold, predicted)
            row.update({"case_id": case_id, "repeat": repeat})
            rows.append(row)
            relations_by_case.setdefault(case_id, []).append(row["prediction_relations"])

    relation_total = sum(x["relation_total"] for x in rows)
    relation_correct = sum(x["relation_correct"] for x in rows)
    primary_total = sum(x["primary_claim_total"] for x in rows)
    primary_covered = sum(x["primary_claim_covered"] for x in rows)
    sourced_primary = sum(x["sourced_primary_claims"] for x in rows)
    expected_predictions = len(gold_cases) * repeats
    stable_cases = sum(
        len(values) == repeats and all(value == values[0] for value in values[1:])
        for values in relations_by_case.values()
    )
    metrics = {
        "relation_accuracy": relation_correct / relation_total if relation_total else 0.0,
        "false_direct_support": sum(x["false_direct_support"] for x in rows),
        "primary_claim_coverage": primary_covered / primary_total if primary_total else 0.0,
        "provenance_completeness": sourced_primary / primary_total if primary_total else 0.0,
        "article_deliverable_coverage": len([x for x in rows if x["has_deliverable"]]) /
        expected_predictions,
        "stable_case_rate": stable_cases / len(gold_cases),
    }
    acceptance = {
        "all_predictions_present": len(rows) == expected_predictions and not missing,
        "relation_accuracy_gte_0_85": metrics["relation_accuracy"] >= 0.85,
        "zero_false_direct_support": metrics["false_direct_support"] == 0,
        "all_primary_claims_mapped": metrics["primary_claim_coverage"] == 1.0,
        "complete_primary_claim_provenance": metrics["provenance_completeness"] == 1.0,
        "every_article_has_deliverable": metrics["article_deliverable_coverage"] == 1.0,
        "relations_stable_across_3_repeats": metrics["stable_case_rate"] == 1.0,
    }
    return {
        "verdict": "pass" if all(acceptance.values()) else "fail",
        "gold_case_count": len(gold_cases),
        "repeats": repeats,
        "expected_predictions": expected_predictions,
        "observed_predictions": len(rows),
        "metrics": metrics,
        "acceptance": acceptance,
        "missing_predictions": missing,
        "rows": rows,
    }


def _write_markdown(report: dict, path: Path) -> None:
    lines = [
        "# Claim-evidence alignment benchmark",
        "",
        f"Verdict: **{report['verdict']}**",
        "",
    ]
    if "metrics" in report:
        lines.extend(["## Metrics", ""])
        for key, value in report["metrics"].items():
            lines.append(f"- {key}: {value}")
        lines.extend(["", "## Acceptance", ""])
        for key, value in report["acceptance"].items():
            lines.append(f"- {key}: {'PASS' if value else 'FAIL'}")
    else:
        lines.append(f"Blocking: {', '.join(report.get('blocking', []))}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--predictions-root", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = score_benchmark(args.manifest, args.predictions_root, args.repeats)
    (args.output_dir / "claim_evidence_score.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    _write_markdown(report, args.output_dir / "claim_evidence_score.md")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))
    return 0 if report["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
