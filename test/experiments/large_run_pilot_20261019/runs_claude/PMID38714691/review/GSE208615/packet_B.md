# Review packet B (the analysis' decisions): GSE208615

## Mechanical flags

- **possible_reversed_contrast**: {"contrast": "grp_RE2_vs_SED", "control": "SED", "treatment": "RE2", "note": "the control side reads as exercise or the test side as control"}

## Samples per design level

### `grp`
- **EX14** (10): GSM6355628 / exe2-0-0_0; GSM6355629 / exe2-0-0_1; GSM6355630 / exe2-0-0_2; GSM6355631 / exe2-0-0_3; GSM6355632 / exe2-0-0_4; GSM6355633 / exe2-0-0_5; GSM6355634 / exe2-0-0_6; GSM6355635 / exe2-0-0_7; GSM6355636 / exe2-0-0_8; GSM6355637 / exe2-0-0_9
- **EX14D14** (10): GSM6355668 / exe2-14-0_0; GSM6355669 / exe2-14-0_1; GSM6355670 / exe2-14-0_2; GSM6355671 / exe2-14-0_3; GSM6355672 / exe2-14-0_4; GSM6355673 / exe2-14-0_5; GSM6355674 / exe2-14-0_6; GSM6355675 / exe2-14-0_7; GSM6355676 / exe2-14-0_8; GSM6355677 / exe2-14-0_9
- **EX14D7** (10): GSM6355648 / exe2-7-0_0; GSM6355649 / exe2-7-0_1; GSM6355650 / exe2-7-0_2; GSM6355651 / exe2-7-0_3; GSM6355652 / exe2-7-0_4; GSM6355653 / exe2-7-0_5; GSM6355654 / exe2-7-0_6; GSM6355655 / exe2-7-0_7; GSM6355656 / exe2-7-0_8; GSM6355657 / exe2-7-0_9
- **EX14D7RE2** (10): GSM6355658 / exe2-7-2_0; GSM6355659 / exe2-7-2_1; GSM6355660 / exe2-7-2_2; GSM6355661 / exe2-7-2_3; GSM6355662 / exe2-7-2_4; GSM6355663 / exe2-7-2_5; GSM6355664 / exe2-7-2_6; GSM6355665 / exe2-7-2_7; GSM6355666 / exe2-7-2_8; GSM6355667 / exe2-7-2_9
- **RE2** (10): GSM6355638 / exe0-0-2_0; GSM6355639 / exe0-0-2_1; GSM6355640 / exe0-0-2_2; GSM6355641 / exe0-0-2_3; GSM6355642 / exe0-0-2_4; GSM6355643 / exe0-0-2_5; GSM6355644 / exe0-0-2_6; GSM6355645 / exe0-0-2_7; GSM6355646 / exe0-0-2_8; GSM6355647 / exe0-0-2_9
- **SED** (10): GSM6355618 / sed_0; GSM6355619 / sed_1; GSM6355620 / sed_2; GSM6355621 / sed_3; GSM6355622 / sed_4; GSM6355623 / sed_5; GSM6355624 / sed_6; GSM6355625 / sed_7; GSM6355626 / sed_8; GSM6355627 / sed_9

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE208615"], "assay": "bulk RNA-seq (TruSeq, HiSeq, 50 bp SE) of bilateral dorsal hippocampus, 12-week-old male C57BL/6J mice, collected 1 h after a subthreshold 3-min OLM acquisition (S4.2.5.p1, S4.2.6.p1)", "factors": {"exercise pattern (initial-delay-reactivation days)": ["0-0-0 (sedentary)", "14-0-0", "0-0-2", "14-7-0", "14-7-2", "14-14-0"]}, "sample_inclusion": "OLM-trained mice of the six exercise patterns (n=10 each in GEO); RIN>9 (S4.2.6.p1). The GEO 'HC' samples (0-0-0, no OLM) are not part of the paper's described RNA-seq contrasts.", "primary_estimand": "Effect of each exercise pattern versus sedentary control on dorsal-hippocampus gene expression during OLM consolidation (1 h post acquisition); focus on 14-0-0 and 14-7-2, the patterns that enable long-term memory (S2.2.p1, S4.2.8.p1)", "planned_contrasts": ["14-0-0 vs 0-0-0 sedentary (S4.2.8.p1, Fig. 2D/F)", "14-7-2 vs 0-0-0 sedentary (S4.2.8.p1, Fig. 2D/H)", "14-7-0 vs 0-0-0 sedentary (S4.2.8.p1, Fig. 2C)", "14-14-0 vs 0-0-0 sedentary (S4.2.8.p1, Fig. 2C)", "0-0-2 vs 0-0-0 sedentary (S4.2.8.p1, Fig. 2C)"], "repeated_measure_unit": "none (one sample per mouse, independent groups)", "batch": "tissue collected over two separate days with equal n per group (S4.2.5.p1) = GEO 'harvest cohort'", "normalization": "Tuxedo / cuffnorm FPKM (S4.2.8.p1)", "paper_method": "Cyber-T Bayesian-regularized t-test, each exercise group vs sedentary pairwise, on FPKM (S4.2.8.p1); linear regression models as a secondar ... [435 more characters]

