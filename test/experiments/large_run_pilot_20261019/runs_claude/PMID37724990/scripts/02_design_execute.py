"""Gates 5-9: design (with suitability), covariance, method, threshold, execution."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder.open(str(RUN))
case = run.case("GSE183150")
paper = case.evidence_item("paper:PMC10618653.paper.json")
A = case.dir / "aligned"
counts_csv, meta_csv = A / "library_counts.csv", A / "design_metadata.csv"
a_mat = case.evidence_item("tool_output:library_counts.csv")
a_meta = case.evidence_item("tool_output:design_metadata.csv")
dm = pd.read_csv(meta_csv, index_col=0)

PLANNED = "grp_visit_ex_eos_vs_uc_base"
# ---------------- 5. design ----------------
import shutil
# (a) Full 30-library design. tools/suitability.check_covariance tests rank of ~ grp + visit + subject,
# which is structurally rank-deficient whenever subjects are nested in a between-subject arm, so it
# reports covariance=fail even though every within-subject contrast and the interaction are estimable.
rep_full, item_full, sum_full = case.suitability(matrix_type="raw counts", metadata=dm, factors=["grp", "visit"],
                                                 matrix_csv=str(counts_csv), organism="Human", subject="subject",
                                                 references={"grp": "uc", "visit": "base"}, planned=[PLANNED])
print("FULL", json.dumps(sum_full, indent=1))
full_dir = case.dir / "suitability_full_design"
if full_dir.exists():
    shutil.rmtree(full_dir)
shutil.copytree(case.dir / "suitability", full_dir)
full_item = case.add_output(full_dir / "suitability.json", "suitability_full_design")
# (b) The model actually fitted: one within-subject change per participant (15 independent units), factor grp.
chg = dm[dm.visit == "eos"].copy()
chg.to_csv(case.dir / "aligned" / "change_unit_metadata.csv")
rep, s_item, s_summary = case.suitability(matrix_type="raw counts", metadata=chg, factors=["grp"],
                                          matrix_csv=str(counts_csv), organism="Human", subject=None,
                                          references={"grp": "uc"}, planned=["grp_ex_vs_uc"])
s_summary = dict(s_summary, unit="per-participant change (eos - base), 15 participants",
                 full_design_report={"verdict": sum_full["verdict"], "failed": sum_full["failed"],
                                     "report": str(full_dir / "suitability.md"),
                                     "why_not_used": "check_covariance requires ~ grp + visit + subject to be full rank; subject is nested in grp (between-subject arm), so that design is rank 16 of 17 by construction although the interaction and within-arm contrasts are estimable. The paired-change model removes subject by differencing."})
print("CHANGE", json.dumps(s_summary, indent=1))
sex = rep["checks"].get("sex", {})
print("SEX", json.dumps({k: v for k, v in sex.items() if k != "split_plan"}, default=str)[:1500])
comparisons = {c["name"]: c for c in rep["comparisons"]}
design_final = {
    "analysis_type": "paired_change",
    "formula": "per-subject change d = log2CPM(eos) - log2CPM(base); ~ 0 + C(grp) on d",
    "contrasts": [
        {"name": PLANNED, "definition": "(ex: eos - base) - (uc: eos - base)", "role": "planned (paper route)",
         "coefficients": {"C(grp)[ex]": 1, "C(grp)[uc]": -1}},
        {"name": "visit_eos_vs_base_grp-ex", "definition": "mean within-subject change in exercise", "role": "exploratory",
         "coefficients": {"C(grp)[ex]": 1}},
        {"name": "visit_eos_vs_base_grp-uc", "definition": "mean within-subject change in usual care", "role": "exploratory",
         "coefficients": {"C(grp)[uc]": 1}},
        {"name": "grp_ex_vs_uc_visit-base", "definition": "exercise vs usual care at baseline (between subjects)",
         "role": "exploratory (baseline balance check)", "estimand_type": "associational"},
        {"name": "grp_ex_vs_uc_visit-eos", "definition": "exercise vs usual care at 12 months (between subjects)",
         "role": "exploratory", "estimand_type": "associational"},
    ],
    "factors": {"grp": ["uc", "ex"], "visit": ["base", "eos"]},
    "reference_levels": {"grp": "uc", "visit": "base"},
    "repeated_measure": "subject",
    "suitability": s_summary,
    "sex_check": {k: v for k, v in sex.items() if k in ("status", "note", "n_mismatch", "inferred_counts")},
}
case.decide("design", final=design_final, evidence=[paper, a_meta, s_item, full_item],
            candidates=[
                {"value": "exercise eos vs base only (paired, exercise arm)", "reason_rejected": "ignores the usual-care control; kept as exploratory contrast"},
                {"value": "exercise vs usual care at 12 months, unpaired", "reason_rejected": "non-randomized arms differ at baseline (age, PGE2); ignores baseline; kept as exploratory"},
                {"value": "pooled visits, grp only", "reason_rejected": "treats repeated biopsies as independent and mixes pre/post"}],
            paper={"locator": "S3.5.p1; FIG3; SUP7"}, confidence="medium",
            reasoning=("Paper compares the 12-month change between exercise and usual care (Fig. 3A shows per-group change vs "
                       "baseline; S3.5.p1 DEGs in exercise compared with usual care). This is the group x visit interaction with "
                       "participants repeated; estimated as a paired change (follow-up minus baseline per participant) and a group "
                       "model on the differences. Per-arm changes come from the same model as exploratory contrasts. The two "
                       "cross-sectional contrasts are exploratory and associational."))

# ---------------- 6. covariance ----------------
pair = native.pairing_report(dm, "subject", "visit", ["base", "eos"])
conf = native.confounding_report(dm, "grp", ["mmr", "age", "subject"])
dc_change = native.design_check(dm[dm.visit == "eos"].set_index("subject"), ["grp"])
dc_full = native.design_check(dm, ["subject", "visit"])
cov_ev = case.write_json("covariance_checks.json", {"pairing": pair, "confounding": conf,
                                                     "design_check_change_model": dc_change,
                                                     "design_check_subject_visit": dc_full})
print("PAIR", json.dumps(pair, default=str)[:800]); print("CONF", json.dumps(conf, default=str)[:1500])
print("DC", dc_change, dc_full)
case.decide("covariance",
            final={"status": "required", "blocking_terms": ["subject"],
                   "blocking_implementation": "within-subject differencing (paired_change); subject effect removed",
                   "covariates": [{"name": "subject", "disposition": "included (differenced out in paired_change)"},
                                  {"name": "age", "disposition": "excluded: baseline-constant participant trait, cancels in the within-subject change; paper does not adjust for it"},
                                  {"name": "mmr", "disposition": "excluded: participant-level trait, cancels in the change; 4 levels for 15 participants; paper does not adjust"},
                                  {"name": "lane", "disposition": "excluded: lanes summed per library before analysis"}],
                   "pairing": {"complete": pair.get("n_complete"), "incomplete": pair.get("incomplete"),
                               "duplicated": pair.get("duplicated")},
                   "residual_df_change_model": dc_change.get("residual_df"), "rank_change_model": dc_change.get("rank")},
            evidence=[a_meta, cov_ev, s_item], paper={"locator": "FIG1; SUP7"}, confidence="high",
            reasoning=("All 15 participants have exactly one baseline and one 12-month library, so the participant is the "
                       "blocking unit. Differencing within participant removes it; the group model on 15 differences has "
                       "rank 2 and 13 residual df. Participant-level covariates cancel in the change."))

# ---------------- 7. method ----------------
case.decide("method",
            final={"method": "limma (paired-change, empirical Bayes) on log2(CPM+1)", "matrix_type": "raw counts",
                   "transform": "log2(CPM+1) after filtering genes with count >= 10 in >= 3 libraries (preprocess_counts)",
                   "formula": "~ subject + visit + grp:visit (estimated as change d_i = eos - base; ~ 0 + C(grp) on d)",
                   "contrast_vectors": {c["name"]: c.get("coefficients") for c in design_final["contrasts"] if c.get("coefficients")},
                   "cross_sectional_route": {"method": "DESeq2 two-arm (Wald, BH) on one visit's 15 independent libraries",
                                             "formula": "~ grp", "contrasts": ["grp_ex_vs_uc_visit-base", "grp_ex_vs_uc_visit-eos"]},
                   "paper_route": {"method": "not_reported (Supplementary Methods unavailable)", "status": "unknown",
                                   "reason": "the main text defers mRNA-seq statistics to Supplementary Methods, which could not be retrieved"},
                   "rejected": "DESeq2 joint model with subject blocking: subject is nested in grp, so ~ subject + cell is rank-deficient in tools.joint_contrasts; no executor fits DESeq2 ~ grp + grp:ind + grp:visit"},
            evidence=[a_mat, a_meta, paper], paper={"locator": "S2.7.p1; S2.8.p1"}, confidence="medium",
            reasoning=("Raw counts allow DESeq2 or limma on log2(CPM+1). The estimand needs subject blocking with the subject "
                       "nested in arm; the available DESeq2 executors cannot fit that nested parameterization, while the "
                       "paired-change limma executor estimates the difference in within-subject change exactly."))

# ---------------- 8. threshold ----------------
applied = {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None}
case.decide("threshold",
            final={"paper_threshold": {"metric": "not_reported", "cutoff": "not_reported", "effect_cutoff": "not_reported",
                                       "source_locator": "S2.8.p1 -> Supplementary Methods (unavailable)"},
                   "threshold_source": "workflow_default", "applied_threshold": applied,
                   "multiplicity": "BH within each contrast"},
            evidence=[paper], paper={"locator": "S2.8.p1; S3.5.p1"}, confidence="medium",
            reasoning="The main text gives no DEG cutoff; workflow default BH-adjusted p < 0.05 with no effect-size cutoff.")

# ---------------- 9. execution ----------------
R = case.dir / "results"
pre_dir = R / "preprocess"
outputs, counts_by = [], {}
try:
    native.call_tool("tools.preprocess_tools:preprocess_counts", counts_csv=str(counts_csv), output_dir=str(pre_dir))
    norm = native.find_outputs(pre_dir, "*_normalized.csv")[0]
    plan = {"analysis_type": "paired_change", "subject_column": "subject", "time_column": "visit",
            "baseline_level": "base", "followup_levels": ["eos"], "group_column": "grp", "formula": "~ 0 + C(grp)",
            "contrasts": [{"name": c["name"], "coefficients": c["coefficients"]} for c in design_final["contrasts"] if c.get("coefficients")]}
    res = native.call_tool("tools.multigroup_tools:run_multigroup_analysis", expression_csv=str(norm),
                           metadata_csv=str(meta_csv), plan=plan, output_dir=str(R / "paired_change"))
    (R / "paired_change" / "plan.json").write_text(json.dumps(plan, indent=1), encoding="utf-8")
    for r in res["results"]:
        t = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=None)
        counts_by[r["name"]] = t
        outputs.append(case.add_output(r["path"], f"deg_table:{r['name']}"))
        print(r["name"], r["residual_df"], {k: t[k] for k in ("n_significant", "n_up", "n_down") if k in t})
    outputs.append(case.add_output(norm, "normalized_matrix"))
    outputs.append(case.add_output(R / "paired_change" / "followup_eos" / "paired_change_pairs.json", "pairs"))
    case.decide("execution",
                final={"method": "limma paired-change on log2(CPM+1)", "outputs": [o["path"] for o in outputs],
                       "n_complete_pairs": res["results"][0]["n_complete_pairs"], "residual_df": res["residual_df"],
                       "counts": {k: {kk: v.get(kk) for kk in ("n_significant", "n_up", "n_down", "deg_sanity")} for k, v in counts_by.items()}},
                evidence=[a_mat, a_meta], execution_status="completed", confidence="high",
                reasoning="paired-change limma ran on 15 complete pairs; threshold applied with native.apply_threshold.")
except native.NativeToolError as e:
    case.decide("execution", final={"method": "limma paired-change on log2(CPM+1)", "execution_error": str(e)},
                evidence=[a_mat, a_meta], execution_status="failed", confidence="high", reasoning="executor failed")
    raise

# cross-sectional exploratory contrasts: DESeq2 on each visit's independent libraries
for vis in ["base", "eos"]:
    name = f"grp_ex_vs_uc_visit-{vis}"
    sub = dm[dm.visit == vis]
    sd = R / f"cross_{vis}"; sd.mkdir(parents=True, exist_ok=True)
    sub.to_csv(sd / "metadata.csv")
    pd.read_csv(counts_csv, index_col=0)[sub.index].to_csv(sd / "counts.csv")
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(sd / "counts.csv"),
                         metadata_csv=str(sd / "metadata.csv"), design_column="grp", control_group="uc",
                         treatment_group="ex", output_dir=str(sd))
        deg = native.deg_outputs(sd)[0]
        t = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
        counts_by[name] = t
        o = case.add_output(deg, f"deg_table:{name}")
        print(name, {k: t[k] for k in ("n_significant", "n_up", "n_down") if k in t})
        case.decide("execution", final={"method": "DESeq2 two-arm (~ grp)", "subset": name, "outputs": [o["path"]],
                                        "counts": {kk: t.get(kk) for kk in ("n_significant", "n_up", "n_down", "deg_sanity")}},
                    evidence=[a_mat, a_meta], execution_status="completed", confidence="high",
                    reasoning=f"exploratory cross-sectional contrast on the {vis} libraries (15 independent participants).")
    except native.NativeToolError as e:
        case.decide("execution", final={"method": "DESeq2 two-arm (~ grp)", "subset": name, "execution_error": str(e)},
                    evidence=[a_mat, a_meta], execution_status="failed", confidence="high", reasoning="executor failed")

json.dump({k: {kk: v.get(kk) for kk in ("n_significant", "n_up", "n_down", "deg_sanity")} for k, v in counts_by.items()},
          open(R / "deg_counts.json", "w"), indent=1, default=str)
print("gates 5-9 recorded")
