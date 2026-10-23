"""Gates 5-8 (design, covariance, method, threshold) for every tissue case. Continues the run
with RunRecorder.open. Writes per-case comparison plans (plan_A.json time-independent,
plan_B.json time-specific) that 04_execute.py runs."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import os, json
from common import *
os.chdir(ROOT)
import pandas as pd
from tools import native
from tools import suitability as su

native.enable_native_mode()
run = native.RunRecorder.open(RUN)
# Sex-check mismatches inspected by hand (suitability/<matrix>_sex_check.tsv): resolution per sample.
SEX_RESOLVED = {
    "GSM7778285": ("QUA male Control ZT05 rep1: Y-gene signal 3.6 log units (every female 0.0) with Xist 4.9; a male "
                   "sample with female RNA admixture, not a label swap. Kept as male; flagged."),
}
REFS = {"sex": "F", "trt": "ctrl", "zt": "zt05"}
only = sys.argv[1:] or list(TISSUES)

for cid in only:
    tissue = TISSUES[cid]
    case = run.case(cid)
    adir = case.dir / "aligned"
    dpath = adir / "design_metadata.csv"
    mpath = adir / "aligned_matrix.csv"
    dm = pd.read_csv(dpath, index_col=0)
    design_ev = case.add_output(dpath, "design_metadata")
    paper_ev = {"id": "paper:PMC11378950", "kind": "paper", "path": PAPER_JSON}
    sexes = sorted(dm["sex"].unique())
    two_sex = len(sexes) == 2
    facA = ["sex", "trt"] if two_sex else ["trt"]
    facB = ["sex", "trt", "zt"] if two_sex else ["trt", "zt"]

    def nm(where):
        return "trt_def_vs_ctrl" + "".join(f"_{k}-{v}" for k, v in where)
    plannedA = [nm([("sex", s)]) for s in sexes] if two_sex else [nm([])]
    plannedB = [nm(([("sex", s)] if two_sex else []) + [("zt", z)]) for s in sexes for z in ("zt05", "zt17")]

    # Library-name style (proxy for sequencing submission/run) vs the design factors.
    conf_sex = native.confounding_report(dm, "sex", ["libstyle"])[0]["status"] if two_sex else "single_sex"
    conf_trt = native.confounding_report(dm, "trt", ["libstyle"])[0]["status"]
    style_aliased_with_sex = two_sex and pd.crosstab(dm["libstyle"], dm["sex"]).gt(0).sum(axis=1).max() == 1 \
        and dm["libstyle"].nunique() > 1

    rep, item, summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=facB, matrix_csv=str(mpath),
                                          organism="Mouse", subject=None, references=REFS, planned=plannedB,
                                          covariate_candidates=[] if style_aliased_with_sex else ["libstyle"])
    sexchk = rep["checks"].get("sex", {})
    unresolved = [g for g in (sexchk.get("mismatched") or []) if g not in SEX_RESOLVED]
    if unresolved:
        raise SystemExit(f"{cid}: sex mismatch {unresolved} - resolve before design")

    compsA = su.enumerate_comparisons(dm, facA, references=REFS)
    compsB = rep["comparisons"]
    # Keep comparisons that answer the request or describe its structure; drop sex main effects
    # where sex is aliased with the library-name style (possible sequencing batch).
    def keep(c):
        if style_aliased_with_sex and c["kind"] == "simple" and c["factor"] == "sex":
            return False
        return True
    planA = [dict(c, planned=c["name"] in plannedA) for c in compsA if keep(c)]
    planB = [dict(c, planned=c["name"] in plannedB) for c in compsB if keep(c)]
    dropped = [c["name"] for c in compsA + compsB if not keep(c)]
    small = []
    for c in planB:  # small n alone is not a stop: run planned contrasts, label them exploratory
        if c["planned"] and not c["analyzable"]:
            c["analyzable"] = True
            c["forced_small_n"] = True
            small.append(c["name"])
    (case.dir / "plan_A.json").write_text(json.dumps(planA, indent=1), encoding="utf-8")
    (case.dir / "plan_B.json").write_text(json.dumps(planB, indent=1), encoding="utf-8")
    pA = case.add_output(case.dir / "plan_A.json", "comparison_plan_time_independent")
    pB = case.add_output(case.dir / "plan_B.json", "comparison_plan_time_specific")

    case.decide("design", final={
        "analysis_type": "multi-factor (sex x treatment x ZT), between-animal, one DESeq2 model per tissue and analysis",
        "formula": "model A: ~ cell (cell = sex x trt); model B: ~ cell (cell = sex x trt x zt)" if two_sex
                   else "model A: ~ cell (cell = trt); model B: ~ cell (cell = trt x zt)",
        "factors": {"A_time_independent": facA, "B_time_specific": facB},
        "references": REFS,
        "contrasts": {"planned_A": plannedA, "planned_B": plannedB,
                      "exploratory_A": [c["name"] for c in planA if not c["planned"]],
                      "exploratory_B": [c["name"] for c in planB if not c["planned"]],
                      "not_run": dropped + [c["name"] for c in planB if not c["analyzable"]]},
        "planned_small_n_run_as_exploratory": small,
        "estimand_type": "causal (randomized high vs low workload), estimand = exercise-linked energy deficiency vs low-workload exercise",
        "suitability": summary,
        "suitability_note": ("libstyle not passed as a covariate candidate: it is aliased with sex (a stratum, not the contrast); the suitability covariance check would otherwise fail the whole case. Sex main-effect comparisons are dropped instead." if style_aliased_with_sex else "libstyle passed as a covariate candidate"),
        "sex_check": {k: sexchk.get(k) for k in ("status", "summary", "predicted", "mismatched")},
        "sex_mismatch_resolution": {g: SEX_RESOLVED[g] for g in (sexchk.get("mismatched") or [])},
    }, evidence=[design_ev, item, pA, pB, paper_ev], paper={"locator": "S4.3.13.p1"}, confidence="medium",
        candidates=[{"value": "~ zt + cell(sex x trt) for the time-independent contrast",
                     "reason_rejected": "paper analysed 'irrespective of the time of day' (S2.3.p1) and reports no ZT term; ZT effects are balanced across arms so no bias"},
                    {"value": "separate DESeq2 per sex", "reason_rejected": "paper normalized per tissue with both sexes together (S4.3.12.p1)"},
                    {"value": "two-group executor (run_deseq2_analysis) per contrast", "reason_rejected": "refits on the two arms only; joint model keeps the per-tissue dispersion fit"}],
        reasoning=("Randomized high vs low workload (S4.2.2.p1). Paper: DESeq2 per tissue, contrasts by sex, energy deficiency and ZT; main "
                   "results per sex irrespective of ZT (FIG3A), plus ZT-specific contrasts (Table S5). Model A pools ZT; model B uses all "
                   "8 cells. Planned = Deficient vs Control within sex (A) and within sex x ZT (B); other comparisons from the suitability "
                   f"report are exploratory. Library-name style aliased with sex: {bool(style_aliased_with_sex)} (sex main-effect comparisons "
                   "dropped then)."))

    dcA = native.design_check(dm, facA)
    dcB = native.design_check(dm, facB)
    case.decide("covariance", final={
        "status": "not_required", "blocking_terms": [],
        "covariates": [
            {"name": "mouse", "disposition": "excluded: one sample per mouse within a tissue (identifier, not a block)"},
            {"name": "zt", "disposition": "excluded from model A (paper pools ZT); a design factor in model B"},
            {"name": "libstyle", "disposition": (f"excluded: library-name format is only a proxy for sequencing run, not a stated batch, "
                                                  f"and the paper did not model it; vs trt: {conf_trt}; vs sex: {conf_sex}"
                                                  + ("; aliased with sex, so sex main-effect comparisons are not run" if style_aliased_with_sex else ""))},
            {"name": "estrous stage", "disposition": "excluded: not in GEO; paper notes control females mostly estrus, deficient mostly diestrus (S3.1.p1)"},
        ],
        "design_check": {"A": {k: dcA.get(k) for k in ("rank", "full_rank", "residual_df", "min_cell_size")},
                         "B": {k: dcB.get(k) for k in ("rank", "full_rank", "residual_df", "min_cell_size")}},
    }, evidence=[design_ev, item], paper={"locator": "S4.3.13.p1"}, confidence="medium",
        reasoning="Between-animal design within a tissue; no repeated measure. Both cell-means designs are full rank with positive residual df.")

    case.decide("method", final={
        "method": "DESeq2 (pydeseq2 joint cell-means model, tools.joint_contrasts.run_joint_deseq2)",
        "matrix_type": "raw counts",
        "formula": "~ cell",
        "formula_A": "~ cell (" + " x ".join(facA) + ")", "formula_B": "~ cell (" + " x ".join(facB) + ")",
        "gene_filter": "keep genes whose mean deposited normalized count (per-tissue DESeq2 median-of-ratios) over the tissue's samples is >= 10 (S4.3.13.p1)",
        "independent_filtering": "pydeseq2 default", "cooks_refit": True,
        "paper_route": {"method": "DESeq2 v1.34.0 (R) per tissue", "status": "reproduced with pydeseq2; formula not reported, interpreted as above"},
    }, evidence=[design_ev, paper_ev], paper={"locator": "S4.3.13.p1"}, confidence="high",
        reasoning="Raw integer counts; paper used DESeq2 per tissue; joint cell-means model keeps all tissue samples in the dispersion fit.")

    case.decide("threshold", final={
        "paper_threshold": PAPER_THRESHOLD, "threshold_source": "paper",
        "applied_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None,
                              "effect_cutoff": None, "inclusive": False},
        "multiplicity": "BH within each contrast",
    }, evidence=[paper_ev], paper={"locator": "S4.3.13.p1"}, confidence="high",
        reasoning="S4.3.13.p1: BH-adjusted p < 0.05, no fold-change cutoff; expressed-gene rule applied as the pre-filter.")
    print(cid, summary["verdict"], summary["warnings"], sexchk.get("status"), "styleXsex", bool(style_aliased_with_sex),
          "nA", len(planA), "nB", sum(c["analyzable"] for c in planB), "small", small, flush=True)
print("gates 5-8 done")
