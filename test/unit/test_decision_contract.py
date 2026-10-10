"""Decision-contract v2: record fields and case-level invariants."""

import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools.decision_contract import check_case, check_record, matrix_family, method_family, validate  # noqa: E402

EV = [{"id": "metadata:meta.csv", "kind": "metadata"}]


def rec(stage, final, status="valid", execution="not_started", stop=None):
    return {"contract_version": "2", "case_id": "c1", "stage": stage, "evidence": EV, "candidates": [],
            "final": final, "confidence": "high", "reasoning": "r", "decision_status": status,
            "execution_status": execution, "stop_reason": stop}


def paired_case():
    """A correct within-subject DESeq2 case with a completed execution."""
    return [
        rec("paper_reconstruction", {"accessions": ["GSE1"], "primary_estimand": "post vs pre",
                                     "planned_contrasts": ["post vs pre"],
                                     "paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None}}),
        rec("ownership", {"accession": "GSE1", "matrix_file": "m.csv", "metadata_file": "x.csv", "owned": True}),
        rec("alignment", {"method": "exact:title", "n_aligned": 16, "n_metadata": 16, "coverage": 1.0}),
        rec("matrix", {"matrix_type": "raw counts", "recommended_method": "DESeq2"}),
        rec("design", {"analysis_type": "paired two-timepoint", "formula": "~ subject + time",
                       "control": "pre", "treatment": "post"}),
        rec("covariance", {"status": "required", "blocking_terms": ["subject"], "covariates": []}),
        rec("method", {"method": "DESeq2", "matrix_type": "raw counts", "formula": "~ subject + time"}),
        rec("threshold", {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None},
                          "threshold_source": "paper",
                          "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None}}),
        rec("execution", {"method": "DESeq2", "outputs": ["DEG_results_post_vs_pre.csv"]}, execution="completed"),
        rec("study", {"route": "paper_aligned"}),
    ]


def set_final(records, stage, **updates):
    for record in records:
        if record["stage"] == stage:
            record["final"].update(updates)
    return records


class RecordTests(unittest.TestCase):
    def test_correct_case_passes(self):
        records = paired_case()
        self.assertEqual([e for r in records for e in check_record(r)], [])
        self.assertEqual(check_case(records), [])

    def test_bare_string_evidence_and_missing_fields_fail(self):
        record = rec("covariance", {})
        record["evidence"] = ["anything"]
        errors = check_record(record)
        self.assertTrue(any("evidence[0]" in e for e in errors))
        self.assertTrue(any("missing final.status" in e for e in errors))

    def test_unresolved_covariance_cannot_be_valid(self):
        errors = check_record(rec("covariance", {"status": "unresolved", "blocking_terms": [], "covariates": []}))
        self.assertTrue(any("unresolved covariance" in e for e in errors))

    def test_failed_execution_needs_error_and_valid_needs_no_stop_reason(self):
        self.assertTrue(check_record(rec("execution", {"method": "DESeq2"}, execution="failed")))
        self.assertTrue(check_record(rec("matrix", {"matrix_type": "raw", "recommended_method": "x"}, stop="no")))

    def test_legacy_mode_skips_stage_fields(self):
        record = rec("covariance", {})
        self.assertEqual(check_record(record, legacy=True), [])


class CaseInvariantTests(unittest.TestCase):
    def test_completed_after_blocked_gate(self):
        records = paired_case()
        records[5] = rec("covariance", {}, status="refused", stop="batch aliased with treatment")
        self.assertTrue(any("blocked" in e for e in check_case(records)))

    def test_paired_design_requires_covariance(self):
        records = set_final(paired_case(), "covariance", status="not_required", blocking_terms=[])
        self.assertTrue(any("paired/repeated" in e for e in check_case(records)))

    def test_blocking_term_must_reach_formula(self):
        records = set_final(paired_case(), "method", formula="~ time")
        set_final(records, "design", formula="~ time")
        self.assertTrue(any("'subject'" in e for e in check_case(records)))

    def test_count_method_on_fpkm(self):
        records = set_final(paired_case(), "matrix", matrix_type="FPKM")
        set_final(records, "method", matrix_type="FPKM")
        self.assertTrue(any("count-based method" in e for e in check_case(records)))

    def test_limma_on_linear_data_needs_transform(self):
        records = set_final(paired_case(), "matrix", matrix_type="FPKM")
        set_final(records, "method", method="limma", matrix_type="FPKM")
        set_final(records, "execution", method="limma")
        self.assertTrue(any("needs final.transform" in e for e in check_case(records)))
        set_final(records, "method", transform="log2(x+1)")
        self.assertEqual(check_case(records), [])

    def test_paper_threshold_cannot_change_silently(self):
        records = paired_case()
        records[7]["final"]["applied_threshold"] = {"metric": "padj", "cutoff": 0.05, "effect_cutoff": 1.0}
        self.assertTrue(any("applied threshold differs" in e for e in check_case(records)))

    def test_paired_change_is_exempt_from_formula_check(self):
        records = set_final(paired_case(), "design", analysis_type="paired_change", formula="~ C(arm)")
        set_final(records, "method", method="limma", formula="~ C(arm)", transform="log2(CPM+1)")
        set_final(records, "execution", method="limma")
        self.assertEqual(check_case(records), [])

    def test_families(self):
        self.assertEqual(matrix_family("fpkm_linear"), "linear_normalized")
        self.assertEqual(matrix_family("log_transformed (RMA log2 microarray)"), "log_scale")
        self.assertEqual(matrix_family("Raw integer counts (featureCounts)"), "raw_counts")
        self.assertEqual(matrix_family("kallisto estimated counts"), "estimated_counts")
        self.assertEqual(matrix_family("beta values"), "methylation_beta")
        self.assertEqual(method_family("limma (declared alternative to the paper's DESeq2)"), "log_linear")
        self.assertEqual(method_family("limma-voom"), "count")


class ValidateFilesTests(unittest.TestCase):
    def test_validate_reads_files_and_groups_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "good.json"
            bad = Path(tmp) / "bad.json"
            good.write_text(json.dumps(paired_case()), encoding="utf-8")
            broken = copy.deepcopy(paired_case())
            for record in broken:
                record["case_id"] = "c2"
            set_final(broken, "covariance", status="not_required", blocking_terms=[])
            bad.write_text(json.dumps(broken), encoding="utf-8")
            count, errors = validate([good])
            self.assertEqual((count, errors), (10, []))
            _, errors = validate([good, bad])
            self.assertTrue(errors and all(e.startswith("c2") for e in errors))


if __name__ == "__main__":
    unittest.main()
