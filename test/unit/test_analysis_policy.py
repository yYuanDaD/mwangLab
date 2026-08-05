"""Deterministic tests for scientific rules that must not depend on an LLM prompt."""

import numpy as np
import pandas as pd
import unittest

from tools.analysis_policy import (
    PolicyViolation,
    enforce_method_matrix_compatibility,
    numeric_matrix,
    select_valid_two_group_design,
)


class AnalysisPolicyTests(unittest.TestCase):
    def test_raw_methods_reject_fractional_matrix(self):
        df = pd.DataFrame([[1.2, 3.4], [0.1, 5.7]], columns=["S1", "S2"])
        with self.assertRaisesRegex(PolicyViolation, "raw integer counts"):
            enforce_method_matrix_compatibility(df, method="deseq2")

    def test_limma_rejects_obvious_raw_counts(self):
        df = pd.DataFrame([[0, 500], [20, 10000]], columns=["S1", "S2"])
        with self.assertRaisesRegex(PolicyViolation, "raw-count-like"):
            enforce_method_matrix_compatibility(df, method="limma")

    def test_numeric_matrix_drops_annotations(self):
        df = pd.DataFrame({"symbol": ["A", "B"], "S1": [1, 2], "S2": [3, 4]})
        out = numeric_matrix(df, label="counts")
        self.assertEqual(list(out.columns), ["S1", "S2"])

    def test_design_requires_replication_in_each_arm(self):
        meta = pd.DataFrame({"group": ["ctrl", "treat", "treat"]}, index=["S1", "S2", "S3"])
        with self.assertRaisesRegex(PolicyViolation, "biological replicates"):
            select_valid_two_group_design(
                meta, design_column="group", control_group="ctrl", treatment_group="treat",
                available_samples=["S1", "S2", "S3"],
            )

    def test_valid_design_is_aligned_and_two_group(self):
        meta = pd.DataFrame(
            {"group": ["ctrl", "ctrl", "treat", "treat", "other"]},
            index=["C1", "C2", "T1", "T2", "X1"],
        )
        selected, counts = select_valid_two_group_design(
            meta, design_column="group", control_group="ctrl", treatment_group="treat",
            available_samples=["C1", "C2", "T1", "T2"],
        )
        self.assertEqual(list(selected.index), ["C1", "C2", "T1", "T2"])
        self.assertEqual(counts.to_dict(), {"ctrl": 2, "treat": 2})

    def test_design_rejects_biased_low_coverage_alignment(self):
        samples = [f"C{i}" for i in range(10)] + [f"T{i}" for i in range(10)]
        meta = pd.DataFrame({"group": ["ctrl"] * 10 + ["treat"] * 10}, index=samples)
        with self.assertRaisesRegex(PolicyViolation, "coverage"):
            select_valid_two_group_design(
                meta, design_column="group", control_group="ctrl", treatment_group="treat",
                available_samples=["C0", "C1", "T0", "T1"],
            )


if __name__ == "__main__":
    unittest.main()
