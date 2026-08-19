"""Compare saved Sonnet and DeepSeek exercise-paper SEA-CDM artifacts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics
import sys

import pandas as pd


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import (  # noqa: E402
    DESCRIPTIVE_TABLES, REQUIRED_TABLES, STRUCTURAL_TABLES, exercise_semantics, token_overlap,
    exercise_semantics_after_projection_fix,
)
from tools.metadata_structural import build_structural_tables  # noqa: E402


def row_text(tables: dict, names) -> str:
    return " ".join(str(value) for name in names for row in tables.get(name, [])
                    for value in row.values() if value not in (None, ""))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-dir", required=True)
    args = parser.parse_args()
    root = Path(args.experiment_dir).resolve()
    reports = {
        provider: json.loads((root / provider / "provider_report.json").read_text(encoding="utf-8"))
        for provider in ("anthropic", "deepseek")
    }
    manifest = json.loads((root / "frozen_manifest.json").read_text(encoding="utf-8"))
    cases = {case["study_id"]: case for case in manifest["cases"]}
    by_provider = {
        provider: {row["study_id"]: row for row in report["records"]}
        for provider, report in reports.items()
    }
    studies = sorted(set(by_provider["anthropic"]) & set(by_provider["deepseek"]))
    pairs = []
    for study in studies:
        left = by_provider["anthropic"][study]
        right = by_provider["deepseek"][study]
        lt = json.loads(Path(left["tables_path"]).read_text(encoding="utf-8"))
        rt = json.loads(Path(right["tables_path"]).read_text(encoding="utf-8"))
        structural_equal = all(lt.get(name) == rt.get(name) for name in STRUCTURAL_TABLES)
        descriptive_overlap = token_overlap(
            row_text(lt, DESCRIPTIVE_TABLES), row_text(rt, DESCRIPTIVE_TABLES)
        )
        table_row_deltas = {name: len(rt.get(name, [])) - len(lt.get(name, [])) for name in lt}
        left_exercise = exercise_semantics(lt, cases[study]["metadata_path"])
        right_exercise = exercise_semantics(rt, cases[study]["metadata_path"])
        left_postfix = exercise_semantics_after_projection_fix(
            lt, cases[study]["metadata_path"]
        )
        right_postfix = exercise_semantics_after_projection_fix(
            rt, cases[study]["metadata_path"]
        )

        def adjudicated_blocking(record, tables, exercise_check):
            blocking = [item for item in record["blocking"] if item != "required_tables_present"]
            if any(not tables.get(name) for name in REQUIRED_TABLES):
                blocking.append("required_tables_present")
            if not exercise_check["passed"]:
                blocking.append("exercise_semantics_valid")
            return sorted(set(blocking))

        left_blocking = adjudicated_blocking(left, lt, left_exercise)
        right_blocking = adjudicated_blocking(right, rt, right_exercise)
        left_postfix_blocking = [item for item in left_blocking if item != "exercise_semantics_valid"]
        right_postfix_blocking = [item for item in right_blocking if item != "exercise_semantics_valid"]
        if not left_postfix["passed"]:
            left_postfix_blocking.append("exercise_semantics_valid")
        if not right_postfix["passed"]:
            right_postfix_blocking.append("exercise_semantics_valid")
        pairs.append({
            "study_id": study,
            "sonnet_pass": not left_blocking, "deepseek_pass": not right_blocking,
            "sonnet_blocking": ";".join(left_blocking),
            "deepseek_blocking": ";".join(right_blocking),
            "exercise_required_by_geo_scope": left_exercise["required_by_geo_scope"],
            "sonnet_exercise_check": left_exercise,
            "deepseek_exercise_check": right_exercise,
            "sonnet_postfix_pass": not left_postfix_blocking,
            "deepseek_postfix_pass": not right_postfix_blocking,
            "sonnet_postfix_blocking": ";".join(sorted(set(left_postfix_blocking))),
            "deepseek_postfix_blocking": ";".join(sorted(set(right_postfix_blocking))),
            "sonnet_postfix_exercise_check": left_postfix,
            "deepseek_postfix_exercise_check": right_postfix,
            "structural_tables_equal": structural_equal,
            "descriptive_token_overlap": round(descriptive_overlap, 4),
            "sonnet_provenance": left["provenance_rate"],
            "deepseek_provenance": right["provenance_rate"],
            "sonnet_cost_usd": left["estimated_cost_usd"],
            "deepseek_cost_usd": right["estimated_cost_usd"],
            "sonnet_latency_seconds": left["elapsed_seconds"],
            "deepseek_latency_seconds": right["elapsed_seconds"],
            "table_row_deltas_deepseek_minus_sonnet": table_row_deltas,
        })

    summaries = {provider: report["summary"] for provider, report in reports.items()}
    sonnet_cost = summaries["anthropic"]["total_cost_usd"]
    deepseek_cost = summaries["deepseek"]["total_cost_usd"]
    adjudicated = {
        "anthropic": sum(row["sonnet_pass"] for row in pairs),
        "deepseek": sum(row["deepseek_pass"] for row in pairs),
    }
    postfix = {
        "anthropic": sum(row["sonnet_postfix_pass"] for row in pairs),
        "deepseek": sum(row["deepseek_postfix_pass"] for row in pairs),
    }
    remediation = {}
    remediated_study = "GSE319603"
    for provider in ("anthropic", "deepseek"):
        post_dir = root / f"{provider}_postfix2_gse319603"
        if not (post_dir / "provider_report.json").is_file():
            continue
        post_report = json.loads((post_dir / "provider_report.json").read_text(encoding="utf-8"))
        record = post_report["records"][0]
        tables = json.loads(Path(record["tables_path"]).read_text(encoding="utf-8"))
        structural = build_structural_tables(
            remediated_study, f"{remediated_study}_exp1",
            cases[remediated_study]["metadata_path"],
        )
        remediation[provider] = {
            "passed": not record["blocking"],
            "blocking": record["blocking"],
            "cost_usd": record["estimated_cost_usd"],
            "latency_seconds": record["elapsed_seconds"],
            "intervention_rows": len(tables.get("interventions") or []),
            "exercise_rows": len(tables.get("exercise") or []),
            "corrected_group_rows": len(structural["groups"]),
            "corrected_group_labels": [row["subject_group"] for row in structural["groups"]],
        }
        audit_path = post_dir / "agent_evaluation.json"
        if audit_path.is_file():
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            remediation[provider]["audit_verdict"] = audit["verdict"]
            remediation[provider]["audit_score"] = audit["score"]
            remediation[provider]["audit_coverage"] = audit["coverage"]
    comparison = {
        "schema_version": "1.0", "papers_compared": len(studies),
        "provider_summaries": summaries,
        "adjudicated_passed": adjudicated,
        "postfix_regraded_passed": postfix,
        "targeted_remediation": remediation,
        "deepseek_cost_fraction_of_sonnet": round(deepseek_cost / sonnet_cost, 4)
        if sonnet_cost else None,
        "structural_equal_studies": sum(row["structural_tables_equal"] for row in pairs),
        "mean_descriptive_token_overlap": round(statistics.mean(
            row["descriptive_token_overlap"] for row in pairs), 4) if pairs else None,
        "pairs": pairs,
        "limitations": [
            "One pass per model; run-to-run stability is not measured.",
            "No full field-by-field domain-expert gold annotation for all papers.",
            "Structural equality is expected because GEO metadata derivation is deterministic.",
            "Adjudicated pass counts condition the Exercise-table requirement on target GEO scope and reject semantically invalid Exercise rows.",
        ],
    }
    json_path = root / "comparison.json"
    csv_path = root / "comparison.csv"
    md_path = root / "comparison.md"
    json_path.write_text(json.dumps(comparison, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.DataFrame([{key: value for key, value in row.items()
                   if key != "table_row_deltas_deepseek_minus_sonnet"}
                  for row in pairs]).to_csv(csv_path, index=False)
    lines = [
        "# Exercise 10-paper SEA-CDM: Sonnet vs DeepSeek", "",
        f"- Papers compared: **{len(studies)}**",
        f"- Sonnet passed (scope-adjudicated): **{adjudicated['anthropic']}/{len(studies)}**",
        f"- DeepSeek passed (scope-adjudicated): **{adjudicated['deepseek']}/{len(studies)}**",
        f"- After corrected deterministic Exercise projection: Sonnet **{postfix['anthropic']}/{len(studies)}**, DeepSeek **{postfix['deepseek']}/{len(studies)}**",
        f"- Legacy unconditional-Exercise score: Sonnet {summaries['anthropic']['passed']}/{len(studies)}, DeepSeek {summaries['deepseek']['passed']}/{len(studies)}",
        f"- Sonnet total cost: **${sonnet_cost:.4f}**",
        f"- DeepSeek total cost: **${deepseek_cost:.4f}**",
        f"- DeepSeek/Sonnet cost: **{comparison['deepseek_cost_fraction_of_sonnet']:.1%}**",
        f"- Structural tables equal: **{comparison['structural_equal_studies']}/{len(studies)}**",
        f"- Mean descriptive token overlap: **{comparison['mean_descriptive_token_overlap']:.1%}**",
        "", "| Study | Sonnet artifact | DeepSeek artifact | Sonnet post-fix | DeepSeek post-fix | Structure | Text overlap | S prov. | DS prov. |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in pairs:
        lines.append(
            f"| {row['study_id']} | {'pass' if row['sonnet_pass'] else 'fail'} | "
            f"{'pass' if row['deepseek_pass'] else 'fail'} | "
            f"{'pass' if row['sonnet_postfix_pass'] else 'fail'} | "
            f"{'pass' if row['deepseek_postfix_pass'] else 'fail'} | "
            f"{'same' if row['structural_tables_equal'] else 'different'} | "
            f"{row['descriptive_token_overlap']:.1%} | {row['sonnet_provenance']:.1%} | "
            f"{row['deepseek_provenance']:.1%} |"
        )
    if remediation:
        lines.extend(["", "## Targeted remediation: GSE319603", ""])
        for provider, result in remediation.items():
            label = "Sonnet" if provider == "anthropic" else "DeepSeek"
            lines.append(
                f"- {label}: **{'pass' if result['passed'] else 'fail'}**, "
                f"{result['intervention_rows']} interventions, {result['exercise_rows']} exercise row, "
                f"${result['cost_usd']:.4f}, {result['latency_seconds']:.1f}s; "
                f"audit {result.get('audit_score', 'n/a')}/100 at "
                f"{result.get('audit_coverage', 'n/a')}% coverage."
            )
        first = next(iter(remediation.values()))
        lines.append(
            f"- Corrected deterministic grouping: **{first['corrected_group_rows']} groups** — "
            + ", ".join(first["corrected_group_labels"]) + "."
        )
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in comparison["limitations"])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "comparison": str(md_path), "papers": len(studies),
        "sonnet_passed": adjudicated["anthropic"],
        "deepseek_passed": adjudicated["deepseek"],
        "deepseek_cost_fraction": comparison["deepseek_cost_fraction_of_sonnet"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
