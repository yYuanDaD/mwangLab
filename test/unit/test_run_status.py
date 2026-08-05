import json
import os
import tempfile
import unittest

from tools.run_status import RunStatusTracker


class RunStatusTests(unittest.TestCase):
    def test_persistent_stage_and_final_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "run_status.json")
            tracker = RunStatusTracker(path, run_id="r1", profile="geo_batch",
                                       stages=["acquire", "analyze"], study_total=2)
            tracker.start("starting")
            tracker.begin_study("GSE1", 1)
            tracker.set_stage("acquire", current_tool="download_geo_data")
            tracker.set_stage("analyze", evidence_ids=["DEC-0001"])
            tracker.add_warning("low coverage")
            tracker.finish("partial", "one warning")
            with open(path, encoding="utf-8") as fh:
                status = json.load(fh)
        self.assertEqual(status["status"], "partial")
        self.assertEqual(status["stage_index"], 2)
        self.assertEqual(status["completed_stages"], ["acquire", "analyze"])
        self.assertEqual(status["warning_count"], 1)
        self.assertEqual(status["evidence_ids"], ["DEC-0001"])
        self.assertIsNotNone(status["finished_at"])

    def test_waiting_approval_and_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            tracker = RunStatusTracker(os.path.join(tmp, "status.json"), run_id="r2", profile="bulk")
            tracker.start()
            tracker.waiting_approval("choose contrast")
            self.assertEqual(tracker.state.status, "waiting_approval")
            tracker.resume()
            self.assertEqual(tracker.state.status, "running")


if __name__ == "__main__":
    unittest.main()
