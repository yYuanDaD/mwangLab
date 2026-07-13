"""edgeR differential expression for RAW integer counts (via inmoose.edgepy).

One of the three raw-counts DA methods in the mentor's method matrix
(DESeq2 / limma-voom / edgeR). edgeR fits a negative-binomial GLM with
quasi-likelihood F-tests — same NB family as DESeq2, commonly used as a
cross-method sanity check.

Output CSV is column-compatible with run_deseq2_analysis / run_limma_analysis
(log2FoldChange / padj / pvalue / lfcSE / stat) so enrichment_tools and GSEA
consume it unchanged.

Notes:
  - inmoose 0.9.1 exposes the full edgeR GLM path (DGEList, estimateGLMCommonDisp,
    estimateGLMTagwiseDisp, glmQLFit, glmQLFTest, topTags) BUT NOT calcNormFactors
    (TMM). We therefore run with default library-size normalization (norm_factors=1);
    TMM would refine normalization but the NB GLM is valid without it.
  - inmoose's topTags already returns DESeq2-style names (log2FoldChange / lfcSE /
    stat / pvalue) plus FDR/adj_pvalue; we rename adj_pvalue -> padj.
  - DGEList expects counts as genes (rows) x samples (columns) — the native GEO
    orientation — so unlike run_deseq2_analysis we do NOT transpose.
"""

import os
import numpy as np
import pandas as pd
from patsy import dmatrix
from inmoose.edgepy import DGEList, glmQLFTest, topTags
from langchain_core.tools import tool

from tools.deseq2_tools import deg_filename, collapse_duplicate_genes


@tool
def run_edger_analysis(
    counts_csv: str,
    metadata_csv: str,
    design_column: str,
    control_group: str,
    treatment_group: str,
    output_dir: str = "./output",
) -> str:
    """
    Run Differential Expression Analysis using edgeR (negative-binomial GLM +
    quasi-likelihood F-test) via inmoose.

    USE THIS TOOL for RAW integer counts (same input as run_deseq2_analysis) —
    it is an alternative to DESeq2 in the raw-counts method matrix. DO NOT use for
    log-scale matrices (CPM/FPKM/TPM/proteomics) — use run_limma_analysis there.

    Args:
        counts_csv: Path to the raw counts CSV (rows=genes, cols=samples).
        metadata_csv: Path to the metadata CSV containing sample grouping (index=sample IDs).
        design_column: Metadata column to use as the design factor.
        control_group: Value in design_column for the control / baseline samples.
        treatment_group: Value in design_column for the treatment samples.
        output_dir: Directory to save the DEG CSV.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        print("Loading data for edgeR analysis...")
        counts_df = pd.read_csv(counts_csv, index_col=0, sep=None, engine="python")
        metadata_df = pd.read_csv(metadata_csv, index_col=0)

        # Drop entirely non-numeric columns (annotation columns some GEO files mix in).
        coerced = counts_df.apply(pd.to_numeric, errors="coerce")
        non_numeric = coerced.columns[coerced.isna().all(axis=0)].tolist()
        if non_numeric:
            print(f"   Dropping {len(non_numeric)} non-numeric columns (likely annotations): {non_numeric}")
            counts_df = counts_df.drop(columns=non_numeric)
        counts_df = collapse_duplicate_genes(counts_df, "edgeR")

        # Smart sample alignment (exact/substring/token-overlap/LLM) — same cascade as DESeq2/limma.
        counts_cols = counts_df.columns.tolist()
        meta_index = metadata_df.index.tolist()
        if len(set(counts_cols).intersection(set(meta_index))) == 0:
            print("Sample names do not match between counts and metadata. Attempting smart alignment...")
            from tools.llm_helpers import align_samples_with_llm_fallback
            mapping, method = align_samples_with_llm_fallback(counts_cols, metadata_df)
            if not mapping:
                return ("FATAL ERROR: sample names could not be matched (exact/substring/token-overlap/llm "
                        "all failed). Counts columns and metadata likely use different naming "
                        "conventions for this study; please check the data manually.")
            metadata_df = metadata_df.rename(index=mapping)
            metadata_df = metadata_df[~metadata_df.index.duplicated(keep="first")]
            print(f"Aligned via {method}.")

        all_available_groups = metadata_df[design_column].dropna().unique().tolist()
        mask = metadata_df[design_column].isin([control_group, treatment_group])
        metadata_df = metadata_df[mask]

        group_stats = metadata_df[design_column].value_counts()
        print(f"Sample distribution after filtering:\n{group_stats}")
        if len(group_stats) < 2:
            return (f"FATAL ERROR: cannot run differential analysis. File {os.path.basename(counts_csv)} "
                    f"does not contain both '{control_group}' and '{treatment_group}'.\n"
                    f"Currently available groups: {group_stats.index.tolist()}\n"
                    f"All groups in metadata column '{design_column}': {all_available_groups}\n"
                    f"Suggestion: check the counts file and that the metadata column name matches.")

        # Keep counts as genes x samples; subset to the contrast samples (columns).
        common = [s for s in metadata_df.index if s in counts_df.columns]
        if len(common) < 4:
            return (f"FATAL ERROR: only {len(common)} samples remain after alignment + group filtering. "
                    f"edgeR needs at least 2 samples per group (4 total).")
        metadata_df = metadata_df.loc[common]
        counts_sub = counts_df[common]

        # Integer counts; drop all-zero genes.
        counts_sub = counts_sub.round().astype(int)
        counts_sub = counts_sub.loc[(counts_sub != 0).any(axis=1)]
        n_genes, n_samples = counts_sub.shape
        print(f"Running edgeR on {n_samples} samples and {n_genes} genes...")

        # Design: ~ Treatment (Treatment=1 for treatment_group). coef index 1 = Treatment vs control.
        design_meta = pd.DataFrame(
            {"Treatment": (metadata_df[design_column] == treatment_group).astype(int).values},
            index=metadata_df.index,
        )
        design = dmatrix("~ Treatment", design_meta)
        group = metadata_df[design_column].astype(str).tolist()

        y = DGEList(counts=counts_sub, group=group)
        y = y.estimateGLMCommonDisp(design)
        y = y.estimateGLMTagwiseDisp(design)
        fit = y.glmQLFit(design)
        qlf = glmQLFTest(fit, coef=1)
        tt = topTags(qlf, n=n_genes, sort_by="PValue")
        res = pd.DataFrame(getattr(tt, "table", tt))

        # inmoose edgeR topTags -> DESeq2-style names already; standardize adj_pvalue -> padj.
        res = res.rename(columns={"adj_pvalue": "padj"})
        if "padj" not in res.columns and "FDR" in res.columns:
            res["padj"] = res["FDR"]
        front = [c for c in ["baseMean", "logCPM", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj"] if c in res.columns]
        rest = [c for c in res.columns if c not in front]
        res = res[front + rest]

        output_file = os.path.join(output_dir, deg_filename(treatment_group, control_group))
        res.to_csv(output_file)

        sig = res.dropna(subset=["padj", "log2FoldChange"])
        sig = sig[sig["padj"] < 0.05]
        up = sig[sig["log2FoldChange"] > 1]
        down = sig[sig["log2FoldChange"] < -1]

        return (f"edgeR analysis completed successfully!\n"
                f"Results saved to: {output_file}\n"
                f"Summary (padj < 0.05, |log2FC| > 1):\n"
                f"- Up-regulated genes: {len(up)}\n"
                f"- Down-regulated genes: {len(down)}")

    except Exception as e:
        print(f"Tool Error: {str(e)}")
        return f"edgeR analysis failed. Error: {str(e)}"
