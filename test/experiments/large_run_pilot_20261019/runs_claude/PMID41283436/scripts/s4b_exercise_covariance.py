import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
run = native.RunRecorder.open("test/experiments/large_run_pilot_20261019/runs_claude/PMID41283436")
case = run.case("exercise_vs_sedentary_ctrl")
case.decide("covariance", decision_status="refused", execution_status="not_run",
            final={"status": "unresolved", "blocking_terms": [], "covariates": [{"name": "project", "disposition": "aliased"}]},
            evidence=[case.evidence_item("artifact:" + "x") if False else case.add_output(case.dir / "design_checks.json", "design_checks_ref")],
            paper={"locator": "S4.6.p1"}, confidence="high",
            reasoning="confounding_report: project vs grp is complete confounding (p01 only fatctl, p02 only sedctl). No within-batch exercise contrast exists, so the exercise effect cannot be separated from sequencing-project batch.",
            stop_reason="exercise (fatctl vs sedctl) is completely confounded with Admera sequencing project (23263-01 = all fatigued, 23263-02 = all sedentary); the paper never makes this transcriptomic comparison")
