"""Native skill runtime: evidence helpers, external-LLM block, run layout, policy guards."""

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools import model_factory, native  # noqa: E402
from tools.analysis_policy import PolicyViolation, enforce_method_matrix_compatibility  # noqa: E402
from tools.multigroup_tools import complete_subject_pairs, run_multigroup_analysis  # noqa: E402


def _write_case(folder: Path) -> dict:
    rng = np.random.default_rng(3)
    titles = [f"P{s}_{t}" for s in range(1, 5) for t in ("pre", "post")]
    meta = pd.DataFrame({"title": titles,
                         "subject": [t.split("_")[0] for t in titles],
                         "time": [t.split("_")[1] for t in titles],
                         "run": ["r1"] * 8},
                        index=[f"GSM{i}" for i in range(1, 9)])
    meta.index.name = "geo_accession"
    counts = pd.DataFrame(rng.poisson(50, size=(30, 8)), columns=titles[::-1],
                          index=[f"g{i}" for i in range(30)])
    counts.insert(0, "symbol", [f"S{i}" for i in range(30)])
    paths = {"metadata": folder / "meta.csv", "matrix": folder / "counts.csv", "paper": folder / "paper.md"}
    meta.to_csv(paths["metadata"])
    counts.to_csv(paths["matrix"])
    paths["paper"].write_text("Paired pre/post biopsies; DESeq2 ~ subject + time; padj < 0.05.\n", encoding="utf-8")
    return paths


