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


def enrichment(final, execution="completed", status="valid", stop=None):
    base = {"method": "GSEA", "gene_sets": "MSigDB Hallmark 2024.1", "organism": "Human",
            "feature_id_type": "gene_symbol", "outputs": ["gsea.csv"]}
    base.update(final)
    return rec("enrichment", base, status=status, execution=execution, stop=stop)


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



class EnrichmentTests(unittest.TestCase):
    def test_gsea_after_completed_execution_passes(self):
        records = paired_case()
        records.insert(-1, enrichment({}))
        self.assertEqual(check_case(records, "c1"), [])
        self.assertEqual(check_record(records[-2], "e"), [])

    def test_enrichment_without_completed_execution_fails(self):
        records = paired_case()
        for record in records:
            if record["stage"] == "execution":
                record.update(execution_status="failed")
                record["final"] = {"method": "DESeq2", "execution_error": "No module named 'pydeseq2'"}
        records.insert(-1, enrichment({}))
        self.assertTrue(any("enrichment completed without" in e for e in check_case(records, "c1")))

    def test_probe_ids_and_rat_need_mappings(self):
        errors = check_record(enrichment({"feature_id_type": "affy_probe", "organism": "Rat"}), "e")
        self.assertTrue(any("id_mapping" in e for e in errors))
        self.assertTrue(any("ortholog_mapping" in e for e in errors))
        ok = enrichment({"feature_id_type": "affy_probe", "organism": "Rat",
                         "id_mapping": "GPL1355 annotation", "ortholog_mapping": "HCOP rat-human"})
        self.assertEqual(check_record(ok, "e"), [])

    def test_ora_list_must_use_applied_threshold(self):
        records = paired_case()
        ora = enrichment({"method": "ORA (Enrichr GO/KEGG)",
                          "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": 1.0},
                          "input_threshold_source": "applied"})
        records.insert(-1, ora)
        self.assertTrue(any("ORA input_threshold differs" in e for e in check_case(records, "c1")))
        ora["final"]["input_threshold_source"] = "audit"
        self.assertEqual(check_case(records, "c1"), [])
        missing = enrichment({"method": "ORA"})
        self.assertTrue(any("input_threshold" in e for e in check_record(missing, "e")))

    def test_refused_enrichment_does_not_block_completed_de(self):
        records = paired_case()
        records.insert(-1, enrichment({}, execution="not_run", status="refused",
                                      stop="transcript IDs without a gene mapping"))
        self.assertEqual(check_case(records, "c1"), [])

    def test_decision_gate_cannot_carry_execution_status(self):
        record = rec("design", {"analysis_type": "two-arm", "design_column": "g", "control": "a",
                                "treatment": "b"}, execution="completed")
        self.assertTrue(any("keeps execution_status not_started" in e for e in check_record(record, "d")))

    def test_planned_enrichment_not_run_needs_reason(self):
        records = paired_case()
        planned = enrichment({}, execution="not_run")
        planned["final"].pop("outputs")
        self.assertTrue(any("reason_not_run" in e for e in check_record(planned, "e")))
        planned["final"]["reason_not_run"] = "differential analysis did not complete; gseapy missing"
        self.assertEqual(check_record(planned, "e"), [])
        records.insert(-1, planned)
        self.assertEqual(check_case(records, "c1"), [])


class ThresholdNameTests(unittest.TestCase):
    def test_fdr_and_padj_are_the_same_metric(self):
        records = set_final(paired_case(), "threshold",
                            paper_threshold={"metric": "FDR", "cutoff": 0.05, "effect_cutoff": None},
                            applied_threshold={"metric": "padj", "cutoff": 0.05, "effect_cutoff": None})
        self.assertEqual(check_case(records, "c1"), [])

    def test_adjustment_change_needs_deviation_route_and_note(self):
        paper = {"metric": "FDR", "adjustment": "permutation-based FDR", "cutoff": 0.05, "effect_cutoff": None}
        applied = {"metric": "padj", "adjustment": "Benjamini-Hochberg", "cutoff": 0.05, "effect_cutoff": None}
        records = set_final(paired_case(), "threshold", paper_threshold=paper, applied_threshold=applied)
        self.assertTrue(any("adjustment changes" in e for e in check_case(records, "c1")))
        set_final(records, "threshold", threshold_source="paper_on_deviation_route",
                  deviation_note="no permutation FDR executor; BH within the contrast")
        self.assertEqual(check_case(records, "c1"), [])
        same = set_final(paired_case(), "threshold",
                         paper_threshold={**paper, "adjustment": "BH"}, applied_threshold=applied)
        self.assertEqual(check_case(same, "c1"), [])


if __name__ == "__main__":
    unittest.main()
