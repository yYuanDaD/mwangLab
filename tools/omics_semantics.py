"""Deterministic helpers for transcript/gene aggregation and count-column selection.

These helpers deliberately fail closed when the input does not contain enough metadata to
identify a true count column.  They are used by the paper-aware benchmark tests and can be
integrated by callers before statistical modelling.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class CountColumnDecision:
    column: str | None
    confidence: str
    reason: str


_COUNT_HINTS = ("count", "counts", "read", "reads", "featurecount", "raw")
_NONCOUNT_HINTS = ("length", "start", "end", "strand", "fpkm", "tpm", "rpkm", "coverage", "score")


def choose_count_column(df: pd.DataFrame, sample_columns: list[str] | None = None) -> CountColumnDecision:
    """Choose a count column using headers and values, or return an explicit ambiguity.

    ``sample_columns`` should be supplied when a per-sample file is being parsed.  A single
    numeric column is accepted; multiple numeric columns require a count-like header and a
    unique winner.  No positional/rightmost fallback is used.
    """
    cols = list(sample_columns or df.columns)
    numeric = [c for c in cols if c in df and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric:
        return CountColumnDecision(None, "none", "no numeric candidate column")
    scored = []
    for c in numeric:
        name = str(c).lower()
        score = sum(2 for h in _COUNT_HINTS if h in name)
        score -= sum(3 for h in _NONCOUNT_HINTS if h in name)
        vals = pd.to_numeric(df[c], errors="coerce").dropna()
        if len(vals) and (vals >= 0).all() and (vals.round() == vals).mean() >= 0.95:
            score += 1
        scored.append((score, str(c)))
    scored.sort(reverse=True)
    if len(scored) == 1:
        return CountColumnDecision(scored[0][1], "high", "only numeric candidate")
    if scored[0][0] <= 0 or scored[0][0] == scored[1][0]:
        return CountColumnDecision(None, "ambiguous", f"numeric candidates: {[c for _, c in scored]}")
    return CountColumnDecision(scored[0][1], "medium", f"header/value score; candidates: {[c for _, c in scored]}")


def aggregate_transcripts_to_genes(counts: pd.DataFrame, transcript_to_gene: pd.Series,
                                   method: str = "sum") -> pd.DataFrame:
    """Aggregate transcript rows to gene rows with a validated transcript→gene mapping."""
    if method not in {"sum", "mean", "max"}:
        raise ValueError("method must be sum, mean, or max")
    mapping = transcript_to_gene.astype("string").str.strip()
    if len(mapping) != len(counts):
        raise ValueError("transcript_to_gene length must equal count rows")
    valid = mapping.notna() & mapping.ne("") & mapping.ne("<NA>")
    numeric = counts.apply(pd.to_numeric, errors="coerce")
    valid_mask = valid.to_numpy()
    numeric = numeric.iloc[valid_mask].copy()
    numeric.index = mapping.iloc[valid_mask].astype(str).to_numpy()
    if method == "sum":
        return numeric.groupby(level=0, sort=False).sum()
    if method == "mean":
        return numeric.groupby(level=0, sort=False).mean()
    return numeric.groupby(level=0, sort=False).max()
