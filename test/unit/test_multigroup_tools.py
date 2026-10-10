"""Regression tests for the explicit multi-group executor."""

import os
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from tools.multigroup_tools import run_multigroup_analysis


class MultiGroupExecutorTests(unittest.TestCase):
    def _matrix_and_meta(self, n=20):
        rng = np.random.default_rng(7)
        cols = [f"S{i}" for i in range(n)]
        expr = pd.DataFrame(rng.normal(loc=5.0, scale=1.0, size=(120, n)),
                            index=[f"gene_{i}" for i in range(120)], columns=cols)
        # Numeric annotation columns must be ignored when all metadata samples
        # are covered (a common GEO processed-matrix layout).
        expr["length"] = 100
        meta = pd.DataFrame({"group": ["control"] * (n // 2) + ["treated"] * (n // 2)},
                            index=cols)
        return expr, meta

    def test_named_multilevel_contrasts_are_fitted(self):
        with tempfile.TemporaryDirectory() as td:
            expr, meta = self._matrix_and_meta()
            ep, mp = os.path.join(td, "expr.csv"), os.path.join(td, "meta.csv")
            expr.to_csv(ep)
            meta.to_csv(mp)
            fake = [{"name": "treated_vs_control", "path": os.path.join(td, "out.csv"),
                     "n_deg": 0, "formula": "~ 0 + C(group)", "design_rank": 2,
                     "residual_df": 6}]
            with patch("tools.multigroup_tools._fit_contrasts", return_value=fake):
                result = run_multigroup_analysis(ep, mp, {
                "analysis_type": "multilevel",
                "formula": "~ 0 + C(group)",
                "contrasts": [{"name": "treated_vs_control", "coefficients": {
                    "C(group)[treated]": 1, "C(group)[control]": -1,
                }}],
                }, os.path.join(td, "out"))
            self.assertEqual(result["n_contrasts"], 1)
            self.assertGreaterEqual(result["results"][0]["residual_df"], 1)

    def test_missing_metadata_sample_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            expr, meta = self._matrix_and_meta()
            ep, mp = os.path.join(td, "expr.csv"), os.path.join(td, "meta.csv")
            expr.to_csv(ep)
            meta.loc["missing_sample"] = {"group": "control"}
            meta.to_csv(mp)
            with self.assertRaises(ValueError):
                run_multigroup_analysis(ep, mp, {
                    "analysis_type": "multilevel",
                    "formula": "~ 0 + C(group)",
                    "contrasts": [{"name": "x", "coefficients": {
                        "C(group)[treated]": 1, "C(group)[control]": -1,
                    }}],
                }, os.path.join(td, "out"))


if __name__ == "__main__":
    unittest.main()
