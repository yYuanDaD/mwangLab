"""Validate one or more bioinformatics decision-contract JSON records.

This is intentionally deterministic and checks structure/invariants only. It
does not judge whether a biological decision is scientifically correct.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STAGES = {
    "paper_reconstruction", "matrix", "alignment", "design", "method",
    "covariance", "threshold", "execution",
}
DECISIONS = {"valid", "unresolved", "manual_review", "refused"}
EXECUTIONS = {"not_started", "completed", "failed", "not_run"}


def _check(record: dict[str, Any], source: str) -> list[str]:
    errors: list[str] = []
    required = {
        "case_id", "stage", "evidence", "candidates", "final", "confidence",
        "reasoning", "decision_status", "execution_status", "stop_reason",
    }
    missing = sorted(required - set(record))
    if missing:
        errors.append(f"{source}: missing {', '.join(missing)}")
        return errors
    if not isinstance(record["case_id"], str) or not record["case_id"].strip():
        errors.append(f"{source}: case_id must be a non-empty string")
    if record["stage"] not in STAGES:
        errors.append(f"{source}: invalid stage {record['stage']!r}")
    if record["decision_status"] not in DECISIONS:
        errors.append(f"{source}: invalid decision_status {record['decision_status']!r}")
    if record["execution_status"] not in EXECUTIONS:
        errors.append(f"{source}: invalid execution_status {record['execution_status']!r}")
    if record["confidence"] not in {"high", "medium", "low"}:
        errors.append(f"{source}: confidence must be high, medium, or low")
    if not isinstance(record["evidence"], list) or not record["evidence"]:
        errors.append(f"{source}: evidence must be a non-empty list")
    if not isinstance(record["candidates"], list):
        errors.append(f"{source}: candidates must be a list")
    if not isinstance(record["final"], dict):
        errors.append(f"{source}: final must be an object")
    if record["stage"] == "paper_reconstruction":
        required_paper = {"accessions", "primary_estimand", "planned_contrasts", "paper_threshold"}
        missing_paper = sorted(required_paper - set(record["final"]))
        if missing_paper:
            errors.append(f"{source}: paper reconstruction missing {', '.join(missing_paper)}")
        if not isinstance(record["final"].get("paper_threshold"), dict):
            errors.append(f"{source}: paper_threshold must be an object")
    if record["stage"] == "threshold":
        if "paper_threshold" not in record["final"]:
            errors.append(f"{source}: threshold decision needs paper_threshold")
    if record["decision_status"] in {"unresolved", "manual_review", "refused"}:
        if not record.get("stop_reason"):
            errors.append(f"{source}: unresolved/review/refused decision needs stop_reason")
        if record["execution_status"] == "completed":
            errors.append(f"{source}: blocked decision cannot have completed execution")
    if record["decision_status"] == "valid" and record.get("stop_reason"):
        errors.append(f"{source}: valid decision cannot have stop_reason")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", nargs="+", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    count = 0
    for path in args.records:
        payload = json.loads(path.read_text(encoding="utf-8"))
        items = payload if isinstance(payload, list) else [payload]
        for index, record in enumerate(items):
            count += 1
            if not isinstance(record, dict):
                errors.append(f"{path}[{index}]: record must be an object")
                continue
            errors.extend(_check(record, f"{path}[{index}]"))
    if errors:
        print("INVALID")
        print("\n".join(errors))
        return 1
    print(f"VALID ({count} decision records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
