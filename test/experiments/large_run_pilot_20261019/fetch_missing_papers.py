"""Fetch Europe PMC full text for queued papers that have a PMCID but no local paper file.

    python test/experiments/large_run_pilot_20261019/fetch_missing_papers.py
Writes papers_extra/<PMCID>.paper.{md,json}; rerun make_queue_211.py afterwards.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
from tools import paper_tools  # noqa: E402

SRC = os.path.join(HERE, "..", "paper_screen_20261028", "analyzable_combined.csv")
OUT = os.path.join(HERE, "papers_extra")
pmc = {r["paper_id"]: r["pmcid"] for r in csv.DictReader(open(SRC, encoding="utf-8"))}
for r in csv.DictReader(open(os.path.join(HERE, "queue_211.csv"), encoding="utf-8")):
    if r["paper_md"] or not pmc.get(r["paper_id"]):
        continue
    fn = getattr(paper_tools.fetch_paper_text, "func", paper_tools.fetch_paper_text)
    res = fn(pmcid=pmc[r["paper_id"]], output_dir=OUT)
    print(r["paper_id"], pmc[r["paper_id"]], str(res)[:160].replace("\n", " "))
