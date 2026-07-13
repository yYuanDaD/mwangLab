"""Tests for rule #1: gene/pathway tables are data-derived, not article-filled."""

import os
import sys
import tempfile

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from tools.gene_loader import gene_rows_for_study_batch
from tools.seacdm_tools import build_reported_findings


def test_reported_findings_do_not_fill_gene_or_pathway():
    d = tempfile.mkdtemp()
    out = build_reported_findings(
        "GSE1",
        "unused",
        os.path.join(d, "GSE1_reported_findings.csv"),
        prefetched_findings=[
            {
                "entity": "Bdnf",
                "entity_type": "gene",
                "direction": "up",
                "magnitude": "2-fold",
                "comparison": "exercise vs control",
                "source": "Bdnf was upregulated",
            },
            {
                "entity": "mitochondrial biogenesis",
                "entity_type": "pathway",
                "direction": "up",
                "magnitude": None,
                "comparison": "exercise vs control",
                "source": "mitochondrial biogenesis increased",
            },
        ],
    )
    assert out["gene"] == []
    assert out["pathway"] == []
    assert len(out["results"]) == 1
    print("  [ok] reported_findings stays evidence-only; no gene/pathway table rows")


def test_gene_rows_from_deg_files():
    d = tempfile.mkdtemp()
    deg = os.path.join(d, "DEG_results_exercise_vs_control.csv")
    pd.DataFrame({
        "log2FoldChange": [2.0, -1.5, 0.2],
        "pvalue": [0.001, 0.002, 0.5],
        "padj": [0.01, 0.02, 0.8],
        "stat": [5.0, -4.0, 0.1],
    }, index=["Bdnf", "Fos", "Noise"]).to_csv(deg)
    rows = gene_rows_for_study_batch("GSE1", d, organism="Mouse", log2fc_cutoff=1.0)
    assert len(rows) == 2
    assert {r["gene_symbol"] for r in rows} == {"Bdnf", "Fos"}
    assert {r["reference_source"] for r in rows} == {"computed_deg"}
    assert all(r["gene_symbol_source"] == os.path.normpath(deg) for r in rows)
    print("  [ok] DEG result files populate computed gene rows")


if __name__ == "__main__":
    test_reported_findings_do_not_fill_gene_or_pathway()
    test_gene_rows_from_deg_files()
    print("\nALL TESTS PASSED.")
