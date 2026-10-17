"""Structured paper full text (tools/paper_structure.py) — offline, NO LLM, NO network.

Guards the change that stopped flattening Europe PMC JATS XML into one line of text:
sections keep their class (methods/results/data_availability), tables stay tables,
figure legends stay separate, and every block has a citable ID.

Fixtures (test/fixtures/papers/) are real Europe PMC fullTextXML downloads:
  PMC12989000  Springer layout; Data availability in <back><notes>
  PMC12803081  uppercase section titles; DATA ACCESS nested under METHODS
  PMC7093805   Data in Brief; specification tables, references inside <body>
  PMC12658470  Wiley; Europe PMC "Associated Data" wrapper repeats supplements and DA

Run:  python test/unit/test_paper_structure.py
"""

import json
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools import paper_structure as ps

FIX = os.path.join("test", "fixtures", "papers")


def _load(pmcid: str) -> dict:
    with open(os.path.join(FIX, f"{pmcid}.xml"), "rb") as f:
        return ps.parse_jats(f.read(), source=f"fixture {pmcid}")


def test_springer_sections_and_data_availability():
    doc = _load("PMC12989000")
    assert doc["pmcid"] == "PMC12989000"
    classes = {s["class"] for s in doc["sections"]}
    assert {"abstract", "introduction", "methods", "results", "discussion",
            "data_availability"} <= classes, classes
    # Abstract mixes <p> and <sec>; both must be kept.
    abs_blocks = [b for b in doc["blocks"] if b["section_id"] == "ABS"]
    assert abs_blocks[0]["text"].startswith("Chronic kidney disease"), abs_blocks[0]["text"][:60]
    # The accession is indexed in both the Methods paragraph and the DA statement.
    where = doc["accession_mentions"]["GSE309619"]
    assert "DA.p1" in where and "S2.2.p1" in where, where
    # Title-word query returns the statistics paragraph verbatim.
    stats = ps.read_section(doc, "statistical analyses")
    assert "Student" in stats and "[S2.4.p1]" in stats, stats
    assert ps.resolve_locator(doc, "S2.4.p1")["section_class"] == "methods"
    # Subsections inherit the parent's class.
    assert all(s["class"] == "methods" for s in doc["sections"] if s["id"].startswith("S2."))


def test_nested_data_access_and_supplement():
    doc = _load("PMC12803081")
    da = ps.read_section(doc, "data_availability")
    assert "upon request" in da and "S4.16" in da, da
    sup = [b for b in doc["blocks"] if b["kind"] == "supplement"]
    assert sup and sup[0]["files"], sup
    # This paper keeps its six figures in <floats-group> after <back>.
    assert sum(b["kind"] == "figure" for b in doc["blocks"]) == 6
    # Methods subsections stay methods even though the parent title is uppercase.
    rna = ps.read_section(doc, "S4.9")
    assert "RNA-seq" in rna, rna[:200]


def test_tables_figures_and_references_skipped():
    doc = _load("PMC7093805")
    tables = [b for b in doc["blocks"] if b["kind"] == "table"]
    assert len(tables) >= 2
    spec = next(b for b in tables if "Data accessibility" in b["text"])
    assert "| Data accessibility |" in spec["text"] and "GSE129694" in spec["text"]
    assert "GSE129694" in doc["accession_mentions"]
    assert not any("reference" in (s["title"] or "").lower() for s in doc["sections"])
    fig = ps.resolve_locator(doc, "Fig. 1")
    assert fig and fig["kind"] == "figure" and fig["id"] == "FIG1", fig
    legends = ps.read_section(doc, "figures")
    assert legends.count("[FIG") == sum(b["kind"] == "figure" for b in doc["blocks"])


def test_europepmc_associated_data_not_duplicated():
    doc = _load("PMC12658470")
    assert not any((s["title"] or "").lower() == "associated data" for s in doc["sections"])
    assert sum(b["kind"] == "supplement" for b in doc["blocks"]) == 3
    assert sum(s["class"] == "data_availability" for s in doc["sections"]) == 1
    assert "Differential Expression" in ps.read_section(doc, "differential expression")


