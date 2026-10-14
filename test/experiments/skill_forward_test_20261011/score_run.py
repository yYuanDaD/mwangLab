"""Score a round-3 blind run (nine cases) against answer_key.json.

Reuses the checks of skill_forward_test_20261010/score_run.py and adds the
modality checks (blocking alternatives, transforms, per-cell-type execution
subsets, executor exclusions, enrichment safety).

Usage:
    python score_run.py <runs_dir> [<runs_dir> ...]
"""
from __future__ import annotations

import argparse
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = runpy.run_path(str(HERE.parent / "skill_forward_test_20261010" / "score_run.py"))
collect_records, text, by_stage, base_score = (BASE["collect_records"], BASE["text"], BASE["by_stage"],
                                               BASE["score_case"])
READY_IDS = {"gene_symbol", "ensembl_gene"}


def score_case(records, key):
    key = dict(key)
    extra = {k: key.pop(k) for k in list(key) if k in {
        "matrix_any", "blocking_any", "transform_any", "execution_subset_excludes", "min_executions",
        "execution_text_excludes", "enrichment_safe"}}
    if "matrix_any" in extra:
        key["matrix"] = ""  # base check passes; real check below
    checks = base_score(records, key)
    if extra.get("matrix_any"):
        matrix = text([r.get("final", {}).get("matrix_type") for r in by_stage(records, "matrix")])
        checks["matrix_type"] = any(m in matrix for m in extra["matrix_any"])
    covariance = by_stage(records, "covariance")
    if extra.get("blocking_any"):
        terms = text([r.get("final", {}).get("blocking_terms") for r in covariance])
        checks["blocking_term"] = any(t in terms for t in extra["blocking_any"])
    if extra.get("transform_any"):
        transforms = text([r.get("final", {}).get("transform") for r in by_stage(records, "method")])
        checks["transform"] = any(t in transforms for t in extra["transform_any"])
    executions = by_stage(records, "execution")
    if extra.get("execution_subset_excludes"):
        checks["skipped_subset_not_run"] = not any(
            extra["execution_subset_excludes"] in str(r.get("final", {}).get("subset", "")).lower() for r in executions)
    if extra.get("min_executions"):
        checks["one_execution_per_subset"] = len(executions) >= extra["min_executions"]
    if extra.get("execution_text_excludes"):
        checks["executor_choice"] = extra["execution_text_excludes"] not in text([r.get("final") for r in executions])
    if extra.get("enrichment_safe"):
        unsafe = [r for r in by_stage(records, "enrichment") if r.get("decision_status") == "valid"
                  and str(r.get("final", {}).get("feature_id_type", "")).lower() not in READY_IDS
                  and not r.get("final", {}).get("id_mapping")]
        checks["enrichment_safe"] = not unsafe
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--key", type=Path, default=HERE / "answer_key.json")
    args = parser.parse_args()
    key = json.loads(args.key.read_text(encoding="utf-8"))["cases"]
    report = {}
    for runs in args.runs:
        per_case = {case_id: score_case(collect_records(runs / case_id), case_key)
                    for case_id, case_key in key.items()}
        passed = sum(all(v.values()) for v in per_case.values())
        report[str(runs)] = {"cases_all_checks_pass": f"{passed}/{len(key)}", "cases": per_case}
        print(f"{runs}: {passed}/{len(key)} cases pass every check")
        for case_id, checks in per_case.items():
            failed = [k for k, v in checks.items() if not v]
            print(f"  {case_id}: {'PASS' if not failed else 'FAIL ' + ', '.join(failed)} ({len(checks)} checks)")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
