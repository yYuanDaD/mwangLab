"""Regression tests for replayable LLM decision provenance."""

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools.batch_tools import _DecisionLog


class DecisionLogLLMTests(unittest.TestCase):
    def test_llm_decision_preserves_provider_confidence_and_inputs(self):
        with tempfile.TemporaryDirectory() as tmp, patch(
                "tools.batch_tools.resolve_model_config",
                return_value=SimpleNamespace(provider="deepseek", model="deepseek-v4-pro")):
            log = _DecisionLog("GSETEST")
            log.record(
                "matrix_type_llm", "assessment", heuristic="fpkm_or_tpm",
                llm_type="log_transformed", confidence="high",
                reason="values are signed log-scale measurements",
                input_stats={"min": -3.2, "max": 8.1},
                input_preview="gene S1 S2",
            )
            path = Path(tmp) / "decisions.json"
            log.save(str(path), status="ok")
            decisions = json.loads(path.read_text(encoding="utf-8"))
            evidence = json.loads((Path(tmp) / "evidence.json").read_text(encoding="utf-8"))

            decision = evidence["decisions"][0]
            source = next(source for source in evidence["sources"] if source["origin"] == "llm")
            self.assertEqual(decision["method"], "llm")
            self.assertEqual(decision["confidence"], 0.9)
            self.assertIn("deepseek:deepseek-v4-pro", source["label"])
            self.assertEqual(decision["details"]["input_stats"]["max"], 8.1)
            self.assertEqual(decisions["decisions"][0]["confidence"], "high")
            self.assertEqual(decisions["decisions"][0]["decision_id"], decision["decision_id"])

    def test_skips_and_unavailability_are_not_attributed_to_llm(self):
        self.assertEqual(_DecisionLog._method("llm_contrast_validation", "skipped_explicit_plan")[0], "user")
        self.assertEqual(_DecisionLog._method("llm_contrast_validation", "skipped_python_confident")[0], "rule")
        self.assertEqual(_DecisionLog._method("matrix_type_llm", "unavailable_blocked")[0], "rule")


if __name__ == "__main__":
    unittest.main()
