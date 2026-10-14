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
