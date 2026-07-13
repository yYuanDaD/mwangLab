"""Smoke test for run_limma_analysis on the existing GSE266241 normalized matrix.

Runs limma on log2(CPM+1) data with the same tissue contrast that DESeq2 was run on,
so we can sanity-check the top-gene overlap between the two methods.

No LLM, no GEO download — just reads existing CSVs and runs the tool.
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from tools.limma_tools import run_limma_analysis


def main():
    expr_csv = "output/GSE266241/GSE266241_1hr_SC_raw_data_normalized.csv"
    meta_csv = "data/GSE266241/GSE266241_metadata.csv"
    out_dir = "test/output/smoke_test/limma"
    os.makedirs(out_dir, exist_ok=True)

    # Same contrast that DESeq2 was run on, so we can compare top-gene overlap.
    result = run_limma_analysis.invoke({
        "normalized_csv": expr_csv,
        "metadata_csv": meta_csv,
        "design_column": "source_name_ch1",
        "control_group": "Cervical Spinal Cord",
        "treatment_group": "Thoracic and Lumbar Spinal Cord",
        "output_dir": out_dir,
    })
    print("\n=== run_limma_analysis result ===")
    print(result)

    limma_csv = os.path.join(out_dir, "DEG_results_Thoracic_and_Lumbar_Spinal_Cord_vs_Cervical_Spinal_Cord.csv")
    deseq_csv = "output/GSE266241/DEG_results_Thoracic and Lumbar Spinal Cord_vs_Cervical Spinal Cord.csv"

    if not os.path.exists(limma_csv):
        print(f"\nFAIL: expected output not found at {limma_csv}")
        sys.exit(1)

    limma = pd.read_csv(limma_csv, index_col=0)
    print(f"\nlimma output: {limma.shape[0]} features, columns={list(limma.columns)}")
    print(f"limma top 5 by padj:\n{limma.nsmallest(5, 'padj')[['log2FoldChange', 'pvalue', 'padj']]}")

    required_cols = {"log2FoldChange", "padj", "pvalue"}
    missing = required_cols - set(limma.columns)
    if missing:
        print(f"\nFAIL: limma output missing DESeq2-compatible columns: {missing}")
        sys.exit(1)

    if not os.path.exists(deseq_csv):
        print(f"\nNo DESeq2 file found at {deseq_csv} — skipping overlap check.")
    else:
        deseq = pd.read_csv(deseq_csv, index_col=0)
        limma_top = set(limma.nsmallest(100, "padj").index)
        deseq_top = set(deseq.nsmallest(100, "padj").index)
        overlap = limma_top & deseq_top
        print(f"\nTop-100 overlap (limma vs DESeq2 on same contrast): {len(overlap)}/100")
        if len(overlap) < 30:
            print("WARNING: low overlap. limma uses log-scale moderated-t, DESeq2 uses raw-counts NB-Wald — ")
            print("they will disagree somewhat, but <30/100 suggests something is off.")
        else:
            print(f"OK: meaningful overlap with DESeq2 on the same contrast.")

    print("\nPASS")


if __name__ == "__main__":
    main()
