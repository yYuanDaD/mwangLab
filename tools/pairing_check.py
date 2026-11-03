"""Test whether a candidate key links samples from the same animal or person.

GEO often has no subject column even when the paper took several samples from each animal
(two fat depots, two muscles, pre and post). A replicate label can still carry the pairing,
but usually only together with the group: in GSE283493 the letters a-f repeat in every group,
so "letter" alone puts exercise and control rats together, while "group + letter" gives 24
rats with one SAT and one VAT library each.

The check: remove each stratum's mean (for example tissue x group), then correlate the
residual profiles of samples that sit in different levels of ``across`` (SAT vs VAT) within the
same ``within`` group. Samples from one animal share animal-level deviations, so if the key is
right, same-key pairs correlate more than other pairs. The p-value comes from shuffling the key
within each stratum. A clear difference supports the key; no difference does not disprove it
(animal effects can be small), so record the key as an assumption either way.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd


def check_pairing_key(log_expr: pd.DataFrame, meta: pd.DataFrame, key: Sequence[str], across: str,
                      within: Sequence[str] = (), *, min_mean: float = 3.0, n_perm: int = 5000,
                      seed: int = 0) -> dict:
    """Residual-correlation test of a candidate pairing key.

    log_expr: genes x samples on a log scale (log2 CPM); meta: indexed by sample.
    key: columns whose combination is the candidate animal ID (e.g. ["grp", "rep_letter"]).
    across: column whose levels the pairs span (e.g. "tissue").
    within: design columns that are constant inside an animal (e.g. ["grp"]); means are removed
        per ``across`` x ``within`` cell and pairs are only formed inside one ``within`` cell.
    """
    within = list(within)
    meta = meta.loc[[s for s in meta.index if s in log_expr.columns]].copy()
    expr = log_expr[meta.index]
    expr = expr.loc[expr.mean(axis=1) > min_mean]
    resid = expr.copy()
    for _, idx in meta.groupby([across, *within]).groups.items():
        resid[idx] = expr[idx].sub(expr[idx].mean(axis=1), axis=0)
    meta["_key"] = meta[list(key)].astype(str).agg("|".join, axis=1)
    blocks = []
    for _, g in (meta.groupby(within) if within else [(None, meta)]):
        levels = sorted(g[across].unique())
        for i, a in enumerate(levels):
            for b in levels[i + 1:]:
                ga, gb = g[g[across] == a], g[g[across] == b]
                if len(ga) and len(gb):
                    corr = np.corrcoef(resid[ga.index].T.values, resid[gb.index].T.values)[:len(ga), len(ga):]
                    blocks.append((np.asarray(ga["_key"], dtype=object), np.asarray(gb["_key"], dtype=object), corr))
    if not blocks:
        return {"status": "not_testable", "reason": f"no stratum has samples in two levels of {across}"}

    def diff(blocks_keys):
        same, other = [], []
        for (ka, kb, corr) in blocks_keys:
            eq = ka[:, None] == kb[None, :]
            same += list(corr[eq])
            other += list(corr[~eq])
        return (np.mean(same) - np.mean(other) if same and other else np.nan), same, other

    observed, same, other = diff(blocks)
    if not same:
        return {"status": "not_testable", "reason": "no key value occurs in two levels of " + across}
    rng = np.random.default_rng(seed)
    null = np.array([diff([(rng.permutation(ka), rng.permutation(kb), c) for ka, kb, c in blocks])[0]
                     for _ in range(n_perm)])
    p = float((np.sum(null >= observed) + 1) / (n_perm + 1))
    return {"key": list(key), "across": across, "within": within, "n_same_key_pairs": len(same),
            "same_key_mean_r": round(float(np.mean(same)), 3), "other_mean_r": round(float(np.mean(other)), 3),
            "difference": round(float(observed), 3), "permutation_p": p, "genes_used": int(len(resid)),
            "status": "supported" if p < 0.01 and observed > 0 else "not_supported"}
