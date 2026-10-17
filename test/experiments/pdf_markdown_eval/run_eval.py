"""Convert each PDF with each backend and compare it with the Europe PMC JATS copy.

Layout of <eval_root>: both/<PMCID>.pdf (papers with JATS), pdfonly/<stem>.pdf.
Writes <eval_root>/out/<paper>/{jats,<backend>}/ and <eval_root>/results_<backend>.json.

    python test/experiments/pdf_markdown_eval/run_eval.py <eval_root> docling
    python test/experiments/pdf_markdown_eval/run_eval.py <eval_root> pymupdf4llm
    python test/experiments/pdf_markdown_eval/run_eval.py <eval_root> docling rescore   # re-parse saved .converted.md

Run from the repository root. No LLM calls; network only for the JATS download.
"""
import sys, os, json, time, re, glob
sys.path.insert(0, os.getcwd())
from tools import paper_structure as ps, pdf_markdown as pm
import pymupdf, xml.etree.ElementTree as ET

ROOT = sys.argv[1]           # E:/agent/pdf_eval
BACKENDS = sys.argv[2].split(",")
RESCORE = len(sys.argv) > 3 and sys.argv[3] == "rescore"
PREV = {}
if RESCORE:
    for be in BACKENDS:
        PREV[be] = json.load(open(os.path.join(ROOT, f"results_{be}.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "out")

def norm(s):
    s = re.sub(r"[*_`\\]", "", s or "").lower()
    s = s.replace("−", "-").replace("–", "-").replace("±", "+-")
    return re.sub(r"\s+", "", s)

def table_cells(text):
    cells = []
    for ln in text.splitlines():
        if ln.startswith("|") and not re.match(r"^\|(-|\s|\|)+$", ln):
            cells += [norm(c) for c in ln.strip().strip("|").split("|")]
    return [c for c in cells if c and c not in ("-",)]

def classes_with_blocks(doc):
    return sorted({b["section_class"] for b in doc["blocks"] if b["kind"] == "paragraph"})

def running_headers(pdf):
    d = pymupdf.open(pdf); cnt = {}
    for page in d:
        blocks = [b for b in page.get_text("blocks") if b[6] == 0 and b[4].strip()]
        if not blocks: continue
        h = page.rect.height
        for b in blocks:
            if b[1] < 0.08 * h or b[3] > 0.93 * h:
                for ln in b[4].splitlines():
                    t = ln.strip()
                    if len(t) >= 12 and not re.fullmatch(r"[\d\s/.of-]+", t):
                        cnt[t] = cnt.get(t, 0) + 1
    n = len(d)
    return [t for t, c in cnt.items() if c >= max(3, n // 3)]

def ref_titles(xml_path):
    if not xml_path or not os.path.exists(xml_path): return []
    root = ET.parse(xml_path).getroot()
    out = []
    for ref in root.iter():
        if ref.tag.rsplit("}", 1)[-1] != "ref": continue
        for e in ref.iter():
            if e.tag.rsplit("}", 1)[-1] == "article-title":
                t = " ".join("".join(e.itertext()).split())
                if len(t) >= 40: out.append(t)
    return out

def leaks(doc, headers, refs):
    hdr, ref = [], []
    hn = [norm(h) for h in headers]
    rn = [norm(r)[:60] for r in refs]
    for b in doc["blocks"]:
        tn = norm(b["text"])
        if any(h and h in tn for h in hn): hdr.append(b["id"])
        if any(r and r in tn for r in rn): ref.append(b["id"])
    return hdr, ref

def gse_compare(jdoc, pdoc):
    res = {}
    jb = {b["id"]: b for b in jdoc["blocks"]} if jdoc else {}
    pb = {b["id"]: b for b in pdoc["blocks"]}
    jacc = {a: w for a, w in (jdoc or {}).get("accession_mentions", {}).items() if a.startswith("GSE")} if jdoc else {}
    pacc = {a: w for a, w in pdoc.get("accession_mentions", {}).items() if a.startswith("GSE")}
    for a in sorted(set(jacc) | set(pacc)):
        jc = sorted({jb[i]["section_class"] for i in jacc.get(a, [])})
        pc = sorted({pb[i]["section_class"] for i in pacc.get(a, [])})
        res[a] = {"jats": jc, "pdf": pc, "found": bool(pc), "same_class": bool(set(jc) & set(pc)) if jc else None}
    return res

def best_table_match(jtab, ptabs):
    jc = table_cells(jtab["text"])
    if not jc: return None, 0.0
    best = (None, 0.0)
    for p in ptabs:
        pc = set(table_cells(p["text"]))
        if not pc: continue
        f = sum(1 for c in jc if c in pc) / len(jc)
        if f > best[1]: best = (p["id"], f)
    return best

def main():
    rows = []
    papers = []
    for d, kind in (("both", "both"), ("pdfonly", "pdf_only")):
        for pdf in sorted(glob.glob(os.path.join(ROOT, d, "*.pdf"))):
            papers.append((os.path.splitext(os.path.basename(pdf))[0], pdf, kind))
    for pid, pdf, kind in papers:
        jdoc, xml_path = None, None
        if kind == "both":
            jdir = os.path.join(OUT, pid, "jats")
            jj = os.path.join(jdir, f"{pid}.paper.json")
            if not os.path.exists(jj):
                xml, url = ps.fetch_jats(pid)
                doc = ps.parse_jats(xml, source=f"Europe PMC ({pid})", fetched_url=url)
                ps.save(doc, jdir, pid, raw_xml=xml)
            jdoc = ps.load(jj); xml_path = os.path.join(jdir, f"{pid}.jats.xml")
        headers = running_headers(pdf)
        refs = ref_titles(xml_path)
        npages = len(pymupdf.open(pdf))
        if jdoc:
            rows.append(summ(pid, kind, "jats", jdoc, None, 0, headers, refs, npages, None))
        for be in BACKENDS:
            t0 = time.time()
            conv = os.path.join(OUT, pid, be, f"{pid}.converted.md")
            if RESCORE:
                # Re-parse the saved converter output with the current parser; keep timing.
                old = next((r for r in PREV.get(be, []) if r["paper"] == pid and r["backend"] == be), {})
                pdoc = ps.parse_markdown(open(conv, encoding="utf-8").read(), quality=f"pdf_markdown:{be}")                     if os.path.exists(conv) else None
                err, dt = old.get("error"), old.get("seconds", 0)
                if pdoc is not None:
                    ps.save(pdoc, os.path.join(OUT, pid, be), pid)
            else:
                try:
                    pdoc, paths = pm.save_pdf(pdf, os.path.join(OUT, pid, be), pid, be)
                    err = None
                except Exception as e:
                    pdoc, err = None, f"{type(e).__name__}: {e}"
                dt = time.time() - t0
            rows.append(summ(pid, kind, be, pdoc, jdoc, dt, headers, refs, npages, err))
            print(json.dumps(rows[-1], ensure_ascii=False)[:400], flush=True)
    name = f"results_{'_'.join(BACKENDS)}{'_rescored' if RESCORE else ''}.json"
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)

def summ(pid, kind, be, doc, jdoc, dt, headers, refs, npages, err):
    r = {"title": (doc or {}).get("title", ""), "paper": pid, "kind": kind, "backend": be, "pages": npages, "seconds": round(dt, 1), "error": err}
    if doc is None: return r
    tabs = [b for b in doc["blocks"] if b["kind"] == "table"]
    r.update({
        "quality": doc.get("structure_quality"),
        "n_sections": len(doc["sections"]), "n_blocks": len(doc["blocks"]),
        "classes": classes_with_blocks(doc),
        "has": {c: any(b["section_class"] == c for b in doc["blocks"]) for c in ("methods", "results", "data_availability")},
        "n_tables": len(tabs), "n_tables_text": sum(1 for t in tabs if not t.get("image_only")),
        "n_figures": sum(1 for b in doc["blocks"] if b["kind"] == "figure"),
        "table_labels": [t.get("label", "") for t in tabs],
        "chars": sum(len(b["text"]) for b in doc["blocks"]),
    })
    hdr, ref = leaks(doc, headers, refs)
    r["header_leak_blocks"] = hdr[:20]; r["n_header_leak"] = len(hdr)
    r["ref_leak_blocks"] = ref[:20]; r["n_ref_leak"] = len(ref)
    r["gse"] = gse_compare(jdoc, doc) if jdoc else gse_compare(None, doc)
    if jdoc and doc is not jdoc:
        ptabs = [t for t in tabs if not t.get("image_only")]
        tm = {}
        for jt in jdoc["blocks"]:
            if jt["kind"] == "table" and not jt.get("image_only"):
                bid, f = best_table_match(jt, ptabs)
                tm[jt.get("label") or jt["id"]] = {"pdf_block": bid, "cell_match": round(f, 2)}
        r["table_match"] = tm
    return r

main()
