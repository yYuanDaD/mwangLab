"""inmoose eBayes fails with KeyError -2 when squeezeVar returns a scalar infinite df_prior.

tools.limma_compat broadcasts the scalar to one value per feature. This test
checks the wrapper without inmoose, and the full eBayes path when inmoose is
installed.
"""
import os
import sys

import numpy as np
import pandas as pd

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

from tools.limma_compat import _vector_df_prior  # noqa: E402


def test_scalar_infinite_df_prior_becomes_vector():
    def fake_squeeze(var, df, **kwargs):
        return {"df_prior": float("inf"), "var_prior": 1.0, "var_post": np.asarray(var)}

    out = _vector_df_prior(fake_squeeze)(np.ones(5), np.full(5, 4.0))
    assert isinstance(out["df_prior"], np.ndarray)
    assert out["df_prior"].shape == (5,)
    assert np.all(np.isinf(out["df_prior"]))
    assert not isinstance(out["df_prior"] > 1e6, bool)


def test_vector_df_prior_is_unchanged():
    vector = np.array([3.0, 4.0])

    def fake_squeeze(var, df, **kwargs):
        return {"df_prior": vector}

    assert _vector_df_prior(fake_squeeze)(np.ones(2), np.ones(2))["df_prior"] is vector


def test_ebayes_with_homoscedastic_data():
    try:
        from inmoose.limma import lmFit, topTable
        from patsy import dmatrix
    except ImportError:
        print("SKIP: inmoose or patsy not installed")
        return
    from tools.limma_compat import ebayes

    rng = np.random.default_rng(0)
    n_genes, n = 300, 4
    effect = np.zeros(n_genes)
    effect[:20] = 1.0
    cols, groups = {}, []
    for i in range(2 * n):
        trt = i >= n
        cols[f"s{i}"] = 8 + trt * effect + rng.normal(0, 0.25, n_genes)
        groups.append(int(trt))
    expr = pd.DataFrame(cols, index=[f"g{i}" for i in range(n_genes)])
    design = dmatrix("~ Treatment", pd.DataFrame({"Treatment": groups}, index=expr.columns))
    top = pd.DataFrame(topTable(ebayes(lmFit(expr, design=design)), coef="Treatment",
                                number=n_genes, sort_by="P", adjust_method="fdr_bh"))
    assert set(top.index[:20]) == {f"g{i}" for i in range(20)}


if __name__ == "__main__":
    test_scalar_infinite_df_prior_becomes_vector()
    test_vector_df_prior_is_unchanged()
    test_ebayes_with_homoscedastic_data()
    print("OK")