_SYNTHETIC = b"""<?xml version="1.0"?>
<article xmlns:xlink="http://www.w3.org/1999/xlink">
 <front><article-meta>
  <article-id pub-id-type="pmcid">PMC1</article-id>
  <title-group><article-title>Synthetic</article-title></title-group>
  <abstract><sec><title>Background</title><p>Why.</p></sec><sec><title>Methods</title><p>How.</p></sec></abstract>
 </article-meta></front>
 <body>
  <sec><title>Results and discussion</title>
   <p>Groups are in <xref ref-type="table" rid="t1">Table 1</xref>.
    <fig id="f1"><label>Figure 1</label><caption><p>Nested figure.</p></caption></fig></p>
   <table-wrap id="t1"><label>Table 1</label><caption><p>Groups</p></caption>
    <table>
     <thead><tr><th rowspan="2">Group</th><th colspan="2">Samples</th></tr>
            <tr><th>Pre</th><th>Post</th></tr></thead>
     <tbody><tr><td rowspan="2">Exercise</td><td>GSM1</td><td>GSM2</td></tr>
            <tr><td>GSM3</td><td>GSM4</td></tr>
            <tr><td>Sedentary</td><td>GSM5</td><td>GSM6</td></tr></tbody>
    </table>
    <table-wrap-foot><p>Paired by subject.</p></table-wrap-foot>
   </table-wrap>
  </sec>
  <sec><title>References</title><p>should be skipped</p></sec>
 </body>
 <back><sec sec-type="data-availability"><title>Data Availability Statement</title><p>GSE999999.</p></sec></back>
</article>"""


def test_synthetic_spans_nested_floats_structured_abstract():
    doc = ps.parse_jats(_SYNTHETIC)
    abs_text = [b["text"] for b in doc["blocks"] if b["section_id"] == "ABS"]
    assert abs_text == ["**Background.** Why.", "**Methods.** How."], abs_text
    s1 = next(s for s in doc["sections"] if s["id"] == "S1")
    assert s1["class"] == "results"  # "Results and discussion": first rule wins
    assert len([s for s in doc["sections"] if s["id"].startswith("S")]) == 1  # References dropped
    fig = ps.resolve_locator(doc, "Figure 1")
    assert fig and fig["section_id"] == "S1" and "Nested figure" in fig["text"]
    para = ps.resolve_locator(doc, "S1.p1")
    assert "Nested figure" not in para["text"]  # floats are not duplicated into paragraphs
    tab = ps.resolve_locator(doc, "Table 1")["text"]
    assert "| Group | Samples / Pre | Samples / Post |" in tab, tab
    assert "| Exercise | GSM1 | GSM2 |" in tab and "| Exercise | GSM3 | GSM4 |" in tab, tab
    assert "Paired by subject." in tab
    assert doc["accession_mentions"] == {"GSE999999": ["DA.p1"]}


def test_pdf_heuristic_fallback():
    pages = [
        "A title line\nAbstract\nWe studied exercise.\n1. Introduction\nMuscle adapts.",
        "2 Materials and methods\nMice ran for 4 weeks (GSE123456).\nResults\nGenes changed.\n"
        "Data availability\nData are in GEO.\nReferences\n1. Someone et al.",
    ]
    doc = ps.parse_pdf_pages(pages, source="pdf")
    assert doc["structure_quality"] == "pdf_heuristic"
    cls = [s["class"] for s in doc["sections"]]
    assert cls[:1] == ["other"] and "methods" in cls and "data_availability" in cls, cls
    assert "Someone" not in json.dumps(doc["blocks"])  # stops at References
    assert doc["accession_mentions"]["GSE123456"][0].startswith("S")


# Shaped like Docling output: every heading at "##", unnumbered subsections, image
# placeholders, a caption line before a pipe table, a running header on each page.
_DOCLING_MD = """## Treadmill training remodels muscle

Journal of Synthetic Exercise Biology

A. Author, B. Author

## Abstract

We trained mice for six weeks.

## Introduction

Earlier work (GSE12345) used microarrays.

Journal of Synthetic Exercise Biology

## Materials and methods

## Animals

Male mice (n = 6 per group) were sedentary or trained. The training

continued for six weeks.

Table 1 Sample groups used for RNA-seq.

| Group     |   n | Sex   |
|-----------|-----|-------|
| Sedentary |   6 | M     |
| Trained   |   6 | M     |

## Statistical analysis

DESeq2, padj < 0.05.

Journal of Synthetic Exercise Biology

## Results

<!-- image -->

Figure 1. Volcano plot of trained versus sedentary muscle.

Table 2 Top genes (shown as an image in the PDF).

## Acknowledgements

We thank the animal facility.

## Data Availability Statement

Raw counts are in GEO (GSE209999).

## References

1. Smith J. GSE99999 cited only here.
"""


