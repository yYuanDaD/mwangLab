"""Token shares for runs on the case-spec route, in the same buckets as REPORT.md.

    python extract_usage.py --match <pattern> --out <dir>
    python classify_casespec.py --dir <dir> [--since 2026-10-28T06:00]

Reads <dir>/calls.csv and <dir>/transcripts.csv (subagent transcripts only) and writes
<dir>/summary_casespec.csv, which holds only aggregate numbers (no command text).
"""
import argparse
import re
from pathlib import Path

import pandas as pd

BUCKETS = {
    "baseline": "fixed overhead",
    "read skill docs": "learning how", "case_runner template/schema/help": "learning how",
    "read library code": "learning how", "read earlier runs/logs": "learning how",
    "write script": "scripts", "run script": "scripts", "shell misc": "scripts", "re-read big output": "scripts",
    "case_runner inspect": "fixed runner", "case_runner execute": "fixed runner",
    "write case spec": "decisions (JSON)",
    "read paper text": "science", "inspect data/metadata": "science", "thinking/text": "science",
    "check own results": "science", "final report": "science",
    "other": "other",
}


def category(r) -> str:
    tool, d = r.tool, str(r.desc)
    dl = d.lower().replace("\\", "/")
    if tool == "(baseline)":
        return "baseline"
    if tool == "(thinking/text)":
        return "thinking/text"
    if tool == "SubagentHandback" or "handback.md" in dl:
        return "final report"
    if tool in ("Write", "Edit"):
        name = dl.split("/")[-1]
        if name.endswith(".json"):
            return "write case spec"
        if name.endswith(".py"):
            return "write script"
        return "other"
    if "case_runner" in dl:
        if re.search(r"case_runner\s+(template|schema)|--help|-h\b", dl):
            return "case_runner template/schema/help"
        if re.search(r"case_runner\s+inspect", dl):
            return "case_runner inspect"
        if re.search(r"case_runner\s+execute", dl):
            return "case_runner execute"
    if "tool-results" in dl:
        return "re-read big output"
    if "skills/bioinformatics-workflow" in dl or "skill.md" in dl:
        return "read skill docs"
    if "paper_structure" in dl or ".paper." in dl or "/papers" in dl or "efetch" in dl:
        return "read paper text"
    runs = [x for x in re.findall(r"runs_claude/+([a-z0-9]+)", dl) if x != str(r.paper_id).lower()]
    if runs or "problems.md" in dl or "case_runner_validation" in dl or "large_run_pilot" in dl and "runs_claude" not in dl:
        return "read earlier runs/logs"
    if tool == "Grep" and re.search(r"tools|case_runner|native|decision_contract|suitability", dl):
        return "read library code"
    if re.search(r"tools/[a-z_]+\.py", dl) and (tool == "Read" or re.search(r"\b(sed|cat|grep|head|select-string|get-content)\b", dl)):
        return "read library code"
    if re.search(r"suitability\.md|decisions\.json|deg_results|/results/|summary\.csv|evidence\.json|case_runner\.log", dl):
        return "check own results"
    if tool in ("Bash", "PowerShell"):
        if "prompt_for" in dl:
            return "baseline"
        if re.search(r"python\S*\s+\S*\.py", dl) and "-c" not in d and "<<" not in d:
            return "run script"
        if re.search(r"\bgeo|data/gse|metadata|\.csv|\.tsv|\.gz|\.tar", dl) or "python" in dl:
            return "inspect data/metadata"
        return "shell misc"
    if tool == "Read":
        return "inspect data/metadata" if re.search(r"metadata|\.csv|\.tsv|inspect_", dl) else "other"
    return "other"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--since", help="keep transcripts that start at or after this ISO time")
    args = ap.parse_args()
    here = Path(args.dir)
    c = pd.read_csv(here / "calls.csv")
    t = pd.read_csv(here / "transcripts.csv")
    t = t[t.sidechain == True].copy()  # noqa: E712
    if args.since:
        t = t[t.first_ts >= args.since]
    t["fname"] = t.file.str.replace("\\", "/", regex=False).str.split("/").str[-1]
    c = c[c.file.isin(t.fname)].merge(t[["fname", "turns"]], left_on="file", right_on="fname")
    n = len(t)
    c["cat"] = c.apply(category, axis=1)
    c["bucket"] = c.cat.map(BUCKETS).fillna("other")
    c["added"] = c.result_tokens + c.output_tokens
    later = (c.turns - 1 - c.turn.clip(lower=0)).clip(lower=0)
    # API-price weights (relative to base input): cache write 1.25, cache read 0.1/turn, output 5
    c["weighted"] = c.result_tokens * (1.25 + 0.1 * later) + c.output_tokens * (5 + 1.25 + 0.1 * later)
    rows = []
    for level in ("bucket", "cat"):
        g = c.groupby(level).agg(calls=("tool", "size"), added=("added", "sum"), weighted=("weighted", "sum"))
        g["per_paper"] = (g.added / n).round(-2)
        g["share_pct"] = (100 * g.added / g.added.sum()).round(1)
        g["weighted_pct"] = (100 * g.weighted / g.weighted.sum()).round(1)
        g = g.sort_values("added", ascending=False)
        print(g[["calls", "per_paper", "share_pct", "weighted_pct"]].to_string(), "\n")
        rows.append(g.reset_index().rename(columns={level: "name"}).assign(level=level))
    print(f"transcripts {n}; mean turns {t.turns.mean():.1f}; mean final context {t.final_context.mean():.0f}; "
          f"mean output {t.sum_output.mean():.0f}; mean cache read {t.sum_cache_read.mean():.0f}")
    pd.concat(rows).to_csv(here / "summary_casespec.csv", index=False)


if __name__ == "__main__":
    main()
