"""Combine the analyzable papers of the three screen batches (fixed screener), dropping duplicates.

A paper counts once; a GEO series claimed by two papers counts once (the first paper keeps it).
Writes analyzable_combined.csv with the batch and whether the paper was already run.

    python test/experiments/paper_screen_20261028/combine.py
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
BATCHES = [("20261019", "paper_screen_20261019/screen_fixed.csv"),
           ("20261027", "paper_screen_20261027/screen.csv"),
           ("20261028", "paper_screen_20261028/screen.csv")]
run = {r["paper_id"] for r in csv.DictReader(open(os.path.join(
    EXP, "large_run_pilot_20261019/runs_claude/progress.csv"), encoding="utf-8"))}

seen_paper, seen_gse, out, dropped = set(), set(), [], []
for batch, path in BATCHES:
    full = os.path.join(EXP, path)
    if not os.path.exists(full):
        continue
    for r in csv.DictReader(open(full, encoding="utf-8")):
        if r["verdict"] != "analyzable":
            continue
        gses = [g for g in r["analyzable_gse"].split(";") if g]
        keys = {k for k in (r.get("pmcid"), r.get("doi"), r["paper_id"]) if k}
        if keys & seen_paper:
            dropped.append((batch, r["paper_id"], "same paper"))
            continue
        new = [g for g in gses if g not in seen_gse]
        if not new:
            dropped.append((batch, r["paper_id"], "all series already counted: " + ";".join(gses)))
            continue
        seen_paper |= keys
        seen_gse |= set(new)
        series = [s for s in json.loads(r.get("series_json") or "[]") if s["gse"] in new]
        out.append({"batch": batch, "paper_id": r["paper_id"], "pmcid": r.get("pmcid", ""), "title": r["title"],
                    "analyzable_gse": ";".join(new), "source": r.get("source", ""),
                    "route": ";".join(sorted({str(s.get("route", "")) for s in series if s.get("route")})),
                    "already_run": r["paper_id"] in run})
with open(os.path.join(HERE, "analyzable_combined.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
by = {}
for o in out:
    by[o["batch"]] = by.get(o["batch"], 0) + 1
print("analyzable, unique:", len(out), by, "already run:", sum(o["already_run"] for o in out))
print("dropped as duplicates:", len(dropped))
for d in dropped:
    print("  ", d)
