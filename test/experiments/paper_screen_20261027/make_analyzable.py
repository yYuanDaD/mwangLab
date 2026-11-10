"""Write analyzable.csv (one row per analyzable paper) from screen.csv and papers.csv.

    python test/experiments/paper_screen_20261019/make_analyzable.py
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIND = {"raw_counts": "raw", "raw_counts_in_tar": "tar"}

papers = {r["paper_id"]: r for r in csv.DictReader(open(os.path.join(HERE, "papers.csv"), encoding="utf-8"))}
out = []
for r in csv.DictReader(open(os.path.join(HERE, "screen.csv"), encoding="utf-8")):
    if r["verdict"] != "analyzable":
        continue
    keep = r["analyzable_gse"].split(";")
    series = [s for s in json.loads(r["series_json"] or "[]") if s["gse"] in keep]
    p = papers[r["paper_id"]]
    out.append({
        "paper_id": r["paper_id"], "pmid": p["pmid"], "pmcid": r["pmcid"], "title": r["title"], "year": p["year"],
        "analyzable_gse": r["analyzable_gse"],
        "taxon": ";".join(s["taxon"] for s in series),
        "n_samples": ";".join(str(s["n_samples"]) for s in series),
        "groups": " || ".join(json.dumps((s.get("design") or {}).get("groups"), ensure_ascii=False) for s in series),
        "file_kind": ";".join(KIND.get((s.get("files") or {}).get("status"), str((s.get("files") or {}).get("status")))
                              for s in series),
        "source": p["source"],
    })
out.sort(key=lambda x: x["paper_id"])
with open(os.path.join(HERE, "analyzable.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
print(f"{len(out)} analyzable papers -> analyzable.csv")