reasoning: Methods S4.2.8.p1: FPKM from Tuxedo; Cyber-T per pair of groups (exercise vs sedentary, 1 h after acquisition); 'only genes with uncorrected p value < 0.05 were used'. No fold-change rule stated. Five exercise groups listed in S4.2.8.p1. DA.p1 names GSE208615.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE208615\\GSE208615_fpkm.csv.gz", "owned": true, "checks": ["DA.p1 names GSE208615", "metadata: Mus musculus, male, adult, dorsal hippocampus, total RNA, RNA-Seq", "exercise parameters 0-0-0/14-0-0/0-0-2/14-7-0/14-7-2/14-14-0 match the paper's groups", "two harvest cohorts match the two collection days (S4.2.5.p1)"], "accession": "GSE208615", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE208615\\GSE208615_metadata.csv"}

reasoning: Accession cited in the paper's data availability; sample annotations match the paper's design exactly.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 70, "n_metadata": 70, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM6355608": "HC home-cage 0-0-0 without OLM; not in the paper's exercise-vs-sedentary contrasts (S4.2.8.p1)", "GSM6355609": "HC home-cage 0-0-0 without OLM; not in the paper's contrasts", "GSM6355610": "HC home-cage 0-0-0 without OLM; not in the paper's contrasts", "GSM6355611": "HC home-cage 0-0-0 without OLM; not in the paper's contrasts", "GSM6355612": "HC home-cage 0-0-0 without OLM; not in the paper's contrasts", "GSM6355613": "HC home-cage 0-0-0 without OLM; not in the paper's contrasts", "GSM6355614": "HC home-cage 0-0-0 without OLM; not in the paper's contrasts", "GSM6355615": "HC home-cage 0-0-0 without OLM; not in the paper's contrasts", "GSM6355616": "HC home-cage 0-0-0 without OLM; not in the paper's contrasts", "GSM6355617": "HC home-cage 0-0-0 without OLM; not in the paper's contrasts"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\aligned\\aligned_metadata_kept.csv", "columns": {"cohort": {"alias_of": "characteristics_ch1.4.harvest cohort", "recode": {"1": "C1", "2": "C2"}}, "grp": {"source": "characteristics_ch1.2.exercise parameters", "regex": "^(\\d+-\\d+-\\d+)$", "recode": {"0-0-0": "SED", "14-0-0": "EX14", "0-0-2": "RE2", "14-7-0": "EX14D7", "14-7-2": "EX14D7RE2", "14-14-0": "EX14D14"}}}, "output": "test\\experiments\\large_ ... [300 more characters]

reasoning: Matrix columns equal metadata title (70/70). The sedentary control is 0-0-0 with OLM (sed_*), because every compared group was sampled 1 h after OLM acquisition (S4.2.8.p1). HC (0-0-0, OLM=No) would confound learning with exercise and is excluded.

rejected alternatives: [{"value": "pool HC with sed as 0-0-0 control", "reason_rejected": "HC did not undergo OLM; the paper's contrasts are 1 h post acquisition in all groups"}]

### matrix (valid, not_started)

