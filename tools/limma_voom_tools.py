"""limma-voom differential expression for RAW counts — backed by R's canonical limma::voom.

inmoose (the pure-Python limma/edgeR port used for run_limma_analysis / run_edger_analysis)
does NOT implement voom. Rather than hand-roll the voom precision-weight algorithm (and risk a
subtly-wrong reimplementation we can't validate against the reference), this tool calls R's
authoritative `limma::voom` via an Rscript subprocess (no rpy2 needed — just R on PATH).

Division of labour: Python does all the messy bits (read counts, drop annotation columns, the
sample-alignment cascade, group filtering, integer coercion) and writes two small temp CSVs;
the bundled tools/limma_voom.R runs voom -> lmFit -> eBayes -> topTable and writes a
DESeq2-compatible DEG CSV (log2FoldChange / padj / pvalue / stat) which we move into place.

Requires R with the `limma` Bioconductor package. If R/limma is unavailable the tool returns a
clear error (it does NOT crash the batch) — the caller can fall back to DESeq2 or edgeR.
"""

import os
import shutil
import subprocess
import tempfile

import numpy as np
import pandas as pd
from langchain_core.tools import tool

from tools.deseq2_tools import deg_filename, collapse_duplicate_genes

_R_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "limma_voom.R")


def _find_rscript() -> str:
    """Locate Rscript: PATH first, then the standard Windows install dir."""
    exe = shutil.which("Rscript") or shutil.which("Rscript.exe")
    if exe:
        return exe
    for base in (r"C:\Program Files\R", r"C:\Program Files\R\R-4.6.0\bin\x64"):
        if os.path.isdir(base):
            for root, _, files in os.walk(base):
                if "Rscript.exe" in files:
                    return os.path.join(root, "Rscript.exe")
    return ""


@tool
def run_limma_voom_analysis(
    counts_csv: str,
    metadata_csv: str,
    design_column: str,
    control_group: str,
    treatment_group: str,
    output_dir: str = "./output",
) -> str:
    """
    Run Differential Expression Analysis using limma-voom (R's canonical limma::voom +
    moderated t / empirical Bayes), for RAW integer counts.

    USE THIS TOOL for raw counts as an alternative to run_deseq2_analysis / run_edger_analysis.
    DO NOT use for log-scale matrices (CPM/FPKM/TPM/proteomics) — use run_limma_analysis there.
    Requires R with the `limma` package installed (calls Rscript under the hood).

    Args:
        counts_csv: Path to the raw counts CSV (rows=genes, cols=samples).
        metadata_csv: Path to the metadata CSV containing sample grouping (index=sample IDs).
        design_column: Metadata column to use as the design factor.
        control_group: Value in design_column for the control / baseline samples.
        treatment_group: Value in design_column for the treatment samples.
        output_dir: Directory to save the DEG CSV.
    """
    os.makedirs(output_dir, exist_ok=True)

    rscript = _find_rscript()
    if not rscript:
        return ("limma-voom unavailable: Rscript not found on this system. limma-voom needs R with the "
                "limma package. Use run_deseq2_analysis or run_edger_analysis for raw counts instead.")
    if not os.path.isfile(_R_SCRIPT):
        return f"limma-voom unavailable: bundled R script missing at {_R_SCRIPT}."

    try:
        print("Loading data for limma-voom analysis...")
        counts_df = pd.read_csv(counts_csv, index_col=0, sep=None, engine="python")
        metadata_df = pd.read_csv(metadata_csv, index_col=0)

        # Drop entirely non-numeric columns (annotation columns some GEO files mix in).
        coerced = counts_df.apply(pd.to_numeric, errors="coerce")
        non_numeric = coerced.columns[coerced.isna().all(axis=0)].tolist()
        if non_numeric:
            print(f"   Dropping {len(non_numeric)} non-numeric columns (likely annotations): {non_numeric}")
            counts_df = counts_df.drop(columns=non_numeric)
        counts_df = collapse_duplicate_genes(counts_df, "limma-voom")

        # Smart sample alignment (exact/substring/token-overlap/LLM) — same cascade as DESeq2/limma/edgeR.
        counts_cols = counts_df.columns.tolist()
        meta_index = metadata_df.index.tolist()
        if len(set(counts_cols).intersection(set(meta_index))) == 0:
            print("Sample names do not match between counts and metadata. Attempting smart alignment...")
            from tools.llm_helpers import align_samples_with_llm_fallback
            mapping, method = align_samples_with_llm_fallback(counts_cols, metadata_df)
            if not mapping:
                return ("FATAL ERROR: sample names could not be matched (exact/substring/token-overlap/llm "
                        "all failed). Counts columns and metadata likely use different naming conventions.")
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
                    f"All groups in metadata column '{design_column}': {all_available_groups}")

        common = [s for s in metadata_df.index if s in counts_df.columns]
        if len(common) < 4:
            return (f"FATAL ERROR: only {len(common)} samples remain after alignment + group filtering. "
                    f"limma-voom needs at least 2 samples per group (4 total).")
        metadata_df = metadata_df.loc[common]
        counts_sub = counts_df[common].round().astype(int)
        counts_sub = counts_sub.loc[(counts_sub != 0).any(axis=1)]
        n_genes, n_samples = counts_sub.shape
        print(f"Running limma-voom (R) on {n_samples} samples and {n_genes} genes...")

        # Hand counts + a {sample -> group} table to R via temp CSVs.
        tmpdir = tempfile.mkdtemp(prefix="voom_")
        counts_tmp = os.path.join(tmpdir, "counts.csv")
        groups_tmp = os.path.join(tmpdir, "groups.csv")
        out_tmp = os.path.join(tmpdir, "deg.csv")
        counts_sub.to_csv(counts_tmp)
        pd.DataFrame({"group": metadata_df[design_column].astype(str)}).to_csv(groups_tmp)

        proc = subprocess.run(
            [rscript, _R_SCRIPT, counts_tmp, groups_tmp, control_group, treatment_group, out_tmp],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600,
        )
        if proc.returncode != 0 or not os.path.isfile(out_tmp):
            tail = (proc.stderr or proc.stdout or "").strip()[-600:]
            return f"limma-voom (R) failed (exit {proc.returncode}). R said:\n{tail}"

        res = pd.read_csv(out_tmp, index_col=0)
        shutil.rmtree(tmpdir, ignore_errors=True)

        output_file = os.path.join(output_dir, deg_filename(treatment_group, control_group))
        res.to_csv(output_file)

        sig = res.dropna(subset=["padj", "log2FoldChange"])
        sig = sig[sig["padj"] < 0.05]
        up = sig[sig["log2FoldChange"] > 1]
        down = sig[sig["log2FoldChange"] < -1]

        return (f"limma-voom analysis completed successfully!\n"
                f"Results saved to: {output_file}\n"
                f"Summary (padj < 0.05, |log2FC| > 1):\n"
                f"- Up-regulated genes: {len(up)}\n"
                f"- Down-regulated genes: {len(down)}")

    except subprocess.TimeoutExpired:
        return "limma-voom (R) timed out after 600s."
    except Exception as e:
        print(f"Tool Error: {str(e)}")
        return f"limma-voom analysis failed. Error: {str(e)}"
