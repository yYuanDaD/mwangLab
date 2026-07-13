"""Smoke test for preprocess_tools, stats_tools, and run_gsea_analysis —
run the underlying functions directly (bypassing @tool .invoke) on the
GSE266241 1hr data plus an existing DEG CSV."""

import os
import sys
import shutil

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(_PROJECT_ROOT)
sys.path.insert(0, _PROJECT_ROOT)

from tools.preprocess_tools import preprocess_counts
from tools.stats_tools import run_pca, sample_correlation_heatmap, sample_qc_summary
from tools.enrichment_tools import run_gsea_analysis

COUNTS = "data/GSE266241/GSE266241_1hr_SC_raw_data.csv"
META = "data/GSE266241/GSE266241_metadata.csv"
DEG = "output/GSE266241/DEG_results_Thoracic_and_Lumbar_Spinal_Cord_vs_Cervical_Spinal_Cord.csv"
OUT = "test/output/smoke_test"

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT, exist_ok=True)


def section(name):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)


section("1) sample_qc_summary on raw counts")
print(sample_qc_summary.invoke({"counts_csv": COUNTS, "output_dir": OUT, "metadata_csv": META}))

section("2) preprocess_counts (filter + log2 CPM)")
print(preprocess_counts.invoke({"counts_csv": COUNTS, "output_dir": OUT}))

normalized = os.path.join(OUT, "GSE266241_1hr_SC_raw_data_normalized.csv")
assert os.path.exists(normalized), f"missing {normalized}"

section("3) sample_correlation_heatmap on normalized matrix")
print(sample_correlation_heatmap.invoke({
    "expression_csv": normalized,
    "output_dir": OUT,
    "method": "pearson",
    "metadata_csv": META,
}))

section("4) run_pca on normalized matrix, colored by tissue")
print(run_pca.invoke({
    "expression_csv": normalized,
    "metadata_csv": META,
    "group_column": "characteristics_ch1.0.tissue",
    "output_dir": OUT,
}))

section("5) run_gsea_analysis on existing DEG CSV (Hallmark, Mouse)")
print(run_gsea_analysis.invoke({
    "deg_csv": DEG,
    "organism": "Mouse",
    "ranking_metric": "stat",
    "output_dir": OUT,
}))

section("Output files")
for f in sorted(os.listdir(OUT)):
    full = os.path.join(OUT, f)
    print(f"  {f}  ({os.path.getsize(full)} bytes)")
