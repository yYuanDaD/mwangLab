"""Print a compact evidence dossier for given paper_ids (for reviewing screener verdicts)."""
import csv, json, os, re, sys
sys.path.insert(0, os.getcwd())
from tools import paper_structure as ps_struct

RUN = "test/experiments/paper_screen_20261019"
REV = os.path.join(RUN, "review_20261027")
papers = {r["paper_id"]: r for r in csv.DictReader(open(os.path.join(RUN, "papers.csv"), encoding="utf-8"))}
screen = {r["paper_id"]: r for r in csv.DictReader(open(os.path.join(REV, "screen.csv"), encoding="utf-8"))}
geo = {r["paper_id"]: json.loads(r["geo_linked"]) for r in csv.DictReader(open(os.path.join(REV, "geo_by_pmid.csv"), encoding="utf-8"))} \
    if os.path.exists(os.path.join(REV, "geo_by_pmid.csv")) else {}
ACC = re.compile(r"\b(GSE\d+|PRJ[NED][A-Z]?\d+|SR[PAR]\d+|E-[A-Z]{4}-\d+|PXD\d+|HRA\d+|CRA\d+|OEP\d+|phs\d+)")
KEY = re.compile(r"deposit|availab|accession|upon (reasonable )?request|GEO\b|Gene Expression Omnibus|repositor", re.I)

def doc_for(p):
    stem = re.sub(r"[^A-Za-z0-9._-]", "_", p.get("pmcid") or p.get("paper_id") or "paper")
    path = os.path.join(RUN, "papers", f"{stem}.paper.json")
    return ps_struct.load(path) if os.path.exists(path) else None

for pid in sys.argv[1:]:
    p, s = papers[pid], screen[pid]
    print("=" * 100)
    print(f"{pid} | PMID {p['pmid']} | {p['pmcid']} | doi {p['doi']} | {p['source']} | {p['year']} | linked_gse={p['linked_gse']}")
    print("TITLE:", p["title"])
    print(f"VERDICT: {s['verdict']} {s['reason']} | own={s['own_gse']} cited={s['cited_gse'][:200]} other={s['other_repos']} text={s['text_source']}")
    print("GEO-by-PMID:", json.dumps(geo.get(pid, "n/a"), ensure_ascii=False)[:600])
    for se in json.loads(s["series_json"] or "[]"):
        f = se.get("files") or {}
        d = se.get("design") or {}
        print(f"  SERIES {se['gse']} {se['verdict']} {se['reason']} type={se['data_type']} taxon={se['taxon']} n={se['n_samples']}")
        if f: print("    files:", json.dumps({k: f[k] for k in f if k != 'value_check'}, ensure_ascii=False)[:500])
        if f.get("value_check"): print("    value_check:", json.dumps(f["value_check"], ensure_ascii=False)[:400])
        if d: print("    design:", json.dumps(d, ensure_ascii=False)[:400])
    doc = doc_for(p)
    if not doc:
        print("  (no cached full text)"); continue
    blocks = doc.get("blocks", [])
    abstract = " ".join(b["text"] for b in blocks if b.get("section_class") == "abstract")[:900]
    print("ABSTRACT:", abstract)
    shown = 0
    for b in blocks:
        t = b.get("text", "")
        if ACC.search(t) or (b.get("section_class") == "data_availability") or \
           (b.get("section_class") in ("methods", "other") and re.search(r"deposit|upon (reasonable )?request|accession", t, re.I)):
            print(f"  [{b.get('id')}|{b.get('section_class')}] {t[:700]}")
            shown += 1
            if shown >= 6: break
