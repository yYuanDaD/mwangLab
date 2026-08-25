"""Run the frozen 30-case x 3-repeat DeepSeek SEA-CDM production gate."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import random
import re
import shutil
import statistics
import sys
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "test" / "experiments" / "seacdm_exercise10_ab"))

from common import (  # noqa: E402
    H, PRICES, REQUIRED_TABLES, STRUCTURAL_TABLES, canon_hash, design_scope_audit,
    exercise_semantics_after_projection_fix, file_hash, table_fill,
)
from tools.evidence import EvidenceRecorder  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402
from tools.sea_cdm_schema import SEA_TABLES  # noqa: E402
from tools.seacdm_tools import extract_tables_from_text  # noqa: E402


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def deepseek_environment():
    keys = (
        "BIOAGENT_LLM_PROVIDER", "BIOAGENT_SEACDM_LLM_PROVIDER",
        "BIOAGENT_LLM_MODEL", "BIOAGENT_STRUCTURED_MAX_TOKENS",
    )
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


def _wilson(successes: int, total: int, z: float = 1.96) -> list[float] | None:
    if total == 0:
        return None
    p = successes / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * total)) / total) / denom
    return [round(max(0.0, centre - margin), 4), round(min(1.0, centre + margin), 4)]


def _record_path(out: Path, study_id: str, repeat: int) -> Path:
    return out / "studies" / study_id / f"r{repeat}" / "trace.json"


def _provider_blocked(record: dict) -> bool:
    errors = record.get("critical_stage_errors") or record.get("stage_errors") or {}
    text = json.dumps(errors, ensure_ascii=False).lower()
    return "insufficient balance" in text or "error code: 402" in text


def _archive_blocked_attempt(out: Path, study_id: str, repeat: int) -> None:
    source = out / "studies" / study_id / f"r{repeat}"
    if not source.is_dir():
        return
    base = out / "provider_blocked_attempts" / study_id / f"r{repeat}"
    attempt = 1
    target = base / f"attempt_{attempt}"
    while target.exists():
        attempt += 1
        target = base / f"attempt_{attempt}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)


def _run_one(case: dict, repeat: int, out: Path) -> dict:
    study_id = case["study_id"]
    run_dir = out / "studies" / study_id / f"r{repeat}"
    run_dir.mkdir(parents=True, exist_ok=True)
    paper = Path(case["text_path"])
    metadata = Path(case["metadata_path"])
    input_hashes = {"paper": file_hash(paper), "metadata": file_hash(metadata)}
    hash_ok = (
        input_hashes["paper"] == case["paper_sha256"]
        and input_hashes["metadata"] == case["metadata_sha256"]
    )
    usage: list[dict] = []
    report: dict = {}
    error = ""
    tables = {name: [] for name in SEA_TABLES}
    started = now()
    t0 = time.perf_counter()
    if hash_ok:
        try:
            text = paper.read_text(encoding="utf-8", errors="ignore")[:100_000]
            with deepseek_environment():
                tables = extract_tables_from_text(
                    study_id, text, case.get("organism", ""), verify=True, report=report,
                    metadata_csv=str(metadata), lean=True, usage=usage,
                    strategy="staged", max_stage_retries=1,
                )
        except Exception as exc:  # persisted as an experimental failure
            error = f"{type(exc).__name__}: {exc}"
    else:
        error = "InputHashMismatch: frozen paper or metadata changed"
    elapsed = round(time.perf_counter() - t0, 3)

    schema_errors = H._schema_errors(tables)
    fk_errors = H._fk_errors(tables)
    row_counts = {name: len(tables.get(name) or []) for name in SEA_TABLES}
    missing = [name for name in REQUIRED_TABLES if row_counts.get(name, 0) == 0]
    exercise = exercise_semantics_after_projection_fix(tables, str(metadata))
    scope = design_scope_audit(tables, study_id)
    metadata_count_ok = row_counts.get("sample", 0) == int(case["metadata_samples"])
    n_total = int(report.get("n_total") or 0)
    n_verified = int(report.get("n_verified") or 0)
    provenance_rate = n_verified / n_total if n_total else 0.0
    output_accessions = {
        item.upper() for item in re.findall(r"\bGSE\d+\b", H._all_text(tables, report), re.I)
    }
    unsupported = sorted(
        output_accessions - set(case.get("source_accessions") or []) - {study_id}
    )
    stage_errors = dict(report.get("group_errors") or {})
    critical_stage_errors = {
        key: value for key, value in stage_errors.items()
        if not str(key).startswith("findings_chunk_")
    }
    checks = {
        "completed": not error,
        "input_hashes_match": hash_ok,
        "schema_conformant": not schema_errors,
        "fk_integrity": not fk_errors,
        "required_tables_present": not missing,
        "exercise_semantics_valid": exercise["passed"],
        "no_critical_stage_errors": not critical_stage_errors,
        "metadata_sample_count_matches": metadata_count_ok,
        "no_foreign_design_accession": scope["passed"],
        "no_unsupported_accession": not unsupported,
        "provenance_measured": n_total > 0,
        "provenance_at_least_90pct": provenance_rate >= 0.90,
    }
    blocking = [name for name, passed in checks.items() if not passed]
    input_tokens = sum(int(row.get("input_tokens") or 0) for row in usage)
    output_tokens = sum(int(row.get("output_tokens") or 0) for row in usage)
    price = PRICES["deepseek"]
    cost = (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000
    structural = {name: tables.get(name, []) for name in STRUCTURAL_TABLES}
    structural_counts = {name: len(rows) for name, rows in structural.items()}
    tables_path = run_dir / "seacdm_tables.json"
    provenance_path = run_dir / "seacdm_provenance.json"
    tables_path.write_text(json.dumps(tables, indent=2, ensure_ascii=False), encoding="utf-8")
    provenance_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    record = {
        "study_id": study_id, "repeat": repeat, "case_labels": case["case_labels"],
        "started_at": started, "finished_at": now(), "elapsed_seconds": elapsed,
        "error": error, "checks": checks, "blocking": blocking,
        "schema_errors": schema_errors, "fk_errors": fk_errors, "missing_tables": missing,
        "stage_errors": stage_errors, "critical_stage_errors": critical_stage_errors,
        "warnings": [f"{key}:{value}" for key, value in stage_errors.items()
                     if key not in critical_stage_errors],
        "row_counts": row_counts, "table_fill": table_fill(tables),
        "exercise_check": exercise, "scope_audit": scope,
        "unsupported_accessions": unsupported,
        "provenance_total": n_total, "provenance_verified": n_verified,
        "provenance_rate": round(provenance_rate, 4),
        "usage": {"calls": len(usage), "input_tokens": input_tokens,
                  "output_tokens": output_tokens},
        "estimated_cost_usd": round(cost, 8),
        "structural_counts": structural_counts,
        "structural_count_hash": canon_hash(structural_counts),
        "structural_content_hash": canon_hash(structural),
        "input_hashes": input_hashes,
        "tables_path": str(tables_path), "provenance_path": str(provenance_path),
    }
    trace_path = run_dir / "trace.json"
    record["trace_path"] = str(trace_path)
    trace_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return record


def _load_records(out: Path) -> list[dict]:
    records = []
    for path in sorted(out.glob("studies/GSE*/r*/trace.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            # Preflight scorer correction: report['group_errors'] contains optional findings
            # chunk completion warnings as well as critical extraction-stage errors.  The
            # preregistered gate blocks group/design construction failures, not an optional
            # findings chunk when all required SEA-CDM tables and provenance remain valid.
            if "no_group_errors" in record.get("checks", {}):
                provenance = json.loads(
                    Path(record["provenance_path"]).read_text(encoding="utf-8")
                )
                stage_errors = dict(provenance.get("group_errors") or {})
                critical = {
                    key: value for key, value in stage_errors.items()
                    if not str(key).startswith("findings_chunk_")
                }
                record["checks"].pop("no_group_errors", None)
                record["checks"]["no_critical_stage_errors"] = not critical
                record["stage_errors"] = stage_errors
                record["critical_stage_errors"] = critical
                record["warnings"] = [
                    f"{key}:{value}" for key, value in stage_errors.items() if key not in critical
                ]
                record["blocking"] = [
                    key for key, passed in record["checks"].items() if not passed
                ]
                record["scorer_version"] = "1.1-preflight-correction"
                path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
            record["operational_status"] = (
                "provider_blocked" if _provider_blocked(record) else "completed"
            )
            record["quality_eligible"] = record["operational_status"] == "completed"
            if record["operational_status"] == "provider_blocked":
                path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
            records.append(record)
        except (OSError, ValueError):
            continue
    return records


def _write_summary(out: Path, manifest: dict, records: list[dict], planned: int) -> dict:
    all_records = list(records)
    provider_blocked = [row for row in all_records if _provider_blocked(row)]
    records = [row for row in all_records if not _provider_blocked(row)]
    cases = {case["study_id"]: case for case in manifest["cases"]}
    by_case: dict[str, list[dict]] = {study_id: [] for study_id in cases}
    for record in records:
        by_case.setdefault(record["study_id"], []).append(record)
    case_rows = []
    for study_id, rows in by_case.items():
        rows.sort(key=lambda row: row["repeat"])
        passed = sum(not row["blocking"] for row in rows)
        signatures = {row["structural_count_hash"] for row in rows}
        case_rows.append({
            "study_id": study_id,
            "case_labels": cases[study_id]["case_labels"],
            "primary_category": cases[study_id].get("primary_category", ""),
            "runs_completed": len(rows), "runs_passed": passed,
            "three_of_three_pass": len(rows) == 3 and passed == 3,
            "structural_counts_stable": len(rows) == 3 and len(signatures) == 1,
            "fallback_required": bool(rows) and any(row["blocking"] for row in rows),
            "blocking": sorted({item for row in rows for item in row["blocking"]}),
            "mean_provenance": round(statistics.mean(
                row["provenance_rate"] for row in rows), 4) if rows else 0.0,
            "cost_usd": round(sum(row["estimated_cost_usd"] for row in rows), 8),
        })

    complete_cases = [row for row in case_rows if row["runs_completed"] == 3]
    passing_cases = [row for row in complete_cases if row["three_of_three_pass"]]
    routine = [row for row in complete_cases if row["primary_category"] == "routine_single"]
    routine_pass = [row for row in routine if row["three_of_three_pass"]]
    stable = [row for row in complete_cases if row["structural_counts_stable"]]
    provenance_values = [row["provenance_rate"] for row in records]
    hard_zero_keys = (
        "input_hashes_match", "schema_conformant", "fk_integrity",
        "no_foreign_design_accession", "no_unsupported_accession",
    )
    hard_failures = {
        key: sum(not row["checks"].get(key, False) for row in records) for key in hard_zero_keys
    }
    case_rate = len(passing_cases) / len(complete_cases) if complete_cases else 0.0
    routine_rate = len(routine_pass) / len(routine) if routine else 0.0
    stability_rate = len(stable) / len(complete_cases) if complete_cases else 0.0
    mean_provenance = statistics.mean(provenance_values) if provenance_values else 0.0
    acceptance = {
        "all_90_runs_completed": len(records) == planned,
        "case_three_of_three_rate_at_least_90pct": case_rate >= 0.90,
        "routine_three_of_three_rate_at_least_95pct": bool(routine) and routine_rate >= 0.95,
        "zero_hash_schema_fk_scope_accession_failures": not any(hard_failures.values()),
        "mean_provenance_at_least_95pct": mean_provenance >= 0.95,
        "structural_count_stability_at_least_90pct": stability_rate >= 0.90,
    }
    if provider_blocked or len(records) < planned:
        verdict = "incomplete_provider_balance"
    else:
        verdict = "pass_production_gate" if all(acceptance.values()) else "not_ready_for_production"

    run_fields = [
        "study_id", "repeat", "operational_status", "status", "blocking", "provenance_rate", "llm_calls",
        "input_tokens", "output_tokens", "cost_usd", "elapsed_seconds",
    ]
    with (out / "per_run_results.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=run_fields)
        writer.writeheader()
        for row in sorted(all_records, key=lambda item: (item["study_id"], item["repeat"])):
            operational = "provider_blocked" if _provider_blocked(row) else "completed"
            writer.writerow({
                "study_id": row["study_id"], "repeat": row["repeat"],
                "operational_status": operational,
                "status": ("provider_blocked" if operational == "provider_blocked" else
                           ("pass" if not row["blocking"] else "fail")),
                "blocking": ";".join(row["blocking"]),
                "provenance_rate": row["provenance_rate"], "llm_calls": row["usage"]["calls"],
                "input_tokens": row["usage"]["input_tokens"],
                "output_tokens": row["usage"]["output_tokens"],
                "cost_usd": row["estimated_cost_usd"],
                "elapsed_seconds": row["elapsed_seconds"],
            })

    with (out / "per_case_results.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = [
            "study_id", "primary_category", "case_labels", "runs_completed", "runs_passed", "three_of_three_pass",
            "structural_counts_stable", "fallback_required", "blocking", "mean_provenance",
            "cost_usd",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in case_rows:
            payload = dict(row)
            payload["case_labels"] = ";".join(payload["case_labels"])
            payload["blocking"] = ";".join(payload["blocking"])
            writer.writerow(payload)

    with (out / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = [
            "study_id", "status", "primary_category", "runs_completed", "runs_passed",
            "three_of_three_pass", "fallback_required", "mean_provenance", "cost_usd",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in case_rows:
            writer.writerow({
                "study_id": row["study_id"],
                "status": "success" if row["three_of_three_pass"] else "partial",
                "primary_category": row["primary_category"],
                "runs_completed": row["runs_completed"], "runs_passed": row["runs_passed"],
                "three_of_three_pass": row["three_of_three_pass"],
                "fallback_required": row["fallback_required"],
                "mean_provenance": row["mean_provenance"], "cost_usd": row["cost_usd"],
            })

    report = {
        "schema_version": "1.0", "experiment": manifest["experiment"],
        "verdict": verdict, "planned_runs": planned, "completed_runs": len(records),
        "attempted_traces": len(all_records),
        "provider_blocked_attempts": len(provider_blocked),
        "provider_blocked_keys": [
            {"study_id": row["study_id"], "repeat": row["repeat"]}
            for row in provider_blocked
        ],
        "case_level": {
            "complete_cases": len(complete_cases), "passing_cases": len(passing_cases),
            "pass_rate": round(case_rate, 4),
            "pass_rate_wilson_95": _wilson(len(passing_cases), len(complete_cases)),
            "routine_cases": len(routine), "routine_passing": len(routine_pass),
            "routine_pass_rate": round(routine_rate, 4),
            "stable_cases": len(stable), "structural_count_stability_rate": round(stability_rate, 4),
            "fallback_required_cases": [row["study_id"] for row in case_rows
                                        if row["fallback_required"]],
        },
        "run_level": {
            "passing_runs": sum(not row["blocking"] for row in records),
            "mean_provenance": round(mean_provenance, 4),
            "median_latency_seconds": round(statistics.median(
                row["elapsed_seconds"] for row in records), 3) if records else None,
            "total_llm_calls": sum(row["usage"]["calls"] for row in records),
            "total_cost_usd": round(sum(row["estimated_cost_usd"] for row in records), 6),
            "hard_failures": hard_failures,
        },
        "acceptance": acceptance, "cases": case_rows,
    }
    (out / "production_gate_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    lines = [
        "# Large-scale SEA-CDM Production Gate v1", "",
        f"- Verdict: **{verdict}**",
        f"- Completed runs: **{len(records)}/{planned}**",
        f"- Provider-blocked attempts: **{len(provider_blocked)}**",
        f"- Three-of-three cases: **{len(passing_cases)}/{len(complete_cases)} "
        f"({case_rate:.1%})**",
        f"- Wilson 95% CI: **{report['case_level']['pass_rate_wilson_95']}**",
        f"- Mean verified provenance: **{mean_provenance:.1%}**",
        f"- Structural-count stability: **{stability_rate:.1%}**",
        f"- DeepSeek cost: **${report['run_level']['total_cost_usd']:.4f}**", "",
        "## Acceptance", "",
    ] + [f"- {'PASS' if value else 'FAIL'} — `{key}`" for key, value in acceptance.items()]
    lines += ["", "## Residual fallback queue", ""] + [
        f"- {study_id}" for study_id in report["case_level"]["fallback_required_cases"]
    ]
    (out / "production_gate_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "workflow.log").write_text(
        f"Large-scale SEA-CDM Production Gate v1\n"
        f"verdict={verdict}\nvalid_runs={len(records)}/{planned}\n"
        f"provider_blocked_attempts={len(provider_blocked)}\n"
        f"estimated_cost_usd={report['run_level']['total_cost_usd']:.6f}\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--budget-usd", type=float, default=4.50)
    parser.add_argument("--reserve-per-run-usd", type=float, default=0.10)
    parser.add_argument("--max-runs", type=int, default=0,
                        help="0 means all planned runs; use 1 for a paid preflight")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--summarize-only", action="store_true",
                        help="Rescore persisted traces without making model calls")
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--worker-only", action="store_true",
                        help="Run one disjoint shard and defer aggregate reporting")
    args = parser.parse_args()
    if args.repeats != 3:
        raise SystemExit("Production Gate v1 requires exactly three repeats")
    if args.budget_usd > 4.50:
        raise SystemExit("DeepSeek-stage budget cannot exceed the preregistered USD 4.50 cap")
    if args.shard_count < 1 or not 0 <= args.shard_index < args.shard_count:
        raise SystemExit("Require 0 <= shard-index < shard-count")
    if args.shard_count > 1 and not args.worker_only:
        raise SystemExit("Sharded execution requires --worker-only; summarize after all shards")

    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if len(manifest.get("cases", [])) != 30:
        raise SystemExit("Frozen manifest must contain exactly 30 cases")
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    copied_manifest = out / "frozen_manifest.json"
    if copied_manifest.exists():
        if file_hash(copied_manifest) != file_hash(manifest_path):
            raise SystemExit("Output directory contains a different frozen manifest")
    else:
        copied_manifest.write_bytes(manifest_path.read_bytes())
        (out / "PREREGISTERED_PROTOCOL.md").write_bytes(
            (manifest_path.parent / "PREREGISTERED_PROTOCOL.md").read_bytes()
        )

    plan = [
        {"study_id": case["study_id"], "repeat": repeat}
        for repeat in range(1, 4) for case in manifest["cases"]
    ]
    random.Random(20260819).shuffle(plan)
    plan_path = out / "execution_plan.json"
    frozen_plan = json.dumps(plan, indent=2)
    if plan_path.exists() and plan_path.read_text(encoding="utf-8") != frozen_plan:
        raise SystemExit("Output directory contains a different execution plan")
    if not plan_path.exists():
        plan_path.write_text(frozen_plan, encoding="utf-8")
    if args.dry_run:
        problems = []
        for case in manifest["cases"]:
            for key, hash_key in (("text_path", "paper_sha256"),
                                  ("metadata_path", "metadata_sha256")):
                path = Path(case[key])
                if not path.is_file() or file_hash(path) != case[hash_key]:
                    problems.append(f"{case['study_id']}:{key}")
        print(json.dumps({
            "dry_run": "pass" if not problems else "fail", "planned_runs": len(plan),
            "budget_usd": args.budget_usd, "input_problems": problems,
        }, indent=2))
        return 0 if not problems else 1

    tracker = RunStatusTracker(
        str(out / (f"run_status_shard{args.shard_index}.json" if args.worker_only
                   else "run_status.json")),
        run_id=f"{out.name}:shard{args.shard_index}" if args.worker_only else out.name,
        profile="seacdm_production_gate_v1", stages=["extract", "summarize", "audit"],
    )
    tracker.start("30-case x 3-repeat DeepSeek staged SEA-CDM production gate")
    shard_plan = [
        item for index, item in enumerate(plan)
        if index % args.shard_count == args.shard_index
    ]
    shard_keys = {(item["study_id"], int(item["repeat"])) for item in shard_plan}
    records = _load_records(out)
    existing = {
        (row["study_id"], int(row["repeat"]))
        for row in records if not _provider_blocked(row)
    }
    spent = sum(
        float(row["estimated_cost_usd"]) for row in records
        if (row["study_id"], int(row["repeat"])) in shard_keys and not _provider_blocked(row)
    )
    cases = {case["study_id"]: case for case in manifest["cases"]}
    limit = 0 if args.summarize_only else (
        args.max_runs if args.max_runs > 0 else len(plan)
    )
    new_runs = 0
    tracker.set_stage("extract", message=f"resuming at {len(records)}/{len(plan)}")
    budget_stopped = False
    for index, item in enumerate(shard_plan, 1):
        key = (item["study_id"], int(item["repeat"]))
        if key in existing:
            continue
        if new_runs >= limit:
            break
        if spent + args.reserve_per_run_usd > args.budget_usd:
            budget_stopped = True
            tracker.add_warning(
                f"budget_stop: spent=${spent:.6f}, reserve=${args.reserve_per_run_usd:.2f}"
            )
            break
        print(
            f"[shard {args.shard_index} {index}/{len(shard_plan)}] "
            f"{item['study_id']} r{item['repeat']} "
            f"spent=${spent:.4f}", flush=True,
        )
        trace_path = _record_path(out, item["study_id"], int(item["repeat"]))
        if trace_path.is_file():
            prior = json.loads(trace_path.read_text(encoding="utf-8"))
            if _provider_blocked(prior):
                _archive_blocked_attempt(out, item["study_id"], int(item["repeat"]))
        record = _run_one(cases[item["study_id"]], int(item["repeat"]), out)
        records.append(record)
        existing.add(key)
        spent += float(record["estimated_cost_usd"])
        new_runs += 1
        tracker.set_usage(
            llm_calls=sum(row["usage"]["calls"] for row in records),
            estimated_cost_usd=round(spent, 6),
        )
        tracker.set_stage("extract", message=f"{len(records)}/{len(plan)} runs")

    shard_completed = sum(key in existing for key in shard_keys)
    if args.worker_only:
        if budget_stopped:
            tracker.finish(
                "partial", f"shard budget stop at {shard_completed}/{len(shard_plan)}"
            )
            return 2
        tracker.finish("completed", f"shard {shard_completed}/{len(shard_plan)} complete")
        print(json.dumps({
            "shard_index": args.shard_index, "shard_count": args.shard_count,
            "completed": shard_completed, "planned": len(shard_plan),
            "cost_usd": round(spent, 6), "output_dir": str(out),
        }, indent=2))
        return 0 if shard_completed == len(shard_plan) else 1

    tracker.set_stage("summarize", message=f"summarizing {len(records)} runs")
    records = _load_records(out)
    report = _write_summary(out, manifest, records, len(plan))
    tracker.set_usage(
        llm_calls=report["run_level"]["total_llm_calls"],
        estimated_cost_usd=report["run_level"]["total_cost_usd"],
    )
    tracker.set_stage("audit", message="aggregate artifacts ready for independent audit")
    evidence = EvidenceRecorder(out.name, subject_id="seacdm:production-gate:v1")
    manifest_source = evidence.add_source(
        "artifact", "Frozen 30-case manifest", uri=str(out / "frozen_manifest.json"),
        attributes={"sha256": file_hash(out / "frozen_manifest.json")},
    )
    protocol_source = evidence.add_source(
        "rule", "Preregistered production-gate protocol",
        uri=str(out / "PREREGISTERED_PROTOCOL.md"),
        attributes={"sha256": file_hash(out / "PREREGISTERED_PROTOCOL.md")},
    )
    decision = evidence.add_decision(
        "evaluate_production_gate", {"verdict": report["verdict"]},
        reason="Frozen 30-case x 3-repeat staged extraction with preregistered hard gates",
        method="rule", evidence_ids=[manifest_source, protocol_source],
        details=report["acceptance"],
    )
    artifacts = [
        ("frozen_manifest.json", "frozen manifest"),
        ("PREREGISTERED_PROTOCOL.md", "preregistered protocol"),
        ("per_run_results.csv", "per-run results"),
        ("per_case_results.csv", "per-case results"),
        ("summary.csv", "root study summary"),
        ("workflow.log", "workflow log"),
        ("production_gate_report.json", "production gate report"),
        ("production_gate_report.md", "production gate report"),
    ]
    if (out / "protocol_amendment_preflight.json").is_file():
        artifacts.append(("protocol_amendment_preflight.json", "preflight scorer correction"))
    if (out / "provider_block_event.json").is_file():
        artifacts.append(("provider_block_event.json", "provider operational block"))
    for name, kind in artifacts:
        evidence.add_artifact(str(out / name), kind, produced_by=decision)
    evidence.finish("partial" if len(records) < len(plan) else "completed")
    evidence.save(str(out / "evidence.json"))
    for case in report["case_level"]["fallback_required_cases"]:
        tracker.add_warning(f"needs_fallback:{case}")
    if budget_stopped:
        tracker.finish("partial", f"budget stop at {len(records)}/{len(plan)} runs")
    elif len(records) < len(plan):
        tracker.finish("partial", f"preflight stop at {len(records)}/{len(plan)} runs")
    else:
        tracker.finish("completed", report["verdict"])
    print(json.dumps({
        "verdict": report["verdict"], "completed_runs": report["completed_runs"],
        "planned_runs": len(plan), "cost_usd": report["run_level"]["total_cost_usd"],
        "output_dir": str(out),
    }, indent=2))
    return 0 if (report["completed_runs"] == len(plan)
                 and report["verdict"] == "pass_production_gate") else 1


if __name__ == "__main__":
    raise SystemExit(main())
