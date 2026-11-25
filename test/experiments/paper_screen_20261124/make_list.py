"""Build the new-batch list from the shard screens: one row per analyzable paper.

Merges screen.csv (shard a, this folder) and shard_*/screen.csv, drops series already
screened or run before (exclude_gse.txt) and duplicates inside the batch (a paper once; a
GEO series once, the first paper keeps it), and adds review hints for the known screen
weak spots (PROBLEM_THEMES #18 of the 211 run). Writes new_batch.csv and prints counts.

    python test/experiments/paper_screen_20261124/make_list.py
"""
import csv
import glob
import json
import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
csv.field_size_limit(1 << 30)
EX = re.compile(r"exerc|train|run|treadmill|wheel|swim|sedent|active|inactiv|endur|resist|hiit|interval|"
                r"athlet|bout|pre|post|base|unload|suspen|bed|immobil|disuse|overload|contract|stim|"
                r"\bex\b|\bsed\b|\bctrl\b|\btr\b|\bex\d|\bsed\d|\bE\b|\bS\b|fit", re.I)
INVITRO = re.compile(r"\b(in vitro|cultured|C2C12|myotubes?|cell line|HUVEC|serum[- ]treated|conditioned medium|"
                     r"organoids?)\b", re.I)

papers = {r["paper_id"]: r for r in csv.DictReader(open(os.path.join(HERE, "papers.csv"), encoding="utf-8"))}
old_gse = set(open(os.path.join(HERE, "exclude_gse.txt"), encoding="utf-8").read().split())
files = [os.path.join(HERE, "screen.csv")] + sorted(glob.glob(os.path.join(HERE, "shard_*", "screen.csv")))
rows = [r for f in files for r in csv.DictReader(open(f, encoding="utf-8"))]
print("screened:", len(rows), dict(Counter(r["verdict"] for r in rows)))

out, seen_p, seen_g, dropped = [], set(), set(), Counter()
for r in rows:
    if r["verdict"] != "analyzable":
        continue
    p = papers.get(r["paper_id"], {})
    keys = {k for k in (r["paper_id"], r.get("pmcid"), r.get("doi")) if k}
    if keys & seen_p:
        dropped["same paper"] += 1
        continue
    gses = [g for g in r["analyzable_gse"].split(";") if g]
    new = [g for g in gses if g not in old_gse and g not in seen_g]
    if not new:
        dropped["series already screened/run before" if any(g in old_gse for g in gses) else "series twice in batch"] += 1
        continue
    seen_p |= keys
    seen_g |= set(new)
    series = [s for s in json.loads(r["series_json"] or "[]") if s["gse"] in new]
    groups = [(s.get("design") or {}).get("groups") or {} for s in series]
    labels = " ".join(str(k) for g in groups for k in g)
    hints = []
    if r.get("text_source") == "geo_only":
        hints.append("no full text: ownership and topic from the GEO record only")
    if labels and not EX.search(labels):
        hints.append("group labels name no exercise arm")
    if INVITRO.search(r["title"]):
        hints.append("title suggests in-vitro / mediator design")
    out.append({
        "paper_id": r["paper_id"], "pmid": p.get("pmid", ""), "pmcid": r.get("pmcid", ""), "doi": r.get("doi", ""),
        "year": p.get("year", ""), "title": r["title"], "gse": ";".join(new),
        "taxon": ";".join(s.get("taxon", "") for s in series),
        "n_samples": ";".join(str(s.get("n_samples", "")) for s in series),
        "groups": " || ".join(", ".join(f"{k}={v}" for k, v in g.items()) for g in groups),
        "route": r.get("route", ""),
        "files": ";".join(str((s.get("files") or {}).get("status", "")) for s in series),
        "screen_flags": r.get("flags", ""), "review_hints": "; ".join(hints),
        "text_source": r.get("text_source", ""), "source": r.get("source", ""),
    })
with open(os.path.join(HERE, "new_batch.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
print("analyzable, unique and new:", len(out), "dropped:", dict(dropped))
print("route:", dict(Counter(o["route"] for o in out)))
print("taxon:", dict(Counter(o["taxon"] for o in out)))
print("source:", dict(Counter(o["source"] for o in out)))
print("with a review hint:", sum(bool(o["review_hints"]) for o in out),
      dict(Counter(h for o in out for h in o["review_hints"].split("; ") if h)))