final: {"matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\aligned\\aligned_matrix.csv", "sha256": "1a24b26e6b99a6a19bcad72da63fcae8cec3adf8185e1c92046f08be2d7fb01c", "n_features": 24346, "n_samples": 60, "annotation_columns_dropped": ["GSM6355608", "GSM6355609", "GSM6355610", "GSM6355611", "GSM6355612", "GSM6355613", "GSM6355614", "GSM6355615", "GSM6355616", "GSM6355617"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 21244.0, "median": 1.45472, "integer_fraction": 0.2768, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File named fpkm; data_processing: 'normalization to FPKM values performed using Tuxedo cuffnorm'; 28% integers (mostly zeros), non-integer values, median 1.46. Paper input is FPKM (S4.2.8.p1). Not counts, so DESeq2/edgeR are not applicable.

### design (valid, not_started)

final: {"analysis_type": "multi-group, one control", "design_column": "grp", "formula": "~ grp", "control": "SED", "contrasts": [{"name": "grp_EX14_vs_SED", "control": "SED", "treatment": "EX14", "role": "primary"}, {"name": "grp_EX14D7RE2_vs_SED", "control": "SED", "treatment": "EX14D7RE2", "role": "primary"}, {"name": "grp_EX14D7_vs_SED", "control": "SED", "treatment": "EX14D7", "role": "secondary"}, {"name": "grp_EX14D14_vs_SED", "control": "SED", "treatment": "EX14D14", "role": "secondary"}, {"name": "grp_RE2_vs_SED", "control": "SED", "treatment": "RE2", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\suitability\\suitability.md", "n_comparisons": 15, "n_analyzable": 15}}

reasoning: Six independent groups (n=10 each) with one sedentary control; the paper compares each exercise pattern to sedentary (S4.2.8.p1). One model with planned contrasts vs SED; levels are not pooled. 14-0-0 and 14-7-2 are primary because they carry the paper's main claim (S2.2.p1).

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "cohort", "disposition": "sensitivity only: balanced harvest day (5/group/day, S4.2.5.p1); not in the paper's model"}], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 60, "n_columns": 6, "columns": ["Intercept", "grp_EX14D14", "grp_EX14D7", "grp_EX14D7RE2", "grp_RE2", "grp_SED"], "rank": 6, "full_rank": true, "residual_df": 54, "levels": {"grp": {"SED": 10, "EX14": 10, "RE2": 10, "EX14D7": 10, "EX14D7RE2": 10, "EX14D14": 10}}, "cells": [{"cell": ["EX14"], "n": 10}, {"cell": ["EX14D14"], "n": 10}, {"cell": ["EX14D7"], "n": 10}, {"cell": ["EX14D7RE2"], "n": 10}, {"cell": ["RE2"], "n": 10}, {"cell": ["SED"], "n": 10}], "min_cell_size": 10, "missing_values": {}}, "confounding": [{"column": "cohort", "n_levels": 2, "status": "crossed", "crosstab": {"EX14": {"C1": 5, "C2": 5}, "EX14D14": {"C1": 5, "C2": 5}, "EX14D7": {"C1": 5, "C2": 5}, "EX14D7RE2": {"C1": 5, "C2": 5}, "RE2": {"C1": 5, "C2": 5}, "SED": {"C1": 5, "C2": 5}}}]}

reasoning: Independent animals, one sample each. Harvest cohort is perfectly balanced across groups so it is not confounded with exercise; the paper did not adjust for it, so the primary model omits it and a sensitivity run adds it.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (limma-trend moderated t on log2(FPKM+1), one model ~ grp, contrasts vs SED)", "formula": "~ grp", "paper_route": {"method": "Cyber-T Bayesian-regularized t-test, pairwise", "status": "blocked", "reason": "no Cyber-T executor in the repository; limma's empirical-Bayes moderated t is the validated analogue (both shrink per-gene variance toward a prior)"}, "deviations": ["limma moderated t from one six-group model instead of pairwise Cyber-T (pooled residual variance across groups)", "log2(FPKM+1) transform for linear modelling", "genes filtered to FPKM >= 1 in >= 10 samples (smallest group n) to remove unexpressed genes; paper states no filter"], "transform": "log2(x+1)"}

reasoning: FPKM is log-scale-compatible after log2(x+1); limma is the policy route for FPKM. Cyber-T itself cannot run here.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper rule (uncorrected p < 0.05, no FC cutoff) applied to limma p-values instead of Cyber-T; BH FDR < 0.05 reported as audit."}

reasoning: S4.2.8.p1: 'only genes with both uncorrected p value < 0.05 were used for analysis'.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "limma_joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 60, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint\\DEG_results_grp_EX14_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint\\DEG_results_grp_EX14D7RE2_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint\\DEG_results_grp_EX14D7_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint\\DEG_results_grp_EX14D14_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint\\DEG_results_grp_RE2_vs_SED.csv"], "counts": {"limma_joint/grp_EX14_vs_SED": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13353, "n_significant": 1543, "n_up": 1062, "n_down": 481, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13353, "n_significant": 8, "n_up": 3, "n_down": 5, "deg_sanity": "ok"}}, "limma_joint/grp_EX14D7RE2_vs_SED": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13353, "n_significant": 1017, "n_up": 522, "n_down": 495, "deg_sani ... [965 more characters]

