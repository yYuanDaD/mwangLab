"""Rescreen the 2026-10-19 papers with the patched screener (scratch copy), reusing that
run's caches. Writes review_20261027/rescreen_fixed/screen.csv and screen_summary.md."""
import csv, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "repo"))
from tools import paper_screen as ps  # the patched copy

RUN = "E:/agent/mwangLab_pdf/test/experiments/paper_screen_20261019"
OUT = os.path.join(RUN, "review_20261027", "rescreen_fixed")
os.makedirs(OUT, exist_ok=True)
cache = os.path.join(RUN, "_http_cache")
# The elink answers fetched for the review use the same cache keys.
elink = os.path.join(RUN, "review_20261027", "_http_cache_elink")
for n in os.listdir(elink):
    if not os.path.exists(os.path.join(cache, n)):
        shutil.copy(os.path.join(elink, n), os.path.join(cache, n))

http = ps.Http(cache_dir=cache)
papers = list(csv.DictReader(open(os.path.join(RUN, "papers.csv"), encoding="utf-8")))
topic = re.compile(ps.DEFAULT_TOPIC, re.I)
contrast = re.compile(ps.DEFAULT_CONTRAST, re.I)
out_csv = os.path.join(OUT, "screen.csv")
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=ps.FIELDS)
    w.writeheader()
    for i, row in enumerate(papers, 1):
        try:
            doc = ps.load_full_text(row, os.path.join(RUN, "papers"), http)
            s = ps.screen_paper(row, doc, http, organisms=ps.DEFAULT_ORGANISMS, topic=topic, contrast=contrast)
        except Exception as e:
            s = ps.Screen(paper_id=row.get("paper_id", ""), title=row.get("title", ""), source=row.get("source", ""),
                          query=row.get("query", ""), verdict="needs_inspection",
                          reason=f"error:{type(e).__name__}: {e}"[:200])
        w.writerow(s.row()); f.flush()
        print(f"[{i}/{len(papers)}] {s.verdict:16} {s.reason[:40]:40} {s.route}", flush=True)
ps.mark_shared_series(out_csv)
open(os.path.join(OUT, "screen_summary.md"), "w", encoding="utf-8").write(ps.summarize(out_csv))
print("done")
