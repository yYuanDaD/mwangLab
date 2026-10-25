import os
import re
import numpy as np
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from tools.tooling import tool
from tools.analysis_policy import (
    PolicyViolation, enforce_method_matrix_compatibility, numeric_matrix,
    select_valid_two_group_design,
)
from tools.multifactor_design import build_multifactor_plan


from tools.de_common import (  # noqa: F401 - re-exported for existing callers
    _FNAME_BAD, collapse_duplicate_genes, deg_filename, safe_for_filename,
)


@tool
def run_deseq2_analysis(
    counts_csv: str,
    metadata_csv: str,
    design_column: str,
    control_group: str,
    treatment_group: str,
    output_dir: str = "./output",
    covariate_columns: str = "",
    interaction_terms: str = "",
    alpha: float = 0.05,
) -> str:
    """
    Run Differential Expression Analysis using PyDESeq2.

    ``alpha`` is the independent-filtering target (pydeseq2 default 0.05; R DESeq2's
    results() uses 0.1). Set it to the paper's FDR cutoff.

    Args:
        counts_csv: Path to the raw counts CSV file (must be unnormalized raw counts).
        metadata_csv: Path to the metadata CSV file containing sample grouping.
        design_column: The column name in metadata representing the experimental conditions (e.g., 'group').
        control_group: The specific value in the design_column representing the control/sham group.
        treatment_group: The specific value in the design_column representing the treatment/disease group.
        output_dir: Directory to save the final DEG results.
        covariate_columns: Optional comma-separated metadata columns for an
            additive multifactor model. Covariates are explicit; they are not
            guessed from metadata names.
        interaction_terms: Optional comma-separated ``factor:factor`` terms.
            DESeq2 currently refuses interaction terms because a main-effect
            pairwise contrast is not a sufficient estimand for an interaction.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        print("Loading data for DESeq2 analysis...")
        counts_df = pd.read_csv(counts_csv, index_col=0, sep=None, engine="python")
        counts_df = numeric_matrix(counts_df, label="DESeq2 counts matrix")
        counts_df = collapse_duplicate_genes(counts_df, "DESeq2")
        metadata_df = pd.read_csv(metadata_csv, index_col=0)

        # Smart alignment: counts columns are sample labels (e.g. WT_ACC_1) but
        # metadata is indexed by GSM IDs. If they don't intersect, try to map
        # GSM -> sample label by substring-matching the sample label inside any
        # metadata cell of that row.
        counts_cols = counts_df.columns.tolist()
        meta_index = metadata_df.index.tolist()

        exact_n = len(set(counts_cols).intersection(set(meta_index)))
        exact_required = max(1, (min(len(counts_cols), len(meta_index)) + 1) // 2)
        if exact_n < exact_required:
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

        # PyDESeq2 requires rows = samples, columns = genes; GEO files are usually transposed.
        counts_df = counts_df.T

        common_samples = counts_df.index.intersection(metadata_df.index)
        if len(common_samples) == 0:
            return "Error: no matching samples found after alignment."

        counts_df = counts_df.loc[common_samples]
        metadata_df = metadata_df.loc[common_samples]

        metadata_df, group_stats = select_valid_two_group_design(
            metadata_df, design_column=design_column, control_group=control_group,
            treatment_group=treatment_group, available_samples=counts_df.index,
        )
        print(f"Sample distribution after filtering:\n{group_stats}")

        counts_df = counts_df.loc[metadata_df.index]
        enforce_method_matrix_compatibility(counts_df, method="deseq2")

        multifactor_plan = None
        if interaction_terms.strip():
            return ("POLICY BLOCKED: DESeq2 interaction terms require an explicit interaction contrast; "
                    "use limma with coefficient='Treatment:...' or provide a precomputed contrast vector.")
        if covariate_columns.strip():
            covs = [x.strip() for x in covariate_columns.split(",") if x.strip()]
            try:
                multifactor_plan = build_multifactor_plan(
                    metadata_df,
                    primary_factor=design_column,
                    control=str(control_group),
                    treatment=str(treatment_group),
                    covariates=covs,
                )
            except PolicyViolation as exc:
                return f"POLICY BLOCKED: multifactor design validation failed: {exc}"

        # Drop genes with zero counts across all samples; PyDESeq2 needs integer counts.
        counts_df = counts_df.loc[:, (counts_df != 0).any(axis=0)]
        counts_df = counts_df.astype(int)

        # pydeseq2 builds a patsy formula `~ <design_factor>` from the column NAME, which breaks
        # when a GEO metadata column has spaces/slashes (e.g. 'characteristics_ch1.2.running protocole'
        # -> "Missing operator"). Rename the design column to a safe identifier for the model; the
        # factor VALUES (control/treatment) are unaffected and stay as-is in the contrast.
        safe_col = "design_factor"
        rename_map = {design_column: safe_col}
        if multifactor_plan is not None:
            for original, safe in multifactor_plan.safe_columns.items():
                if original != design_column:
                    rename_map[original] = safe
        metadata_df = metadata_df.rename(columns=rename_map)
        # Recode the levels so the control sorts first: pydeseq2 takes the alphabetically first
        # level as reference (ref_level is ignored with design_factors), and lfc_shrink can only
        # shrink a model coefficient, so treatment-vs-control must be one. A C(..., contr.treatment)
        # formula would set the reference too but shrinks every LFC to 0 once a covariate is added.
        others = sorted({str(v) for v in metadata_df[safe_col]} - {str(control_group), str(treatment_group)})
        level_codes = {str(control_group): "A_control", str(treatment_group): "B_treatment"}
        level_codes.update({v: f"C_other{i}" for i, v in enumerate(others)})
        metadata_df[safe_col] = metadata_df[safe_col].astype(str).map(level_codes)

        print(f"Running DESeq2 on {len(counts_df.index)} samples and {len(counts_df.columns)} genes...")

        design_factors = [safe_col]
        if multifactor_plan is not None:
            design_factors.extend(
                multifactor_plan.safe_columns[col]
                for col in multifactor_plan.covariates
            )
        dds = DeseqDataSet(
            counts=counts_df,
            metadata=metadata_df,
            design_factors=design_factors,
            refit_cooks=True,
            n_cpus=8,
        )
        dds.deseq2()

        stat_res = DeseqStats(
            dds,
            contrast=(safe_col, "B_treatment", "A_control"),
            alpha=alpha,
            n_cpus=8,
        )
        stat_res.summary()

        # log2FoldChange stays the MLE so every DA method writes the same quantity; the apeglm
        # shrunken estimate (what DESeq2 papers usually threshold on) goes in its own columns.
        # Shrinkage leaves stat/pvalue/padj unchanged.
        res_df = stat_res.results_df.copy()
        shrink_note = ""
        coeff = f"{safe_col}[T.B_treatment]"
        try:
            stat_res.lfc_shrink(coeff=coeff)
            res_df["log2FoldChange_shrunk"] = stat_res.results_df["log2FoldChange"]
            res_df["lfcSE_shrunk"] = stat_res.results_df["lfcSE"]
        except Exception as e:  # keep the MLE results rather than failing the run
            shrink_note = f"\nLFC shrinkage skipped ({type(e).__name__}: {e})."
            print(shrink_note.strip())
        res_df = res_df.sort_values("padj")

        output_file = os.path.join(output_dir, deg_filename(treatment_group, control_group))
        res_df.to_csv(output_file)

        sig_genes = res_df[res_df["padj"] < 0.05]
        up_regulated = sig_genes[sig_genes["log2FoldChange"] > 1]
        down_regulated = sig_genes[sig_genes["log2FoldChange"] < -1]

        summary = (f"DESeq2 analysis completed successfully!\n"
                   f"Results saved to: {output_file}\n"
                   f"Summary (padj < 0.05, |log2FC| > 1):\n"
                   f"- Up-regulated genes: {len(up_regulated)}\n"
                   f"- Down-regulated genes: {len(down_regulated)}")
        if "log2FoldChange_shrunk" in res_df:
            shrunk = sig_genes["log2FoldChange_shrunk"]
            summary += (f"\nWith apeglm-shrunken log2FC (column log2FoldChange_shrunk), |log2FC| > 1: "
                        f"{int((shrunk > 1).sum())} up, {int((shrunk < -1).sum())} down.")
        return summary + shrink_note

    except PolicyViolation as e:
        return f"POLICY BLOCKED: {e}"
    except Exception as e:
        print(f"Tool Error: {str(e)}")
        return f"DESeq2 analysis failed. Error: {str(e)}"


@tool
def inspect_metadata(metadata_csv: str) -> str:
    """
    Inspect the metadata CSV to find the correct column name and group names for DESeq2.
    It returns the column names and the unique values of potential grouping columns (like 'characteristics' or 'title').
    """
    try:
        df = pd.read_csv(metadata_csv, index_col=0)

        potential_columns = [
            col for col in df.columns
            if any(keyword in col.lower() for keyword in ["title", "characteristics", "source", "treatment", "disease"])
        ]

        inspection_result = "Here are the potential design columns and their unique values:\n"
        for col in potential_columns:
            unique_values = df[col].dropna().unique()
            # Skip columns with too many unique values; they are likely per-sample free text, not grouping labels.
            if 1 < len(unique_values) <= 10:
                inspection_result += f"- Column: '{col}' | Unique values: {list(unique_values)}\n"

        if inspection_result == "Here are the potential design columns and their unique values:\n":
            return f"No obvious grouping columns found. All columns: {list(df.columns)}"

        return inspection_result
    except Exception as e:
        return f"Failed to inspect metadata: {str(e)}"
