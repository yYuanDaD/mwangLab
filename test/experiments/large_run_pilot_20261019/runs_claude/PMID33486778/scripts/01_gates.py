"""Gates 1-8 (paper_reconstruction .. threshold) for GSE156724 / PMID33486778."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID33486778"
CASE = "PMID33486778"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC8686756.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC8686756.paper.md"
MATRIX = "data/GSE156724/GSE156724_Raw_gene_counts_matrix.txt.gz"
META = "data/GSE156724/GSE156724_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE156724 for PMID 33486778 (Low responders to endurance training exhibit impaired "
             "hypertrophy and divergent biological process responses in rat skeletal muscle): how exercise "
             "affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=[CASE])
case = run.case(CASE, accession="GSE156724")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
mat_ev = case.add_input(MATRIX, "matrix")

LFC = 1.0  # fold change > 2 -> |log2FC| > log2(2) = 1 exactly
paper_threshold = {"metric": "FDR", "adjustment": "not_reported (limma topTable default BH assumed)",
                   "cutoff": 0.001, "effect_metric": "log2FC", "effect_cutoff": LFC,
                   "effect_cutoff_original": "fold change > 2 ('twofold or greater' in S3.5.p1)",
                   "inclusive": False, "source_locator": "S2.5.p3; FIG2; S3.5.p1"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID33486778 / PMC8686756 (Exp Physiol 2021)",
    "accessions": ["GSE156724"],
    "accession_locator": "DA.p1",
    "assay": "bulk total RNA-seq (TruSeq Stranded Total RNA, Ribo-Zero Gold), rat plantaris, NextSeq 500 PE100; Salmon + tximport gene-level counts (S2.4.p1, S2.5.p2)",
    "sample_inclusion": ["24 female rats, generation 19, 14 months old: HRT and LRT lines x {FO 14 d, non-overloaded control}, n = 6/group, separate animals (S2.2.p1, S2.3.p1)"],
    "sample_exclusion": ["not_reported (none)"],
    "factors": [
        {"name": "line", "levels": ["HRT (high responder to endurance training)", "LRT (low responder)"],
         "type": "between-animal, selectively bred genotype", "locator": "S2.2.p1"},
        {"name": "overload", "levels": ["CTRL (no surgery)", "FO (14 d synergist ablation)"],
         "type": "between-animal; FO limb from FO animals vs plantaris of separate control animals",
         "locator": "S2.2.p1, S2.3.p1"}],
    "primary_estimand": ("Transcriptome response of plantaris muscle to 14 days of functional overload "
                         "(synergist-ablation mechanical loading, a resistance-type contractile stimulus) within "
                         "each endurance-trainability line (FOinLRT, FOinHRT), and the line difference in that "
                         "response (DELTA = FOinLRT - FOinHRT, a 2x2 interaction). The endurance training itself "
                         "(8 weeks, ~12 weeks of age) was used only to phenotype/breed the lines and precedes the "
                         "sampled period by ~1 year; there is no sedentary-vs-trained contrast in the sequenced samples."),
    "planned_contrasts": [
        {"name": "FOinLRT", "definition": "LRT FO vs LRT CTRL", "locator": "S2.5.p3"},
        {"name": "FOinHRT", "definition": "HRT FO vs HRT CTRL", "locator": "S2.5.p3"},
        {"name": "DELTA", "definition": "(LRT FO - LRT CTRL) - (HRT FO - HRT CTRL)", "locator": "S2.5.p3"}],
    "exploratory_contrasts": ["LRT vs HRT within CTRL", "LRT vs HRT within FO"],
    "blocking_or_covariance": {"status": "not_required for animal (one sample per animal); RIN covariate in the paper model",
                               "locator": "S2.5.p2"},
    "matrix_scale": "Salmon estimated counts summarised by tximport (non-integer) (S2.5.p2; GEO data_processing)",
    "paper_method": "edgeR TMM + limma-voom, linear model incl. RNA integrity (RIN) covariate; genes with median CPM < 0.5 over all 24 samples excluded (S2.5.p2)",
    "paper_formula": "not_reported explicitly; implied ~ group (4 cells) + RIN with contrasts FOinLRT, FOinHRT, DELTA",
    "paper_threshold": paper_threshold,
    "reported_counts": {
        "n_genes_after_filter": "14,956 (S3.4.p1)",
        "FOinLRT": "1866 DEGs, 92.4% up (S3.5.p1, FIG2; FDR<0.001, FC>2)",
        "FOinHRT": "2460 DEGs, 79.6% up (S3.5.p1, FIG2)",
        "common": "1612 (S3.5.p1)",
        "DELTA": "no DEG count reported; analysed by GSEA (224 GO BP differ, 96 up / 101 down magnitude, 27 direction; S3.6.p1)"},
    "enrichment": {"method": "GSEA on limma moderated t, GO biological process, clusterProfiler, 10,000 permutations, size 25-500; FDR<0.05 and P<0.001 for display",
                   "locator": "S2.5.p3, S3.6.p1, FIG4"},
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
discrepancies = [
    {"item": "matrix scale", "paper": "voom on tximport counts", "data": "GSE156724_Raw_gene_counts_matrix: non-integer Salmon/tximport estimated counts despite the 'Raw' file name",
     "classification": "requires_explicit_deviation",
     "note": "the voom executor enforces integer counts and has no covariate/multigroup interface"},
    {"item": "method", "paper": "TMM + limma-voom with RIN covariate, one model on 24 samples",
     "data": "no executor for voom with covariates and multigroup contrasts (tools/limma_voom_tools.py is two-arm, no covariates, no TMM)",
     "classification": "requires_explicit_deviation",
     "note": "run limma (inmoose) on log2(CPM+1) with ~ 0 + grp + rin, all 24 samples; no voom precision weights, no TMM"},
    {"item": "library kit", "paper": "TruSeq Stranded Total RNA with Ribo-Zero Gold (S2.4.p1)",
     "data": "GEO extract protocol: TruSeq RNA Sample Prep Kit (FC-122-1001)", "classification": "executable_without_change"},
    {"item": "RIN", "paper": "RIN > 8.0 for each sample (S2.4.p1); used as covariate",
     "data": "GEO rin 8.0-9.4; FO samples have higher RIN than CTRL (partly aligned with overload)",
     "classification": "executable_without_change", "note": "RIN kept as a continuous covariate as in the paper; this absorbs part of the FO effect"},
    {"item": "endurance exercise", "paper": "lines defined by endurance training response; training at ~12 weeks",
     "data": "no trained-vs-sedentary samples; all sequenced animals are 14 months old", "classification": "executable_without_change",
     "note": "the analysable exercise-type stimulus is functional overload; line differences are genotype (associational)"},
    {"item": "enrichment library", "paper": "GO biological process via clusterProfiler", "data": "repository GSEA: MSigDB Hallmark (mouse) only; rat by mouse symbols",
     "classification": "requires_explicit_deviation"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE156724"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": ["FOinLRT", "FOinHRT", "DELTA"],
                   "exploratory_contrasts": study_map["exploratory_contrasts"],
                   "paper_threshold": paper_threshold, "paper_method": study_map["paper_method"],
                   "matrix_scale": study_map["matrix_scale"], "reported_counts": study_map["reported_counts"]},
            evidence=[paper, pr_ev], paper={"locator": "S2.5.p3"}, confidence="high",
            reasoning=("GSE156724 is the paper's deposit (DA.p1). 2x2 between-animal design line (HRT/LRT) x overload "
                       "(CTRL/FO), n=6 per cell. Planned: FO within each line and the DELTA interaction (S2.5.p3). "
                       "DEG rule FDR<0.001 and FC>2 (FIG2 legend, S3.5.p1). The request's 'exercise' maps to the paper's "
                       "loading stimulus (FO); the endurance trait is the line factor."))

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
own = {"series_id": sorted(meta.series_id.unique().tolist()), "n_samples": int(len(meta)),
       "line_x_treatment": pd.crosstab(meta["characteristics_ch1.0.line"], meta["characteristics_ch1.4.treatment"]).to_dict(),
       "sex": meta["characteristics_ch1.1.Sex"].unique().tolist(), "age": meta["characteristics_ch1.3.age"].unique().tolist(),
       "generation": meta["characteristics_ch1.5.line generation"].astype(str).unique().tolist(),
       "data_processing": meta.data_processing.iloc[0], "supplementary": "GSE156724_Raw_gene_counts_matrix.txt.gz (only file)"}
case.decide("ownership",
            final={"accession": "GSE156724", "matrix_file": MATRIX, "metadata_file": META, "owned": True, "checks": own},
            evidence=[meta_ev, mat_ev, paper], paper={"locator": "DA.p1"}, confidence="high",
            reasoning=("series GSE156724 = paper accession; 24 female plantaris samples, 14 months, generation 19, HRT/LRT x "
                       "FO/CTRL 6 each, Salmon->tximport on Rnor_6.0 r91, matching S2.2-S2.5."))

# ---------------------------------------------------------------- 3 alignment
keyed = native.derive_columns(META, case.dir / "aligned" / "metadata_keyed.csv",
                              patterns={"mkey": ("title", r"^Plantaris (\S+ \S+ rep\d)$")})
keymap = {v: v.replace(" ", "_") for v in keyed["levels"]["mkey"]}
keyed = native.derive_columns(META, case.dir / "aligned" / "metadata_keyed.csv",
                              patterns={"mkey": ("title", r"^Plantaris (\S+ \S+ rep\d)$")},
                              recode={"mkey": keymap})
aln = native.align_to_metadata(MATRIX, keyed["output"], case.dir / "aligned", key_column="mkey")
assert aln["coverage"] == 1.0 and not aln["unmatched_matrix_columns"], aln
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    aliases={"line": "characteristics_ch1.0.line", "rin": "characteristics_ch1.6.rin"},
    patterns={"load": ("characteristics_ch1.4.treatment", r"\((FO|CTRL)\)$"),
              "grp": ("mkey", r"^(\w+_\w+)_rep\d$")},
    recode={"grp": {"LRT_FO": "LFO", "LRT_CTRL": "LCT", "HRT_FO": "HFO", "HRT_CTRL": "HCT"}})
dm = pd.read_csv(derived["output"], index_col=0)
# cross-check: title-derived group agrees with characteristics line/treatment
chk = (dm.grp.str[0] == dm.line.str[0]) & (dm.grp.str[1:].map({"FO": "FO", "CT": "CTRL"}) == dm.load)
assert chk.all(), dm[~chk]
derived["levels"] = {c: dm[c].astype(str).value_counts().to_dict() for c in ["grp", "line", "load"]}
derived["title_key_recode"] = "title 'Plantaris X Y repN' -> 'X_Y_repN' (spaces to underscores), matching matrix column names"
design_meta = case.add_output(derived["output"], "design_metadata")
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
case.write_json("aligned/derived_columns.json", {"key": keyed, "design": derived}, role="derived_columns")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched": aln["unmatched_matrix_columns"],
                   "key_derivation": derived["title_key_recode"],
                   "derived_columns": derived["columns"], "levels": derived["levels"]},
            evidence=[mat_ev, meta_ev, aligned_mat, design_meta], paper={"locator": "S2.2.p1"}, confidence="high",
            reasoning=("Matrix columns (e.g. HRT_FO_rep1) equal GEO titles 'Plantaris HRT FO rep1' after removing the "
                       "'Plantaris ' prefix and replacing spaces; 24/24 exact. grp/line/load derived and cross-checked "
                       "against characteristics line and treatment (all agree)."))

# ---------------------------------------------------------------- 4 matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
prof_short = {k: prof[k] for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                   "missing_values", "negative_values", "duplicated_feature_ids", "candidates")}
am = pd.read_csv(aln["outputs"]["aligned_matrix"]["path"], index_col=0)
prof_short["library_sizes_range"] = [float(am.sum().min()), float(am.sum().max())]
cpm = am / am.sum() * 1e6
prof_short["n_genes_median_cpm_ge_0.5"] = int((cpm.median(axis=1) >= 0.5).sum())
prof_short["feature_ids"] = native.feature_id_report(aln["outputs"]["aligned_matrix"]["path"])
case.write_json("matrix_profile.json", prof_short, role="matrix_profile")
case.decide("matrix",
            final={"matrix_type": "estimated counts", "recommended_method": "limma on log2(CPM+1) (voom in paper)",
                   "profile": prof_short,
                   "provenance": "Salmon v0.9.1 quasi-mapping -> tximport gene-level counts (GEO data_processing; S2.5.p2)",
                   "rounding_documented": False},
            evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S2.5.p2"}, confidence="high",
            reasoning=(f"Non-negative, integer fraction {prof['integer_fraction']}, max {prof['max']:.0f}, library sizes "
                       "27-34 M (paper: 27.0-34.4 M reads); file name says 'Raw' but values are tximport estimated counts. "
                       "The paper's median-CPM>=0.5 filter keeps exactly 14,956 genes, as in S3.4.p1. Count-only "
                       "methods would need an undocumented rounding; limma on log-CPM needs none."))

# ---------------------------------------------------------------- 5 design
planned = ["load_FO_vs_CTRL_line-LRT", "load_FO_vs_CTRL_line-HRT", "line_LRT_vs_HRT_load-CTRL",
           "line_LRT_vs_HRT_load-FO", "line_load_LRT_FO_vs_HRT_CTRL"]
rep, suit_item, suit_summary = case.suitability(
    matrix_type="estimated counts", metadata=dm, factors=["line", "load"],
    matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Rat", subject=None,
    references={"line": "HRT", "load": "CTRL"}, planned=planned[:2] + planned[4:])
comps = [{k: c[k] for k in ("name", "kind", "test", "reference", "within", "analyzable")} for c in rep["comparisons"]]
print("suitability", json.dumps(suit_summary, default=str))
print(json.dumps(comps, indent=1, default=str))
case.write_json("suitability_comparisons.json", comps, role="suitability_comparisons")
case.decide("design",
            final={"analysis_type": "factorial (2x2 between-animal, line x load) fitted as 4-cell means model",
                   "formula": "~ 0 + grp + rin", "design_column": "grp",
                   "contrasts": [
                       {"name": "FOinLRT", "suitability_name": "load_FO_vs_CTRL_line-LRT", "vector": "LFO - LCT", "role": "paper_planned"},
                       {"name": "FOinHRT", "suitability_name": "load_FO_vs_CTRL_line-HRT", "vector": "HFO - HCT", "role": "paper_planned"},
                       {"name": "DELTA", "suitability_name": "line_load_LRT_FO_vs_HRT_CTRL", "vector": "(LFO - LCT) - (HFO - HCT)", "role": "paper_planned (interaction)"},
                       {"name": "LRTvsHRT_CTRL", "suitability_name": "line_LRT_vs_HRT_load-CTRL", "vector": "LCT - HCT", "role": "exploratory", "estimand_type": "associational (genotype)"},
                       {"name": "LRTvsHRT_FO", "suitability_name": "line_LRT_vs_HRT_load-FO", "vector": "LFO - HFO", "role": "exploratory", "estimand_type": "associational (genotype)"}],
                   "estimand_type": "interventional for FO contrasts (randomised surgery, S2.2.p1); associational for line contrasts",
                   "suitability": suit_summary},
            candidates=[
                {"value": "separate two-arm fits per line (12 samples each)", "reason_rejected": "paper fits one linear model on 24 samples with all three contrasts; pooled variance"},
                {"value": "pool HRT and LRT to FO vs CTRL", "reason_rejected": "the paper's estimand is line-specific; pooling hides the DELTA"},
                {"value": "trained vs sedentary contrast", "reason_rejected": "not present in the sequenced samples"},
                {"value": "FO limb vs contralateral limb within animal", "reason_rejected": "contralateral limbs were not sequenced; controls are separate animals"}],
            evidence=[design_meta, suit_item, paper], paper={"locator": "S2.5.p3"}, confidence="high",
            reasoning=("Four independent groups of 6 animals. Paper contrasts FOinLRT, FOinHRT and DELTA from one limma model "
                       "(S2.5.p2-p3). Line contrasts within CTRL and FO added as exploratory."))

# ---------------------------------------------------------------- 6 covariance
conf = native.confounding_report(derived["output"], "grp", ["line", "load"])
dc = native.design_check(derived["output"], ["grp"])
dc_short = {k: dc[k] for k in ("formula_equivalent", "n_samples", "n_columns", "rank", "full_rank", "residual_df", "min_cell_size")}
rin_by_grp = dm.groupby("grp")["rin"].agg(["mean", "min", "max"]).round(2).to_dict()
import numpy as np, patsy
X = patsy.dmatrix("~ 0 + C(grp) + rin", dm)
rank_rin = int(np.linalg.matrix_rank(np.asarray(X)))
rin_cov = {"rank_with_rin": rank_rin, "n_columns_with_rin": int(X.shape[1]), "residual_df_with_rin": int(len(dm) - rank_rin),
           "rin_by_grp": rin_by_grp,
           "r2_rin_on_grp": float(1 - ((dm.rin - dm.groupby('grp').rin.transform('mean')) ** 2).sum() / ((dm.rin - dm.rin.mean()) ** 2).sum())}
case.write_json("covariance_reports.json", {"confounding": conf, "design_check": dc_short, "rin": rin_cov}, role="covariance_reports")
assert dc["full_rank"] and rank_rin == X.shape[1]
case.decide("covariance",
            final={"status": "required", "blocking_terms": [],
                   "covariates": [{"name": "rin", "disposition": "included: continuous RNA integrity covariate as in the paper (S2.5.p2); not aliased (full rank 5/5, residual df 19) but correlated with load (FO mean higher)"},
                                  {"name": "animal", "disposition": "excluded: one sample per animal, groups are separate animals"},
                                  {"name": "sex/age/generation", "disposition": "excluded: single level (female, 14 months, gen 19)"},
                                  {"name": "cage (2 per cage)", "disposition": "excluded: not deposited"}],
                   "design_check": dc_short, "rin_check": rin_cov, "confounding": conf},
            evidence=[design_meta, paper], paper={"locator": "S2.5.p2"}, confidence="high",
            reasoning=(f"Independent animals, no repeated measures. Paper model includes RIN; ~ 0 + grp + rin is full rank "
                       f"({rank_rin}/{X.shape[1]}), residual df {len(dm) - rank_rin}. RIN explains R2={rin_cov['r2_rin_on_grp']:.2f} "
                       "of its variance by group, so adjusted FO effects are conservative relative to unadjusted."))

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "limma (inmoose lmFit/contrasts.fit/eBayes) on log2(CPM+1), one model on all 24 samples",
                   "matrix_type": "estimated counts", "transform": "log2(CPM+1) via preprocess_counts after the paper's median-CPM>=0.5 filter",
                   "filter": "keep genes with median CPM >= 0.5 across all 24 samples (paper rule) -> 14,956 genes",
                   "formula": "~ 0 + grp + rin",
                   "executor": "tools.multigroup_tools:run_multigroup_analysis (multilevel plan, rin continuous)",
                   "paper_route": {"method": "edgeR TMM + limma-voom with RIN covariate", "status": "blocked",
                                   "reason": ("tools/limma_voom_tools.py is two-arm only with no covariates, uses library sizes "
                                              "without TMM, and enforces integer counts; no executor fits voom weights for "
                                              "~ group + RIN with interaction contrasts")},
                   "not_used": "tools.joint_contrasts:run_joint_limma casts covariates to strings (C(cov0)), which would make RIN a 12-level factor"},
            evidence=[aligned_mat, paper], paper={"locator": "S2.5.p2"}, confidence="medium",
            reasoning=("Same model family (limma linear model + eBayes, same design and contrasts, same gene filter) without "
                       "voom precision weights and TMM. Declared deviation."))

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": dict(paper_threshold),
                   "deviation_note": "paper rule applied to limma on log2(CPM+1) instead of voom",
                   "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": None, "label": "audit: workflow default"}},
            evidence=[paper], paper={"locator": "S2.5.p3"}, confidence="high",
            reasoning="S2.5.p3: FDR<0.001; FIG2 legend: fold change > 2 and FDR < 0.001. Applied to every contrast.")
print(json.dumps({"alignment": {k: aln[k] for k in ("method", "n_aligned", "coverage")},
                  "design_check": dc_short, "rin": rin_cov, "profile": {k: prof_short[k] for k in ("integer_fraction", "max", "n_genes_median_cpm_ge_0.5")}}, indent=1, default=str))
