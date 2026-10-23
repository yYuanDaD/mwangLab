"""Paper screening (tools/paper_screen.py) — offline, NO LLM, NO network.

HTTP is replaced by canned responses, so each layer (own vs cited accessions, GEO data
type, supplementary files, sample design, verdict) is checked on its own and end to end.

Run:  python test/unit/test_paper_screen.py
"""

import gzip
import json
import re
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

    def get(self, url, params=None, binary=False, timeout=60, max_bytes=0):
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
                suppl=("GSE123456_raw_counts.txt.gz", "filelist.txt"), groups=(4, 4), title="Bulk muscle",
                sample_files=None, taxon="Mus musculus", pubmedids=()):
    """GEO responses for one series. ``sample_files`` maps a per-sample file name (one per
    sample, named GSM<i>_<name>) to its content, for _RAW.tar series."""
    esearch = json.dumps({"esearchresult": {"idlist": ["200123456"]}})
    esummary = json.dumps({"result": {"200123456": {
        "title": title, "summary": "", "gdstype": gdstype, "taxon": taxon, "pubmedids": list(pubmedids),
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
              "!Sample_characteristics_ch1\t" + "\t".join('"Sex: male"' for _ in range(n)) + "\n")
    files = {}
    if sample_files:
        name, content = next(iter(sample_files.items()))
        urls = [f"ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSMnnn/GSM{i}/suppl/GSM{i}_{name}" for i in range(n)]
        header += "!Sample_supplementary_file_1\t" + "\t".join(f'"{u}"' for u in urls) + "\n"
        files = {f"GSM{i}_{name}": gzip.compress(content.encode()) for i in range(n)}
    header += "!series_matrix_table_begin\nID_REF\tGSM0\n"
    stub = sc.geo_stub(gse)
    return {
        **files,
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


def test_reuse_wording_beats_section():
    """Reuse phrasing in Methods or data availability is a citation (GSE97084 case)."""
    md = ("## Methods\n\nPublicly available RNA-seq data (GSE97084) were downloaded from GEO and "
          "re-analysed. Our own samples were sequenced on a NovaSeq.\n\n"
          "## Data availability\n\nThe data generated in this study have been deposited in GEO under "
          "GSE200001. This study also analysed publicly available datasets: GSE113165.\n")
    dep = sc.deposits_from_doc(_doc(md))
    assert dep["own"] == {"geo": ["GSE200001"]}, dep
    assert sorted(dep["cited"]) == ["GSE113165", "GSE97084"], dep
    # A neighbouring accession's phrase is not borrowed.
    md = "## Methods\n\nData were obtained from GSE1111. Sequencing data are in GSE2222.\n"
    dep = sc.deposits_from_doc(_doc(md))
    assert dep["own"] == {"geo": ["GSE2222"]} and dep["cited"] == ["GSE1111"], dep


def test_shared_series_flagged():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "screen.csv")
        import csv as _csv
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = _csv.DictWriter(f, fieldnames=sc.FIELDS)
            w.writeheader()
            for pid, own, ok in (("A", "GSE97084", "GSE97084"), ("B", "GSE97084;GSE5", "GSE97084;GSE5"),
                                 ("C", "GSE7", "GSE7")):
                w.writerow({k: "" for k in sc.FIELDS} | {"paper_id": pid, "own_gse": own,
                                                        "analyzable_gse": ok, "verdict": "analyzable"})
        sc.mark_shared_series(path)
        rows = {r["paper_id"]: r for r in _csv.DictReader(open(path, encoding="utf-8"))}
        assert rows["A"]["verdict"] == "needs_inspection" and rows["A"]["reason"] == "shared_gse:GSE97084(2 papers)"
        assert rows["B"]["verdict"] == "needs_inspection" and rows["C"]["verdict"] == "analyzable", rows


def test_blocked_pdf_is_no_full_text():
    """A 403 from a publisher is "unavailable" (None), so the paper is no_full_text."""
    import types
    http = sc.Http(cache_dir="")
    fake = types.SimpleNamespace(status_code=403, content=b"", raise_for_status=lambda: None)
    import requests
    orig = requests.get
    requests.get = lambda *a, **k: fake
    try:
        assert http.get("https://example.org/x.pdf", binary=True) is None
        doc = sc.load_full_text({"paper_id": "P", "pdf_url": "https://example.org/x.pdf"},
                                tempfile.mkdtemp(), http)
    finally:
        requests.get = orig
    assert doc is None
    assert sc.screen_paper({"paper_id": "P"}, doc, None).reason == "no_full_text"


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
    # GSE71972: "Counts" between underscores, next to a _RAW.tar and DE tables.
    real = ["GSE71972_RAW.tar", "GSE71972_Differential_Expression_Tables.xlsx",
            "GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx"]
    assert c(real)["raw"] == ["GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx"], c(real)
    assert c(["GSE1_discounts.txt"])["status"] == "unlabelled_matrix"
    # 1000-paper run (2026-10-19): names the first rules missed.
    assert c(["GSE207992_DESeq2_normcounts.xlsx"])["status"] == "normalized_only"
    assert c(["GSE1_Cortex_EV_NormCounts.xlsx"])["status"] == "normalized_only"
    for name in ("GSE274311_SI_allcounts.txt.gz", "GSE1_CounTable.txt.gz", "GSE1_silver_hmt_raw.csv.gz",
                 "GSE1_Human_skm_total_RNA_RAW_ENSEMBL.csv.gz"):
        assert c([name])["status"] == "raw_counts", name
    de = ["GSE1_DEG_CET_Post_vs_Pre.txt.gz", "GSE1_REST--_versus_REST++_DiffExpr.txt.gz",
          "GSE1_de_summary.txt.gz", "GSE1_Gene_differential_expression.xlsx"]
    assert c(de)["status"] == "de_tables_only", c(de)
    assert c(de + ["GSE1_processed_data.txt.gz"])["status"] == "unlabelled_matrix"


def test_data_from_named_authors_is_reuse():
    """GSE214544 in PMC11624283: 'Single-cell RNA sequencing data from Lovrić et al (GSE214544)'."""
    md = ("## Methods\n\nSingle-cell RNA sequencing data from Lovrić et al (GSE214544) were used for the "
          "reference matrix. Raw and processed files have been deposited in the GEO database (GSE252357).\n")
    dep = sc.deposits_from_doc(_doc(md))
    assert dep["own"] == {"geo": ["GSE252357"]} and dep["cited"] == ["GSE214544"], dep


def test_reuse_phrase_covers_accession_list():
    """PMC10443797: 'Data from the Amar et al. meta-analysis ... are accessible at GSE59088 and
    GSE97084' -- the phrase before the first item covers the whole list."""
    md = ("## Data availability\n\nStrength training data associated with this study have been deposited in "
          "Gene Expression Omnibus at GSE208639. Data from the Amar et al. (26) long-term exercise "
          "meta-analysis used to compare previously published exercise genes are accessible at GSE59088 "
          "and GSE97084.\n\n## Methods\n\nWe compiled human skeletal muscle RNA-seq data (GSE129643).\n")
    dep = sc.deposits_from_doc(_doc(md))
    assert dep["own"] == {"geo": ["GSE208639"]}, dep
    assert sorted(dep["cited"]) == ["GSE129643", "GSE59088", "GSE97084"], dep
    # PMC12355375: a reference marker right before the accession credits another paper.
    md = "## Results\n\nUsing RNA-seq data from the GESTALT cohort^6 (GSE129643), PSI fell with age.\n"
    assert sc.deposits_from_doc(_doc(md))["cited"] == ["GSE129643"]
    # PMC7185955: series pooled in a meta-analysis are reused.
    md = ("## Methods\n\nWe performed a meta-analysis including 3 studies of a single bout of exercise "
          "(q < 0.05, GSE43219, GSE71972 and GSE28422) (37).\n")
    assert sorted(sc.deposits_from_doc(_doc(md))["cited"]) == ["GSE28422", "GSE43219", "GSE71972"]
    # PMC9259242: a re-analysis that also says "available upon request" reuses public data.
    md = ("## Methods\n\nWe downloaded the GSE101931 dataset from GEO.\n\n## Data availability\n\n"
          "The datasets analysed are available from the corresponding author upon request.\n")
    s = sc.screen_paper({"paper_id": "p"}, _doc(md), FakeHttp({}))
    assert (s.verdict, s.reason) == ("excluded", "no_own_deposit:reuses_public_gse"), s


def test_meta_analysis_series_are_reuse():
    """MetaMEx (PMC6981202) and the AD portrait (PMC9561721) list dozens of series with no
    deposit wording; none is the paper's own."""
    rows = "\n".join(f"| GSE{100000 + i} | Exercise | {i} |" for i in range(12))
    md = ("## Methods\n\nRepositories were screened for human exercise studies.\n\n"
          "## Results\n\nTable 1. Datasets.\n\n| GEO | Treatment | Score |\n|---|---|---|\n" + rows + "\n")
    dep = sc.deposits_from_doc(_doc(md))
    assert "geo" not in dep["own"] and len(dep["cited"]) == 12, dep
    md += "\n## Data availability\n\nOur RNA-seq data have been deposited in GEO under GSE999999.\n"
    dep = sc.deposits_from_doc(_doc(md))
    assert dep["own"] == {"geo": ["GSE999999"]}, dep


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


HTSEQ = "".join(f"ENSMUSG{i:011d}\t{(i * 7) % 300}\n" for i in range(200)) + "__no_feature\t1234\n"
FEATURECOUNTS = ("# Program:featureCounts v2.0.1\nGeneid\tChr\tStart\tEnd\tStrand\tLength\tsample.bam\n"
                 + "".join(f"G{i}\tchr1;chr1\t1;50\t40;90\t+;+\t{900 + i}\t{i % 17}\n" for i in range(200)))
RSEM = ("gene_id\ttranscript_id(s)\tlength\teffective_length\texpected_count\tTPM\tFPKM\n"
        + "".join(f"G{i}\tT{i}\t1000.00\t850.5\t{i * 1.37:.2f}\t{i * 0.11:.2f}\t{i * 0.07:.2f}\n" for i in range(200)))
FPKM = "gene\tFPKM\n" + "".join(f"G{i}\t{i * 0.731:.3f}\n" for i in range(200))
UNLABELLED_FLOATS = "".join(f"G{i}\t{i * 0.731 + 0.1:.3f}\n" for i in range(200))


def test_citation_after_accession_is_reuse():
    md = ("## Data availability\n\nRNA sequencing data have been deposited in GEO under accession "
          "GSE294565 (Nolt et al. 2024). New data from this study are deposited under GSE300001.\n")
    dep = sc.deposits_from_doc(_doc(md))
    assert dep["own"] == {"geo": ["GSE300001"]} and dep["cited"] == ["GSE294565"], dep
    # A plain parenthetical is not a citation.
    dep = sc.deposits_from_doc(_doc("## Data availability\n\nData were deposited in GEO (GSE300002).\n"))
    assert dep["own"] == {"geo": ["GSE300002"]}, dep


def test_topic_and_organism_filters():
    topic = re.compile(sc.DEFAULT_TOPIC, re.I)
    off = _doc("# Drug resistance in Trichomonas vaginalis\n\n## Abstract\n\nMetronidazole resistance.\n\n"
               + PAPER_MD.split("\n", 1)[1])
    s = sc.screen_paper({"paper_id": "p", "title": "Drug resistance in Trichomonas vaginalis"}, off,
                        FakeHttp(_geo_routes()), topic=topic)
    assert (s.verdict, s.reason) == ("excluded", "off_topic"), (s.verdict, s.reason)
    s = sc.screen_paper({"paper_id": "p", "title": "Training and muscle"}, _doc(PAPER_MD),
                        FakeHttp(_geo_routes()), topic=topic, organisms=sc.DEFAULT_ORGANISMS)
    assert s.verdict == "analyzable", (s.verdict, s.reason)
    s = sc.screen_paper({"paper_id": "p", "title": "Training and muscle"}, _doc(PAPER_MD),
                        FakeHttp(_geo_routes(taxon="Escherichia coli")), organisms=sc.DEFAULT_ORGANISMS)
    assert (s.verdict, s.reason) == ("excluded", "unsupported_organism:Escherichia coli"), (s.verdict, s.reason)
    # Filters are off unless asked for (library default), and a mixed-species series passes.
    assert sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD),
                           FakeHttp(_geo_routes(taxon="Escherichia coli"))).verdict == "analyzable"
    assert sc.organism_ok("Homo sapiens; Escherichia coli", sc.DEFAULT_ORGANISMS)
    # GEO labels some laboratory rats Rattus rattus; the genus decides.
    assert sc.organism_ok("Rattus rattus", sc.DEFAULT_ORGANISMS)
    # "training" in the machine-learning sense is not the topic.
    assert not topic.search("Radiomics of melanoma: a training cohort and a validation set")
    for t in ("Endurance training remodels muscle", "Trained mice ran more", "Resistance-training intervention",
              "Effects of exercise on liver"):
        assert topic.search(t), t


def test_series_linked_to_other_paper_is_reuse():
    # Listed in Methods with no deposit wording, and GEO links it to another paper only.
    md = "# Exercise\n\n## Methods\n\nCohorts: GSE123456 and our clinical data.\n"
    s = sc.screen_paper({"paper_id": "p", "pmid": "999"}, _doc(md), FakeHttp(_geo_routes(pubmedids=["111"])))
    assert (s.verdict, s.reason) == ("excluded", "no_own_deposit:linked_to_other_paper"), (s.verdict, s.reason)
    # Linked to this paper's preprint or journal version (same title, another PMID): own.
    routes = _geo_routes(pubmedids=["111"])
    gds_summary = routes["esummary.fcgi"]
    pubmed = json.dumps({"result": {"uids": ["111"], "111": {"title": "Exercise.", "pubdate": "2024",
                                                             "articleids": []}}})
    routes["esummary.fcgi"] = lambda params: pubmed if params["db"] == "pubmed" else gds_summary
    s = sc.screen_paper({"paper_id": "p", "pmid": "999", "title": "Exercise"}, _doc(md), FakeHttp(routes))
    assert s.verdict == "analyzable", (s.verdict, s.reason)
    # Linked to this paper, not linked yet, or with deposit wording: own.
    for pubmedids, doc in ((["999", "111"], _doc(md)), ([], _doc(md)), (["111"], _doc(PAPER_MD))):
        s = sc.screen_paper({"paper_id": "p", "pmid": "999"}, doc, FakeHttp(_geo_routes(pubmedids=pubmedids)))
        assert s.verdict == "analyzable", (pubmedids, s.verdict, s.reason)


def test_sniff_count_file():
    assert sc.sniff_count_file(HTSEQ) == "raw_counts"
    assert sc.sniff_count_file(FEATURECOUNTS) == "raw_counts"
    assert sc.sniff_count_file(RSEM) == "raw_counts"      # expected_count, not the FPKM column
    assert sc.sniff_count_file(FPKM) == "normalized"
    assert sc.sniff_count_file(UNLABELLED_FLOATS) == "normalized"
    assert sc.sniff_count_file("G1\t3\nG2\t4\n") == "unknown"   # too few rows to judge


def test_raw_tar_judged_from_sample_files():
    tar = ("GSE123456_RAW.tar", "filelist.txt")
    s = sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD),
                        FakeHttp(_geo_routes(suppl=tar, sample_files={"counts.txt.gz": HTSEQ})))
    assert (s.verdict, s.analyzable_gse) == ("analyzable", ["GSE123456"]), s.series
    f = s.series[0]["files"]
    assert f["status"] == "raw_counts_in_tar" and f["tar_inspection"]["n_tables"] == 8, f
    assert "sample_files" not in s.series[0]["design"]
    s = sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD),
                        FakeHttp(_geo_routes(suppl=tar, sample_files={"genes.txt.gz": FPKM})))
    assert (s.verdict, s.reason) == ("excluded", "normalized_only"), (s.verdict, s.reason)
    s = sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD),
                        FakeHttp(_geo_routes(suppl=tar, sample_files={"signal.bw": "x"})))
    assert (s.verdict, s.reason) == ("excluded", "no_processed_matrix"), (s.verdict, s.reason)
    # A file that cannot be fetched leaves the series for a person to look at.
    routes = _geo_routes(suppl=tar, sample_files={"counts.txt.gz": HTSEQ})
    for k in [k for k in routes if k.startswith("GSM")]:
        routes[k] = None
    s = sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD), FakeHttp(routes))
    assert (s.verdict, s.reason) == ("needs_inspection", "matrix_raw_tar"), (s.verdict, s.reason)


