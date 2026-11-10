"""Helpers shared by the differential-analysis tools (pandas and numpy only).

Kept out of ``deseq2_tools`` so that limma, edgeR, limma-voom, the multigroup
executor, and single-cell routes do not need pydeseq2 just to import.
"""

import re

import numpy as np
import pandas as pd

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


def tmm_factors(counts: pd.DataFrame, logratio_trim: float = 0.3, sum_trim: float = 0.05) -> pd.Series:
    """edgeR TMM normalisation factors (``calcNormFactors(method="TMM")``) for a genes x
    samples count matrix, scaled to a geometric mean of 1.

    inmoose's edgepy has no ``calcNormFactors``; without TMM a composition shift between
    groups (about 0.27 log2 in GSE208639 disease vs control) inflates the DEG count.
    The reference sample is the one whose upper-quartile proportion is closest to the mean,
    as in edgeR; each factor is the precision-weighted mean of the trimmed log ratios.
    """
    x = counts.astype(float)
    x = x.loc[(x > 0).any(axis=1)]
    lib = x.sum(axis=0)
    f75 = (x / lib).quantile(0.75)
    if f75.median() < 1e-20:
        ref = np.sqrt(x).sum(axis=0).idxmax()
    else:
        ref = (f75 - f75.mean()).abs().idxmin()
    r = x[ref]
    n_r = lib[ref]
    factors = {}
    with np.errstate(divide="ignore", invalid="ignore"):
        for col in x.columns:
            o = x[col]
            n_o = lib[col]
            log_r = np.log2((o / n_o) / (r / n_r))
            abs_e = (np.log2(o / n_o) + np.log2(r / n_r)) / 2
            v = (n_o - o) / n_o / o + (n_r - r) / n_r / r
            fin = np.isfinite(log_r) & np.isfinite(abs_e)
            log_r, abs_e, v = log_r[fin], abs_e[fin], v[fin]
            if len(log_r) == 0 or log_r.abs().max() < 1e-6:
                factors[col] = 1.0
                continue
            n = len(log_r)
            lo_l = np.floor(n * logratio_trim) + 1
            hi_l = n + 1 - lo_l
            lo_s = np.floor(n * sum_trim) + 1
            hi_s = n + 1 - lo_s
            rk_r = log_r.rank(method="average")
            rk_e = abs_e.rank(method="average")
            keep = (rk_r >= lo_l) & (rk_r <= hi_l) & (rk_e >= lo_s) & (rk_e <= hi_s)
            f = (log_r[keep] / v[keep]).sum() / (1 / v[keep]).sum()
            factors[col] = float(2 ** (0.0 if not np.isfinite(f) else f))
    out = pd.Series(factors)[counts.columns]
    return out / np.exp(np.log(out).mean())


def limma_standard_error(top: pd.DataFrame) -> pd.DataFrame:
    """Replace inmoose's ``lfcSE`` with the moderated standard error, ``|logFC / t|``.

    inmoose's topTable fills ``lfcSE`` with the unscaled coefficient SD (sqrt(1/n1 + 1/n2)),
    the same constant for every gene; limma's moderated SE is sqrt(s2.post) times that.
    """
    top = top.copy()
    if {"log2FoldChange", "stat"} <= set(top.columns):
        with np.errstate(divide="ignore", invalid="ignore"):
            top["lfcSE"] = (top["log2FoldChange"] / top["stat"]).abs()
    return top