class EvidenceHelperTests(unittest.TestCase):
    def test_profile_align_pairing_design_confounding(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _write_case(Path(tmp))
            profile = native.profile_matrix(paths["matrix"])
            self.assertEqual(profile["annotation_columns_dropped"], ["symbol"])
            self.assertTrue(profile["candidates"][0].startswith("raw_counts"))
            aligned = native.align_to_metadata(paths["matrix"], paths["metadata"], Path(tmp) / "a",
                                               key_column="title")
            self.assertEqual((aligned["n_aligned"], aligned["coverage"]), (8, 1.0))
            matrix = pd.read_csv(aligned["outputs"]["aligned_matrix"]["path"], index_col=0)
            self.assertEqual(list(matrix.columns), [f"GSM{i}" for i in range(1, 9)])
            raw = pd.read_csv(paths["matrix"], index_col=0)
            self.assertTrue((matrix["GSM1"] == raw["P1_pre"]).all())  # mapped by label, not position
            meta = aligned["outputs"]["aligned_metadata"]["path"]
            pairing = native.pairing_report(meta, "subject", "time", ["pre", "post"])
            self.assertTrue(pairing["complete_and_unique"])
            design = native.design_check(meta, ["subject", "time"])
            self.assertEqual((design["rank"], design["residual_df"], design["full_rank"]), (5, 3, True))
            report = {r["column"]: r["status"] for r in native.confounding_report(meta, "time")}
            self.assertEqual(report["subject"], "crossed")
            self.assertEqual(report["run"], "constant")
            self.assertEqual(report["title"], "sample_identifier")

    def test_alignment_never_guesses(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _write_case(Path(tmp))
            with self.assertRaises(native.NativeToolError):
                native.align_to_metadata(paths["matrix"], paths["metadata"], Path(tmp) / "a")

    def test_confounding_detects_aliased_batch(self):
        meta = pd.DataFrame({"group": ["sed"] * 4 + ["run"] * 4, "batch": ["b1"] * 4 + ["b2"] * 4,
                             "animal": [f"a{i}" for i in range(8)]}, index=[f"S{i}" for i in range(8)])
        report = {r["column"]: r["status"] for r in native.confounding_report(meta, "group")}
        self.assertEqual(report, {"batch": "complete_confounding", "animal": "sample_identifier"})

    def test_apply_threshold_adds_no_cutoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            deg = Path(tmp) / "DEG_results_x.csv"
            pd.DataFrame({"log2FoldChange": [0.3, 2.0, -1.5, 0.1], "padj": [0.01, 0.01, 0.2, 0.04]},
                         index=list("abcd")).to_csv(deg)
            self.assertEqual(native.apply_threshold(deg)["n_significant"], 3)
            strict = native.apply_threshold(deg, effect_cutoff=0.585)
            self.assertEqual((strict["n_significant"], strict["n_up"], strict["n_down"]), (1, 1, 0))
            self.assertIn("implausible_sig_fraction", strict["deg_sanity"] + native.apply_threshold(deg)["deg_sanity"])

    def test_log_transform_refuses_log_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            linear = Path(tmp) / "fpkm.csv"
            pd.DataFrame({"S1": [0.0, 120.5], "S2": [3.2, 900.1]}, index=["a", "b"]).to_csv(linear)
            out = native.log_transform(linear, Path(tmp) / "log.csv")
            self.assertAlmostEqual(pd.read_csv(out["output"], index_col=0).loc["b", "S2"], np.log2(901.1))
            with self.assertRaises(native.NativeToolError):
                native.log_transform(out["output"], Path(tmp) / "again.csv")


class ExternalLLMBlockTests(unittest.TestCase):
    def setUp(self):
        self.previous = os.environ.get(native.NATIVE_ENV)
        native.enable_native_mode()

    def tearDown(self):
        if self.previous is None:
            os.environ.pop(native.NATIVE_ENV, None)
        else:
            os.environ[native.NATIVE_ENV] = self.previous

    def test_clients_are_blocked_and_logged(self):
        before = len(model_factory.blocked_external_llm_attempts())
        self.assertIsNone(model_factory.create_structured_chat_model(required=False))
        with self.assertRaises(model_factory.ExternalLLMDisabledError):
            model_factory.create_chat_model(required=True)
        self.assertEqual(len(model_factory.blocked_external_llm_attempts()), before + 2)

    def test_call_tool_fails_on_error_text_and_hidden_calls(self):
        def failing(**_):
            return "POLICY BLOCKED: design is rank deficient"

        def sneaky(**_):
            model_factory.create_structured_chat_model(required=False)
            return "limma analysis completed successfully"

        with self.assertRaises(native.NativeToolError):
            native.call_tool(failing)
        with self.assertRaises(native.NativeToolError):
            native.call_tool(sneaky)
        self.assertEqual(native.call_tool(lambda **kw: "PCA completed", x=1), "PCA completed")
        for text in ("limma-voom unavailable: Rscript not found", "DESeq2 analysis failed. Error: x",
                     "Only 3 valid genes after filtering"):
            self.assertTrue(native.tool_failed(text), text)


class PolicyGuardTests(unittest.TestCase):
    def test_limma_rejects_linear_scale(self):
        linear = pd.DataFrame({"S1": [0.5, 812.3], "S2": [1.7, 455.9]})
        with self.assertRaisesRegex(PolicyViolation, "linear"):
            enforce_method_matrix_compatibility(linear, method="limma")
        enforce_method_matrix_compatibility(np.log2(linear + 1), method="limma")

    def test_multigroup_rejects_raw_counts_before_fitting(self):
        with tempfile.TemporaryDirectory() as tmp:
            cols = [f"S{i}" for i in range(8)]
            pd.DataFrame(np.random.default_rng(1).poisson(300, (50, 8)), columns=cols,
                         index=[f"g{i}" for i in range(50)]).to_csv(Path(tmp) / "c.csv")
            pd.DataFrame({"group": ["a"] * 4 + ["b"] * 4}, index=cols).to_csv(Path(tmp) / "m.csv")
            with self.assertRaisesRegex(PolicyViolation, "raw-count-like"):
                run_multigroup_analysis(str(Path(tmp) / "c.csv"), str(Path(tmp) / "m.csv"),
                                        {"analysis_type": "multilevel", "formula": "~ C(group)",
                                         "contrasts": []}, str(Path(tmp) / "out"))

    def test_paired_change_reports_excluded_subjects(self):
        meta = pd.DataFrame({"subject": ["a", "a", "b", "c", "c", "c"],
                             "time": ["pre", "post", "pre", "pre", "post", "post"],
                             "arm": ["x"] * 6}, index=[f"S{i}" for i in range(6)])
        pairs, excluded = complete_subject_pairs(meta, "subject", "time", "pre", "post", "arm")
        self.assertEqual([p["subject"] for p in pairs], ["a"])
        self.assertEqual({e["subject"]: e["reason"] for e in excluded},
                         {"b": "missing_followup", "c": "duplicate_samples"})


class RunRecorderTests(unittest.TestCase):
    def test_layout_validates_and_audits(self):
        previous = os.environ.get(native.NATIVE_ENV)
        native.enable_native_mode()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                paths = _write_case(tmp)
                run = native.RunRecorder(tmp / "run", request="test", platform_name="unit-test",
                                         decision_maker="unit test", case_ids=["c1", "c2"])
                case = run.case("c1", accession="GSE1")
                paper = case.add_input(paths["paper"], "paper")
                meta = case.add_input(paths["metadata"], "metadata")
                mat = case.add_input(paths["matrix"], "matrix")
                threshold = {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None}
                case.decide("paper_reconstruction", final={
                    "accessions": ["GSE1"], "primary_estimand": "post vs pre within subject",
                    "planned_contrasts": ["post vs pre"], "paper_threshold": threshold},
                    evidence=[paper], reasoning="Methods", confidence="high")
                aln = native.align_to_metadata(mat["path"], meta["path"], case.dir / "aligned",
                                               key_column="title")
                aligned = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
                case.decide("alignment", final={k: aln[k] for k in ("method", "n_aligned", "n_metadata",
                                                                     "coverage")},
                            evidence=[mat, meta, aligned], reasoning="exact title match", confidence="high")
                with self.assertRaises(native.NativeToolError):  # missing required fields
                    case.decide("matrix", final={}, evidence=[aligned], reasoning="x", confidence="high")
                case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2"},
                            evidence=[aligned], reasoning="integers", confidence="high")
                _, suit, summary = case.suitability(matrix_type="raw counts", factors=["time"],
                                                    metadata=pd.read_csv(paths["metadata"], index_col=0),
                                                    subject="subject")
                self.assertEqual(summary["verdict"], "analyzable", summary)
                with self.assertRaises(native.NativeToolError):  # the report is part of a valid design
                    case.decide("design", final={"analysis_type": "paired two-timepoint",
                                                 "formula": "~ subject + time", "design_column": "time",
                                                 "control": "pre", "treatment": "post"},
                                evidence=[meta], reasoning="paper", confidence="high")
                case.decide("design", final={"analysis_type": "paired two-timepoint",
                                             "formula": "~ subject + time", "design_column": "time",
                                             "control": "pre", "treatment": "post", "suitability": summary},
                            evidence=[meta, suit], reasoning="paper", confidence="high")
                case.decide("covariance", final={"status": "required", "blocking_terms": ["subject"],
                                                 "covariates": []},
                            evidence=[meta], reasoning="4 complete pairs", confidence="high")
                case.decide("method", final={"method": "DESeq2", "matrix_type": "raw counts",
                                             "formula": "~ subject + time"},
                            evidence=[aligned], reasoning="paper route", confidence="high")
                case.decide("threshold", final={"paper_threshold": threshold, "threshold_source": "paper",
                                                "applied_threshold": threshold},
                            evidence=[paper], reasoning="Methods", confidence="high")

                def fake_deseq2(output_dir, **_):
                    out = Path(output_dir) / "DEG_results_post_vs_pre.csv"
                    out.parent.mkdir(parents=True, exist_ok=True)
                    pd.DataFrame({"log2FoldChange": [1.0, -0.2, 0.1], "padj": [0.01, 0.5, 0.9]},
                                 index=["g1", "g2", "g3"]).to_csv(out)
                    return "DESeq2 analysis completed successfully!"

                native.call_tool(fake_deseq2, output_dir=str(case.dir / "results"))
                deg = native.deg_outputs(case.dir / "results")[0]
                counts = native.apply_threshold(deg)
                out = case.add_output(deg, "deg_table")
                case.decide("execution", final={"method": "DESeq2", "outputs": [deg]}, evidence=[out],
                            reasoning="ran", confidence="high", execution_status="completed")
                case.decide("study", final={"route": "paper_aligned"}, evidence=[out], reasoning="done",
                            confidence="high")
                row = case.finish(n_deg=counts["n_significant"], deg_sanity=counts["deg_sanity"])
                self.assertEqual(row["status"], "completed")

                stopped = run.case("c2", accession="GSE2")
                meta2 = stopped.add_input(paths["metadata"], "metadata")
                stopped.decide("design", final={}, evidence=[meta2], reasoning="no exercise arm",
                               confidence="high", decision_status="refused", execution_status="not_run",
                               stop_reason="no exercise contrast")
                self.assertEqual(stopped.finish()["status"], "stopped:design")
                result = run.finish()
                self.assertEqual(result["status"], "completed")
                self.assertEqual(result["external_llm_blocked_attempts"], 0)

                from tools.decision_contract import validate
                count, errors = validate(sorted((tmp / "run").rglob("decisions.json")))
                self.assertEqual(errors, [])
                spec = importlib.util.spec_from_file_location(
                    "audit_run", ROOT / ".agents/skills/evaluate-bioinformatics-agent/scripts/audit_run.py")
                audit = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(audit)
                report = audit.audit_run(tmp / "run")
                checks = {c["id"]: c["status"] for c in report["checks"]}
                self.assertEqual(checks["decision_contract"], "pass")
                self.assertEqual(checks["study_completion"], "pass")
                self.assertEqual(checks["matrix_method_compatibility"], "pass")
                self.assertEqual(report["blocking_findings"], [])
                self.assertGreaterEqual(report["coverage"], 60)
        finally:
            if previous is None:
                os.environ.pop(native.NATIVE_ENV, None)
            else:
                os.environ[native.NATIVE_ENV] = previous


class ModalityHelperTests(unittest.TestCase):
    def test_feature_id_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases = {
                "ensembl_gene": [f"ENSMUSG{i:011d}.2" for i in range(50)],
                "ensembl_transcript": [f"ENST{i:011d}" for i in range(50)],
                "affy_probe": [f"{1370000 + i}_at" for i in range(48)] + ["AFFX-BioB-5_at", "1367452_s_at"],
                "gene_symbol": ["Gapdh", "Actb", "ISG15", "MX1", "HLA-A", "H2-K1"] * 8,
                "cpg_probe": [f"cg{i:08d}" for i in range(50)],
                "uniprot": ["P04637", "Q9Y6K9", "O14786", "P68871-2"] * 12,
            }
            for expected, ids in cases.items():
                path = Path(tmp) / f"{expected}.csv"
                pd.DataFrame({"x": range(len(ids))}, index=pd.Index(ids, name="id")).to_csv(path)
                report = native.feature_id_report(path)
                self.assertEqual(report["dominant_type"], expected, report)
                self.assertEqual(report["gene_set_ready"], expected in {"ensembl_gene", "gene_symbol"})

    def test_beta_to_m(self):
        with tempfile.TemporaryDirectory() as tmp:
            beta = pd.DataFrame({"a": [0.5, 0.0, 1.0], "b": [0.2, 0.8, 0.9]}, index=["cg1", "cg2", "cg3"])
            beta.to_csv(Path(tmp) / "beta.csv")
            info = native.beta_to_m(Path(tmp) / "beta.csv", Path(tmp) / "m.csv")
            m = pd.read_csv(info["output"], index_col=0)
            self.assertAlmostEqual(m.loc["cg1", "a"], 0.0, places=6)
            self.assertTrue(np.isfinite(m.to_numpy()).all())
            (beta * 100).to_csv(Path(tmp) / "pct.csv")
            m_pct = pd.read_csv(native.beta_to_m(Path(tmp) / "pct.csv", Path(tmp) / "m2.csv")["output"], index_col=0)
            self.assertTrue(np.allclose(m.to_numpy(), m_pct.to_numpy()))
            pd.DataFrame({"a": [5.0, 300.0], "b": [1.0, 2.0]}).to_csv(Path(tmp) / "bad.csv")
            with self.assertRaises(native.NativeToolError):
                native.beta_to_m(Path(tmp) / "bad.csv", Path(tmp) / "m3.csv")

    def test_nested_failure_and_lazy_import_errors(self):
        native.enable_native_mode()
        self.assertTrue(native.tool_failed("Differential methylation on 900 sites.\n--- limma result ---\n"
                                           "FATAL ERROR: only 2 samples remain"))
        self.assertFalse(native.tool_failed("limma complete\nSummary (padj < 0.05): 12 genes"))

        def lazy():
            import a_package_that_is_not_installed  # noqa: F401
        with self.assertRaises(native.NativeToolError) as raised:
            native.call_tool(lazy)
        self.assertIn("No module named", str(raised.exception))

    def test_environment_failures_make_a_partial_run(self):
        native.enable_native_mode()
        with tempfile.TemporaryDirectory() as tmp:
            run = native.RunRecorder(Path(tmp) / "run", request="r", platform_name="test",
                                     decision_maker="test", case_ids=["c1"])
            self.assertNotIn("enrichment", run.tracker.stages)
            self.assertIn("numpy", run.manifest["packages"])
            case = run.case("c1", "GSE1")
            spec = Path(tmp) / "spec.txt"
            spec.write_text("x", encoding="utf-8")
            item = case.add_input(spec, "user")
            case.decide("execution", final={"method": "DESeq2",
                                            "execution_error": "cannot import tools.deseq2_tools: No module named 'pydeseq2'"},
                        evidence=[item], reasoning="r", confidence="high", execution_status="failed")
            case.finish()
            result = run.finish()
            self.assertEqual(result["status"], "partial")
            status = json.loads((Path(tmp) / "run" / "run_status.json").read_text(encoding="utf-8"))
            self.assertEqual(status["status"], "partial")

    def test_accession_survives_reopen_before_first_record(self):
        # Large run: a case created in one script and first recorded in the next lost its
        # accession (summary.csv showed it empty).
        native.enable_native_mode()
        with tempfile.TemporaryDirectory() as tmp:
            native.RunRecorder(Path(tmp) / "run", request="r", platform_name="test",
                               decision_maker="test", case_ids=["c1"]).case("c1", "GSE1")
            reopened = native.RunRecorder.open(Path(tmp) / "run")
            self.assertEqual(reopened.case("c1").accession, "GSE1")


class RoundThreeFixTests(unittest.TestCase):
    def test_large_linear_values_are_not_integers(self):
        rng = np.random.default_rng(5)
        lfq = pd.DataFrame(2 ** rng.normal(25, 2, (300, 4)), columns=list("abcd"))
        self.assertLess(native._profile(lfq).integer_fraction, 0.01)
        with self.assertRaises(PolicyViolation):
            enforce_method_matrix_compatibility(lfq, method="deseq2")

    def test_collapse_to_genes(self):
        with tempfile.TemporaryDirectory() as tmp:
            deg = pd.DataFrame({"baseMean": [5.0, 9.0, 7.0, 3.0], "stat": [4.0, 1.0, -6.0, 2.0],
                                "padj": [0.01, 0.5, 0.001, 0.2]},
                               index=pd.Index(["ILMN_1", "ILMN_2", "ILMN_3", "ILMN_4"], name="ID_REF"))
            deg.to_csv(Path(tmp) / "deg.csv")
            annotation = pd.DataFrame({"Symbol": ["GENEA", "GENEA", "GENEB", None]},
                                      index=pd.Index(["ILMN_1", "ILMN_2", "ILMN_3", "ILMN_4"], name="ID_REF"))
            annotation.to_csv(Path(tmp) / "matrix.csv")
            info = native.collapse_to_genes(Path(tmp) / "deg.csv", Path(tmp) / "genes.csv",
                                            mapping_csv=Path(tmp) / "matrix.csv", mapping_column="Symbol")
            genes = pd.read_csv(info["output"], index_col=0)
            self.assertEqual(info["n_genes"], 2)
            self.assertEqual(info["n_unmapped"], 1)
            self.assertEqual(genes.loc["GENEA", "source_feature"], "ILMN_2")  # highest baseMean
            info = native.collapse_to_genes(Path(tmp) / "deg.csv", Path(tmp) / "genes2.csv",
                                            mapping_csv=Path(tmp) / "matrix.csv", mapping_column="Symbol",
                                            rule="max_abs_score")
            self.assertEqual(pd.read_csv(info["output"], index_col=0).loc["GENEA", "source_feature"], "ILMN_1")
            self.assertIn("max_abs_score", info["mapping_record"]["rule"])

    def test_complete_pairs_subset(self):
        with tempfile.TemporaryDirectory() as tmp:
            meta = pd.DataFrame({"donor": ["d1", "d1", "d2", "d3", "d3"],
                                 "time": ["pre", "post", "pre", "pre", "post"]},
                                index=["s1", "s2", "s3", "s4", "s5"])
            meta.to_csv(Path(tmp) / "meta.csv")
            pd.DataFrame(np.ones((3, 5)), columns=meta.index, index=["g1", "g2", "g3"]).to_csv(Path(tmp) / "m.csv")
            info = native.complete_pairs_subset(Path(tmp) / "m.csv", Path(tmp) / "meta.csv", Path(tmp) / "out",
                                                subject_column="donor", condition_column="time",
                                                levels=["pre", "post"])
            self.assertEqual(info["n_complete_pairs"], 2)
            self.assertEqual(info["excluded_subjects"]["incomplete"], ["d2"])
            self.assertEqual(list(pd.read_csv(info["matrix"], index_col=0).columns), ["s1", "s2", "s4", "s5"])


if __name__ == "__main__":
    unittest.main()
