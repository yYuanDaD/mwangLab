"""Offline wiring test for batch-pipeline subset evaluation.

This test proves that run_batch_geo_pipeline(..., evaluate_subsets=True) launches
repeated subset DA runs, feeds the outputs to evaluation_tools, and writes eval_*
columns into summary.csv. Heavy/network steps are monkeypatched.

Run:
  PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_batch_subset_evaluation.py
"""

import os
import sys

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import tools.batch_tools as bt
from tools.deseq2_tools import deg_filename


class _DummyTool:
    def __init__(self, fn):
        self.fn = fn

    def invoke(self, kwargs):
        return self.fn(kwargs)


def _setup_fake_study(acc: str):
    data_dir = os.path.join("data", acc)
    os.makedirs(data_dir, exist_ok=True)
    meta = pd.DataFrame({
        "title": [f"sample {i}" for i in range(1, 7)],
        "condition": ["control"] * 3 + ["exercise"] * 3,
    }, index=[f"s{i}" for i in range(1, 7)])
    meta.to_csv(os.path.join(data_dir, f"{acc}_metadata.csv"))
    expr = pd.DataFrame({
        "s1": [5.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.5, 0.2],
        "s2": [5.1, 4.1, 3.0, 2.1, 1.4, 1.0, 0.5, 0.2],
        "s3": [4.9, 3.9, 3.1, 2.0, 1.5, 1.1, 0.4, 0.2],
        "s4": [8.0, 6.5, 1.0, 3.8, 0.2, 1.2, 0.4, 0.2],
        "s5": [8.1, 6.6, 1.1, 3.9, 0.2, 1.1, 0.5, 0.3],
        "s6": [7.9, 6.4, 0.9, 3.7, 0.3, 1.2, 0.4, 0.2],
    }, index=[f"Gene{i}" for i in range(1, 9)])
    expr.to_csv(os.path.join(data_dir, f"{acc}_log_expr.csv"))


def _fake_da(method, counts_path, da_input_path, metadata_csv, col, ctrl, treat, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    meta = pd.read_csv(metadata_csv, index_col=0)
    # tiny deterministic perturbation so the evaluator exercises correlations, not byte identity
    offset = (len(meta.index) % 3) * 0.02
    df = pd.DataFrame({
        "log2FoldChange": [3.0 + offset, 2.5 + offset, -2.0 - offset, 1.2, -1.1, 0.4, -0.3, 0.1],
        "pvalue": [0.001, 0.002, 0.003, 0.02, 0.04, 0.2, 0.6, 0.9],
        "padj": [0.005, 0.01, 0.015, 0.04, 0.049, 0.3, 0.7, 0.95],
        "stat": [9.0, 8.0, -7.0, 3.0, -2.8, 0.7, -0.3, 0.1],
    }, index=[f"Gene{i}" for i in range(1, 9)])
    out = os.path.join(output_dir, deg_filename(treat, ctrl))
    df.to_csv(out)
    return f"fake {method} wrote {out}"


def _fake_gsea(deg_csv, organism, study_out, dlog, fail_log, acc, label):
    df = pd.DataFrame({
        "Term": ["HALLMARK_A", "HALLMARK_B", "HALLMARK_C"],
        "NES": [2.0, 1.4, -1.8],
        "FDR q-val": [0.03, 0.2, 0.1],
    })
    base = os.path.splitext(os.path.basename(deg_csv))[0]
    df.to_csv(os.path.join(study_out, f"{base}_GSEA_Hallmark.csv"), index=False)
    return 2, "deg_gsea_ok"


def test_batch_subset_evaluation_wiring():
    acc = "GSEFAKEEVAL"
    _setup_fake_study(acc)

    old_dl = bt.download_geo_data
    old_supp = bt.download_supplementary_files
    old_qc = bt.sample_qc_summary
    old_sex = bt._run_sex_check
    old_da = bt._invoke_da_method
    old_gsea = bt._gsea_for_deg
    try:
        bt.download_geo_data = _DummyTool(lambda kwargs: "fake metadata already present")
        bt.download_supplementary_files = _DummyTool(lambda kwargs: "fake supplementary skip")
        bt.sample_qc_summary = _DummyTool(lambda kwargs: "fake QC")
        bt._run_sex_check = lambda *a, **k: {
            "verdict": "skipped", "summary": "fake sex check", "n_mismatch": 0, "mismatched": []}
        bt._invoke_da_method = _fake_da
        bt._gsea_for_deg = _fake_gsea

        fn = getattr(bt.run_batch_geo_pipeline, "func", bt.run_batch_geo_pipeline)
        report = fn(
            accessions=[acc],
            organism="Mouse",
            treatment_keywords=["exercise"],
            control_keywords=["control"],
            output_base=os.path.join("test", "output"),
            run_label="subset_eval_wiring",
            llm_datatype=False,
            evaluate_subsets=True,
            evaluation_runs=3,
            evaluation_subset_fraction=0.67,
            evaluation_include_gsea=False,
        )
    finally:
        bt.download_geo_data = old_dl
        bt.download_supplementary_files = old_supp
        bt.sample_qc_summary = old_qc
        bt._run_sex_check = old_sex
        bt._invoke_da_method = old_da
        bt._gsea_for_deg = old_gsea

    summary_path = os.path.join("test", "output", "cohort_subset_eval_wiring", "summary.csv")
    assert os.path.exists(summary_path), report
    row = pd.read_csv(summary_path).iloc[0].to_dict()
    assert row["status"] == "deg_gsea_ok"
    assert row["eval_verdict"] == "stable", row
    assert float(row["eval_deg_log2fc_r"]) > 0.99
    assert os.path.exists(row["eval_summary_json"]), row["eval_summary_json"]
    print("  [ok] batch evaluate_subsets=True writes eval_* summary columns and artifacts")


if __name__ == "__main__":
    test_batch_subset_evaluation_wiring()
    print("\nALL TESTS PASSED.")
