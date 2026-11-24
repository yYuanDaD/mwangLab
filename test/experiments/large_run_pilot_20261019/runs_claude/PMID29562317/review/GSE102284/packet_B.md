# Review packet B (the analysis' decisions): GSE102284

## Mechanical flags

- **pairing_key_candidate**: {"key": "key without the age level", "across": "age", "pairs_or_sets": 17, "samples_linked": 34, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Samples per design level

### `age`
- **O** (19): GSM2732910 / Old Mouse Number 1 in Control Group; GSM2732911 / Old Mouse Number 2 in Control Group; GSM2732912 / Old Mouse Number 3 in Control Group; GSM2732913 / Old Mouse Number 4 in Control Group; GSM2732914 / Old Mouse Number 5 in Control Group; GSM2732915 / Old Mouse Number 6 in Control Group; GSM2732916 / Old Mouse Number 7 in Control Group; GSM2732917 / Old Mouse Number 8 in Control Group; GSM2732918 / Old Mouse Number 9 in Control Group; GSM2732919 / Old Mouse Number 1 in Hind Limb Unloadin; GSM2732920 / Old Mouse Number 2 in Hind Limb Unloadin; GSM2732921 / Old Mouse Number 3 in Hind Limb Unloadin; GSM2732922 / Old Mouse Number 4 in Hind Limb Unloadin; GSM2732923 / Old Mouse Number 5 in Hind Limb Unloadin; GSM2732924 / Old Mouse Number 6 in Hind Limb Unloadin; GSM2732925 / Old Mouse Number 1 in Hind Limb Unloadin; GSM2732926 / Old Mouse Number 2 in Hind Limb Unloadin; GSM2732927 / Old Mouse Number 3 in Hind Limb Unloadin; GSM2732928 / Old Mouse Number 4 in Hind Limb Unloadin
- **Y** (17): GSM2732893 / Young (Adult) Mouse Number 1 in Control ; GSM2732894 / Young (Adult) Mouse Number 2 in Control ; GSM2732895 / Young (Adult) Mouse Number 3 in Control ; GSM2732896 / Young (Adult) Mouse Number 4 in Control ; GSM2732897 / Young (Adult) Mouse Number 5 in Control ; GSM2732898 / Young (Adult) Mouse Number 6 in Control ; GSM2732899 / Young (Adult) Mouse Number 7 in Control ; GSM2732900 / Young (Adult) Mouse Number 8 in Control ; GSM2732901 / Young (Adult) Mouse Number 9 in Control ; GSM2732902 / Young (Adult) Mouse Number 1 in Hind Lim; GSM2732903 / Young (Adult) Mouse Number 2 in Hind Lim; GSM2732904 / Young (Adult) Mouse Number 3 in Hind Lim; GSM2732905 / Young (Adult) Mouse Number 4 in Hind Lim; GSM2732906 / Young (Adult) Mouse Number 1 in Hind Lim; GSM2732907 / Young (Adult) Mouse Number 2 in Hind Lim; GSM2732908 / Young (Adult) Mouse Number 3 in Hind Lim; GSM2732909 / Young (Adult) Mouse Number 4 in Hind Lim

### `cond`
- **CON** (18): GSM2732893 / Young (Adult) Mouse Number 1 in Control ; GSM2732894 / Young (Adult) Mouse Number 2 in Control ; GSM2732895 / Young (Adult) Mouse Number 3 in Control ; GSM2732896 / Young (Adult) Mouse Number 4 in Control ; GSM2732897 / Young (Adult) Mouse Number 5 in Control ; GSM2732898 / Young (Adult) Mouse Number 6 in Control ; GSM2732899 / Young (Adult) Mouse Number 7 in Control ; GSM2732900 / Young (Adult) Mouse Number 8 in Control ; GSM2732901 / Young (Adult) Mouse Number 9 in Control ; GSM2732910 / Old Mouse Number 1 in Control Group; GSM2732911 / Old Mouse Number 2 in Control Group; GSM2732912 / Old Mouse Number 3 in Control Group; GSM2732913 / Old Mouse Number 4 in Control Group; GSM2732914 / Old Mouse Number 5 in Control Group; GSM2732915 / Old Mouse Number 6 in Control Group; GSM2732916 / Old Mouse Number 7 in Control Group; GSM2732917 / Old Mouse Number 8 in Control Group; GSM2732918 / Old Mouse Number 9 in Control Group
- **RL** (8): GSM2732906 / Young (Adult) Mouse Number 1 in Hind Lim; GSM2732907 / Young (Adult) Mouse Number 2 in Hind Lim; GSM2732908 / Young (Adult) Mouse Number 3 in Hind Lim; GSM2732909 / Young (Adult) Mouse Number 4 in Hind Lim; GSM2732925 / Old Mouse Number 1 in Hind Limb Unloadin; GSM2732926 / Old Mouse Number 2 in Hind Limb Unloadin; GSM2732927 / Old Mouse Number 3 in Hind Limb Unloadin; GSM2732928 / Old Mouse Number 4 in Hind Limb Unloadin
- **UN** (10): GSM2732902 / Young (Adult) Mouse Number 1 in Hind Lim; GSM2732903 / Young (Adult) Mouse Number 2 in Hind Lim; GSM2732904 / Young (Adult) Mouse Number 3 in Hind Lim; GSM2732905 / Young (Adult) Mouse Number 4 in Hind Lim; GSM2732919 / Old Mouse Number 1 in Hind Limb Unloadin; GSM2732920 / Old Mouse Number 2 in Hind Limb Unloadin; GSM2732921 / Old Mouse Number 3 in Hind Limb Unloadin; GSM2732922 / Old Mouse Number 4 in Hind Limb Unloadin; GSM2732923 / Old Mouse Number 5 in Hind Limb Unloadin; GSM2732924 / Old Mouse Number 6 in Hind Limb Unloadin

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE102284"], "assay": "bulk RNA-seq (Illumina HiSeq 2500), soleus, male C57BL/6J", "factors": {"age": ["adult 6 mo (Y)", "old 22-24 mo (O)"], "condition": ["CON (cage control 10 d)", "UN (10 d hind limb unloading)", "RL (10 d unloading + 3 d reloading with voluntary cage ambulation)"]}, "sample_inclusion": "36 soleus samples: YC 9, YU 4, YR 4, OC 9, OU 6, OR 4 (GEO); paper does not state RNA-seq n per group", "primary_estimand": "Effect of mechanical (un)loading / physical activity on soleus transcriptome within each age: disuse (UN vs CON) and early recovery after 3 d reloading (RL vs CON); the reloading step (RL vs UN) is the re-ambulation (activity resumption) effect. This is a disuse/reloading model, not an exercise-training intervention.", "planned_contrasts": ["UN vs CON in adult (S2.4.p1, FIG4A)", "RL vs CON in adult (S2.4.p1, FIG4A)", "UN vs CON in old (S2.4.p1, FIG4A)", "RL vs CON in old (S2.4.p1, FIG4A)"], "repeated_measure_unit": "none; one soleus per independent mouse", "normalization": "Partek Genomics Suite 6.6 quantification on RefSeq transcripts (GEO data_processing)", "paper_method": "R package DESeq (original DESeq, not DESeq2) per GEO data_processing; supplementary methods (S1.8.p1) not available", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false, "source_locator": "FIG4 legend (B): RPKM > 1, p < 0.05"}, "paper_results": "No DEG counts reported. KEGG (DAVID) ... [273 more characters]

reasoning: Paper (S1.1.p1, S2.4.p1) defines six groups age x {CON, UN, RL}; FIG4A/B compare UN and RL with control in each age. GEO data_processing names DESeq. The only threshold given for the RNA-seq data is FIG4B legend 'RPKM > 1, p < 0.05' (raw p, no FC). No exercise-training arm exists; the activity manipulation is disuse and reloading (S2.1.p1 '3 days of reloading and voluntary cage ambulation'), which is what the paper intends to study, so it is analysed with that label rather than called exercise.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\input\\matrix_feature_ids.csv", "owned": true, "checks": ["paper S1.9.p1 names GSE102284", "GEO contact Paul M Coen = paper funding PI (S5.p1)", "soleus, male C57BL/6J, 6 and 22-24 mo, UN/RL/CON as in S1.1.p1", "36 GSM samples = 36 Reads columns in the deposited matrix"], "accession": "GSE102284", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE102284\\GSE102284_metadata.csv"}

