"""Coverage invariants for deterministic sample alignment."""

import unittest
from unittest.mock import patch

import pandas as pd

from tools.sample_align import align_samples
from tools.llm_helpers import align_samples_with_llm_fallback


class SampleAlignPolicyTests(unittest.TestCase):
    def test_tiny_exact_intersection_does_not_short_circuit(self):
        meta = pd.DataFrame(
            {"title": ["S1", "sample S2 lane", "sample S3 lane", "sample S4 lane"]},
            index=["S1", "GSM2", "GSM3", "GSM4"],
        )
        mapping, method = align_samples(["S1", "S2", "S3", "S4"], meta)
        self.assertEqual(len(mapping), 4)
        self.assertTrue(method.startswith("substring"), method)

    def test_tiny_exact_intersection_alone_is_rejected(self):
        meta = pd.DataFrame({"title": ["unrelated"] * 4}, index=["S1", "M2", "M3", "M4"])
        mapping, method = align_samples(["S1", "S2", "S3", "S4"], meta)
        self.assertEqual(mapping, {})
        self.assertEqual(method, "no_match")

    def test_llm_tiny_proposal_does_not_define_its_own_denominator(self):
        cols = [f"C{i}" for i in range(20)]
        meta = pd.DataFrame({"title": [f"unrelated {i}" for i in range(20)]},
                            index=[f"M{i}" for i in range(20)])
        with patch("tools.llm_helpers._llm_align_samples", return_value={"M0": "C0", "M1": "C1"}):
            mapping, method = align_samples_with_llm_fallback(cols, meta)
        self.assertEqual(mapping, {})
        self.assertIn("required=10", method)

    def test_llm_can_match_metadata_subset_among_extra_numeric_columns(self):
        cols = [f"C{i}" for i in range(6)] + [f"stat{i}" for i in range(7)]
        meta = pd.DataFrame({"title": [f"unrelated {i}" for i in range(6)]},
                            index=[f"M{i}" for i in range(6)])
        proposed = {f"M{i}": f"C{i}" for i in range(6)}
        with patch("tools.llm_helpers._llm_align_samples", return_value=proposed):
            mapping, method = align_samples_with_llm_fallback(cols, meta)
        self.assertEqual(mapping, proposed)
        self.assertEqual(method, "llm (6/6)")


if __name__ == "__main__":
    unittest.main()
