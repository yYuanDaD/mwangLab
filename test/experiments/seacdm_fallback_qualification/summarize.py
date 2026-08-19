"""Consolidate the bounded fallback runs, including failed-call cost, for independent audit."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.evidence import EvidenceRecorder, file_sha256  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402


def load_report(path: Path) -> dict:
    return json.loads((path / "qualification_report.json").read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial-run", required=True)
    parser.add_argument("--retry-run", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    initial_dir = Path(args.initial_run).resolve()
    retry_dir = Path(args.retry_run).resolve()
    out = Path(args.output_dir).resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty directory: {out}")
    out.mkdir(parents=True, exist_ok=True)
    initial = load_report(initial_dir)
    retry = load_report(retry_dir)
    initial_rows = {row["study_id"]: row for row in initial["records"]}
    retry_rows = {row["study_id"]: row for row in retry["records"]}
    final_rows = [initial_rows["GSE319603"], retry_rows["GSE318937"],
                  initial_rows["GSE282166"]]
    total_cost = round(float(initial["total_cost_usd"]) + float(retry["total_cost_usd"]), 6)
    total_calls = int(initial["actual_paid_calls"]) + int(retry["actual_paid_calls"])
    successful_paid = sum(
        row["called_opus"] and row["status"] == "success" for row in final_rows
    )
    report = {
        "schema_version": "1.0",
        "model": "claude-opus-5",
        "verdict": "pass" if all(row["status"] == "success" for row in final_rows) else "fail",
        "final_cases_passed": sum(row["status"] == "success" for row in final_rows),
        "final_cases": len(final_rows),
        "successful_paid_fallback_cases": successful_paid,
        "negative_routes_skipped": sum(not row["called_opus"] for row in final_rows),
        "all_billable_calls_including_parse_failure": total_calls,
        "all_cost_usd_including_parse_failure": total_cost,
        "compatibility_failure": {
            "study_id": "GSE318937",
            "reason": "provider wrapped experiment_control as {value, source}",
            "fixed_and_retried": True,
            "failed_call_cost_usd": initial_rows["GSE318937"]["cost_usd"],
        },
        "final_records": final_rows,
        "source_runs": [str(initial_dir), str(retry_dir)],
    }
    report_path = out / "qualification_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    summary_rows = [{
        "study_id": row["study_id"], "status": row["status"], "mode": row["mode"],
        "called_opus": row["called_opus"], "blocking": ";".join(row["blocking"]),
        "llm_calls": row["llm_calls"], "cost_usd": row["cost_usd"],
        "elapsed_seconds": row["elapsed_seconds"],
    } for row in final_rows]
    pd.DataFrame(summary_rows).to_csv(out / "summary.csv", index=False)
    markdown = [
        "# Opus 5 SEA-CDM fallback qualification", "",
        f"- Verdict: **{report['verdict']}**",
        f"- Final cases passed: **{report['final_cases_passed']}/{report['final_cases']}**",
        f"- Successful paid fallback cases: **{successful_paid}/2**",
        f"- Negative routes skipped: **{report['negative_routes_skipped']}/1**",
        f"- All billable calls: **{total_calls}**",
        f"- Total cost including failed parse: **${total_cost:.6f}**", "",
        "| Study | Mode | Final | Opus call | Cost |", "|---|---|---:|---:|---:|",
    ]
    for row in final_rows:
        markdown.append(
            f"| {row['study_id']} | {row['mode']} | {row['status']} | "
            f"{'yes' if row['called_opus'] else 'no'} | ${float(row['cost_usd']):.6f} |"
        )
    markdown.extend([
        "", "The first GSE318937 call was billable but failed schema parsing. Its cost remains in "
        "the total; a provider-compatibility coercion was added before the successful retry.",
        "", "One run per paid case does not measure stochastic stability.",
    ])
    md_path = out / "qualification_summary.md"
    md_path.write_text("\n".join(markdown) + "\n", encoding="utf-8")
    workflow = out / "workflow.log"
    workflow.write_text(
        f"{datetime.now().isoformat()} consolidated {initial_dir.name} + {retry_dir.name}\n"
        f"verdict={report['verdict']} calls={total_calls} cost=${total_cost:.6f}\n",
        encoding="utf-8",
    )
    evidence = EvidenceRecorder(out.name, subject_id="seacdm:fallback:opus5:qualification")
    source_ids = []
    for run_dir in (initial_dir, retry_dir):
        path = run_dir / "qualification_report.json"
        source_ids.append(evidence.add_source(
            "artifact", f"source run {run_dir.name}", uri=str(path),
            attributes={"sha256": file_sha256(str(path))},
        ))
    decision = evidence.add_decision(
        "qualify_opus5_fallback", {"verdict": report["verdict"], "model": report["model"]},
        reason="Two targeted repairs passed and the negative scope case skipped paid fallback.",
        method="hybrid", evidence_ids=source_ids,
        details={"calls": total_calls, "cost_usd": total_cost},
    )
    for path, role in ((report_path, "qualification report"),
                       (out / "summary.csv", "qualification summary"),
                       (md_path, "human-readable qualification"),
                       (workflow, "workflow log")):
        evidence.add_artifact(str(path), role, produced_by=decision, evidence_ids=source_ids)
    for row in final_rows:
        if row.get("tables_path"):
            evidence.add_artifact(row["tables_path"], f"final {row['study_id']} tables",
                                  produced_by=decision, evidence_ids=source_ids)
    evidence.finish("completed" if report["verdict"] == "pass" else "partial")
    evidence.save(str(out / "evidence.json"))
    tracker = RunStatusTracker(
        str(out / "run_status.json"), run_id=out.name,
        profile="seacdm_opus5_fallback_qualification", stages=["route", "fallback", "report"],
    )
    tracker.start("Consolidated Opus 5 fallback qualification")
    tracker.set_stage("route", message="negative route passed")
    tracker.set_stage("fallback", message="2/2 final fallback cases passed")
    tracker.set_stage("report", message="evidence consolidated")
    tracker.set_usage(llm_calls=total_calls, estimated_cost_usd=total_cost)
    tracker.finish("completed" if report["verdict"] == "pass" else "partial",
                   f"{report['final_cases_passed']}/{report['final_cases']} passed")
    print(json.dumps({"output_dir": str(out), "verdict": report["verdict"],
                      "cost_usd": total_cost, "calls": total_calls}, indent=2))
    return 0 if report["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
