"""A/B test: paper extraction/workflow planning without vs with one curated example."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import statistics
import sys
from typing import Any

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
TARGET_PAPER = ROOT / "data" / "papers" / "e75202c88162591e3fd87ca88a1721c51d408f1a.txt"
MODEL = "claude-sonnet-4-6"

sys.path.insert(0, str(ROOT))
from tools.run_status import RunStatusTracker  # noqa: E402


class WorkflowStep(BaseModel):
    stage: str
    action: str
    reason: str


class PaperWorkflowExtraction(BaseModel):
    paper_title: str
    organisms: list[str]
    geo_accessions: list[str]
    modalities: list[str]
    comparison_groups: list[str]
    reported_methods: list[str]
    recommended_workflow: list[WorkflowStep]
    requires_manual_review: bool
    review_reasons: list[str]
    evidence_snippets: list[str] = Field(
        description="At most 3 exact short snippets from the target paper, each at most 8 words."
    )


BASE_SYSTEM = """You are evaluating one biomedical paper for a bioinformatics agent.
Extract study facts and recommend a scientifically safe computational workflow.

Rules:
- Use only facts supported by the TARGET PAPER.
- Return every GEO accession stated as a dataset used by the study.
- Separate bulk and single-cell modalities.
- Never recommend treating individual cells as biological replicates.
- Do not invent a treatment-control contrast for observational, clustering, validation, or
  prognostic designs.
- If matrix scale, replicate identity, ownership, or design is unresolved, require manual review.
- Evidence snippets must be exact target-paper phrases, maximum 3 snippets and 8 words each.
- Example identifiers, groups, genes, and conclusions are illustrative. Never copy them unless
  they independently occur in the target paper.
