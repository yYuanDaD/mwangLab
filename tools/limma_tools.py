import os
import pandas as pd
from patsy import dmatrix
from inmoose.limma import lmFit, eBayes, topTable
from langchain_core.tools import tool

from tools.deseq2_tools import deg_filename, collapse_duplicate_genes
from tools.analysis_policy import (
    PolicyViolation, enforce_method_matrix_compatibility, numeric_matrix,
    select_valid_two_group_design,
)


@tool
def run_limma_analysis(
    normalized_csv: str,
    metadata_csv: str,
    design_column: str,
    control_group: str,
    treatment_group: str,
    output_dir: str = "./output",
    design_formula: str = "",
    coefficient: str = "",
) -> str:
    """
    Run Differential Expression Analysis using limma (moderated t + empirical Bayes).

    USE THIS TOOL when the expression matrix is already on a log scale:
      - log2(CPM+1) normalized RNA-seq (output of preprocess_counts)
      - FPKM / TPM / RPKM (apply log2(x+1) first)
      - Proteomics intensities (LFQ / TMT / iBAQ, log2-transformed)
    DO NOT use for raw integer counts — call run_deseq2_analysis instead.

    Args:
        normalized_csv: Path to a log-scale expression CSV (rows=features, cols=samples).
        metadata_csv: Path to the metadata CSV containing sample grouping (index = sample IDs).
        design_column: Metadata column to use as the design factor (e.g. 'group').
        control_group: Value in design_column for the control / baseline samples.
        treatment_group: Value in design_column for the treatment samples.
        output_dir: Directory to save the DEG CSV.
        design_formula: Optional patsy formula for multifactor designs, e.g.
            ``~ genotype + exercise + genotype:exercise``. The treatment indicator
            remains the default when omitted.
        coefficient: Optional design-matrix coefficient to test when using a
            multifactor formula. For paired donor designs this is typically
            ``Treatment`` in ``~ C(donor) + Treatment``.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        print("Loading data for limma analysis...")
        expr_df = pd.read_csv(normalized_csv, index_col=0, sep=None, engine="python")
        metadata_df = pd.read_csv(metadata_csv, index_col=0)

        # Drop columns that are entirely non-numeric (e.g. gene_symbol / gene_biotype
        # annotation columns that some GEO files mix in). Match the same behaviour
        # stats_tools uses, so LLM-B's alignment denominator isn't inflated by columns
        # that could never plausibly be samples.
        expr_df = numeric_matrix(expr_df, label="limma expression matrix")
        expr_df = collapse_duplicate_genes(expr_df, "limma")

        expr_cols = expr_df.columns.tolist()
        meta_index = metadata_df.index.tolist()

        exact_n = len(set(expr_cols).intersection(set(meta_index)))
        exact_required = max(1, (min(len(expr_cols), len(meta_index)) + 1) // 2)
        if exact_n < exact_required:
            print("Sample names do not match between expression matrix and metadata. Attempting smart alignment...")
            from tools.llm_helpers import align_samples_with_llm_fallback
            mapping, method = align_samples_with_llm_fallback(expr_cols, metadata_df)
            if not mapping:
                return ("FATAL ERROR: sample names could not be matched (exact/substring/token-overlap/llm "
                        "all failed). Expression columns and metadata index likely use different naming "
                        "conventions for this study; please check the data manually.")
            metadata_df = metadata_df.rename(index=mapping)
            metadata_df = metadata_df[~metadata_df.index.duplicated(keep="first")]
            print(f"Aligned via {method}.")

        metadata_df, group_stats = select_valid_two_group_design(
            metadata_df, design_column=design_column, control_group=control_group,
            treatment_group=treatment_group, available_samples=expr_df.columns,
        )
        print(f"Sample distribution after filtering:\n{group_stats}")

        common = [s for s in metadata_df.index if s in expr_df.columns]
        if len(common) < 4:
            return (f"FATAL ERROR: only {len(common)} samples remain after alignment + group filtering. "
                    f"limma needs at least 2 samples per group (4 total) for meaningful moderation.")

        metadata_df = metadata_df.loc[common]
        expr_mat = expr_df[common]
        enforce_method_matrix_compatibility(expr_mat, method="limma")

        # Drop features that are mostly NA or have zero variance (limma can't moderate a constant row).
        nonna = expr_mat.notna().sum(axis=1)
        expr_mat = expr_mat.loc[nonna >= max(3, len(common) // 2)]
        variance = expr_mat.var(axis=1, skipna=True)
        expr_mat = expr_mat.loc[variance > 0]

        n_features, n_samples = expr_mat.shape
        print(f"Running limma on {n_samples} samples and {n_features} features...")

        # patsy dmatrix (DesignMatrix, NOT return_type='dataframe') — inmoose preserves
        # coefficient names only from a true DesignMatrix; DataFrames lose names on conversion.
        if design_formula:
            design_meta = metadata_df.copy()
            # Make the requested two-group contrast available to formulas that
            # include blocking terms (for example ``~ C(sample) + Treatment``).
            # Callers may provide their own Treatment column; otherwise derive
            # it from the validated design factor and group labels.
            if "Treatment" not in design_meta.columns:
                design_meta["Treatment"] = (
                    metadata_df[design_column] == treatment_group
                ).astype(int).values
            # Patsy formulas cannot safely reference arbitrary GEO column names;
            # callers should pass sanitized names or use Q('original name').
            design = dmatrix(design_formula, design_meta)
        else:
            design_meta = pd.DataFrame(
                {"Treatment": (metadata_df[design_column] == treatment_group).astype(int).values},
                index=metadata_df.index,
            )
            design = dmatrix("~ Treatment", design_meta)

        fit = lmFit(expr_mat, design=design)
        fit = eBayes(fit)

        design_names = list(design.design_info.column_names)
        coef = coefficient.strip() if coefficient else ("Treatment" if "Treatment" in design_names else design_names[-1])
        if coef not in design_names:
            return (f"FATAL ERROR: requested coefficient {coef!r} is not present in the design matrix. "
                    f"Available coefficients: {design_names}")
        top = topTable(fit, coef=coef, number=n_features, sort_by="P", adjust_method="fdr_bh")

        # inmoose's topTable already returns DESeq2-style column names (baseMean / log2FoldChange /
        # pvalue / lfcSE / stat) — only adj_pvalue needs renaming to padj for downstream consistency.
        # Cast to a plain DataFrame first to avoid DEResults' required-column validation on rename.
        top = pd.DataFrame(top).rename(columns={"adj_pvalue": "padj"})

        front = [c for c in ["baseMean", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj", "B"] if c in top.columns]
        rest = [c for c in top.columns if c not in front]
        top = top[front + rest]

        output_file = os.path.join(output_dir, deg_filename(treatment_group, control_group))
        top.to_csv(output_file)

        sig = top.dropna(subset=["padj", "log2FoldChange"])
        sig = sig[sig["padj"] < 0.05]
        up = sig[sig["log2FoldChange"] > 1]
        down = sig[sig["log2FoldChange"] < -1]

        return (f"limma analysis completed successfully!\n"
                f"Results saved to: {output_file}\n"
                f"Summary (padj < 0.05, |log2FC| > 1):\n"
                f"- Up-regulated features: {len(up)}\n"
                f"- Down-regulated features: {len(down)}")

    except PolicyViolation as e:
        return f"POLICY BLOCKED: {e}"
    except Exception as e:
        print(f"Tool Error: {str(e)}")
        return f"limma analysis failed. Error: {str(e)}"
