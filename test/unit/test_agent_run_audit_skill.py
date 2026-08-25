"""Offline tests for the repository-local agent evaluation skill."""

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents" / "skills" / "evaluate-bioinformatics-agent" / "scripts" / "audit_run.py"
SPEC = importlib.util.spec_from_file_location("agent_run_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AgentRunAuditTests(unittest.TestCase):
    def test_complete_grounded_run_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifact = root / "deg.csv"
            artifact.write_text("gene,log2FoldChange,padj\nA,2,0.01\n", encoding="utf-8")
            digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            (root / "run_status.json").write_text(json.dumps({
                "status": "completed", "stage": "completed", "finished_at": "2026-01-01T00:00:00",
                "stage_total": 2, "completed_stages": ["analyze", "report"],
                "elapsed_seconds": 1.2, "llm_calls": 0, "estimated_cost_usd": 0,
                "failure_count": 0, "warning_count": 0,
            }), encoding="utf-8")
            with (root / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=[
                    "status", "matrix_type", "da_method", "n_deg", "design_col",
                    "control", "treatment", "deg_sanity",
                ])
                writer.writeheader()
                writer.writerow({"status": "deg_ok", "matrix_type": "raw_counts",
                                 "da_method": "deseq2", "n_deg": "1", "design_col": "condition",
                                 "control": "control", "treatment": "treated", "deg_sanity": "ok"})
            (root / "workflow.log").write_text("done\n", encoding="utf-8")
            study = root / "GSE1"
            study.mkdir()
            (study / "evidence.json").write_text(json.dumps({
                "sources": [{"source_id": "SRC-0001"}],
                "claims": [{"claim_id": "CLM-0001", "evidence_ids": ["SRC-0001"]}],
                "decisions": [{"decision_id": "DEC-0001", "evidence_ids": ["SRC-0001"]}],
                "artifacts": [{"artifact_id": "ART-0001", "path": str(artifact),
                               "produced_by": "DEC-0001", "evidence_ids": ["SRC-0001"],
                               "sha256": digest}],
            }), encoding="utf-8")

            report = MODULE.audit_run(root)
            self.assertEqual(report["verdict"], "pass")
            self.assertGreaterEqual(report["score"], 85)
            self.assertGreaterEqual(report["coverage"], 80)
            self.assertEqual(report["blocking_findings"], [])

    def test_missing_evidence_is_not_false_confidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "run_status.json").write_text(json.dumps({
                "status": "completed", "stage": "completed", "finished_at": "2026-01-01T00:00:00",
                "stage_total": 1, "completed_stages": ["report"],
                "elapsed_seconds": 1, "llm_calls": 1, "estimated_cost_usd": 0.01,
                "failure_count": 0, "warning_count": 0,
            }), encoding="utf-8")
            report = MODULE.audit_run(root)
            self.assertEqual(report["verdict"], "insufficient_evidence")
            self.assertLess(report["coverage"], 60)

    def test_hash_mismatch_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifact = root / "result.csv"
            artifact.write_text("x\n1\n", encoding="utf-8")
            (root / "evidence.json").write_text(json.dumps({
                "sources": [{"source_id": "SRC-0001"}], "claims": [],
                "decisions": [{"decision_id": "DEC-0001", "evidence_ids": ["SRC-0001"]}],
                "artifacts": [{"artifact_id": "ART-0001", "path": str(artifact),
                               "produced_by": "DEC-0001", "evidence_ids": ["SRC-0001"],
                               "sha256": "0" * 64}],
            }), encoding="utf-8")
            report = MODULE.audit_run(root)
            check = next(item for item in report["checks"] if item["id"] == "artifact_integrity")
            self.assertEqual(check["status"], "fail")
            self.assertTrue(check["blocking"])
            self.assertEqual(report["verdict"], "fail")

    def test_failed_terminal_status_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "run_status.json").write_text(json.dumps({
                "status": "failed", "stage": "failed", "finished_at": "2026-01-01T00:00:00",
                "stage_total": 2, "completed_stages": ["analyze"],
                "elapsed_seconds": 1, "llm_calls": 0, "estimated_cost_usd": 0,
                "failure_count": 1, "warning_count": 0,
            }), encoding="utf-8")
            report = MODULE.audit_run(root)
            terminal = next(item for item in report["checks"] if item["id"] == "run_terminal")
            self.assertEqual(terminal["status"], "fail")
            self.assertEqual(report["verdict"], "fail")


if __name__ == "__main__":
    unittest.main()
