"""Gates 1-8 (paper_reconstruction .. threshold) for GSE159861 / PMID35025912."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import numpy as np
import pandas as pd
import patsy
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID35025912"
CASE = "PMID35025912"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC8757917.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC8757917.paper.md"
MATRIX = "data/GSE159861/GSE159861_Raw_gene_counts_matrix.txt.gz"
META = "data/GSE159861/GSE159861_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE159861 for PMID 35025912 (Effect of short-term hindlimb immobilization on skeletal muscle "
             "atrophy and the transcriptome in a low compared with high responder to endurance training model): how "
             "exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=[CASE])
case = run.case(CASE, accession="GSE159861")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
mat_ev = case.add_input(MATRIX, "matrix")

# Results/FIG2 rule, which is the one the reported DEG counts use.
paper_threshold = {"metric": "FDR", "adjustment": "BH (limma topTable default; method not named)",
                   "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": 1.0,
                   "effect_cutoff_original": "logFC > 1 (S3.5.p1, FIG2 legend); applied to |logFC| (up and down DEGs counted)",
                   "inclusive": False, "source_locator": "S3.5.p1; FIG2",
                   "conflicting_statement": "S2.2.p2 says significance accepted at FDR < 0.001 (no effect cutoff)"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID35025912 / PMC8757917 (PLoS One 2022)",
    "accessions": ["GSE159861"], "accession_locator": "S7.p1",
    "assay": "bulk total RNA-seq (TruSeq Stranded Total RNA, Ribo-Zero Gold), NextSeq 500 PE100; Salmon 0.9.1 -> tximport gene-level (S2.2.p1-p2)",
    "sample_inclusion": ["24 female rats, generation 19, 14 months: HRT and LRT lines x {3 d hindlimb cast immobilisation (HI), control (CTRL)}, n=6/group, separate control animals (S2.p1, S2.1.p2)",
                         "plantaris and soleus from each animal (immobilised limb for HI) -> 48 libraries (S2.1.p2, S2.2.p1)"],
    "sample_exclusion": ["not_reported (none)"],
    "factors": [
        {"name": "line", "levels": ["HRT", "LRT"], "type": "between-animal selectively bred genotype (endurance trainability)", "locator": "S2.p1"},
        {"name": "trt", "levels": ["CTRL", "HI"], "type": "between-animal, randomised (S2.p1)", "locator": "S2.p1, S2.1.p2"},
        {"name": "tis", "levels": ["plantaris", "soleus"], "type": "within-animal (two muscles per rat); analysed separately", "locator": "S2.1.p2, FIG2"}],
    "primary_estimand": ("Within each muscle (plantaris, soleus): transcriptome response to 3 d hindlimb immobilisation "
                         "(disuse atrophy) in each endurance-trainability line (HIinLRT, HIinHRT), and the line difference "
                         "in that response (DELTA = HIinLRT - HIinHRT, a line x treatment interaction). The 8-week endurance "
                         "training at ~12 weeks only phenotyped the breeding lines; all sequenced rats are 14 months old and "
                         "there is no trained-vs-sedentary contrast in the sequenced samples. 'Exercise' enters as the "
                         "genetic endurance-trainability line (associational)."),
    "planned_contrasts": [
        {"name": "PLN_HIinLRT", "definition": "plantaris LRT HI vs LRT CTRL", "locator": "S2.2.p2, S3.5.p1"},
        {"name": "PLN_HIinHRT", "definition": "plantaris HRT HI vs HRT CTRL", "locator": "S2.2.p2, S3.5.p1"},
        {"name": "PLN_DELTA", "definition": "plantaris (LRT HI - LRT CTRL) - (HRT HI - HRT CTRL)", "locator": "S2.2.p2"},
        {"name": "SOL_HIinLRT", "definition": "soleus LRT HI vs LRT CTRL", "locator": "S2.2.p2, S3.5.p1"},
        {"name": "SOL_HIinHRT", "definition": "soleus HRT HI vs HRT CTRL", "locator": "S2.2.p2, S3.5.p1"},
        {"name": "SOL_DELTA", "definition": "soleus (LRT HI - LRT CTRL) - (HRT HI - HRT CTRL)", "locator": "S2.2.p2"}],
    "exploratory_contrasts": ["LRT vs HRT within CTRL and within HI, per muscle (associational, genotype)"],
    "blocking_or_covariance": {"status": "one sample per animal per muscle; RIN covariate in the paper model (S2.2.p2); animal key not reported",
                               "locator": "S2.2.p2"},
    "matrix_scale": "Salmon estimated counts summarised by tximport (S2.2.p2; GEO data_processing)",
    "paper_method": "limma-voom with RNA integrity (RIN) covariate; gene filter not stated (14,789 genes 'detected/expressed', S3.4.p1, S3.5.p1, FIG2)",
    "paper_formula": "not_reported; implied group means + RIN with pairwise contrasts HIinLRT, HIinHRT, DELTA",
    "paper_threshold": paper_threshold,
    "reported_counts": {
        "n_genes": "14,789 (S3.4.p1, S3.5.p1, FIG2)",
        "PLN_HIinLRT": "744 DEGs, 58.5% down (S3.5.p1; logFC>1, FDR<0.05)",
        "PLN_HIinHRT": "251 DEGs, 66.5% down",
        "SOL_HIinLRT": "294 DEGs, 57.1% down",
        "SOL_HIinHRT": "326 DEGs, 57.1% down",
        "common_all_four": "40 genes (S3.5.p1)",
        "DELTA": "no DEG count; GSEA GO BP: 140 processes plantaris, 118 soleus (S3.6.p1)",
        "atrogenes_logFC": "PLN HRT Trim63 1.41, Fbxo32 1.62, Hdac4 2.14; PLN LRT Trim63 2.55, Fbxo32 2.74, Hdac4 2.89; SOL Hdac4 1.85 (HRT) / 2.21 (LRT) (S3.7.p1)"},
    "enrichment": {"method": "GSEA ranked by t on GO BP, clusterProfiler, 10,000 permutations, size 25-500; FDR<0.05 & P<0.001",
                   "locator": "S2.2.p2, S3.6.p1"},
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
discrepancies = [
    {"item": "threshold", "paper": "S2.2.p2: FDR < 0.001", "data": "S3.5.p1 / FIG2 report the DEG counts at logFC > 1 and FDR < 0.05",
     "classification": "executable_without_change",
     "note": "the count-bearing rule (FDR<0.05 & |logFC|>1) is the paper_threshold; FDR<0.001 (with and without |logFC|>1) reported as audit"},
    {"item": "matrix scale", "paper": "voom on tximport counts", "data": "'Raw_gene_counts_matrix' holds non-integer Salmon/tximport estimated counts (34% integers)",
     "classification": "requires_explicit_deviation", "note": "voom executor needs integer counts, two arms, no covariates"},
    {"item": "method", "paper": "limma-voom with RIN covariate", "data": "no executor for voom + covariate + multigroup contrasts",
     "classification": "requires_explicit_deviation", "note": "limma (inmoose) on log2(CPM+1), ~ 0 + cell + rin on all 48 samples"},
    {"item": "gene filter", "paper": "14,789 genes, filter not stated",
     "data": "median CPM >= 0.5 over all 48 samples keeps exactly 14,789 genes (the rule of the authors' companion paper PMID33486778)",
     "classification": "executable_without_change", "note": "also implies a single filter (and likely one model) over both muscles"},
    {"item": "RIN", "paper": "RIN > 8.0 for each sample (S2.2.p1)", "data": "GEO rin 7.8-8.6; 9 samples below 8.0",
     "classification": "executable_without_change", "note": "RIN used as given, continuous covariate"},
    {"item": "library kit", "paper": "TruSeq Stranded Total RNA + Ribo-Zero Gold", "data": "GEO extract protocol: TruSeq RNA Sample Prep Kit (FC-122-1001)",
     "classification": "executable_without_change"},
    {"item": "animal identity", "paper": "plantaris and soleus taken from the same rats", "data": "no animal ID in GEO; rep numbers may or may not pair across muscles",
     "classification": "requires_explicit_deviation", "note": "tissue (within-animal) comparisons not run; within-muscle contrasts are between animals"},
    {"item": "exercise", "paper": "lines defined by response to 8-wk treadmill training at ~12 wk", "data": "no trained/sedentary samples; all rats 14 months",
     "classification": "executable_without_change", "note": "analysable stimulus is disuse (HI); line effect is genotype (associational)"},
    {"item": "enrichment library", "paper": "GO BP GSEA (clusterProfiler)", "data": "repository GSEA: MSigDB Hallmark (mouse) only; rat via symbol identity",
     "classification": "requires_explicit_deviation"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE159861"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": [c["name"] for c in study_map["planned_contrasts"]],
                   "exploratory_contrasts": study_map["exploratory_contrasts"],
                   "paper_threshold": paper_threshold, "paper_method": study_map["paper_method"],
                   "matrix_scale": study_map["matrix_scale"], "reported_counts": study_map["reported_counts"]},
            evidence=[paper, pr_ev], paper={"locator": "S2.2.p2"}, confidence="high",
            reasoning=("GSE159861 is the paper's deposit (S7.p1). 2x2 between-animal design line (HRT/LRT) x treatment "
                       "(CTRL/HI), n=6 per cell, in two muscles. Planned per muscle: HIinLRT, HIinHRT, DELTA (S2.2.p2). "
                       "Two thresholds stated: FDR<0.001 (S2.2.p2) and logFC>1 & FDR<0.05 (S3.5.p1, FIG2); the counts are "
                       "reported under the latter, so it is the paper_threshold. The request's 'exercise' maps to the "
                       "endurance-trainability line; no training intervention is in the sequenced samples."))

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
own = {"series_id": sorted(meta.series_id.unique().tolist()), "n_samples": int(len(meta)),
       "tissue_x_line_x_trt": meta.groupby(["characteristics_ch1.1.tissue", "characteristics_ch1.0.line",
                                            "characteristics_ch1.4.treatment"]).size().astype(int).to_dict(),
       "sex": meta["characteristics_ch1.3.Sex"].unique().tolist(), "age": meta["characteristics_ch1.2.age"].unique().tolist(),
       "generation": meta["characteristics_ch1.5.line generation"].astype(str).unique().tolist(),
       "data_processing": meta.data_processing.iloc[0], "supplementary": "GSE159861_Raw_gene_counts_matrix.txt.gz (only file)"}
own["tissue_x_line_x_trt"] = {" | ".join(k): v for k, v in own["tissue_x_line_x_trt"].items()}
case.decide("ownership",
            final={"accession": "GSE159861", "matrix_file": MATRIX, "metadata_file": META, "owned": True, "checks": own},
            evidence=[meta_ev, mat_ev, paper], paper={"locator": "S7.p1"}, confidence="high",
            reasoning=("Series GSE159861 = paper accession; 48 female samples, 14 months, generation 19, 2 muscles x "
                       "HRT/LRT x HI/CTRL, 6 each; Salmon v0.9.1 -> tximport on Rnor_6.0 r91, matching S2-S2.2."))

# ---------------------------------------------------------------- 3 alignment
kpath = case.dir / "aligned" / "metadata_keyed.csv"
keyed = native.derive_columns(
    META, kpath,
    patterns={"tis": ("title", r"^(Plantaris|Soleus) "), "line": ("title", r"^\w+ (HRT|LRT) "),
              "trt": ("title", r"^\w+ \w+ (HI|CTRL) "), "rep": ("title", r" rep(\d)$")},
    recode={"tis": {"Plantaris": "PLN", "Soleus": "SOL"}})
km = pd.read_csv(kpath, index_col=0)
km["mkey"] = km.line + "_" + km.trt + "_" + km.tis + "_rep" + km.rep.astype(str)
km.to_csv(kpath)
aln = native.align_to_metadata(MATRIX, str(kpath), case.dir / "aligned", key_column="mkey")
assert aln["coverage"] == 1.0 and not aln["unmatched_matrix_columns"], aln
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    aliases={"rin": "characteristics_ch1.6.rin"},
    patterns={"line_c": ("characteristics_ch1.0.line", r"^(HRT|LRT)$"),
              "trt_c": ("characteristics_ch1.4.treatment", r"\((HI|CTRL)\)$"),
              "tis_c": ("characteristics_ch1.1.tissue", r"^(plantaris|soleus)$")},
    recode={"tis_c": {"plantaris": "PLN", "soleus": "SOL"}})
dm = pd.read_csv(derived["output"], index_col=0)
chk = (dm.line == dm.line_c) & (dm.trt == dm.trt_c) & (dm.tis == dm.tis_c)
assert chk.all(), dm[~chk]
dm["grp"] = dm.tis + "_" + dm.line + "_" + dm.trt
dm.to_csv(derived["output"])
derived["levels"] = {c: dm[c].astype(str).value_counts().to_dict() for c in ["grp", "line", "trt", "tis"]}
derived["key"] = ("title 'Plantaris HRT HI rep1' -> tis/line/trt/rep by regex -> mkey 'HRT_HI_PLN_rep1' "
                  "(= matrix column names); grp = tis_line_trt")
design_meta = case.add_output(derived["output"], "design_metadata")
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
case.write_json("aligned/derived_columns.json", {"key": keyed, "design": derived}, role="derived_columns")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched": aln["unmatched_matrix_columns"],
                   "key_derivation": derived["key"], "derived_columns": ["tis", "line", "trt", "rep", "rin", "grp"],
                   "levels": derived["levels"],
                   "caveat": "rep numbers are only matched within tissue/line/treatment; whether repN is the same animal across muscles is not stated"},
            evidence=[mat_ev, meta_ev, aligned_mat, design_meta], paper={"locator": "S2.2.p1"}, confidence="high",
            reasoning=("Matrix columns (e.g. HRT_CTRL_SOL_rep1) are the GEO titles ('Soleus HRT CTRL rep1') re-ordered; "
                       "48/48 exact on the derived key. Title-derived tis/line/trt agree with the characteristics columns "
                       "for every sample."))

# ---------------------------------------------------------------- 4 matrix
am_path = aln["outputs"]["aligned_matrix"]["path"]
prof = native.profile_matrix(am_path)
prof_short = {k: prof[k] for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                   "missing_values", "negative_values", "duplicated_feature_ids", "candidates")}
am = pd.read_csv(am_path, index_col=0)
prof_short["library_sizes_millions"] = [round(float(am.sum().min()) / 1e6, 2), round(float(am.sum().max()) / 1e6, 2)]
cpm = am / am.sum() * 1e6
prof_short["n_genes_median_cpm_ge_0.5"] = int((cpm.median(axis=1) >= 0.5).sum())
prof_short["feature_ids"] = native.feature_id_report(am_path)
case.write_json("matrix_profile.json", prof_short, role="matrix_profile")
case.decide("matrix",
            final={"matrix_type": "estimated counts", "recommended_method": "limma on log2(CPM+1) (paper: voom)",
                   "profile": prof_short,
                   "provenance": "Salmon v0.9.1 quasi-mapping -> tximport gene-level counts (GEO data_processing; S2.2.p2)",
                   "rounding_documented": False},
            evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S2.2.p2"}, confidence="high",
            reasoning=(f"Non-negative, integer fraction {prof['integer_fraction']}, max {prof['max']:.0f}, library sizes "
                       f"{prof_short['library_sizes_millions']} M; the 'Raw' file name notwithstanding, these are tximport "
                       "estimated counts. Median CPM >= 0.5 over 48 samples keeps "
                       f"{prof_short['n_genes_median_cpm_ge_0.5']} genes = the paper's 14,789."))

# ---------------------------------------------------------------- 5 design
refs = {"tis": "PLN", "line": "HRT", "trt": "CTRL"}
planned = ["trt_HI_vs_CTRL_tis-PLN_line-LRT", "trt_HI_vs_CTRL_tis-PLN_line-HRT", "line_trt_LRT_HI_vs_HRT_CTRL_tis-PLN",
           "trt_HI_vs_CTRL_tis-SOL_line-LRT", "trt_HI_vs_CTRL_tis-SOL_line-HRT", "line_trt_LRT_HI_vs_HRT_CTRL_tis-SOL"]
rep, suit_item, suit_summary = case.suitability(
    matrix_type="estimated counts", metadata=dm, factors=["tis", "line", "trt"],
    matrix_csv=am_path, organism="Rat", subject=None, references=refs, planned=planned)
comps = [{k: c[k] for k in ("name", "kind", "test", "reference", "within", "analyzable")} for c in rep["comparisons"]]
print("suitability", json.dumps(suit_summary, default=str))
print(json.dumps([c["name"] for c in comps], indent=1))
names = {c["name"] for c in comps}
assert all(p in names for p in planned), [p for p in planned if p not in names]
exploratory = [c["name"] for c in comps if c["name"].startswith("line_LRT_vs_HRT_")]
not_run = [c["name"] for c in comps if c["name"] not in planned and c["name"] not in exploratory]
case.write_json("suitability_comparisons.json", {"comparisons": comps, "planned": planned, "exploratory": exploratory,
                                                 "not_run": not_run}, role="suitability_comparisons")
label = {planned[0]: "PLN_HIinLRT", planned[1]: "PLN_HIinHRT", planned[2]: "PLN_DELTA",
         planned[3]: "SOL_HIinLRT", planned[4]: "SOL_HIinHRT", planned[5]: "SOL_DELTA"}
case.decide("design",
            final={"analysis_type": "factorial (2x2 between-animal line x treatment, per muscle) fitted as an 8-cell means model on all 48 samples",
                   "formula": "~ 0 + cell + rin  (cell = tis x line x trt)", "design_column": "grp",
                   "contrasts": ([{"name": label[p], "suitability_name": p, "role": "paper_planned"} for p in planned]
                                 + [{"name": e, "suitability_name": e, "role": "exploratory", "estimand_type": "associational (genotype line)"} for e in exploratory]),
                   "not_run": {"comparisons": not_run,
                               "reason": "tissue comparisons are within-animal (both muscles from each rat) but no animal key is deposited, and they do not address the paper's question"},
                   "estimand_type": "interventional for HI contrasts (randomised, S2.p1); associational for line contrasts",
                   "suitability": suit_summary},
            candidates=[
                {"value": "separate two-arm fits per line and muscle (12 samples)", "reason_rejected": "paper fits a linear model with all contrasts and one gene filter over the 48 samples"},
                {"value": "pool HRT and LRT to HI vs CTRL", "reason_rejected": "the estimand is line-specific; pooling hides DELTA"},
                {"value": "pool muscles", "reason_rejected": "paper analyses plantaris and soleus separately (FIG2)"},
                {"value": "trained vs sedentary", "reason_rejected": "not present in the sequenced samples"}],
            evidence=[design_meta, suit_item, paper], paper={"locator": "S2.2.p2"}, confidence="medium",
            reasoning=("Four independent groups of 6 rats; each rat gave plantaris and soleus. Within a muscle all contrasts "
                       "are between animals. The paper reports one gene universe (14,789) for all four volcano plots, "
                       "which the 48-sample median-CPM filter reproduces exactly, so one model over both muscles is the "
                       "most faithful reading; per-muscle models are run as an audit."))

# ---------------------------------------------------------------- 6 covariance
conf = native.confounding_report(derived["output"], "grp", ["rin"])
dc = native.design_check(derived["output"], ["grp"])
dc_short = {k: dc[k] for k in ("formula_equivalent", "n_samples", "n_columns", "rank", "full_rank", "residual_df", "min_cell_size")}
X = patsy.dmatrix("~ 0 + C(grp) + rin", dm)
rank_rin = int(np.linalg.matrix_rank(np.asarray(X)))
rin_cov = {"rank_with_rin": rank_rin, "n_columns_with_rin": int(X.shape[1]), "residual_df_with_rin": int(len(dm) - rank_rin),
           "rin_by_grp": dm.groupby("grp")["rin"].agg(["mean", "min", "max"]).round(2).to_dict(),
           "r2_rin_on_grp": float(1 - ((dm.rin - dm.groupby('grp').rin.transform('mean')) ** 2).sum() / ((dm.rin - dm.rin.mean()) ** 2).sum())}
case.write_json("covariance_reports.json", {"confounding": conf, "design_check": dc_short, "rin": rin_cov}, role="covariance_reports")
assert dc["full_rank"] and rank_rin == X.shape[1]
case.decide("covariance",
            final={"status": "required", "blocking_terms": [],
                   "covariates": [{"name": "rin", "disposition": "included: continuous RNA integrity covariate as in the paper (S2.2.p2); not aliased"},
                                  {"name": "animal", "disposition": "excluded: not deposited; within-muscle contrasts are between animals; the two muscles of a rat share residual correlation that the pooled 48-sample variance ignores (per-muscle audit fits check this)"},
                                  {"name": "sex/age/generation", "disposition": "excluded: single level (female, 14 months, gen 19)"}],
                   "design_check": dc_short, "rin_check": rin_cov},
            evidence=[design_meta, paper], paper={"locator": "S2.2.p2"}, confidence="medium",
            reasoning=(f"~ 0 + grp + rin is full rank ({rank_rin}/{X.shape[1]}), residual df {len(dm) - rank_rin}; RIN "
                       f"R2 on group {rin_cov['r2_rin_on_grp']:.2f}. No repeated measures within a muscle."))

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "limma (inmoose lmFit/contrasts.fit/eBayes) on log2(CPM+1), one model on all 48 samples",
                   "matrix_type": "estimated counts", "transform": "log2(CPM+1) via preprocess_counts after median-CPM>=0.5 filter (48 samples)",
                   "filter": "median CPM >= 0.5 across all 48 samples -> 14,789 genes (= paper)",
                   "formula": "~ 0 + cell + rin",
                   "executor": "tools.joint_contrasts:run_joint_limma (covariates=['rin'], continuous)",
                   "paper_route": {"method": "limma-voom with RIN covariate", "status": "blocked",
                                   "reason": ("tools/limma_voom_tools.py + tools/limma_voom.R fit only ~ g on two arms, no "
                                              "covariates, integer counts required; no voom executor for an 8-cell + RIN model")}},
            evidence=[aligned_mat, paper], paper={"locator": "S2.2.p2"}, confidence="medium",
            reasoning="Same linear model family, design, contrasts and gene filter as the paper, without voom precision weights. Declared deviation.")

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": dict(paper_threshold),
                   "deviation_note": "paper rule applied to limma on log2(CPM+1) instead of voom",
                   "audit_thresholds": [{"metric": "padj", "cutoff": 0.001, "effect_metric": None, "label": "audit: S2.2.p2 rule"},
                                        {"metric": "padj", "cutoff": 0.001, "effect_metric": "log2FC", "effect_cutoff": 1.0, "label": "audit"},
                                        {"metric": "padj", "cutoff": 0.05, "effect_metric": None, "label": "audit: workflow default"}]},
            evidence=[paper], paper={"locator": "S3.5.p1"}, confidence="medium",
            reasoning="S3.5.p1/FIG2 count DEGs at logFC>1 & FDR<0.05; S2.2.p2's FDR<0.001 is kept as an audit.")
print(json.dumps({"alignment": {k: aln[k] for k in ("method", "n_aligned", "coverage")},
                  "design_check": dc_short, "rin": rin_cov,
                  "profile": {k: prof_short[k] for k in ("integer_fraction", "max", "n_genes_median_cpm_ge_0.5", "library_sizes_millions")}},
                 indent=1, default=str))