reasoning: Accession cited in the paper; metadata groups match the paper's design.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 36, "n_metadata": 36, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\aligned\\aligned_metadata.csv", "columns": {"age": {"source": "characteristics_ch1.2.sample group", "regex": "^(young|old)", "recode": {"young": "Y", "old": "O"}}, "cond": {"source": "characteristics_ch1.2.sample group", "regex": "^(?:young|old) (.+)$", "recode": {"control": "CON", "unloading": "UN", "unloading + reloading": "RL"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\aligned\\design_metadata.csv", "sha256": "9375830e171496867d582c843a97d710b9471e2abc3b5a0874eab7b72096f95d", "levels": {"age": {"O": 19, "Y": 17}, "cond": {"CON": 18, "UN": 10, "RL": 8}}}}

reasoning: Matrix columns are OC_1..YU_4 (age letter, group letter C/U/R, mouse number) with '(Reads)' and '(RPKM)' duplicates; keep the Reads columns and strip the suffix. The metadata key is derived from title ('Young (Adult) Mouse Number 1 in Control Group' -> Y_C_1, normalized to yc1 = YC_1). Age and condition come from the sample group characteristic.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\aligned\\aligned_matrix.csv", "sha256": "0db019654694790f83c5897845ee8b41215d5024f4172ae8df7ffdf166a4377c", "n_features": 21154, "n_samples": 36, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 10032640.0, "median": 104.0, "integer_fraction": 0.7879, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: '(Reads)' columns are Partek E/M read assignments to RefSeq transcripts: ~52% integers, fractional values from multi-isoform reads, library sums ~1.7-1.9 M reads; separate RPKM columns are also deposited. Paper input to DESeq was read counts. Summed to gene symbol (Gene column) so the counts are per gene; summing estimated counts is valid. Rounded for DESeq2.

