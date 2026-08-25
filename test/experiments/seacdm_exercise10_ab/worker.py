"""Run one provider over the shared frozen exercise-paper manifest."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import statistics
import sys
import time

import pandas as pd


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import (  # noqa: E402
    DESCRIPTIVE_TABLES, H, PRICES, REQUIRED_TABLES, ROOT, STRUCTURAL_TABLES,
    canon_hash, design_scope_audit, exercise_semantics, table_fill,
)

from tools.evidence import EvidenceRecorder  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402
from tools.sea_cdm_schema import SEA_TABLES  # noqa: E402
from tools.seacdm_tools import extract_tables_from_text  # noqa: E402


def now():
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def provider_environment(provider: str):
    keys = ("BIOAGENT_LLM_PROVIDER", "BIOAGENT_SEACDM_LLM_PROVIDER",
            "BIOAGENT_LLM_MODEL", "BIOAGENT_STRUCTURED_MAX_TOKENS")
    old = {key: os.environ.get(key) for key in keys}
    os.environ["BIOAGENT_LLM_PROVIDER"] = provider
    os.environ["BIOAGENT_SEACDM_LLM_PROVIDER"] = provider
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=("anthropic", "deepseek"), required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    out = Path(args.output_dir).resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty provider directory: {out}")
    out.mkdir(parents=True, exist_ok=True)
    tracker = RunStatusTracker(
        str(out / "run_status.json"), run_id=out.name,
        profile=f"exercise10_seacdm_{args.provider}", stages=["extract", "report"],
    )
    tracker.start(f"Exercise 10-paper SEA-CDM: {args.provider}")
    tracker.set_stage("extract", message=f"{len(manifest['cases'])} frozen papers")
    records = []
    evidence = EvidenceRecorder(out.name, subject_id=f"exercise:{args.provider}")

    with provider_environment(args.provider):
        for index, case in enumerate(manifest["cases"], 1):
            study_id = case["study_id"]
            print(f"[{index}/{len(manifest['cases'])}] {args.provider}:{study_id}", flush=True)
            study_dir = out / "studies" / study_id
            study_dir.mkdir(parents=True, exist_ok=True)
            usage, report, error = [], {}, ""
            tables = {name: [] for name in SEA_TABLES}
            text = Path(case["text_path"]).read_text(encoding="utf-8", errors="ignore")[:100000]
            t0 = time.perf_counter()
            try:
                tables = extract_tables_from_text(
                    study_id, text, case.get("organism", ""), verify=True, report=report,
                    metadata_csv=case["metadata_path"], lean=True, usage=usage,
                    strategy="staged", max_stage_retries=1,
                )
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
            elapsed = round(time.perf_counter() - t0, 3)
            schema_errors = H._schema_errors(tables)
            fk_errors = H._fk_errors(tables)
            row_counts = {name: len(rows) for name, rows in tables.items()}
            missing = [name for name in REQUIRED_TABLES if row_counts.get(name, 0) == 0]
            exercise_check = exercise_semantics(tables, case["metadata_path"])
            scope = design_scope_audit(tables, study_id)
            metadata_count_ok = row_counts.get("sample", 0) == int(case["metadata_samples"])
            n_total = int(report.get("n_total") or 0)
            n_verified = int(report.get("n_verified") or 0)
            provenance_rate = n_verified / n_total if n_total else 0.0
            output_accessions = {item.upper() for item in re.findall(
                r"\bGSE\d+\b", H._all_text(tables, report), re.I
            )}
            unsupported = sorted(output_accessions - set(case["source_accessions"]) - {study_id})
            checks = {
                "completed": not error,
                "schema_conformant": not schema_errors,
                "fk_integrity": not fk_errors,
                "required_tables_present": not missing,
                "exercise_semantics_valid": exercise_check["passed"],
                "no_group_errors": not report.get("group_errors"),
                "metadata_sample_count_matches": metadata_count_ok,
                "no_foreign_design_accession": scope["passed"],
                "provenance_measured": n_total > 0,
                "provenance_at_least_90pct": provenance_rate >= 0.90,
                "no_unsupported_accession": not unsupported,
            }
            blocking_keys = (
                "completed", "schema_conformant", "fk_integrity", "required_tables_present",
                "exercise_semantics_valid",
                "no_group_errors", "metadata_sample_count_matches",
                "no_foreign_design_accession", "no_unsupported_accession",
            )
            blocking = [name for name in blocking_keys if not checks[name]]
            input_tokens = sum(int(row.get("input_tokens") or 0) for row in usage)
            output_tokens = sum(int(row.get("output_tokens") or 0) for row in usage)
            price = PRICES[args.provider]
            cost = (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000
            semantics = H._semantic_sets(tables, report)
            structural = {name: tables.get(name, []) for name in STRUCTURAL_TABLES}
            descriptive = {name: tables.get(name, []) for name in DESCRIPTIVE_TABLES}
            tables_path = study_dir / "seacdm_tables.json"
            provenance_path = study_dir / "seacdm_provenance.json"
            trace_path = study_dir / "trace.json"
            tables_path.write_text(json.dumps(tables, indent=2, ensure_ascii=False), encoding="utf-8")
            provenance_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            record = {
                "provider": args.provider, "study_id": study_id, "title": case["title"],
                "started_at": now(), "elapsed_seconds": elapsed, "error": error,
                "checks": checks, "blocking": blocking, "schema_errors": schema_errors,
                "fk_errors": fk_errors, "missing_tables": missing, "row_counts": row_counts,
                "exercise_check": exercise_check,
                "table_fill": table_fill(tables), "scope_audit": scope,
                "unsupported_accessions": unsupported,
                "provenance_total": n_total, "provenance_verified": n_verified,
                "provenance_rate": round(provenance_rate, 4),
                "usage": {"calls": len(usage), "input_tokens": input_tokens,
                          "output_tokens": output_tokens},
                "estimated_cost_usd": round(cost, 8),
                "semantic_sets": {name: sorted(values) for name, values in semantics.items()},
                "structural_hash": canon_hash(structural),
                "descriptive_hash": canon_hash(descriptive),
                "tables_path": str(tables_path), "provenance_path": str(provenance_path),
            }
            record["trace_path"] = str(trace_path)
            trace_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
            records.append(record)
            decision = evidence.add_decision(
                "exercise10_seacdm_extract", {"provider": args.provider, "study_id": study_id},
                reason="Same frozen exercise-paper manifest", method="llm", details=checks,
            )
            for path, kind in ((tables_path, "SEA-CDM tables"),
                               (provenance_path, "provenance audit"),
                               (trace_path, "run trace")):
                evidence.add_artifact(str(path), kind, produced_by=decision)

    passed = sum(not row["blocking"] for row in records)
    summary = {
        "provider": args.provider, "papers": len(records), "passed": passed,
        "failed": len(records) - passed,
        "mean_provenance_rate": round(statistics.mean(
            row["provenance_rate"] for row in records), 4),
        "median_latency_seconds": round(statistics.median(
            row["elapsed_seconds"] for row in records), 3),
        "total_cost_usd": round(sum(row["estimated_cost_usd"] for row in records), 6),
        "total_llm_calls": sum(row["usage"]["calls"] for row in records),
        "schema_failures": sum(bool(row["schema_errors"]) for row in records),
        "fk_failures": sum(bool(row["fk_errors"]) for row in records),
        "scope_failures": sum(not row["checks"]["no_foreign_design_accession"] for row in records),
        "metadata_count_failures": sum(
            not row["checks"]["metadata_sample_count_matches"] for row in records
        ),
    }
    pd.DataFrame([{
        "provider": row["provider"], "study_id": row["study_id"],
        "status": "success" if not row["blocking"] else "failed",
        "blocking": ";".join(row["blocking"]),
        "provenance_rate": row["provenance_rate"],
        "llm_calls": row["usage"]["calls"], "cost_usd": row["estimated_cost_usd"],
        "elapsed_seconds": row["elapsed_seconds"],
        **{f"rows_{name}": count for name, count in row["row_counts"].items()},
    } for row in records]).to_csv(out / "summary.csv", index=False)
    report_path = out / "provider_report.json"
    report_path.write_text(json.dumps({
        "schema_version": "1.0", "manifest": str(manifest_path),
        "summary": summary, "records": records,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    evidence.add_artifact(str(out / "summary.csv"), "provider summary")
    evidence.add_artifact(str(report_path), "provider report")
    evidence.finish("completed")
    evidence.save(str(out / "evidence.json"))
    tracker.set_stage("report", message=f"{passed}/{len(records)} passed")
    tracker.set_usage(llm_calls=summary["total_llm_calls"],
                      estimated_cost_usd=summary["total_cost_usd"])
    for row in records:
        for blocker in row["blocking"]:
            tracker.add_warning(f"{row['study_id']}:{blocker}")
    tracker.finish("completed", f"{passed}/{len(records)} passed")
    print(json.dumps({"summary": summary, "output_dir": str(out)}, indent=2))
    return 0 if passed == len(records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
