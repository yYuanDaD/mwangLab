"""Review step of the 211-paper run (after finish_paper.py).

    python test/experiments/large_run_pilot_20261019/review_paper.py prepare <paper_id>
        builds runs_claude/<paper_id>/review/<case_id>/ (packet_A.md, packet_B.md, flags.json) for every case
        with a decisions.json and prints the reviewer prompt (REVIEW_PROMPT_211.md) filled in.
    python test/experiments/large_run_pilot_20261019/review_paper.py record <paper_id> <minutes> <tokens>
        reads each case's review.json, appends rows to runs_claude/reviews.csv, adds fix/human items to
        runs_claude/REVIEW_QUEUE.md, and prints the fix items to send back to the analysis subagent.
    python test/experiments/large_run_pilot_20261019/review_paper.py resolve <paper_id> applied|rebutted|skipped "<note>"
        records what happened to the fix items (one round only); rebutted items go to REVIEW_QUEUE.md.
"""
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
RUNS = HERE / "runs_claude"


def _cases(paper_id):
    run = RUNS / paper_id
    return sorted(p.parent for p in run.glob("*/decisions.json")
                  if "_previous" not in p.parts and p.parent.name != "review")


def prepare(paper_id):
    from tools.case_review import build
    run = RUNS / paper_id
    spec = run / "case_spec.json"
    lines, paper = [], None
    for case in _cases(paper_id):
        out = run / "review" / case.name
        s = build(case, out, spec=str(spec) if spec.exists() else None, root=ROOT)
        paper = paper or s["paper"]
        lines.append(f"- {case.name}: review folder {out} ; case folder {case}")
        print(f"# {case.name}: flags {[f['flag'] for f in s['flags']]}", file=sys.stderr)
    if not lines:
        sys.exit(f"no case with decisions.json under {run}")
    doc = (HERE / "REVIEW_PROMPT_211.md").read_text(encoding="utf-8")
    template = doc.split("\n---\n")[1].strip()
    print(template.format(paper=paper or "no full text: use the PubMed abstract and the GEO description",
                          cases="\n".join(lines)))


def _queue(paper_id, case, items):
    path = RUNS / "REVIEW_QUEUE.md"
    new = not path.exists()
    with open(path, "a", encoding="utf-8") as f:
        if new:
            f.write("# Review queue (items for the owner)\n\nOne section per case; newest last.\n")
        f.write(f"\n## {paper_id} / {case} ({datetime.now(timezone.utc):%Y-%m-%d})\n\n")
        for it in items:
            f.write(f"- {it}\n")


def record(paper_id, minutes, tokens):
    rows, fixes = [], []
    for case in _cases(paper_id):
        p = RUNS / paper_id / "review" / case.name / "review.json"
        if not p.exists():
            rows.append([paper_id, case.name, "missing", "", minutes, tokens, ""])
            continue
        r = json.loads(p.read_text(encoding="utf-8"))
        bad = [c for c in r.get("checks", []) if c.get("verdict") in ("disagree", "unsure")
               and c.get("severity") in ("blocking", "major")]
        tag = ";".join(f"{c['id']}:{c['verdict']}:{c['severity']}" for c in bad)
        rows.append([paper_id, case.name, r.get("overall", ""), tag, minutes, tokens, len(r.get("checks", []))])
        if r.get("overall") == "fix":
            fixes += [f"[{case.name}] {c['id']} ({c['severity']}): {c.get('fix') or c.get('evidence')}"
                      for c in bad if c.get("verdict") == "disagree"]
        human = [f"{c['id']} ({c['verdict']}, {c['severity']}): {c.get('evidence', '')}" for c in bad
                 if r.get("overall") == "human" or c.get("verdict") == "unsure"]
        human += [f"policy: {h}" for h in r.get("human_items", [])]
        if human:
            _queue(paper_id, case.name, human)
    path = RUNS / "reviews.csv"
    new = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["paper_id", "case", "overall", "major_items", "review_minutes", "review_tokens", "n_checks"])
        w.writerows(rows)
    for r in rows:
        print(f"{r[1]}: {r[2]} {r[3]}")
    if fixes:
        print("\nFIX ITEMS (send once to the analysis subagent):")
        print("\n".join(fixes))


def resolve(paper_id, outcome, note):
    with open(RUNS / "reviews.csv", "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([paper_id, "*", f"fix_{outcome}", re.sub(r"\s+", " ", note)[:300], "", "", ""])
    if outcome == "rebutted":
        _queue(paper_id, "*", [f"analysis agent rebutted the reviewer: {note}"])
    print(f"recorded fix_{outcome}")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "prepare":
        prepare(*args)
    elif cmd == "record":
        record(*args)
    elif cmd == "resolve":
        resolve(*args)
    else:
        sys.exit(__doc__)