def _matrix(fmt, n=60):
    rows = ["gene\ts1\ts2\ts3\ts4"]
    for i in range(n):
        rows.append(f"G{i}\t" + "\t".join(fmt(i, j) for j in range(4)))
    return "\n".join(rows) + "\n"


def test_sniff_matrix_file_and_value_check():
    counts = _matrix(lambda i, j: str(i * 7 + j))
    salmon = _matrix(lambda i, j: f"{i * 7 + j}.001" if j == 0 else str(i * 7 + j))
    fractional = _matrix(lambda i, j: f"{i}.5" if (i + j) % 3 == 0 else str(i))
    rpkm = _matrix(lambda i, j: f"{(i + 1) / 7:.4f}")
    assert sc.sniff_matrix_file(counts) == "raw_counts"
    assert sc.sniff_matrix_file(salmon) == "raw_counts"     # 132.001-style noise is still a count
    assert sc.sniff_matrix_file(fractional) == "mostly_integer"
    assert sc.sniff_matrix_file(rpkm) == "decimal"
    assert sc.sniff_matrix_file('gene\ts1\n"G1"\t"3"\n') == "unknown"   # quoted numbers, too few values
    files = {"raw": ["GSE1_raw_counts.txt.gz"]}

    def check(content, processing=""):
        return sc.check_raw_values("GSE1", files, FakeHttp({"GSE1_raw_counts": gzip.compress(content.encode())}),
                                   processing)["status"]
    assert check(counts) == "raw_counts"
    assert check(rpkm, "processed data are RPKM normalized read counts") == "normalized_only"
    assert check(rpkm, "quasi-mapped using Salmon; tximport") == "estimated_counts"
    assert check(rpkm) == "decimal_unexplained"
    assert check(fractional) == "estimated_counts"


