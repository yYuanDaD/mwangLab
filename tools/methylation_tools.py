"""Differential DNA-methylation DA (data-coverage roadmap P1) — the cheapest grid cell to fill
because it REUSES the existing limma backend.

Data-level rationale (for the non-bioinformatician): RRBS/WGBS/array methylation is, per CpG site,
a fraction methylated β ∈ [0, 1] (`.cov` files or a sites×samples β matrix). β is BOUNDED and
HETEROSCEDASTIC (variance shrinks near 0 and 1), which breaks limma's normal/homoscedastic
assumption. The standard fix (Du et al. 2010) is the **M-value = log2( β / (1−β) )**: it maps
[0,1] → (−∞,+∞) and is roughly homoscedastic — the recommended input for limma differential
methylation. We convert β→M then hand the matrix to `run_limma_analysis` (limma-trend) unchanged,
so the DEG output (log2FoldChange = ΔM, padj) is column-compatible with the RNA-seq/proteomics
path and downstream ORA/GSEA/agreement consume it without changes.

NOTE: output rows are differentially-methylated SITES (the matrix index). Mapping CpG→gene for
enrichment is a separate annotation step (out of scope here).
"""
import os
import numpy as np
import pandas as pd
from langchain_core.tools import tool

from tools.limma_tools import run_limma_analysis


def _beta_to_mvalue(df: pd.DataFrame, offset: float = 1e-3) -> pd.DataFrame:
    """β (in [0,1]) -> M = log2((β+offset)/(1-β+offset)). The offset (and a [offset,1-offset] clip)
    keeps log2 finite at β=0 / β=1. Non-numeric annotation columns are dropped first."""
    num = df.apply(pd.to_numeric, errors="coerce")
    num = num.loc[:, ~num.isna().all(axis=0)]              # drop all-non-numeric columns
    # if values look like percentages (0..100), scale to fractions
    finite = num.values[np.isfinite(num.values)]
    if finite.size and float(np.nanmax(finite)) > 1.5:
        num = num / 100.0
    b = num.clip(lower=offset, upper=1 - offset)
    return np.log2((b + offset) / (1 - b + offset))


def _looks_like_beta(df: pd.DataFrame) -> bool:
    """True if the numeric values look like methylation β/percent (mostly within [0,1] or [0,100])."""
    num = df.apply(pd.to_numeric, errors="coerce")
    vals = num.values[np.isfinite(num.values)]
    if vals.size == 0:
        return False
    mx = float(np.nanmax(vals))
    in01 = float(np.mean((vals >= -0.001) & (vals <= 1.001)))
    in0100 = float(np.mean((vals >= -0.1) & (vals <= 100.1)))
    return (mx <= 1.001 and in01 >= 0.9) or (mx <= 100.1 and in0100 >= 0.95 and mx > 1.5)


@tool
def run_methylation_da(beta_matrix_csv: str, metadata_csv: str, design_column: str,
                       control_group: str, treatment_group: str,
                       output_dir: str = "./output", beta_offset: float = 1e-3) -> str:
    """Differential DNA-methylation analysis from a β-value matrix (CpG sites × samples, values in
    [0,1] or 0-100%).

    Converts β to M-values (M = log2((β+ε)/(1-β+ε)) — the limma-recommended transform for bounded
    methylation β) and runs limma moderated-t + empirical Bayes via the shared limma backend. The
    output DEG CSV is column-compatible with run_deseq2_analysis (log2FoldChange = ΔM-value between
    groups, padj) so ORA/GSEA/agreement consume it unchanged.

    USE for RRBS / WGBS / methylation-array β matrices. DO NOT use for raw counts (DESeq2) or
    log-expression (run_limma_analysis directly).

    Args:
        beta_matrix_csv: β matrix CSV (rows = CpG sites/regions, cols = samples; values 0..1 or 0..100).
        metadata_csv: metadata with sample grouping (index = sample IDs).
        design_column: metadata column used as the design factor.
        control_group / treatment_group: the two values in design_column to contrast.
        output_dir: where the M-value matrix + DEG CSV are written.
        beta_offset: small ε to keep log2 finite at β=0/1 (default 1e-3).
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        df = pd.read_csv(beta_matrix_csv, index_col=0, sep=None, engine="python")
        if not _looks_like_beta(df):
            return ("Error: this matrix does not look like methylation β values (expected mostly "
                    "[0,1] or 0-100%). For raw counts use run_deseq2_analysis; for log-expression "
                    "use run_limma_analysis.")
        mvals = _beta_to_mvalue(df, offset=beta_offset)
        # Drop invariant / near-invariant CpG sites (standard methylation QC — sites that are
        # always ~0% or ~100% methylated carry no signal; also keeps limma's eBayes variance-trend
        # from degenerating on a block of near-constant features).
        sd = mvals.std(axis=1)
        keep = sd > 0.02
        n_dropped = int((~keep).sum())
        if n_dropped:
            print(f"   dropped {n_dropped} invariant/low-SD sites (M-value SD <= 0.02)")
        mvals = mvals.loc[keep]
        n_sites, n_samples = mvals.shape
        if n_sites < 50:
            return (f"Only {n_sites} variable sites after QC — too few for limma moderation. "
                    f"Check the β matrix (mostly invariant?).")
        base = os.path.splitext(os.path.basename(beta_matrix_csv))[0]
        mpath = os.path.join(output_dir, f"{base}_mvalues.csv")
        mvals.to_csv(mpath)
        print(f"Converted β -> M-values: {n_sites} sites x {n_samples} samples -> {mpath}")
        # reuse the limma backend exactly (M-values are log-scale; the DEG schema is identical)
        msg = run_limma_analysis.invoke({
            "normalized_csv": mpath, "metadata_csv": metadata_csv, "design_column": design_column,
            "control_group": control_group, "treatment_group": treatment_group, "output_dir": output_dir,
        })
        return (f"Differential methylation (β→M-value→limma) on {n_sites} sites.\n"
                f"M-value matrix: {mpath}\n"
                f"--- limma result ---\n{msg}")
    except Exception as e:
        return f"Methylation DA failed. Error: {type(e).__name__}: {e}"
