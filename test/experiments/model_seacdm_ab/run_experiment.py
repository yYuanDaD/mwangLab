"""Paired Sonnet 4.6 vs DeepSeek V4 Pro SEA-CDM extraction evaluation.

The same cached open-access exercise paper and GEO metadata are used for every
run. Each provider is evaluated three times with alternating execution order.
The scorer is deterministic: schema, FK closure, provenance verification,
critical-fact recovery, stability, cost, and latency are measured from artifacts.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import statistics
import sys
import time
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.determinism_similarity import rouge_l_f1  # noqa: E402
from tools.evidence import EvidenceRecorder, file_sha256  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402
from tools.sea_cdm_schema import SEA_TABLES, csv_columns  # noqa: E402
from tools.seacdm_tools import extract_tables_from_text  # noqa: E402


STUDY_ID = "GSE208615"
ORGANISM = "Mouse"
PAPER_PATH = ROOT / "data" / "papers" / "ce74938ff6bc79920a89e84c09b0c0300e7c634f.txt"
METADATA_PATH = ROOT / "data" / STUDY_ID / f"{STUDY_ID}_metadata.csv"
PAPER_URL = "https://www.nature.com/articles/s41467-024-47996-w"
MAX_CHARS = 100_000
PROVIDERS = ("anthropic", "deepseek")
PRICES = {
    "anthropic": {"input": 3.00, "output": 15.00},
    "deepseek": {"input": 0.435, "output": 0.87},
}
CHECK_WEIGHTS = {
    "completed": 10,
    "schema_conformant": 10,
    "required_tables_present": 10,
    "fk_integrity": 15,
    "no_group_errors": 10,
    "provenance_measured": 5,
    "provenance_verified_at_least_90pct": 15,
    "study_id_preserved": 5,
    "exercise_fact_recovered": 5,
    "acvr1c_fact_recovered": 10,
    "no_unsupported_geo_accession": 5,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def _provider(name: str):
    old_provider = os.environ.get("BIOAGENT_LLM_PROVIDER")
    old_seacdm_provider = os.environ.get("BIOAGENT_SEACDM_LLM_PROVIDER")
    old_model = os.environ.get("BIOAGENT_LLM_MODEL")
    os.environ["BIOAGENT_LLM_PROVIDER"] = name
    os.environ["BIOAGENT_SEACDM_LLM_PROVIDER"] = name
    os.environ.pop("BIOAGENT_LLM_MODEL", None)
    try:
        yield
    finally:
        if old_provider is None:
            os.environ.pop("BIOAGENT_LLM_PROVIDER", None)
        else:
            os.environ["BIOAGENT_LLM_PROVIDER"] = old_provider
        if old_seacdm_provider is None:
            os.environ.pop("BIOAGENT_SEACDM_LLM_PROVIDER", None)
        else:
            os.environ["BIOAGENT_SEACDM_LLM_PROVIDER"] = old_seacdm_provider
        if old_model is None:
            os.environ.pop("BIOAGENT_LLM_MODEL", None)
        else:
            os.environ["BIOAGENT_LLM_MODEL"] = old_model


def _canon_hash(value: Any) -> str:
    blob = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _normalized(value: Any) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", str(value or "").lower()))


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b) if a | b else 1.0


def _mean_pairwise(sets: list[set[str]]) -> float:
    pairs = [_jaccard(a, b) for a, b in itertools.combinations(sets, 2)]
    return statistics.mean(pairs) if pairs else 1.0


def _semantic_sets(tables: dict, report: dict) -> dict[str, set[str]]:
    materials = {
        _normalized(row.get("material_name"))
        for row in tables.get("material", []) if _normalized(row.get("material_name"))
    }
    interventions = {
        _normalized("|".join(str(row.get(k) or "") for k in (
            "intervention_name", "intervention_type", "comments"
        )))
        for row in tables.get("interventions", [])
    }
    interventions.discard("")
    findings = {
        _normalized(f"{row.get('entity')}|{row.get('direction')}")
        for row in report.get("reported_findings", [])
        if _normalized(row.get("entity"))
    }
    return {"material": materials, "intervention": interventions, "finding": findings}


def _schema_errors(tables: dict) -> list[str]:
    errors = []
    if set(tables) != set(SEA_TABLES):
        errors.append(f"table_set:{sorted(set(tables) ^ set(SEA_TABLES))}")
    for table, rows in tables.items():
        if table not in SEA_TABLES:
            continue
        expected = csv_columns(table)
        for index, row in enumerate(rows):
            if list(row) != expected:
                errors.append(f"{table}[{index}]:columns")
    return errors


def _fk_errors(tables: dict) -> list[str]:
    ids = {
        "study": {str(r.get("study_id")) for r in tables.get("study", [])},
        "experiment": {str(r.get("experiment_id")) for r in tables.get("experiment", [])},
        "subject": {str(r.get("subject_id")) for r in tables.get("subject", [])},
        "groups": {str(r.get("group_id")) for r in tables.get("groups", [])},
        "documentation": {str(r.get("documentation_id")) for r in tables.get("documentation", [])},
    }
    errors: list[str] = []

    def require(table: str, field: str, target: str, *, optional: bool = False,
                sentinels: set[str] | None = None) -> None:
        allowed = ids[target] | (sentinels or set())
        for index, row in enumerate(tables.get(table, [])):
            value = row.get(field)
            if optional and (value is None or str(value).strip() == ""):
                continue
            if str(value) not in allowed:
                errors.append(f"{table}[{index}].{field}={value!r}->{target}")

    require("experiment", "study_id", "study")
    require("subject", "experiment_id", "experiment")
    require("subject", "group_id", "groups", optional=True)
    require("sample", "organism_id", "subject", sentinels={"0", "1"})
    require("sample", "group_id", "groups", optional=True)
    require("groups", "study_id", "study")
    require("interventions", "experiment_id", "experiment")
    require("assay", "experiment_id", "experiment")
    require("assay", "documentation_id", "documentation", optional=True)
    require("documentation", "study_id", "study")
    require("study", "documentation_id", "documentation", optional=True)
    return errors


def _all_text(tables: dict, report: dict) -> str:
    return json.dumps({"tables": tables, "reported_findings": report.get("reported_findings", [])},
                      ensure_ascii=False).lower()


def _score(checks: dict[str, bool]) -> int:
    return int(sum(weight for name, weight in CHECK_WEIGHTS.items() if checks.get(name)))


def _run_one(provider: str, repeat: int, paper_text: str, source_accessions: set[str],
             run_dir: Path) -> dict:
    run_dir.mkdir(parents=True, exist_ok=True)
    usage: list[dict] = []
    report: dict = {}
    tables: dict = {name: [] for name in SEA_TABLES}
    started = _utc_now()
    t0 = time.perf_counter()
    error = ""
    try:
        with _provider(provider):
            tables = extract_tables_from_text(
                STUDY_ID, paper_text, ORGANISM, verify=True, report=report,
                metadata_csv=str(METADATA_PATH), lean=True, usage=usage,
            )
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    elapsed = round(time.perf_counter() - t0, 3)

    schema_errors = _schema_errors(tables)
    fk_errors = _fk_errors(tables)
    row_counts = {name: len(rows) for name, rows in tables.items()}
    required = all(row_counts.get(name, 0) > 0 for name in (
        "study", "experiment", "subject", "sample", "groups", "assay", "documentation"
    ))
    n_total = int(report.get("n_total") or 0)
    n_verified = int(report.get("n_verified") or 0)
    provenance_rate = n_verified / n_total if n_total else 0.0
    text = _all_text(tables, report)
    output_accessions = set(re.findall(r"\bGSE\d+\b", text, flags=re.I))
    unsupported_accessions = sorted(a.upper() for a in output_accessions
                                    if a.upper() not in source_accessions)
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
        "no_unsupported_geo_accession": not unsupported_accessions,
    }
    blocking = []
    for name in ("completed", "schema_conformant", "required_tables_present", "fk_integrity",
                 "no_group_errors", "study_id_preserved", "no_unsupported_geo_accession"):
        if not checks[name]:
            blocking.append(name)
    input_tokens = sum(int(item.get("input_tokens") or 0) for item in usage)
    output_tokens = sum(int(item.get("output_tokens") or 0) for item in usage)
    price = PRICES[provider]
    cost = (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000
    semantics = _semantic_sets(tables, report)
    structural = {name: tables.get(name, []) for name in ("subject", "sample", "groups", "assay")}

    tables_path = run_dir / "seacdm_tables.json"
    provenance_path = run_dir / "seacdm_provenance.json"
    tables_path.write_text(json.dumps(tables, indent=2, ensure_ascii=False), encoding="utf-8")
    provenance_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    record = {
        "provider": provider, "repeat": repeat, "study_id": STUDY_ID,
        "started_at": started, "finished_at": _utc_now(), "elapsed_seconds": elapsed,
        "error": error, "checks": checks, "score": _score(checks),
        "coverage": 100.0, "blocking": blocking, "schema_errors": schema_errors,
        "fk_errors": fk_errors, "row_counts": row_counts,
        "provenance_total": n_total, "provenance_verified": n_verified,
        "provenance_rate": round(provenance_rate, 4),
        "unsupported_accessions": unsupported_accessions,
        "usage": {"calls": len(usage), "input_tokens": input_tokens,
                  "output_tokens": output_tokens},
        "estimated_cost_usd": round(cost, 8),
        "semantic_sets": {name: sorted(values) for name, values in semantics.items()},
        "structural_hash": _canon_hash(structural),
        "whole_output_hash": _canon_hash(tables),
        "tables_path": str(tables_path.resolve()),
        "provenance_path": str(provenance_path.resolve()),
    }
    trace_path = run_dir / "trace.json"
    trace_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    record["trace_path"] = str(trace_path.resolve())
    return record


def _rescore_existing_record(original: dict, source_accessions: set[str]) -> dict:
    """Recompute deterministic checks from saved artifacts without another LLM call."""
    tables_path = Path(original["tables_path"])
    provenance_path = Path(original["provenance_path"])
    tables = json.loads(tables_path.read_text(encoding="utf-8"))
    report = json.loads(provenance_path.read_text(encoding="utf-8"))
    schema_errors = _schema_errors(tables)
    fk_errors = _fk_errors(tables)
    row_counts = {name: len(rows) for name, rows in tables.items()}
    required = all(row_counts.get(name, 0) > 0 for name in (
        "study", "experiment", "subject", "sample", "groups", "assay", "documentation"
    ))
    n_total = int(report.get("n_total") or 0)
    n_verified = int(report.get("n_verified") or 0)
    provenance_rate = n_verified / n_total if n_total else 0.0
    text = _all_text(tables, report)
    output_accessions = set(re.findall(r"\bGSE\d+\b", text, flags=re.I))
    unsupported_accessions = sorted(a.upper() for a in output_accessions
                                    if a.upper() not in source_accessions)
    checks = {
        "completed": not original.get("error"),
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
        "no_unsupported_geo_accession": not unsupported_accessions,
    }
    blocking = [name for name in (
        "completed", "schema_conformant", "required_tables_present", "fk_integrity",
        "no_group_errors", "study_id_preserved", "no_unsupported_geo_accession"
    ) if not checks[name]]
    semantics = _semantic_sets(tables, report)
    structural = {name: tables.get(name, []) for name in ("subject", "sample", "groups", "assay")}
    updated = dict(original)
    updated.update({
        "checks": checks, "score": _score(checks), "coverage": 100.0,
        "blocking": blocking, "schema_errors": schema_errors, "fk_errors": fk_errors,
        "row_counts": row_counts, "provenance_total": n_total,
        "provenance_verified": n_verified, "provenance_rate": round(provenance_rate, 4),
        "unsupported_accessions": unsupported_accessions,
        "semantic_sets": {name: sorted(values) for name, values in semantics.items()},
        "structural_hash": _canon_hash(structural), "whole_output_hash": _canon_hash(tables),
    })
    Path(updated["trace_path"]).write_text(
        json.dumps(updated, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return updated


def _provider_stability(records: list[dict], provider: str) -> dict:
    rows = [row for row in records if row["provider"] == provider]
    result = {
        "structural_identical": len({row["structural_hash"] for row in rows}) == 1,
        "whole_output_identical": len({row["whole_output_hash"] for row in rows}) == 1,
    }
    for key in ("material", "intervention", "finding"):
        sets = [set(row["semantic_sets"][key]) for row in rows]
        result[f"mean_{key}_jaccard"] = round(_mean_pairwise(sets), 4)
    study_names = [
        json.loads(Path(row["tables_path"]).read_text(encoding="utf-8"))["study"][0].get("study_name", "")
        for row in rows
    ]
    rouge = [rouge_l_f1(a, b) for a, b in itertools.combinations(study_names, 2)]
    result["mean_study_name_rouge_l"] = round(statistics.mean(rouge), 4) if rouge else 1.0
    return result


def _cross_stability(records: list[dict]) -> dict:
    pairs = []
    for repeat in sorted({row["repeat"] for row in records}):
        pair = {row["provider"]: row for row in records if row["repeat"] == repeat}
        if set(pair) != set(PROVIDERS):
            continue
        item = {"repeat": repeat,
                "structural_identical": pair["anthropic"]["structural_hash"] == pair["deepseek"]["structural_hash"]}
        for key in ("material", "intervention", "finding"):
            item[f"{key}_jaccard"] = round(_jaccard(
                set(pair["anthropic"]["semantic_sets"][key]),
                set(pair["deepseek"]["semantic_sets"][key]),
            ), 4)
        pairs.append(item)
    return {
        "pairs": pairs,
        "structural_identical": bool(pairs) and all(row["structural_identical"] for row in pairs),
        **{
            f"mean_{key}_jaccard": round(statistics.mean(row[f"{key}_jaccard"] for row in pairs), 4)
            if pairs else 0.0
            for key in ("material", "intervention", "finding")
        },
    }


def _aggregate(records: list[dict], provider: str) -> dict:
    rows = [row for row in records if row["provider"] == provider]
    passed = [row for row in rows if not row["blocking"] and row["score"] >= 85]
    return {
        "runs": len(rows), "passed": len(passed), "pass_rate": len(passed) / len(rows) if rows else 0,
        "mean_score": round(statistics.mean(row["score"] for row in rows), 2) if rows else 0,
        "blocking_runs": sum(bool(row["blocking"]) for row in rows),
        "mean_provenance_rate": round(statistics.mean(row["provenance_rate"] for row in rows), 4),
        "median_latency_seconds": round(statistics.median(row["elapsed_seconds"] for row in rows), 3),
        "total_cost_usd": round(sum(row["estimated_cost_usd"] for row in rows), 6),
        "cost_per_pass_usd": round(sum(row["estimated_cost_usd"] for row in rows) / len(passed), 6)
        if passed else None,
        "llm_calls": sum(row["usage"]["calls"] for row in rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--postprocess-existing", default="",
                        help="Rescore and finalize saved model artifacts without new API calls")
    args = parser.parse_args()
    if args.repeats != 3:
        raise SystemExit("SEA-CDM model evaluation requires exactly 3 repeats per provider")
    if not PAPER_PATH.is_file() or not METADATA_PATH.is_file():
        raise SystemExit("Frozen paper text or GEO metadata is missing")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = (Path(args.postprocess_existing).resolve() if args.postprocess_existing else
           Path(args.output_dir).resolve() if args.output_dir else
           ROOT / "output" / f"model_seacdm_ab_{stamp}")
    out.mkdir(parents=True, exist_ok=True)
    tracker = RunStatusTracker(str(out / "run_status.json"), run_id=out.name,
                               profile="paired_model_seacdm_ab",
                               stages=["freeze_inputs", "extract", "stability", "report"])
    tracker.start("paired SEA-CDM extraction A/B")
    tracker.set_stage("freeze_inputs", message="cached PMC11076285 text + GSE208615 metadata")
    paper_text = PAPER_PATH.read_text(encoding="utf-8", errors="ignore")[:MAX_CHARS]
    source_accessions = {item.upper() for item in re.findall(r"\bGSE\d+\b", paper_text, flags=re.I)}

    records = []
    tracker.set_stage("extract", message="2 providers x 3 repeats; alternating order")
    if args.postprocess_existing:
        prior_path = out / "model_seacdm_ab.json"
        if not prior_path.is_file():
            raise SystemExit(f"Missing saved report: {prior_path}")
        prior = json.loads(prior_path.read_text(encoding="utf-8"))
        records = [_rescore_existing_record(row, source_accessions) for row in prior["records"]]
    else:
        for repeat in range(1, args.repeats + 1):
            order = ("deepseek", "anthropic") if repeat % 2 else ("anthropic", "deepseek")
            for provider in order:
                print(f"[{repeat}/{args.repeats}] {provider}: extracting SEA-CDM ...", flush=True)
                records.append(_run_one(provider, repeat, paper_text, source_accessions,
                                        out / provider / f"r{repeat}"))

    tracker.set_stage("stability", message="within-provider and paired cross-provider comparison")
    stability = {
        "within_provider": {provider: _provider_stability(records, provider) for provider in PROVIDERS},
        "cross_provider": _cross_stability(records),
    }
    aggregate = {provider: _aggregate(records, provider) for provider in PROVIDERS}
    sonnet, deepseek = aggregate["anthropic"], aggregate["deepseek"]
    ratio = (deepseek["cost_per_pass_usd"] / sonnet["cost_per_pass_usd"]
             if deepseek["cost_per_pass_usd"] is not None and sonnet["cost_per_pass_usd"] else None)
    blocking = sorted({f"{row['provider']}:r{row['repeat']}:{item}"
                       for row in records for item in row["blocking"]})
    acceptance = {
        "all_six_runs_pass": all(v["pass_rate"] == 1 for v in aggregate.values()),
        "zero_blocking_findings": not blocking,
        "metadata_structures_identical": stability["cross_provider"]["structural_identical"],
        "deepseek_provenance_noninferior_within_5pct":
            deepseek["mean_provenance_rate"] >= sonnet["mean_provenance_rate"] - 0.05,
        "cross_provider_material_jaccard_at_least_50pct":
            stability["cross_provider"]["mean_material_jaccard"] >= 0.50,
        "cross_provider_finding_jaccard_at_least_50pct":
            stability["cross_provider"]["mean_finding_jaccard"] >= 0.50,
        "cost_per_pass_at_most_30pct": ratio is not None and ratio <= 0.30,
    }
    verdict = "deepseek_seacdm_validated" if all(acceptance.values()) else "retain_sonnet_for_seacdm"

    summary_rows = [{
        "accession": STUDY_ID, "provider": row["provider"], "repeat": row["repeat"],
        "status": "completed" if not row["blocking"] else "failed",
        "n_samples": row["row_counts"].get("sample", 0),
        "score": row["score"], "coverage": row["coverage"],
        "provenance_rate": row["provenance_rate"],
        "material_rows": row["row_counts"].get("material", 0),
        "reported_findings": len(row["semantic_sets"]["finding"]),
        "elapsed_seconds": row["elapsed_seconds"],
        "estimated_cost_usd": row["estimated_cost_usd"],
        "artifact": row["tables_path"], "error": row["error"],
    } for row in records]
    summary_path = out / "summary.csv"
    pd.DataFrame(summary_rows).to_csv(summary_path, index=False)
    report = {
        "schema_version": "1.0", "evaluation_unit": "paired SEA-CDM paper extraction",
        "verdict": verdict, "score": {p: aggregate[p]["mean_score"] for p in PROVIDERS},
        "coverage": 100.0, "blocking_findings": blocking, "study_id": STUDY_ID,
        "paper_title": "Specific exercise patterns generate an epigenetic molecular memory window that drives long-term memory formation and identifies ACVR1C as a bidirectional regulator of memory in mice",
        "paper_url": PAPER_URL, "paper_text_path": str(PAPER_PATH.resolve()),
        "paper_text_sha256": file_sha256(str(PAPER_PATH)),
        "metadata_path": str(METADATA_PATH.resolve()),
        "metadata_sha256": file_sha256(str(METADATA_PATH)),
        "repeats": args.repeats, "aggregate": aggregate,
        "cost_ratio_deepseek_vs_sonnet": round(ratio, 4) if ratio is not None else None,
        "total_cost_ratio_deepseek_vs_sonnet": round(
            deepseek["total_cost_usd"] / sonnet["total_cost_usd"], 4
        ) if sonnet["total_cost_usd"] else None,
        "stability": stability, "acceptance": acceptance, "records": records,
        "unmeasured_checks": [
            "Manual domain-expert adjudication of every descriptive field",
            "A second paper without GEO metadata (legacy three-call extraction)",
        ],
    }
    report_path = out / "model_seacdm_ab.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    evaluation_dir = out / "evaluation"
    evaluation_dir.mkdir(exist_ok=True)
    stability_path = evaluation_dir / "model_seacdm_summary.json"
    stability_path.write_text(json.dumps({
        "schema_version": "1.0", "seacdm": stability,
        "judge": {"verdict": "stable" if acceptance["metadata_structures_identical"] else "unstable",
                  "reason": "Deterministic metadata-derived structures are compared by canonical hash."},
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    workflow_path = out / "workflow.log"
    workflow_path.write_text("\n".join([
        "Paired SEA-CDM extraction A/B",
        f"paper={PAPER_PATH.resolve()}", f"paper_sha256={report['paper_text_sha256']}",
        f"metadata={METADATA_PATH.resolve()}", f"metadata_sha256={report['metadata_sha256']}",
        "providers=anthropic:claude-sonnet-4-6,deepseek:deepseek-v4-pro",
        "temperature=0", f"max_chars={MAX_CHARS}", "repeats=3",
        "execution_order=alternated by repeat", "network_steps=disabled",
        f"verdict={verdict}",
    ]) + "\n", encoding="utf-8")

    evidence = EvidenceRecorder(out.name, subject_id=STUDY_ID)
    paper_source = evidence.add_source("paper", report["paper_title"], uri=PAPER_URL,
                                       attributes={"local_path": str(PAPER_PATH.resolve())})
    evidence.bundle.sources[-1].sha256 = report["paper_text_sha256"]
    metadata_source = evidence.add_source("metadata", f"{STUDY_ID} GEO metadata",
                                          uri=str(METADATA_PATH.resolve()))
    evidence.bundle.sources[-1].sha256 = report["metadata_sha256"]
    for row in records:
        decision = evidence.add_decision(
            "seacdm_extraction", {"provider": row["provider"], "repeat": row["repeat"]},
            reason="Paired extraction on frozen paper text and metadata", method="llm",
            evidence_ids=[paper_source, metadata_source],
            details={"score": row["score"], "checks": row["checks"]},
        )
        for path, kind in ((row["tables_path"], "SEA-CDM tables"),
                           (row["provenance_path"], "provenance audit"),
                           (row["trace_path"], "run trace")):
            evidence.add_artifact(path, kind, produced_by=decision,
                                  evidence_ids=[paper_source, metadata_source],
                                  attributes={"provider": row["provider"], "repeat": row["repeat"]})
    evidence.add_claim("DeepSeek V4 Pro", "paired_seacdm_verdict", verdict,
                       f"Paired SEA-CDM extraction verdict: {verdict}", method="computation",
                       evidence_ids=[a.artifact_id for a in evidence.bundle.artifacts])
    for path, kind in ((str(summary_path), "evaluation summary"),
                       (str(report_path), "evaluation report"),
                       (str(stability_path), "stability summary"),
                       (str(workflow_path), "workflow log")):
        evidence.add_artifact(path, kind)
    evidence.finish("completed")
    evidence.save(str(out / "evidence.json"))

    lines = [
        "# Paired SEA-CDM extraction model A/B", "",
        f"- Verdict: **{verdict}**", "- Coverage: **100%**",
        f"- Blocking findings: **{len(blocking)}**", "",
        "| Metric | Sonnet 4.6 | DeepSeek V4 Pro |", "|---|---:|---:|",
        f"| Runs passed | {sonnet['passed']}/3 | {deepseek['passed']}/3 |",
        f"| Mean score | {sonnet['mean_score']} | {deepseek['mean_score']} |",
        f"| Mean provenance verified | {sonnet['mean_provenance_rate']:.1%} | {deepseek['mean_provenance_rate']:.1%} |",
        f"| Median latency (s) | {sonnet['median_latency_seconds']} | {deepseek['median_latency_seconds']} |",
        f"| Total model cost (USD) | {sonnet['total_cost_usd']:.6f} | {deepseek['total_cost_usd']:.6f} |",
        f"| Cost/pass (USD) | {sonnet['cost_per_pass_usd']} | {deepseek['cost_per_pass_usd']} |",
        "", "## Stability", "",
        f"- Metadata-derived structures identical: **{stability['cross_provider']['structural_identical']}**",
        f"- Cross-provider material Jaccard: **{stability['cross_provider']['mean_material_jaccard']:.3f}**",
        f"- Cross-provider intervention Jaccard: **{stability['cross_provider']['mean_intervention_jaccard']:.3f}**",
        f"- Cross-provider reported-finding Jaccard: **{stability['cross_provider']['mean_finding_jaccard']:.3f}**",
        "", "## Acceptance gates", "",
    ]
    lines.extend(f"- {name}: **{'pass' if value else 'fail'}**" for name, value in acceptance.items())
    lines.extend(["", "## Unmeasured checks", ""])
    lines.extend(f"- {item}" for item in report["unmeasured_checks"])
    (out / "model_seacdm_ab.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    tracker.set_stage("report", message=verdict)
    tracker.set_usage(llm_calls=sum(row["usage"]["calls"] for row in records),
                      estimated_cost_usd=sum(row["estimated_cost_usd"] for row in records))
    for finding in blocking:
        tracker.add_warning(finding)
    tracker.finish("completed", verdict)
    print(json.dumps({
        "verdict": verdict, "blocking": len(blocking), "aggregate": aggregate,
        "cost_ratio": report["cost_ratio_deepseek_vs_sonnet"],
        "stability": stability["cross_provider"], "output_dir": str(out),
    }, indent=2, ensure_ascii=False))
    return 0 if args.postprocess_existing or verdict == "deepseek_seacdm_validated" else 1


if __name__ == "__main__":
    raise SystemExit(main())