def test_raw_counts_named_file_with_rpkm_values():
    """GSE273041: a file named raw_counts that holds RPKM is not a count matrix."""
    rpkm = _matrix(lambda i, j: f"{(i + 1) / 7:.4f}", n=8)
    # The file's route goes first: the suppl/ listing route is a prefix of its URL.
    routes = {"GSE123456_raw_counts.txt.gz": gzip.compress(rpkm.encode()), **_geo_routes()}
    matrix_key = next(k for k in routes if k.endswith("_series_matrix.txt.gz"))
    header = gzip.decompress(routes[matrix_key]).decode().replace(
        "!series_matrix_table_begin",
        "!Sample_data_processing\t\"alignment via TopHat\"\n"
        "!Sample_data_processing\t\"processed data are RPKM normalized read counts\"\n!series_matrix_table_begin")
    routes[matrix_key] = gzip.compress(header.encode())
    s = sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD), FakeHttp(routes))
    # 8 genes x 8 samples is below the sniff minimum: the name decides, as before.
    assert s.verdict == "analyzable", s.series
    routes["GSE123456_raw_counts.txt.gz"] = gzip.compress(_matrix(lambda i, j: f"{(i + 1) / 7:.4f}").encode())
    s = sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD), FakeHttp(routes))
    assert (s.verdict, s.reason) == ("excluded", "normalized_only"), (s.verdict, s.reason)
    assert "RPKM" in s.series[0]["files"]["value_check"]["processing"]
    assert "processing" not in s.series[0]["design"]


