"""Everything already collected, screened or run, so the new batch holds only new papers.

Reads every papers.csv / screen.csv of the earlier screen batches (2026-10-17 to 2026-10-28)
and the 211-paper run queue. Writes:
  exclude_papers.csv  paper_id, doi, pmid, pmcid, title  (one row per earlier paper row)
  exclude_gse.txt     every GEO series an earlier screen looked at or a run used

    python test/experiments/paper_screen_20261124/build_exclude.py <experiments_dir>

<experiments_dir> is the test/experiments folder that holds the earlier batches with their
untracked files (E:/agent/mwangLab_pdf/test/experiments on the lab PC).
"""
import csv
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
csv.field_size_limit(1 << 30)

paper_files, screen_files = [], []
for batch in ("paper_screen_20261017", "paper_screen_20261018", "paper_screen_20261019",
              "paper_screen_20261027", "paper_screen_20261028"):
    for f in glob.glob(os.path.join(EXP, batch, "**", "*.csv"), recursive=True):
        if os.sep + "papers" + os.sep in f or "_http_cache" in f:
            continue
        name = os.path.basename(f)
        if name.startswith(("papers", "exclude_all", "screen", "analyzable", "rescreen", "sample", "geo_by_pmid")):
            (screen_files if name.startswith("screen") else paper_files).append(f)

rows, gses = [], set()
GSE = re.compile(r"\bGSE\d{3,7}\b")
for f in paper_files + screen_files:
    for r in csv.DictReader(open(f, encoding="utf-8", errors="replace")):
        rows.append({"paper_id": r.get("paper_id", ""), "doi": (r.get("doi") or "").lower(),
                     "pmid": r.get("pmid", ""), "pmcid": r.get("pmcid", ""), "title": r.get("title", ""),
                     "from": os.path.relpath(f, EXP)})
        if os.path.basename(f).startswith("screen") or "analyzable" in f:
            for col in ("series_json", "analyzable_gse", "gse", "own_gse", "all_gse"):
                gses |= set(GSE.findall(r.get(col) or ""))
for f in glob.glob(os.path.join(EXP, "large_run_pilot_20261019", "*.csv")) + \
        glob.glob(os.path.join(EXP, "large_run_pilot_20261019", "runs_claude", "progress.csv")):
    for r in csv.DictReader(open(f, encoding="utf-8", errors="replace")):
        gses |= set(GSE.findall(" ".join(str(v) for v in r.values())))
        if r.get("paper_id"):
            rows.append({"paper_id": r["paper_id"], "doi": "", "pmid": r["paper_id"][4:] if r["paper_id"].startswith("PMID") else "",
                         "pmcid": "", "title": r.get("title", ""), "from": os.path.relpath(f, EXP)})

with open(os.path.join(HERE, "exclude_papers.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["paper_id", "doi", "pmid", "pmcid", "title", "from"])
    w.writeheader()
    w.writerows(rows)
with open(os.path.join(HERE, "exclude_gse.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(sorted(gses)) + "\n")
pmids = {r["pmid"] for r in rows if r["pmid"]}
print(f"{len(paper_files)} paper files, {len(screen_files)} screen files -> {len(rows)} rows, "
      f"{len(pmids)} distinct PMIDs, {len(gses)} GEO series")
