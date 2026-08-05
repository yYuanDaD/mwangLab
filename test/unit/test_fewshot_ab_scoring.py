import importlib.util
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "test" / "experiments" / "fewshot_case_ab" / "run_experiment.py"
SPEC = importlib.util.spec_from_file_location("fewshot_ab", SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)


class FewshotABScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        here = SCRIPT.parent
        cls.gold = json.loads((here / "gold_target.json").read_text(encoding="utf-8"))
        cls.target = MOD.TARGET_PAPER.read_text(encoding="utf-8")

    def test_gold_like_output_scores_high(self):
        result = MOD.PaperWorkflowExtraction(
            paper_title=self.gold["paper_title"], organisms=["Human"],
            geo_accessions=["GSE71014", "GSE116256"],
            modalities=["bulk gene expression", "single-cell RNA-seq"],
            comparison_groups=["cluster A", "cluster B", "high MRI", "low MRI"],
            reported_methods=self.gold["reported_methods"],
            recommended_workflow=[
                MOD.WorkflowStep(stage="inspect", action="Inspect each dataset separately.", reason="Different platforms."),
                MOD.WorkflowStep(stage="single_cell", action="Require biological replicate IDs and use pseudobulk.",
                                 reason="Do not treat cells as biological replicates."),
                MOD.WorkflowStep(stage="design", action="Do not force a treatment-control contrast.",
                                 reason="This is a prognostic clustering design."),
            ],
            requires_manual_review=True, review_reasons=["Multi-dataset prognostic design"],
            evidence_snippets=["GSE71014 and TARGET datasets were utilized", "GSE116256 data were derived"],
        )
        score = MOD._score(result, self.target, self.gold)
        self.assertGreaterEqual(score["total"], 90)
        self.assertEqual(score["hallucinated_accessions"], [])

    def test_copied_example_accession_is_penalized(self):
        result = MOD.PaperWorkflowExtraction(
            paper_title=self.gold["paper_title"], organisms=["Mouse"],
            geo_accessions=["GSE279359"], modalities=["long-read RNA-seq"],
            comparison_groups=["pre-exercise", "post-exercise"],
            reported_methods=["TALON"], recommended_workflow=[],
            requires_manual_review=False, review_reasons=[], evidence_snippets=[],
        )
        score = MOD._score(result, self.target, self.gold)
        self.assertIn("GSE279359", score["copied_example_accessions"])
        self.assertLess(score["total"], 30)


if __name__ == "__main__":
    unittest.main()
