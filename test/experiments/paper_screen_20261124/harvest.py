"""Collect new candidate papers from the GEO side, skipping everything seen before.

Two sources, both starting from GEO bulk RNA-seq series (human, mouse, rat) whose title or
summary names an exercise-type term (the screener's own topic regex):
  geo_all   every such series GEO links to a PubMed ID (all pages, not only the top hits the
            earlier ``geo`` source took per query)
  geo_epmc  series with no PubMed link: Europe PMC full-text search for the accession finds
            the papers that mention it (the screener then decides whether it is their own)

Papers already in exclude_papers.csv (by PMID, PMCID, DOI or title) are dropped, and so are
series in exclude_gse.txt. No LLM calls. Writes papers.csv in the screener's format plus
series.csv (one row per harvested series, with what happened to it).

    python test/experiments/paper_screen_20261124/harvest.py     (cwd: code with tools/ from 94d6028)
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
# Stricter than the screener's topic regex: in GEO records its loose terms ("overload",
# "trained", "aerobic", "fitness", "contraction") mostly mean pressure/iron overload, trained
# immunity, aerobic glycolysis or genetic fitness. The first run with the loose regex gave
# 38 off-topic of 42 analysable in its first 319 papers.
TOPIC = re.compile(
    r"exercis|physical(ly)? (activ|inactiv|train|fitness)|endurance (train|exercis|capacity|running|athlet)|"
    r"resistance[- ](train|exercis)|strength[- ]train|interval[- ]train|HIIT|treadmill|wheel[- ]running|"
    r"running wheel|voluntary (wheel|running)|swim(ming)?[- ](train|exercis)|sedentar|athlet|detrain|bed[- ]rest|"
    r"hind[- ]?limb (unloading|suspension)|(muscle|limb) (unloading|disuse|immobili)|immobili[sz]ation|"
    r"cardiorespiratory fitness|aerobic (train|exercis|capacity|fitness)|VO2 ?max|marathon|exerkine|"
    r"running (train|exercis)|trained (mice|rats|athletes|subjects|individuals|men|women|state)|"
    r"training (program|protocol|intervention|regimen)", re.I)
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
TERMS = ["exercise", "exercised", "exercising", "training", "trained", "detraining", "running", "runners",
         "treadmill", "wheel", "swimming", "endurance", "resistance training", "strength training",
         "HIIT", "interval training", "aerobic", "sedentary", "athletes", "athlete", "physical activity",
         "physical inactivity", "physical fitness", "cardiorespiratory fitness", "VO2max", "cycling",
         "marathon", "sprint", "unloading", "hindlimb suspension", "bed rest", "immobilization", "disuse",
         "overload", "muscle contraction", "electrical stimulation", "myokine", "exerkine", "sport"]
ORG = '("Homo sapiens"[Organism] OR "Mus musculus"[Organism] OR "Rattus norvegicus"[Organism])'

ex = list(csv.DictReader(open(os.path.join(HERE, "exclude_papers.csv"), encoding="utf-8")))
seen = set()
for r in ex:
    if r["paper_id"].startswith("PMID"):
        seen.add("pmid:" + r["paper_id"][4:])
    for k, v in (("pmid", r["pmid"]), ("pmcid", r["pmcid"]), ("doi", r["doi"])):
        if v:
            seen.add(f"{k}:{v.lower()}")
    t = re.sub(r"\W+", "", (r["title"] or "").lower())[:80]
    if len(t) > 20:
        seen.add("t:" + t)
seen_gse = set(open(os.path.join(HERE, "exclude_gse.txt"), encoding="utf-8").read().split())


def is_seen(r):
    keys = [f"pmid:{r.get('pmid')}", f"pmcid:{(r.get('pmcid') or '').lower()}", f"doi:{(r.get('doi') or '').lower()}",
            "t:" + re.sub(r"\W+", "", (r.get("title") or "").lower())[:80]]
    return any(k in seen for k in keys if not k.endswith(":"))


# 1. every matching GEO series
term = "(" + " OR ".join(f'"{t}"' if " " in t else t for t in TERMS) + f") AND gse[Entry Type] AND {sc._GEO_RNASEQ} AND {ORG}"
uids, start = [], 0
while True:
    s = http.get(f"{sc.EUTILS}/esearch.fcgi", {"db": "gds", "term": term, "retmax": 5000, "retstart": start,
                                                 "retmode": "json"})
    res = json.loads(s)["esearchresult"]
    uids += res["idlist"]
    start += 5000
    if start >= int(res["count"]):
        break
print(f"GEO series matching the terms: {len(uids)}", flush=True)

series = []
for i in range(0, len(uids), 200):
    s = http.get(f"{sc.EUTILS}/esummary.fcgi", {"db": "gds", "id": ",".join(uids[i:i + 200]), "retmode": "json"})
    res = json.loads(s).get("result", {}) if s else {}
    for uid in res.get("uids", []):
        r = res[uid]
        series.append({"gse": r.get("accession", ""), "title": r.get("title", ""), "summary": r.get("summary", ""),
                       "taxon": r.get("taxon", ""), "n_samples": r.get("n_samples", ""), "pdat": r.get("pdat", ""),
                       "pubmedids": ";".join(str(p) for p in r.get("pubmedids") or [])})

pmid_gse, no_pmid = {}, []
for s in series:
    if s["gse"] in seen_gse:
        s["fate"] = "series seen before"
    elif not TOPIC.search(s["title"] + " " + s["summary"]):
        s["fate"] = "no exercise term in GEO title/summary"
    elif s["pubmedids"]:
        s["fate"] = "pubmed-linked"
        for p in s["pubmedids"].split(";"):
            pmid_gse.setdefault(p, []).append(s["gse"])
    else:
        s["fate"] = "no pubmed link"
        no_pmid.append(s)
print(f"on topic and new: {len(pmid_gse)} linked PMIDs, {len(no_pmid)} series without a PubMed link", flush=True)

rows = sc._pubmed_summaries(list(pmid_gse), http, "geo_all")
for r in rows:
    r["linked_gse"] = ";".join(dict.fromkeys(pmid_gse.get(r["pmid"], [])))
    r["query"] = "geo_all"

# 2. series without a PubMed link -> papers that mention the accession (Europe PMC)
epmc = {}
for s in no_pmid:
    body = http.get(EPMC, {"query": f'"{s["gse"]}"', "format": "json", "resultType": "lite", "pageSize": 25})
    hits = (json.loads(body).get("resultList", {}).get("result") or []) if body else []
    hits = [h for h in hits if h.get("source") in ("MED", "PMC")]
    s["epmc_hits"] = len(hits)
    for h in hits:
        key = h.get("pmid") or h.get("pmcid")
        if not key:
            continue
        e = epmc.setdefault(key, {"paper_id": f"PMID{h['pmid']}" if h.get("pmid") else h["pmcid"],
                                  "source": "geo_epmc", "title": (h.get("title") or "").strip(),
                                  "year": h.get("pubYear", ""), "doi": (h.get("doi") or "").lower(),
                                  "pmid": h.get("pmid", ""), "pmcid": h.get("pmcid", ""), "pdf_url": "",
                                  "linked_gse": "", "query": "geo_epmc"})
        e["linked_gse"] = ";".join(filter(None, dict.fromkeys(e["linked_gse"].split(";") + [s["gse"]])))
print(f"Europe PMC: {len(epmc)} papers mention one of those series", flush=True)

out, have = [], set()
for r in rows + list(epmc.values()):
    if is_seen(r) or (r["pmid"] and r["pmid"] in have):
        continue
    have.add(r["pmid"] or r["pmcid"])
    out.append(r)
fields = ["paper_id", "source", "title", "year", "doi", "pmid", "pmcid", "pdf_url", "linked_gse", "query"]
with open(os.path.join(HERE, "papers.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(out)
with open(os.path.join(HERE, "series.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["gse", "taxon", "n_samples", "pdat", "pubmedids", "fate", "epmc_hits", "title"],
                       extrasaction="ignore")
    w.writeheader()
    w.writerows(series)
from collections import Counter  # noqa: E402
print("series fates:", dict(Counter(s["fate"] for s in series)))
print(f"{len(out)} new papers -> papers.csv", dict(Counter(r['source'] for r in out)),
      "with PMCID:", sum(bool(r["pmcid"]) for r in out))
