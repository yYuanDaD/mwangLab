"""For every paper with a PMID: which GEO series does GEO itself link to that PMID?

An independent check on the screener's ownership layers. Writes geo_by_pmid.csv."""
import csv, json, os, sys
sys.path.insert(0, os.getcwd())
from tools import paper_screen as ps

RUN = "test/experiments/paper_screen_20261019"
OUT = os.path.join(RUN, "review_20261027")
http = ps.Http(cache_dir=os.path.join(OUT, "_http_cache_elink"))
papers = list(csv.DictReader(open(os.path.join(RUN, "papers.csv"), encoding="utf-8")))
rows = []
for i, p in enumerate(papers, 1):
    pmid = (p.get("pmid") or "").strip()
    if not pmid:
        continue
    s = http.get(f"{ps.EUTILS}/elink.fcgi", {"dbfrom": "pubmed", "db": "gds", "id": pmid, "retmode": "json"})
    uids = []
    try:
        for ls in json.loads(s)["linksets"]:
            for db in ls.get("linksetdbs", []):
                if db.get("linkname") == "pubmed_gds":
                    uids += db["links"]
    except Exception:
        pass
    series = []
    if uids:
        r = http.get(f"{ps.EUTILS}/esummary.fcgi", {"db": "gds", "id": ",".join(uids), "retmode": "json"})
        try:
            res = json.loads(r)["result"]
            for u in res.get("uids", []):
                rec = res[u]
                if rec.get("entrytype") == "GSE":
                    series.append({"gse": rec["accession"], "gdstype": rec.get("gdstype", ""),
                                   "taxon": rec.get("taxon", ""), "n_samples": rec.get("n_samples"),
                                   "suppfile": rec.get("suppfile", "")})
        except Exception:
            pass
    rows.append({"paper_id": p["paper_id"], "pmid": pmid, "geo_linked": json.dumps(series, ensure_ascii=False)})
    if i % 50 == 0:
        print(i, flush=True)
with open(os.path.join(OUT, "geo_by_pmid.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["paper_id", "pmid", "geo_linked"]); w.writeheader(); w.writerows(rows)
print("done", len(rows), "with links:", sum(1 for r in rows if r["geo_linked"] != "[]"))
