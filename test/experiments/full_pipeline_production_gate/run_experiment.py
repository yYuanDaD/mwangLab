"""Run the six-case cached-input full RNA-seq pipeline preflight."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import sys
import time
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import tools.batch_tools as bt  # noqa: E402
from tools.analysis_policy import (  # noqa: E402
    PolicyViolation,
    enforce_method_matrix_compatibility,
    select_valid_two_group_design,
)
from tools.evidence import EvidenceRecorder, file_sha256  # noqa: E402
from tools.llm_helpers import llm_usage_checkpoint, llm_usage_summary  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402


RAW_METHODS = ("deseq2", "edger", "voom")


class _CachedAcquisitionTool:
    def __init__(self, label: str):
        self.label = label

    def invoke(self, kwargs: dict) -> str:
        return (
            f"{self.label}: frozen cached input for {kwargs.get('geo_accession')} "
            "(network acquisition intentionally skipped by preflight protocol)."
        )


def _as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or pd.isna(value):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _load_decisions(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("decisions") or [])


def _decision_details(decisions: list[dict], step: str) -> dict:
    for item in decisions:
        if item.get("step") == step:
            details = dict(item.get("details") or {})
            details.setdefault("verdict", item.get("decision"))
            return details
    return {}


def _da_treatments(decisions: list[dict]) -> set[str]:
    values = set()
    for item in decisions:
        if item.get("step") not in {"deseq2", "edger", "limma-voom", "limma"}:
            continue
        details = item.get("details") or {}
        if item.get("decision") == "ok" and details.get("treatment"):
            values.add(str(details["treatment"]))
    return values


def _method_compatible(matrix_type: str, method: str) -> bool:
    matrix = str(matrix_type).lower()
    selected = str(method).lower()
    if "raw" in matrix:
        return any(token in selected for token in RAW_METHODS)
    if any(token in matrix for token in ("fpkm", "tpm", "log")):
        return "limma" in selected and "voom" not in selected
    return False


def evaluate_case(
    case: dict,
    row: dict,
    decisions: list[dict],
    artifacts: dict[str, int | bool],
    *,
    hashes_match: bool,
    run_terminal: bool,
) -> dict:
    alignment = _decision_details(decisions, "metadata_alignment")
    alignment_method = str(alignment.get("method") or alignment.get("verdict") or "")
    observed_treatments = _da_treatments(decisions)
    expected_treatments = {str(value) for value in case["expected_treatments"]}
    expected_alignment = case.get("expected_alignment_prefix")
    min_aligned = int(case.get("expected_min_aligned") or 0)
    selected_name = Path(str(row.get("counts_file") or "")).name
    pipeline_status = str(row.get("status") or "")
    deg_sanity = str(row.get("deg_sanity") or "").strip().lower()
    method = str(row.get("da_method") or "")
    checks = {
        "input_hashes_match": hashes_match,
        "matrix_selected": selected_name == case["expected_matrix"],
        "matrix_type": str(row.get("matrix_type")) == case["expected_matrix_type"],
        "matrix_method_compatible": _method_compatible(str(row.get("matrix_type")), method),
        "expected_method": case["expected_method"].lower() in method.lower(),
        "design_column": str(row.get("design_col")) == case["expected_design"],
        "control_group": str(row.get("control")) == case["expected_control"],
        "treatment_set": observed_treatments == expected_treatments,
        "contrast_count": _as_int(row.get("n_contrasts")) == case["expected_n_contrasts"],
        "sample_alignment": alignment.get("verdict") not in {None, "no_align", "read_failed"},
        "minimum_alignment": not min_aligned or _as_int(alignment.get("n_aligned")) >= min_aligned,
        "expected_alignment_path": (
            True if not expected_alignment else alignment_method.lower().startswith(expected_alignment.lower())
        ),
        "pipeline_status": pipeline_status == "deg_gsea_ok",
        "deg_sanity": deg_sanity == "ok",
        "run_terminal": run_terminal,
        "deg_artifacts": int(artifacts.get("deg", 0)) >= case["expected_n_contrasts"],
        "gsea_artifacts": int(artifacts.get("gsea", 0)) >= case["expected_n_contrasts"],
        "gsea_decisions": sum(
            item.get("step") == "gsea" and item.get("decision") == "ok" for item in decisions
        ) >= case["expected_n_contrasts"],
        "qc_artifact": bool(artifacts.get("qc")),
        "decision_log": bool(artifacts.get("decisions")),
    }
    blocking = sorted(name for name, passed in checks.items() if not passed)
    return {
        "checks": checks,
        "blocking": blocking,
        "passed": not blocking,
        "alignment": alignment,
        "observed_treatments": sorted(observed_treatments),
        "pipeline_status": pipeline_status,
    }


def run_policy_probes() -> dict[str, bool]:
    probes = {}
    fractional = pd.DataFrame([[1.2, 3.4], [0.1, 5.7]], columns=["S1", "S2"])
    raw = pd.DataFrame([[0, 500], [20, 10000]], columns=["S1", "S2"])
    metadata = pd.DataFrame(
        {"group": ["control", "treatment", "treatment"]},
        index=["C1", "T1", "T2"],
    )
    try:
        enforce_method_matrix_compatibility(fractional, method="deseq2")
        probes["deseq2_rejects_fractional"] = False
    except PolicyViolation:
        probes["deseq2_rejects_fractional"] = True
    try:
        enforce_method_matrix_compatibility(raw, method="limma")
        probes["limma_rejects_raw_counts"] = False
    except PolicyViolation:
        probes["limma_rejects_raw_counts"] = True
    try:
        select_valid_two_group_design(
            metadata,
            design_column="group",
            control_group="control",
            treatment_group="treatment",
            available_samples=metadata.index,
        )
        probes["underpowered_design_rejected"] = False
    except PolicyViolation:
        probes["underpowered_design_rejected"] = True
    return probes


def _case_artifacts(case_dir: Path) -> dict[str, int | bool]:
    return {
        "deg": len(list(case_dir.glob("DEG_results_*.csv"))),
        "gsea": len(list(case_dir.glob("*_GSEA_Hallmark.csv"))),
        "qc": bool(list(case_dir.glob("*_sample_qc.tsv"))),
        "decisions": (case_dir / "decisions.json").is_file(),
    }


def _hashes_match(case: dict) -> bool:
    matrix = ROOT / case["matrix_path"]
    metadata = ROOT / case["metadata_path"]
    return (
        matrix.is_file()
        and metadata.is_file()
        and file_sha256(str(matrix)) == case["matrix_sha256"]
        and file_sha256(str(metadata)) == case["metadata_sha256"]
    )


def _json_safe_row(row: dict) -> dict:
    safe = {}
    for key, value in row.items():
        if value is None or (not isinstance(value, (list, dict)) and pd.isna(value)):
            safe[str(key)] = None
        elif hasattr(value, "item"):
            safe[str(key)] = value.item()
        else:
            safe[str(key)] = value
    return safe


def _run_case(case: dict, out: Path, *, llm_datatype: bool = False) -> dict:
    run_label = case["id"]
    batch_root = out / "runs"
    fn = getattr(bt.run_batch_geo_pipeline, "func", bt.run_batch_geo_pipeline)
    fn(
        accessions=[case["accession"]],
        organism=case["organism"],
        treatment_keywords=case["treatment_keywords"],
        control_keywords=case["control_keywords"],
        output_base=str(batch_root),
        run_label=run_label,
        raw_da_method="deseq2",
        llm_datatype=llm_datatype,
        evaluate_subsets=False,
    )
    cohort = batch_root / f"cohort_{run_label}"
    summary_path = cohort / "summary.csv"
    if not summary_path.is_file():
        raise RuntimeError(f"Missing batch summary: {summary_path}")
    row = _json_safe_row(pd.read_csv(summary_path).iloc[0].to_dict())
    case_dir = cohort / case["accession"]
    decisions_path = case_dir / "decisions.json"
    decisions = _load_decisions(decisions_path)
    status_path = cohort / "run_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.is_file() else {}
    evaluation = evaluate_case(
        case,
        row,
        decisions,
        _case_artifacts(case_dir),
        hashes_match=_hashes_match(case),
        run_terminal=status.get("status") == "completed" and bool(status.get("finished_at")),
    )
    result = {
        "case_id": case["id"],
        "accession": case["accession"],
        "row": row,
        "case_dir": str(case_dir.resolve()),
        "cohort_dir": str(cohort.resolve()),
        "decisions_path": str(decisions_path.resolve()),
        "run_status_path": str(status_path.resolve()),
        **evaluation,
    }
    result_path = out / "case_results" / f"{case['id']}.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    result["result_path"] = str(result_path.resolve())
    return result


def _summary_row(result: dict) -> dict:
    row = result.get("row") or {}
    return {
        "case_id": result["case_id"],
        "accession": result["accession"],
        "status": "deg_gsea_ok" if result["passed"] else "failed_preflight",
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
        "checks_passed": sum(result["checks"].values()),
        "checks_total": len(result["checks"]),
        "blocking": ";".join(result["blocking"]),
    }


def _write_report(out: Path, manifest: dict, results: list[dict], probes: dict, usage: dict) -> dict:
    passing = sum(bool(item["passed"]) for item in results)
    all_probes = all(probes.values())
    expected = len(manifest["cases"])
    acceptance = {
        "all_six_cases_executed": len(results) == expected == 6,
        "all_six_cases_passed": passing == expected == 6,
        "all_policy_probes_passed": all_probes,
        "all_input_hashes_match": all(
            item["checks"].get("input_hashes_match", False) for item in results
        ),
        "all_matrix_method_routes_correct": all(
            item["checks"].get("matrix_method_compatible", False) for item in results
        ),
        "all_contrasts_correct": all(
            all(item["checks"].get(key, False) for key in (
                "design_column", "control_group", "treatment_set", "contrast_count"
            )) for item in results
        ),
        "all_live_gsea_completed": all(
            item["checks"].get("gsea_artifacts", False)
            and item["checks"].get("gsea_decisions", False)
            for item in results
        ),
        "zero_deg_sanity_flags": all(
            item["checks"].get("deg_sanity", False) for item in results
        ),
        "all_llm_usage_measured_and_priced": (
            usage["llm_calls"] == usage["usage_measured_calls"]
            and usage["unpriced_calls"] == 0
        ),
    }
    verdict = "preflight_pass" if all(acceptance.values()) else "preflight_fail"
    report = {
        "schema_version": "1.0",
        "experiment": "full_pipeline_six_case_preflight",
        "verdict": verdict,
        "case_count": expected,
        "executed_cases": len(results),
        "passing_cases": passing,
        "policy_probes": probes,
        "acceptance": acceptance,
        "blocking_findings": {
            item["case_id"]: item["blocking"] for item in results if item["blocking"]
        },
        "cases": results,
    }
    (out / "preflight_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    lines = [
        "# Full RNA-seq Pipeline Six-case Preflight",
        "",
        f"- Verdict: **{verdict}**",
        f"- Cases passed: **{passing}/{expected}**",
        f"- Policy probes passed: **{sum(probes.values())}/{len(probes)}**",
        "- Acquisition: **frozen cached inputs with SHA-256 verification**",
        "- Enrichment: **live Hallmark GSEA**",
        "",
        "## Acceptance",
        "",
    ]
    lines.extend(
        f"- {'PASS' if passed else 'FAIL'} — `{name}`"
        for name, passed in acceptance.items()
    )
    lines.extend(["", "## Cases", "", "| Case | Status | Blocking |", "|---|---|---|"])
    for item in results:
        lines.append(
            f"| {item['case_id']} | {'PASS' if item['passed'] else 'FAIL'} | "
            f"{', '.join(item['blocking']) or 'none'} |"
        )
    (out / "preflight_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def _write_evidence(out: Path, manifest_path: Path, report: dict, results: list[dict]) -> None:
    recorder = EvidenceRecorder(out.name, subject_id="rnaseq:full-pipeline:preflight")
    manifest_source = recorder.add_source(
        "artifact",
        "Frozen six-case full-pipeline manifest",
        uri=str(out / "frozen_preflight_manifest.json"),
        attributes={"sha256": file_sha256(str(out / "frozen_preflight_manifest.json"))},
    )
    protocol_source = recorder.add_source(
        "rule",
        "Preregistered six-case preflight protocol",
        uri=str(out / "PREREGISTERED_PROTOCOL.md"),
        attributes={"sha256": file_sha256(str(out / "PREREGISTERED_PROTOCOL.md"))},
    )
    decision = recorder.add_decision(
        "evaluate_full_pipeline_preflight",
        {"verdict": report["verdict"]},
        reason="Six frozen cached GEO studies evaluated against preregistered scientific hard gates.",
        method="rule",
        evidence_ids=[manifest_source, protocol_source],
        details=report["acceptance"],
    )
    root_artifacts = [
        (out / "frozen_preflight_manifest.json", "frozen manifest"),
        (out / "PREREGISTERED_PROTOCOL.md", "preregistered protocol"),
        (out / "summary.csv", "case summary"),
        (out / "preflight_report.json", "machine-readable preflight report"),
        (out / "preflight_report.md", "human-readable preflight report"),
        (out / "run_status.json", "root run status"),
        (out / "workflow.log", "root workflow log"),
        (out / "llm_usage.json", "structured LLM token and cost usage"),
    ]
    for path, role in root_artifacts:
        recorder.add_artifact(str(path), role, produced_by=decision)
    for result in results:
        result_path = Path(result["result_path"])
        recorder.add_artifact(str(result_path), f"case result {result['case_id']}", produced_by=decision)
        decisions_path = Path(result["decisions_path"])
        if decisions_path.is_file():
            recorder.add_artifact(
                str(decisions_path), f"case decisions {result['case_id']}", produced_by=decision
            )
    recorder.finish("completed" if report["verdict"] == "preflight_pass" else "partial")
    recorder.save(str(out / "evidence.json"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--provider", default="deepseek", choices=["deepseek", "anthropic"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--rerun", action="store_true")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("case_count") != 6 or len(manifest.get("cases") or []) != 6:
        raise SystemExit("The preflight manifest must contain exactly six frozen cases")
    invalid = [case["id"] for case in manifest["cases"] if not _hashes_match(case)]
    probes = run_policy_probes()
    if args.dry_run:
        print(json.dumps({
            "dry_run": "pass" if not invalid and all(probes.values()) else "fail",
            "invalid_input_hashes": invalid,
            "policy_probes": probes,
            "cases": [case["id"] for case in manifest["cases"]],
        }, indent=2, ensure_ascii=False))
        return 0 if not invalid and all(probes.values()) else 1
    if invalid:
        raise SystemExit(f"Frozen input hash mismatch: {invalid}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(args.output_dir).resolve() if args.output_dir else (
        ROOT / "output" / f"full_pipeline_preflight_{stamp}"
    )
    out.mkdir(parents=True, exist_ok=True)
    frozen = out / "frozen_preflight_manifest.json"
    if frozen.exists() and file_sha256(str(frozen)) != file_sha256(str(manifest_path)):
        raise SystemExit("Output directory contains a different frozen manifest")
    if not frozen.exists():
        shutil.copy2(manifest_path, frozen)
    protocol = Path(__file__).with_name("PREREGISTERED_PROTOCOL.md")
    shutil.copy2(protocol, out / protocol.name)

    tracker = RunStatusTracker(
        str(out / "run_status.json"),
        run_id=out.name,
        profile="full_pipeline_six_case_preflight",
        stages=("validate_inputs", "execute", "score", "report"),
        study_total=6,
    )
    tracker.start("six-case cached-input full pipeline preflight")
    tracker.set_stage("validate_inputs", message="frozen hashes and policy probes passed")
    os.environ["BIOAGENT_LLM_PROVIDER"] = args.provider
    os.environ["BIOAGENT_LLM_MODEL"] = (
        "deepseek-v4-pro" if args.provider == "deepseek" else "claude-sonnet-4-6"
    )
    if args.provider == "deepseek":
        os.environ["BIOAGENT_LLM_EFFORT"] = "max"

    original_download = bt.download_geo_data
    original_supplement = bt.download_supplementary_files
    bt.download_geo_data = _CachedAcquisitionTool("metadata")
    bt.download_supplementary_files = _CachedAcquisitionTool("supplementary")
    started = time.perf_counter()
    llm_usage_start = llm_usage_checkpoint()
    results = []
    workflow_lines = [
        "Full RNA-seq pipeline six-case preflight",
        f"manifest={manifest_path}",
        f"provider={args.provider}",
        "acquisition=frozen cached inputs",
        "enrichment=live Hallmark GSEA",
    ]
    try:
        selected_cases = manifest["cases"][: args.max_cases or None]
        tracker.set_stage("execute", message=f"running {len(selected_cases)} cases")
        for index, case in enumerate(selected_cases, 1):
            result_path = out / "case_results" / f"{case['id']}.json"
            print(f"[{index}/{len(selected_cases)}] {case['id']}", flush=True)
            if result_path.is_file() and not args.rerun:
                result = json.loads(result_path.read_text(encoding="utf-8"))
                result["result_path"] = str(result_path.resolve())
                print("  reused completed case result", flush=True)
            else:
                try:
                    result = _run_case(case, out)
                except Exception as exc:
                    tracker.add_failure(f"{case['id']}: {type(exc).__name__}: {exc}")
                    result = {
                        "case_id": case["id"],
                        "accession": case["accession"],
                        "row": {},
                        "passed": False,
                        "checks": {},
                        "blocking": ["execution_exception"],
                        "alignment": {},
                        "pipeline_status": "exception",
                        "execution_error": f"{type(exc).__name__}: {exc}",
                        "decisions_path": "",
                        "run_status_path": "",
                    }
                    result_path.parent.mkdir(parents=True, exist_ok=True)
                    result_path.write_text(
                        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
                    )
                    result["result_path"] = str(result_path.resolve())
            results.append(result)
            workflow_lines.append(
                f"{case['id']}: {'pass' if result['passed'] else 'fail'} "
                f"blocking={','.join(result.get('blocking') or []) or 'none'}"
            )
    finally:
        bt.download_geo_data = original_download
        bt.download_supplementary_files = original_supplement

    tracker.set_stage("score", message="writing aggregate deterministic scores")
    pd.DataFrame([_summary_row(item) for item in results]).to_csv(out / "summary.csv", index=False)
    usage = llm_usage_summary(llm_usage_start)
    report = _write_report(out, manifest, results, probes, usage)
    elapsed = round(time.perf_counter() - started, 3)
    tracker.set_usage(
        llm_calls=usage["llm_calls"], estimated_cost_usd=usage["estimated_cost_usd"]
    )
    (out / "llm_usage.json").write_text(
        json.dumps(usage, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    tracker.set_stage("report", message=report["verdict"])
    workflow_lines.extend([
        f"elapsed_seconds={elapsed}",
        f"llm_calls={usage['llm_calls']}",
        f"llm_input_tokens={usage['input_tokens']}",
        f"llm_output_tokens={usage['output_tokens']}",
        f"llm_cost_usd={usage['estimated_cost_usd']:.8f}",
        f"verdict={report['verdict']}",
    ])
    (out / "workflow.log").write_text("\n".join(workflow_lines) + "\n", encoding="utf-8")
    tracker.finish(
        "completed" if report["verdict"] == "preflight_pass" else "partial",
        report["verdict"],
    )
    _write_evidence(out, manifest_path, report, results)
    print(json.dumps({
        "verdict": report["verdict"],
        "passing_cases": report["passing_cases"],
        "case_count": report["case_count"],
        "policy_probes": probes,
        "elapsed_seconds": elapsed,
        "output_dir": str(out),
    }, indent=2, ensure_ascii=False))
    return 0 if report["verdict"] == "preflight_pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

