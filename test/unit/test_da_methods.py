"""Tests for the raw-counts DA method matrix: DESeq2 / edgeR / limma-voom.

Run:  PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_da_methods.py

Uses the already-downloaded GSE279359 (no network). Runs all three methods on the same
pre-vs-post contrast, checks each DEG CSV is DESeq2-column-compatible, prints concordance,
then runs run_batch_geo_pipeline with raw_da_method='edger' to confirm the dispatch wiring
records the chosen method in summary.csv.
"""

import os
import sys
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

import pandas as pd

COUNTS = "data/GSE279359/GSE279359_processed_counts.txt.gz"
META = "data/GSE279359/GSE279359_metadata.csv"
DESIGN = "characteristics_ch1.1.time"
CTRL, TREAT = "pre-exercise", "immediately post-exercise"
_REQUIRED = {"log2FoldChange", "padj", "pvalue", "stat"}


def _check_deg(path, label):
    assert os.path.isfile(path), f"{label}: DEG csv not written"
    d = pd.read_csv(path, index_col=0)
    missing = _REQUIRED - set(d.columns)
    assert not missing, f"{label}: DEG csv missing DESeq2-compatible columns {missing} (has {list(d.columns)})"
    n_sig = int((d["padj"] < 0.05).sum())
    return len(d), n_sig


def test_three_methods():
    if not os.path.isfile(COUNTS):
        print("SKIP: GSE279359 not downloaded.")
        return
    from tools.deseq2_tools import run_deseq2_analysis
    from tools.edger_tools import run_edger_analysis
    from tools.limma_voom_tools import run_limma_voom_analysis

    results = {}
    for name, tool, kwargs in [
        ("deseq2", run_deseq2_analysis, {"counts_csv": COUNTS}),
        ("edger", run_edger_analysis, {"counts_csv": COUNTS}),
        ("limma-voom", run_limma_voom_analysis, {"counts_csv": COUNTS}),
    ]:
        out = f"test/output/smoke_test/da_{name.replace('-', '_')}"
        if os.path.isdir(out):
            import shutil; shutil.rmtree(out)
        msg = tool.invoke({**kwargs, "metadata_csv": META, "design_column": DESIGN,
                           "control_group": CTRL, "treatment_group": TREAT, "output_dir": out})
        if "unavailable" in msg.lower():
            print(f"  [{name}] SKIP — {msg.splitlines()[0]}")
            continue
        degs = glob.glob(os.path.join(out, "DEG_*.csv"))
        assert degs, f"{name}: no DEG csv. Tool said: {msg.splitlines()[-1]}"
        n_genes, n_sig = _check_deg(degs[0], name)
        results[name] = (n_genes, n_sig)
        print(f"  [{name}] {n_genes} genes, {n_sig} sig(padj<0.05) — DESeq2-compatible columns OK")

    # all methods that ran should cover the same gene universe
    gene_counts = {n: g for n, (g, _) in results.items()}
    assert len(set(gene_counts.values())) == 1, f"gene-count mismatch across methods: {gene_counts}"
    print(f"[methods] {len(results)} methods ran on identical gene universe; sig counts: "
          f"{ {n: s for n, (_, s) in results.items()} }")


def test_batch_wiring_edger():
    if not os.path.isfile(COUNTS):
        print("SKIP batch wiring: GSE279359 not downloaded.")
        return
    from tools.batch_tools import run_batch_geo_pipeline, _RAW_DA_METHODS
    assert _RAW_DA_METHODS == {"deseq2", "edger", "limma-voom"}, _RAW_DA_METHODS
    out_base = "test/output/smoke_test"
    label = "da_wiring"
    run_dir = os.path.join(out_base, f"cohort_{label}")
    if os.path.isdir(run_dir):
        import shutil; shutil.rmtree(run_dir)
    run_batch_geo_pipeline.invoke({
        "accessions": ["GSE279359"], "organism": "Mouse",
        "treatment_keywords": ["post", "immediately", "exercise"],
        "control_keywords": ["pre", "baseline"],
        "output_base": out_base, "run_label": label, "raw_da_method": "edger",
    })
    summary = pd.read_csv(os.path.join(run_dir, "summary.csv"))
    method = str(summary.iloc[0]["da_method"])
    assert method == "edger", f"expected da_method=edger, got {method}"
    print(f"[batch-wiring] raw_da_method='edger' -> summary.da_method={method}, "
          f"status={summary.iloc[0]['status']} | wiring OK")


if __name__ == "__main__":
    test_three_methods()
    test_batch_wiring_edger()
    print("\nAll DA-method tests passed.")
