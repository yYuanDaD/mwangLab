"""Gates 1-8 (paper_reconstruction .. threshold) for GSE273041 / PMID40069235."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40069235"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC11897176.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC11897176.paper.md"
MATRIX = "data/GSE273041/GSE273041_raw_counts.txt.gz"
META = "data/GSE273041/GSE273041_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Use the bioinformatics-workflow skill to analyze GSE273041 for PMID 40069235 (HC vs LC diet "
             "elite ultra-endurance athletes); determine how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=["case_01"])
case = run.case("case_01", accession="GSE273041")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
mat_ev = case.add_input(MATRIX, "matrix")

EFFECT = 1.0
paper_threshold = {"metric": "FDR", "adjustment": "Benjamini-Hochberg", "cutoff": 0.05,
                   "effect_metric": "log2FC", "effect_cutoff": EFFECT, "inclusive": False,
                   "source_locator": "S5.6.p3"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID40069235 / PMC11897176",
    "accessions": ["GSE273041"],
    "accession_locator": "DA.p1",
    "assay": "bulk polyA mRNA-seq (Illumina HiSeq 2500, PE100), vastus lateralis biopsies",
    "sample_inclusion": ["20 male elite ultra-endurance athletes (HC n=10, LC n=10) x 3 biopsies (BL, H0, H2) = 60 samples (S5.1.p1, S5.5.p1, TAB1)"],
    "sample_exclusion": ["not_reported"],
    "factors": [{"name": "diet", "levels": ["HC", "LC"], "type": "between-subject (cross-sectional, habitual)", "locator": "S5.1.p1"},
                {"name": "time", "levels": ["BL", "H0 (immediately post 180-min run)", "H2 (120 min post)"],
                 "type": "within-subject repeated measure", "locator": "S5.1.p3"}],
    "primary_estimand": ("Exercise response: change from baseline (BL) within each diet group at H0 and at H2 "
                         "(S2.3.p1, S2.3.p6, S5.6.p3); diet differences at each time point are a secondary, "
                         "associational estimand (S2.2.p1) and are not the requested exercise question."),
    "planned_contrasts": [
        {"name": "HC_H0_vs_BL", "locator": "S5.6.p3; S2.3.p1-p3; FIG4"},
        {"name": "HC_H2_vs_BL", "locator": "S5.6.p3; S2.3.p6; FIG4"},
        {"name": "LC_H0_vs_BL", "locator": "S5.6.p3; S2.3.p1-p3; FIG4"},
        {"name": "LC_H2_vs_BL", "locator": "S5.6.p3; S2.3.p6; FIG4"}],
    "secondary_contrasts_not_run": ["LC vs HC at BL/H0/H2 (diet, associational; S2.2.p1, TAB2)",
                                    "diet, exercise, diet x exercise ANOVA omnibus effects (S2.1.p1; no omnibus F executor)",
                                    "gene ~ metabolic-trait linear models (S2.4, S5.6.p4; exploratory, not exercise DE)"],
    "blocking_or_covariance": {"status": "required", "unit": "athlete (3 biopsies each)",
                               "paper_model": "mixed-effect model, diet x exercise, Type I ANOVA via car, Tukey post-hoc (S5.6.p3)"},
    "matrix_scale": "RPKM (easyRNASeq), filtered at 50 mapped reads; values < 10 reads replaced by the RPKM equivalent of 10 reads (S5.6.p2)",
    "paper_method": "mixed-effect ANOVA (car, R 3.0) + Tukey post-hoc, BH FDR (S5.6.p3)",
    "paper_formula": "expression ~ diet * time + (1|subject) [described, not given as formula]",
    "paper_threshold": paper_threshold,
    "reported_counts": {
        "omnibus": "diet 653, exercise 8,413, interaction 312 transcripts (p<0.01, FDR<0.05) (S2.1.p1)",
        "HC_only_vs_BL": "330 genes 'differentially expressed vs. baseline in HC only' (S2.3.p2; time point not stated, read with FIG4)",
        "LC_H0_vs_BL": "161 genes 'different at H0 vs. baseline in LC' (S2.3.p2; unclear whether total or LC-unique)",
        "shared_H0": "198 genes DE at H0 irrespective of diet (both HC and LC) (S2.3.p3)",
        "HC_H2_vs_BL": "222 genes (S2.3.p6)",
        "LC_H2_vs_BL": "193 genes, described as 'a separate group' (S2.3.p6)",
        "shared_H2": "100 DEGs shared between diets at H2 (S2.3.p6)",
        "direction": "up/down split not reported in text (only in FIG4 bars)"},
    "pathway_method": "ORA via WebGestaltR (GO) on DEG intersections; clusterProfiler GO (S5.6.p3, FIG5)",
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE273041"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": [c["name"] for c in study_map["planned_contrasts"]],
                   "paper_threshold": paper_threshold, "paper_method": study_map["paper_method"],
                   "matrix_scale": study_map["matrix_scale"], "blocking": "subject (repeated biopsies)",
                   "reported_counts": study_map["reported_counts"]},
            evidence=[paper, pr_ev], paper={"locator": "S5.6.p3"}, confidence="high",
            reasoning=("Paper's own deposit is GSE273041 (DA.p1). Exercise effects are defined as change from BL "
                       "within each diet at H0 and H2 (S2.3.p1, S2.3.p6, S5.6.p3) with FDR<0.05 and |log2FC|>1. "
                       "Per-contrast DEG totals are only partly unambiguous in text (S2.3.p2-p6)."))

# ---------------------------------------------------------------- 2 ownership
import pandas as pd
meta = pd.read_csv(META, index_col=0)
own = {"series_id": sorted(meta.series_id.unique().tolist()), "n_samples": int(len(meta)),
       "diet": meta["characteristics_ch1.2.diet"].value_counts().to_dict(),
       "timepoint": meta["characteristics_ch1.3.timepoint"].value_counts().to_dict(),
       "data_processing": meta.data_processing.iloc[0]}
case.decide("ownership",
            final={"accession": "GSE273041", "matrix_file": MATRIX, "metadata_file": META, "owned": True,
                   "checks": own},
            evidence=[meta_ev, mat_ev, paper], paper={"locator": "DA.p1"}, confidence="high",
            reasoning=("Metadata series_id GSE273041 = paper's DA accession; 60 samples = 20 athletes x 3 biopsies; "
                       "30 HiCarb / 30 LowCarb; 20 Base/IP/IP120 each; TopHat + Hg19 + RPKM matches S5.6.p2. "
                       "The only supplementary matrix is GSE273041_raw_counts.txt.gz."))

# ---------------------------------------------------------------- 3 alignment
aln = native.align_to_metadata(MATRIX, META, case.dir / "aligned", key_column="description")
assert aln["coverage"] == 1.0, aln
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    aliases={"diet": "characteristics_ch1.2.diet", "time": "characteristics_ch1.3.timepoint"},
    patterns={"subject": ("characteristics_ch1.1.participant id", r"^(\d+)_(?:Base|IP|IP120|IP20)$")},
    recode={"diet": {"HiCarb": "HC", "LowCarb": "LC"}, "time": {"Base": "BL", "IP": "H0", "IP120": "H2"}})
dm = pd.read_csv(derived["output"], index_col=0)
dm["subject"] = "s" + dm["subject"].astype(str)
# Check: the participant-id time suffix agrees with the timepoint field.
suffix = meta.loc[dm.index, "characteristics_ch1.1.participant id"].str.extract(r"_(\w+)$")[0]
assert (suffix.map({"Base": "BL", "IP": "H0", "IP120": "H2", "IP20": "H2"}) == dm["time"]).all()
# tgrp: BL shared reference (subject absorbs diet at baseline); diet-specific post-exercise levels
dm["tgrp"] = [("BL" if t == "BL" else f"{d}_{t}") for d, t in zip(dm.diet, dm.time)]
dm["dt"] = dm["diet"] + "_" + dm["time"]
dm.to_csv(derived["output"])
derived["post_edits"] = {"subject": "prefixed with 's' (formula-safe categorical label)",
                         "tgrp": "BL if time==BL else <diet>_<time> (levels BL, HC_H0, HC_H2, LC_H0, LC_H2)",
                         "dt": "<diet>_<time> (6 cells)"}
derived["levels"] = {c: dm[c].astype(str).value_counts().to_dict() for c in ["diet", "time", "tgrp", "dt"]}
derived["n_subjects"] = int(dm.subject.nunique()); derived["sha256"] = native.sha256(derived["output"])
design_meta = case.add_output(derived["output"], "design_metadata")
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
case.write_json("aligned/derived_columns.json", derived, role="derived_columns")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched": aln["unmatched_matrix_columns"],
                   "derived_columns": derived["columns"], "levels": derived["levels"]},
            evidence=[mat_ev, meta_ev, aligned_mat, design_meta], paper={"locator": "S5.1.p3"}, confidence="high",
            reasoning=("All 60 matrix columns match the GEO 'description' field exactly (e.g. CC39020001_1_Base). "
                       "Matrix column CC39020003_1_IP20 carries a typo ('IP20') but maps exactly via description to "
                       "GSM8417462, whose timepoint field is IP120 (participant id '1_IP20' carries the same typo); subject and time come from the participant-id and "
                       "timepoint fields, and the participant-id suffix agrees with timepoint for every sample."))

# ---------------------------------------------------------------- 4 matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
prof_short = {k: prof[k] for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                   "missing_values", "negative_values", "candidates")}
case.write_json("aligned/matrix_profile.json", prof_short, role="matrix_profile")
case.decide("matrix",
            final={"matrix_type": "RPKM (linear, filtered/floored by submitter)", "recommended_method": "limma on log2(RPKM+1)",
                   "profile": prof_short, "file_name_note": "file named raw_counts but contents are RPKM"},
            evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S5.6.p2"}, confidence="high",
            reasoning=("Integer fraction 0, min 0.052, max 70,799, median 1.98: linear normalized. GEO data_processing "
                       "says 'processed data are RPKM normalized read counts' and S5.6.p2 describes easyRNASeq RPKM with "
                       "low values replaced by the 10-read RPKM equivalent (per-gene floor ~0.109 visible). The file "
                       "name 'raw_counts' is misleading; no integer counts were deposited, so count methods are excluded. "
                       "25,262 genes vs 25,282 reported in S2.1.p1 (20-gene difference)."))

# ---------------------------------------------------------------- 5 design
pr = native.pairing_report(derived["output"], "subject", "time", ["BL", "H0", "H2"])
conf = native.confounding_report(derived["output"], "diet", ["subject", "time"])
case.write_json("aligned/pairing_report.json", {"pairing": pr, "confounding": conf}, role="pairing_report")
assert pr["complete_and_unique"] and pr["n_complete"] == 20
contrasts = [
    {"name": "HC_H0_vs_BL", "coefficients": {"C(tgrp)[T.HC_H0]": 1}},
    {"name": "HC_H2_vs_BL", "coefficients": {"C(tgrp)[T.HC_H2]": 1}},
    {"name": "LC_H0_vs_BL", "coefficients": {"C(tgrp)[T.LC_H0]": 1}},
    {"name": "LC_H2_vs_BL", "coefficients": {"C(tgrp)[T.LC_H2]": 1}},
]
formula = "~ C(subject) + C(tgrp)"
case.decide("design",
            final={"analysis_type": "repeated", "formula": formula, "contrasts": contrasts,
                   "factors": {"diet": ["HC", "LC"], "time": ["BL", "H0", "H2"]},
                   "parameterization": ("tgrp = BL for every baseline sample, otherwise <diet>_<time>; with subject "
                                        "fixed effects (which absorb diet) this equals ~ subject + diet:time with "
                                        "diet-specific time effects; each coefficient is a within-diet change from BL"),
                   "estimand_type": "within-subject exercise effect, per diet group"},
            candidates=[
                {"value": "pooled H0 vs BL across diets", "reason_rejected": "paper reports within-diet changes from BL (S2.3.p1); its 'irrespective of diet' 198 genes are the intersection of the two within-diet lists (S2.3.p3), reproduced as an overlap"},
                {"value": "~ subject + diet*time (full factorial)", "reason_rejected": "rank deficient: diet main effect is aliased with subject fixed effects; the within-diet time effects are the same estimable quantities as in the tgrp parameterization"},
                {"value": "LC vs HC at each time point", "reason_rejected": "diet comparison (associational, S2.2) is not the exercise estimand requested"},
                {"value": "separate per-diet paired models (30 samples each)", "reason_rejected": "paper fits one model with both diets; a pooled residual variance across all 60 samples is closer to its single mixed model"}],
            evidence=[design_meta, paper], paper={"locator": "S5.6.p3"}, confidence="high",
            reasoning=("20 athletes each biopsied at BL/H0/H2 (complete, unique); diet is between-subject. Exercise "
                       "estimand per paper = change from BL within each diet at H0 and H2 (4 planned contrasts)."))

# ---------------------------------------------------------------- 6 covariance
dc = native.design_check(derived["output"], ["subject", "tgrp"])
dc_short = {k: dc[k] for k in ("formula_equivalent", "n_samples", "n_columns", "rank", "full_rank", "residual_df", "min_cell_size")}
dc_short["levels_tgrp"] = dc["levels"]["tgrp"]
case.write_json("aligned/design_check.json", dc_short, role="design_check")
assert dc["full_rank"] and dc["residual_df"] >= 4
case.decide("covariance",
            final={"status": "required", "blocking_terms": ["subject"],
                   "covariates": [{"name": "subject", "disposition": "included (fixed-effect block for 3 biopsies per athlete)"},
                                  {"name": "diet", "disposition": "nested: subjects are nested in diet; diet main effect absorbed by subject; diet-specific time effects kept via tgrp"},
                                  {"name": "biopsy leg/site", "disposition": "excluded: not in metadata (alternate legs, S5.3.p1)"},
                                  {"name": "flow-cell/batch (CC39020 vs CC39034 prefix)", "disposition": "excluded: within-subject constant (all 3 biopsies of an athlete share a prefix), absorbed by subject block"}],
                   "pairing": {"n_subjects": pr["n_subjects"], "n_complete": pr["n_complete"]},
                   "design_check": dc_short,
                   "paper_covariance": "mixed-effect model with subject random effect (S5.6.p3); fixed subject block used here"},
            evidence=[design_meta, paper], paper={"locator": "S5.6.p3"}, confidence="high",
            reasoning=(f"Repeated biopsies per athlete; pairing complete for 20/20. Design {formula}: rank {dc['rank']}/"
                       f"{dc['n_columns']}, residual df {dc['residual_df']}. Fixed subject effects replace the paper's random "
                       "subject intercept; for within-subject contrasts in a complete balanced design these give the same "
                       "point estimates."))
# check sample-prefix batch is within subject
pref = pd.Series(dm.title.str[:7].values, index=dm.index)
assert (pd.crosstab(dm.subject, pref) > 0).sum(axis=1).max() == 1

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "limma (lmFit + contrasts.fit + eBayes, inmoose) via run_multigroup_analysis",
                   "matrix_type": "RPKM", "transform": "log2(x+1)", "formula": "~ subject + tgrp",
                   "executor_formula": formula,
                   "paper_route": {"method": "mixed-effect ANOVA (car, subject random effect) + Tukey post-hoc on RPKM, BH FDR",
                                   "status": "blocked",
                                   "reason": "no executor for car Type-I mixed ANOVA + Tukey post-hoc; R car route not available in repository tools"}},
            evidence=[aligned_mat, paper], paper={"locator": "S5.6.p3"}, confidence="medium",
            reasoning=("Deposited data are RPKM (linear), so count methods are invalid; limma on log2(RPKM+1) with a subject "
                       "block and planned contrasts is the validated route for repeated-measures linear-normalized data. "
                       "This is a declared deviation from the paper's mixed ANOVA/Tukey route."))

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": dict(paper_threshold),
                   "deviation_note": ("Paper FDR came from BH on mixed-model/Tukey p-values; here BH is applied within each "
                                      "limma moderated-t contrast. log2FC is the limma coefficient on log2(RPKM+1), "
                                      "which is compressed toward 0 for low-expressed genes relative to a log2 ratio of mean RPKM.")},
            evidence=[paper], paper={"locator": "S5.6.p3"}, confidence="high",
            reasoning="Paper: FDR < 0.05 and |log2FC| > 1 (S5.6.p3), applied unchanged on the deviation route.")
print(json.dumps({"alignment": {k: aln[k] for k in ("method", "n_aligned", "coverage")},
                  "design_check": dc_short, "pairing": pr["n_complete"], "conf": conf}, indent=1, default=str))
