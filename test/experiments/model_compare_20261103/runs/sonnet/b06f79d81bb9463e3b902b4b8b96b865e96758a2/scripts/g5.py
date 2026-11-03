import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
RD = "test/experiments/model_compare_20261103/runs/sonnet/b06f79d81bb9463e3b902b4b8b96b865e96758a2"
native.enable_native_mode()
run = native.RunRecorder.open(RD); case = run.case("GSE164890")
meta = case.evidence_item("metadata:GSE164890_metadata.csv"); mat = case.evidence_item("matrix:GSE164890_rsem.genes.counts.tsv.gz")
paper = case.evidence_item("paper:PMC9027771.paper.md")
case.decide("method", final={"method": "DESeq2 (pydeseq2 executor; paper used R DESeq2 v1.18.1)", "matrix_type": "estimated counts", "formula": "~ subject + ex",
    "contrast": "ex: after vs before", "transform": "round(RSEM expected counts) to integers", "rounding_documented": True,
    "rounding_recipe": "numpy.rint on aligned_matrix.csv, written to results/counts_rounded.csv",
    "deviations": ["python pydeseq2 instead of R DESeq2 1.18.1: numerical differences in dispersion fitting/independent filtering expected",
                   "RSEM expected counts rounded to integers (paper's exact rounding unknown)",
                   "genes with zero counts in all samples dropped by the executor"]},
  candidates=[{"value": "limma-voom / edgeR", "reason_rejected": "paper used DESeq2; same data type; no reason to deviate"},
              {"value": "ComBat-corrected matrix then DE", "reason_rejected": "paper used ComBat only for diagnostic plots; DE model has donor term"}],
  evidence=[paper, mat], paper={"locator": "S2.5.p1"}, confidence="high",
  reasoning="Reproduce paper DESeq2 'donor + exercise'. Paper route is runnable; the only departures are the python implementation and integer rounding.")
thr = {"metric": "FDR", "adjustment": "BH (DESeq2 padj)", "cutoff": 0.1, "effect_metric": "log2FC", "effect_cutoff": None, "inclusive": False, "source_locator": "S2.5.p1"}
case.decide("threshold", final={"paper_threshold": thr, "threshold_source": "paper", "applied_threshold": dict(thr),
    "audit_thresholds": ["padj<0.1 & |log2FC|>1 (paper 'more than twofold', S3.2.p2: 104 up/58 down)", "padj<0.05 workflow default", "padj<0.1 & |log2FC|>=0.5 (S3.5.p4, plus TPM>=10; applied there only to altitude-specific DEGs)"]},
  evidence=[paper], paper={"locator": "S2.5.p1"}, confidence="high",
  reasoning="Paper retains genes with FDR < 0.1, no effect-size cutoff for the main count (2516 up/1542 down).")