reasoning: One limma model on the six OLM groups; contrasts of each exercise pattern vs sedentary as in S4.2.8.p1.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "limma_joint_cohort", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 60, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint_cohort\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell) + C(cov0)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint_cohort\\DEG_results_grp_EX14_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint_cohort\\DEG_results_grp_EX14D7RE2_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint_cohort\\DEG_results_grp_EX14D7_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint_cohort\\DEG_results_grp_EX14D14_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\limma_joint_cohort\\DEG_results_grp_RE2_vs_SED.csv"], "counts": {"limma_joint_cohort/grp_EX14_vs_SED": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13353, "n_significant": 1576, "n_up": 1090, "n_down": 486, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13353, "n_significant": 9, "n_up": 4, "n_down": 5, "deg_sanity": "ok"}}, "limma_joint_cohort/grp_EX14D7RE2_vs_SED": {"applied": {"rule": "pvalue < 0.05", "n ... [1063 more characters]

reasoning: Same model adjusted for the balanced harvest day (S4.2.5.p1).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_joint/grp_EX14_vs_SED", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\enrichment_limma_joint_grp_EX14_vs_SED\\ora_up\\DEG_results_grp_EX14_vs_SED_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\enrichment_limma_joint_grp_EX14_vs_SED\\ora_up\\DEG_results_grp_EX14_vs_SED_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\enrichment_limma_joint_grp_EX14_vs_SED\\ora_up\\DEG_results_grp_EX14_vs_SED_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\enrichment_limma_joint_grp_EX14_vs_SED\\ora_up\\DEG_results_grp_EX14_vs_SED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 1062 Mouse genes (direction=up, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Fatty Acid Beta-Oxidation (GO:0006635) | padj=7.38e-06 | overlap=1 ... [1271 more characters]

reasoning: Paper ran GO/KEGG (DAVID) on up-regulated DEGs (S4.2.8.p1, Fig. S5-S6).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_joint/grp_EX14_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\enrichment_limma_joint_grp_EX14_vs_SED\\gsea\\DEG_results_grp_EX14_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13353 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 28 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_PROTEIN_SECRETION | NES=2.22 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.96 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.86 | NOM p=0.00e+00 | FDR q=2.21e-03 - HALLMARK_PEROXISOME | NES=1.84 | NOM p=1.32e-03 | FDR q=2.56e-03 - HALLMARK_BILE_ACID_METABOLISM | NES=1.83 | NOM p=1.37e-03 | FDR q=2.13e-03 - HALLMARK_ANDROGEN_RESPONSE | NES=1.78 | NOM p=0.00e+00 | FDR q=2.81e-03 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.68 | NOM p=0.00e+00 | FDR q=9.96e-03 - HALLMARK_ADIPOGENESIS | NES=1.67 | NOM p=0.00e+00 | FDR q=1.08e-02 - HALLMARK_COAGULATION | NES=1.64 | NOM p=1.38e-03 | FDR q=1.20e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=-2.04 | NOM p=0.00e+00 | FDR q=2.10e-03 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NE ... [414 more characters]

