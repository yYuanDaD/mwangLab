import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.sea_cdm_schema import Sourced
from tools.seacdm_tools import (
    DocumentationExtract,
    DocumentationOnlyExtraction,
    ExperimentInterventionExtraction,
    ExperimentLite,
    InterventionExtract,
    MaterialExtract,
    MaterialExtraction,
    ReportedFinding,
    ReportedFindingsExtraction,
    StudyOnlyExtraction,
    StudyExtract,
    extract_tables_from_text,
)


def sourced(value):
    return Sourced(value=value, source=value)


class StagedSeaCdmTests(unittest.TestCase):
    def _metadata(self, folder: str) -> str:
        path = Path(folder) / "GSEX_metadata.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow([
                "sample", "title", "characteristics_ch1.0.condition",
                "organism_ch1", "instrument_model",
            ])
            writer.writerow(["GSM1", "sedentary", "control", "Mus musculus", "NovaSeq"])
            writer.writerow(["GSM2", "exercise", "exercise", "Mus musculus", "NovaSeq"])
        return str(path)

    def test_staged_retries_required_empty_stage_and_records_trace(self):
        calls = {"study": 0}

        def study_stage(text, study_id, organism, usage=None):
            calls["study"] += 1
            if calls["study"] == 1:
                return StudyOnlyExtraction()
            return StudyOnlyExtraction(
                study=StudyExtract(study_name=sourced("Test exercise paper")),
            )

        def documentation_stage(text, study_id, organism, usage=None):
            return DocumentationOnlyExtraction(documentation=[DocumentationExtract(
                document_name=sourced("Test exercise paper"),
                documentation_type=sourced("paper"),
            )])

        def design_stage(text, study_id, organism, usage=None):
            return ExperimentInterventionExtraction(
                experiments=[ExperimentLite(
                    experiment_type=sourced("exercise experiment"),
                    experiment_subject=sourced("Mus musculus"),
                )],
                interventions=[InterventionExtract(
                    material=sourced("running wheel"),
                    intervention_type=sourced("exercise"),
                )],
            )

        def material_stage(text, study_id, organism, usage=None):
            return MaterialExtraction(material=[MaterialExtract(
                material_name=sourced("anti-ACVR1C antibody"),
                organization=sourced("Example vendor"),
            )])

        def finding_stage(text, study_id, organism, usage=None):
            return ReportedFindingsExtraction(findings=[ReportedFinding(
                entity="Acvr1c", entity_type="gene", direction="up",
                comparison="exercise vs control", source="Acvr1c increased after exercise",
            )])

        paper = (
            "Test exercise paper Abstract exercise study. Introduction background. "
            "Results Acvr1c increased after exercise. Discussion exercise improved memory. "
            "Methods Mice used a running wheel and anti-ACVR1C antibody from Example vendor. "
            "Data availability GSEX. References ignored."
        )
        with tempfile.TemporaryDirectory() as folder:
            with patch("tools.seacdm_tools._extract_study_only", study_stage), \
                 patch("tools.seacdm_tools._extract_documentation_only", documentation_stage), \
                 patch("tools.seacdm_tools._extract_experiment_interventions", design_stage), \
                 patch("tools.seacdm_tools._extract_materials", material_stage), \
                 patch("tools.seacdm_tools._extract_reported_findings", finding_stage):
                report = {}
                tables = extract_tables_from_text(
                    "GSEX", paper, "Mouse", report=report,
                    metadata_csv=self._metadata(folder), strategy="staged",
                    max_stage_retries=1,
                )

        self.assertEqual(calls["study"], 2)
        self.assertEqual(report["extraction_mode"], "lean(staged)")
        self.assertFalse(report.get("group_errors"))
        self.assertEqual(len(tables["experiment"]), 1)
        self.assertEqual(len(tables["interventions"]), 1)
        self.assertEqual(len(tables["exercise"]), 1)
        self.assertEqual(len(tables["material"]), 1)
        self.assertEqual(len(tables["documentation"]), 1)
        study_events = [event for event in report["decision_trace"]
                        if event["stage"] == "study"]
        self.assertEqual([event["status"] for event in study_events],
                         ["incomplete", "complete"])
        self.assertEqual(report["reported_findings"][0]["entity"], "Acvr1c")

    def test_invalid_strategy_fails_before_llm_work(self):
        with self.assertRaisesRegex(ValueError, "strategy"):
            extract_tables_from_text("GSEX", "paper", strategy="unknown")

    def test_documentation_coerces_sourced_shape_for_plain_reference_ids(self):
        row = DocumentationExtract.model_validate({
            "document_name": {"value": "Paper", "source": "Paper"},
            "documentation_type": {"value": "paper", "source": "Paper"},
            "reference_source": {"value": "PMCID", "source": "PMC1"},
            "reference_source_id": {"value": "PMC1", "source": "PMC1"},
        })
        self.assertEqual(row.reference_source, "PMCID")
        self.assertEqual(row.reference_source_id, "PMC1")

    def test_staged_repairs_missing_study_title_from_grounded_documentation(self):
        def empty_study(text, study_id, organism, usage=None):
            return StudyOnlyExtraction(study=StudyExtract(
                study_description=sourced("Exercise study objective")
            ))

        def documentation(text, study_id, organism, usage=None):
            return DocumentationOnlyExtraction(documentation=[DocumentationExtract(
                document_name=sourced("Grounded paper title"),
                documentation_type=sourced("paper"),
            )])

        def design(text, study_id, organism, usage=None):
            return ExperimentInterventionExtraction(
                experiments=[ExperimentLite(experiment_type=sourced("exercise"))],
                interventions=[InterventionExtract(
                    material=sourced("running wheel"), intervention_type=sourced("exercise")
                )],
            )

        def materials(text, study_id, organism, usage=None):
            return MaterialExtraction(material=[MaterialExtract(
                material_name=sourced("kit")
            )])

        def findings(text, study_id, organism, usage=None):
            return ReportedFindingsExtraction(findings=[ReportedFinding(
                entity="Gene1", entity_type="gene", direction="up", source="Gene1 increased"
            )])

        paper = (
            "Grounded paper title Results Gene1 increased after exercise. Discussion results. "
            "Methods running wheel kit. Data availability GSEX. References ignored."
        )
        with tempfile.TemporaryDirectory() as folder:
            with patch("tools.seacdm_tools._extract_study_only", empty_study), \
                 patch("tools.seacdm_tools._extract_documentation_only", documentation), \
                 patch("tools.seacdm_tools._extract_experiment_interventions", design), \
                 patch("tools.seacdm_tools._extract_materials", materials), \
                 patch("tools.seacdm_tools._extract_reported_findings", findings):
                report = {}
                tables = extract_tables_from_text(
                    "GSEX", paper, "Mouse", report=report,
                    metadata_csv=self._metadata(folder), strategy="staged",
                )

        self.assertEqual(tables["study"][0]["study_name"], "Grounded paper title")
        self.assertFalse(report.get("group_errors"))
        repairs = [event for event in report["decision_trace"]
                   if event["stage"] == "repair_study_name"]
        self.assertEqual(len(repairs), 1)


if __name__ == "__main__":
    unittest.main()