AGING_MD = """# Muscle transcriptome and physical function in older mice

## Abstract

We measured physical function and exercise capacity (treadmill, voluntary wheel running)
in 6, 24 and 28 month old mice and related it to muscle gene expression.

## Introduction

Exercise in its many forms preserves physical function during aging.

## Methods

Mice aged 6, 24 and 28 months were tested on a treadmill to exhaustion.

## Data availability

RNA-seq data were deposited in GEO under GSE123456.
"""


def test_exercise_contrast_required():
    contrast = re.compile(sc.DEFAULT_CONTRAST, re.I)
    s = sc.screen_paper({"paper_id": "p"}, _doc(AGING_MD), FakeHttp(_geo_routes()), contrast=contrast)
    assert (s.verdict, s.reason) == ("excluded", "no_exercise_contrast"), (s.verdict, s.reason)
    s = sc.screen_paper({"paper_id": "p"}, _doc(PAPER_MD), FakeHttp(_geo_routes()), contrast=contrast)
    assert s.verdict == "analyzable", (s.verdict, s.reason)    # "Mice were trained for six weeks."
    for text in ("Rats were randomized to sedentary or wheel running groups.",
                 "Biopsies were taken before and after a 12-week strength-training program.",
                 "Patients were grouped by physical activity tertiles.",
                 "Participants performed a single bout of cycling."):
        assert sc.contrast_evidence(_doc(f"# T\n\n## Methods\n\n{text}\n"), contrast), text
    assert sc.contrast_evidence(_doc(AGING_MD), None) == ["(not checked)"]


