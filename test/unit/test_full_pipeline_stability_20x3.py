"""Deterministic tests for the 20 x 3 stability experiment harness."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


PREPARE = _load(
    "stability_prepare",
    ROOT / "test" / "experiments" / "full_pipeline_stability_20x3" / "prepare_manifest.py",
)
RUN = _load(
    "stability_run",
    ROOT / "test" / "experiments" / "full_pipeline_stability_20x3" / "run_experiment.py",
)


class FullPipelineStabilityTests(unittest.TestCase):
    def test_case_bank_has_twenty_and_three_matrix_scales(self):
        self.assertEqual(len(PREPARE.CASE_SPECS), 20)
        counts = {
            kind: sum(case["expected_matrix_type"] == kind for case in PREPARE.CASE_SPECS)
            for kind in ("raw_counts", "fpkm_or_tpm", "log_transformed")
        }
        self.assertEqual(counts, {"raw_counts": 12, "fpkm_or_tpm": 5, "log_transformed": 3})
        self.assertEqual(
            sum(case.get("expected_alignment_prefix") == "llm" for case in PREPARE.CASE_SPECS),
            3,
        )

    def test_budget_plan_is_below_hard_cap_with_peak_contingency(self):
        regular = RUN.EXPECTED_CALLS_PER_REPEAT * 3 * RUN.REGULAR_ESTIMATE_PER_CALL_USD
        peak = regular * RUN.PEAK_MULTIPLIER
        self.assertAlmostEqual(regular, 0.126, places=6)
        self.assertAlmostEqual(peak, 0.252, places=6)
        self.assertLess(peak, RUN.DEFAULT_BUDGET_USD)

    def test_usage_merge_preserves_calls_tokens_and_cost(self):
        results = [
            {"usage": {"calls": [{"usage_measured": True, "input_tokens": 10,
                                    "cache_read_input_tokens": 5, "output_tokens": 2,
                                    "estimated_cost_usd": 0.001}]}},
            {"usage": {"calls": [{"usage_measured": True, "input_tokens": 20,
                                    "cache_read_input_tokens": 0, "output_tokens": 3,
                                    "estimated_cost_usd": 0.002}]}},
        ]
        merged = RUN._merge_usage(results)
        self.assertEqual(merged["llm_calls"], 2)
        self.assertEqual(merged["input_tokens"], 30)
        self.assertEqual(merged["output_tokens"], 5)
        self.assertAlmostEqual(merged["estimated_cost_usd"], 0.003)

    def test_identical_three_repeat_artifacts_pass_stability(self):
        with tempfile.TemporaryDirectory() as tmp:
            dirs = []
            for repeat in range(1, 4):
                case_dir = Path(tmp) / f"r{repeat}"
                case_dir.mkdir()
                pd.DataFrame({
                    "log2FoldChange": [2.0, -2.0, 0.2],
                    "padj": [0.01, 0.02, 0.8],
                }, index=["A", "B", "C"]).to_csv(case_dir / "DEG_results_T_vs_C.csv")
                pd.DataFrame({
                    "Term": ["P1", "P2", "P3"],
                    "NES": [2.1, -1.8, 0.2],
                    "FDR q-val": [0.01, 0.02, 0.9],
                }).to_csv(case_dir / "DEG_results_T_vs_C_GSEA_Hallmark.csv", index=False)
                dirs.append(case_dir)
            case = {"id": "TEST", "accession": "TEST", "expected_n_contrasts": 1}
            trials = [
                {"repeat": index, "passed": True, "case_dir": str(case_dir)}
                for index, case_dir in enumerate(dirs, 1)
            ]
            result = RUN.evaluate_case_stability(case, trials, 3)
            self.assertTrue(result["passed"], result)
            self.assertEqual(result["min_sig_deg_jaccard"], 1.0)
            self.assertEqual(result["min_sig_pathway_jaccard"], 1.0)


if __name__ == "__main__":
    unittest.main()