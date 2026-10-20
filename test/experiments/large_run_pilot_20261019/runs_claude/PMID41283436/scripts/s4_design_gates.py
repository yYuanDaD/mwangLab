import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41283436"
run = native.RunRecorder.open(RUN)
PJ_ID = "paper:PMC12641718.paper.json"
thr = {"metric": "padj", "adjustment": "not_reported", "cutoff": 0.05, "effect_metric": None,
       "effect_cutoff": None, "inclusive": False, "source_locator": "S4.9.p1"}
CONF_CANDS = ["project", "characteristics_ch1.1.genotype", "characteristics_ch1.0.tissue", "instrument_model", "platform_id"]
for cid, ctrl, trt, loc in [("fatigued_pbmt_vs_ctrl", "fatctl", "fatpbm", "S2.3.p1"),
                            ("sedentary_pbmt_vs_ctrl", "sedctl", "sedpbm", "S2.1.p1"),
                            ("exercise_vs_sedentary_ctrl", "sedctl", "fatctl", "S4.6.p1")]:
    case = run.case(cid)
    ev = {i["kind"]: i for i in []}
    dm = case.dir / "aligned" / "derived_metadata.csv"
    am = case.dir / "aligned" / "aligned_matrix.csv"
    prof = case.add_output(case.dir / "matrix_profile.json", "matrix_profile")
    dme = case.add_output(dm, "design_metadata")
    paper = case.evidence_item(PJ_ID)
    case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
                                 "evidence": "integer_fraction=1.0, no negatives, max ~3.6e6; per-sample files *_count.txt.gz; GEO data_processing: STAR + featureCounts/HTSeq gene counts, GRCm38 Ensembl gene IDs"},
                evidence=[prof, case.evidence_item("metadata:GSE297318_metadata.csv")], paper={"locator": "S4.9.p1"}, confidence="high",
                reasoning="Values are integer read counts consistent with featureCounts/HTSeq output; the paper used DESeq2, which needs raw counts.")
    dc = native.design_check(dm, ["grp"])
    cr = native.confounding_report(dm, "grp", candidates=CONF_CANDS)
    print(cid, json.dumps(dc, default=str)[:400]); print([ (r.get("column"), r.get("relation")) for r in cr])
    case.write_json("design_checks.json", {"design_check": dc, "confounding": cr})
    if cid != "exercise_vs_sedentary_ctrl":
        case.decide("design", final={"analysis_type": "two_group", "design_column": "grp", "control": ctrl, "treatment": trt,
                                     "formula": "~ grp", "n_per_arm": 6},
                    candidates=[{"value": "one 2x2 model (PBMT x exercise) on all 24 samples", "reason_rejected": "paper analysed each Admera project separately (S4.6.p1); exercise arm aliased with sequencing project, so a pooled model would borrow dispersion across batches and deviate from the paper"}],
                    evidence=[paper, dme], paper={"locator": loc}, confidence="high",
                    reasoning=f"Paper contrast {trt} vs {ctrl} within one sequencing project, 6 vs 6 independent mice.")
        case.decide("covariance", final={"status": "not_required", "blocking_terms": [],
                                         "covariates": [{"name": "project", "disposition": "excluded: single level within case"},
                                                        {"name": "genotype", "disposition": "excluded: single level (WT)"},
                                                        {"name": "run_duration", "disposition": "excluded: not in GEO metadata; paper reports it only per group"}]},
                    evidence=[dme, case.add_output(case.dir / "design_checks.json", "design_checks")], paper={"locator": "S4.3.p1"}, confidence="high",
                    reasoning="Different mice per group (S4.3.p1), no pairing key; no metadata covariate varies within the case; design full rank.")
        case.decide("method", final={"method": "DESeq2 (pydeseq2 implementation)", "matrix_type": "raw counts", "formula": "~ grp",
                                     "paper_method": "DESeq2 1.4.1 (R)", "implementation_note": "pydeseq2 Python port; Wald test, BH padj"},
                    evidence=[paper, prof], paper={"locator": "S4.9.p1"}, confidence="high",
                    reasoning="Paper route DESeq2 on raw counts is runnable on the deposited counts.")
        case.decide("threshold", final={"paper_threshold": thr, "threshold_source": "paper",
                                        "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None, "inclusive": False}},
                    evidence=[paper], paper={"locator": "S4.9.p1"}, confidence="high",
                    reasoning="Paper: significance reported as adjusted p-value < 0.05; no fold-change cutoff stated, none added.")
    else:
        case.decide("design", final={"analysis_type": "two_group", "design_column": "grp", "control": "sedctl", "treatment": "fatctl",
                                     "formula": "~ grp", "paper_planned": False,
                                     "note": "direct effect of acute exhaustive exercise in non-irradiated controls; not a paper contrast"},
                    evidence=[paper, dme], paper={"locator": "S4.6.p1"}, confidence="medium",
                    reasoning="The request asks how exercise affects expression; the only exercise contrast in the sequenced samples is fatigued control vs sedentary control. Checked for identifiability at covariance.")
        case.decide("covariance", decision_status="refused", execution_status="not_run",
                    final={"status": "unresolved", "blocking_terms": [],
                           "covariates": [{"name": "project", "disposition": "aliased"}]},
                    evidence=[dme, case.add_output(case.dir / "design_checks.json", "design_checks")], paper={"locator": "S4.6.p1"}, confidence="high",
                    stop_reason="exercise (fatctl vs sedctl) is completely confounded with Admera sequencing project (23263-01 = all fatigued, 23263-02 = all sedentary; separate libraries/sequencing runs); the paper never makes this transcriptomic comparison")