JATS_BODY = ("<pmc-articleset><article><front><article-meta><title-group><article-title>T</article-title>"
             "</title-group><abstract><p>Abstract.</p></abstract></article-meta></front><body>"
             + "".join(f"<sec><title>S{i}</title><p>Paragraph {i}. Data are in GSE123456.</p></sec>" for i in range(6))
             + "</body></article></pmc-articleset>")
JATS_FRONT = ("<pmc-articleset><article><front><article-meta><title-group><article-title>T</article-title>"
              "</title-group><abstract><p>Abstract.</p></abstract></article-meta></front></article></pmc-articleset>")


def test_full_text_falls_back_to_ncbi_pmc():
    with tempfile.TemporaryDirectory() as d:
        http = FakeHttp({"europepmc": None, "efetch.fcgi": JATS_BODY})
        doc = sc.load_full_text({"pmcid": "PMC42"}, d, http)
        assert doc and sc.has_body(doc) and "NCBI PMC" in doc["source"], doc and doc.get("source")
        assert http.calls[1][1]["id"] == "42", http.calls
    with tempfile.TemporaryDirectory() as d:
        # Front matter only (publisher withholds the body) is not full text.
        http = FakeHttp({"europepmc": JATS_FRONT, "efetch.fcgi": JATS_FRONT})
        assert sc.load_full_text({"pmcid": "PMC42"}, d, http) is None


