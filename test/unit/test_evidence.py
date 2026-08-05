import json
import os
import tempfile
import unittest

from tools.evidence import EvidenceRecorder
from tools.batch_tools import _DecisionLog


class EvidenceTests(unittest.TestCase):
    def test_bundle_round_trip_and_reference_integrity(self):
        rec = EvidenceRecorder("run-1", subject_id="GSE1")
        src = rec.add_source("metadata", "GEO metadata", uri="data/GSE1/meta.csv")
        dec = rec.add_decision("design", "treated_vs_control", method="rule", evidence_ids=[src])
        rec.add_claim("GSE1", "contrast", "treated_vs_control", "Selected contrast",
                      method="rule", evidence_ids=[src], status="inferred")
        rec.add_artifact("missing.csv", "deg_results", produced_by=dec, evidence_ids=[src])
        rec.finish("success")
        with tempfile.TemporaryDirectory() as tmp:
            path = rec.save(os.path.join(tmp, "evidence.json"))
            with open(path, encoding="utf-8") as fh:
                payload = json.load(fh)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["subject_id"], "GSE1")
        self.assertEqual(payload["decisions"][0]["evidence_ids"], [src])

    def test_dangling_reference_is_rejected(self):
        rec = EvidenceRecorder("run-2")
        rec.add_decision("x", "y", evidence_ids=["SRC-9999"])
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "dangling"):
                rec.save(os.path.join(tmp, "evidence.json"))

    def test_batch_decision_log_emits_unified_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact = os.path.join(tmp, "deg.csv")
            with open(artifact, "w", encoding="utf-8") as fh:
                fh.write("gene,padj\nA,0.01\n")
            decisions_path = os.path.join(tmp, "decisions.json")
            log = _DecisionLog("GSE_TEST")
            log.record("auto_design_python", "match", reason="keyword-grounded",
                       design_column="group")
            log.record("deseq2", "ok", reason="fit completed", deg_file=artifact)
            log.save(decisions_path, status="success")

            with open(decisions_path, encoding="utf-8") as fh:
                legacy = json.load(fh)
            with open(os.path.join(tmp, "evidence.json"), encoding="utf-8") as fh:
                evidence = json.load(fh)

        self.assertEqual(legacy["schema_version"], "1.0")
        self.assertTrue(legacy["evidence_file"].endswith("evidence.json"))
        self.assertEqual(len(evidence["decisions"]), 2)
        self.assertEqual(evidence["decisions"][0]["method"], "rule")
        self.assertEqual(evidence["decisions"][1]["method"], "computation")
        self.assertEqual(evidence["artifacts"][0]["role"], "deg_file")
        self.assertIsNotNone(evidence["artifacts"][0]["sha256"])


if __name__ == "__main__":
    unittest.main()
