"""Smoke test for `_classify_matrix` and `_is_derived_stat_column`.

Verifies the 2026-05-28 fix to the GSE317978 misclassification, plus the
heuristic stays correct on the 4 canonical input shapes:
  - raw_counts: integers, max >> 100
  - fpkm_or_tpm: positive floats, max ≥ 30 (real FPKM values can exceed 10000)
  - log_transformed: floats with negatives OR decimals with small max (≤30)
  - mixed FPKM + diffexp_* derived stats (GSE317978 case): must NOT be misled
    by the negative log2fc values into classifying as log_transformed

No network, no LLM. Run: PYTHONIOENCODING=utf-8 python test/unit/test_classify_matrix.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd

from tools.batch_tools import _classify_matrix, _is_derived_stat_column


def _write_csv(out_dir: str, name: str, df: pd.DataFrame) -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    df.to_csv(path, index=False)
    return path


def test_synthetic_classification():
    print("=" * 70)
    print(" _classify_matrix — synthetic canonical inputs")
    print("=" * 70)
    out_dir = "test/output/classify_matrix"
    rng = np.random.default_rng(42)
    n_genes = 50

    cases = []
    # Raw counts: integers, max large
    cases.append((
        "raw_counts",
        _write_csv(out_dir, "synth_raw_counts.csv", pd.DataFrame({
            "gene_id": [f"g{i:05d}" for i in range(n_genes)],
            **{f"S{j}": rng.integers(0, 50000, n_genes) for j in range(6)},
        })),
    ))
    # FPKM/TPM: positive floats, max can be very high (real-world FPKM can hit 10k+)
    cases.append((
        "fpkm_or_tpm",
        _write_csv(out_dir, "synth_fpkm.csv", pd.DataFrame({
            "gene_id": [f"g{i:05d}" for i in range(n_genes)],
            **{f"S{j}": np.exp(rng.uniform(-2, 11, n_genes)) for j in range(6)},
        })),
    ))
    # Log-transformed: positive floats with small max (log2(CPM+1) caps ~20)
    cases.append((
        "log_transformed",
        _write_csv(out_dir, "synth_log_cpm.csv", pd.DataFrame({
            "gene_id": [f"g{i:05d}" for i in range(n_genes)],
            **{f"S{j}": rng.uniform(0.1, 18, n_genes) for j in range(6)},
        })),
    ))
    # Log-transformed with negatives: log2 ratios
    cases.append((
        "log_transformed",
        _write_csv(out_dir, "synth_log_ratios.csv", pd.DataFrame({
            "gene_id": [f"g{i:05d}" for i in range(n_genes)],
            **{f"S{j}": rng.uniform(-8, 8, n_genes) for j in range(6)},
        })),
    ))

    n_pass, n_fail = 0, 0
    for expected, path in cases:
        got, _ = _classify_matrix(path)
        status = "OK " if got == expected else "FAIL"
        if got == expected: n_pass += 1
        else: n_fail += 1
        print(f"  [{status}] {os.path.basename(path)}: expected {expected}, got {got}")
    return n_pass, n_fail


def test_stat_column_filter_regression():
    """The GSE317978 case: 6 fpkm_Sample* cols (positive floats) + 6 diffexp_*
    cols (negatives + p/q values). Without the filter, negatives dominate and
    the file misclassifies as log_transformed. With the filter, the 6 sample
    cols drive classification → fpkm_or_tpm."""
    print("\n" + "=" * 70)
    print(" _classify_matrix — GSE317978 mixed FPKM+diffexp regression")
    print("=" * 70)
    out_dir = "test/output/classify_matrix"
    rng = np.random.default_rng(317)
    n_genes = 50
    df = pd.DataFrame({"gene_id": [f"g{i:05d}" for i in range(n_genes)]})
    # 6 FPKM sample cols: positive floats with realistic max
    for j in range(6):
        df[f"fpkm_Sample{16+j}"] = np.exp(rng.uniform(-2, 11, n_genes))
    # 6 derived stat cols mimicking the real GSE317978 file
    df["diffexp_log2fc_A-vs-B"] = rng.uniform(-8, 8, n_genes)
    df["diffexp_deseq2_pvalue_A-vs-B"] = rng.uniform(0, 1, n_genes)
    df["diffexp_deseq2_qvalue_A-vs-B"] = rng.uniform(0, 1, n_genes)
    df["diffexp_log2fc_B-vs-C"] = rng.uniform(-8, 8, n_genes)
    df["diffexp_deseq2_pvalue_B-vs-C"] = rng.uniform(0, 1, n_genes)
    df["diffexp_deseq2_qvalue_B-vs-C"] = rng.uniform(0, 1, n_genes)
    path = _write_csv(out_dir, "synth_gse317978_pattern.csv", df)

    got, _ = _classify_matrix(path)
    expected = "fpkm_or_tpm"
    n_pass, n_fail = 0, 0
    ok = got == expected
    print(f"  [{'OK ' if ok else 'FAIL'}] mixed-cols file: expected {expected}, got {got}")
    if ok: n_pass += 1
    else:  n_fail += 1

    # Spot-check that each diffexp_* col is flagged by the filter
    stat_hits = [c for c in df.columns if _is_derived_stat_column(c)]
    sample_hits = [c for c in df.columns if c.startswith("fpkm_")]
    expected_stats = {c for c in df.columns if c.startswith("diffexp_")}
    expected_samples = {c for c in df.columns if c.startswith("fpkm_")}
    stats_ok = set(stat_hits) == expected_stats
    samples_not_flagged = not any(_is_derived_stat_column(c) for c in sample_hits)
    print(f"  [{'OK ' if stats_ok else 'FAIL'}] all 6 diffexp_* flagged as stats (got {len(stat_hits)})")
    print(f"  [{'OK ' if samples_not_flagged else 'FAIL'}] fpkm_Sample* NOT flagged as stats")
    n_pass += (1 if stats_ok else 0) + (1 if samples_not_flagged else 0)
    n_fail += (0 if stats_ok else 1) + (0 if samples_not_flagged else 1)
    return n_pass, n_fail


def run():
    p1, f1 = test_synthetic_classification()
    p2, f2 = test_stat_column_filter_regression()
    total_pass, total_fail = p1 + p2, f1 + f2
    print("\n" + "=" * 70)
    print(f" TOTAL: {total_pass} passed, {total_fail} failed")
    print(f"   canonical 4-shape classification: {p1}/{p1 + f1}")
    print(f"   GSE317978 stat-filter regression:  {p2}/{p2 + f2}")
    print("=" * 70)
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
