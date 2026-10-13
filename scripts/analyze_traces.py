"""Summarize decision traces from one or many native skill runs.

    python scripts/analyze_traces.py <run_dir_or_parent> [...] --out <dir>

A run is any folder holding run_manifest.json. For each run the script reads
trace.jsonl (written by tools/native.py) and every <case>/decisions.json. Runs
recorded before tracing existed still contribute their decisions; tool and
rejection statistics then cover only traced runs.

Outputs in --out:
  trace_summary.json   all statistics
  trace_summary.md     the same, readable
  review_sheet.csv     one row per case and gate, with empty reviewer columns

What it answers:
  - where agents stop, at which gate, and why;
  - where agents hesitate: low or medium confidence, revised decisions (and which
    fields changed), records the decision contract rejected;
  - which tools fail and how long they take;
  - the usual order of actions (transitions between gates and tool calls).
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.decision_contract import BLOCKED, STAGES  # noqa: E402


def decision_slot(stage: str, final: dict) -> tuple:
    """Same rule as tools.native.decision_slot, without importing pandas."""
    final = final or {}
    if stage == "enrichment":
        return (stage, str(final.get("method") or "").split("(")[0].strip().lower())
    if stage == "execution":
        return (stage, str(final.get("subset") or ""))
    return (stage,)

REVIEW_COLUMNS = [
    "run_id", "case_id", "accession", "stage", "record_index", "decision_status", "execution_status",
    "confidence", "revisions", "stop_reason", "final", "reasoning", "evidence_ids",
    # filled in by a reviewer
    "reviewer_correct", "reviewer_issue_type", "reviewer_note",
]
REVIEW_GUIDE = (
    "reviewer_correct: 1 (correct), 0 (wrong), NA (cannot judge). "
    "reviewer_issue_type: agent_error, data_limitation, or none. "
    "A correct stop on unusable data is 1/none, not a data_limitation."
)


def find_runs(paths: list[Path]) -> list[Path]:
    runs = []
    for path in paths:
        if (path / "run_manifest.json").exists():
            runs.append(path)
        else:
            runs.extend(sorted(p.parent for p in path.rglob("run_manifest.json")))
    return list(dict.fromkeys(runs))


def load_trace(run: Path) -> list[dict]:
    path = run / "trace.jsonl"
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def load_cases(run: Path) -> dict[str, dict]:
    cases = {}
    for decisions in sorted(run.glob("*/decisions.json")):
        try:
            records = json.loads(decisions.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        state_path = decisions.parent / "case_state.json"
        state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
        cases[decisions.parent.name] = {"records": records, "accession": state.get("accession") or "",
                                        "row": state.get("row") or {}}
    return cases


def _excerpt(text: str, limit: int) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[:limit - 3] + "..."


def _compress(sequence: list[str]) -> list[str]:
    out = []
    for item in sequence:
        if not out or out[-1] != item:
            out.append(item)
    return out


def analyze(runs: list[Path]) -> tuple[dict, list[dict]]:
    stage_stats = {s: {"records": 0, "cases": 0, "status": Counter(), "confidence": Counter(),
                       "revised_cases": 0, "rejected": 0} for s in STAGES}
    stops, hotspots, review_rows = Counter(), [], []
    changed_fields = defaultdict(Counter)
    rejection_examples = defaultdict(list)
    tools = defaultdict(lambda: {"calls": 0, "errors": 0, "seconds": 0.0, "max_seconds": 0.0,
                                 "error_examples": []})
    transitions = Counter()
    case_status = Counter()
    n_cases = n_traced_runs = first_pass = 0
    per_run = []

    for run in runs:
        trace, cases = load_trace(run), load_cases(run)
        n_traced_runs += bool(trace)
        per_run.append({"run": str(run), "cases": len(cases), "trace_events": len(trace)})
        rejected_by_case = Counter()
        sequences = defaultdict(list)

        for event in trace:
            kind, case = event.get("kind"), event.get("case")
            if kind == "call":
                name = event.get("name", "?")
                stats = tools[name]
                stats["calls"] += 1
                stats["seconds"] += float(event.get("duration_s") or 0)
                stats["max_seconds"] = max(stats["max_seconds"], float(event.get("duration_s") or 0))
                if not event.get("ok", True):
                    stats["errors"] += 1
                    if len(stats["error_examples"]) < 3:
                        stats["error_examples"].append(f"{case}: {event.get('error', '')}")
                if case:
                    sequences[case].append(name)
            elif kind == "decision":
                if case:
                    sequences[case].append(f"decide:{event.get('stage')}")
            elif kind == "decision_rejected":
                stage = event.get("stage")
                if stage in stage_stats:
                    stage_stats[stage]["rejected"] += 1
                rejected_by_case[case] += 1
                if len(rejection_examples[stage]) < 3:
                    rejection_examples[stage].append(f"{case}: {(event.get('errors') or [''])[0]}")
                hotspots.append({"run": run.name, "case": case, "stage": stage, "signal": "rejected_record",
                                 "detail": _excerpt((event.get("errors") or [""])[0], 200)})
                if case:
                    sequences[case].append(f"rejected:{stage}")
        for sequence in sequences.values():
            compact = _compress(sequence)
            transitions.update(zip(compact, compact[1:]))

        for case_id, case in cases.items():
            n_cases += 1
            records = case["records"]
            by_slot = defaultdict(list)
            for index, record in enumerate(records):
                by_slot[decision_slot(record.get("stage"), record.get("final"))].append((index, record))
            clean = not rejected_by_case.get(case_id)
            revised_stages = set()
            for slot, items in by_slot.items():
                stage = slot[0]
                stats = stage_stats.setdefault(stage, {"records": 0, "cases": 0, "status": Counter(),
                                                       "confidence": Counter(), "revised_cases": 0,
                                                       "rejected": 0})
                stats["records"] += len(items)
                if len(items) > 1:
                    if stage not in revised_stages:
                        stats["revised_cases"] += 1
                        revised_stages.add(stage)
                    clean = False
                    for (_, before), (_, after) in zip(items, items[1:]):
                        keys = sorted(k for k in set(before.get("final", {})) | set(after.get("final", {}))
                                      if json.dumps(before.get("final", {}).get(k), sort_keys=True, default=str)
                                      != json.dumps(after.get("final", {}).get(k), sort_keys=True, default=str))
                        changed_fields[stage].update(keys or ["(status or reasoning only)"])
                    hotspots.append({"run": run.name, "case": case_id, "stage": stage, "signal": "revised",
                                     "detail": _excerpt(items[-1][1].get("reasoning"), 240)})
                for index, record in items:
                    status = record.get("decision_status", "")
                    stats["status"][status] += 1
                    stats["confidence"][record.get("confidence", "")] += 1
                    if record.get("confidence") in {"low", "medium"}:
                        clean = False if record.get("confidence") == "low" else clean
                        hotspots.append({"run": run.name, "case": case_id, "stage": stage,
                                         "signal": f"{record.get('confidence')}_confidence",
                                         "detail": _excerpt(record.get("reasoning"), 240)})
                    review_rows.append({
                        "run_id": run.name, "case_id": case_id, "accession": case["accession"],
                        "stage": stage, "record_index": index, "decision_status": status,
                        "execution_status": record.get("execution_status", ""),
                        "confidence": record.get("confidence", ""), "revisions": len(items) - 1,
                        "stop_reason": record.get("stop_reason") or "",
                        "final": _excerpt(json.dumps(record.get("final", {}), ensure_ascii=False,
                                                     sort_keys=True, default=str), 600),
                        "reasoning": _excerpt(record.get("reasoning"), 800),
                        "evidence_ids": "; ".join(str(e.get("id", "")) for e in record.get("evidence", [])),
                        "reviewer_correct": "", "reviewer_issue_type": "", "reviewer_note": "",
                    })
            for stage in {r.get("stage") for r in records}:
                stage_stats[stage]["cases"] += 1
            blocked = next((r for r in records if r.get("decision_status") in BLOCKED
                            and r.get("stage") != "enrichment"), None)
            if blocked:
                stops[(blocked.get("stage"), _excerpt(blocked.get("stop_reason"), 120))] += 1
            status = case["row"].get("status") or (f"stopped:{blocked['stage']}" if blocked else "unfinished")
            case_status[status] += 1
            first_pass += clean

    order = {s: i for i, s in enumerate(STAGES)}
    review_rows.sort(key=lambda r: (r["run_id"], r["case_id"], order.get(r["stage"], 99), r["record_index"]))
    stage_table = []
    for stage in sorted(stage_stats, key=lambda s: order.get(s, 99)):
        stats = stage_stats[stage]
        if not stats["records"] and not stats["rejected"]:
            continue
        total = sum(stats["confidence"].values()) or 1
        stage_table.append({
            "stage": stage, "cases": stats["cases"], "records": stats["records"],
            "status": dict(stats["status"]), "confidence": dict(stats["confidence"]),
            "not_high_confidence_rate": round(1 - stats["confidence"].get("high", 0) / total, 3),
            "revised_cases": stats["revised_cases"],
            "revision_rate": round(stats["revised_cases"] / stats["cases"], 3) if stats["cases"] else 0.0,
            "rejected_records": stats["rejected"],
            "changed_fields": dict(changed_fields[stage].most_common(6)),
            "rejection_examples": rejection_examples.get(stage, []),
        })
    tool_table = sorted(({"tool": name, "calls": s["calls"], "errors": s["errors"],
                          "error_rate": round(s["errors"] / s["calls"], 3) if s["calls"] else 0.0,
                          "mean_seconds": round(s["seconds"] / s["calls"], 3) if s["calls"] else 0.0,
                          "max_seconds": round(s["max_seconds"], 3), "error_examples": s["error_examples"]}
                         for name, s in tools.items()), key=lambda r: (-r["errors"], -r["calls"]))
    summary = {
        "runs": per_run,
        "n_runs": len(runs), "n_traced_runs": n_traced_runs, "n_cases": n_cases,
        "case_status": dict(case_status),
        "first_pass_cases": first_pass,
        "first_pass_note": "no revised gate, no rejected record, and no low-confidence decision",
        "stages": stage_table,
        "stops": [{"stage": s, "reason": r, "cases": n} for (s, r), n in stops.most_common()],
        "hotspots": hotspots,
        "tools": tool_table,
        "transitions": [{"from": a, "to": b, "count": n} for (a, b), n in transitions.most_common(25)],
    }
    return summary, review_rows


def to_markdown(summary: dict) -> str:
    lines = ["# Decision trace summary", "",
             f"Runs: {summary['n_runs']} ({summary['n_traced_runs']} with trace.jsonl). "
             f"Cases: {summary['n_cases']}. First-pass cases: {summary['first_pass_cases']} "
             f"({summary['first_pass_note']}).", "",
             "Case outcomes: " + ", ".join(f"{k} {v}" for k, v in sorted(summary["case_status"].items())), "",
             "## Gates", "",
             "| Gate | Cases | Records | Not high confidence | Revised cases | Rejected records | Statuses | Fields changed on revision |",
             "|---|---:|---:|---:|---:|---:|---|---|"]
    for row in summary["stages"]:
        lines.append(f"| {row['stage']} | {row['cases']} | {row['records']} | "
                     f"{row['not_high_confidence_rate']:.0%} | {row['revised_cases']} | {row['rejected_records']} | "
                     + ", ".join(f"{k} {v}" for k, v in row["status"].items()) + " | "
                     + ", ".join(f"{k} {v}" for k, v in row["changed_fields"].items()) + " |")
    lines += ["", "## Stops", ""]
    lines += [f"- {s['stage']}: {s['cases']} case(s) - {s['reason']}" for s in summary["stops"]] or ["- none"]
    lines += ["", "## Where the agent hesitated", ""]
    if summary["hotspots"]:
        lines += ["| Run | Case | Gate | Signal | Detail |", "|---|---|---|---|---|"]
        for h in summary["hotspots"][:60]:
            lines.append(f"| {h['run']} | {h['case']} | {h['stage']} | {h['signal']} | "
                         f"{str(h['detail']).replace('|', '/')} |")
    else:
        lines.append("- none")
    lines += ["", "## Tools", ""]
    if summary["tools"]:
        lines += ["| Tool | Calls | Errors | Mean s | Max s | Example error |", "|---|---:|---:|---:|---:|---|"]
        for t in summary["tools"]:
            example = t["error_examples"][0].replace("|", "/") if t["error_examples"] else ""
            lines.append(f"| {t['tool']} | {t['calls']} | {t['errors']} | {t['mean_seconds']} | "
                         f"{t['max_seconds']} | {example} |")
    else:
        lines.append("- no traced tool calls")
    lines += ["", "## Most common transitions", ""]
    lines += [f"- {t['from']} -> {t['to']}: {t['count']}" for t in summary["transitions"]] or ["- none"]
    lines += ["", "## Review sheet", "", REVIEW_GUIDE, ""]
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    runs = find_runs(args.paths)
    if not runs:
        print("no run_manifest.json found under the given paths", file=sys.stderr)
        return 1
    summary, review_rows = analyze(runs)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "trace_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False),
                                                 encoding="utf-8")
    (args.out / "trace_summary.md").write_text(to_markdown(summary), encoding="utf-8")
    with open(args.out / "review_sheet.csv", "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        writer.writerows(review_rows)
    print(f"{summary['n_runs']} run(s), {summary['n_cases']} case(s), {len(review_rows)} review rows -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
