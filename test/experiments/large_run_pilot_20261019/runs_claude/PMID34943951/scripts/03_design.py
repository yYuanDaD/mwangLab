import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID34943951"
run = native.RunRecorder.open(RUN); case = run.case("GSE188236")
# Continues 02_gates.py, which recorded paper_reconstruction..matrix and then crashed in case.suitability (sex check).
E = case.evidence_item
paper, meta = E("paper:PMC8700369.paper.md"), E("metadata:GSE188236_metadata.csv")
amd = E("tool_output:design_metadata.csv")
adir = case.dir / "aligned"
# ---------- design: suitability, then refusal
dm = pd.read_csv(adir / "design_metadata.csv", index_col=0)
# matrix_csv omitted: tools/suitability.py:367 check_sex raises IndexError when metadata has no sex column
rep, item, summary = case.suitability(matrix_type="normalized counts", metadata=dm, factors=["trt"],
    organism="Human", subject=None, planned=[])
summary = dict(summary, sex_check="skipped: check_sex crashes without a metadata sex column (tools/suitability.py:367); cultured cells from 5 donors, sex not reported")
print(json.dumps(summary, default=str)[:2500])
comps = [c.get("name") for c in rep.get("comparisons", [])]
print(comps)
case.decide("design", final={"suitability": summary, "available_contrasts": comps},
    evidence=[paper, meta, amd, item], paper={"locator": "S2.5.p1"}, confidence="high",
    candidates=[{"value": "trt: tgfb vs ctrl", "reason_rejected": "TGF-beta1 treatment of cultured myotubes is not exercise; answering the exercise request with it would change the estimand"},
                {"value": "trt: tgfbsb vs tgfb", "reason_rejected": "pharmacological inhibitor contrast, not exercise"},
                {"value": "post vs pre training, LRE vs RE (paper's exercise analysis)", "reason_rejected": "samples are in GSE72462/GSE161749 microarrays, not in GSE188236"}],
    decision_status="refused",
    stop_reason="GSE188236 contains only cultured primary human myotubes treated with vehicle, TGF-beta1, or TGF-beta1+SB431542 (in-vitro arm of the paper, S2.4.p1/S3.1.p1). It has no exercise, training, or responder factor, so it cannot identify how exercise affects gene expression. The paper's exercise analysis (8-week endurance training, pre/post biopsies, responders vs low responders) uses microarrays GSE72462 and GSE161749 (S2.5.p1), outside this request.",
    reasoning="Refused at design: the requested estimand (exercise effect) is not present in the sequenced samples. The in-vitro TGF-beta1 contrasts are analyzable but answer a different question.")
case.write_json("reproduction_plan.json", {"route": "stopped at design (refused)", "reason": "no exercise contrast in GSE188236",
    "possible_follow_up": "analyze GSE72462 + GSE161749 (microarray, paired limma, post vs pre and LRE vs RE) for the exercise question; or run TGF-beta1 vs vehicle on GSE188236 as a separate non-exercise request"})
case.write_json("reproduction_summary.json", {"status": "refused", "gate": "design", "n_deg": None,
    "paper_counts_not_compared": {"tgfb_vs_ctrl_long": 2066, "tgfb_sb_vs_tgfb_long": 1900}})
print(case.finish())
print(run.finish())
