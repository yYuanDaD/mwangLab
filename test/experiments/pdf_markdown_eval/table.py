"""Markdown tables for docs/status/PDF_MARKDOWN_EVAL.md from results_*.json."""
import json, re, sys
from statistics import median

rows = []
for f in sys.argv[1:]:
    rows += json.load(open(f, encoding="utf-8"))
seen, out = set(), []
for r in rows:
    k = (r["paper"], r["backend"])
    if k not in seen:
        seen.add(k)
        out.append(r)
ORDER = {"jats": 0, "docling": 1, "pymupdf4llm": 2}
out.sort(key=lambda r: (r["kind"] != "both", r["paper"], ORDER.get(r["backend"], 3)))
jats = {r["paper"]: r for r in out if r["backend"] == "jats"}


def n(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def t1(r):
    tm = r.get("table_match") or {}
    return next((v["cell_match"] for k, v in tm.items() if n(k) == "table1"), None)


def fmt(x):
    return "–" if x is None else (f"{x:.2f}" if isinstance(x, float) else str(x))


def mrd(r):
    return " ".join(c[0].upper() if r["has"][c] else "·" for c in ("methods", "results", "data_availability"))


print("### Papers with JATS (10)\n")
print("| paper | source | sec | pages | M R D | tables (with cells) | Table 1 cells | all tables cells | GSE in JATS: found / same class | extra GSE | header leak | ref leak | title |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in out:
    if r["kind"] != "both":
        continue
    j = jats[r["paper"]]
    if r.get("error"):
        print(f"| {r['paper']} | {r['backend']} | {r['seconds']} | | ERROR {r['error'][:80]} |")
        continue
    if r["backend"] == "jats":
        g = ", ".join(f"{a} ({'/'.join(v['pdf'])})" for a, v in r["gse"].items()) or "none"
        print(f"| **{r['paper']}** | JATS | – | {r['pages']} | {mrd(r)} | {r['n_tables']} ({r['n_tables_text']}) | – | – | {g} | – | – | – | – |")
        continue
    g = r["gse"]
    jg = [a for a, v in g.items() if v["jats"]]
    gs = (f"{sum(g[a]['found'] for a in jg)}/{len(jg)} / {sum(bool(g[a]['same_class']) for a in jg)}/{len(jg)}"
          if jg else "–")
    extra = ",".join(a for a, v in g.items() if v["found"] and not v["jats"]) or "–"
    tm = r.get("table_match") or {}
    allc = round(sum(v["cell_match"] for v in tm.values()) / len(tm), 2) if tm else None
    title_ok = "ok" if n(r.get("title"))[:40] and n(r.get("title"))[:40] == n(j.get("title"))[:40] else "✗"
    print(f"| | {r['backend']} | {r['seconds']} | | {mrd(r)} | {r['n_tables']} ({r['n_tables_text']}) | {fmt(t1(r))} | {fmt(allc)} | {gs} | {extra} | {r['n_header_leak']} | {r['n_ref_leak']} | {title_ok} |")

print("\n### PDF-only papers (7)\n")
print("| paper | backend | sec | pages | M R D | tables (with cells) | figures | GSE found (section class) | header leak | title |")
print("|---|---|---|---|---|---|---|---|---|---|")
for r in out:
    if r["kind"] == "both":
        continue
    if r.get("error"):
        print(f"| {r['paper']} | {r['backend']} | {r['seconds']} | | ERROR {r['error'][:80]} |")
        continue
    g = ", ".join(f"{a} ({'/'.join(v['pdf'])})" for a, v in r["gse"].items()) or "none"
    print(f"| {r['paper']} | {r['backend']} | {r['seconds']} | {r['pages']} | {mrd(r)} | {r['n_tables']} ({r['n_tables_text']}) | {r['n_figures']} | {g} | {r['n_header_leak']} | {(r.get('title') or '(none)')[:40]} |")

print("\n### Totals\n")
print("| backend | conversions | median sec | total sec | M/R/D found vs JATS | JATS tables with cells → matched ≥0.8 | GSE found / same class (JATS papers) | header-leak blocks | ref-leak blocks | titles ok (JATS papers) |")
print("|---|---|---|---|---|---|---|---|---|---|")
for be in ("docling", "pymupdf4llm"):
    rs = [r for r in out if r["backend"] == be and not r.get("error")]
    both = [r for r in rs if r["kind"] == "both"]
    hit = tot = 0
    for r in both:
        j = jats[r["paper"]]
        for c in ("methods", "results", "data_availability"):
            if j["has"][c]:
                tot += 1
                hit += r["has"][c]
    tabs = [v["cell_match"] for r in both for v in (r.get("table_match") or {}).values()]
    gf = gs = gt = 0
    for r in both:
        for a, v in r["gse"].items():
            if v["jats"]:
                gt += 1
                gf += v["found"]
                gs += bool(v["same_class"])
    tok = sum(1 for r in both if n(r.get("title"))[:40] == n(jats[r["paper"]].get("title"))[:40] and n(r.get("title")))
    secs = [r["seconds"] for r in rs]
    print(f"| {be} | {len(rs)} | {median(secs):.0f} | {sum(secs):.0f} | {hit}/{tot} | {sum(1 for x in tabs if x >= 0.8)}/{len(tabs)} | {gf}/{gt} / {gs}/{gt} | {sum(r['n_header_leak'] for r in rs)} | {sum(r['n_ref_leak'] for r in rs)} | {tok}/{len(both)} |")
