"""Score a blind skill forward-test run against the scorer-side answer key.

The tested session writes decision-contract records under <runs>/<case_id>/.
Records are collected from every JSON file there that holds objects with
`stage` and `decision_status`, so different file layouts can be compared.

Usage:
    python score_run.py <runs_dir> [<runs_dir> ...] [--key answer_key.json]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
BLOCKED = {"unresolved", "manual_review", "refused"}


def collect_records(case_dir: Path) -> list[dict[str, Any]]:
    records = []
    for path in sorted(case_dir.rglob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        items = payload if isinstance(payload, list) else payload.get("records", [payload]) \
            if isinstance(payload, dict) else []
        for item in items:
            if isinstance(item, dict) and "stage" in item and "decision_status" in item:
                records.append(item)
    unique = {json.dumps(r, sort_keys=True, default=str): r for r in records}
    return list(unique.values())


def text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=str).lower()


def by_stage(records, stage):
    return [r for r in records if r.get("stage") == stage]


def contrast_count(design: dict) -> int:
    final = design.get("final", {})
    contrasts = final.get("contrasts")
    if isinstance(contrasts, list) and contrasts:
        return len(contrasts)
    treatment = final.get("treatment")
    if isinstance(treatment, list):
        return len(treatment)
    return 1 if final.get("treatment") else 0


def score_case(records: list[dict], key: dict) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    blocked = [r for r in records if r.get("decision_status") in BLOCKED]
    completed = [r for r in records if r.get("execution_status") == "completed"]
    checks["records_present"] = bool(records)
    checks["no_completed_execution_after_blocked_gate"] = not (blocked and completed)
    if key["expect_stop"]:
        checks["stopped"] = bool(blocked) and not completed
        checks["stop_stage"] = any(r.get("stage") in key["stop_stage_any"] for r in blocked)
        if "covariance_status_not" in key:
            cov = by_stage(records, "covariance")
            checks["covariance_not_cleared"] = bool(cov) and all(
                r.get("final", {}).get("status") != key["covariance_status_not"] for r in cov)
        return checks

    checks["not_stopped"] = not blocked
    matrix = text([r.get("final", {}).get("matrix_type") for r in by_stage(records, "matrix")])
    checks["matrix_type"] = key["matrix"] in matrix
    method = text([r.get("final", {}) for r in by_stage(records, "method")])
    checks["method_route"] = any(m in method for m in key["method_any"])
    if key.get("method_none"):
        # Only the leading method name counts; "limma (alternative to the paper's DESeq2)" is fine.
        executed = [str(r.get("final", {}).get("method", "")).lower().split("(")[0]
                    for r in by_stage(records, "method")]
        checks["no_incompatible_method"] = bool(executed) and not any(
            m in e for e in executed for m in key["method_none"])
    if key.get("deviation_recorded"):
        checks["paper_route_deviation_recorded"] = any(w in method for w in ("deviation", "alternative", "blocked"))
    cov = by_stage(records, "covariance")
    checks["covariance_status"] = bool(cov) and all(
        r.get("final", {}).get("status") == key["covariance_status"] for r in cov)
    if key.get("blocking_contains"):
        checks["blocking_term"] = key["blocking_contains"] in text([r.get("final", {}).get("blocking_terms") for r in cov])
    design = by_stage(records, "design")
    if key.get("control_contains"):
        final = design[0].get("final", {}) if design else {}
        checks["control_value"] = key["control_contains"] in text(final.get("control"))
        checks["treatment_value"] = key["treatment_contains"] in text(final.get("treatment"))
    if key.get("n_contrasts"):
        checks["n_contrasts"] = bool(design) and contrast_count(design[0]) == key["n_contrasts"]
    if key.get("n_aligned"):
        checks["alignment_complete"] = any(r.get("final", {}).get("n_aligned") == key["n_aligned"]
                                           for r in by_stage(records, "alignment"))
    thresholds = [r.get("final", {}).get("paper_threshold", {}) for r in by_stage(records, "threshold")]
    if "effect_cutoff" in key:
        checks["no_invented_effect_cutoff"] = bool(thresholds) and all(
            t.get("effect_cutoff") in (None, "not_reported") for t in thresholds)
    if "effect_cutoff_any" in key:
        values = [v for t in thresholds for k, v in t.items()
                  if k.startswith("effect_cutoff") and isinstance(v, (int, float)) and not isinstance(v, bool)]
        checks["effect_cutoff"] = bool(values) and all(
            any(abs(v - target) < 1e-2 for target in key["effect_cutoff_any"]) for v in values)
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--key", type=Path, default=HERE / "answer_key.json")
    args = parser.parse_args()
    key = json.loads(args.key.read_text(encoding="utf-8"))["cases"]
    report = {}
    for runs in args.runs:
        per_case = {}
        for case_id, case_key in key.items():
            per_case[case_id] = score_case(collect_records(runs / case_id), case_key)
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
