"""End-to-end FUNCTIONAL validation of the proteomics pipeline on REAL PRIDE data.

There is no proteomics ground-truth DEG database (new_deg3 is RNA-seq), so this is a
plumbing/functional check, NOT a concordance validation: confirm the full chain runs on a
real DIA-LFQ matrix and emits a DESeq2-column-compatible DEG.

  identify_proteomics_labeling(PXD025560)         -> label_free + has_quant_matrix
  preprocess_proteomics_matrix(real .xlsx, LFQ)   -> log2 + missingness filter + MinProb + center
  run_limma_analysis(preprocessed, 2-group)       -> DEG CSV (the shared, already-validated DA)

PXD025560 is a classification cohort with no clean case/control labels in the matrix columns, so
the limma contrast here is an ARBITRARY half/half split of the cohort samples — it exercises the DA
plumbing, the numbers are not a biological result.
"""

import os
import sys
import json
import glob
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.proteomics_tools import identify_proteomics_labeling, preprocess_proteomics_matrix
from tools.limma_tools import run_limma_analysis

PXD = "PXD025560"
QUANT = "data/PXD025560/Protein_results.xlsx"
OUT = "test/output/smoke_test/proteomics_e2e"
_REQUIRED = {"log2FoldChange", "padj", "pvalue", "stat"}


def main():
    os.makedirs(OUT, exist_ok=True)

    print("=== 1. identify labeling ===")
    info = json.loads(identify_proteomics_labeling.invoke({"pxd_accession": PXD}))
    print(f"  labeling={info['labeling']} reagent={info.get('reagent')} "
          f"has_quant_matrix={info['has_quant_matrix']} source={info.get('source')}")
    assert info["labeling"] == "label_free", info["labeling"]

    print("\n=== 2. preprocess real matrix ===")
    msg = preprocess_proteomics_matrix.invoke({
        "quant_path": QUANT, "labeling": "label_free", "output_dir": OUT,
    })
    print("  " + "\n  ".join(msg.splitlines()[-6:]))
    pre = glob.glob(os.path.join(OUT, "*_preprocessed.csv"))
    assert pre, "no preprocessed file written"
    pre = pre[0]
    m = pd.read_csv(pre, index_col=0)
    print(f"  preprocessed matrix: {m.shape[0]} proteins x {m.shape[1]} samples")
    assert m.isna().sum().sum() == 0, "LFQ output should have no NaN after imputation"
    assert float(m.to_numpy().max()) < 40, "should be log-scale"

    print("\n=== 3. limma DA (ARBITRARY half/half split — plumbing check) ===")
    cols = list(m.columns)
    half = len(cols) // 2
    grp = pd.DataFrame({"grp": ["A"] * half + ["B"] * (len(cols) - half)}, index=cols)
    meta_path = os.path.join(OUT, "arbitrary_groups.csv")
    grp.to_csv(meta_path)
    msg = run_limma_analysis.invoke({
        "normalized_csv": pre, "metadata_csv": meta_path,
        "design_column": "grp", "control_group": "A", "treatment_group": "B", "output_dir": OUT,
    })
    print("  " + "\n  ".join(msg.splitlines()[-4:]))
    deg = glob.glob(os.path.join(OUT, "DEG_*.csv"))
    assert deg, "no DEG written"
    d = pd.read_csv(deg[0], index_col=0)
    missing = _REQUIRED - set(d.columns)
    assert not missing, f"DEG missing DESeq2-compatible columns: {missing} (has {list(d.columns)})"
    print(f"  DEG: {d.shape[0]} proteins, columns OK (DESeq2-compatible: log2FoldChange/padj/pvalue/stat)")
    print(f"  protein IDs (head): {list(d.index[:5])}")

    print("\n=== PROTEOMICS E2E: PASS (identify -> preprocess[real] -> limma -> DEG) ===")


if __name__ == "__main__":
    main()
