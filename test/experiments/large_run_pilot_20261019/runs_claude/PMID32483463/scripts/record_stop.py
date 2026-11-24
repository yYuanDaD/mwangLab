"""Record GSE128651 / PMID 32483463: paper_reconstruction valid, ownership manual_review
(the only deposited matrix, GSE128651_gene_fpkm.txt.gz, cannot be downloaded from this host).
The case-spec runner cannot record this stop because it hashes inputs.matrix before any gate
(tools/case_runner.py:529-530), so the gates are recorded with the native recorder."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
from tools import native

native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
REPO = next(p for p in RUN.parents if (p / "tools" / "native.py").exists())
PAPER_MD = REPO / "test/experiments/paper_screen_20261027/papers/PMC7255041.paper.md"
PAPER_JSON = REPO / "test/experiments/paper_screen_20261027/papers/PMC7255041.paper.json"

run = native.RunRecorder(
    RUN, request="Analyze GSE128651 for PMID 32483463 (Exercise protects proliferative muscle satellite cells "
                 "against exhaustion via the Igfbp7-Akt-mTOR axis.): how exercise affects gene expression as the paper intends.",
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) session", case_ids=["GSE128651"])
case = run.case("GSE128651", accession="GSE128651")
paper = case.add_input(PAPER_MD, "paper")
paper_j = case.add_input(PAPER_JSON, "paper")
series = case.add_input(RUN / "evidence_geo/GSE128651_series.soft.txt", "metadata", label="GEO series record (acc.cgi text)")
samples = case.add_input(RUN / "evidence_geo/GSE128651_samples.soft.txt", "metadata", label="GEO sample records (acc.cgi text)")
attempts = case.add_input(RUN / "evidence_geo/download_attempts.txt", "user", label="download attempts log")

recon = {
    "accessions": ["GSE128651"],
    "assay": "bulk RNA-seq (QIAseq FX Single Cell RNA Library Kit, ~800 FACS-sorted SCs/sample), Illumina HiSeq 2000 (S4.p10)",
    "sample_inclusion": "FACS-sorted Lin- CD34+ a7-integrin+ muscle satellite cells, n=4 mice per arm (FIG3 legend B)",
    "factors": {"grp": ["Con (sedentary/untrained)", "Exe (4-week treadmill training)"]},
    "primary_estimand": "effect of 4-week treadmill training on the SC transcriptome: Exe vs Con (S2.3.p1, FIG3)",
    "planned_contrasts": ["grp_Exe_vs_Con (S2.3.p1; paper: 573 up + 1,326 down = 1,899 DEGs, >2-fold, p<0.01)"],
    "repeated_measure_unit": None,
    "paper_method": "bowtie -> HTSeq counts -> DESeq2; Cufflinks FPKM for display (S4.p10)",
    "paper_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange",
                        "effect_cutoff": 1.0, "inclusive": False, "source_locator": "S2.3.p1; FIG3 legend B"},
    "paper_threshold_alternative": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None, "source_locator": "S4.p10"},
    "paper_results": {"up": 573, "down": 1326, "total": 1899,
                      "named_genes": {"down": ["Igfbp4", "Igfbp5", "Igfbp6"], "up": ["Igfbp7"]},
                      "gsea": "up: ECM receptor interaction, cardiac muscle contraction, S phase; "
                              "down: OXPHOS, ATP synthesis, PI3K-Akt, mTOR, TCA cycle (FIG3 C-K)"},
}
case.write_json("paper_reconstruction.json", recon)
case.write_json("paper_data_discrepancies.json", [
    {"item": "DEG threshold", "paper": "S2.3.p1/FIG3B: >2-fold and p<0.01 (1,899 DEGs)",
     "data": "S4.p10 methods: P<0.05 FDR-adjusted", "disposition": "results rule taken as paper_threshold (it produced the reported counts); FDR rule kept as audit"},
    {"item": "deposited matrix", "paper": "DESeq2 on HTSeq read counts (S4.p10)",
     "data": "GEO deposits only GSE128651_gene_fpkm.txt.gz (Series_supplementary_file); data_processing says RPKM via Cufflinks",
     "disposition": "paper DESeq2 route would be blocked even with the file (no counts); FPKM->log2->limma would be a declared deviation"},
    {"item": "matrix availability", "paper": "-", "data": "NCBI GEO FTP/HTTPS returns 403 for every ftp.ncbi.nlm.nih.gov path from this host",
     "disposition": "case stopped: manual_review at ownership"},
])
case.decide("paper_reconstruction", final=recon, evidence=[paper, paper_j, series],
            reasoning="Paper names GSE128651 (S4.p22) as the SC RNA-seq of control vs exercise mice (S2.3.p1, FIG3A). "
                      "Two arms, 4 mice each; GEO record confirms Con1-4 / Exe1-4. The DEG rule that yields the reported "
                      "573/1,326 is 'over 2-fold change, p<0.01' (S2.3.p1, FIG3B); methods state FDR<0.05 (S4.p10). "
                      "Whether 'p' is raw or adjusted is not stated; taken as raw p as written.",
            confidence="medium", paper={"locator": "S2.3.p1; FIG3; S4.p10; S4.p22"})

case.decide("ownership",
            final={"owned": None, "accession": "GSE128651",
                   "expected_matrix_file": "GSE128651_gene_fpkm.txt.gz (GEO Series_supplementary_file; RPKM/FPKM per data_processing)",
                   "matrix_file": None, "metadata_file": "evidence_geo/GSE128651_samples.soft.txt",
                   "checks": {"pubmed_id_on_series": "32483463 (matches)", "samples": "8 GSM (GSM3681653-60): Con1-4 untrained, Exe1-4 trained",
                              "matrix_retrieved": False,
                              "download_status": "HTTP 403 Forbidden from ftp.ncbi.nlm.nih.gov (https and GEOparse), FTP 550; "
                                                 "geo/download redirects to the same FTP host"}},
            evidence=[series, samples, attempts, paper],
            reasoning="GEO series GSE128651 carries PubMed 32483463 and 8 samples matching the paper's n=4 vs n=4 design, so "
                      "the series belongs to the paper. But the only expression file (GSE128651_gene_fpkm.txt.gz) could not be "
                      "retrieved: every ftp.ncbi.nlm.nih.gov request from this host returns 403 (also for unrelated series), and "
                      "the metadata SOFT download via GEOparse fails the same way. Without the matrix, ownership of the file "
                      "(its columns vs the 8 GSMs) and every later gate cannot be checked. A specific fact unblocks it: the "
                      "deposited FPKM file. Note for resumption: the deposit is FPKM only, so the paper's DESeq2-on-counts route "
                      "is blocked; the expected route is log2(FPKM+1) + limma (declared deviation) or SRA SRP189039 re-quantification.",
            confidence="high", decision_status="manual_review",
            stop_reason="matrix file GSE128651_gene_fpkm.txt.gz unavailable: NCBI GEO FTP returns HTTP 403 from this host; "
                        "rerun when the file is placed in data/GSE128651/")
print(case.finish())
print(run.finish())