def test_collect_multiple_queries_and_geo_source():
    def esearch(params):
        if params["db"] == "gds":
            assert "gse[Entry Type]" in params["term"] and "high throughput sequencing" in params["term"]
            return json.dumps({"esearchresult": {"idlist": ["200001", "200002"]}})
        ids = {"(exercise) AND free full text[sb]": ["11"], "(training) AND free full text[sb]": ["11", "22"]}
        return json.dumps({"esearchresult": {"idlist": ids[params["term"]]}})

    def esummary(params):
        if params["db"] == "gds":
            return json.dumps({"result": {"uids": ["200001", "200002"],
                                          "200001": {"accession": "GSE1", "pubmedids": ["33"]},
                                          "200002": {"accession": "GSE2", "pubmedids": []}}})
        return json.dumps({"result": {"uids": params["id"].split(","), **{
            u: {"title": f"Paper {u}", "pubdate": "2024", "articleids": []} for u in params["id"].split(",")}}})

    http = FakeHttp({"esearch.fcgi": esearch, "esummary.fcgi": esummary})
    rows = sc.collect_papers(["exercise", "training"], http, max_papers=10, sources=("pubmed", "geo"))
    assert [r["paper_id"] for r in rows] == ["PMID11", "PMID33", "PMID22"], [r["paper_id"] for r in rows]
    assert rows[1]["linked_gse"] == "GSE1" and rows[1]["source"] == "geo"
    assert [r["query"] for r in rows] == ["exercise", "exercise", "training"]


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
