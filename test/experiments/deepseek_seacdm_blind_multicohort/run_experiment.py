"""Frozen unseen multi-accession SEA-CDM blind test for DeepSeek V4 Pro.

The case and gates in this file were fixed before the first model call.  GSE197045 is the
myonuclear RRBS accession in a paper that also reports RNA-seq under GSE198652.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.util
import itertools
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


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


GENERAL = _load_module(
    "seacdm_generalization_helpers_blind",
    ROOT / "test" / "experiments" / "deepseek_seacdm_generalization" / "run_experiment.py",
)
H = GENERAL.H
PRICE = GENERAL.PRICE
CASE = {
    "study_id": "GSE197045",
    "organism": "Mouse",
    "paper_path": ROOT / "data" / "papers" / "ca50a66730bea8f1f02557af9bd39d7e338e7a4e.txt",
    "metadata_path": ROOT / "data" / "GSE197045" / "GSE197045_metadata.csv",
    "paper_only_accession": "GSE198652",
    "required_design_term_groups": (
        ("power", "progressive weighted wheel"),
        ("8 wk", "8 week"),
        ("bisulfite", "rrbs"),
        ("soleus", "myonuclei"),
        ("mus musculus", "mouse", "mice"),
    ),
    "excluded_design_terms": (
        "gse198652", "rna-seq", "rna sequencing", "transcriptomic profiling",
    ),
    "expected_structural_counts": {"subject": 1, "sample": 6, "groups": 2, "assay": 1},
    "description": (
        "Unseen multi-accession paper: target old-mouse soleus myonuclear RRBS; "
        "paper also deposits RNA-seq as GSE198652"
    ),
}
CHECK_WEIGHTS = {
    "completed": 10,
    "schema_conformant": 10,
    "required_tables_present": 10,
    "fk_integrity": 10,
    "no_group_errors": 5,
    "provenance_measured": 5,
    "provenance_verified_at_least_90pct": 15,
    "study_id_preserved": 5,
    "geo_scope_consistent": 15,
    "structural_counts_match_metadata": 10,
    "no_unsupported_geo_accession": 5,
}


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def _deepseek_environment():
    keys = ("BIOAGENT_LLM_PROVIDER", "BIOAGENT_SEACDM_LLM_PROVIDER",
            "BIOAGENT_LLM_MODEL", "BIOAGENT_STRUCTURED_MAX_TOKENS")
    old = {key: os.environ.get(key) for key in keys}
    os.environ["BIOAGENT_LLM_PROVIDER"] = "deepseek"
    os.environ["BIOAGENT_SEACDM_LLM_PROVIDER"] = "deepseek"
    os.environ.pop("BIOAGENT_LLM_MODEL", None)
    os.environ["BIOAGENT_STRUCTURED_MAX_TOKENS"] = "16384"
    try:
        yield
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _canon_hash(value) -> str:
    blob = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _score(checks: dict[str, bool]) -> int:
    return sum(weight for name, weight in CHECK_WEIGHTS.items() if checks.get(name))


def _scope_audit(tables: dict) -> dict:
    design_text = GENERAL._table_text(tables, ("experiment", "interventions", "assay"))
    required_hits = {
        " | ".join(group): [term for term in group if term.lower() in design_text]
        for group in CASE["required_design_term_groups"]
    }
    excluded_hits = sorted({
        term for term in CASE["excluded_design_terms"] if term.lower() in design_text
    })
    design_accessions = sorted(set(re.findall(r"\bGSE\d+\b", design_text, re.I)))
    foreign_accessions = [
        item.upper() for item in design_accessions if item.upper() != CASE["study_id"]
    ]
    return {
        "policy": "target_geo_accession",
        "required_hits": required_hits,
        "excluded_hits": excluded_hits,
        "foreign_design_accessions": foreign_accessions,
        "passed": all(required_hits.values()) and not excluded_hits and not foreign_accessions,
    }


def _run_one(repeat: int, out: Path) -> dict:
    paper_text = CASE["paper_path"].read_text(encoding="utf-8", errors="ignore")
    source_accessions = {item.upper() for item in re.findall(r"\bGSE\d+\b", paper_text, re.I)}
    run_dir = out / f"r{repeat}"
    run_dir.mkdir(parents=True, exist_ok=True)
    usage, report = [], {}
    tables = {name: [] for name in SEA_TABLES}
    error = ""
    started = _utc_now()
    t0 = time.perf_counter()
    try:
        with _deepseek_environment():
            tables = extract_tables_from_text(
                CASE["study_id"], paper_text, CASE["organism"], verify=True, report=report,
                metadata_csv=str(CASE["metadata_path"]), lean=True, usage=usage,
                strategy="staged", max_stage_retries=1,
            )
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    elapsed = round(time.perf_counter() - t0, 3)

    schema_errors = H._schema_errors(tables)
    fk_errors = H._fk_errors(tables)
    row_counts = {name: len(rows) for name, rows in tables.items()}
    required = all(row_counts.get(name, 0) > 0 for name in (
        "study", "experiment", "subject", "sample", "groups", "interventions",
        "exercise", "assay", "documentation",
    ))
    n_total = int(report.get("n_total") or 0)
    n_verified = int(report.get("n_verified") or 0)
    provenance_rate = n_verified / n_total if n_total else 0.0
    all_text = H._all_text(tables, report)
    output_accessions = set(re.findall(r"\bGSE\d+\b", all_text, flags=re.I))
    unsupported = sorted(
        item.upper() for item in output_accessions
        if item.upper() not in source_accessions | {CASE["study_id"]}
    )
    scope = _scope_audit(tables)
    structural_counts_match = all(
        row_counts.get(name) == expected
        for name, expected in CASE["expected_structural_counts"].items()
    )
    checks = {
        "completed": not error,
        "schema_conformant": not schema_errors,
        "required_tables_present": required,
        "fk_integrity": not fk_errors,
        "no_group_errors": not report.get("group_errors"),
        "provenance_measured": n_total > 0,
        "provenance_verified_at_least_90pct": provenance_rate >= 0.90,
        "study_id_preserved": bool(tables.get("study")) and
                              tables["study"][0].get("study_id") == CASE["study_id"],
        "geo_scope_consistent": scope["passed"],
        "structural_counts_match_metadata": structural_counts_match,
        "no_unsupported_geo_accession": not unsupported,
    }
    blocking_names = tuple(name for name in CHECK_WEIGHTS if name != "provenance_measured")
    blocking = [name for name in blocking_names if not checks[name]]
    input_tokens = sum(int(row.get("input_tokens") or 0) for row in usage)
    output_tokens = sum(int(row.get("output_tokens") or 0) for row in usage)
    cost = (input_tokens * PRICE["input"] + output_tokens * PRICE["output"]) / 1_000_000
    semantics = GENERAL._semantic_sets(tables, report)
    structural = {name: tables.get(name, []) for name in ("subject", "sample", "groups", "assay")}

    tables_path = run_dir / "seacdm_tables.json"
    provenance_path = run_dir / "seacdm_provenance.json"
    decision_trace_path = run_dir / "decision_trace.json"
    tables_path.write_text(json.dumps(tables, indent=2, ensure_ascii=False), encoding="utf-8")
    provenance_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    decision_trace_path.write_text(json.dumps({
        "study_id": CASE["study_id"], "repeat": repeat,
        "attempts": report.get("decision_trace", []),
        "stage_errors": report.get("stage_errors", {}), "usage": usage,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    record = {
        "repeat": repeat, "study_id": CASE["study_id"], "started_at": started,
        "finished_at": _utc_now(), "elapsed_seconds": elapsed, "error": error,
        "checks": checks, "score": _score(checks), "coverage": 100.0,
        "blocking": blocking, "schema_errors": schema_errors, "fk_errors": fk_errors,
        "row_counts": row_counts, "scope_audit": scope,
        "provenance_total": n_total, "provenance_verified": n_verified,
        "provenance_rate": round(provenance_rate, 4),
        "unsupported_accessions": unsupported,
        "usage": {"calls": len(usage), "input_tokens": input_tokens,
                  "output_tokens": output_tokens},
        "estimated_cost_usd": round(cost, 8),
        "semantic_sets": {name: sorted(values) for name, values in semantics.items()},
        "structural_hash": _canon_hash(structural), "whole_output_hash": _canon_hash(tables),
        "tables_path": str(tables_path.resolve()),
        "provenance_path": str(provenance_path.resolve()),
        "decision_trace_path": str(decision_trace_path.resolve()),
    }
    trace_path = run_dir / "trace.json"
    record["trace_path"] = str(trace_path.resolve())
    trace_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return record


def _pairwise_jaccard(sets: list[set[str]]) -> float:
    pairs = [H._jaccard(a, b) for a, b in itertools.combinations(sets, 2)]
    return statistics.mean(pairs) if pairs else 1.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()
    if args.repeats != 3:
        raise SystemExit("Blind LLM validation requires exactly three repeats")
    for key in ("paper_path", "metadata_path"):
        if not CASE[key].is_file():
            raise SystemExit(f"Frozen input missing: {CASE[key]}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(args.output_dir).resolve() if args.output_dir else (
        ROOT / "output" / f"deepseek_seacdm_blind_multicohort_{stamp}"
    )
    out.mkdir(parents=True, exist_ok=True)
    tracker = RunStatusTracker(
        str(out / "run_status.json"), run_id=out.name,
        profile="deepseek_seacdm_blind_multicohort",
        stages=["freeze", "extract", "stability", "report"],
    )
    tracker.start("DeepSeek staged SEA-CDM unseen multi-accession blind test")
    tracker.set_stage("freeze", message="GSE197045; rules fixed before first model call")
    frozen = {
        **{key: str(value.resolve()) if isinstance(value, Path) else value
           for key, value in CASE.items()},
        "paper_sha256": file_sha256(str(CASE["paper_path"])),
        "metadata_sha256": file_sha256(str(CASE["metadata_path"])),
        "check_weights": CHECK_WEIGHTS,
        "frozen_at": _utc_now(),
    }
    (out / "frozen_case.json").write_text(
        json.dumps(frozen, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    tracker.set_stage("extract", message="DeepSeek V4 Pro x3; temperature=0")
    records = []
    for repeat in range(1, 4):
        print(f"[{repeat}/3] {CASE['study_id']} extracting...", flush=True)
        records.append(_run_one(repeat, out))

    tracker.set_stage("stability", message="scope, structure, semantic stability")
    passed = [row for row in records if not row["blocking"]]
    stability = {
        "runs": 3,
        "passed": len(passed),
        "mean_score": round(statistics.mean(row["score"] for row in records), 2),
        "mean_provenance_rate": round(
            statistics.mean(row["provenance_rate"] for row in records), 4
        ),
        "median_latency_seconds": round(
            statistics.median(row["elapsed_seconds"] for row in records), 3
        ),
        "cost_per_run_usd": round(
            statistics.mean(row["estimated_cost_usd"] for row in records), 6
        ),
        "structural_identical": len({row["structural_hash"] for row in records}) == 1,
        "intervention_jaccard": round(_pairwise_jaccard([
            set(row["semantic_sets"]["intervention"]) for row in records
        ]), 4),
        "finding_jaccard": round(_pairwise_jaccard([
            set(row["semantic_sets"]["finding"]) for row in records
        ]), 4),
    }
    blocking = sorted({f"r{row['repeat']}:{item}"
                       for row in records for item in row["blocking"]})
    acceptance = {
        "all_three_runs_pass": len(passed) == 3,
        "zero_blocking_findings": not blocking,
        "provenance_at_least_90pct": stability["mean_provenance_rate"] >= 0.90,
        "structure_stable": stability["structural_identical"],
        "cost_at_most_30pct_of_sonnet": stability["cost_per_run_usd"] <= 0.253341 * 0.30,
    }
    verdict = "blind_case_pass" if all(acceptance.values()) else "blind_case_fail"
    pd.DataFrame([{
        "accession": row["study_id"], "repeat": row["repeat"],
        "status": "completed" if not row["blocking"] else "failed",
        "score": row["score"], "coverage": row["coverage"],
        "provenance_rate": row["provenance_rate"],
        "scope_consistent": row["checks"]["geo_scope_consistent"],
        "excluded_hits": "; ".join(row["scope_audit"]["excluded_hits"]),
        "foreign_design_accessions": "; ".join(
            row["scope_audit"]["foreign_design_accessions"]
        ),
        "elapsed_seconds": row["elapsed_seconds"],
        "estimated_cost_usd": row["estimated_cost_usd"],
        "artifact": row["tables_path"], "error": row["error"],
    } for row in records]).to_csv(out / "summary.csv", index=False)
    report = {
        "schema_version": "1.0", "evaluation_unit": "unseen multi-accession SEA-CDM case",
        "verdict": verdict, "score": stability["mean_score"], "coverage": 100.0,
        "blocking_findings": blocking, "case": frozen, "repeats": 3,
        "stability": stability, "acceptance": acceptance, "records": records,
        "unmeasured_checks": [
            "Manual domain-expert adjudication of every material and reported finding",
            "A second unseen multi-accession paper",
        ],
    }
    report_path = out / "blind_multicohort_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# DeepSeek SEA-CDM unseen multi-accession blind test", "",
        f"- Verdict: **{verdict}**", f"- Score: **{stability['mean_score']}/100**",
        "- Coverage: **100% of frozen case gates**",
        f"- Blocking findings: **{len(blocking)}**", "",
        "| Metric | GSE197045 |", "|---|---:|",
        f"| Runs passed | {stability['passed']}/3 |",
        f"| Mean provenance | {stability['mean_provenance_rate']:.1%} |",
        f"| Structural identical | {stability['structural_identical']} |",
        f"| Intervention Jaccard | {stability['intervention_jaccard']:.3f} |",
        f"| Median latency | {stability['median_latency_seconds']} s |",
        f"| Cost/run | ${stability['cost_per_run_usd']} |", "",
        "## Frozen acceptance gates", "",
    ]
    lines.extend(f"- {name}: **{'pass' if value else 'fail'}**"
                 for name, value in acceptance.items())
    lines.extend(["", "## Unmeasured", ""])
    lines.extend(f"- {item}" for item in report["unmeasured_checks"])
    (out / "blind_multicohort_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    (out / "workflow.log").write_text("\n".join([
        "DeepSeek staged SEA-CDM unseen multi-accession blind test",
        "case=GSE197045", "paper_only_accession=GSE198652",
        "model=deepseek-v4-pro", "temperature=0", "strategy=staged",
        "repeats=3", "rules_frozen_before_calls=true", f"verdict={verdict}",
    ]) + "\n", encoding="utf-8")

    evidence = EvidenceRecorder(out.name, subject_id=CASE["study_id"])
    paper_source = evidence.add_source(
        "paper", "PMC9233305 source paper", uri=str(CASE["paper_path"].resolve())
    )
    evidence.bundle.sources[-1].sha256 = file_sha256(str(CASE["paper_path"]))
    metadata_source = evidence.add_source(
        "metadata", "GSE197045 GEO metadata", uri=str(CASE["metadata_path"].resolve())
    )
    evidence.bundle.sources[-1].sha256 = file_sha256(str(CASE["metadata_path"]))
    for row in records:
        decision = evidence.add_decision(
            "blind_multicohort_seacdm",
            {"study_id": row["study_id"], "repeat": row["repeat"]},
            reason="Frozen unseen multi-accession scope test", method="llm",
            evidence_ids=[paper_source, metadata_source],
            details={"score": row["score"], "checks": row["checks"]},
        )
        for key, kind in (("tables_path", "SEA-CDM tables"),
                          ("provenance_path", "provenance audit"),
                          ("decision_trace_path", "decision trace"),
                          ("trace_path", "run trace")):
            evidence.add_artifact(row[key], kind, produced_by=decision,
                                  evidence_ids=[paper_source, metadata_source])
    for path, kind in ((out / "frozen_case.json", "frozen case manifest"),
                       (out / "summary.csv", "evaluation summary"),
                       (report_path, "evaluation report"),
                       (out / "workflow.log", "workflow log")):
        evidence.add_artifact(str(path), kind)
    evidence.finish("completed")
    evidence.save(str(out / "evidence.json"))

    tracker.set_stage("report", message=verdict)
    tracker.set_usage(llm_calls=sum(row["usage"]["calls"] for row in records),
                      estimated_cost_usd=sum(row["estimated_cost_usd"] for row in records))
    for item in blocking:
        tracker.add_warning(item)
    tracker.finish("completed", verdict)
    print(json.dumps({
        "verdict": verdict, "stability": stability, "acceptance": acceptance,
        "output_dir": str(out.resolve()),
    }, indent=2, ensure_ascii=False))
    return 0 if verdict == "blind_case_pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
