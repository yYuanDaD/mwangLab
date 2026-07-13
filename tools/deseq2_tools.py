import os
import re
import numpy as np
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from langchain_core.tools import tool


_FNAME_BAD = re.compile(r'[<>:"/\\|?*\s]+')


def collapse_duplicate_genes(df: pd.DataFrame, label: str = "counts") -> pd.DataFrame:
    """Return df with a UNIQUE gene index. Real GEO matrices often index by gene symbol where
    several source IDs (Ensembl/probes) collapse to the same symbol -> duplicate rownames, which
    break DESeq2 (reindex error), limma (R read.csv), and silently confuse edgeR. We keep the
    highest-mean row per duplicated gene (MaxMean collapse — the most-expressed representative).
    No-op when the index is already unique."""
    if not df.index.has_duplicates:
        return df
    n_before = len(df)
    means = df.apply(pd.to_numeric, errors="coerce").mean(axis=1).fillna(-np.inf).to_numpy()
    order = np.argsort(-means, kind="stable")
    df2 = df.iloc[order]
    df2 = df2[~df2.index.duplicated(keep="first")]
    print(f"   Collapsed {n_before - len(df2)} duplicate gene IDs ({label}, kept highest-mean row).")
    return df2


def safe_for_filename(s: str) -> str:
    """Sanitize a metadata value (e.g. 'db/db (leptin receptor mutant)') for use
    in a filename. Replaces illegal Windows chars and whitespace with '_', then
    collapses repeats and strips leading/trailing '_'. Keeps parens/brackets/etc
    intact since they're legal on Windows."""
    cleaned = _FNAME_BAD.sub("_", str(s))
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "value"


def deg_filename(treatment: str, control: str) -> str:
    """Canonical DEG filename used by run_deseq2_analysis (writer) and
    batch_tools (reader). Both sides must use this helper to stay in sync."""
    return f"DEG_results_{safe_for_filename(treatment)}_vs_{safe_for_filename(control)}.csv"


@tool
def run_deseq2_analysis(
    counts_csv: str,
    metadata_csv: str,
    design_column: str,
    control_group: str,
    treatment_group: str,
    output_dir: str = "./output"
) -> str:
    """
    Run Differential Expression Analysis using PyDESeq2.

    Args:
        counts_csv: Path to the raw counts CSV file (must be unnormalized raw counts).
        metadata_csv: Path to the metadata CSV file containing sample grouping.
        design_column: The column name in metadata representing the experimental conditions (e.g., 'group').
        control_group: The specific value in the design_column representing the control/sham group.
        treatment_group: The specific value in the design_column representing the treatment/disease group.
        output_dir: Directory to save the final DEG results.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        print("Loading data for DESeq2 analysis...")
        counts_df = pd.read_csv(counts_csv, index_col=0, sep=None, engine="python")
        counts_df = collapse_duplicate_genes(counts_df, "DESeq2")
        metadata_df = pd.read_csv(metadata_csv, index_col=0)

        # Smart alignment: counts columns are sample labels (e.g. WT_ACC_1) but
        # metadata is indexed by GSM IDs. If they don't intersect, try to map
        # GSM -> sample label by substring-matching the sample label inside any
        # metadata cell of that row.
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

        # PyDESeq2 requires rows = samples, columns = genes; GEO files are usually transposed.
        counts_df = counts_df.T

        common_samples = counts_df.index.intersection(metadata_df.index)
        if len(common_samples) == 0:
            return "Error: no matching samples found after alignment."

        counts_df = counts_df.loc[common_samples]
        metadata_df = metadata_df.loc[common_samples]

        all_available_groups = metadata_df[design_column].unique().tolist()

        mask = metadata_df[design_column].isin([control_group, treatment_group])
        metadata_df = metadata_df[mask]

        group_stats = metadata_df[design_column].value_counts()
        print(f"Sample distribution after filtering:\n{group_stats}")

        if len(group_stats) < 2:
            return (f"FATAL ERROR: cannot run differential analysis. File {os.path.basename(counts_csv)} "
                    f"does not contain both '{control_group}' and '{treatment_group}'.\n"
                    f"Currently available groups: {group_stats.index.tolist()}\n"
                    f"All groups in metadata column '{design_column}': {all_available_groups}\n"
                    f"Suggestion: check that the correct counts file was selected and that the metadata column name matches.")

        counts_df = counts_df.loc[metadata_df.index]

        # Drop genes with zero counts across all samples; PyDESeq2 needs integer counts.
        counts_df = counts_df.loc[:, (counts_df != 0).any(axis=0)]
        counts_df = counts_df.round().astype(int)

        # pydeseq2 builds a patsy formula `~ <design_factor>` from the column NAME, which breaks
        # when a GEO metadata column has spaces/slashes (e.g. 'characteristics_ch1.2.running protocole'
        # -> "Missing operator"). Rename the design column to a safe identifier for the model; the
        # factor VALUES (control/treatment) are unaffected and stay as-is in the contrast.
        safe_col = "design_factor"
        metadata_df = metadata_df.rename(columns={design_column: safe_col})

        print(f"Running DESeq2 on {len(counts_df.index)} samples and {len(counts_df.columns)} genes...")

        dds = DeseqDataSet(
            counts=counts_df,
            metadata=metadata_df,
            design_factors=safe_col,
            refit_cooks=True,
            n_cpus=8,
        )
        dds.deseq2()

        stat_res = DeseqStats(
            dds,
            contrast=(safe_col, treatment_group, control_group),
            n_cpus=8,
        )
        stat_res.summary()

        res_df = stat_res.results_df
        res_df = res_df.sort_values("padj")

        output_file = os.path.join(output_dir, deg_filename(treatment_group, control_group))
        res_df.to_csv(output_file)

        sig_genes = res_df[res_df["padj"] < 0.05]
        up_regulated = sig_genes[sig_genes["log2FoldChange"] > 1]
        down_regulated = sig_genes[sig_genes["log2FoldChange"] < -1]

        return (f"DESeq2 analysis completed successfully!\n"
                f"Results saved to: {output_file}\n"
                f"Summary (padj < 0.05, |log2FC| > 1):\n"
                f"- Up-regulated genes: {len(up_regulated)}\n"
                f"- Down-regulated genes: {len(down_regulated)}")

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