### design (valid, not_started)

final: {"analysis_type": "factorial (2 ages x 3 conditions), simple effects of condition within age from one model", "formula": "~ age + cond + age:cond", "contrasts": [{"name": "cond_UN_vs_CON_age-Y", "control": "CON", "treatment": "UN", "role": "primary"}, {"name": "cond_RL_vs_CON_age-Y", "control": "CON", "treatment": "RL", "role": "primary"}, {"name": "cond_UN_vs_CON_age-O", "control": "CON", "treatment": "UN", "role": "primary"}, {"name": "cond_RL_vs_CON_age-O", "control": "CON", "treatment": "RL", "role": "primary"}, {"name": "cond_RL_vs_UN_age-Y", "control": "UN", "treatment": "RL", "role": "exploratory"}, {"name": "cond_RL_vs_UN_age-O", "control": "UN", "treatment": "RL", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\suitability\\suitability.md", "n_comparisons": 11, "n_analyzable": 11}}

reasoning: Paper compares UN and RL with CON within each age (FIG4A). Reloading vs unloading (activity resumption) and age contrasts/interactions are exploratory. Pooling ages would mix the age factor the paper keeps separate. All males (S1.1.p1).

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(age) + C(cond)", "n_samples": 36, "n_columns": 4, "columns": ["Intercept", "age_Y", "cond_RL", "cond_UN"], "rank": 4, "full_rank": true, "residual_df": 32, "levels": {"age": {"O": 19, "Y": 17}, "cond": {"CON": 18, "UN": 10, "RL": 8}}, "cells": [{"cell": ["O", "CON"], "n": 9}, {"cell": ["O", "RL"], "n": 4}, {"cell": ["O", "UN"], "n": 6}, {"cell": ["Y", "CON"], "n": 9}, {"cell": ["Y", "RL"], "n": 4}, {"cell": ["Y", "UN"], "n": 4}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 36, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 36, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.sample group", "n_levels": 6, "status": "n ... [2399 more characters]

reasoning: Independent mice, one sample each; no batch, lane or date recorded in GEO. Age is a design factor, not a covariate.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "DESeq2 (pydeseq2 Wald, joint model on all 36 samples)", "formula": "~ age + cond + age:cond (cell-means)", "paper_route": {"method": "DESeq (original Bioconductor DESeq, Partek counts)", "status": "blocked", "reason": "original DESeq is deprecated/not available in this environment; per-comparison fitting details are in an unavailable supplement"}, "deviations": ["DESeq2 instead of DESeq", "gene-level (summed transcripts) instead of transcript-level", "estimated counts rounded", "paper's RPKM > 1 filter approximated by CPM >= 1 in >= 4 samples on the read counts"], "rounding_documented": true}

reasoning: Estimated counts support DESeq2, the maintained successor of the paper's DESeq.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Paper rule (raw p < 0.05, FIG4B) applied on the DESeq2 route; BH FDR < 0.05 reported as audit."}

reasoning: FIG4 legend B: 'filtered with RPKM > 1, p < 0.05'. No FC cutoff stated.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 36, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\joint\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\joint\\DEG_results_cond_UN_vs_CON_age-Y.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\joint\\DEG_results_cond_RL_vs_CON_age-Y.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\joint\\DEG_results_cond_UN_vs_CON_age-O.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\joint\\DEG_results_cond_RL_vs_CON_age-O.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\joint\\DEG_results_cond_RL_vs_UN_age-Y.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\joint\\DEG_results_cond_RL_vs_UN_age-O.csv"], "counts": {"joint/cond_UN_vs_CON_age-Y": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13141, "n_significant": 6799, "n_up": 3343, "n_down": 3456, "deg_sanity": "implausible_sig_fraction=52%(6799/13141)"}, "audit": {"rule": "padj < 0.05", "n_tested": 13141, "n_significant": 6029, "n_up": 2944, "n_down": 3085, "deg_sanity": "ok"}}, "joint/cond_RL_vs_CON_ ... [1720 more characters]

reasoning: One DESeq2 model on all six cells; planned within-age contrasts vs control, plus exploratory reloading-vs-unloading.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/cond_UN_vs_CON_age-Y", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_UN_vs_CON_age-Y\\ora_down\\DEG_results_cond_UN_vs_CON_age-Y_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_UN_vs_CON_age-Y\\ora_down\\DEG_results_cond_UN_vs_CON_age-Y_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_UN_vs_CON_age-Y\\ora_down\\DEG_results_cond_UN_vs_CON_age-Y_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_UN_vs_CON_age-Y\\ora_down\\DEG_results_cond_UN_vs_CON_age-Y_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 3456 Mouse genes (direction=down, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Mitochondrial Gene Expression (GO:01400 ... [1296 more characters]

reasoning: FIG4A: KEGG pathways down with unloading

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/cond_UN_vs_CON_age-Y", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_UN_vs_CON_age-Y\\gsea\\DEG_results_cond_UN_vs_CON_age-Y_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13146 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 16 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_SPERMATOGENESIS | NES=1.59 | NOM p=4.94e-03 | FDR q=6.62e-02 - HALLMARK_G2M_CHECKPOINT | NES=1.29 | NOM p=3.64e-02 | FDR q=4.09e-01 - HALLMARK_MITOTIC_SPINDLE | NES=1.23 | NOM p=3.98e-02 | FDR q=4.50e-01 - HALLMARK_DNA_REPAIR | NES=1.20 | NOM p=7.83e-02 | FDR q=4.32e-01 - HALLMARK_E2F_TARGETS | NES=1.19 | NOM p=8.01e-02 | FDR q=3.62e-01 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.15 | NOM p=2.37e-01 | FDR q=4.03e-01 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=1.15 | NOM p=2.41e-01 | FDR q=3.49e-01 - HALLMARK_HEME_METABOLISM | NES=1.13 | NOM p=1.92e-01 | FDR q=3.63e-01 - HALLMARK_NOTCH_SIGNALING | NES=1.10 | NOM p=2.98e-01 | FDR q=3.74e-01 - HALLMARK_KRAS_SIGNALING_DN | NES=1.01 | NOM p=4.30e-01 | FDR q=6.12e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-3.50 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=-2.60 | NOM p=0.00e+00 | FDR  ... [417 more characters]

reasoning: FIG4A: KEGG pathways down with unloading

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/cond_UN_vs_CON_age-O", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_UN_vs_CON_age-O\\ora_down\\DEG_results_cond_UN_vs_CON_age-O_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_UN_vs_CON_age-O\\ora_down\\DEG_results_cond_UN_vs_CON_age-O_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_UN_vs_CON_age-O\\ora_down\\DEG_results_cond_UN_vs_CON_age-O_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_UN_vs_CON_age-O\\ora_down\\DEG_results_cond_UN_vs_CON_age-O_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 3557 Mouse genes (direction=down, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Mitochondrial Translation (GO:0032543)  ... [1296 more characters]

reasoning: FIG4A

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/cond_UN_vs_CON_age-O", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_UN_vs_CON_age-O\\gsea\\DEG_results_cond_UN_vs_CON_age-O_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13146 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 31 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_SPERMATOGENESIS | NES=1.75 | NOM p=2.17e-03 | FDR q=9.41e-03 - HALLMARK_DNA_REPAIR | NES=1.44 | NOM p=4.60e-03 | FDR q=9.63e-02 - HALLMARK_E2F_TARGETS | NES=1.41 | NOM p=4.90e-03 | FDR q=8.95e-02 - HALLMARK_MITOTIC_SPINDLE | NES=1.21 | NOM p=6.81e-02 | FDR q=3.44e-01 - HALLMARK_G2M_CHECKPOINT | NES=1.20 | NOM p=8.25e-02 | FDR q=2.91e-01 - HALLMARK_HEME_METABOLISM | NES=1.20 | NOM p=8.24e-02 | FDR q=2.49e-01 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.06 | NOM p=3.14e-01 | FDR q=5.60e-01 - HALLMARK_P53_PATHWAY | NES=1.05 | NOM p=3.25e-01 | FDR q=4.92e-01 - HALLMARK_KRAS_SIGNALING_DN | NES=1.05 | NOM p=3.57e-01 | FDR q=4.62e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=0.92 | NOM p=6.23e-01 | FDR q=7.95e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-3.17 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=-2.38 | NOM p=0.00e+00 | FDR q=0.00e ... [417 more characters]

reasoning: FIG4A

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/cond_RL_vs_CON_age-Y", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_RL_vs_CON_age-Y\\ora_down\\DEG_results_cond_RL_vs_CON_age-Y_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_RL_vs_CON_age-Y\\ora_down\\DEG_results_cond_RL_vs_CON_age-Y_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_RL_vs_CON_age-Y\\ora_down\\DEG_results_cond_RL_vs_CON_age-Y_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_RL_vs_CON_age-Y\\ora_down\\DEG_results_cond_RL_vs_CON_age-Y_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 3704 Mouse genes (direction=down, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cellular Respiration (GO:0045333) | pad ... [1296 more characters]

reasoning: FIG4A: pathways further down after reloading

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/cond_RL_vs_CON_age-Y", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_RL_vs_CON_age-Y\\gsea\\DEG_results_cond_RL_vs_CON_age-Y_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13146 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 29 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_E2F_TARGETS | NES=2.63 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=2.52 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.22 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.05 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=1.99 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.78 | NOM p=0.00e+00 | FDR q=3.24e-03 - HALLMARK_APICAL_SURFACE | NES=1.78 | NOM p=0.00e+00 | FDR q=2.84e-03 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.76 | NOM p=0.00e+00 | FDR q=2.52e-03 - HALLMARK_NOTCH_SIGNALING | NES=1.63 | NOM p=1.98e-02 | FDR q=1.13e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-3.44 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=-2.82 ... [417 more characters]

reasoning: FIG4A: pathways further down after reloading

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/cond_RL_vs_CON_age-O", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_RL_vs_CON_age-O\\ora_down\\DEG_results_cond_RL_vs_CON_age-O_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_RL_vs_CON_age-O\\ora_down\\DEG_results_cond_RL_vs_CON_age-O_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_RL_vs_CON_age-O\\ora_down\\DEG_results_cond_RL_vs_CON_age-O_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_RL_vs_CON_age-O\\ora_down\\DEG_results_cond_RL_vs_CON_age-O_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 3387 Mouse genes (direction=down, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cellular Respiration (GO:0045333) | pad ... [1296 more characters]

reasoning: FIG4A

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/cond_RL_vs_CON_age-O", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29562317\\GSE102284\\results\\enrichment_joint_cond_RL_vs_CON_age-O\\gsea\\DEG_results_cond_RL_vs_CON_age-O_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13146 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 32 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.51 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=2.42 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=2.11 | NOM p=0.00e+00 | FDR q=5.41e-04 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.10 | NOM p=0.00e+00 | FDR q=8.12e-04 - HALLMARK_APICAL_JUNCTION | NES=2.02 | NOM p=0.00e+00 | FDR q=6.49e-04 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.85 | NOM p=0.00e+00 | FDR q=1.89e-03 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.85 | NOM p=0.00e+00 | FDR q=1.62e-03 - HALLMARK_COMPLEMENT | NES=1.83 | NOM p=0.00e+00 | FDR q=1.83e-03 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.83 | NOM p=0.00e+00 | FDR q=1.80e-03 - HALLMARK_COAGULATION | NES=1.76 | NOM p=0.00e+00 | FDR q=3.08e-03 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-3.34 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES ... [417 more characters]

reasoning: FIG4A

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["No exercise-training arm: the activity manipulation is hind limb unloading (disuse) and 3 d reloading with voluntary cage ambulation; results describe disuse/reloading, not exercise.", "Paper reports no DEG counts; comparison is limited to pathway direction and Ppargc1a/Esrra/Esrrg.", "Unequal small groups (n = 4 for YU, YR, OR)."], "results": {"joint/cond_UN_vs_CON_age-Y": {"n_deg": 6799, "up": 3343, "down": 3456, "rule": "pvalue < 0.05", "audit_n": 6029}, "joint/cond_RL_vs_CON_age-Y": {"n_deg": 7763, "up": 4059, "down": 3704, "rule": "pvalue < 0.05", "audit_n": 7109}, "joint/cond_UN_vs_CON_age-O": {"n_deg": 7098, "up": 3541, "down": 3557, "rule": "pvalue < 0.05", "audit_n": 6375}, "joint/cond_RL_vs_CON_age-O": {"n_deg": 6822, "up": 3435, "down": 3387, "rule": "pvalue < 0.05", "audit_n": 6043}, "joint/cond_RL_vs_UN_age-Y": {"n_deg": 7559, "up": 3933, "down": 3626, "rule": "pvalue < 0.05", "audit_n": 6902}, "joint/cond_RL_vs_UN_age-O": {"n_deg": 7842, "up": 4027, "down": 3815, "rule": "pvalue < 0.05", "audit_n": 7279}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"joint/cond_UN_vs_CON_age-Y": {"Ppargc1a": {"baseMean": 3524.7962, "log2FoldChange": -1.7248, "padj": 0.000134, "pvalue": 2.71e-05}, "Esrra": {"baseMean": 2756.6849, "log2FoldChange": -0.7047, "padj": 1.6e-08, "pvalue": 1.33e-09}, "Esrrg": {"baseMean": 3955.3368, "log2FoldChange": -1.0114, "padj": 1.45e-10, "pvalue": 8.18e-12}}, "joint/cond_UN_vs_CON_age-O": ... [959 more characters]

reasoning: Paper's own route (DESeq) is blocked; DESeq2 runs as a declared deviation with the paper's threshold.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 36 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "DESeq (GEO data_processing)",
    "data": "DESeq2 run instead",
    "disposition": "declared_deviation"
  },
  {
    "item": "feature level",
    "paper": "RefSeq transcripts (Partek)",
    "data": "summed to gene symbol",
    "disposition": "declared_deviation"
  },
  {
    "item": "expression filter",
    "paper": "RPKM > 1 (FIG4B)",
    "data": "CPM >= 1 in >= 4 samples on reads",
    "disposition": "declared_deviation"
  },
  {
    "item": "exercise framing",
    "paper": "disuse (unloading) and reloading recovery; no exercise training",
    "data": "same",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID29562317 / GSE102284

**Status: finished** (case-spec route, validator 18 records, 0 errors). Route: `declared_deviation`.

## Estimand and the exercise question
The study has no exercise-training arm. The activity manipulation is 10 days of hind limb unloading (disuse, UN), then 10 days of unloading plus 3 days of reloading with voluntary cage ambulation (RL), compared with cage controls (CON), in adult (6 months, Y) and old (22–24 months, O) male mice; tissue is soleus (S1.1.p1, S2.1.p1). The paper intends a disuse/reloading analysis, so it was run with that label rather than refused. The caveat is in `study.caveats`: results describe disuse and early reloading, not exercise. RL vs UN, the effect of resuming loading and ambulation, was run as exploratory.

## What ran
- Matrix: deposited `GSE102284_Expression_profiling_analysis-Coen.csv`, `(Reads)` columns only. These are Partek E/M estimated counts on RefSeq transcripts, about 52% integers and about 35 M per library. They were summed to gene symbol (`feature_column: Gene`, sum; 21,154 genes), rounded, and filtered at CPM ≥ 1 in ≥ 4 samples, leaving 13,146 genes.
- Alignment: the key was derived from the title (`Y_C_1` matched to `YC_1`, normalized). 36 of 36 samples aligned exactly. Groups: YC 9, YU 4, YR 4, OC 9, OU 6, OR 4.
- Model: one pydeseq2 model on all 36 samples, cells age × cond (`tools.joint_contrasts:run_joint_deseq2`). The planned contrasts were UN vs CON and RL vs CON within each age. RL vs UN within each age was exploratory.
- Enrichment: ORA on down-regulated genes (Enrichr GO and KEGG) and Hallmark GSEA for the 4 planned contrasts.

## DEG counts (applied = paper rule: raw p < 0.05, no FC cutoff, FIG4B legend; audit = BH FDR < 0.05)
| contrast | n (p<0.05) | up | down | audit FDR<0.05 | paper |
|---|---|---|---|---|---|
| UN vs CON, adult | 6799 | 3343 | 3456 | 6029 | not reported |
| RL vs CON, adult | 7763 | 4059 | 3704 | 7109 | not reported |
| UN vs CON, old | 7098 | 3541 | 3557 | 6375 | not reported |
| RL vs CON, old | 6822 | 3435 | 3387 | 6043 | not reported |
| RL vs UN, adult (exploratory) | 7559 | 3933 | 3626 | 6902 | — |
| RL vs UN, old (exploratory) | 7842 | 4027 | 3815 | 7279 | — |

The paper gives no DEG counts. Comparison with the paper is qualitative and agrees with it:
- KEGG oxidative phosphorylation, TCA cycle and fatty acid degradation are enriched among down-regulated genes in all 4 planned contrasts (adjusted p from 1e-38 to 1e-2). Hallmark OXPHOS  ... [1942 more characters]