"""


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()


def _concept_set(values: list[str], aliases: dict[str, tuple[str, ...]]) -> set[str]:
    joined = " | ".join(_normalize(x) for x in values)
    return {concept for concept, terms in aliases.items() if any(_normalize(t) in joined for t in terms)}


def _f1(pred: set[str], gold: set[str]) -> float:
    if not pred and not gold:
        return 1.0
    if not pred or not gold:
        return 0.0
    tp = len(pred & gold)
    precision, recall = tp / len(pred), tp / len(gold)
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def _score(result: PaperWorkflowExtraction, target_text: str, gold: dict) -> dict[str, Any]:
    predicted_accessions = {x.upper() for x in result.geo_accessions if re.fullmatch(r"GSE\d+", x.upper())}
    gold_accessions = set(gold["geo_accessions"])
    accession_f1 = _f1(predicted_accessions, gold_accessions)
    hallucinated = sorted(predicted_accessions - gold_accessions)

    modality_aliases = {
        "bulk": ("bulk", "microarray", "gene expression"),
        "single_cell": ("single cell", "scrna", "sc rna"),
    }
    group_aliases = {
        "cluster_a": ("cluster a",), "cluster_b": ("cluster b",),
        "high_mri": ("high mri", "high macrophage related index"),
        "low_mri": ("low mri", "low macrophage related index"),
    }
    method_aliases = {
        "consensus_clustering": ("consensus clustering",),
        "differential_expression": ("differential expression", "deg"),
        "go": ("go enrichment", "gene ontology"), "kegg": ("kegg",),
        "gsva": ("gsva",), "lasso": ("lasso",),
        "cox": ("cox",), "survival": ("kaplan meier", "km curve", "survival analysis"),
        "roc": ("roc",), "ssgsea": ("ssgsea", "single sample gene set enrichment"),
    }
    modality_f1 = _f1(_concept_set(result.modalities, modality_aliases), set(modality_aliases))
    group_f1 = _f1(_concept_set(result.comparison_groups, group_aliases), set(group_aliases))
    method_f1 = _f1(_concept_set(result.reported_methods, method_aliases), set(method_aliases))
    organism = 1.0 if any("human" in _normalize(x) or "homo sapiens" in _normalize(x)
                          for x in result.organisms) else 0.0
    title = 1.0 if _normalize(gold["paper_title"]) == _normalize(result.paper_title) else 0.0

    workflow_text = _normalize(" ".join(
        [f"{x.stage} {x.action} {x.reason}" for x in result.recommended_workflow]
        + result.review_reasons
    ))
    scale_pattern = r"(?:fpkm|tpm|log(?: scale| transformed)?|normalized continuous|float)"
    voom_pattern = r"(?:limma voom|voom)"
    unsafe_log_voom = bool(
        re.search(scale_pattern + r"[a-z0-9 ]{0,120}" + voom_pattern, workflow_text)
        or re.search(voom_pattern + r"[a-z0-9 ]{0,120}" + scale_pattern, workflow_text)
    )
    dataset_coverage = sum(name in workflow_text for name in ("tcga", "gse71014", "target", "gse116256"))
    safety_checks = {
        "separate_datasets": (dataset_coverage >= 3 or
                              any(x in workflow_text for x in ("each dataset", "separately", "dataset specific"))),
        "no_cell_as_replicate": ("pseudobulk" in workflow_text or
                                  ("cell" in workflow_text and "biological replicate" in workflow_text)),
        "replicate_gate": "replicate" in workflow_text,
        "no_forced_contrast": any(x in workflow_text for x in (
            "do not force", "do not impose", "no clean", "not treatment control",
            "not a treatment control", "not pre assigned experimental", "prognostic clustering study",
        )),
        "manual_review": result.requires_manual_review,
        "matrix_method_compatibility": not unsafe_log_voom,
    }
    safety = sum(safety_checks.values()) / len(safety_checks)

    normalized_target = _normalize(target_text)
    grounded = []
    for snippet in result.evidence_snippets[:3]:
        words = snippet.split()
        grounded.append(bool(snippet.strip()) and len(words) <= 8 and _normalize(snippet) in normalized_target)
    evidence_grounding = sum(grounded) / max(1, len(grounded)) if result.evidence_snippets else 0.0

    copied_example = sorted(predicted_accessions & {"GSE279359"})
    penalty = min(0.20, 0.10 * len(hallucinated) + 0.10 * len(copied_example))
    weighted = (
        0.22 * accession_f1 + 0.10 * modality_f1 + 0.08 * organism + 0.08 * title
        + 0.12 * group_f1 + 0.15 * method_f1 + 0.18 * safety + 0.07 * evidence_grounding
        - penalty
    )
    return {
        "total": round(max(0.0, weighted) * 100, 2),
        "components": {
            "accession_f1": round(accession_f1, 4), "modality_f1": round(modality_f1, 4),
            "organism": organism, "title": title, "group_f1": round(group_f1, 4),
            "method_f1": round(method_f1, 4), "workflow_safety": round(safety, 4),
            "evidence_grounding": round(evidence_grounding, 4),
        },
        "safety_checks": safety_checks,
        "predicted_accessions": sorted(predicted_accessions),
        "hallucinated_accessions": hallucinated,
        "copied_example_accessions": copied_example,
    }


def _usage(raw) -> dict[str, int]:
    metadata = getattr(raw, "usage_metadata", None) or {}
    input_tokens = int(metadata.get("input_tokens") or 0)
    output_tokens = int(metadata.get("output_tokens") or 0)
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_usd": round(input_tokens * 3 / 1_000_000 + output_tokens * 15 / 1_000_000, 6),
    }


def _acceptance(records: list[dict[str, Any]]) -> dict[str, Any]:
    deltas = [float(item["delta_b_minus_a"]) for item in records]
    method_gate_passed = all(
        bool(item["condition_b"]["score"]["safety_checks"].get("matrix_method_compatibility"))
        for item in records
    )
    safety_non_regression = all(
        float(item["condition_b"]["score"]["components"]["workflow_safety"])
        >= float(item["condition_a"]["score"]["components"]["workflow_safety"])
        for item in records
    )
    no_hallucinated_accessions = all(
        not item["condition_b"]["score"].get("hallucinated_accessions")
        and not item["condition_b"]["score"].get("copied_example_accessions")
        for item in records
    )
    positive_mean = statistics.mean(deltas) > 0
    accepted = positive_mean and method_gate_passed and safety_non_regression and no_hallucinated_accessions
    return {
        "verdict": "accept" if accepted else "reject",
        "positive_mean_delta": positive_mean,
        "method_compatibility_gate_passed": method_gate_passed,
        "paired_safety_non_regression": safety_non_regression,
        "no_hallucinated_or_copied_accessions": no_hallucinated_accessions,
        "paired_wins": sum(delta > 0 for delta in deltas),
        "paired_ties": sum(delta == 0 for delta in deltas),
        "paired_losses": sum(delta < 0 for delta in deltas),
        "delta_sample_stdev": round(statistics.stdev(deltas), 2) if len(deltas) > 1 else None,
    }


def _run_condition(llm, target_text: str, context: dict | str | None) -> tuple[PaperWorkflowExtraction, dict]:
    system = BASE_SYSTEM
    if isinstance(context, dict):
        system += "\nCURATED EXAMPLE (structure and reasoning only):\n" + json.dumps(context, ensure_ascii=False, indent=2)
    elif isinstance(context, str):
        system += "\nRUNTIME SKILL (loaded before reasoning):\n" + context
    prompt = system + "\n\nTARGET PAPER:\n" + target_text
    runnable = llm.with_structured_output(PaperWorkflowExtraction, include_raw=True)
    response = runnable.invoke(prompt)
    if response.get("parsing_error") or response.get("parsed") is None:
        raise RuntimeError(f"structured parsing failed: {response.get('parsing_error')}")
    return response["parsed"], _usage(response.get("raw"))


def _write_json(path: Path, value: Any) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(value, fh, indent=2, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--condition-b", choices=("example", "runtime-skill"), default="example")
    parser.add_argument("--skill-name", default="paper-workflow-safety")
    args = parser.parse_args()
    if args.repeats < 1:
        raise SystemExit("--repeats must be >= 1")

    load_dotenv(ROOT / ".env")
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        raise SystemExit("CLAUDE_API_KEY not found")
    target_text = TARGET_PAPER.read_text(encoding="utf-8")
    if args.condition_b == "runtime-skill":
        from tools.runtime_skills import load_runtime_skill_bundle
        condition_b_context: dict | str = load_runtime_skill_bundle(args.skill_name)
        condition_b_label = f"runtime skill: {args.skill_name}"
    else:
        condition_b_context = json.loads((HERE / "example_case.json").read_text(encoding="utf-8"))
        condition_b_label = "curated example"
    gold = json.loads((HERE / "gold_target.json").read_text(encoding="utf-8"))

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(args.output_dir) if args.output_dir else ROOT / "output" / f"fewshot_case_ab_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    if isinstance(condition_b_context, str):
        (out / "condition_b_runtime_skill_bundle.txt").write_bytes(condition_b_context.encode("utf-8"))
        condition_b_sha256 = hashlib.sha256(condition_b_context.encode("utf-8")).hexdigest()
    else:
        context_text = json.dumps(condition_b_context, ensure_ascii=False, indent=2)
        (out / "condition_b_curated_example.json").write_text(context_text, encoding="utf-8")
        condition_b_sha256 = hashlib.sha256(context_text.encode("utf-8")).hexdigest()
    tracker = RunStatusTracker(str(out / "run_status.json"), run_id=f"fewshot_ab_{stamp}",
                               profile="fewshot_ab", stages=["condition_a", "condition_b", "score", "report"])
    tracker.start("controlled A/B experiment")
    llm = ChatAnthropic(model=MODEL, api_key=api_key, temperature=0)

    records = []
    try:
        for repeat in range(1, args.repeats + 1):
            outputs = {}
            # Alternate call order to reduce provider/order effects while preserving paired inputs.
            order = ("condition_b", "condition_a") if repeat % 2 else ("condition_a", "condition_b")
            for condition in order:
                if condition == "condition_a":
                    tracker.set_stage("condition_a", message=f"repeat {repeat}: no added context")
                    result, usage = _run_condition(llm, target_text, None)
                else:
                    tracker.set_stage("condition_b", message=f"repeat {repeat}: {condition_b_label}")
                    result, usage = _run_condition(llm, target_text, condition_b_context)
                outputs[condition] = {"result": result, "usage": usage}
            a, usage_a = outputs["condition_a"]["result"], outputs["condition_a"]["usage"]
            b, usage_b = outputs["condition_b"]["result"], outputs["condition_b"]["usage"]
            score_a, score_b = _score(a, target_text, gold), _score(b, target_text, gold)
            records.append({
                "repeat": repeat,
                "condition_a": {"output": a.model_dump(mode="json"), "score": score_a, "usage": usage_a},
                "condition_b": {"output": b.model_dump(mode="json"), "score": score_b, "usage": usage_b},
                "delta_b_minus_a": round(score_b["total"] - score_a["total"], 2),
            })
            tracker.set_usage(
                llm_calls=2 * len(records),
                estimated_cost_usd=sum(
                    item[condition]["usage"].get("estimated_usd", 0.0)
                    for item in records
                    for condition in ("condition_a", "condition_b")
                ),
            )
            _write_json(out / f"condition_a_no_example_r{repeat}.json", records[-1]["condition_a"])
            condition_b_file_label = "with_example" if args.condition_b == "example" else "runtime_skill"
            _write_json(out / f"condition_b_{condition_b_file_label}_r{repeat}.json",
                        records[-1]["condition_b"])

        tracker.set_stage("score", message="aggregating metrics")
        deltas = [x["delta_b_minus_a"] for x in records]
        aggregate = {
            "experiment": f"same target paper; no added context vs {condition_b_label}",
            "model": MODEL, "temperature": 0, "repeats": args.repeats,
            "target_paper": str(TARGET_PAPER.relative_to(ROOT)),
            "condition_b": condition_b_label,
            "condition_b_sha256": condition_b_sha256,
            "records": records,
            "mean_score_a": round(statistics.mean(x["condition_a"]["score"]["total"] for x in records), 2),
            "mean_score_b": round(statistics.mean(x["condition_b"]["score"]["total"] for x in records), 2),
            "mean_delta_b_minus_a": round(statistics.mean(deltas), 2),
        }
        aggregate["acceptance"] = _acceptance(records)
        _write_json(out / "scores.json", aggregate)

        tracker.set_stage("report", message="writing comparison report")
        report = [
            "# Runtime-context A/B result", "",
            f"- Model: `{MODEL}`", f"- Repeats: {args.repeats}",
            f"- Condition B: **{condition_b_label}**",
            f"- Condition B SHA-256: `{condition_b_sha256}`",
            f"- Mean A (no added context): **{aggregate['mean_score_a']}**",
            f"- Mean B: **{aggregate['mean_score_b']}**",
            f"- Mean delta B-A: **{aggregate['mean_delta_b_minus_a']:+.2f}**", "",
            f"- Acceptance verdict: **{aggregate['acceptance']['verdict']}**",
            f"- Paired wins/ties/losses: **{aggregate['acceptance']['paired_wins']}/"
            f"{aggregate['acceptance']['paired_ties']}/{aggregate['acceptance']['paired_losses']}**",
            f"- Delta sample SD: **{aggregate['acceptance']['delta_sample_stdev']}**", "",
            f"- Total estimated model cost: **${sum(item[condition]['usage'].get('estimated_usd', 0.0) for item in records for condition in ('condition_a', 'condition_b')):.4f}**", "",
            "A positive delta supports condition B only when safety checks do not regress. "
            "One repeat is only a smoke result.", "",
        ]
        for record in records:
            report += [
                f"## Repeat {record['repeat']}", "",
                f"- A: {record['condition_a']['score']['total']}",
                f"- B: {record['condition_b']['score']['total']}",
                f"- Delta: {record['delta_b_minus_a']:+.2f}", "",
            ]
        (out / "comparison.md").write_text("\n".join(report), encoding="utf-8")
        tracker.finish("completed", f"mean delta={aggregate['mean_delta_b_minus_a']:+.2f}")
        print(json.dumps({k: aggregate[k] for k in ("mean_score_a", "mean_score_b", "mean_delta_b_minus_a")}, indent=2))
        print(f"Output: {out}")
        return 0
    except Exception as exc:
        tracker.add_failure(f"{type(exc).__name__}: {exc}")
        tracker.finish("failed", str(exc))
        raise


if __name__ == "__main__":
    raise SystemExit(main())
