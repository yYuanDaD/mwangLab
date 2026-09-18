"""Offline fixtures for dataset leakage, conflicts, reproducibility and provenance."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("dataset_export", ROOT / "test/scripts/export_training_dataset.py")
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)


class DatasetExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.output = self.root / "output"
        self.data = self.root / "data"
        path = self.data / "GSE123" / "GSE123_metadata.csv"
        path.parent.mkdir(parents=True)
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["sample", "condition"])
            w.writerows([(f"S{i}", label) for i, label in enumerate(["Control"] * 3 + ["Treatment"] * 3 + ["Alternative"] * 3)])

    def cohort(self, name, treatment="Treatment", with_log=True, **kwargs):
        folder = self.output / name
        folder.mkdir(parents=True)
        row = dict(accession="GSE123", status="deg_gsea_ok", design_col="condition",
                   control="Control", treatment=treatment, llm_validated="True",
                   llm_reasoning="private outcome rationale")
        row.update(kwargs)
        with (folder / "summary.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(row))
            w.writeheader()
            w.writerow(row)
        if with_log:
            (folder / "workflow.log").write_text(
                "# organism=Mouse\n# treatment_keywords=['treatment']\n"
                "# control_keywords=['control']\n\nresult: private outcome rationale\n", encoding="utf-8")
        return folder

    def export(self, name="dataset"):
        dest = self.root / name
        report = EXPORT.export_dataset(self.output, self.data, dest)
        rows = [json.loads(line) for line in (dest / "contrast_candidates.jsonl").read_text(encoding="utf-8").splitlines()]
        return report, rows

    def test_duplicates_retain_all_provenance_without_target_leak(self):
        self.cohort("one")
        self.cohort("two", status="deg_failed", llm_reasoning="different rationale")
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob("*") if p.is_file()}
        report, rows = self.export()
        self.assertEqual(report["candidate_rows"], 2)
        self.assertEqual(report["repeated_input_label_rows_collapsed"], 1)
        self.assertEqual(len(rows[0]["label_variants"][0]["sources"]), 2)
        self.assertEqual(set(rows[0]["input"]), {"accession", "organism", "control_keywords", "treatment_keywords", "metadata_columns_summary"})
        self.assertNotIn("rationale", json.dumps(rows[0]["input"]))
        self.assertFalse(rows[0]["training_ready"])
        for path, sha in before.items():
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), sha)

    def test_conflicting_labels_not_silently_picked(self):
        self.cohort("one")
        self.cohort("two", treatment="Alternative")
        report, rows = self.export()
        self.assertEqual(report["conflicting_input_groups"], 1)
        self.assertEqual(report["repeated_input_label_rows_collapsed"], 0)
        self.assertEqual(len(rows[0]["label_variants"]), 2)
        self.assertEqual(len((self.root / "dataset/conflicts.jsonl").read_text().splitlines()), 1)

    def test_missing_labels_not_refusal_and_bad_values_flagged(self):
        self.cohort("missing", treatment="", status="skipped_no_matrix_file", design_col="", control="")
        self.cohort("wrong", treatment="not in metadata")
        _, rows = self.export()
        flags = [f for v in rows[0]["label_variants"] for f in v["flags"]]
        self.assertIn("missing_contrast_not_a_verified_refusal", flags)
        self.assertIn("arm_not_in_current_metadata", flags)

    def test_aggregate_summaries_and_bad_accessions_excluded(self):
        self.cohort("aggregate", with_log=False)
        self.cohort("bad", accession="../../GSE123")
        report, rows = self.export()
        self.assertEqual(rows, [])
        self.assertEqual(report["summary_file_statuses"]["skipped_no_workflow_context"], 1)
        self.assertEqual(report["read_or_row_errors"], 1)

    def test_reproducible_and_existing_destination_protected(self):
        self.cohort("one")
        _, first = self.export("first")
        _, second = self.export("second")
        self.assertEqual(first, second)
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.export("first")

    def test_missing_metadata_and_malformed_source_visible(self):
        self.cohort("missing", accession="GSE999")
        bad = self.cohort("bad") / "summary.csv"
        bad.write_bytes(b"\xff\xfe\xff")
        report, rows = self.export()
        self.assertIn("metadata_summary_missing", rows[0]["flags"])
        self.assertEqual(report["read_or_row_errors"], 1)
        self.assertEqual(report["training_ready_examples"], 0)


if __name__ == "__main__":
    unittest.main()
