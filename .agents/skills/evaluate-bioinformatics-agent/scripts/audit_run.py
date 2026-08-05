#!/usr/bin/env python3
"""Deterministically audit a mwangLab agent run directory."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


TERMINAL_STATUSES = {"completed", "partial", "failed"}
SUCCESS_TOKENS = ("ok", "completed", "success")
FAILURE_TOKENS = ("exception", "failed", "error")
BLOCKING_CHECKS = {
    "run_terminal", "study_completion", "matrix_method_compatibility",
    "contrast_definition", "deg_sanity", "evidence_references", "artifact_integrity",
}


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _number(value: Any) -> float | None:
    try:
        if value is None or str(value).strip().lower() in {"", "nan", "none"}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _check(check_id: str, dimension: str, status: str, points: float, maximum: float,
           detail: str, remediation: str = "") -> dict[str, Any]:
    return {
        "id": check_id,
        "dimension": dimension,
        "status": status,
        "points": round(points, 2),
        "max_points": maximum,
        "blocking": check_id in BLOCKING_CHECKS and status == "fail",
        "detail": detail,
        "remediation": remediation,
    }


def _resolve_artifact(raw: str, evidence_path: Path, run_dir: Path) -> Path | None:
    candidate = Path(raw)
    choices = [candidate] if candidate.is_absolute() else [
        run_dir / candidate, evidence_path.parent / candidate, Path.cwd() / candidate,
    ]
    return next((path.resolve() for path in choices if path.is_file()), None)


def _audit_evidence(run_dir: Path, evidence_paths: list[Path]) -> list[dict[str, Any]]:
    if not evidence_paths:
        return [
            _check("evidence_references", "provenance", "not_measured", 0, 10,
                   "No evidence.json found.", "Emit one evidence bundle per analyzed study."),
            _check("artifact_integrity", "provenance", "not_measured", 0, 10,
                   "No evidence artifact records found.", "Record artifact paths and SHA-256 hashes."),
            _check("decision_grounding", "provenance", "not_measured", 0, 5,
                   "No decisions or claims were available for grounding checks."),
        ]

    dangling: list[str] = []
    duplicate_ids: list[str] = []
    invalid_files: list[str] = []
    artifacts_total = artifacts_verified = artifacts_missing = hash_mismatch = 0
    grounded_total = grounded = 0

    for path in evidence_paths:
        try:
            bundle = _read_json(path)
        except Exception as exc:  # keep auditing other bundles
            invalid_files.append(f"{path}: {type(exc).__name__}: {exc}")
            continue
        groups = [bundle.get(name) or [] for name in ("sources", "claims", "decisions", "artifacts")]
        ids: list[str] = []
        for records in groups:
            for record in records:
                for key in ("source_id", "claim_id", "decision_id", "artifact_id"):
                    if record.get(key):
                        ids.append(str(record[key]))
                        break
        seen: set[str] = set()
        for item in ids:
            if item in seen:
                duplicate_ids.append(item)
            seen.add(item)
        source_ids = {str(x.get("source_id")) for x in bundle.get("sources", [])
                      if x.get("source_id")}
        claim_ids = {str(x.get("claim_id")) for x in bundle.get("claims", [])
                     if x.get("claim_id")}
        artifact_ids = {str(x.get("artifact_id")) for x in bundle.get("artifacts", [])
                        if x.get("artifact_id")}
        valid_refs = source_ids | claim_ids | artifact_ids
        decision_ids = {str(x.get("decision_id")) for x in bundle.get("decisions", [])
                        if x.get("decision_id")}
        for group_name in ("claims", "decisions", "artifacts"):
            for record in bundle.get(group_name, []) or []:
                refs = [str(x) for x in record.get("evidence_ids", [])]
                if group_name in {"claims", "decisions"}:
                    grounded_total += 1
                    grounded += bool(refs)
                dangling.extend(f"{path.name}:{group_name}:{ref}" for ref in refs
                                if ref not in valid_refs)
                produced_by = record.get("produced_by")
                if produced_by and str(produced_by) not in decision_ids:
                    dangling.append(f"{path.name}:produced_by:{produced_by}")
        for artifact in bundle.get("artifacts", []) or []:
            artifacts_total += 1
            resolved = _resolve_artifact(str(artifact.get("path", "")), path, run_dir)
            if resolved is None:
                artifacts_missing += 1
                continue
            expected = str(artifact.get("sha256") or "")
            if expected:
                if _sha256(resolved).lower() == expected.lower():
                    artifacts_verified += 1
                else:
                    hash_mismatch += 1

    reference_ok = not (invalid_files or duplicate_ids or dangling)
    ref_detail = (f"bundles={len(evidence_paths)}, invalid={len(invalid_files)}, "
                  f"duplicate_ids={len(duplicate_ids)}, dangling_refs={len(dangling)}")
    if hash_mismatch:
        artifact_status, artifact_points = "fail", 0
    elif artifacts_missing:
        artifact_status, artifact_points = "warn", 5 * artifacts_verified / max(1, artifacts_total)
    elif artifacts_total and artifacts_verified == artifacts_total:
        artifact_status, artifact_points = "pass", 10
    elif artifacts_total:
        artifact_status, artifact_points = "warn", 5
    else:
        artifact_status, artifact_points = "not_measured", 0
    artifact_detail = (f"artifacts={artifacts_total}, hash_verified={artifacts_verified}, "
                       f"missing={artifacts_missing}, hash_mismatch={hash_mismatch}")
    if grounded_total:
        ratio = grounded / grounded_total
        grounding_status, grounding_points = ("pass" if ratio == 1 else "warn"), 5 * ratio
        grounding_detail = f"grounded claims/decisions={grounded}/{grounded_total}"
    else:
        grounding_status, grounding_points, grounding_detail = "not_measured", 0, "No claims or decisions found."
    return [
        _check("evidence_references", "provenance", "pass" if reference_ok else "fail",
               10 if reference_ok else 0, 10, ref_detail,
               "Repair duplicate or dangling evidence identifiers."),
        _check("artifact_integrity", "provenance", artifact_status, artifact_points, 10,
               artifact_detail, "Preserve artifacts and record verifiable SHA-256 hashes."),
        _check("decision_grounding", "provenance", grounding_status, grounding_points, 5,
               grounding_detail, "Attach evidence_ids to every scientific claim and decision."),
    ]


def _audit_summary(summary_path: Path | None) -> list[dict[str, Any]]:
    if summary_path is None:
        return [
            _check("study_completion", "execution", "not_measured", 0, 8, "No root summary.csv found."),
            _check("matrix_method_compatibility", "scientific_validity", "not_measured", 0, 8,
                   "No matrix_type/da_method rows found."),
            _check("contrast_definition", "scientific_validity", "not_measured", 0, 6,
                   "No per-study contrast rows found."),
            _check("deg_sanity", "scientific_validity", "not_measured", 0, 8,
                   "No DEG sanity field found."),
        ]
    rows = _read_csv(summary_path)
    if not rows:
        return [_check("study_completion", "execution", "fail", 0, 8,
                       "summary.csv has no rows.", "Write one row per requested study.")]

    statuses = [str(row.get("status", "")).lower() for row in rows]
    failed = sum(any(token in status for token in FAILURE_TOKENS) for status in statuses)
    successful = sum(any(token in status for token in SUCCESS_TOKENS) for status in statuses)
    completion_status = "fail" if failed else "pass" if successful == len(rows) else "warn"
    checks = [_check("study_completion", "execution", completion_status,
                     8 * successful / len(rows), 8,
                     f"successful={successful}/{len(rows)}, failed={failed}",
                     "Inspect failed or partial rows and failures.log.")]

    has_route = all("matrix_type" in row and ("da_method" in row or "da_methods_run" in row)
                    for row in rows)
    if not has_route:
        checks.append(_check("matrix_method_compatibility", "scientific_validity", "not_measured", 0, 8,
                             "Summary does not expose matrix_type and DA method."))
    else:
        incompatible: list[str] = []
        for idx, row in enumerate(rows, start=1):
            matrix = str(row.get("matrix_type", "")).lower()
            method = str(row.get("da_methods_run") or row.get("da_method") or "").lower()
            if not method:
                continue
            raw_ok = any(x in method for x in ("deseq2", "edger", "voom"))
            log_ok = "limma" in method and "voom" not in method
            if "raw" in matrix and not raw_ok:
                incompatible.append(f"row {idx}: {matrix}->{method}")
            if any(x in matrix for x in ("fpkm", "tpm", "log", "proteom", "methyl")) and not log_ok:
                incompatible.append(f"row {idx}: {matrix}->{method}")
        checks.append(_check("matrix_method_compatibility", "scientific_validity",
                             "fail" if incompatible else "pass", 0 if incompatible else 8, 8,
                             "incompatible routes: " + "; ".join(incompatible) if incompatible
                             else f"Checked {len(rows)} matrix/method routes.",
                             "Route counts to count-aware DA and log-scale values to limma."))

    da_rows = [row for row in rows if _number(row.get("n_deg")) is not None
               or "deg_" in str(row.get("status", ""))]
    if not da_rows:
        checks.append(_check("contrast_definition", "scientific_validity", "not_measured", 0, 6,
                             "No successful DA rows were present."))
    else:
        missing = [row for row in da_rows if not all(str(row.get(key, "")).strip()
                                                     for key in ("design_col", "control", "treatment"))]
        checks.append(_check("contrast_definition", "scientific_validity",
                             "fail" if missing else "pass", 0 if missing else 6, 6,
                             f"DA rows={len(da_rows)}, missing contrast fields={len(missing)}",
                             "Record design_col, control, and treatment for every DA result."))

    if not da_rows or not all("deg_sanity" in row for row in da_rows):
        checks.append(_check("deg_sanity", "scientific_validity", "not_measured", 0, 8,
                             "DEG sanity was not recorded for every DA row."))
    else:
        flagged = [str(row.get("deg_sanity", "")) for row in da_rows
                   if str(row.get("deg_sanity", "")).strip().lower() not in {"", "ok"}]
        checks.append(_check("deg_sanity", "scientific_validity",
                             "fail" if flagged else "pass", 0 if flagged else 8, 8,
                             "flags: " + "; ".join(flagged) if flagged else "All DA rows passed sanity checks.",
                             "Review sample size, normalization, model fit, and DEG fraction."))
    return checks


def _audit_stability(run_dir: Path) -> list[dict[str, Any]]:
    candidates = [path for path in run_dir.rglob("*_summary.json") if "evaluation" in path.parts]
    usable: list[dict[str, Any]] = []
    for path in candidates:
        try:
            payload = _read_json(path)
            if payload.get("deg") or payload.get("gsea"):
                usable.append(payload)
        except Exception:
            continue
    if not usable:
        return [_check("subset_stability", "reproducibility", "not_measured", 0, 10,
                       "No repeated or subset evaluation summary found.",
                       "Run at least three stratified subset reruns for important contrasts.")]
    verdicts = [str(item.get("judge", {}).get("verdict", "unknown")).lower() for item in usable]
    stable = sum(verdict == "stable" for verdict in verdicts)
    return [_check("subset_stability", "reproducibility",
                   "pass" if stable == len(verdicts) else "warn",
                   10 * stable / len(verdicts), 10,
                   f"stable verdicts={stable}/{len(verdicts)} ({', '.join(verdicts)})")]


def audit_run(run_dir: str | Path) -> dict[str, Any]:
    root = Path(run_dir).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Run directory not found: {root}")
    checks: list[dict[str, Any]] = []
    status_path = root / "run_status.json"
    if status_path.is_file():
        status = _read_json(status_path)
        run_state = str(status.get("status", "")).lower()
        terminal = run_state in TERMINAL_STATUSES
        points = 8 if run_state == "completed" and status.get("finished_at") else 4 if terminal else 0
        terminal_result = "pass" if points == 8 else "warn" if run_state == "partial" else "fail"
        checks.append(_check("run_terminal", "execution", terminal_result,
                             points, 8,
                             f"status={status.get('status')}, stage={status.get('stage')}, "
                             f"finished_at={status.get('finished_at')}",
                             "Finish the tracker with completed, partial, or failed status."))
        total = _number(status.get("stage_total")) or 0
        completed = len(status.get("completed_stages") or [])
        ratio = min(1.0, completed / total) if total else 0
        checks.append(_check("stage_completion", "execution",
                             "pass" if total and ratio == 1 else "warn", 5 * ratio, 5,
                             f"completed_stages={completed}/{int(total) if total else 0}"))
        has_usage = (_number(status.get("elapsed_seconds")) is not None
                     and "llm_calls" in status and "estimated_cost_usd" in status)
        checks.append(_check("usage_accounting", "efficiency", "pass" if has_usage else "not_measured",
                             6 if has_usage else 0, 6,
                             f"elapsed={status.get('elapsed_seconds')}, llm_calls={status.get('llm_calls')}, "
                             f"cost_usd={status.get('estimated_cost_usd')}"))
        consistent = int(status.get("failure_count") or 0) == 0 or status.get("status") in {"partial", "failed"}
        checks.append(_check("failure_accounting", "execution", "pass" if consistent else "warn",
                             4 if consistent else 2, 4,
                             f"status={status.get('status')}, failures={status.get('failure_count')}, "
                             f"warnings={status.get('warning_count')}"))
    else:
        checks.extend([
            _check("run_terminal", "execution", "not_measured", 0, 8, "No run_status.json found."),
            _check("stage_completion", "execution", "not_measured", 0, 5, "No stage tracker found."),
            _check("usage_accounting", "efficiency", "not_measured", 0, 6,
                   "No elapsed time or call/cost tracker found."),
            _check("failure_accounting", "execution", "not_measured", 0, 4,
                   "No warning or failure counters found."),
        ])

    summary_path = root / "summary.csv" if (root / "summary.csv").is_file() else None
    checks.extend(_audit_summary(summary_path))
    checks.extend(_audit_evidence(root, list(root.rglob("evidence.json"))))
    checks.extend(_audit_stability(root))

    core_files = [root / "workflow.log", root / "summary.csv", root / "run_status.json"]
    present = sum(path.is_file() for path in core_files)
    checks.append(_check("reproducibility_artifacts", "reproducibility",
                         "pass" if present == len(core_files) else "warn",
                         4 * present / len(core_files), 4,
                         f"core artifacts present={present}/{len(core_files)}"))

    evaluated = [item for item in checks if item["status"] != "not_measured"]
    earned = sum(float(item["points"]) for item in evaluated)
    available = sum(float(item["max_points"]) for item in evaluated)
    total = sum(float(item["max_points"]) for item in checks)
    score = round(100 * earned / available, 1) if available else 0.0
    coverage = round(100 * available / total, 1) if total else 0.0
    blockers = [item for item in checks if item["blocking"]]
    if blockers:
        verdict = "fail"
    elif coverage < 60:
        verdict = "insufficient_evidence"
    elif score >= 85:
        verdict = "pass"
    elif score >= 70:
        verdict = "caution"
    else:
        verdict = "fail"

    dimensions: dict[str, dict[str, float]] = {}
    for item in checks:
        bucket = dimensions.setdefault(item["dimension"],
                                       {"earned": 0.0, "available": 0.0, "total": 0.0})
        bucket["total"] += float(item["max_points"])
        if item["status"] != "not_measured":
            bucket["earned"] += float(item["points"])
            bucket["available"] += float(item["max_points"])
    for bucket in dimensions.values():
        bucket["score"] = round(100 * bucket["earned"] / bucket["available"], 1) if bucket["available"] else 0.0
        bucket["coverage"] = round(100 * bucket["available"] / bucket["total"], 1) if bucket["total"] else 0.0

    return {
        "schema_version": "1.0", "run_dir": str(root), "verdict": verdict,
        "score": score, "coverage": coverage,
        "blocking_findings": [item["id"] for item in blockers],
        "dimensions": dimensions, "checks": checks,
    }


def _markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Agent run evaluation", "", f"- Verdict: **{report['verdict']}**",
        f"- Observed score: **{report['score']}/100**",
        f"- Evidence coverage: **{report['coverage']}%**",
        f"- Blocking findings: {', '.join(report['blocking_findings']) or 'none'}",
        "", "## Dimensions", "", "| Dimension | Score | Coverage |", "|---|---:|---:|",
    ]
    for name, values in report["dimensions"].items():
        lines.append(f"| {name} | {values['score']} | {values['coverage']}% |")
    lines.extend(["", "## Checks", "", "| Check | Status | Points | Detail |",
                  "|---|---|---:|---|"])
    for item in report["checks"]:
        detail = str(item["detail"]).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {item['id']} | {item['status']} | "
                     f"{item['points']}/{item['max_points']} | {detail} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, help="Completed run directory to audit")
    parser.add_argument("--output-dir", help="Defaults to the run directory")
    parser.add_argument("--no-write", action="store_true", help="Print JSON only")
    args = parser.parse_args()
    report = audit_run(args.run_dir)
    if not args.no_write:
        output = Path(args.output_dir).resolve() if args.output_dir else Path(args.run_dir).resolve()
        output.mkdir(parents=True, exist_ok=True)
        (output / "agent_evaluation.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        (output / "agent_evaluation.md").write_text(_markdown(report), encoding="utf-8")
    print(json.dumps({key: report[key] for key in
                      ("verdict", "score", "coverage", "blocking_findings")},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