def test_markdown_docling_style():
    doc = ps.parse_markdown(_DOCLING_MD, source="docling", quality="pdf_markdown:docling")
    assert doc["structure_quality"] == "pdf_markdown:docling"
    secs = {s["id"]: s for s in doc["sections"]}
    # Unnumbered subsections nest under Methods; back matter stays top-level.
    assert secs["S2.1"]["title"] == "Animals" and secs["S2.1"]["class"] == "methods", secs
    assert secs["S2.2"]["class"] == "methods"
    ack = [s for s in doc["sections"] if s["title"] == "Acknowledgements"][0]
    assert ack["parent"] is None, ack
    assert secs["DA"]["class"] == "data_availability" and secs["ABS"]["class"] == "abstract"
    blocks = {b["id"]: b for b in doc["blocks"]}
    # Running header removed; the first heading is the title.
    assert doc["title"] == "Treadmill training remodels muscle"
    assert "Journal of Synthetic" not in json.dumps(doc["blocks"])
    # A paragraph split by a page break is rejoined.
    assert blocks["S2.1.p1"]["text"].endswith("The training continued for six weeks."), blocks["S2.1.p1"]
    # Caption attached to its table; an image-only table keeps its caption.
    assert blocks["TAB1"]["label"] == "Table 1" and "| Sedentary | 6 | M |" in blocks["TAB1"]["text"]
    assert blocks["TAB2"].get("image_only") and blocks["TAB2"]["section_id"] == "S3"
    assert blocks["FIG1"]["label"] == "Figure 1" and blocks["FIG1"]["section_id"] == "S3"
    assert "<!-- image -->" not in json.dumps(doc["blocks"])
    # Nothing after References; accessions indexed by block.
    assert "GSE99999" not in doc["accession_mentions"]
    assert doc["accession_mentions"]["GSE209999"] == ["DA.p1"]
    assert "[TAB1]" in ps.read_section(doc, "methods")


def test_markdown_numbered_headings_and_h1_title():
    md = ("# A study of exercise\n\n# 1 Introduction\n\nText.\n\n# 2 Methods\n\n"
          "# 2.1 Subjects\n\nTen men.\n\n# 2.1.1 Inclusion\n\nHealthy.\n\n# 3 Results\n\nMore.\n")
    doc = ps.parse_markdown(md)
    assert doc["title"] == "A study of exercise"
    ids = [(s["id"], s["class"]) for s in doc["sections"]]
    assert ids == [("S1", "introduction"), ("S2", "methods"), ("S2.1", "methods"),
                   ("S2.1.1", "methods"), ("S3", "results")], ids


def test_pdf_to_structure_backends():
    try:
        from tools import pdf_markdown as pm
    except ImportError as e:
        print(f"  SKIP pdf_markdown ({e})")
        return
    pdf = os.path.join(FIX, "synthetic_two_column.pdf")
    # pypdf is a core dependency: the heuristic route must always work.
    doc, md = pm.structure_pdf(pdf, backend="pypdf")
    assert doc["structure_quality"] == "pdf_heuristic" and md == ""
    assert "GSE209999" in doc["accession_mentions"]
    installed = [b for b in pm.available_backends() if b != "pypdf"]
    if not installed:
        print("  SKIP markdown backends (install pymupdf4llm or docling)")
        return
    for backend in installed:
        doc, md = pm.structure_pdf(pdf, backend=backend)
        assert doc["structure_quality"] == f"pdf_markdown:{backend}", doc["structure_quality"]
        cls = {s["class"] for s in doc["sections"]}
        assert {"abstract", "introduction", "methods", "results", "discussion",
                "data_availability"} <= cls, (backend, cls)
        tabs = [b for b in doc["blocks"] if b["kind"] == "table"]
        assert tabs and "Sedentary" in tabs[0]["text"] and tabs[0]["label"] == "Table 1", (backend, tabs)
        assert doc["accession_mentions"].get("GSE209999") == ["DA.p1"], (backend, doc["accession_mentions"])
        assert "Journal of Synthetic" not in json.dumps(doc["blocks"]), backend
        assert "Smith J." not in json.dumps(doc["blocks"]), backend
        with tempfile.TemporaryDirectory() as d:
            _, paths = pm.save_pdf(pdf, d, "P1", backend=backend)
            assert os.path.exists(paths["converted_md"]) and ps.load(paths["json"])["blocks"]


