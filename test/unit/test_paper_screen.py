"""Paper screening (tools/paper_screen.py) — offline, NO LLM, NO network.

HTTP is replaced by canned responses, so each layer (own vs cited accessions, GEO data
type, supplementary files, sample design, verdict) is checked on its own and end to end.

Run:  python test/unit/test_paper_screen.py
"""

import gzip
import json
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools import paper_screen as sc
from tools import paper_structure as ps


class FakeHttp(sc.Http):
    def __init__(self, routes):
        super().__init__()
        self.routes = routes
        self.calls = []

    def get(self, url, params=None, binary=False, timeout=60):
        self.calls.append((url, params))
        for key, val in self.routes.items():
            if key in url or (params and key == params.get("term")):
                if callable(val):
                    val = val(params)
                if val is None:
                    return None
                if binary:
                    return val if isinstance(val, bytes) else val.encode()
                return val.decode() if isinstance(val, bytes) else val
        return None


def _doc(md: str) -> dict:
    return ps.parse_markdown(md)


PAPER_MD = """# Training and muscle

## Introduction

Earlier work used GSE11111 and found little.

## Methods

Mice were trained for six weeks.

## Discussion

Unlike GSE22222, we saw more genes.

## Data availability

RNA-seq data were deposited in GEO under GSE123456.
"""


def _geo_routes(gse="GSE123456", gdstype="Expression profiling by high throughput sequencing",
                suppl=("GSE123456_raw_counts.txt.gz", "filelist.txt"), groups=(4, 4), title="Bulk muscle"):
    esearch = json.dumps({"esearchresult": {"idlist": ["200123456"]}})
    esummary = json.dumps({"result": {"200123456": {
        "title": title, "summary": "", "gdstype": gdstype, "taxon": "Mus musculus",
        "n_samples": sum(groups), "gpl": "24247", "suppfile": "TXT",
        "samples": [{"accession": f"GSM{i}", "title": f"s{i}"} for i in range(sum(groups))]}}})
    suppl_html = "".join(f'<a href="{n}">{n}</a>' for n in suppl)
    n = sum(groups)
    labels = ["sedentary"] * groups[0] + ["trained"] * groups[1]
    header = ("!Series_title\t\"x\"\n"
              "!Sample_title\t" + "\t".join(f'"m{i}"' for i in range(n)) + "\n"
              "!Sample_geo_accession\t" + "\t".join(f'"GSM{i}"' for i in range(n)) + "\n"
              "!Sample_characteristics_ch1\t" + "\t".join('"tissue: muscle"' for _ in range(n)) + "\n"
              "!Sample_characteristics_ch1\t" + "\t".join(f'"group: {g}"' for g in labels) + "\n"
              "!Sample_characteristics_ch1\t" + "\t".join('"Sex: male"' for _ in range(n)) + "\n"
              "!series_matrix_table_begin\nID_REF\tGSM0\n")
    stub = sc.geo_stub(gse)
    return {
        "esearch.fcgi": esearch,
        "esummary.fcgi": esummary,
        f"{stub}/{gse}/suppl/": suppl_html,
        f"{stub}/{gse}/matrix/{gse}_series_matrix.txt.gz": gzip.compress(header.encode()),
        f"{stub}/{gse}/matrix/": f'<a href="{gse}_series_matrix.txt.gz">x</a>',
    }


def test_own_vs_cited_by_section():
    dep = sc.deposits_from_doc(_doc(PAPER_MD))
    assert dep["own"] == {"geo": ["GSE123456"]}, dep
    assert sorted(dep["cited"]) == ["GSE11111", "GSE22222"], dep
    # Results mention with a reuse phrase is a citation.
    doc = _doc("## Results\n\nWe re-analyzed data downloaded from GSE33333 to compare.\n")
    assert sc.deposits_from_doc(doc)["cited"] == ["GSE33333"]


def test_other_repositories_and_on_request():
    doc = _doc("## Data availability\n\nProteomics data are in PRIDE (PXD012345).\n")
    s = sc.screen_paper({"paper_id": "p"}, doc, FakeHttp({}))
    assert (s.verdict, s.reason) == ("excluded", "non_geo_repository:pride"), s
    doc = _doc("## Data availability\n\nData are available from the corresponding author upon reasonable request.\n")
    s = sc.screen_paper({"paper_id": "p"}, doc, FakeHttp({}))
    assert s.reason == "data_on_request", s
    assert sc.screen_paper({"paper_id": "p"}, None, None).reason == "no_full_text"


def test_gdstype_and_single_cell():
    assert sc.classify_gdstype("Expression profiling by array") == "microarray"
    assert sc.classify_gdstype("Expression profiling by high throughput sequencing",
                               "single-cell RNA-seq of muscle") == "scrnaseq"
    assert sc.classify_gdstype("Expression profiling by high throughput sequencing; "
                               "Genome binding/occupancy profiling by high throughput sequencing") == "rnaseq+chromatin"
    assert sc.geo_stub("GSE123456") == "GSE123nnn" and sc.geo_stub("GSE12") == "GSEnnn"


def test_supplementary_classification():
    c = sc.classify_supplementary
    assert c(["GSE1_featureCounts.txt.gz"])["status"] == "raw_counts"
    assert c(["GSE1_gene_counts.csv.gz", "GSE1_FPKM.xlsx"])["status"] == "raw_counts"
    assert c(["GSE1_normalized_counts.txt.gz"])["status"] == "normalized_only"
    assert c(["GSE1_TPM.tsv.gz"])["status"] == "normalized_only"
    assert c(["GSE1_RAW.tar", "filelist.txt"])["status"] == "raw_tar"
    assert c(["filelist.txt"])["status"] == "none"
    assert c(["GSE1_processed_data.txt.gz"])["status"] == "unlabelled_matrix"


