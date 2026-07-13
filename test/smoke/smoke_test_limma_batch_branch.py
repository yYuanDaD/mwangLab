"""Smoke test for the new limma branch in batch_tools.

Verifies, on existing on-disk studies (no re-download):
  1. _find_expression_file now accepts log_transformed and fpkm_or_tpm matrices
  2. _log2_transform_matrix produces a valid sibling file for fpkm_or_tpm
  3. The full DA → DEG output chain works via limma on a real non-raw matrix

Uses GSE283691 (fpkm_or_tpm, 7 groups × 7 samples, picks HFD vs SD contrast).
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from tools.batch_tools import _find_expression_file, _log2_transform_matrix
from tools.limma_tools import run_limma_analysis


def main():
    print("=== test 1: _find_expression_file accepts log_transformed ===")
    p, mt = _find_expression_file("data/GSE315104")
    print(f"GSE315104 -> {mt}  (path={os.path.basename(p) if p else '-'})")
    assert mt == "log_transformed", f"expected log_transformed, got {mt}"
    assert p and os.path.exists(p)
    print("PASS")

    print("\n=== test 2: _find_expression_file accepts fpkm_or_tpm ===")
    p, mt = _find_expression_file("data/GSE283691")
    print(f"GSE283691 -> {mt}  (path={os.path.basename(p) if p else '-'})")
    assert mt == "fpkm_or_tpm", f"expected fpkm_or_tpm, got {mt}"
    assert p and os.path.exists(p)
    print("PASS")

    print("\n=== test 3: _log2_transform_matrix on the fpkm/tpm file ===")
    log2_path = _log2_transform_matrix(p)
    assert log2_path.endswith("_log2.csv"), f"unexpected output name: {log2_path}"
    assert os.path.exists(log2_path)
    df = pd.read_csv(log2_path, index_col=0, nrows=200)
    numeric = df.select_dtypes(include="number")
    max_val = float(numeric.max().max())
    print(f"log2 file: {os.path.basename(log2_path)} | preview max = {max_val:.2f}")
    assert max_val < 30, f"log2 values look too big (max={max_val}); transform may not have run"
    print("PASS")

    print("\n=== test 4: run_limma_analysis on the log2-transformed file (HFD vs SD) ===")
    out_dir = "test/output/smoke_test/limma_batch"
    os.makedirs(out_dir, exist_ok=True)
    result = run_limma_analysis.invoke({
        "normalized_csv": log2_path,
        "metadata_csv": "data/GSE283691/GSE283691_metadata.csv",
        "design_column": "characteristics_ch1.2.treatment",
        "control_group": "SD",
        "treatment_group": "HFD",
        "output_dir": out_dir,
    })
    print(result)
    deg_csv = os.path.join(out_dir, "DEG_results_HFD_vs_SD.csv")
    assert os.path.exists(deg_csv), f"DEG output missing: {deg_csv}"
    deg = pd.read_csv(deg_csv, index_col=0)
    required = {"log2FoldChange", "padj", "pvalue"}
    assert required.issubset(set(deg.columns)), f"missing cols: {required - set(deg.columns)}"
    n_sig = int((deg["padj"] < 0.05).sum())
    print(f"DEG features: {len(deg)} | padj<0.05: {n_sig}")
    print("PASS")

    print("\n=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    main()
