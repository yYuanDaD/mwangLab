"""Regression tests for the ExerGeneDB gold export and contrast scoring."""

import importlib.util
import os
import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools.contrast_gold import (  # noqa: E402
    pairing_signal, production_route, samples_for_value, score_contrast_set,
)


def _load_fetch_module():
    spec = importlib.util.spec_from_file_location(
        "fetch_exergenedb_labels", ROOT / "scripts" / "fetch_exergenedb_labels.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _record(sample, series, group, seqtype="mRNA", time="Post exercise", sex="Male"):
    return {"id": f"EGDB_{seqtype}_{sample}", "sample_id": sample, "series_id": series,
            "organism": "Homo sapiens", "seqtech": "Microarray", "seqtype": seqtype,
            "group": group, "sampling_time": time if group == "Exercise" else "Pre exercise",
            "tissue_char1": "Vastus lateralis", "health_condition": "Health", "gender": sex,
            "other_treatment": "None", "age_char2": "Young adult"}


class FetchExportTests(unittest.TestCase):
    def setUp(self):
        self.fetch = _load_fetch_module()

    def test_mrna_and_ncrna_rows_collapse_to_one_sample(self):
        records = [_record("GSM1", "GSE1", "Exercise"), _record("GSM1", "GSE1", "Exercise", "ncRNA"),
                   _record("GSM2", "GSE1", "Sedentary")]
        samples = self.fetch.deduplicate_samples(records)
        self.assertEqual(len(samples), 2)
        row = samples.set_index("sample_id").loc["GSM1"]
        self.assertEqual(row["seqtype"], "mRNA;ncRNA")
        self.assertEqual(row["role"], "treatment")

    def test_conflicting_labels_fail_closed(self):
        records = [_record("GSM1", "GSE1", "Exercise"), _record("GSM1", "GSE1", "Sedentary", "ncRNA")]
        with self.assertRaises(RuntimeError):
            self.fetch.deduplicate_samples(records)

    def test_series_design_class(self):
        records = [_record("GSM1", "GSE1", "Sedentary"), _record("GSM2", "GSE1", "Exercise", time="1h post exercise"),
                   _record("GSM3", "GSE1", "Exercise", time="24h post exercise"),
                   _record("GSM4", "GSE2", "Sedentary"), _record("GSM5", "GSE2", "Exercise"),
                   _record("GSM6", "GSE2", "Exercise", sex="Female")]
        series = self.fetch.summarize_series(self.fetch.deduplicate_samples(records)).set_index("accession")
        self.assertEqual(series.loc["GSE1", "design_class"], "multi_time")
        self.assertEqual(series.loc["GSE2", "design_class"], "multi_strata")


class ContrastScoringTests(unittest.TestCase):
    def setUp(self):
        self.meta = pd.DataFrame({
            "characteristics_ch1.0.time": ["pre", "pre", "post", "post", "post", "pre"],
            "title": ["Ctrl.1", "Ctrl.2", "Ex.1", "Ex.2", "Ex.3", "KO.1"],
            "characteristics_ch1.1.subject id": ["s1", "s2", "s1", "s2", "s3", "s9"],
        }, index=[f"GSM{i}" for i in range(1, 7)])
        # GSM6 is outside the gold (for example an excluded knockout sample).
        self.gold = pd.DataFrame({
            "series_id": ["GSE1"] * 5,
            "role": ["control", "control", "treatment", "treatment", "treatment"],
            "stratum_key": ["a", "a", "a", "a", "a"],
        }, index=[f"GSM{i}" for i in range(1, 6)])
        self.roles = self.gold["role"]
        self.col = "characteristics_ch1.0.time"

    def verdict(self, contrasts):
        return score_contrast_set(self.meta, self.roles, contrasts, self.gold)

    def test_correct_reversed_and_refused(self):
        self.assertEqual(self.verdict([(self.col, "pre", "post")])["verdict"], "correct")
        self.assertEqual(self.verdict([(self.col, "post", "pre")])["verdict"], "reversed")
        self.assertEqual(self.verdict([])["verdict"], "refused")

    def test_unlabelled_samples_do_not_count_against_a_correct_pick(self):
        scored = self.verdict([(self.col, "pre", "post")])
        self.assertEqual(scored["purity"], 1.0)
        self.assertEqual(scored["contrasts"][0]["control_arm_gold"]["unlabelled"], 1)

    def test_mixed_and_unresolvable(self):
        self.meta["batch"] = ["b1", "b2", "b1", "b2", "b1", "b2"]
        self.assertEqual(self.verdict([("batch", "b1", "b2")])["verdict"], "mixed")
        self.assertEqual(self.verdict([("no_such_column", "x", "y")])["verdict"], "unresolvable")

    def test_replicate_grouped_column_resolves_but_is_flagged_non_executable(self):
        ids, how = samples_for_value(self.meta, "title__replicate_grouped", "Ex")
        self.assertEqual((ids, how), (["GSM3", "GSM4", "GSM5"], "replicate_grouped"))
        scored = self.verdict([("title__replicate_grouped", "Ctrl", "Ex")])
        self.assertEqual(scored["verdict"], "correct")
        self.assertFalse(scored["all_columns_executable"])

    def test_pairing_signal_detects_subjects_shared_across_arms(self):
        hits = pairing_signal(self.meta, ["GSM1", "GSM2"], ["GSM3", "GSM4", "GSM5"])
        self.assertEqual(hits, [("characteristics_ch1.1.subject id", 2)])
        self.assertEqual(self.verdict([(self.col, "pre", "post")])["pairing_signal"],
                         ["characteristics_ch1.1.subject id"])


class ProductionRouteTests(unittest.TestCase):
    py = [("time", "pre", "1h"), ("time", "pre", "24h")]

    @staticmethod
    def llm(triple=None, is_valid=False, confidence="high", intent=True):
        col, ctrl, treat = triple or (None, None, None)
        return {"design_column": col, "control_value": ctrl, "treatment_value": treat,
                "is_valid": is_valid, "confidence": confidence, "intent_match": intent}

    def test_routes_mirror_batch_policy(self):
        self.assertEqual(production_route(self.py, True, None), (self.py, "python_confident"))
        self.assertEqual(production_route(self.py, False, None), ([], "llm_unavailable_blocked"))
        confirm = self.llm(self.py[0], is_valid=True)
        self.assertEqual(production_route(self.py, False, confirm), (self.py, "llm_confirm"))
        self.assertEqual(production_route(self.py, False, confirm, strict=True),
                         ([self.py[0]], "llm_confirm"))
        override = self.llm(("group", "sed", "ex"))
        self.assertEqual(production_route(self.py, False, override), ([("group", "sed", "ex")], "llm_override"))
        self.assertEqual(production_route([], False, override)[1], "llm_proposed")
        self.assertEqual(production_route(self.py, False, self.llm(self.py[0], confidence="low"))[1],
                         "llm_refuse")
        self.assertEqual(production_route(self.py, False, self.llm(intent=False))[1],
                         "llm_refuse_intent_mismatch")
        self.assertEqual(production_route(self.py, True, override, strict=True)[1], "llm_override")


if __name__ == "__main__":
    unittest.main()
