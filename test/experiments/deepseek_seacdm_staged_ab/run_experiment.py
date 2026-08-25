"""Paired DeepSeek SEA-CDM process A/B: single-call 4K vs staged 16K.

Both conditions use the same DeepSeek V4 Pro model, cached paper, metadata, temperature,
and deterministic scorer. Execution order alternates across three repeats.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import statistics
import sys
import time

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.evidence import EvidenceRecorder, file_sha256  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402
from tools.sea_cdm_schema import SEA_TABLES  # noqa: E402
from tools.seacdm_tools import extract_tables_from_text  # noqa: E402


def _load_baseline_helpers():
    path = ROOT / "test" / "experiments" / "model_seacdm_ab" / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("seacdm_ab_helpers", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


H = _load_baseline_helpers()
STUDY_ID = H.STUDY_ID
ORGANISM = H.ORGANISM
PAPER_PATH = H.PAPER_PATH
METADATA_PATH = H.METADATA_PATH
PAPER_URL = H.PAPER_URL
MAX_CHARS = H.MAX_CHARS
PRICE = H.PRICES["deepseek"]
VARIANTS = {
    "single_4k": {"strategy": "single", "max_tokens": "4096"},
    "staged_16k": {"strategy": "staged", "max_tokens": "16384"},
}
SONNET_REFERENCE = (
    ROOT / "output" / "model_seacdm_ab_20260817_221240" / "anthropic" / "r2"
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def _variant_environment(variant: str):
    keys = (
        "BIOAGENT_LLM_PROVIDER", "BIOAGENT_SEACDM_LLM_PROVIDER",
        "BIOAGENT_LLM_MODEL", "BIOAGENT_STRUCTURED_MAX_TOKENS",
    )
    old = {key: os.environ.get(key) for key in keys}
    os.environ["BIOAGENT_LLM_PROVIDER"] = "deepseek"
    os.environ["BIOAGENT_SEACDM_LLM_PROVIDER"] = "deepseek"
    os.environ.pop("BIOAGENT_LLM_MODEL", None)
    os.environ["BIOAGENT_STRUCTURED_MAX_TOKENS"] = VARIANTS[variant]["max_tokens"]
    try:
        yield
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _run_one(variant: str, repeat: int, paper_text: str, source_accessions: set[str],
             run_dir: Path) -> dict:
    run_dir.mkdir(parents=True, exist_ok=True)
    usage, report = [], {}
    tables = {name: [] for name in SEA_TABLES}
    error = ""
    started = _utc_now()
    t0 = time.perf_counter()
    try:
        with _variant_environment(variant):
            tables = extract_tables_from_text(
                STUDY_ID, paper_text, ORGANISM, verify=True, report=report,
                metadata_csv=str(METADATA_PATH), lean=True, usage=usage,
                strategy=VARIANTS[variant]["strategy"], max_stage_retries=1,
            )
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    elapsed = round(time.perf_counter() - t0, 3)

    schema_errors = H._schema_errors(tables)
    fk_errors = H._fk_errors(tables)
    row_counts = {name: len(rows) for name, rows in tables.items()}
    required = all(row_counts.get(name, 0) > 0 for name in (
        "study", "experiment", "subject", "sample", "groups", "assay", "documentation"
    ))
    n_total = int(report.get("n_total") or 0)
    n_verified = int(report.get("n_verified") or 0)
    provenance_rate = n_verified / n_total if n_total else 0.0
    text = H._all_text(tables, report)
    output_accessions = set(re.findall(r"\bGSE\d+\b", text, flags=re.I))
    unsupported = sorted(item.upper() for item in output_accessions
                         if item.upper() not in source_accessions)
    checks = {
        "completed": not error,
        "schema_conformant": not schema_errors,
        "required_tables_present": required,
        "fk_integrity": not fk_errors,
        "no_group_errors": not report.get("group_errors"),
        "provenance_measured": n_total > 0,
        "provenance_verified_at_least_90pct": provenance_rate >= 0.90,
        "study_id_preserved": bool(tables.get("study")) and
                              tables["study"][0].get("study_id") == STUDY_ID,
        "exercise_fact_recovered": "exercise" in text,
        "acvr1c_fact_recovered": "acvr1c" in text,
        "no_unsupported_geo_accession": not unsupported,
    }
    blocking = [name for name in (
        "completed", "schema_conformant", "required_tables_present", "fk_integrity",
        "no_group_errors", "study_id_preserved", "no_unsupported_geo_accession",
    ) if not checks[name]]
    input_tokens = sum(int(row.get("input_tokens") or 0) for row in usage)
    output_tokens = sum(int(row.get("output_tokens") or 0) for row in usage)
    cost = (input_tokens * PRICE["input"] + output_tokens * PRICE["output"]) / 1_000_000
    semantics = H._semantic_sets(tables, report)

    tables_path = run_dir / "seacdm_tables.json"
    provenance_path = run_dir / "seacdm_provenance.json"
    decision_trace_path = run_dir / "decision_trace.json"
    tables_path.write_text(json.dumps(tables, indent=2, ensure_ascii=False), encoding="utf-8")
    provenance_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    decision_trace_path.write_text(json.dumps({
        "variant": variant,
        "extraction_mode": report.get("extraction_mode"),
        "stage_errors": report.get("stage_errors", {}),
        "attempts": report.get("decision_trace", []),
        "usage": usage,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    record = {
        "variant": variant, "repeat": repeat, "study_id": STUDY_ID,
        "started_at": started, "finished_at": _utc_now(), "elapsed_seconds": elapsed,
        "error": error, "checks": checks, "score": H._score(checks), "coverage": 100.0,
        "blocking": blocking, "schema_errors": schema_errors, "fk_errors": fk_errors,
        "row_counts": row_counts, "provenance_total": n_total,
        "provenance_verified": n_verified, "provenance_rate": round(provenance_rate, 4),
        "unsupported_accessions": unsupported,
        "usage": {"calls": len(usage), "input_tokens": input_tokens,
                  "output_tokens": output_tokens},
        "estimated_cost_usd": round(cost, 8),
        "semantic_sets": {name: sorted(values) for name, values in semantics.items()},
        "tables_path": str(tables_path.resolve()),
        "provenance_path": str(provenance_path.resolve()),
        "decision_trace_path": str(decision_trace_path.resolve()),
    }
    trace_path = run_dir / "trace.json"
    record["trace_path"] = str(trace_path.resolve())
    trace_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return record


def _aggregate(records: list[dict], variant: str) -> dict:
    rows = [row for row in records if row["variant"] == variant]
    passed = [row for row in rows if not row["blocking"] and row["score"] >= 85]
    return {
        "runs": len(rows), "passed": len(passed),
        "mean_score": round(statistics.mean(row["score"] for row in rows), 2),
        "median_latency_seconds": round(statistics.median(row["elapsed_seconds"] for row in rows), 3),
        "mean_provenance_rate": round(statistics.mean(row["provenance_rate"] for row in rows), 4),
        "total_cost_usd": round(sum(row["estimated_cost_usd"] for row in rows), 6),
        "cost_per_pass_usd": round(sum(row["estimated_cost_usd"] for row in rows) / len(passed), 6)
        if passed else None,
        "llm_calls": sum(row["usage"]["calls"] for row in rows),
    }


def _reference_sets():
    tables = json.loads((SONNET_REFERENCE / "seacdm_tables.json").read_text(encoding="utf-8"))
    report = json.loads((SONNET_REFERENCE / "seacdm_provenance.json").read_text(encoding="utf-8"))
    return H._semantic_sets(tables, report)


def _overlap_similarity(left: str, right: str) -> float:
    """Token overlap coefficient, robust to one model returning a more specific label."""
    a = set(re.findall(r"[a-z0-9]+", left.lower()))
    b = set(re.findall(r"[a-z0-9]+", right.lower()))
    return len(a & b) / min(len(a), len(b)) if a and b else 0.0


def _reference_recall(got: set[str], expected: set[str], threshold: float = 0.60) -> float:
    if not expected:
        return 1.0
    matched = sum(
        max((_overlap_similarity(item, candidate) for candidate in got), default=0.0) >= threshold
        for item in expected
    )
    return matched / len(expected)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()
    if args.repeats != 3:
        raise SystemExit("This LLM-dependent A/B requires exactly three repeats per condition")
    for path in (PAPER_PATH, METADATA_PATH, SONNET_REFERENCE / "seacdm_tables.json"):
        if not path.is_file():
            raise SystemExit(f"Frozen input/reference missing: {path}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(args.output_dir).resolve() if args.output_dir else (
        ROOT / "output" / f"deepseek_seacdm_staged_ab_{stamp}"
    )
    out.mkdir(parents=True, exist_ok=True)
    tracker = RunStatusTracker(
        str(out / "run_status.json"), run_id=out.name,
        profile="paired_deepseek_seacdm_process_ab",
        stages=["freeze_inputs", "extract", "compare", "audit"],
    )
    tracker.start("DeepSeek single-call vs staged SEA-CDM A/B")
    tracker.set_stage("freeze_inputs", message="cached paper, GEO metadata, Sonnet reference")
    paper_text = PAPER_PATH.read_text(encoding="utf-8", errors="ignore")[:MAX_CHARS]
    source_accessions = {item.upper() for item in re.findall(r"\bGSE\d+\b", paper_text, re.I)}

    records = []
    tracker.set_stage("extract", message="two process variants x three repeats")
    for repeat in range(1, args.repeats + 1):
        order = ("staged_16k", "single_4k") if repeat % 2 else ("single_4k", "staged_16k")
        for variant in order:
            print(f"[{repeat}/3] {variant}: extracting...", flush=True)
            records.append(_run_one(
                variant, repeat, paper_text, source_accessions, out / variant / f"r{repeat}"
            ))

    tracker.set_stage("compare", message="quality gates, reference recall, cost, latency")
    aggregate = {variant: _aggregate(records, variant) for variant in VARIANTS}
    reference = _reference_sets()
    staged_rows = [row for row in records if row["variant"] == "staged_16k"]
    reference_similarity = {
        key: round(statistics.mean(
            H._jaccard(set(row["semantic_sets"][key]), reference[key]) for row in staged_rows
        ), 4)
        for key in ("material", "intervention", "finding")
    }
    reference_recall = {
        key: round(statistics.mean(
            _reference_recall(set(row["semantic_sets"][key]), reference[key])
            for row in staged_rows
        ), 4)
        for key in ("material", "intervention", "finding")
    }
    staged = aggregate["staged_16k"]
    acceptance = {
        "staged_three_of_three_pass": staged["passed"] == 3,
        "staged_zero_blocking": all(not row["blocking"] for row in staged_rows),
        "staged_provenance_at_least_90pct": staged["mean_provenance_rate"] >= 0.90,
        "material_reference_recall_at_least_70pct": reference_recall["material"] >= 0.70,
        "finding_reference_recall_at_least_70pct": reference_recall["finding"] >= 0.70,
        "cost_per_pass_at_most_30pct_of_sonnet":
            staged["cost_per_pass_usd"] is not None and staged["cost_per_pass_usd"] <= 0.253341 * 0.30,
    }
    verdict = "staged_deepseek_candidate" if all(acceptance.values()) else "retain_sonnet_for_seacdm"
    blocking = sorted({f"{row['variant']}:r{row['repeat']}:{item}"
                       for row in records for item in row["blocking"]})

    pd.DataFrame([{
        "accession": STUDY_ID, "variant": row["variant"], "repeat": row["repeat"],
        "status": "completed" if not row["blocking"] else "failed",
        "score": row["score"], "coverage": row["coverage"],
        "provenance_rate": row["provenance_rate"],
        "material_rows": row["row_counts"].get("material", 0),
        "reported_findings": len(row["semantic_sets"]["finding"]),
        "llm_calls": row["usage"]["calls"], "elapsed_seconds": row["elapsed_seconds"],
        "estimated_cost_usd": row["estimated_cost_usd"], "artifact": row["tables_path"],
        "error": row["error"],
    } for row in records]).to_csv(out / "summary.csv", index=False)

    report = {
        "schema_version": "1.0", "evaluation_unit": "DeepSeek SEA-CDM process A/B",
        "verdict": verdict, "coverage": 100.0, "blocking_findings": blocking,
        "study_id": STUDY_ID, "paper_url": PAPER_URL,
        "paper_text_path": str(PAPER_PATH.resolve()),
        "paper_text_sha256": file_sha256(str(PAPER_PATH)),
        "metadata_path": str(METADATA_PATH.resolve()),
        "metadata_sha256": file_sha256(str(METADATA_PATH)),
        "variants": VARIANTS, "repeats": 3, "aggregate": aggregate,
        "reference_similarity": reference_similarity, "reference_recall": reference_recall,
        "acceptance": acceptance,
        "sonnet_reference": str(SONNET_REFERENCE.resolve()), "records": records,
        "unmeasured_checks": [
            "Manual domain-expert adjudication of every field",
            "Generalization to routine and adversarial papers",
            "Ablation separating output-budget gain from staged-flow gain",
        ],
    }
    (out / "deepseek_seacdm_staged_ab.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    lines = [
        "# DeepSeek SEA-CDM staged-process A/B", "", f"- Verdict: **{verdict}**",
        "- Coverage: **100%**", f"- Blocking findings: **{len(blocking)}**", "",
        "| Metric | Single 4K | Staged 16K |", "|---|---:|---:|",
        f"| Runs passed | {aggregate['single_4k']['passed']}/3 | {staged['passed']}/3 |",
        f"| Mean score | {aggregate['single_4k']['mean_score']} | {staged['mean_score']} |",
        f"| Provenance | {aggregate['single_4k']['mean_provenance_rate']:.1%} | {staged['mean_provenance_rate']:.1%} |",
        f"| Median latency (s) | {aggregate['single_4k']['median_latency_seconds']} | {staged['median_latency_seconds']} |",
        f"| Cost/pass (USD) | {aggregate['single_4k']['cost_per_pass_usd']} | {staged['cost_per_pass_usd']} |",
        "", "## Staged vs Sonnet semantic similarity", "",
        f"- Material Jaccard: **{reference_similarity['material']:.3f}**",
        f"- Intervention Jaccard: **{reference_similarity['intervention']:.3f}**",
        f"- Finding Jaccard: **{reference_similarity['finding']:.3f}**",
        f"- Material fuzzy reference recall: **{reference_recall['material']:.1%}**",
        f"- Finding fuzzy reference recall: **{reference_recall['finding']:.1%}**",
        "", "## Acceptance gates", "",
    ]
    lines.extend(f"- {name}: **{'pass' if value else 'fail'}**" for name, value in acceptance.items())
    lines.extend(["", "## Unmeasured checks", ""])
    lines.extend(f"- {item}" for item in report["unmeasured_checks"])
    (out / "deepseek_seacdm_staged_ab.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "workflow.log").write_text("\n".join([
        "DeepSeek SEA-CDM process A/B", f"paper={PAPER_PATH.resolve()}",
        f"paper_sha256={report['paper_text_sha256']}", f"metadata={METADATA_PATH.resolve()}",
        f"metadata_sha256={report['metadata_sha256']}", "model=deepseek-v4-pro",
        "temperature=0", "single=one-call,max_tokens=4096",
        "staged=focused-small-schema,max_tokens=16384,targeted-retry=1",
        "execution_order=alternated", f"verdict={verdict}",
    ]) + "\n", encoding="utf-8")

    evidence = EvidenceRecorder(out.name, subject_id=STUDY_ID)
    paper_source = evidence.add_source("paper", "GSE208615 source paper", uri=PAPER_URL)
    metadata_source = evidence.add_source("metadata", "GSE208615 GEO metadata",
                                          uri=str(METADATA_PATH.resolve()))
    for row in records:
        decision = evidence.add_decision(
            "seacdm_process_ab", {"variant": row["variant"], "repeat": row["repeat"]},
            reason="Paired DeepSeek extraction on frozen inputs", method="llm",
            evidence_ids=[paper_source, metadata_source],
            details={"score": row["score"], "checks": row["checks"]},
        )
        for key, kind in (("tables_path", "SEA-CDM tables"),
                          ("provenance_path", "provenance audit"),
                          ("decision_trace_path", "decision trace"),
                          ("trace_path", "run trace")):
            evidence.add_artifact(row[key], kind, produced_by=decision,
                                  evidence_ids=[paper_source, metadata_source])
    for path, kind in ((out / "summary.csv", "evaluation summary"),
                       (out / "deepseek_seacdm_staged_ab.json", "evaluation report"),
                       (out / "workflow.log", "workflow log")):
        evidence.add_artifact(str(path), kind)
    evidence.finish("completed")
    evidence.save(str(out / "evidence.json"))

    tracker.set_stage("audit", message=verdict)
    tracker.set_usage(llm_calls=sum(row["usage"]["calls"] for row in records),
                      estimated_cost_usd=sum(row["estimated_cost_usd"] for row in records))
    for item in blocking:
        tracker.add_warning(item)
    tracker.finish("completed", verdict)
    print(json.dumps({
        "verdict": verdict, "aggregate": aggregate,
        "reference_similarity": reference_similarity, "reference_recall": reference_recall,
        "acceptance": acceptance,
        "output_dir": str(out.resolve()),
    }, indent=2, ensure_ascii=False))
    return 0 if verdict == "staged_deepseek_candidate" else 1


if __name__ == "__main__":
    raise SystemExit(main())
