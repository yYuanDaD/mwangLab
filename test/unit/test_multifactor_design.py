"""Tests for explicit multifactor design validation."""

import unittest

import pandas as pd

from tools.analysis_policy import PolicyViolation
from tools.multifactor_design import build_multifactor_plan, candidate_covariates


def _metadata():
    return pd.DataFrame(
        {
            "condition": ["ctrl", "ctrl", "ctrl", "ctrl", "treat", "treat", "treat", "treat"],
            "batch": ["b1", "b2", "b1", "b2", "b1", "b2", "b1", "b2"],
            "sex": ["F", "F", "M", "M", "F", "M", "F", "M"],
            "irrelevant": ["x"] * 8,
        },
        index=[f"S{i}" for i in range(8)],
    )


class MultifactorDesignTests(unittest.TestCase):
    def test_balanced_additive_plan_has_residual_df(self):
        plan = build_multifactor_plan(
            _metadata(),
            primary_factor="condition",
            control="ctrl",
            treatment="treat",
            covariates=["batch", "sex"],
        )
        self.assertEqual(plan.covariates, ("batch", "sex"))
        self.assertEqual(plan.n_control, 4)
        self.assertEqual(plan.n_treatment, 4)
        self.assertGreaterEqual(plan.residual_df, 1)
        self.assertIn("C(Covariate0)", plan.formula)

    def test_complete_confounding_is_blocked(self):
        metadata = _metadata()
        metadata["batch"] = ["b1"] * 4 + ["b2"] * 4
        with self.assertRaisesRegex(PolicyViolation, "rank deficient"):
            build_multifactor_plan(
                metadata,
                primary_factor="condition",
                control="ctrl",
                treatment="treat",
                covariates=["batch"],
            )

    def test_candidate_covariates_are_review_only(self):
        candidates = candidate_covariates(_metadata(), "condition")
        self.assertEqual(candidates, ["batch", "sex"])
        self.assertNotIn("irrelevant", candidates)

    def test_interaction_is_validated(self):
        plan = build_multifactor_plan(
            _metadata(),
            primary_factor="condition",
            control="ctrl",
            treatment="treat",
            covariates=["batch"],
            interactions=[("condition", "batch")],
        )
        self.assertEqual(plan.interactions, (("condition", "batch"),))
        self.assertIn("Treatment:C(Covariate0)", plan.formula)

    def test_missing_covariate_is_blocked(self):
        metadata = _metadata()
        metadata.loc["S0", "batch"] = None
        with self.assertRaisesRegex(PolicyViolation, "missing values"):
            build_multifactor_plan(
                metadata,
                primary_factor="condition",
                control="ctrl",
                treatment="treat",
                covariates=["batch"],
            )


if __name__ == "__main__":
    unittest.main()
