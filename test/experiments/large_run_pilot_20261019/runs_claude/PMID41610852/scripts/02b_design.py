"""Gates design -> threshold for GSE312780 (suitability rerun without the time/arm source columns)."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math; os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41610852"
run = native.RunRecorder.open(RUN)
case = run.case("GSE312780")
D = case.dir
sub = D / "aligned/primary_16subjects"
paper_md = case.evidence_item("paper:PMC13237580.paper.md")
pm = pd.read_csv(sub / "design_metadata.csv", index_col=0)
sex = pd.read_csv(D / "suitability/aligned_matrix_sex_check.tsv", sep="\t", index_col=0)["predicted_sex"]
pm["sex"] = sex.reindex(pm.index)
assert pm["sex"].notna().all()
pm.to_csv(sub / "design_metadata.csv")   # adds inferred sex (XIST / chrY genes) for reporting and per-sex splits
sm_item = case.add_output(sub / "design_metadata.csv", "design_metadata_primary")
sx_item = case.add_output(sub / "aligned_matrix.csv", "aligned_matrix_primary")
excl_item = case.add_output(D / "sample_exclusion_resolution.json", "sample_exclusion_resolution")
qc_item = case.add_output(D / "qc/qc_pca_scores.csv", "qc_pca_scores")

refs = {"time": "pre", "arm": "CREST"}
planned = ["time_post_vs_pre_arm-BFRT", "time_post_vs_pre_arm-CREST", "arm_time_BFRT_post_vs_CREST_pre"]
rep, s_item, s_summary = case.suitability(matrix_type="estimated counts", metadata=pm, factors=["arm", "time"],
                                          matrix_csv=str(sub / "aligned_matrix.csv"), organism="Human",
                                          subject="subject", references=refs, planned=planned,
                                          covariate_candidates=[])
print(json.dumps(s_summary, indent=1))
assert s_summary["verdict"] != "not_analyzable", s_summary

contrasts = [
    {"name": "time_post_vs_pre_arm-BFRT", "route": "paper_planned", "estimand": "BFRT week 12 vs week 0 within subjects"},
    {"name": "time_post_vs_pre_arm-CREST", "route": "paper_planned", "estimand": "CREST week 12 vs week 0 within subjects"},
    {"name": "arm_time_BFRT_post_vs_CREST_pre", "route": "paper_planned",
     "estimand": "interaction: (BFRT post-pre) - (CREST post-pre)"},
    {"name": "arm_BFRT_vs_CREST_time-pre", "route": "exploratory", "estimand_type": "associational",
     "estimand": "baseline between-arm difference (randomization check); not estimable under subject blocking, separate ~ arm:time model"},
    {"name": "arm_BFRT_vs_CREST_time-post", "route": "exploratory", "estimand_type": "associational",
     "estimand": "post-training between-arm difference; separate ~ arm:time model without subject blocking"},
    {"name": "sensitivity_17subjects", "route": "exploratory",
     "estimand": "planned three contrasts with Resist18 retained (all 17 GEO subjects)"},
    {"name": "per_sex", "route": "exploratory",
     "estimand": "male-only (8 BFRT, 5 CREST) planned contrasts; female CREST (3) time effect; no female BFRT subjects"},
]
case.decide("design",
            final={"analysis_type": "repeated (paired pre/post within subject, subject nested in arm)",
                   "formula": "~ subject + tcell  (tcell = base | post_BFRT | post_CREST; equals paper's "
                              "~ cohort + cohort:person_within_cohort + cohort:timepoint)",
                   "contrasts": contrasts, "suitability": s_summary,
                   "sample_set": "16 subjects (8 BFRT, 8 CREST), 32 samples; Resist18 excluded (inferred paper exclusion)",
                   "sex_note": "inferred sex: 3 female subjects, all CREST; sex is between-subject and absorbed by subject blocking; "
                               "the interaction may carry sex-by-training differences (paper notes groups were not sex-matched, S3.1.p1)"},
            candidates=[{"value": "~ arm + time (no subject)", "reason_rejected": "ignores pairing of pre/post biopsies"},
                        {"value": "~ subject + arm + time + arm:time", "reason_rejected": "arm is aliased with subject; "
                         "re-parameterized as subject + per-arm post effects (same column space as the paper model)"},
                        {"value": "pool BFRT and CREST into one training effect", "reason_rejected": "paper estimates arms separately"},
                        {"value": "17 subjects including Resist18", "reason_rejected": "paper excluded one BFRT participant after PCA; "
                         "Resist18 is the only outlier; kept as exploratory sensitivity"}],
            evidence=[paper_md, sm_item, s_item, excl_item, qc_item], paper={"locator": "S8.3.15.p1; S8.3.16.p2; S2.4.p2"},
            reasoning="Paper's DESeq2 model nests person in cohort with cohort-specific timepoint effects; planned per-arm "
                      "post-vs-pre and the interaction. Between-arm cross-sectional contrasts are exploratory.",
            confidence="high")

# ---- covariance
pr = native.pairing_report(pm, "subject", "time", ["pre", "post"])
cf = native.confounding_report(pm, "time", ["subject", "arm", "sex"])
cf_arm = native.confounding_report(pm, "arm", ["subject", "sex"])
dc = native.design_check(pm, ["subject", "tcell"])
cov = {"pairing": pr, "confounding_time": cf, "confounding_arm": cf_arm, "design_check": dc}
cov_item = case.write_json("covariance_reports.json", cov)
print(json.dumps(cov, indent=1, default=str)[:3000])
assert dc.get("full_rank", True)
case.decide("covariance",
            final={"status": "required", "blocking_terms": ["subject"],
                   "covariates": [{"name": "subject", "disposition": "included (blocking, nested in arm)"},
                                  {"name": "arm", "disposition": "nested: between-subject, absorbed by subject; enters only via per-arm post effects"},
                                  {"name": "sex", "disposition": "nested: inferred, constant within subject, absorbed by subject"},
                                  {"name": "characteristics_ch1.2.batch", "disposition": "excluded: GEO 'batch' field holds Before/After, the source of time"},
                                  {"name": "characteristics_ch1.1.treatment", "disposition": "excluded: source of arm"}],
                   "rank": dc.get("rank"), "residual_df": dc.get("residual_df"),
                   "complete_pairs": pr.get("n_complete", pr.get("complete"))},
            evidence=[sm_item, cov_item, paper_md], paper={"locator": "S8.3.15.p1"},
            reasoning="Every subject has exactly one pre and one post biopsy; subject is the blocking unit (paper: "
                      "cohort:person_within_cohort). No other non-constant metadata columns.",
            confidence="high")

# ---- method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2 joint model, Wald tests on contrast vectors)",
                   "matrix_type": "estimated counts", "rounding_documented": "rounded to nearest integer",
                   "formula": "~ subject + tcell",
                   "contrast_vectors": {"time_post_vs_pre_arm-BFRT": "tcell[post_BFRT] - tcell[base]",
                                        "time_post_vs_pre_arm-CREST": "tcell[post_CREST] - tcell[base]",
                                        "arm_time_BFRT_post_vs_CREST_pre": "tcell[post_BFRT] - tcell[post_CREST]"},
                   "gene_filter": "genes with < 10 total counts across the analysed samples removed (paper S8.3.15.p1)",
                   "exploratory_between_arm": "DESeq2 ~ cell2 (arm_time cells), no subject block, 32 samples",
                   "paper_route": {"method": "DESeq2 1.48.2 on tximport lengthScaledTPM counts with apeglm LFC shrinkage",
                                   "status": "blocked",
                                   "reason": "quant.sf files not deposited (only unscaled salmon gene counts), and the "
                                             "repository joint DESeq2 executor has no apeglm shrinkage; MLE log2FC used"}},
            evidence=[paper_md, sm_item, cov_item], paper={"locator": "S8.3.15.p1"},
            reasoning="Same model family and design as the paper, run as a declared deviation on rounded unscaled salmon "
                      "counts with unshrunken LFCs.", confidence="medium")

# ---- threshold
paper_threshold = {"metric": "padj", "adjustment": "BH (DESeq2 default; method not named)", "cutoff": 0.05,
                   "effect_metric": "log2FC", "effect_cutoff": 0.585,
                   "effect_cutoff_original": "|log2FC| >= 0.585 (Methods S8.3.15.p1); |FC| > 1.5 (FIG4)",
                   "inclusive": "padj strict; effect >= in Methods", "source_locator": "S8.3.15.p1; FIG4"}
applied = {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": 0.585,
           "inclusive": False}
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": applied,
                   "deviation_note": "paper applied the cutoff to apeglm-shrunken LFC; applied here to MLE LFC. "
                                     "Effect tie rule '>' vs paper '>=' (no gene sits exactly at 0.585).",
                   "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FC",
                                       "effect_cutoff": 0.585, "reason": "Results S2.4.p2 wording 'p < 0.05'"}},
            evidence=[paper_md], paper={"locator": "S8.3.15.p1; FIG4; S2.4.p2"},
            reasoning="Methods and Figure 4 legend give adjusted p < 0.05 with |log2FC| >= 0.585 (FC 1.5); used as stated.",
            confidence="high")
print("gates recorded")