def test_pdf_backend_options_and_ocr_retry():
    """pymupdf4llm's layout mode keeps page headers/footers and OCRs every page with a
    picture unless told not to (3-4x slower, figure text pasted into the body). OCR
    runs only when the text layer is empty."""
    import types
    try:
        from tools import pdf_markdown as pm
    except ImportError as e:
        print(f"  SKIP pdf_markdown ({e})")
        return
    assert not pm._has_text("<!-- image -->\n\n## \n\n<!-- image -->\n")
    assert pm._has_text(_DOCLING_MD)
    calls = []

    def fake_to_markdown(path, **kw):
        calls.append(kw)
        return _DOCLING_MD if kw.get("use_ocr") else "<!-- image -->\n"

    fake = types.ModuleType("pymupdf4llm")
    fake.to_markdown = fake_to_markdown
    saved = sys.modules.get("pymupdf4llm")
    sys.modules["pymupdf4llm"] = fake
    orig_find = pm.importlib.util.find_spec
    pm.importlib.util.find_spec = lambda name: object() if name == "pymupdf4llm" else orig_find(name)
    try:
        md, used = pm.pdf_to_markdown("scanned.pdf", backend="pymupdf4llm")
    finally:
        pm.importlib.util.find_spec = orig_find
        if saved is None:
            sys.modules.pop("pymupdf4llm", None)
        else:
            sys.modules["pymupdf4llm"] = saved
    assert used == "pymupdf4llm" and md == _DOCLING_MD
    assert [c["use_ocr"] for c in calls] == [False, True], calls
    assert all(c["header"] is False and c["footer"] is False for c in calls), calls


def test_save_load_and_tool_wrapper():
    doc = _load("PMC12989000")
    with tempfile.TemporaryDirectory() as d:
        paths = ps.save(doc, d, "PMC12989000", raw_xml=b"<article/>")
        assert all(os.path.exists(p) for p in paths.values())
        md = open(paths["md"], encoding="utf-8").read()
        assert "[DA.p1]" in md and "`S2.4` · methods" in md
        # load() accepts the .txt sibling path that fetch_paper_text reports.
        assert ps.load(os.path.join(d, "PMC12989000.txt"))["pmcid"] == "PMC12989000"
        try:
            from tools.paper_tools import read_paper_section
        except ImportError as e:  # pandas/requests missing in a minimal env
            print(f"  SKIP tool wrapper ({e})")
            return
        out = read_paper_section.invoke({"paper": paths["json"],
                                         "section": "data_availability,S2.4",
                                         "block_ids": "S2.2.p1", "find": "GraphPad"})
        assert "GSE309619" in out and "[S2.4.p1]" in out and "GraphPad" in out, out
        assert "Accessions:" in read_paper_section.invoke({"paper": paths["json"]})


def test_fetch_paper_text_writes_structure_offline():
    try:
        import tools.paper_tools as pt
    except ImportError as e:
        print(f"  SKIP fetch integration ({e})")
        return
    raw = open(os.path.join(FIX, "PMC12989000.xml"), "rb").read()
    orig = pt._fetch_europepmc_xml
    pt._fetch_europepmc_xml = lambda pmcid: (raw, "fixture://PMC12989000")
    saved_rows = list(pt._LAST_SEARCH_ROWS)
    pt._LAST_SEARCH_ROWS.clear()
    try:
        with tempfile.TemporaryDirectory() as d:
            rep = pt.fetch_paper_text.invoke({"pmcid": "PMC12989000", "output_dir": d})
            assert "Structured full text:" in rep and "GSE309619 → " in rep, rep
            txt = open(os.path.join(d, "PMC12989000.txt"), encoding="utf-8").read()
            assert txt == pt._flatten_jats(raw)  # the historical .txt is unchanged
            assert os.path.exists(os.path.join(d, "PMC12989000.paper.json"))
            assert os.path.exists(os.path.join(d, "PMC12989000.jats.xml"))
    finally:
        pt._fetch_europepmc_xml = orig
        pt._LAST_SEARCH_ROWS[:] = saved_rows


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {str(e)[:500]}")
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
