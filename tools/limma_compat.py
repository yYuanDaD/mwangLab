"""Workarounds for inmoose.limma.

inmoose 0.9.x eBayes fails with ``KeyError: -2`` when every feature has about
the same residual variance. squeezeVar then returns ``df_prior = inf`` as a
plain Python float, so ``Infdf = df_prior > 1e6`` is the Python bool ``True``
and ``~Infdf`` evaluates to ``-2``, which eBayes uses as a column key while
computing the B-statistic. R limma handles an infinite prior df normally.

``ebayes`` broadcasts a scalar ``df_prior`` to one value per feature before
eBayes uses it. The moderated t, p-values, and B-statistic are unchanged; only
the type of ``df_prior`` differs (R limma also returns a vector when
``robust=TRUE``).
"""
from __future__ import annotations

import numpy as np


def _vector_df_prior(squeeze_var):
    def wrapped(var, df, *args, **kwargs):
        out = squeeze_var(var, df, *args, **kwargs)
        df_prior = out.get("df_prior")
        if df_prior is not None and np.ndim(df_prior) == 0:
            out["df_prior"] = np.full(np.shape(var)[0], float(df_prior))
        return out

    wrapped.__wrapped__ = squeeze_var
    return wrapped


def ebayes(fit, **kwargs):
    """inmoose ``eBayes`` with the infinite-prior-df fix applied."""
    import importlib

    ebayes_module = importlib.import_module("inmoose.limma.ebayes")
    eBayes = ebayes_module.eBayes

    original = ebayes_module.squeezeVar
    ebayes_module.squeezeVar = _vector_df_prior(original)
    try:
        return eBayes(fit, **kwargs)
    finally:
        ebayes_module.squeezeVar = original
