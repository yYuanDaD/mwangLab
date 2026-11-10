"""Fill <out>/papers with each paper's structured full text, one subprocess per paper.

A docling crash in one PDF then kills only that subprocess, not the batch.
Usage (repo root): python prefetch.py <papers.csv> <out_dir>
"""
import csv, os, re, subprocess, sys

papers_csv, out = sys.argv[1], sys.argv[2]
CHILD = r'''
import csv, os, sys
sys.path.insert(0, os.getcwd())
from tools import paper_screen as sc
row = {k: v for k, v in zip(sys.argv[3::2], sys.argv[4::2])}
out = sys.argv[1]
doc = sc.load_full_text(row, os.path.join(out, "papers"), sc.Http(cache_dir=os.path.join(out, "_http_cache")))
print("ok" if doc else "none")
'''
rows = list(csv.DictReader(open(papers_csv, encoding="utf-8")))
for i, row in enumerate(rows, 1):
    stem = re.sub(r"[^A-Za-z0-9._-]", "_", row.get("pmcid") or row.get("paper_id") or "paper")
    if os.path.exists(os.path.join(out, "papers", f"{stem}.paper.json")):
        continue
    if not (row.get("pmcid") or row.get("pdf_url")):
        continue
    args = [sys.executable, "-c", CHILD, out, "x"]
    for k in ("paper_id", "pmcid", "pdf_url", "title", "doi"):
        args += [k, row.get(k, "")]
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=900, encoding="utf-8", errors="replace")
        res = p.stdout.strip().splitlines()[-1:] or [f"exit {p.returncode}"]
    except subprocess.TimeoutExpired:
        res = ["timeout"]
    print(f"[{i}/{len(rows)}] {stem[:40]} {res[0]}", flush=True)