reasoning: Paper ran GO/KEGG (DAVID) on up-regulated DEGs (S4.2.8.p1, Fig. S5-S6).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_joint/grp_EX14D7RE2_vs_SED", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\enrichment_limma_joint_grp_EX14D7RE2_vs_SED\\ora_up\\DEG_results_grp_EX14D7RE2_vs_SED_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\enrichment_limma_joint_grp_EX14D7RE2_vs_SED\\ora_up\\DEG_results_grp_EX14D7RE2_vs_SED_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\enrichment_limma_joint_grp_EX14D7RE2_vs_SED\\ora_up\\DEG_results_grp_EX14D7RE2_vs_SED_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\enrichment_limma_joint_grp_EX14D7RE2_vs_SED\\ora_up\\DEG_results_grp_EX14D7RE2_vs_SED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 522 Mouse genes (direction=up, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Positive Regulation Of ... [1316 more characters]

reasoning: Second memory-enabling pattern (S2.2.p1).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_joint/grp_EX14D7RE2_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38714691\\GSE208615\\results\\enrichment_limma_joint_grp_EX14D7RE2_vs_SED\\gsea\\DEG_results_grp_EX14D7RE2_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13353 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 18 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_PROTEIN_SECRETION | NES=1.67 | NOM p=2.09e-03 | FDR q=3.65e-02 - HALLMARK_ANDROGEN_RESPONSE | NES=1.38 | NOM p=4.29e-02 | FDR q=2.49e-01 - HALLMARK_UV_RESPONSE_DN | NES=1.36 | NOM p=1.84e-02 | FDR q=1.96e-01 - HALLMARK_PEROXISOME | NES=1.34 | NOM p=4.27e-02 | FDR q=1.77e-01 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.32 | NOM p=8.73e-02 | FDR q=1.70e-01 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.17 | NOM p=1.50e-01 | FDR q=4.12e-01 - HALLMARK_HEME_METABOLISM | NES=1.09 | NOM p=2.74e-01 | FDR q=6.17e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=1.06 | NOM p=3.62e-01 | FDR q=6.29e-01 - HALLMARK_PI3K_AKT_MTOR_SIGNALING | NES=1.01 | NOM p=4.09e-01 | FDR q=7.32e-01 - HALLMARK_MYC_TARGETS_V1 | NES=0.94 | NOM p=6.31e-01 | FDR q=9.03e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYOGENESIS | NES=-1.83 | NOM p=0.00e+00 | FDR q=1.63e-02 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-1.82 | NOM  ... [429 more characters]

reasoning: Second memory-enabling pattern (S2.2.p1).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper's per-group DEG counts are only in Fig. 2C/D (not in text), so counts cannot be compared numerically; the comparable statements are the 21-gene 14-0-0 ∩ 14-7-2 up-regulated intersection and Acvr1c/Bdnf up in both.", "Uncorrected p < 0.05 across ~15k genes admits many false positives by design."], "results": {"limma_joint/grp_EX14_vs_SED": {"n_deg": 1543, "up": 1062, "down": 481, "rule": "pvalue < 0.05", "audit_n": 8}, "limma_joint/grp_EX14D7RE2_vs_SED": {"n_deg": 1017, "up": 522, "down": 495, "rule": "pvalue < 0.05", "audit_n": 7}, "limma_joint/grp_EX14D7_vs_SED": {"n_deg": 866, "up": 464, "down": 402, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_joint/grp_EX14D14_vs_SED": {"n_deg": 823, "up": 607, "down": 216, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_joint/grp_RE2_vs_SED": {"n_deg": 482, "up": 219, "down": 263, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_joint_cohort/grp_EX14_vs_SED": {"n_deg": 1576, "up": 1090, "down": 486, "rule": "pvalue < 0.05", "audit_n": 9}, "limma_joint_cohort/grp_EX14D7RE2_vs_SED": {"n_deg": 1025, "up": 530, "down": 495, "rule": "pvalue < 0.05", "audit_n": 7}, "limma_joint_cohort/grp_EX14D7_vs_SED": {"n_deg": 873, "up": 476, "down": 397, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_joint_cohort/grp_EX14D14_vs_SED": {"n_deg": 824, "up": 604, "down": 220, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_joint_cohort/grp_RE2_vs_SED": {"n_deg": 490, "up": 223, "down": 267, "rule": "pvalue < 0. ... [634 more characters]

