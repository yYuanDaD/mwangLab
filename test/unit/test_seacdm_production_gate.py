import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load(name, relative):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


PREP = load(
    "seacdm_production_gate_prepare",
    "test/experiments/seacdm_production_gate/prepare_manifest.py",
)
RUN = load(
    "seacdm_production_gate_run",
    "test/experiments/seacdm_production_gate/run_experiment.py",
)


class ProductionGateTests(unittest.TestCase):
    def test_wilson_interval(self):
        low, high = RUN._wilson(27, 30)
        self.assertLess(low, 0.9)
        self.assertGreater(high, 0.9)
        self.assertIsNone(RUN._wilson(0, 0))

    def test_case_labels_cover_scope_and_complexity(self):
        labels = PREP._labels(
            ["GSE1", "GSE2"],
            {"viable_axis_columns": 3, "max_levels": 5, "exercise_required": False},
        )
        self.assertEqual(
            labels, ["multi_accession", "complex_metadata", "target_no_exercise"]
        )

    def test_balanced_selection_is_deterministic(self):
        cases = [
            {"study_id": f"GSE{i}", "search_index": i,
             "source_accessions": ["GSE1", "GSE2"] if i % 2 else ["GSE1"],
             "metadata_profile": {
                 "exercise_required": i % 5 != 0,
                 "viable_axis_columns": i % 4,
             },
             "case_labels": ["multi_accession"] if i % 2 else ["routine_single"]}
            for i in range(1, 41)
        ]
        first = PREP._select_balanced(cases, 30)
        second = PREP._select_balanced(cases, 30)
        self.assertEqual([row["study_id"] for row in first],
                         [row["study_id"] for row in second])
        self.assertEqual(len(first), 30)

    def test_record_path_is_repeat_isolated(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = RUN._record_path(Path(tmp), "GSE123", 2)
        self.assertTrue(str(path).endswith("GSE123\\r2\\trace.json") or
                        str(path).endswith("GSE123/r2/trace.json"))

    def test_optional_findings_warning_is_not_a_critical_stage_error(self):
        errors = {
            "findings_chunk_1": "completion gate failed",
            "design": "schema parse failed",
        }
        critical = {
            key: value for key, value in errors.items()
            if not key.startswith("findings_chunk_")
        }
        self.assertEqual(critical, {"design": "schema parse failed"})

    def test_provider_balance_error_is_operationally_blocked(self):
        record = {
            "critical_stage_errors": {
                "study": "APIStatusError: Error code: 402 - Insufficient Balance"
            }
        }
        self.assertTrue(RUN._provider_blocked(record))
        self.assertFalse(RUN._provider_blocked({"critical_stage_errors": {}}))


if __name__ == "__main__":
    unittest.main()
