# Review packet B (the analysis' decisions): GSE152347

## Mechanical flags

- **unused_subject_like_column**: {"column": "source_name_ch1", "n_values": 8, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pvalues_piled_near_1**: {"table": "genotype_main", "frac_p_gt_0.9": 0.227, "note": "p-value histogram piled up near 1: normalization or model may be wrong"}
- **other_rule_matches_paper**: {"table": "genotype_main", "paper": 56, "applied": 130, "applied_rule": "padj < 0.05", "closest_rule": "padj<0.05 & |lfc|>0.584963", "closest_n": 52, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **pvalues_piled_near_1**: {"table": "joint/time_geno_ex60_KO_vs_rest_WT", "frac_p_gt_0.9": 0.234, "note": "p-value histogram piled up near 1: normalization or model may be wrong"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| exercise_main | 1615 | 2232 | padj < 0.05 | 2232 | 880 | 400 | 2855 | 4409 | 1498 | 678 | 2635 | 0.209 | 0.125 |
| genotype_main | 56 | 130 | padj < 0.05 | 130 | 52 | 28 | 168 | 1407 | 379 | 201 | 489 | 0.227 | 0.04 |
| joint/time_geno_ex60_KO_vs_rest_WT | 0 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 650 | 437 | 332 | 98 | 0.234 | 0.018 |

## Samples per design level

### `time`
- **ex60** (13): GSM4613315 / 10_M_KO_60_RNA-seq; GSM4613321 / 16_M_WT_60_RNA-seq; GSM4613322 / 17_M_KO_60_RNA-seq; GSM4613323 / 18_M_WT_60_RNA-seq; GSM4613324 / 19_M_KO_60_RNA-seq; GSM4613328 / 22_F_WT_60_RNA-seq; GSM4613329 / 23_F_KO_60_RNA-seq; GSM4613331 / 25_F_WT_60_RNA-seq; GSM4613333 / 3_F_KO_60_RNA-seq; GSM4613334 / 4_F_WT_60_RNA-seq; GSM4613335 / 5_F_WT_60_RNA-seq; GSM4613336 / 6_F_KO_60_RNA-seq; GSM4613339 / 9_M_WT_60_RNA-seq
- **rest** (12): GSM4613316 / 11_M_WT_Bas_RNA-seq; GSM4613317 / 12_M_KO_Bas_RNA-seq; GSM4613318 / 13_M_WT_Bas_RNA-seq; GSM4613319 / 14_M_WT_Bas_RNA-seq; GSM4613320 / 15_M_KO_Bas_RNA-seq; GSM4613325 / 1_F_WT_Bas_RNA-seq; GSM4613326 / 20_F_WT_Bas_RNA-seq; GSM4613327 / 21_F_KO_Bas_RNA-seq; GSM4613330 / 24_F_KO_Bas_RNA-seq; GSM4613332 / 2_F_KO_Bas_RNA-seq; GSM4613337 / 7_M_KO_Bas_RNA-seq; GSM4613338 / 8_M_KO_Bas_RNA-seq

### `geno`
- **KO** (13): GSM4613315 / 10_M_KO_60_RNA-seq; GSM4613317 / 12_M_KO_Bas_RNA-seq; GSM4613320 / 15_M_KO_Bas_RNA-seq; GSM4613322 / 17_M_KO_60_RNA-seq; GSM4613324 / 19_M_KO_60_RNA-seq; GSM4613327 / 21_F_KO_Bas_RNA-seq; GSM4613329 / 23_F_KO_60_RNA-seq; GSM4613330 / 24_F_KO_Bas_RNA-seq; GSM4613332 / 2_F_KO_Bas_RNA-seq; GSM4613333 / 3_F_KO_60_RNA-seq; GSM4613336 / 6_F_KO_60_RNA-seq; GSM4613337 / 7_M_KO_Bas_RNA-seq; GSM4613338 / 8_M_KO_Bas_RNA-seq
- **WT** (12): GSM4613316 / 11_M_WT_Bas_RNA-seq; GSM4613318 / 13_M_WT_Bas_RNA-seq; GSM4613319 / 14_M_WT_Bas_RNA-seq; GSM4613321 / 16_M_WT_60_RNA-seq; GSM4613323 / 18_M_WT_60_RNA-seq; GSM4613325 / 1_F_WT_Bas_RNA-seq; GSM4613326 / 20_F_WT_Bas_RNA-seq; GSM4613328 / 22_F_WT_60_RNA-seq; GSM4613331 / 25_F_WT_60_RNA-seq; GSM4613334 / 4_F_WT_60_RNA-seq; GSM4613335 / 5_F_WT_60_RNA-seq; GSM4613339 / 9_M_WT_60_RNA-seq

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE152349 (SuperSeries, S4.16.p1)", "GSE152347 (RNA-seq SubSeries)"], "assay": "Total RNA-seq (TruSeq Stranded Total RNA, Ribo-Zero Gold), 75-bp PE, soleus muscle (S4.9.p1, S2.1.p1)", "sample_inclusion": "12-week-old male and female WT (Dnmt3a flox/flox) and mD3AKO mice; RNA-seq on 'rest' (sham treadmill) and 60 min after a 30-min treadmill bout only (S4.3.p1); n = 5-7 per genotype x exercise group (FIG2)", "factors": {"exercise": ["rest", "60 min post exercise"], "genotype": ["WT", "mD3AKO"], "sex": ["male", "female"]}, "primary_estimand": "Main effect of acute exercise (60 min after 30-min treadmill run vs rest) on soleus gene expression, pooled over genotype and sex (S2.2.p2, S4.17.p1)", "planned_contrasts": ["exercise main effect: 60 min post vs rest (S2.2.p2; paper: 1615 DEGs, FDR 5%)", "genotype main effect: mD3AKO vs WT (S2.2.p2, S2.6.p1; paper: 56 DEGs, 43 up / 13 down)", "genotype x exercise interaction (S2.2.p2; paper: 0 DEGs)"], "repeated_measure_unit": "none (one soleus per mouse; independent animals)", "normalization": "not_reported in this article ('processed as previously described [34]', S4.11.p1); expression threshold leaves 17389 genes (S4.9.p1), rule not stated", "paper_method": "Differential expression for a main effect of genotype, a main effect of exercise and a genotype/exercise interaction (S4.17.p1); software and model details deferred to ref [34] (S4.11.p1), not reported here. Sex handling in the RNA-seq model not reported.", "paper_ ... [367 more characters]

reasoning: Paper-first: the RNA-seq arm (S4.3.p1) is soleus from 12-week mice at rest vs 60 min after 30-min treadmill running, in both genotypes and both sexes. S4.17.p1 says DE was tested for main effects of genotype and exercise plus their interaction, FDR < 5%. S2.2.p2 reports 1615 exercise DEGs, 56 genotype DEGs, 0 interaction DEGs. No fold-change cutoff is stated. The DE software is not named (ref [34]).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE152347\\GSE152347_RNA_counts.csv.gz", "owned": true, "checks": ["metadata series_id = 'GSE152347,GSE152349'; paper data availability names SuperSeries GSE152349 (S4.16.p1)", "25 soleus samples, C57BL/6 mice, Sex Male/Female, genotype WT/KO, timepoint Bas/60 match S4.3.p1 (rest and 60 min) and FIG2 n = 5-7 per group", "data_processing: STAR to mm10 + GENCODE vM15 + featureCounts matches S4.11.p1 (GENCODE M15)", "contact Lars Roed Ingerslev, Copenhagen (author lab)"], "accession": "GSE152347", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE152347\\GSE152347_metadata.csv"}

reasoning: GSE152347 is the RNA-seq SubSeries of the paper's GSE152349; sample groups and processing match the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 25, "n_metadata": 25, "coverage": 1.0, "unmatched_matrix_columns": ["Start", "End", "Length"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\aligned\\aligned_metadata.csv", "columns": {"sex": {"source": "title", "regex": "^\\d+_([MF])_"}, "geno": {"source": "title", "regex": "^\\d+_[MF]_(KO|WT)_"}, "time": {"source": "title", "regex": "_(Bas|60)_RNA-seq$", "recode": {"Bas": "rest", "60": "ex60"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\aligned\\design_metadata.csv", "sha256": "64b302ff25356240b25436fa7c0debc8b5ab9eda990cb189e3364ce42cc9c82a", "levels": {"sex": {"M": 13, "F": 12}, "geno": {"KO": 13, "WT": 12}, "time": {"ex60": 13, "rest": 12}}}}

reasoning: Matrix columns (e.g. 10_M_KO_60) equal the metadata title minus '_RNA-seq' for 25/25 samples (inspect alignment_keys). Sex, genotype and exercise state are parsed from the title; they agree with characteristics Sex/genotype/timepoint. 'Bas' is the rested/sham group, '60' is 60 min post exercise (S4.3.p1).

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\aligned\\aligned_matrix.csv", "sha256": "015e39c11e516cd273089c45021971f90b8c77db03f192688970044c63f1b586", "n_features": 52636, "n_samples": 25, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 5436456.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values are integers (integer_fraction 1.0, max 5.4e6). GEO data_processing: featureCounts fragment counts, 'Values are observed fragments'. Annotation columns Chr/Start/End/Strand/Length are dropped. The paper's input is the same featureCounts pipeline (S4.11.p1).

### design (valid, not_started)

final: {"analysis_type": "two-group with additive covariates (factorial 2x2 plus sex)", "design_column": "time", "control": "rest", "treatment": "ex60", "formula": "~ sex + geno + time", "contrasts": [{"name": "time_ex60_vs_rest", "control": "rest", "treatment": "ex60", "role": "primary", "note": "exercise main effect, additive model pooled over genotype and sex"}, {"name": "geno_KO_vs_WT", "control": "WT", "treatment": "KO", "role": "secondary", "note": "genotype main effect; not an exercise estimand, kept for comparison with the paper's 56 DEGs"}, {"name": "interaction geno x time", "role": "secondary", "note": "from a joint cell-means model with sex"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: S4.17.p1: main effects of genotype and exercise plus interaction. The primary exercise estimand is the main effect, which the additive model ~ sex + geno + time estimates (the paper found no interaction). The interaction and per-genotype exercise contrasts come from one joint model. Sex is added because the MDS shows sex separation (S2.2.p3) and both sexes are in every genotype x time cell. The suitability report enumerates only cell-level comparisons, so the paper's planned interaction (time_geno_ex60_KO_vs_rest_WT) is the planned name given here; the exercise main effect is the additive-model primary execution exercise_main.

rejected alternatives: [{"value": "pool genotypes and test time alone (~ time)", "reason_rejected": "the paper models genotype as a main effect; leaving it and sex out inflates residual variance (sex separates samples on MDS, S2.2.p3)"}, {"value": "exercise within WT only", "reason_rejected": "the paper's estimand is the main effect over both genotypes; per-genotype contrasts are run as exploratory"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "sex", "disposition": "included"}, {"name": "geno", "disposition": "included"}], "design_check": {"formula_equivalent": "~ C(time) + C(geno)", "n_samples": 25, "n_columns": 3, "columns": ["Intercept", "time_rest", "geno_WT"], "rank": 3, "full_rank": true, "residual_df": 22, "levels": {"time": {"ex60": 13, "rest": 12}, "geno": {"KO": 13, "WT": 12}}, "cells": [{"cell": ["ex60", "KO"], "n": 6}, {"cell": ["ex60", "WT"], "n": 7}, {"cell": ["rest", "KO"], "n": 7}, {"cell": ["rest", "WT"], "n": 5}], "min_cell_size": 5, "missing_values": {}}, "confounding": [{"column": "sex", "n_levels": 2, "status": "crossed", "crosstab": {"ex60": {"F": 7, "M": 6}, "rest": {"F": 5, "M": 7}}}, {"column": "geno", "n_levels": 2, "status": "crossed", "crosstab": {"ex60": {"KO": 6, "WT": 7}, "rest": {"KO": 7, "WT": 5}}}]}

reasoning: One soleus per mouse; no repeated measures, so no blocking term. Genotype is a design factor of the paper (S4.17.p1). Sex is a biological covariate: both sexes appear in every genotype x exercise cell, so it is not confounded with exercise. No batch, cage or litter column is recorded.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald test)", "formula": "~ sex + geno + time", "paper_route": {"method": "not_reported (ref [34]); main effects genotype and exercise + interaction", "status": "not_reported", "reason": "the article does not name the DE software"}, "deviations": ["DE software chosen by the workflow (DESeq2) because the article does not name it", "the paper's expression filter (17389 genes kept) is not specified; DESeq2 independent filtering used in the primary; a CPM >= 1 in >= 3 samples filter is run as sensitivity"]}

reasoning: Raw featureCounts counts support a count model. The article does not name the package, so DESeq2 is used with the paper's model structure (main effects plus sex). The interaction is tested in a joint DESeq2 cell-means model with sex as covariate.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: S4.17.p1 and S2.2.p2: FDR < 5%, no fold-change cutoff.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "exercise_main", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 25, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\aligned\\aligned_matrix.csv", "formula": "~ sex,geno + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\exercise_main\\DEG_results_ex60_vs_rest.csv"], "counts": {"exercise_main": {"applied": {"rule": "padj < 0.05", "n_tested": 20893, "n_significant": 2232, "n_up": 1144, "n_down": 1088, "deg_sanity": "ok"}}}}

reasoning: Paper's exercise main effect, ~ sex + geno + time (S4.17.p1, S2.2.p2)

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "genotype_main", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 25, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\aligned\\aligned_matrix.csv", "formula": "~ sex,time + geno", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\genotype_main\\DEG_results_KO_vs_WT.csv"], "counts": {"genotype_main": {"applied": {"rule": "padj < 0.05", "n_tested": 20212, "n_significant": 130, "n_up": 89, "n_down": 41, "deg_sanity": "ok"}}}}

reasoning: Paper's genotype main effect (56 DEGs), same additive model

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "secondary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 25, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\aligned\\aligned_matrix.csv", "formula": "~ sex + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\joint\\DEG_results_time_ex60_vs_rest_geno-KO.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\joint\\DEG_results_time_ex60_vs_rest_geno-WT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\joint\\DEG_results_geno_KO_vs_WT_time-ex60.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\joint\\DEG_results_geno_KO_vs_WT_time-rest.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\joint\\DEG_results_time_geno_ex60_KO_vs_rest_WT.csv"], "counts": {"joint/time_ex60_vs_rest_geno-KO": {"applied": {"rule": "padj < 0.05", "n_tested": 18869, "n_significant": 1352, "n_up": 762, "n_down": 590, "deg_sanity": "ok"}}, "joint/time_ex60_vs_rest_geno-WT": {"applied": {"rule": "padj < 0.05", "n_tested": 18869, "n_significant": 859, "n_up": 512, "n_down": 347, "deg_sanity": "ok"}}, "joint/geno_KO_vs_WT_time-ex60": {"applied": {"rule": "padj < 0.05", "n_tested": 18869, "n_significant": 45, "n_up": 32, "n_down": 13, "deg_san ... [329 more characters]

reasoning: Genotype x exercise interaction (paper: 0 DEGs) and per-genotype exercise effects from one model of all 25 samples with sex

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "exercise_main_cpmfilter", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 25, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\exercise_main_cpmfilter\\input\\matrix_filtered.csv", "formula": "~ sex,geno + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\exercise_main_cpmfilter\\DEG_results_ex60_vs_rest.csv"], "counts": {"exercise_main_cpmfilter": {"applied": {"rule": "padj < 0.05", "n_tested": 13484, "n_significant": 2015, "n_up": 999, "n_down": 1016, "deg_sanity": "ok"}}}}

reasoning: Paper applies an unstated expression threshold (17389 genes kept); CPM >= 1 in >= 3 samples approximates it

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "exercise_male", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 13, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\exercise_male\\input\\matrix.csv", "formula": "~ geno + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\exercise_male\\DEG_results_ex60_vs_rest.csv"], "counts": {"exercise_male": {"applied": {"rule": "padj < 0.05", "n_tested": 17060, "n_significant": 1350, "n_up": 798, "n_down": 552, "deg_sanity": "ok"}}}}

reasoning: Per-sex exploratory analysis (both sexes present; paper pooled them)

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "exercise_female", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\exercise_female\\input\\matrix.csv", "formula": "~ geno + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33513138\\GSE152347\\results\\exercise_female\\DEG_results_ex60_vs_rest.csv"], "counts": {"exercise_female": {"applied": {"rule": "padj < 0.05", "n_tested": 20287, "n_significant": 752, "n_up": 461, "n_down": 291, "deg_sanity": "ok"}}}}

reasoning: Per-sex exploratory analysis (both sexes present; paper pooled them)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["DE package not named in the article; DESeq2 used, so counts differ (2232 vs 1615 exercise DEGs at FDR 5%)", "expression filter rule not stated; a CPM>=1 in >=3 samples sensitivity keeps 13504 genes vs the paper's 17389", "per-sex exercise analyses are exploratory: female WT rest has n = 2", "sex added as an additive covariate; the article does not say whether its RNA-seq model included sex"], "exploratory_reason": "exercise_female subset has a WT/rest cell of n = 2 (< 3); per-sex runs are exploratory", "results": {"exercise_main": {"n_deg": 2232, "up": 1144, "down": 1088, "rule": "padj < 0.05"}, "genotype_main": {"n_deg": 130, "up": 89, "down": 41, "rule": "padj < 0.05"}, "joint/time_ex60_vs_rest_geno-KO": {"n_deg": 1352, "up": 762, "down": 590, "rule": "padj < 0.05"}, "joint/time_ex60_vs_rest_geno-WT": {"n_deg": 859, "up": 512, "down": 347, "rule": "padj < 0.05"}, "joint/geno_KO_vs_WT_time-ex60": {"n_deg": 45, "up": 32, "down": 13, "rule": "padj < 0.05"}, "joint/geno_KO_vs_WT_time-rest": {"n_deg": 29, "up": 24, "down": 5, "rule": "padj < 0.05"}, "joint/time_geno_ex60_KO_vs_rest_WT": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "exercise_main_cpmfilter": {"n_deg": 2015, "up": 999, "down": 1016, "rule": "padj < 0.05"}, "exercise_male": {"n_deg": 1350, "up": 798, "down": 552, "rule": "padj < 0.05"}, "exercise_female": {"n_deg": 752, "up": 461, "down": 291, "rule": "padj < 0.05"}}, "paper_counts": {"exercise_main": 1615, " ... [666 more characters]

reasoning: The model structure follows the paper; the DE package and filter are workflow choices, so the route is a declared deviation.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Covariance | pass | not_required; sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
- | Sex | pass | Sex inference completed on 25 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DE software",
    "paper": "not named; 'processed as previously described [34]' (S4.11.p1)",
    "data": "raw featureCounts counts",
    "disposition": "executable_without_change"
  },
  {
    "item": "expression filter",
    "paper": "17389 genes survive the expression threshold (S4.9.p1), rule not stated",
    "data": "52636 GENCODE features",
    "disposition": "executable_without_change"
  },
  {
    "item": "sample sizes",
    "paper": "n = 5-7 per genotype x exercise group (FIG2)",
    "data": "WT rest 5, WT ex60 7, KO rest 7, KO ex60 6 (Female WT rest has 2)",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID33513138 / GSE152347

STATUS: finished (route `declared_deviation`; validator 15 records, 0 errors; suitability `analyzable`)

## What ran
- Case-spec route (`tools.case_runner execute case_spec.json`). Preflight was skipped as instructed. No external LLM calls were made.
- Data: GSE152347 is the RNA-seq SubSeries of the paper's SuperSeries GSE152349 (S4.16.p1). The matrix is featureCounts raw fragment counts (52,636 GENCODE vM15 genes x 25 soleus samples). Alignment: exact match on the title minus `_RNA-seq`, 25/25 samples.
- Design (S4.3.p1, S4.17.p1): 12-week-old male and female WT and mD3AKO mice, at rest (`Bas`) or 60 min after a 30-min treadmill run (`60`). Cells: WT rest 5, WT ex60 7, KO rest 7, KO ex60 6. Independent animals, so no blocking term. Sex is an additive covariate, crossed with every cell. The X/Y sex check passed.
- Executions (DESeq2/pydeseq2):
  - **primary** `exercise_main`: `~ sex + geno + time`, ex60 vs rest (the paper's exercise main effect).
  - secondary `genotype_main`: KO vs WT with `~ sex + time + geno`.
  - secondary `joint`: cell-means `~ sex + cell` giving per-genotype exercise effects, genotype within time, and the genotype x exercise interaction.
  - sensitivity `exercise_main_cpmfilter`: CPM >= 1 in >= 3 samples.
  - exploratory `exercise_male` and `exercise_female` (`~ geno + time` within each sex).
- Threshold: paper rule, FDR < 0.05 with no fold-change cutoff (S4.17.p1, S2.2.p2). `threshold_source: paper`.
- No enrichment was run. The paper's only GO analysis is on the genotype DEGs (Fig 7F), and the request does not ask for pathways.

## DEG counts vs the paper (padj < 0.05, no FC cutoff)
| Table | Ours (up/down) | Paper |
|---|---|---|
| exercise_main (primary) | 2232 (1144/1088) | 1615 |
| genotype_main | 130 (89/41) | 56 (43 up / 13 down) |
| joint interaction time x geno | 0 | 0 |
| exercise_main_cpmfilter (sensitivity) | 2015 (999/1016) | 1615 |
| joint ex60 vs rest within WT / within KO | 859 / 1352 | not reported |
| exercise_male / exercise_female (exploratory) | 1350 / 752 | not reported |

The paper's named exercise genes all rise strongly in the primary table, in the paper's direction:
- Nr4a3: log2FC 3.16, padj 1e-31
- Ppargc1a: log2FC 1.11, padj 6e-19
- Hk2: log2FC 0.53, padj 2e-14
- Atf3: log2FC 3.98 (about 16-fold; the paper says about 15-fold), padj 2e-16

There is no genotype x exercise interaction, as in the paper. The direction of the result is reproduced, but the exercise and geno ... [2079 more characters]