reasoning: limma route is a declared deviation from Cyber-T; paper's threshold kept. Acvr1c expected up in EX14 and EX14D7RE2, not in EX14D7 (S2.2.p1).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 60 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "Cyber-T Bayesian-regularized t, pairwise",
    "data": "no Cyber-T executor; limma-trend moderated t",
    "disposition": "declared_deviation"
  },
  {
    "item": "HC samples",
    "paper": "not described among RNA-seq contrasts",
    "data": "10 GEO samples 0-0-0 without OLM",
    "disposition": "excluded"
  },
  {
    "item": "paper DEG counts",
    "paper": "graphical only (Fig. 2C/D)",
    "data": "-",
    "disposition": "not_comparable"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID38714691 / GSE208615

## What ran
- `case_runner inspect GSE208615` → one matrix, `GSE208615_fpkm.csv.gz` (24,346 genes × 70 samples, Tuxedo/cuffnorm FPKM, gene symbols). Columns align exactly to metadata `title` (70/70).
- `case_runner execute case_spec.json` → status completed; the contract validator reported 15 records and 0 errors.
- Decisions:
  - **Samples:** 60 OLM-trained mice in 6 groups of n=10: SED (0-0-0), EX14 (14-0-0), RE2 (0-0-2), EX14D7 (14-7-0), EX14D7RE2 (14-7-2), EX14D14 (14-14-0). I excluded the 10 GEO "HC" samples (0-0-0 with no OLM). The paper's contrasts are all taken 1 h after OLM acquisition (S4.2.8.p1), so HC is not part of them.
  - **Matrix:** FPKM.
  - **Method:** limma-trend on log2(FPKM+1), one model `~ grp` with 5 contrasts vs SED. EX14 and EX14D7RE2 are primary (S2.2.p1); the other three are secondary.
  - **Sensitivity run:** the same model plus `cohort` (harvest day). Harvest day is balanced at 5 per group per day (S4.2.5.p1), so it is not confounded with exercise.
  - **Enrichment:** ORA on up-regulated genes plus Hallmark GSEA, for EX14 and EX14D7RE2.
- **Threshold:** the paper's own rule, uncorrected p < 0.05 with no fold-change cutoff (S4.2.8.p1). It is applied to limma p-values (`paper_on_deviation_route`). BH FDR < 0.05 is reported separately as an audit count.

## DEG counts (p < 0.05, no FC rule) — total (up/down) [audit FDR<0.05]
| Contrast | ours | with cohort covariate | paper |
|---|---|---|---|
| 14-0-0 vs SED | 1543 (1062/481) [8] | 1576 [9] | Fig. 2C/D only, no number in text |
| 14-7-2 vs SED | 1017 (522/495) [7] | 1025 [7] | Fig. 2C/D only |
| 14-7-0 vs SED | 866 (464/402) [0] | 873 | Fig. 2C only |
| 14-14-0 vs SED | 823 (607/216) [0] | 824 | Fig. 2C only |
| 0-0-2 vs SED | 482 (219/263) [0] | 490 | Fig. 2C only |

- **Genes up in both 14-0-0 and 14-7-2:** 273 in our run vs **21 in the paper** (Data Table S1). This is the only numeric paper result we can compare.
- **Named genes, which match the paper's direction:**
  - Acvr1c is up in 14-0-0 (log2FC 0.43, p=8e-4) and in 14-7-2 (log2FC 0.43, p=8e-4).
  - It is not significant in 14-7-0 (log2FC 0.19, p=0.12), as the paper reports.
  - Bdnf is up in 14-0-0 (log2FC 0.55, p=0.012) and in 14-7-2 (log2FC 0.44, p=0.044).
  - Both genes are in our 273-gene intersection.
  - Neither gene passes FDR; the paper's rule is raw p.
- **Enrichment (kept separate from the DE result):**
  - 14-0-0, up-regulated genes, GO cellular component ORA: Lysosome t ... [1357 more characters]
