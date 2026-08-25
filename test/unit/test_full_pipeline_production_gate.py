"""Deterministic tests for the full-pipeline production-gate harness."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


PREPARE = _load(
    "full_pipeline_prepare",
    ROOT / "test" / "experiments" / "full_pipeline_production_gate" / "prepare_manifest.py",
)
RUN = _load(
    "full_pipeline_run",
    ROOT / "test" / "experiments" / "full_pipeline_production_gate" / "run_experiment.py",
)

from tools.batch_tools import _DecisionLog
from tools.llm_helpers import (
    SampleAlignmentResult,
    _invoke_structured,
    _llm_align_samples,
    estimate_llm_cost_usd,
    llm_usage_checkpoint,
    llm_usage_summary,
    reset_llm_alignment_cache,
    reset_llm_usage,
)


class FullPipelineProductionGateTests(unittest.TestCase):
    def test_case_bank_is_frozen_to_six_complementary_cases(self):
        self.assertEqual(len(PREPARE.CASE_SPECS), 6)
        matrix_types = {case["expected_matrix_type"] for case in PREPARE.CASE_SPECS}
        self.assertEqual(matrix_types, {"raw_counts", "fpkm_or_tpm", "log_transformed"})
        self.assertTrue(any(case.get("expected_alignment_prefix") == "llm"
                            for case in PREPARE.CASE_SPECS))
        self.assertTrue(any(len(case["expected_treatments"]) > 1
                            for case in PREPARE.CASE_SPECS))

    def test_policy_probes_all_reject_unsafe_inputs(self):
        probes = RUN.run_policy_probes()
        self.assertEqual(set(probes), {
            "deseq2_rejects_fractional",
            "limma_rejects_raw_counts",
            "underpowered_design_rejected",
        })
        self.assertTrue(all(probes.values()), probes)

    def test_method_compatibility_is_scale_aware(self):
        self.assertTrue(RUN._method_compatible("raw_counts", "deseq2"))
        self.assertTrue(RUN._method_compatible("fpkm_or_tpm", "limma"))
        self.assertTrue(RUN._method_compatible("log_transformed", "limma"))
        self.assertFalse(RUN._method_compatible("raw_counts", "limma"))
        self.assertFalse(RUN._method_compatible("fpkm_or_tpm", "deseq2"))

    def test_case_evaluator_requires_exact_treatment_set_and_artifacts(self):
        case = {
            "expected_matrix": "matrix.csv",
            "expected_matrix_type": "raw_counts",
            "expected_method": "deseq2",
            "expected_design": "condition",
            "expected_control": "control",
            "expected_treatments": ["exercise"],
            "expected_n_contrasts": 1,
        }
        row = {
            "counts_file": "GSETEST/matrix.csv",
            "matrix_type": "raw_counts",
            "da_method": "deseq2",
            "design_col": "condition",
            "control": "control",
            "n_contrasts": 1,
            "status": "deg_gsea_ok",
            "deg_sanity": "ok",
        }
        decisions = [
            {"step": "metadata_alignment", "decision": "exact_match",
             "details": {"verdict": "exact_match", "n_aligned": 6}},
            {"step": "deseq2", "decision": "ok",
             "details": {"control": "control", "treatment": "exercise"}},
            {"step": "gsea", "decision": "ok", "details": {}},
        ]
        artifacts = {"deg": 1, "gsea": 1, "qc": True, "decisions": True}
        result = RUN.evaluate_case(
            case, row, decisions, artifacts, hashes_match=True, run_terminal=True
        )
        self.assertTrue(result["passed"], result)
        decisions[1]["details"]["treatment"] = "wrong"
        result = RUN.evaluate_case(
            case, row, decisions, artifacts, hashes_match=True, run_terminal=True
        )
        self.assertFalse(result["passed"])
        self.assertIn("treatment_set", result["blocking"])


    def test_deepseek_v4_pro_cost_uses_public_token_rates(self):
        self.assertAlmostEqual(
            estimate_llm_cost_usd("deepseek", "deepseek-v4-pro", 1_000_000, 1_000_000),
            1.305,
            places=6,
        )
        self.assertAlmostEqual(
            estimate_llm_cost_usd(
                "deepseek", "deepseek-v4-pro", 1_000_000, 0, 500_000
            ),
            0.2193125,
            places=7,
        )

    def test_structured_usage_ledger_captures_raw_tokens(self):
        class FakeRunnable:
            def invoke(self, prompt):
                raw = SimpleNamespace(
                    usage_metadata={"input_tokens": 1000, "output_tokens": 200},
                    response_metadata={},
                )
                return {"raw": raw, "parsed": "ok", "parsing_error": None}

        class FakeLLM:
            def with_structured_output(self, schema, include_raw=False):
                self.include_raw = include_raw
                return FakeRunnable()

        reset_llm_usage()
        start = llm_usage_checkpoint()
        with patch.dict(os.environ, {
            "BIOAGENT_LLM_PROVIDER": "deepseek",
            "BIOAGENT_LLM_MODEL": "deepseek-v4-pro",
        }):
            self.assertEqual(_invoke_structured(FakeLLM(), object, "prompt", "test"), "ok")
        usage = llm_usage_summary(start)
        self.assertEqual(usage["llm_calls"], 1)
        self.assertEqual(usage["usage_measured_calls"], 1)
        self.assertEqual(usage["input_tokens"], 1000)
        self.assertEqual(usage["output_tokens"], 200)
        self.assertGreater(usage["estimated_cost_usd"], 0)
        reset_llm_usage()

    def test_semantic_alignment_cache_reuses_only_within_run(self):
        counts = ["HC_F1_TL", "RUN_F1_TL"]
        metadata = pd.DataFrame(
            {"title": ["HomeCage Female1 TotalLysate", "Run Female1 TotalLysate"]},
            index=["GSM1", "GSM2"],
        )
        expected = {"GSM1": counts[0], "GSM2": counts[1]}
        reset_llm_alignment_cache()
        result = SampleAlignmentResult(mapping=expected, reasoning="test mapping")
        with patch("tools.llm_helpers._get_validation_llm", return_value=object()), \
                patch("tools.llm_helpers._invoke_structured", return_value=result) as invoke:
            self.assertEqual(_llm_align_samples(counts, metadata), expected)
            self.assertEqual(_llm_align_samples(counts, metadata), expected)
            self.assertEqual(invoke.call_count, 1)
        reset_llm_alignment_cache()

    def test_decision_log_resolves_data_relative_artifact_and_hash(self):
        data_root = ROOT / "data"
        data_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=data_root) as tmp:
            artifact = Path(tmp) / "matrix.csv"
            artifact.write_text("gene,S1\nA,1\n", encoding="utf-8")
            relative = artifact.relative_to(data_root)
            dlog = _DecisionLog("GSETEST")
            dlog.record("counts_detection", "selected", counts_file=str(relative))
            recorded = dlog.evidence.bundle.artifacts[0]
            self.assertEqual(Path(recorded.path), artifact.resolve())
            self.assertIsNotNone(recorded.sha256)


if __name__ == "__main__":
    unittest.main()

