"""Zero-cost scan: which cached papers OWN a GSE (strict 'own') whose data we already have as
raw counts? That paper is the ideal seed for demonstrating raw_da_method='all' through the cohort.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/scan_own_gse_papers.py
"""
import os
import sys
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from tools.cohort_tools import choose_own_gse
from tools.batch_tools import _find_expression_file

papers = sorted(glob.glob(os.path.join("data", "papers", "*.txt")))
print(f"scanning {len(papers)} cached papers...\n")

hits = []
for p in papers:
    with open(p, encoding="utf-8", errors="ignore") as f:
        text = f.read()[:100000]
    gse, ownership, classes = choose_own_gse(text)
    if not gse:
        continue
    # is the data local + what matrix type?
    data_dir = os.path.join("data", gse)
    mtype = None
    if os.path.isdir(data_dir):
        try:
            _, mtype = _find_expression_file(data_dir)
        except Exception as e:
            mtype = f"err:{type(e).__name__}"
    # grab a title-ish first non-empty line for keyword crafting
    title = ""
    for line in text.splitlines():
        if len(line.strip()) > 25:
            title = line.strip()[:90]
            break
    raw = mtype in ("raw_counts", "raw_counts_from_tar")
    flag = "  <== OWN + LOCAL RAW COUNTS" if (ownership == "own" and raw) else ""
    print(f"{os.path.basename(p)[:20]:20s} | {gse:11s} | {ownership:18s} | "
          f"data={'yes' if os.path.isdir(data_dir) else 'NO ':3s} | mtype={str(mtype):20s}{flag}")
    if ownership == "own" and raw:
        hits.append((p, gse, title))

print("\n=== ideal seeds (own + local raw counts) ===")
for p, gse, title in hits:
    print(f"  {gse}  <-  {os.path.basename(p)}")
    print(f"        title: {title}")