def test_end_to_end_analyzable():
    s = sc.screen_paper({"paper_id": "p", "title": "t"}, _doc(PAPER_MD), FakeHttp(_geo_routes()))
    assert (s.verdict, s.analyzable_gse) == ("analyzable", ["GSE123456"]), s.series
    d = s.series[0]["design"]
    assert d["groups"] == {"sedentary": 4, "trained": 4} and d["sex_column"].endswith("Sex"), d
    assert s.data_types == "rnaseq"
    row = s.row()
    assert row["cited_gse"] == "GSE11111;GSE22222" and "GSE123456" in row["evidence_json"]


def test_end_to_end_exclusions():
    cases = [
        (_geo_routes(gdstype="Expression profiling by array"), "unsupported_data_type:microarray"),
        (_geo_routes(title="Single-cell RNA-seq atlas"), "unsupported_data_type:scrnaseq"),
        (_geo_routes(suppl=("GSE123456_TPM.txt.gz",)), "normalized_only"),
        (_geo_routes(suppl=("filelist.txt",)), "no_processed_matrix"),
        (_geo_routes(groups=(2, 2)), "group_too_small"),
    ]
    for routes, reason in cases:
        s = sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD), FakeHttp(routes))
        assert (s.verdict, s.reason) == ("excluded", reason), (reason, s.verdict, s.reason)
    routes = _geo_routes()
    routes["esearch.fcgi"] = json.dumps({"esearchresult": {"idlist": []}})
    assert sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD), FakeHttp(routes)).reason == "geo_not_public"
    s = sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD), FakeHttp(_geo_routes(suppl=("GSE123456_RAW.tar",))))
    assert (s.verdict, s.reason) == ("needs_inspection", "matrix_raw_tar"), s
    # Routing other data types in is a parameter, not a code change.
    s = sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD),
                        FakeHttp(_geo_routes(gdstype="Expression profiling by array")),
                        check_files=False, routes={"rnaseq", "microarray"})
    assert s.verdict == "analyzable", s.series


def test_screen_file_and_summary():
    with tempfile.TemporaryDirectory() as d:
        papers = os.path.join(d, "papers.csv")
        with open(papers, "w", encoding="utf-8") as f:
            f.write("paper_id,title,pmcid,doi,pdf_url\nA,Good paper,,,\nB,No text,,,\n")
        os.makedirs(os.path.join(d, "out", "papers"))
        ps.save(_doc(PAPER_MD), os.path.join(d, "out", "papers"), "A")
        orig = sc.Http
        sc.Http = lambda cache_dir="": FakeHttp(_geo_routes())
        try:
            out = sc.screen_file(papers, os.path.join(d, "out"))
        finally:
            sc.Http = orig
        rows = list(__import__("csv").DictReader(open(out, encoding="utf-8")))
        assert [r["verdict"] for r in rows] == ["analyzable", "excluded"], rows
        summary = open(os.path.join(d, "out", "screen_summary.md"), encoding="utf-8").read()
        assert "| analyzable | 1 |" in summary and "| no_full_text | 1 |" in summary, summary


def test_collect_dedupes_sources():
    s2 = json.dumps({"data": [{"paperId": "S1", "title": "Exercise muscle", "year": 2024,
                               "externalIds": {"DOI": "10.1/ABC", "PubMed": "111", "PubMedCentral": "999"},
                               "openAccessPdf": {"url": "http://x/1.pdf"}}]})
    pub_search = json.dumps({"esearchresult": {"idlist": ["111", "222"]}})
    pub_sum = json.dumps({"result": {"uids": ["111", "222"],
                                     "111": {"title": "Exercise muscle", "pubdate": "2024",
                                             "articleids": [{"idtype": "doi", "value": "10.1/abc"}]},
                                     "222": {"title": "Another", "pubdate": "2023",
                                             "articleids": [{"idtype": "pmc", "value": "PMC5"}]}}})
    calls = {"n": 0}

    def s2_page(params):
        calls["n"] += 1
        return s2 if calls["n"] == 1 else json.dumps({"data": []})

    http = FakeHttp({"semanticscholar": s2_page, "esearch.fcgi": pub_search, "esummary.fcgi": pub_sum})
    rows = sc.collect_papers("exercise", http, max_papers=5)
    assert [r["paper_id"] for r in rows] == ["S1", "PMID222"], rows
    assert rows[0]["pmcid"] == "PMC999" and rows[1]["pmcid"] == "PMC5"


def test_collect_caps_at_max_and_mixes_sources():
    # --max is the total, not per source; both sources are represented; a PubMed row kept
    # first still gets the Semantic Scholar PDF URL of its duplicate.
    s2 = json.dumps({"data": [{"paperId": f"S{i}", "title": f"Paper {i}", "year": 2024,
                               "externalIds": {"PubMed": str(100 + i)},
                               "openAccessPdf": {"url": f"http://x/{i}.pdf"}} for i in range(4)]})
    pub_search = json.dumps({"esearchresult": {"idlist": ["101", "200", "201", "202"]}})
    pub_sum = json.dumps({"result": {"uids": ["101", "200", "201", "202"], **{
        u: {"title": f"Paper {u}", "pubdate": "2023", "articleids": []} for u in ("101", "200", "201", "202")}}})
    http = FakeHttp({"semanticscholar": s2, "esearch.fcgi": pub_search, "esummary.fcgi": pub_sum})
    rows = sc.collect_papers("exercise", http, max_papers=4)
    assert [r["paper_id"] for r in rows] == ["S0", "PMID101", "PMID200", "S2"], [r["paper_id"] for r in rows]
    assert rows[1]["pdf_url"] == "http://x/1.pdf", rows[1]


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
