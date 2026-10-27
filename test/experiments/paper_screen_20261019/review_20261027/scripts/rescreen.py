"""Rescreen the 2026-10-19 papers with the current screener, reusing that run's caches.

Writes <out>/screen.csv and screen_summary.md; caches stay in the 10-19 folder."""
import csv, os, re, sys
sys.path.insert(0, os.getcwd())
from tools import paper_screen as ps

RUN = "test/experiments/paper_screen_20261019"
OUT = os.path.join(RUN, "review_20261027")

class CountingHttp(ps.Http):
    misses = 0
    def get(self, url, params=None, **kw):
        path = self._key(url, {k: v for k, v in dict(params or {}).items() if k != "api_key"}
                         | ({"__max_bytes__": kw["max_bytes"]} if kw.get("max_bytes") else {}))
        if not os.path.exists(path):
            CountingHttp.misses += 1
        return super().get(url, params, **kw)

http = CountingHttp(cache_dir=os.path.join(RUN, "_http_cache"))
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
        print(f"[{i}/{len(papers)}] misses={CountingHttp.misses} {s.verdict:16} {s.reason[:40]}", flush=True)
ps.mark_shared_series(out_csv)
open(os.path.join(OUT, "screen_summary.md"), "w", encoding="utf-8").write(ps.summarize(out_csv))
print("done; cache misses:", CountingHttp.misses)
