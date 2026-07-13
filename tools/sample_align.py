"""Shared sample-name alignment for counts <-> metadata.

GEO submissions are inconsistent about how counts matrix columns relate to
metadata sample IDs. This tries a cascade of strategies in order of specificity
and stops on the first one that matches at least `min_match_fraction` of the
counts columns. Used by deseq2_tools and stats_tools."""

import re

_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9]+|[0-9]+")


def _tokens(s):
    return set(t.lower() for t in _TOKEN_RE.findall(str(s)))


def align_samples(counts_cols, metadata_df, min_match_fraction: float = 0.5,
                  token_threshold: int = 3):
    """Find a mapping from metadata index -> counts column name.

    Strategies attempted in order:
      1. exact         - counts columns are literally a subset of metadata index
      2. substring     - the counts column name appears as substring within any
                         metadata row text (legacy behavior)
      3. token_overlap - the counts column and a metadata row share >= token_threshold
                         distinct alphanumeric tokens; greedy 1:1 assignment with
                         highest-overlap match wins per metadata row

    Returns (mapping, method_str). Mapping is empty + method='no_match' if no
    strategy reached min_match_fraction. NO position-based fallback — silently
    aligning by row order risks producing biologically wrong DESeq2 results when
    counts and metadata happen to be ordered differently.
    """
    counts_cols = list(counts_cols)
    n = len(counts_cols)
    if n == 0:
        return {}, "no_counts_cols"

    counts_set = set(counts_cols)
    meta_idx = [str(x) for x in metadata_df.index]

    # 1. Exact intersection
    common = counts_set & set(meta_idx)
    if common:
        return {c: c for c in common}, f"exact ({len(common)}/{n})"

    # 2. Substring (counts col appears in metadata row text)
    mapping = {}
    used = set()
    for idx, row in metadata_df.iterrows():
        row_text = " ".join(str(x) for x in row.values).lower()
        for col in counts_cols:
            if col in used:
                continue
            if col.lower() in row_text:
                mapping[idx] = col
                used.add(col)
                break
    if len(mapping) >= n * min_match_fraction:
        return mapping, f"substring ({len(mapping)}/{n})"

    # 3. Token overlap (greedy by max overlap per metadata row)
    col_tokens = {col: _tokens(col) for col in counts_cols}
    mapping = {}
    used = set()
    for idx, row in metadata_df.iterrows():
        row_tokens = set()
        for v in row.values:
            row_tokens |= _tokens(v)
        candidates = []
        for col, ct in col_tokens.items():
            if col in used:
                continue
            overlap = len(ct & row_tokens)
            if overlap >= token_threshold:
                candidates.append((overlap, col))
        if candidates:
            candidates.sort(reverse=True, key=lambda x: x[0])
            best_col = candidates[0][1]
            mapping[idx] = best_col
            used.add(best_col)
    if len(mapping) >= n * min_match_fraction:
        return mapping, f"token_overlap ({len(mapping)}/{n})"

    return {}, "no_match"
