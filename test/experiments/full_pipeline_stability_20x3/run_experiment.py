"""Run the frozen 20-study x 3-repeat full RNA-seq stability benchmark."""

from __future__ import annotations

import argparse
from datetime import datetime
from itertools import combinations
import json
import os
from pathlib import Path
import shutil
import sys
import time
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import tools.batch_tools as bt  # noqa: E402
from test.experiments.full_pipeline_production_gate.run_experiment import (  # noqa: E402
    _CachedAcquisitionTool,
    _run_case,
)
from tools.evidence import EvidenceRecorder, file_sha256  # noqa: E402
from tools.llm_helpers import llm_usage_checkpoint, llm_usage_summary, reset_llm_usage  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402


REGULAR_ESTIMATE_PER_CALL_USD = 0.003
EXPECTED_CALLS_PER_REPEAT = 14
PEAK_MULTIPLIER = 2.0
DEFAULT_BUDGET_USD = 0.50


def _input_hashes_match(case: dict) -> bool:
    matrix = ROOT / case["matrix_path"]
    metadata = ROOT / case["metadata_path"]
    return (
        matrix.is_file() and metadata.is_file()
        and file_sha256(str(matrix)) == case["matrix_sha256"]
        and file_sha256(str(metadata)) == case["metadata_sha256"]
    )


def _merge_usage(results: list[dict]) -> dict:
    calls = []
    for result in results:
        calls.extend((result.get("usage") or {}).get("calls") or [])
    priced = [call.get("estimated_cost_usd") for call in calls
              if call.get("estimated_cost_usd") is not None]
    return {
        "llm_calls": len(calls),
        "usage_measured_calls": sum(bool(call.get("usage_measured")) for call in calls),
        "input_tokens": sum(int(call.get("input_tokens") or 0) for call in calls),
        "cache_read_input_tokens": sum(
            int(call.get("cache_read_input_tokens") or 0) for call in calls
        ),
        "output_tokens": sum(int(call.get("output_tokens") or 0) for call in calls),
        "estimated_cost_usd": round(sum(float(value) for value in priced), 8),
        "unpriced_calls": sum(call.get("estimated_cost_usd") is None for call in calls),
        "calls": calls,
    }


def _safe_corr(left: pd.Series, right: pd.Series) -> float | None:
    joined = pd.concat([pd.to_numeric(left, errors="coerce"),
                        pd.to_numeric(right, errors="coerce")], axis=1).dropna()
    if len(joined) < 3:
        return None
    if joined.iloc[:, 0].nunique() < 2 or joined.iloc[:, 1].nunique() < 2:
        return 1.0 if joined.iloc[:, 0].equals(joined.iloc[:, 1]) else None
    return float(joined.iloc[:, 0].corr(joined.iloc[:, 1]))


def _jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return 1.0 if not union else len(left & right) / len(union)


def _deg_payload(path: Path) -> tuple[pd.Series, set[str]]:
    frame = pd.read_csv(path, index_col=0)
    ranked = pd.to_numeric(frame["log2FoldChange"], errors="coerce")
    padj = pd.to_numeric(frame["padj"], errors="coerce")
    significant = set(frame.index[(padj < 0.05) & (ranked.abs() > 1)].astype(str))
    ranked.index = ranked.index.astype(str)
    return ranked, significant


def _gsea_payload(path: Path) -> tuple[pd.Series, set[str]]:
    frame = pd.read_csv(path)
    term_col = next((col for col in ("Term", "Name", "pathway") if col in frame.columns), frame.columns[0])
    nes_col = next(col for col in frame.columns if str(col).upper() == "NES")
    fdr_col = next(col for col in frame.columns if "fdr" in str(col).lower())
    index = frame[term_col].astype(str)
    nes = pd.Series(pd.to_numeric(frame[nes_col], errors="coerce").to_numpy(), index=index)
    fdr = pd.Series(pd.to_numeric(frame[fdr_col], errors="coerce").to_numpy(), index=index)
    return nes, set(fdr.index[fdr < 0.25])


