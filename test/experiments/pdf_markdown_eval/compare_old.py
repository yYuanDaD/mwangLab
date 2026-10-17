"""Score the same converted Markdown with an older and the current parse_markdown.

Usage (repo root): python test/experiments/pdf_markdown_eval/compare_old.py old_paper_structure.py <eval_root>/out
"""
import sys, json, re, os, importlib.util
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
old = load(sys.argv[1], "ps_old")  # e.g. git show 8216daa:tools/paper_structure.py > old.py
new = load("tools/paper_structure.py", "ps_new")
OUT = sys.argv[2]
n = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())
def score(ps, md, jats):
    d = ps.parse_markdown(md)
    has = {c: any(b["section_class"] == c for b in d["blocks"]) for c in ("methods", "results", "data_availability")}
    tabs = [b for b in d["blocks"] if b["kind"] == "table" and not b.get("image_only")]
    labelled = sum(1 for t in tabs if t.get("label"))
    gse = {a for a in d["accession_mentions"] if a.startswith("GSE")}
    return d, has, len(tabs), labelled, gse
agg = {}
for p in sorted(os.listdir(OUT)):
    jp = f"{OUT}/{p}/jats/{p}.paper.json"
    j = json.load(open(jp, encoding="utf-8")) if os.path.exists(jp) else None
    for be in ("docling", "pymupdf4llm"):
        md = open(f"{OUT}/{p}/{be}/{p}.converted.md", encoding="utf-8").read()
        for tag, ps in (("old", old), ("new", new)):
            d, has, nt, nl, gse = score(ps, md, j)
            a = agg.setdefault((be, tag), {"title_ok": 0, "titled": 0, "mrd": 0, "mrd_tot": 0, "tables": 0, "labelled": 0, "gse": 0, "gse_tot": 0, "papers": 0})
            a["papers"] += 1; a["tables"] += nt; a["labelled"] += nl
            if j:
                a["titled"] += 1; a["title_ok"] += n(d["title"])[:40] == n(j.get("title"))[:40] and bool(n(d["title"]))
                for c in has:
                    if any(b["section_class"] == c for b in j["blocks"]):
                        a["mrd_tot"] += 1; a["mrd"] += has[c]
                jg = {x for x in j["accession_mentions"] if x.startswith("GSE")}
                a["gse_tot"] += len(jg); a["gse"] += len(jg & gse)
print("| backend | parser | titles ok (10 JATS papers) | M/R/D found vs JATS | GSE found vs JATS | tables with cells (17 papers) | of which labelled |")
print("|---|---|---|---|---|---|---|")
for (be, tag), a in sorted(agg.items(), key=lambda x: (x[0][0], x[0][1] != "old")):
    print(f"| {be} | {'before (8216daa)' if tag=='old' else 'after'} | {a['title_ok']}/{a['titled']} | {a['mrd']}/{a['mrd_tot']} | {a['gse']}/{a['gse_tot']} | {a['tables']} | {a['labelled']} |")
