"""Tests for KG-style CSV export matching kg_extraction_results_v8.csv."""

import os
import sys
import tempfile

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from tools.kg_export_tools import KG_COLUMNS, export_kg_style_results_core


def test_kg_export_columns_and_mapping():
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "csv"), exist_ok=True)
    os.makedirs(os.path.join(d, "studies"), exist_ok=True)

    pd.DataFrame([{
        "study_id": "GSE1",
        "study_name": "Exercise study",
        "study_description": "",
    }]).to_csv(os.path.join(d, "csv", "study.csv"), index=False)
    pd.DataFrame([{
        "gene_id": "GSE1_deg_gene1",
        "study_id": "GSE1",
        "gene_symbol": "Bdnf",
        "gene_symbol_source": "DEG_results_exercise_vs_control.csv",
        "comparison": "exercise vs control",
        "regulation_direction": "up",
        "magnitude": "log2FC=2.1; padj=0.01",
        "reference_source": "computed_deg",
    }]).to_csv(os.path.join(d, "csv", "gene.csv"), index=False)
    pd.DataFrame([{
        "entity": "grip strength",
        "entity_type": "phenotype",
        "direction": "up",
        "magnitude": "",
        "comparison": "exercise vs control",
        "source": "grip strength was increased",
    }]).to_csv(os.path.join(d, "studies", "GSE1_reported_findings.csv"), index=False)

    out = os.path.join(d, "kg.csv")
    res = export_kg_style_results_core(d, out)
    df = pd.read_csv(out)
    assert list(df.columns) == KG_COLUMNS
    assert res["n_rows"] == 1
    row = df.iloc[0].to_dict()
    assert row["regulated_gene"] == "Bdnf"
    assert row["relationship"] == "upregulates"
    assert row["phenotypic_change"] == "grip strength"
    assert "computed_deg" in row["data_source"]
    print("  [ok] KG-style exporter writes reference columns and maps DEG gene + paper phenotype")


if __name__ == "__main__":
    test_kg_export_columns_and_mapping()
    print("\nALL TESTS PASSED.")
