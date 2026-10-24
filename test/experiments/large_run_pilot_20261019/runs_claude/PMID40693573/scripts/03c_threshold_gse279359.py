"""Gates 1-8 (paper_reconstruction .. threshold) for case GSE279359 (mouse long-read, PMID40693573)."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40693573"
CASE = "GSE279359"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12248044.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12248044.paper.md"
MATRIX = "data/GSE279359/GSE279359_processed_counts.txt.gz"
META = "data/GSE279359/GSE279359_metadata.csv"
run = native.RunRecorder.open(RUN); case = run.case(CASE); paper = case.evidence_item("paper:PMC12248044.paper.json")
paper_threshold = {"metric": "padj", "adjustment": "not_reported (executor applies BH)", "cutoff": 0.05, "inclusive": False,
                   "effect_metric": "log2FC", "effect_cutoff": 1.5, "effect_inclusive": False,
                   "effect_cutoff_original": "|log2FC| > 1.5 (log2 scale)", "source_locator": "S3.1.p2",
                   "note": "S3.1.p2 first applies |log2FC| > 1.5, p-adj < .05 and then a relaxed |log2FC| > 1.0, p-adj < .05 "
                           "for figures 2F-H; the relaxed rule is kept as a labelled audit threshold"}
# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": dict(paper_threshold),
                   "deviation_note": "paper rule applied to DESeq2 instead of Swan; p-value adjustment is BH",
                   "audit_thresholds": [{"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": 1.0,
                                         "label": "audit: paper's relaxed rule (S3.1.p2)"},
                                        {"metric": "padj", "cutoff": 0.05, "effect_metric": None, "label": "audit: workflow default"}]},
            evidence=[paper], paper={"locator": "S3.1.p2"}, confidence="high",
            reasoning="S3.1.p2: |log2FC| > 1.5 and p-adj < .05; the relaxed |log2FC| > 1.0 rule is reported as an audit count.")
print("done gates 1-8 for", CASE)
