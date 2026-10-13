"""Decision traces: tools/native.py writes trace.jsonl; scripts/analyze_traces.py summarizes it."""
import csv
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools import native  # noqa: E402

spec = importlib.util.spec_from_file_location("analyze_traces", ROOT / "scripts" / "analyze_traces.py")
analyze_traces = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze_traces)

THRESHOLD = {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None}


def _files(tmp: Path) -> dict:
    samples = [f"S{i}" for i in range(6)]
    pd.DataFrame({s: [10 + i, 20, 30 + 2 * i, 5] for i, s in enumerate(samples)},
                 index=["g1", "g2", "g3", "g4"]).to_csv(tmp / "matrix.csv")
    pd.DataFrame({"group": ["ctrl"] * 3 + ["ex"] * 3, "batch": ["a", "b", "a", "b", "a", "b"]},
                 index=pd.Index(samples, name="sample")).to_csv(tmp / "meta.csv")
    (tmp / "paper.md").write_text("Methods: DESeq2, FDR < 0.05.", encoding="utf-8")
    return {"matrix": tmp / "matrix.csv", "metadata": tmp / "meta.csv", "paper": tmp / "paper.md"}


class DecisionTraceTests(unittest.TestCase):
    def setUp(self):
        self.previous = os.environ.get(native.NATIVE_ENV)
        native.enable_native_mode()

    def tearDown(self):
        if self.previous is None:
            os.environ.pop(native.NATIVE_ENV, None)
        else:
            os.environ[native.NATIVE_ENV] = self.previous

    def test_trace_records_calls_decisions_and_hesitation(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            files = _files(tmp)
            run = native.RunRecorder(tmp / "run", request="trace test", platform_name="unit-test",
                                     decision_maker="unit test", case_ids=["c1", "c2"])
            case = run.case("c1", accession="GSE1")
            paper = case.add_input(files["paper"], "paper")
            meta = case.add_input(files["metadata"], "metadata")
            mat = case.add_input(files["matrix"], "matrix")
            case.decide("paper_reconstruction", final={
                "accessions": ["GSE1"], "primary_estimand": "exercise vs control",
                "planned_contrasts": ["ex vs ctrl"], "paper_threshold": THRESHOLD},
                evidence=[paper], reasoning="Methods section", confidence="high")
            native.profile_matrix(files["matrix"])
            native.confounding_report(files["metadata"], "group", ["batch"])

            def broken(**_):
                return "FATAL ERROR: something the agent passed was wrong"

            with self.assertRaises(native.NativeToolError):
                native.call_tool(broken, output_dir=str(tmp / "out"))
            with self.assertRaises(native.NativeToolError):  # rejected: required fields missing
                case.decide("matrix", final={}, evidence=[mat], reasoning="x", confidence="high")
            case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2"},
                        evidence=[mat], reasoning="integers", confidence="high")
            case.decide("design", final={"analysis_type": "two-group", "design_column": "group",
                                         "control": "ex", "treatment": "ctrl"},
                        evidence=[meta], reasoning="first reading of the labels", confidence="low")
            case.decide("design", final={"analysis_type": "two-group", "design_column": "group",
                                         "control": "ctrl", "treatment": "ex"},
                        evidence=[meta, paper], reasoning="paper names ctrl as the reference",
                        confidence="high")
            native.note("re-read the paper before fixing the reference level", stage="design")

            stopped = run.case("c2", accession="GSE2")
            meta2 = stopped.add_input(files["metadata"], "metadata")
            stopped.decide("covariance", final={}, evidence=[meta2], reasoning="batch aliased with group",
                           confidence="high", decision_status="refused", execution_status="not_run",
                           stop_reason="batch completely aliased with the exercise arm")
            stopped.finish()
            run.finish()
            self.assertIsNone(native._ACTIVE_RUN)

            events = [json.loads(line) for line in
                      (tmp / "run" / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
            kinds = [e["kind"] for e in events]
            self.assertEqual(kinds[0], "run_start")
            self.assertEqual(kinds[-1], "run_finish")
            self.assertEqual([e["seq"] for e in events], list(range(1, len(events) + 1)))
            calls = [e for e in events if e["kind"] == "call"]
            self.assertEqual([c["name"] for c in calls],
                             ["profile_matrix", "confounding_report", "tool:broken"])
            self.assertTrue(calls[0]["ok"])
            self.assertEqual(calls[0]["args"]["path"], "matrix.csv")  # file name, not full path
            self.assertFalse(calls[2]["ok"])
            self.assertIn("FATAL ERROR", calls[2]["error"])
            rejected = [e for e in events if e["kind"] == "decision_rejected"]
            self.assertEqual(len(rejected), 1)
            self.assertEqual(rejected[0]["stage"], "matrix")
            revised = [e for e in events if e["kind"] == "decision" and e["stage"] == "design"]
            self.assertEqual([e["revision"] for e in revised], [0, 1])
            self.assertEqual(revised[1]["changed"], ["control", "treatment"])
            self.assertTrue(all(e["case"] == "c1" for e in calls))
            self.assertIn("note", kinds)
            finish = [e for e in events if e["kind"] == "case_finish"]
            self.assertEqual(finish[0]["case"], "c2")
            self.assertEqual(finish[0]["status"], "stopped:covariance")

            out = tmp / "analysis"
            self.assertEqual(analyze_traces.main([str(tmp), "--out", str(out)]), 0)
            summary = json.loads((out / "trace_summary.json").read_text(encoding="utf-8"))
            stages = {s["stage"]: s for s in summary["stages"]}
            self.assertEqual(stages["design"]["revised_cases"], 1)
            self.assertEqual(stages["design"]["changed_fields"], {"control": 1, "treatment": 1})
            self.assertEqual(stages["matrix"]["rejected_records"], 1)
            self.assertEqual(summary["stops"][0]["stage"], "covariance")
            self.assertEqual(summary["first_pass_cases"], 1)  # c2 only; c1 was revised and rejected
            signals = {(h["case"], h["stage"], h["signal"]) for h in summary["hotspots"]}
            self.assertIn(("c1", "design", "revised"), signals)
            self.assertIn(("c1", "design", "low_confidence"), signals)
            self.assertIn(("c1", "matrix", "rejected_record"), signals)
            tools = {t["tool"]: t for t in summary["tools"]}
            self.assertEqual(tools["tool:broken"]["errors"], 1)
            with open(out / "review_sheet.csv", encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 5)  # 4 accepted records in c1, 1 in c2
            self.assertEqual(rows[0]["stage"], "paper_reconstruction")
            self.assertEqual({r["reviewer_correct"] for r in rows}, {""})
            self.assertIn("## Where the agent hesitated", (out / "trace_summary.md").read_text(encoding="utf-8"))

    def test_untraced_runs_still_contribute_decisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            files = _files(tmp)
            run = native.RunRecorder(tmp / "run", request="r", platform_name="t", decision_maker="t",
                                     case_ids=["c1"])
            case = run.case("c1")
            meta = case.add_input(files["metadata"], "metadata")
            case.decide("design", final={}, evidence=[meta], reasoning="no exercise arm",
                        confidence="medium", decision_status="refused", execution_status="not_run",
                        stop_reason="no exercise contrast")
            run.finish()
            (tmp / "run" / "trace.jsonl").unlink()
            summary, rows = analyze_traces.analyze(analyze_traces.find_runs([tmp]))
            self.assertEqual(summary["n_traced_runs"], 0)
            self.assertEqual(summary["n_cases"], 1)
            self.assertEqual(summary["stops"][0]["reason"], "no exercise contrast")
            self.assertEqual(len(rows), 1)

    def test_separate_methods_and_subsets_are_not_revisions(self):
        self.assertNotEqual(native.decision_slot("enrichment", {"method": "ORA (Enrichr GO/KEGG)"}),
                            native.decision_slot("enrichment", {"method": "GSEA preranked Hallmark"}))
        self.assertNotEqual(native.decision_slot("execution", {"subset": "CD14 monocyte"}),
                            native.decision_slot("execution", {"subset": "CD4 T cell"}))
        self.assertEqual(native.decision_slot("design", {"control": "a"}),
                         native.decision_slot("design", {"control": "b"}))
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "run"
            (run / "c1").mkdir(parents=True)
            (run / "run_manifest.json").write_text("{}", encoding="utf-8")
            base = {"decision_status": "valid", "execution_status": "completed", "confidence": "high",
                    "reasoning": "r", "evidence": []}
            records = [
                {**base, "stage": "execution", "final": {"method": "limma", "subset": "A"}},
                {**base, "stage": "execution", "final": {"method": "limma", "subset": "B"}},
                {**base, "stage": "enrichment", "final": {"method": "ORA (Enrichr GO/KEGG)"}},
                {**base, "stage": "enrichment", "final": {"method": "GSEA preranked Hallmark"}},
                {**base, "stage": "enrichment", "final": {"method": "GSEA preranked Hallmark",
                                                          "ranking_metric": "stat"}},
            ]
            (run / "c1" / "decisions.json").write_text(json.dumps(records), encoding="utf-8")
            summary, _ = analyze_traces.analyze([run])
            stages = {s["stage"]: s for s in summary["stages"]}
            self.assertEqual(stages["execution"]["revised_cases"], 0)
            self.assertEqual(stages["execution"]["cases"], 1)
            self.assertEqual(stages["enrichment"]["revised_cases"], 1)  # only the GSEA re-record
            self.assertEqual(stages["enrichment"]["changed_fields"], {"ranking_metric": 1})

    def test_tracing_never_breaks_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            files = _files(tmp)
            native.RunRecorder(tmp / "gone", request="r", platform_name="t", decision_maker="t")
            import shutil
            shutil.rmtree(tmp / "gone")
            self.assertIn("candidates", native.profile_matrix(files["matrix"]))
            self.assertIsNone(native._ACTIVE_RUN)


if __name__ == "__main__":
    unittest.main()
