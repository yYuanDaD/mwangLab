import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
RD = "test/experiments/model_compare_20261103/runs/sonnet/b06f79d81bb9463e3b902b4b8b96b865e96758a2"
DATA = "E:/agent/mwangLab_pdf/data/GSE164890"
PAPER = "E:/agent/mwangLab_pdf/test/experiments/paper_screen_20261019/papers/PMC9027771.paper.md"
native.enable_native_mode()
run = native.RunRecorder(RD, request="Analyze GSE164890 for PMC9027771: how exercise affects gene expression as the paper intends",
        platform_name="claude-code", decision_maker="Claude Sonnet 5.5 (claude-sonnet-5-5)", case_ids=["GSE164890"])
case = run.case("GSE164890", accession="GSE164890")
paper = case.add_input(PAPER, "paper")
meta = case.add_input(f"{DATA}/GSE164890_metadata.csv", "metadata")
mat = case.add_input(f"{DATA}/GSE164890_rsem.genes.counts.tsv.gz", "matrix")
thr = {"metric": "FDR", "adjustment": "BH (DESeq2 padj)", "cutoff": 0.1, "effect_metric": "log2FC", "effect_cutoff": None,
       "inclusive": False, "source_locator": "S2.5.p1"}
case.decide("paper_reconstruction", final={
    "accessions": ["GSE164890"], "assay": "whole-blood globin-depleted polyA RNA-seq, STAR+RSEM gene counts (GRCh38/GENCODE v26)",
    "samples": "7 elite female speed skaters x (before, after) one ~1h strenuous skating bout on day 18 of altitude camp (1850 m); 14 samples",
    "factors": {"donor": 7, "exercise": ["before", "after"]},
    "primary_estimand": "within-person change in whole-blood gene expression after an intense exercise bout at altitude (after vs before)",
    "planned_contrasts": ["after_vs_before"],
    "repeated_measure_unit": "donor (skater)",
    "design": "DESeq2 ~ donor + exercise", "method": "DESeq2 v1.18.1 on RSEM per-gene raw counts; rlog + ComBat donor correction only for PCA/heatmaps",
    "normalization": "DESeq2 size factors; rlog for diagnostics",
    "paper_threshold": thr,
    "paper_reported_deg": {"up": 2516, "down": 1542, "total": 4058, "locator": "S3.2.p2"},
    "enrichment": "ORA (clusterProfiler) and fGSEA on MSigDB H and CP",
    "out_of_scope": "microarray reanalyses of 8 public datasets / scRNA deconvolution (S2.6, S2.7) are not part of GSE164890"},
  evidence=[paper], paper={"locator": "S2.5.p1"}, confidence="high",
  reasoning="Paper S2.5.p1/FIG1 state DESeq2 'donor + exercise' at 10% FDR; S3.2.p2 reports 2516 up / 1542 down. Pairing by donor stated in S2.3.p1.")
