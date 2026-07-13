"""Offline tests for repeated subset/rerun evaluation.

Run:
  PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_evaluation_tools.py
"""

import os
import sys
import tempfile

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from tools.evaluation_tools import (
    compare_deg_result_files,
    compare_gsea_result_files,
    evaluate_repeated_results_core,
)


def _write_deg(path, shift=0.0):
    genes = [f"Gene{i}" for i in range(1, 9)]
    df = pd.DataFrame({
        "log2FoldChange": [3.0, 2.4, -2.2, 1.4, -1.2, 0.5, -0.3, 0.1],
        "pvalue": [0.001, 0.002, 0.003, 0.02, 0.03, 0.2, 0.6, 0.9],
        "padj": [0.005, 0.01, 0.015, 0.04, 0.06, 0.3, 0.7, 0.95],
    }, index=genes)
    df["log2FoldChange"] = df["log2FoldChange"] + shift
    df.to_csv(path)


def _write_gsea(path, shift=0.0):
    df = pd.DataFrame({
        "Term": ["HALLMARK_A", "HALLMARK_B", "HALLMARK_C", "HALLMARK_D"],
        "NES": [2.1 + shift, 1.6 + shift, -1.8 - shift, -1.2],
        "FDR q-val": [0.02, 0.08, 0.12, 0.5],
    })
    df.to_csv(path, index=False)


def test_deg_pairwise_metrics():
    d = tempfile.mkdtemp()
    a = os.path.join(d, "deg_run1.csv")
    b = os.path.join(d, "deg_run2.csv")
    _write_deg(a, 0.0)
    _write_deg(b, 0.05)
    pairwise, summary = compare_deg_result_files([a, b], top_n=3)
    assert len(pairwise) == 1
    assert pairwise.loc[0, "log2fc_pearson"] > 0.99
    assert pairwise.loc[0, "top3_jaccard"] == 1.0
    assert summary["mean_sig_deg_jaccard"] == 1.0
    print("  [ok] DEG repeated-run metrics: correlation + top/significant overlap")


def test_gsea_pairwise_metrics():
    d = tempfile.mkdtemp()
    a = os.path.join(d, "gsea_run1.csv")
    b = os.path.join(d, "gsea_run2.csv")
    _write_gsea(a, 0.0)
    _write_gsea(b, 0.03)
    pairwise, summary = compare_gsea_result_files([a, b], top_n=2)
    assert len(pairwise) == 1
    assert pairwise.loc[0, "nes_pearson"] > 0.99
    assert pairwise.loc[0, "top2_pathway_jaccard"] == 1.0
    assert summary["mean_sig_pathway_jaccard"] == 1.0
    print("  [ok] GSEA repeated-run metrics: NES correlation + pathway overlap")


def test_core_writes_artifacts_without_llm():
    d = tempfile.mkdtemp()
    deg1, deg2 = os.path.join(d, "deg1.csv"), os.path.join(d, "deg2.csv")
    gsea1, gsea2 = os.path.join(d, "gsea1.csv"), os.path.join(d, "gsea2.csv")
    _write_deg(deg1, 0.0)
    _write_deg(deg2, 0.1)
    _write_gsea(gsea1, 0.0)
    _write_gsea(gsea2, 0.02)
    summary = evaluate_repeated_results_core(
        deg_csvs=[deg1, deg2],
        gsea_csvs=[gsea1, gsea2],
        output_dir=d,
        label="synthetic",
        use_llm_judge=False,
    )
    assert summary["judge"]["verdict"] == "stable"
    for p in summary["artifacts"].values():
        assert os.path.exists(p), p
    print("  [ok] evaluation core writes pairwise CSVs + summary JSON with heuristic judge")


if __name__ == "__main__":
    test_deg_pairwise_metrics()
    test_gsea_pairwise_metrics()
    test_core_writes_artifacts_without_llm()
    print("\nALL TESTS PASSED.")
