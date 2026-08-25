import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.metadata_structural import build_structural_tables, summarize_geo_scope
from tools.seacdm_tools import (
    ExperimentInterventionExtraction,
    _extract_experiment_interventions,
)


ROOT = Path(__file__).resolve().parents[2]


class _CaptureRunnable:
    def __init__(self):
        self.prompt = ""

    def invoke(self, prompt):
        self.prompt = prompt
        return ExperimentInterventionExtraction()


class SeaCdmScopePolicyTests(unittest.TestCase):
    def _metadata(self, folder: str) -> str:
        path = Path(folder) / "GSEX_metadata.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow([
                "sample", "title", "source_name_ch1", "organism_ch1",
                "characteristics_ch1.0.training status",
                "characteristics_ch1.1.time point", "molecule_ch1", "type",
                "platform_id", "hyb_protocol", "data_processing",
            ])
            writer.writerow([
                "GSM1", "Muscle_baseline_untrained", "vastus lateralis, baseline",
                "Homo sapiens", "untrained", "baseline", "total RNA", "RNA",
                "GPL13667", "Affymetrix array hybridization", "RMA from CEL files",
            ])
            writer.writerow([
                "GSM2", "Muscle_30min_trained", "vastus lateralis, exercised, 60 min",
                "Homo sapiens", "trained", "+30min", "total RNA", "RNA",
                "GPL13667", "Affymetrix array hybridization", "RMA from CEL files",
            ])
        return str(path)

    def test_geo_scope_summary_is_compact_and_accession_specific(self):
        with tempfile.TemporaryDirectory() as folder:
            summary = summarize_geo_scope(self._metadata(folder))
        self.assertIn("GEO sample count: 2", summary)
        self.assertIn("baseline", summary)
        self.assertIn("+30min", summary)
        self.assertNotIn("8-week", summary)

    def test_microarray_is_not_mislabeled_as_sequencing(self):
        with tempfile.TemporaryDirectory() as folder:
            tables = build_structural_tables("GSEX", "GSEX_exp1", self._metadata(folder))
        self.assertEqual(tables["assay"][0]["assay_name"],
                         "microarray gene expression profiling")
        self.assertIn("hyb_protocol", tables["assay"][0]["assay_name_source"])

    def test_design_prompt_states_hard_geo_scope_boundary(self):
        capture = _CaptureRunnable()
        text = (
            "[TARGET GEO SCOPE]\nGEO sample count: 2\ntime point: baseline | +30min\n"
            "[END TARGET GEO SCOPE]\nPaper also reports an independent 8-week qPCR cohort."
        )
        with patch("tools.seacdm_tools._get_llm", return_value=object()), \
             patch("tools.seacdm_tools._structured_runnable", return_value=capture):
            _extract_experiment_interventions(text, "GSEX", "Human")
        self.assertIn("The extraction unit is the target GEO accession", capture.prompt)
        self.assertIn("Exclude independent validation cohorts", capture.prompt)
        self.assertIn("trained", capture.prompt)

    def test_evaluator_accepts_geo_scope_and_rejects_cross_cohort_merge(self):
        runner_path = (
            ROOT / "test" / "experiments" / "deepseek_seacdm_generalization" /
            "run_experiment.py"
        )
        spec = importlib.util.spec_from_file_location("scope_eval_runner", runner_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        case = module.CASES["multifactor"]
        correct = {
            "experiment": [{"experiment_type": "acute exercise microarray"}],
            "interventions": [{"material": "60 min cycling at 80% VO2max"}],
            "assay": [{"assay_name": "Affymetrix U219 microarray"}],
        }
        merged = {
            **correct,
            "interventions": correct["interventions"] + [{
                "material": "8-week training program with qPCR validation"
            }],
        }
        self.assertTrue(module._scope_audit(correct, case)["passed"])
        audit = module._scope_audit(merged, case)
        self.assertFalse(audit["passed"])
        self.assertIn("8-week", audit["excluded_hits"])

    def test_evaluator_intervention_semantics_uses_material_and_dosage(self):
        runner_path = (
            ROOT / "test" / "experiments" / "deepseek_seacdm_generalization" /
            "run_experiment.py"
        )
        spec = importlib.util.spec_from_file_location("scope_eval_semantics", runner_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        semantics = module._semantic_sets({
            "interventions": [{
                "material": "high-intensity cycling exercise",
                "dosage": "60 min at 80% VO2max",
                "intervention_type": "exercise",
            }]
        }, {})
        value = next(iter(semantics["intervention"]))
        self.assertIn("high-intensity cycling", value)
        self.assertIn("80% vo2max", value)

    def test_blind_multicohort_gate_rejects_paper_only_rnaseq_accession(self):
        runner_path = (
            ROOT / "test" / "experiments" / "deepseek_seacdm_blind_multicohort" /
            "run_experiment.py"
        )
        spec = importlib.util.spec_from_file_location("blind_scope_eval", runner_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        correct = {
            "experiment": [{
                "experiment_type": "soleus myonuclei RRBS in old mice after 8 weeks PoWeR"
            }],
            "interventions": [{
                "material": "progressive weighted wheel running (PoWeR)",
                "intervention_time": "8 weeks",
            }],
            "assay": [{"assay_name": "Bisulfite-Seq"}],
        }
        contaminated = {
            **correct,
            "assay": correct["assay"] + [{
                "assay_name": "RNA-seq", "comments": "GSE198652"
            }],
        }
        self.assertTrue(module._scope_audit(correct)["passed"])
        audit = module._scope_audit(contaminated)
        self.assertFalse(audit["passed"])
        self.assertIn("GSE198652", audit["foreign_design_accessions"])


if __name__ == "__main__":
    unittest.main()