def _repeat_metrics(paths: list[Path], loader) -> tuple[list[float], list[float]]:
    payloads = [loader(path) for path in paths]
    correlations, jaccards = [], []
    for (rank_a, sig_a), (rank_b, sig_b) in combinations(payloads, 2):
        corr = _safe_corr(rank_a, rank_b)
        if corr is not None:
            correlations.append(corr)
        jaccards.append(_jaccard(sig_a, sig_b))
    return correlations, jaccards


def evaluate_case_stability(case: dict, trials: list[dict], repeats: int) -> dict:
    passed_trials = [trial for trial in trials if trial.get("passed")]
    checks = {
        "all_repeats_present": len(trials) == repeats,
        "all_repeats_passed": len(passed_trials) == repeats,
        "route_and_contrast_consistent": all(trial.get("passed") for trial in trials),
    }
    deg_r: list[float] = []
    deg_j: list[float] = []
    gsea_r: list[float] = []
    gsea_j: list[float] = []
    if checks["all_repeats_passed"]:
        case_dirs = [Path(trial["case_dir"]) for trial in sorted(trials, key=lambda x: x["repeat"])]
        deg_names = set.intersection(*[
            {p.name for p in d.glob("DEG_results_*.csv") if "_GSEA_" not in p.name}
            for d in case_dirs
        ])
        gsea_names = set.intersection(*[{p.name for p in d.glob("*_GSEA_Hallmark.csv")}
                                        for d in case_dirs])
        for name in sorted(deg_names):
            correlations, jaccards = _repeat_metrics([d / name for d in case_dirs], _deg_payload)
            deg_r.extend(correlations)
            deg_j.extend(jaccards)
        for name in sorted(gsea_names):
            correlations, jaccards = _repeat_metrics([d / name for d in case_dirs], _gsea_payload)
            gsea_r.extend(correlations)
            gsea_j.extend(jaccards)
        expected_pairs = int(case["expected_n_contrasts"]) * 3
        checks.update({
            "deg_repeat_pairs_complete": len(deg_r) >= expected_pairs,
            "gsea_repeat_pairs_complete": len(gsea_r) >= expected_pairs,
            "deg_rank_stable": bool(deg_r) and min(deg_r) >= 0.99,
            "gsea_rank_stable": bool(gsea_r) and min(gsea_r) >= 0.99,
            "deg_threshold_stable": bool(deg_j) and min(deg_j) >= 0.95,
            "gsea_threshold_stable": bool(gsea_j) and min(gsea_j) >= 0.95,
        })
    else:
        checks.update({
            "deg_repeat_pairs_complete": False,
            "gsea_repeat_pairs_complete": False,
            "deg_rank_stable": False,
            "gsea_rank_stable": False,
            "deg_threshold_stable": False,
            "gsea_threshold_stable": False,
        })
    blocking = sorted(name for name, value in checks.items() if not value)
    return {
        "case_id": case["id"],
        "accession": case["accession"],
        "trials": len(trials),
        "passing_trials": len(passed_trials),
        "checks": checks,
        "passed": not blocking,
        "blocking": blocking,
        "min_deg_log2fc_r": min(deg_r) if deg_r else None,
        "mean_deg_log2fc_r": float(np.mean(deg_r)) if deg_r else None,
        "min_sig_deg_jaccard": min(deg_j) if deg_j else None,
        "min_gsea_nes_r": min(gsea_r) if gsea_r else None,
        "mean_gsea_nes_r": float(np.mean(gsea_r)) if gsea_r else None,
        "min_sig_pathway_jaccard": min(gsea_j) if gsea_j else None,
    }


