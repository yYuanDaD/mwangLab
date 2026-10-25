"""Gates paper_reconstruction .. threshold for GSE292369 (PMID 40960642)."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json, math
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
import numpy as np
import pandas as pd
from tools import native
native.enable_native_mode()

REL = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40960642"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12948831.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12948831.paper.md"
META = "data/GSE292369/GSE292369_metadata.csv"
TX = "data/GSE292369/GSE292369_Partek_KE_recovery_transcript_counts.txt.gz"
NORM = "data/GSE292369/GSE292369_Partek_KE_recovery_Normalization_Outliers_Removed_Deseq2.txt.gz"
REQUEST = ("Analyze GSE292369 for PMID 40960642 (Acute nutritional ketosis during early recovery from aerobic exercise "
           "does not affect skeletal muscle transcriptomic response in humans): how exercise affects gene expression "
           "as the paper intends.")
CASE = "GSE292369"
run = native.RunRecorder(REL, request=REQUEST, platform_name="claude-code",
                         decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=[CASE])
case = run.case(CASE, accession="GSE292369")
paper = case.add_input(PAPER_JSON, "paper")
paper_md = case.add_input(PAPER_MD, "paper")
meta = case.add_input(META, "metadata")
tx = case.add_input(TX, "matrix")
norm = case.add_input(NORM, "matrix")

# ------------------------------------------------------------------ paper_reconstruction
L2 = math.log2(1.5)
PT = {"metric": "FDR", "adjustment": "BH (DESeq2 FDR step-up, Partek Flow)", "cutoff": 0.05,
      "effect_metric": "log2FC", "effect_cutoff": L2, "effect_cutoff_original": "fold change > 1.5 (either direction)",
      "inclusive": False, "source_locator": "S2.9.p3",
      "note": "'significantly different ... when FDR q < 0.05 and fold change (FC) > 1.5' (S2.9.p3); ABS.p3 'q < 0.05 fold change > +/- 1.5'"}
PRIMARY = "time_POST_vs_PRE_pooled"
PLANNED = {
    PRIMARY: "Exercise effect: 180 min POST vs PRE (~60 min pre-exercise), pooled over KME and PLA trials, within visit (ABS.p3: 1561 DEGs, 909 up / 652 down)",
    "time_POST_vs_PRE_cond-PLA": "Exercise effect within the placebo trial (S3.4.p1 / FIG4C: per-condition POST vs PRE log2FC)",
    "time_POST_vs_PRE_cond-KME": "Exercise effect within the ketone-ester trial (S3.4.p1 / FIG4C)",
    "cond_time_KME_POST_vs_PLA_PRE": "Condition x time interaction: does KME change the exercise response (paper: no gene at FDR 0.05)",
    "cond_KME_vs_PLA_time-POST": "KME vs PLA at POST (paper: KME did not regulate any gene, S3.4.p1)",
}
EXPLORATORY = {"cond_KME_vs_PLA_time-PRE": "KME vs PLA at PRE (baseline check; drinks not yet given at the PRE biopsy)"}
recon = {
    "paper_id": "PMID40960642 / PMC12948831 / doi 10.1007/s00421-025-05987-9",
    "accessions": ["GSE292369"],
    "assay": "bulk poly-A mRNA-seq, vastus lateralis, NextSeq 2000 2x50 bp; STAR 2.7.8a GRCh38, Ensembl 99 quantification in Partek Flow (S2.9.p2-p3)",
    "organism": "Homo sapiens, recreationally active men",
    "sample_inclusion": ["10 recruited, 1 excluded (drink provision error) -> 9 participants (S2.1.p1)",
                         "biopsies ~60 min pre-exercise and 180 min post-exercise in each of 2 trials (S2.7.p1) -> 36 biopsies"],
    "sample_exclusion": ["participant excluded for drink error (S2.1.p1); no sample-level outlier removal reported in the paper"],
    "factors": [{"name": "time", "levels": ["PRE", "POST (180 min after 90 min cycling at 60% VO2max)"], "reference": "PRE"},
                {"name": "condition", "levels": ["PLA", "KME"], "reference": "PLA",
                 "note": "randomised double-blind crossover, 7-14 d washout (S2.3.p1)"}],
    "repeated_measure_unit": "participant (4 biopsies each); within each trial a PRE/POST pair from the same visit",
    "primary_estimand": ("Effect of an acute 90-min aerobic exercise bout (180 min recovery) on vastus lateralis gene "
                         "expression (POST vs PRE, within participant), and whether KME modifies it"),
    "planned_contrasts": list(PLANNED),
    "planned_contrast_labels": PLANNED,
    "blocking_or_covariance": {"status": "required", "note": "within-subject crossover; paper also ran lmerseq mixed models 'appropriate for within-subject RNA-seq designs' (S2.9.p3)"},
    "matrix_scale": "Partek 'filtered raw counts' (S2.9.p3); GEO deposits Partek transcript-level estimated counts and a DESeq2-normalized gene matrix with outliers removed",
    "normalization": "DESeq2 median-of-ratios (Partek Flow)",
    "paper_method": "DESeq2 in Partek Flow (S2.9.p3); lmerseq sensitivity (S2.9.p3, S3.4.p1)",
    "paper_formula": "not_reported (Partek DESeq2 model terms not printed)",
    "paper_prefilter": "'filtered raw counts' - filter rule not_reported; 16,898 genes measured (ABS.p3, S4.p1)",
    "paper_threshold": PT,
    "paper_reported_deg_counts": {PRIMARY: {"total": 1561, "up": 909, "down": 652, "locator": "ABS.p3; S3.4.p1; S4.p1"},
                                  "cond_KME_vs_PLA (condition effect)": {"total": 0, "locator": "S3.4.p1 (FDR 0.05)"},
                                  "note": "S3.4.p1 also calls the 1561 'overlapped DEGs between conditions'; ABS.p3 calls them DEGs 'post vs pre-exercise'"},
    "paper_top_genes": {"up": ["NR4A3", "SOCS3", "MAFF", "PPARGC1A"], "down": ["ARRDC2", "HIF3A", "DDIT4", "NR1D1"], "locator": "S3.4.p1"},
}
case.write_json("paper_reconstruction.json", recon, role="paper_reconstruction")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE292369"], "primary_estimand": recon["primary_estimand"],
                   "planned_contrasts": list(PLANNED), "paper_threshold": PT, "paper_method": recon["paper_method"],
                   "paper_formula": recon["paper_formula"], "assay": recon["assay"], "factors": recon["factors"],
                   "repeated_measure_unit": recon["repeated_measure_unit"],
                   "paper_reported_deg_counts": recon["paper_reported_deg_counts"]},
            evidence=[paper, paper_md], paper={"locator": "ABS.p2; ABS.p3; S2.1.p1; S2.3.p1; S2.7.p1; S2.9.p3; S3.4.p1; FIG4"},
            confidence="high",
            reasoning=("Randomised crossover: 9 men x 2 trials (KME, PLA) x 2 biopsies (PRE, POST) = 36 libraries. The request is the "
                       "exercise effect: the paper reports 1561 DEGs POST vs PRE at FDR q < 0.05 and FC > 1.5 (DESeq2, Partek). "
                       "The condition effect (KME vs PLA) is the paper's own hypothesis, reported as null; kept as secondary planned "
                       "contrasts. Model terms and the gene filter are not reported."))

# ------------------------------------------------------------------ ownership
mdf = pd.read_csv(META, index_col=0)
nm = pd.read_csv(NORM, sep="\t", index_col=0)
case.decide("ownership",
            final={"accession": "GSE292369", "matrix_file": TX, "metadata_file": META, "owned": True,
                   "checks": {"series_id": sorted(mdf["series_id"].astype(str).unique().tolist()),
                              "data_availability": "S2.9.p3 'Raw data can be found at the GEO accession GSE292369'",
                              "samples": "36 libraries = 9 subjects (P1-P4, P6-P10; P5 absent = the excluded participant) x {placebo, ketone ester} x {rest, exercised}",
                              "labels": "GEO 'rest' = PRE biopsy, 'exercised' = 180 min POST biopsy; 'placebo' = PLA, 'ketone ester' = KME",
                              "matrix_columns": "transcript-count columns are the GEO library names ('description' field)",
                              "normalized_file": f"DESeq2-normalized gene matrix, {nm.shape[0]} samples (2 outliers removed) x {nm.shape[1]-4} genes; gene sums of the transcript counts divided by this matrix give one constant per sample (size factor), so the transcript file is the input of the deposited DESeq2 analysis"},
                   "other_files": {"Normalization_Outliers_Removed_Deseq2.txt.gz": "normalized counts; used only to identify the deposited analysis' sample set and to verify the gene aggregation, not as DE input"}},
            evidence=[meta, tx, norm, paper], paper={"locator": "S2.9.p3; S2.1.p1"}, confidence="high",
            reasoning="Accession is the paper's own deposit; subject count, design and processing (Partek, STAR, GRCh38) match the paper.")

# ------------------------------------------------------------------ alignment (gene aggregation + exact alignment)
aligned_dir = case.dir / "aligned"
aligned_dir.mkdir(parents=True, exist_ok=True)
txdf = pd.read_csv(TX, sep="\t", low_memory=False)
samp = [c for c in txdf.columns if c.startswith("GC-DO")]
gene = txdf.groupby("Gene")[samp].sum()
gene.index.name = "gene"
gene_path = aligned_dir / "gene_estimated_counts_all36.csv"
gene.to_csv(gene_path)
gene_item = case.add_output(gene_path, "gene_level_estimated_counts")
# verify against the deposited normalized matrix
genes_n = [g for g in nm.columns[4:] if g in gene.index]
ratio = gene.loc[genes_n, nm.index] / nm.loc[:, genes_n].T.astype(float)
ratio = ratio.replace([np.inf, -np.inf], np.nan)
sf = ratio.median()
rel = ((ratio.quantile(0.99) - ratio.quantile(0.01)) / sf).max()
agg_check = {"n_transcripts": int(len(txdf)), "n_genes": int(gene.shape[0]),
             "genes_shared_with_normalized_file": len(genes_n),
             "implied_size_factors": sf.round(4).to_dict(),
             "max_relative_spread_1_99pct_of_ratio": float(rel),
             "verdict": "gene = sum of transcript estimated counts reproduces the deposited DESeq2 input exactly (constant ratio per sample)"}
agg_item = case.write_json("gene_aggregation_check.json", agg_check, role="gene_aggregation_check")

lib_meta = mdf.copy()
lib_meta["library_name"] = lib_meta["description"].str.replace("Library name: ", "", regex=False).str.strip()
lib_meta_path = aligned_dir / "metadata_with_library.csv"
lib_meta.to_csv(lib_meta_path)
aln = native.align_to_metadata(gene_path, lib_meta_path, aligned_dir, key_column="library_name")
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
visit_vals = sorted(set(lib_meta["library_name"].str.extract(r"GC-DO-11238-(\d+-\d)-")[0]))
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], aligned_dir / "design_metadata_all36.csv",
    aliases={"subject": "characteristics_ch1.3.subject id", "cond": "characteristics_ch1.2.treatment",
             "time": "characteristics_ch1.1.treatment"},
    patterns={"visit": ("library_name", r"GC-DO-11238-(\d+-\d)-")},
    recode={"cond": {"placebo": "PLA", "ketone ester": "KME"}, "time": {"rest": "PRE", "exercised": "POST"},
            "visit": {v: "s{}v{}".format(*v.split("-")) for v in visit_vals}})
dm_all = pd.read_csv(derived["output"], index_col=0)
# consistency: visit subject number must equal the GEO subject id; each visit one condition
vs = dm_all["visit"].str.extract(r"s(\d+)v")[0]
assert (("P" + vs) == dm_all["subject"]).all()
assert (dm_all.groupby("visit")["cond"].nunique() == 1).all()
dm_item = case.add_output(derived["output"], "design_metadata_all36")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                   "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                   "gene_aggregation": "sum of Partek transcript estimated counts per Gene symbol (60,583 genes); verified against the deposited DESeq2-normalized matrix",
                   "derived_columns": derived["columns"], "levels": derived["levels"]},
            evidence=[tx, meta, gene_item, agg_item, am, amd, amap, dm_item], paper={"locator": "S2.9.p3"}, confidence="high",
            reasoning=("Matrix columns are GEO library names; metadata 'description' = 'Library name: <name>'. Exact match on the "
                       "stripped library_name, 36/36. Gene-level counts are transcript sums (deterministic summary; equals the deposited "
                       "DESeq2 input up to a per-sample size factor). Derived subject, cond (PLA/KME), time (PRE/POST) and visit "
                       "(subject x trial from the library name; checked against subject id and one condition per visit)."))

# ------------------------------------------------------------------ matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
prof_item = case.write_json("matrix_profile.json", prof, role="matrix_profile")
fid = native.feature_id_report(aln["outputs"]["aligned_matrix"]["path"])
case.decide("matrix",
            final={"matrix_type": "estimated counts", "recommended_method": "DESeq2",
                   "rounding_documented": "gene-level sums of Partek EM transcript estimated counts rounded to the nearest integer before DESeq2",
                   "integer_fraction": prof.get("integer_fraction"), "min": prof.get("min"), "max": prof.get("max"),
                   "missing_values": prof.get("missing_values"), "negative_values": prof.get("negative_values"),
                   "n_features": prof.get("n_features"), "feature_ids": fid.get("dominant_type"),
                   "paper_input": "Partek 'filtered raw counts' into DESeq2 (S2.9.p3)"},
            candidates=[{"value": "DESeq2-normalized matrix + limma", "reason_rejected": "normalized counts are not a DE input; the count-scale file is deposited and the paper used DESeq2"},
                        {"value": "raw counts (integer)", "reason_rejected": "transcript values are fractional EM estimates (integer fraction < 1)"}],
            evidence=[am, prof_item, agg_item, meta, paper], paper={"locator": "S2.9.p3"}, confidence="high",
            reasoning=("Non-negative, no missing values, library sizes ~19-36 M, but fractional values: Partek expectation-maximisation "
                       "estimated counts. Their gene sums are exactly what the deposited DESeq2 analysis normalized (constant ratio), so "
                       "rounding to integers for DESeq2 reproduces the paper's input as closely as possible."))

# ------------------------------------------------------------------ design (suitability, sample set)
OUTLIERS = sorted(set(dm_all["library_name"]) - set(nm.index))
out_ids = dm_all.index[dm_all["library_name"].isin(OUTLIERS)].tolist()
keep = [s for s in dm_all.index if s not in out_ids]
dm34 = dm_all.loc[keep]
dm34_path = aligned_dir / "design_metadata.csv"
dm34.to_csv(dm34_path)
mat_all = pd.read_csv(aln["outputs"]["aligned_matrix"]["path"], index_col=0)
mat34_path = aligned_dir / "aligned_matrix_34.csv"
mat_all[keep].to_csv(mat34_path)
dm34_item = case.add_output(dm34_path, "design_metadata")
mat34_item = case.add_output(mat34_path, "aligned_matrix_34")
excl = dm_all.loc[out_ids, ["library_name", "subject", "cond", "time", "visit"]].to_dict(orient="index")

planned_suit = [k for k in PLANNED if k != PRIMARY] + list(EXPLORATORY)
rep, suit_item, suit_summary = case.suitability(matrix_type="estimated counts", metadata=dm34, factors=["cond", "time"],
                                                matrix_csv=str(mat34_path), organism="Human", subject="subject",
                                                covariate_candidates=[], references={"cond": "PLA", "time": "PRE"},
                                                planned=planned_suit)
names = [c["name"] for c in rep["comparisons"]]
assert set(planned_suit) == set(names), names
contrasts = [{"name": PRIMARY, "kind": "main effect (average over conditions)", "model": "~ visit + time",
              "role": "planned (primary)", "description": PLANNED[PRIMARY]}]
for c in rep["comparisons"]:
    contrasts.append({"name": c["name"], "kind": c["kind"], "cells": c["cells"], "model": "~ subject + cell",
                      "role": "planned" if c["name"] in PLANNED else "exploratory",
                      "description": PLANNED.get(c["name"]) or EXPLORATORY.get(c["name"])})
case.write_json("comparisons.json", rep["comparisons"], role="comparisons")
case.decide("design",
            final={"analysis_type": "repeated (2x2 within-subject crossover: condition x time)",
                   "formula": "primary: ~ visit + time (visit = subject x trial); per-cell contrasts: ~ subject + cell (cell = cond x time)",
                   "design_column": "time", "control": "PRE", "treatment": "POST",
                   "factors": {"cond": ["PLA", "KME"], "time": ["PRE", "POST"]},
                   "references": {"cond": "PLA", "time": "PRE"},
                   "contrasts": contrasts, "primary_contrasts": [PRIMARY],
                   "sample_set": {"n": len(keep), "excluded": excl,
                                  "rule": "the 2 libraries absent from the deposited 'Normalization_Outliers_Removed_Deseq2' matrix (authors' outlier removal)"},
                   "estimand_type": "within-subject effect of exercise (time); condition randomised",
                   "suitability": suit_summary},
            candidates=[{"value": "all 36 libraries", "reason_rejected": "the deposited DESeq2 analysis removed 2 outliers; kept as an audit sensitivity run"},
                        {"value": "~ time without blocking", "reason_rejected": "ignores the within-subject pairing"},
                        {"value": "per-condition POST vs PRE only", "reason_rejected": "ABS.p3 reports one POST-vs-PRE DEG set; per-condition contrasts are kept as secondary planned"}],
            evidence=[dm34_item, mat34_item, norm, suit_item, paper], paper={"locator": "ABS.p3; S2.3.p1; S2.9.p3; S3.4.p1"},
            confidence="medium",
            reasoning=("Exercise is the within-subject factor (PRE vs POST biopsy on the same visit); condition is randomised across "
                       "two visits. The paper's headline count is POST vs PRE pooled over conditions, so the primary contrast is the "
                       "time main effect blocked on visit. The suitability enumerator lists only cell contrasts; they are fitted "
                       "jointly with subject blocking. Two libraries (s2 PLA PRE, s7 KME PRE) are missing from the authors' "
                       "outlier-removed matrix and are excluded to match the deposited analysis; the paper text does not mention it. "
                       "Confidence medium because Partek's exact model terms are not reported."))

# ------------------------------------------------------------------ covariance
dc_primary = native.design_check(dm34_path, ["visit", "time"])
dc_joint = native.design_check(dm34_path, ["subject", "cond", "time"], interactions=[("cond", "time")])
conf = native.confounding_report(dm34_path, "time", ["subject", "cond", "visit"])
pair_visit = native.pairing_report(dm34_path, "visit", "time", ["PRE", "POST"])
pair_subj_cond = native.pairing_report(dm34_path, "subject", "cond", ["PLA", "KME"])
cov_item = case.write_json("covariance_checks.json",
                           {"design_check_primary": dc_primary, "design_check_joint": dc_joint, "confounding": conf,
                            "pairing_visit_time": pair_visit, "pairing_subject_cond": pair_subj_cond},
                           role="covariance_checks")
case.decide("covariance",
            final={"status": "required", "blocking_terms": ["visit", "subject"],
                   "blocking_by_model": {"primary ~ visit + time": "visit (subject x trial; nests subject and condition)",
                                         "joint ~ subject + cell": "subject (visit would alias the condition part of cell)"},
                   "covariates": [{"name": "visit", "disposition": "included (primary model blocking term)"},
                                  {"name": "subject", "disposition": "included (joint model blocking term); nested in visit for the primary model"},
                                  {"name": "cond", "disposition": "included in the joint model via cell; nested in visit for the primary model"},
                                  {"name": "batch / lane / RIN", "disposition": "excluded: not in GEO metadata, paper reports none"}],
                   "rank_primary": dc_primary.get("rank"), "residual_df_primary": dc_primary.get("residual_df"),
                   "rank_joint": dc_joint.get("rank"), "residual_df_joint": dc_joint.get("residual_df"),
                   "incomplete_visits": "s2v2 (PLA) and s7v1 (KME) have POST only after outlier removal; they inform no time contrast in the visit-blocked model"},
            evidence=[dm34_item, cov_item, paper], paper={"locator": "S2.3.p1; S2.7.p1; S2.9.p3"}, confidence="high",
            reasoning=(f"Each visit gives a PRE/POST pair from the same leg on the same day; time is crossed with subject and visit. "
                       f"~ visit + time: rank {dc_primary.get('rank')}, residual df {dc_primary.get('residual_df')}. "
                       f"~ subject + cond*time: rank {dc_joint.get('rank')}, residual df {dc_joint.get('residual_df')}. "
                       "No batch fields to adjust for."))

# ------------------------------------------------------------------ method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2 Wald test)", "matrix_type": "estimated counts",
                   "rounding_documented": "gene sums of transcript estimated counts rounded to nearest integer",
                   "formula": "~ visit + time (primary); ~ subject + cell (secondary cell contrasts)",
                   "executors": {"primary": "tools.deseq2_tools:run_deseq2_analysis(design_column='time', covariate_columns='visit')",
                                 "secondary": "tools.joint_contrasts:run_joint_deseq2(covariates=['subject'], round_estimated_counts=True)"},
                   "pre_filter": "all-zero genes dropped; DESeq2 independent filtering (paper's Partek filter rule not reported)",
                   "effect_size": "MLE log2FoldChange (unshrunken)",
                   "implementation_note": "pydeseq2 0.5.4 instead of Partek Flow DESeq2; same model family, Wald test, BH"},
            candidates=[{"value": "lmerseq mixed model", "reason_rejected": "paper's sensitivity route; no executor in the repository"},
                        {"value": "limma on log2(CPM+1) with duplicateCorrelation", "reason_rejected": "not the paper's method; counts support DESeq2"}],
            evidence=[prof_item, cov_item, paper], paper={"locator": "S2.9.p3"}, confidence="high",
            reasoning="Count-scale (estimated, rounding documented) input supports the paper's DESeq2 route; subject/visit blocking as fixed effects.")

# ------------------------------------------------------------------ threshold
case.decide("threshold",
            final={"paper_threshold": PT, "threshold_source": "paper", "applied_threshold": dict(PT)},
            evidence=[paper], paper={"locator": "S2.9.p3; ABS.p3"}, confidence="high",
            reasoning="Paper: FDR q < 0.05 and FC > 1.5 -> padj < 0.05 and |log2FC| > log2(1.5) = 0.5849625, applied with apply_threshold.")

plan = {"case": CASE, "primary": {"executor": "tools.deseq2_tools:run_deseq2_analysis", "counts": "aligned/aligned_matrix_34_int.csv",
                                  "metadata": str(dm34_path), "design_column": "time", "control": "PRE", "treatment": "POST",
                                  "covariate_columns": "visit"},
        "secondary": {"executor": "tools.joint_contrasts:run_joint_deseq2", "counts": str(mat34_path), "metadata": str(dm34_path),
                      "comparisons": rep["comparisons"], "covariates": ["subject"], "round_estimated_counts": True},
        "audit": "primary model on all 36 libraries (no outlier removal), audit only",
        "roles": {c["name"]: c["role"] for c in contrasts}, "threshold": PT}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
disc = [
    {"item": "sample set", "paper": "36 biopsies from 9 participants implied; no outlier removal reported", "data": "deposited DESeq2-normalized matrix has 34 samples ('Outliers_Removed'): s2 PLA PRE and s7 KME PRE absent", "disposition": "requires_explicit_deviation", "action": "follow the deposited analysis (34); 36-sample audit run"},
    {"item": "matrix scale", "paper": "'filtered raw counts'", "data": "Partek transcript-level EM estimated counts (fractional)", "disposition": "executable_without_change", "action": "sum to gene, round (documented); verified equal to deposited DESeq2 input"},
    {"item": "gene filter", "paper": "filter rule not reported; 16,898 genes", "data": "60,583 genes", "disposition": "requires_explicit_deviation", "action": "DESeq2 independent filtering only; BH denominators may differ"},
    {"item": "model terms", "paper": "Partek DESeq2 model not printed", "data": "crossover with subject/visit", "disposition": "requires_explicit_deviation", "action": "~ visit + time primary; ~ subject + cell secondary"},
    {"item": "DESeq2 implementation", "paper": "Partek Flow DESeq2", "data": "pydeseq2 0.5.4", "disposition": "executable_without_change", "action": "implementation note"},
    {"item": "1561 DEG definition", "paper": "ABS.p3 'post vs pre'; S3.4.p1 'overlapped DEGs between conditions'", "data": "n/a", "disposition": "executable_without_change", "action": "report pooled count and the overlap of per-condition DEG sets"},
    {"item": "FIG4B legend", "paper": "'log2FC < 1.5' in legend", "data": "S2.9.p3 FC > 1.5", "disposition": "executable_without_change", "action": "Methods rule used"},
]
case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
print(json.dumps(suit_summary, indent=1))
print("excluded", excl)
print("primary rank/df", dc_primary.get("rank"), dc_primary.get("residual_df"), "joint", dc_joint.get("rank"), dc_joint.get("residual_df"))
print("agg max rel spread", rel)
