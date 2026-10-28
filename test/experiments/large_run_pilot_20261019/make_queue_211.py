"""Build queue_211.csv: the analyzable papers not yet run, with the paper file each run should read.

    python test/experiments/large_run_pilot_20261019/make_queue_211.py
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
SRC = os.path.join(EXP, "paper_screen_20261028", "analyzable_combined.csv")
PAPER_DIRS = ["paper_screen_20261019", "paper_screen_20261027", "paper_screen_20261028"]


def find_paper(row):
    names = [n for n in (row["pmcid"], row["paper_id"]) if n]
    order = sorted(PAPER_DIRS, key=lambda d: d != f"paper_screen_{row['batch']}")
    for d in order:
        for n in names:
            p = os.path.join(EXP, d, "papers", f"{n}.paper.md")
            if os.path.exists(p):
                return os.path.relpath(p, os.path.dirname(os.path.dirname(EXP))).replace("\\", "/")
    return ""


rows = [r for r in csv.DictReader(open(SRC, encoding="utf-8")) if r["already_run"] != "True"]
out = os.path.join(HERE, "queue_211.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["n", "paper_id", "gse", "route", "batch", "title", "paper_md"])
    for i, r in enumerate(rows, 1):
        w.writerow([i, r["paper_id"], r["analyzable_gse"], r["route"], r["batch"], r["title"], find_paper(r)])
missing = sum(1 for r in rows if not find_paper(r))
print(f"{len(rows)} papers -> {out}; {missing} without a paper file")
