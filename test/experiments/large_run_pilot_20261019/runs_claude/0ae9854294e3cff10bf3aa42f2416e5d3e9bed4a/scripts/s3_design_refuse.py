import sys, os, json; sys.path.insert(0, r"E:\agent\mwangLab_pdf"); os.chdir(r"E:\agent\mwangLab_pdf")
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/0ae9854294e3cff10bf3aa42f2416e5d3e9bed4a"
run = native.RunRecorder.open(RUN); case = run.case("case_01")
paper = case.evidence_item("paper:PMC10597580.paper.md")
dm = case.evidence_item("tool_output:design_metadata.csv")
meta = case.evidence_item("metadata:GSE152133_metadata.csv")
disc = [{"item": "requested estimand", "paper": "aging (6m vs 24m/28m) and DEG~CFAB association; no exercise intervention",
         "data": "factors are age (m6/m24/m28) and sequencing run only", "consequence": "exercise effect not identifiable"},
        {"item": "library count", "paper": "22 RNA samples, 6m libraries prepared twice (S2.4.p1)",
         "data": "29 GSMs = 7 m6 run1 + 7 m6 run2 (_repeat) + 7 m24 run1 + 8 m28 run2", "consequence": "consistent"}]
case.write_json("paper_data_discrepancies.json", disc)
case.decide("design", final={}, evidence=[paper, dm, meta], confidence="high", paper={"locator": "S2.1.p1"},
    decision_status="refused", execution_status="not_run",
    candidates=[{"value": "age: m28 vs m6 (run2), m24 vs m6 (run1) -- the paper's DESeq2 contrasts",
                 "reason_rejected": "answers aging, not exercise; no animal was exercise-trained or sedentary-controlled"},
                {"value": "CFAB score / exercise-capacity regression (S3.2.p2)",
                 "reason_rejected": "associational function score measured on all mice, restricted to age DEGs; not an exercise intervention contrast"}],
    stop_reason="no exercise contrast in the sequenced samples: GSE152133 is a cross-sectional aging study "
                "(male C57BL/6 TA muscle at 6, 24, 28 months); exercise appears only as part of the CFAB functional "
                "test battery given to every mouse (S2.2.p1) and in discussion of external datasets (S5.8.p2)",
    reasoning="Requested estimand (exercise effect on expression) has no arm in the data; the paper's own contrasts are age contrasts.")
print(case.finish())
print(run.finish())