def _trial_row(result: dict) -> dict:
    row = result.get("row") or {}
    usage = result.get("usage") or {}
    return {
        "repeat": result.get("repeat"),
        "case_id": result.get("case_id"),
        "accession": result.get("accession"),
        "status": "deg_gsea_ok" if result.get("passed") else "failed_gate",
        "pipeline_status": result.get("pipeline_status"),
        "matrix_type": row.get("matrix_type"),
        "da_method": row.get("da_method"),
        "design_col": row.get("design_col"),
        "control": row.get("control"),
        "treatment": row.get("treatment"),
        "n_contrasts": row.get("n_contrasts"),
        "n_deg": row.get("n_deg"),
        "n_gsea_sig": row.get("n_gsea_sig"),
        "deg_sanity": row.get("deg_sanity"),
        "alignment_method": (result.get("alignment") or {}).get("method"),
        "aligned_samples": (result.get("alignment") or {}).get("n_aligned"),
        "llm_calls": usage.get("llm_calls", 0),
        "estimated_cost_usd": usage.get("estimated_cost_usd", 0),
        "blocking": ";".join(result.get("blocking") or []),
    }


def _write_budget(out: Path, budget_usd: float, *, actual: dict | None = None) -> dict:
    regular = EXPECTED_CALLS_PER_REPEAT * 3 * REGULAR_ESTIMATE_PER_CALL_USD
    payload = {
        "schema_version": "1.0",
        "provider": "deepseek",
        "model": "deepseek-v4-pro",
        "pricing_source": "https://api-docs.deepseek.com/quick_start/pricing",
        "pricing_checked_at": "2026-08-25",
        "regular_rates_per_million_tokens_usd": {
            "cache_hit_input": 0.003625,
            "cache_miss_input": 0.435,
            "output": 0.87,
        },
        "expected_calls": EXPECTED_CALLS_PER_REPEAT * 3,
        "planning_cost_per_call_usd": REGULAR_ESTIMATE_PER_CALL_USD,
        "estimated_regular_cost_usd": round(regular, 3),
        "peak_multiplier_contingency": PEAK_MULTIPLIER,
        "estimated_peak_cost_usd": round(regular * PEAK_MULTIPLIER, 3),
        "hard_budget_usd": budget_usd,
        "budget_scope": "LLM token charges; GEO/MSigDB/MyGene endpoints have no per-call project charge",
        "actual": actual,
    }
    (out / "budget.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _write_report(out: Path, manifest: dict, results: list[dict], stability: list[dict],
                  usage: dict, budget: dict, budget_exceeded: bool) -> dict:
    expected_trials = manifest["case_count"] * manifest["repeats"]
    acceptance = {
        "all_60_trials_executed": len(results) == expected_trials == 60,
        "all_60_trials_passed": len(results) == expected_trials and all(r.get("passed") for r in results),
        "all_20_cases_repeat_stable": len(stability) == 20 and all(item["passed"] for item in stability),
        "all_llm_usage_measured_and_priced": (
            usage["llm_calls"] == usage["usage_measured_calls"]
            and usage["unpriced_calls"] == 0
        ),
        "all_input_hashes_match": all(_input_hashes_match(case) for case in manifest["cases"]),
        "within_peak_budget": not budget_exceeded and (
            usage["estimated_cost_usd"] * PEAK_MULTIPLIER <= budget["hard_budget_usd"]
        ),
    }
    verdict = "production_stability_pass" if all(acceptance.values()) else "production_stability_fail"
    report = {
        "schema_version": "1.0",
        "experiment": manifest["experiment"],
        "verdict": verdict,
        "acceptance": acceptance,
        "trial_count": len(results),
        "passing_trials": sum(bool(result.get("passed")) for result in results),
        "stable_cases": sum(bool(item["passed"]) for item in stability),
        "llm_usage": {key: value for key, value in usage.items() if key != "calls"},
        "budget": budget,
        "blocking_findings": {
            item["case_id"]: item["blocking"] for item in stability if item["blocking"]
        },
        "cases": stability,
    }
    (out / "large_experiment_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    lines = [
        "# Full Pipeline Stability 20 x 3",
        "",
        f"- Verdict: **{verdict}**",
        f"- Trials passed: **{report['passing_trials']}/{expected_trials}**",
        f"- Repeat-stable cases: **{report['stable_cases']}/20**",
        f"- LLM calls: **{usage['llm_calls']}**",
        f"- Regular estimated token cost: **${usage['estimated_cost_usd']:.6f}**",
        f"- 2x peak contingency: **${usage['estimated_cost_usd'] * PEAK_MULTIPLIER:.6f}**",
        "",
        "## Acceptance",
        "",
    ]
    lines.extend(f"- {'PASS' if value else 'FAIL'} - `{key}`" for key, value in acceptance.items())
    lines.extend(["", "## Cases", "", "| Case | Repeats | Stable | Blocking |", "|---|---:|---|---|"])
    for item in stability:
        lines.append(
            f"| {item['case_id']} | {item['passing_trials']}/3 | "
            f"{'PASS' if item['passed'] else 'FAIL'} | {', '.join(item['blocking']) or 'none'} |"
        )
    (out / "large_experiment_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def _write_evidence(out: Path, report: dict, results: list[dict]) -> None:
    recorder = EvidenceRecorder(out.name, subject_id="rnaseq:full-pipeline:stability-20x3")
    manifest_source = recorder.add_source(
        "artifact", "Frozen 20x3 manifest", uri=str(out / "frozen_manifest.json"),
        attributes={"sha256": file_sha256(str(out / "frozen_manifest.json"))},
    )
    protocol_source = recorder.add_source(
        "rule", "Preregistered 20x3 protocol", uri=str(out / "PREREGISTERED_PROTOCOL.md"),
        attributes={"sha256": file_sha256(str(out / "PREREGISTERED_PROTOCOL.md"))},
    )
    decision = recorder.add_decision(
        "evaluate_full_pipeline_stability", {"verdict": report["verdict"]},
        reason="Twenty frozen GEO cases executed in three independent repeats.",
        method="rule", evidence_ids=[manifest_source, protocol_source],
        details=report["acceptance"],
    )
    for name, role in (
        ("frozen_manifest.json", "frozen manifest"),
        ("PREREGISTERED_PROTOCOL.md", "preregistered protocol"),
        ("summary.csv", "60-trial summary"),
        ("case_stability.csv", "20-case stability metrics"),
        ("large_experiment_report.json", "machine report"),
        ("large_experiment_report.md", "human report"),
        ("llm_usage.json", "token and cost ledger"),
        ("budget.json", "budget plan and actual"),
        ("run_status.json", "run status"),
        ("workflow.log", "workflow log"),
    ):
        path = out / name
        if path.is_file():
            recorder.add_artifact(str(path), role, produced_by=decision)
    for result in results:
        path = Path(result.get("result_path") or "")
        if path.is_file():
            recorder.add_artifact(str(path), f"trial result {result['case_id']} r{result['repeat']}", produced_by=decision)
    recorder.finish("completed" if report["verdict"] == "production_stability_pass" else "partial")
    recorder.save(str(out / "evidence.json"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--budget-usd", type=float, default=DEFAULT_BUDGET_USD)
    parser.add_argument("--rerun", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("case_count") != 20 or manifest.get("repeats") != 3:
        raise SystemExit("Formal manifest must freeze exactly 20 cases x 3 repeats")
    invalid = [case["id"] for case in manifest["cases"] if not _input_hashes_match(case)]
    if invalid:
        raise SystemExit(f"Frozen input hash mismatch: {invalid}")
    if args.budget_usd <= 0:
        raise SystemExit("--budget-usd must be positive")
    if args.dry_run:
        print(json.dumps({
            "status": "pass", "trials": 60, "invalid_hashes": invalid,
            "expected_llm_calls": EXPECTED_CALLS_PER_REPEAT * 3,
            "estimated_regular_cost_usd": EXPECTED_CALLS_PER_REPEAT * 3 * REGULAR_ESTIMATE_PER_CALL_USD,
            "estimated_peak_cost_usd": EXPECTED_CALLS_PER_REPEAT * 3 * REGULAR_ESTIMATE_PER_CALL_USD * PEAK_MULTIPLIER,
            "hard_budget_usd": args.budget_usd,
        }, indent=2))
        return 0

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(args.output_dir).resolve() if args.output_dir else ROOT / "output" / f"full_pipeline_stability_20x3_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    frozen = out / "frozen_manifest.json"
    if frozen.is_file() and file_sha256(str(frozen)) != file_sha256(str(manifest_path)):
        raise SystemExit("Output directory contains a different frozen manifest")
    if not frozen.is_file():
        shutil.copy2(manifest_path, frozen)
    protocol = Path(__file__).with_name("PREREGISTERED_PROTOCOL.md")
    shutil.copy2(protocol, out / protocol.name)
    budget = _write_budget(out, args.budget_usd)
    tracker = RunStatusTracker(
        str(out / "run_status.json"), run_id=out.name,
        profile="full_pipeline_stability_20x3",
        stages=("validate_inputs", "execute", "stability", "report"),
        study_total=60,
    )
    tracker.start("20 cases x 3 independent repeats")
    tracker.set_stage("validate_inputs", message="manifest, hashes, and budget passed")
    os.environ["BIOAGENT_LLM_PROVIDER"] = "deepseek"
    os.environ["BIOAGENT_LLM_MODEL"] = "deepseek-v4-pro"
    os.environ["BIOAGENT_LLM_EFFORT"] = "max"
    reset_llm_usage()
    original_download = bt.download_geo_data
    original_supplement = bt.download_supplementary_files
    bt.download_geo_data = _CachedAcquisitionTool("metadata")
    bt.download_supplementary_files = _CachedAcquisitionTool("supplementary")
    results: list[dict] = []
    workflow = [
        "Full pipeline stability experiment: 20 cases x 3 repeats",
        f"manifest={manifest_path}",
        f"budget_usd={args.budget_usd}",
        "provider=deepseek model=deepseek-v4-pro",
        "llm_datatype=true acquisition=frozen-cache gsea=live",
    ]
    budget_exceeded = False
    started = time.perf_counter()
    try:
        tracker.set_stage("execute", message="running 60 trials")
        trial_index = 0
        for repeat in range(1, manifest["repeats"] + 1):
            repeat_dir = out / f"repeat_{repeat:02d}"
            for case in manifest["cases"]:
                trial_index += 1
                existing = repeat_dir / "case_results" / f"{case['id']}.json"
                tracker.set_stage("execute", message=f"trial {trial_index}/60: {case['id']} repeat {repeat}")
                if existing.is_file() and not args.rerun:
                    result = json.loads(existing.read_text(encoding="utf-8"))
                    result["result_path"] = str(existing.resolve())
                    workflow.append(f"r{repeat} {case['id']}: reused")
                else:
                    checkpoint = llm_usage_checkpoint()
                    try:
                        result = _run_case(case, repeat_dir, llm_datatype=True)
                    except Exception as exc:
                        result = {
                            "case_id": case["id"], "accession": case["accession"],
                            "row": {}, "passed": False, "checks": {},
                            "blocking": ["execution_exception"], "alignment": {},
                            "pipeline_status": "exception",
                            "execution_error": f"{type(exc).__name__}: {exc}",
                        }
                    # Each child cohort writes its own measured usage. Read that rather
                    # than relying on a process-global cursor so resume remains exact.
                    cohort_status = repeat_dir / "runs" / f"cohort_{case['id']}" / "run_status.json"
                    child_usage = {"llm_calls": 0, "estimated_cost_usd": 0.0, "calls": []}
                    # Detailed records are the calls appended since the previous trial.
                    usage = llm_usage_summary(checkpoint)
                    if cohort_status.is_file():
                        child = json.loads(cohort_status.read_text(encoding="utf-8"))
                        usage["llm_calls"] = child.get("llm_calls", usage["llm_calls"])
                        usage["estimated_cost_usd"] = child.get("estimated_cost_usd", usage["estimated_cost_usd"])
                    child_usage = usage
                    result["repeat"] = repeat
                    result["usage"] = child_usage
                    existing.parent.mkdir(parents=True, exist_ok=True)
                    result["result_path"] = str(existing.resolve())
                    existing.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
                    workflow.append(
                        f"r{repeat} {case['id']}: {'pass' if result.get('passed') else 'fail'} "
                        f"calls={child_usage['llm_calls']} cost={child_usage['estimated_cost_usd']:.8f}"
                    )
                result.setdefault("repeat", repeat)
                result.setdefault("usage", {"llm_calls": 0, "estimated_cost_usd": 0.0, "calls": []})
                results.append(result)
                usage_total = _merge_usage(results)
                tracker.set_usage(
                    llm_calls=usage_total["llm_calls"],
                    estimated_cost_usd=usage_total["estimated_cost_usd"],
                )
                (out / "progress.json").write_text(json.dumps({
                    "completed_trials": len(results), "expected_trials": 60,
                    "passing_trials": sum(bool(item.get("passed")) for item in results),
                    "usage": {key: value for key, value in usage_total.items() if key != "calls"},
                }, indent=2), encoding="utf-8")
                if usage_total["estimated_cost_usd"] * PEAK_MULTIPLIER > args.budget_usd:
                    budget_exceeded = True
                    workflow.append("budget exceeded; stopped before next trial")
                    break
            if budget_exceeded:
                break
    finally:
        bt.download_geo_data = original_download
        bt.download_supplementary_files = original_supplement

    tracker.set_stage("stability", message="computing cross-repeat DEG/GSEA stability")
    stability = []
    for case in manifest["cases"]:
        trials = [result for result in results if result.get("case_id") == case["id"]]
        stability.append(evaluate_case_stability(case, trials, manifest["repeats"]))
    pd.DataFrame([_trial_row(result) for result in results]).to_csv(out / "summary.csv", index=False)
    pd.DataFrame([{key: value for key, value in item.items() if key != "checks"}
                  for item in stability]).to_csv(out / "case_stability.csv", index=False)
    usage = _merge_usage(results)
    (out / "llm_usage.json").write_text(json.dumps(usage, indent=2), encoding="utf-8")
    budget = _write_budget(out, args.budget_usd, actual={
        "regular_estimated_cost_usd": usage["estimated_cost_usd"],
        "peak_contingency_cost_usd": round(usage["estimated_cost_usd"] * PEAK_MULTIPLIER, 8),
        "llm_calls": usage["llm_calls"],
    })
    tracker.set_stage("report", message="writing report and evidence")
    report = _write_report(out, manifest, results, stability, usage, budget, budget_exceeded)
    workflow.extend([
        f"elapsed_seconds={time.perf_counter() - started:.3f}",
        f"llm_calls={usage['llm_calls']}",
        f"llm_cost_usd={usage['estimated_cost_usd']:.8f}",
        f"verdict={report['verdict']}",
    ])
    (out / "workflow.log").write_text("\n".join(workflow) + "\n", encoding="utf-8")
    tracker.finish(
        "completed" if report["verdict"] == "production_stability_pass" else "partial",
        report["verdict"],
    )
    _write_evidence(out, report, results)
    print(json.dumps({
        "verdict": report["verdict"], "passing_trials": report["passing_trials"],
        "stable_cases": report["stable_cases"], "llm_calls": usage["llm_calls"],
        "estimated_cost_usd": usage["estimated_cost_usd"], "output_dir": str(out),
    }, indent=2))
    return 0 if report["verdict"] == "production_stability_pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())