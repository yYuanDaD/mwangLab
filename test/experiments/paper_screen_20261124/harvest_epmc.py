"""Third source: Europe PMC papers on an exercise topic whose text mentions a GEO accession.

Europe PMC text-mines accession numbers (ACCESSION_TYPE:geo), so this finds papers that cite
a GEO series in the text even when GEO links the series to no paper or to another one. The
screener still decides whether the series is the paper's own. Appends new papers to
papers.csv (source ``epmc_acc``), skipping exclude_papers.csv and papers already there.

    python test/experiments/paper_screen_20261124/harvest_epmc.py     (cwd: code with tools/ from 94d6028)
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.getcwd())
from tools import paper_screen as sc  # noqa: E402

http = sc.Http(cache_dir=os.path.join(HERE, "_http_cache"))
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
WORDS = ['exercise', 'exercised', '"physical activity"', '"physical inactivity"', 'treadmill', '"wheel running"',
         '"voluntary running"', 'swimming', '"endurance training"', '"resistance training"', '"strength training"',
         '"interval training"', 'HIIT', '"aerobic training"', 'sedentary', 'athletes', 'detraining',
         '"bed rest"', '"hindlimb unloading"', '"hindlimb suspension"', 'immobilization', '"muscle disuse"',
         '"physical fitness"', '"cardiorespiratory fitness"', '"exercise training"', 'exerkine', 'myokine']
query = ("(" + " OR ".join(f"TITLE_ABS:{w}" for w in WORDS) + ") AND ACCESSION_TYPE:geo AND "
         "(SRC:MED OR SRC:PMC) AND PUB_YEAR:[2010 TO 2026]")

existing = list(csv.DictReader(open(os.path.join(HERE, "papers.csv"), encoding="utf-8")))
keys = set()
for r in list(csv.DictReader(open(os.path.join(HERE, "exclude_papers.csv"), encoding="utf-8"))) + existing:
    if r["paper_id"].startswith("PMID"):
        keys.add("pmid:" + r["paper_id"][4:])
    for k in ("pmid", "pmcid", "doi"):
        if r.get(k):
            keys.add(f"{k}:{r[k].lower()}")
    t = re.sub(r"\W+", "", (r.get("title") or "").lower())[:80]
    if len(t) > 20:
        keys.add("t:" + t)

hits, cursor = [], "*"
while True:
    body = http.get(EPMC, {"query": query, "format": "json", "resultType": "lite", "pageSize": 1000,
                           "cursorMark": cursor})
    d = json.loads(body)
    page = d.get("resultList", {}).get("result") or []
    hits += page
    if not page or d.get("nextCursorMark") in (None, cursor):
        break
    cursor = d["nextCursorMark"]
print(f"Europe PMC hits: {len(hits)} (reported {d.get('hitCount')})", flush=True)

new = []
for h in hits:
    r = {"paper_id": f"PMID{h['pmid']}" if h.get("pmid") else h.get("pmcid", h.get("id", "")),
         "source": "epmc_acc", "title": (h.get("title") or "").strip(), "year": h.get("pubYear", ""),
         "doi": (h.get("doi") or "").lower(), "pmid": h.get("pmid", ""), "pmcid": h.get("pmcid", ""),
         "pdf_url": "", "linked_gse": "", "query": "epmc ACCESSION_TYPE:geo"}
    ks = [f"pmid:{r['pmid']}", f"pmcid:{r['pmcid'].lower()}", f"doi:{r['doi']}",
          "t:" + re.sub(r"\W+", "", r["title"].lower())[:80]]
    if any(k in keys for k in ks if not k.endswith(":")):
        continue
    keys.update(k for k in ks if not k.endswith(":"))
    new.append(r)
fields = ["paper_id", "source", "title", "year", "doi", "pmid", "pmcid", "pdf_url", "linked_gse", "query"]
with open(os.path.join(HERE, "papers.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(existing + new)
print(f"{len(new)} new papers appended; papers.csv now {len(existing) + len(new)}; "
      f"new with PMCID: {sum(bool(r['pmcid']) for r in new)}")
