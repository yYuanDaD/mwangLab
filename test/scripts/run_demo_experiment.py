"""Live demo of this session's headline work, rate-limit-safe (analysis side only):
  #1  deterministic raw-DA picker  -> raw_da_method='auto' => rule => DESeq2 (no LLM)
  #8  multi-contrast splitting     -> GSE279359 time column (pre / +3 post timepoints)
                                      => 3 separate DESeq2, one DEG file per timepoint
Reads back summary.csv and lists the per-contrast DEG files produced.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_demo_experiment.py
"""
import os
import sys
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

import pandas as pd
from tools.batch_tools import run_batch_geo_pipeline

ACC = "GSE279359"
LABEL = "demo_all_0612"
COHORT = os.path.join("output", f"cohort_{LABEL}")

print("=" * 78)
print(f"EXPERIMENT: batch pipeline on {ACC}  (raw_da_method='all' -> 3 methods + consensus)")
print("=" * 78)

report = run_batch_geo_pipeline.invoke({
    "accessions": [ACC],
    "organism": "Mouse",
    # design column = characteristics_ch1.1.time : pre-exercise (baseline) + 3 post timepoints
    "treatment_keywords": ["post-exercise", "post", "exercise"],
    "control_keywords": ["pre-exercise", "pre"],
    "output_base": "./output",
    "run_label": LABEL,
    "raw_da_method": "all",          # <-- run DESeq2 + edgeR + limma-voom, report consensus
})

print("\n----- run_batch_geo_pipeline report -----")
print(report)

# ---- read back the machine-readable summary ----
summ = os.path.join(COHORT, "summary.csv")
print("\n----- summary.csv (key columns) -----")
if os.path.isfile(summ):
    df = pd.read_csv(summ)
    cols = [c for c in ["accession", "matrix_type", "da_method",
                        "n_contrasts", "contrasts", "n_deg", "n_deg_detail",
                        "da_methods_run", "da_per_method_deg", "da_consensus_deg",
                        "da_logfc_r", "llm_validated", "status"] if c in df.columns]
    with pd.option_context("display.max_colwidth", 90, "display.width", 200):
        print(df[cols].T)
else:
    print("  (no summary.csv)")

# ---- per-method DEG files + the comparison CSVs ('all' proof) ----
print("\n----- per-method DEG files (DEG_results_..._<method>.csv) -----")
deg = sorted(glob.glob(os.path.join(COHORT, ACC, "DEG_results_*__*.csv")))
deg = [p for p in deg if "_GSEA_" not in os.path.basename(p) and "__DA_compare" not in os.path.basename(p)]
for p in deg:
    n = max(0, sum(1 for _ in open(p, encoding="utf-8")) - 1)
    print(f"   {os.path.basename(p):66s}  {n} genes")

print("\n----- per-gene comparison tables (one per contrast) -----")
comp = sorted(glob.glob(os.path.join(COHORT, ACC, "*__DA_compare.csv")))
for p in comp:
    print(f"   {os.path.basename(p)}")
# show the head of the first comparison table (top consensus genes)
if comp:
    print(f"\n----- head of {os.path.basename(comp[0])} (top genes by method agreement) -----")
    cdf = pd.read_csv(comp[0], index_col=0)
    with pd.option_context("display.max_colwidth", 16, "display.width", 200):
        print(cdf.head(8).round(3).to_string())

print("\nDONE.")
