# Review packet B (the analysis' decisions): GSE306842

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "grp", "pairs_or_sets": 6, "samples_linked": 24, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Samples per design level

### `grp`
- **CTRL** (6): GSM9210532 / Muscle.30mins.Control.1 / Library name: D24-12376,Singular G4; GSM9210533 / Muscle.30mins.Control.2 / Library name: D24-12377,Singular G4; GSM9210534 / Muscle.30mins.Control.3 / Library name: D24-12378,Singular G4; GSM9210535 / Muscle.30mins.Control.4 / Library name: D24-12379,Singular G4; GSM9210536 / Muscle.30mins.Control.5 / Library name: D24-12380,Singular G4; GSM9210537 / Muscle.30mins.Control.6 / Library name: D24-12381,Singular G4
- **F1** (6): GSM9210538 / Muscle.30mins.x1Hz.1 / Library name: D24-12382,Singular G4; GSM9210539 / Muscle.30mins.x1Hz.2 / Library name: D24-12383,Singular G4; GSM9210540 / Muscle.30mins.x1Hz.3 / Library name: D24-12384,Singular G4; GSM9210541 / Muscle.30mins.x1Hz.4 / Library name: D24-12385,Singular G4; GSM9210542 / Muscle.30mins.x1Hz.5 / Library name: D24-12386,Singular G4; GSM9210543 / Muscle.30mins.x1Hz.6 / Library name: D24-12387,Singular G4
- **F10** (6): GSM9210550 / Muscle.30mins.x10Hz.1 / Library name: D24-12394,Singular G4; GSM9210551 / Muscle.30mins.x10Hz.2 / Library name: D24-12395,Singular G4; GSM9210552 / Muscle.30mins.x10Hz.3 / Library name: D24-12396,Singular G4; GSM9210553 / Muscle.30mins.x10Hz.4 / Library name: D24-12397,Singular G4; GSM9210554 / Muscle.30mins.x10Hz.5 / Library name: D24-12398,Singular G4; GSM9210555 / Muscle.30mins.x10Hz.6 / Library name: D24-12399,Singular G4
- **F4** (6): GSM9210544 / Muscle.30mins.x4Hz.1 / Library name: D24-12388,Singular G4; GSM9210545 / Muscle.30mins.x4Hz.2 / Library name: D24-12389,Singular G4; GSM9210546 / Muscle.30mins.x4Hz.3 / Library name: D24-12390,Singular G4; GSM9210547 / Muscle.30mins.x4Hz.4 / Library name: D24-12391,Singular G4; GSM9210548 / Muscle.30mins.x4Hz.5 / Library name: D24-12392,Singular G4; GSM9210549 / Muscle.30mins.x4Hz.6 / Library name: D24-12393,Singular G4

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE306860 (SuperSeries, S10.p1)", "GSE306842"], "experiment": "30-min daily optical exercise experiment (S2.2.p2); RNA extracted DM day 14 (S5.6.p1); 0.6 mL media (S5.2.p1)", "assay": "bulk poly(A) RNA-seq, Singular G4 50-bp PE; nf-core/rnaseq 3.11.1, GRCm39/Ensembl (S5.6.p2-p3)", "system": "C2C12 ChR2(H134R)-tdTomato mouse myotube 2D monolayers on grooved fibrin, 24-well plates (S2.2.p1, S5.2.p1)", "factors": {"stimulation": ["unstimulated control", "1 Hz", "4 Hz", "10 Hz"]}, "sample_inclusion": "6 biological replicates (wells) per condition, 24 samples per experiment (FIG2 caption, S2.2.p2, S5.4.p1)", "primary_estimand": "effect of ~2 weeks of daily 30-min optogenetic exercise at 1, 4 or 10 Hz vs unstimulated control on muscle gene expression, within the 30-min experiment", "planned_contrasts": ["1 Hz vs control (30 min) (FIG2 d; S2.3.p1; paper count only in a bar chart)", "4 Hz vs control (30 min) (FIG2 d; S2.3.p1; paper count only in a bar chart)", "10 Hz vs control (30 min) (FIG2 d; S2.3.p1; paper count only in a bar chart)"], "repeated_measure_unit": "none: each well is one independent sample", "paper_method": "DESeq2 (R 4.2.0) with apeglm LFC shrinkage, BH-adjusted p (S5.6.p4); each condition vs control within its experiment (FIG2 d caption)", "paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false, "effect_note": "log2(fold change) > 0.5 on the apeglm-shrunken LFC; up and down b ... [522 more characters]

reasoning: S2.2.p2 and FIG2 describe two separate experiments (30 and 60 min), each with its own unstimulated control (n=6) and 1/4/10 Hz arms (n=6). GSE306842 is the 30-min experiment. FIG2 d caption gives the DEG rule: log2FC > 0.5 and padj < 0.05, each condition vs control. S5.6.p4: DESeq2 + apeglm. The DEG counts are drawn as bars only; no numbers appear in the text.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE306842\\GSE306842_salmon.merged.gene_counts.tsv.gz", "owned": true, "checks": ["metadata series_id = 'GSE306842,GSE306860'; the paper's data statement names SuperSeries GSE306860 (S10.p1)", "titles 'Muscle.30mins.<Control|x1Hz|x4Hz|x10Hz>.<1-6>' match the 30-min design of S2.2.p2", "cell line C2C12, genotype ChR2::tdTomato, organism Mus musculus match S5.2.p1", "GEO contact Ritu Raman, MIT = senior author", "matrix has 24 columns (6 per condition) matching the 24 GSMs; the other experiment is GSE306857 (60 min)"], "accession": "GSE306842", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE306842\\GSE306842_metadata.csv"}

reasoning: GEO series is a SubSeries of the paper's SuperSeries; sample labels, cell line, genotype and design agree with the paper.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 24, "n_metadata": 24, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^Muscle\\.30mins\\.(Control|x1Hz|x4Hz|x10Hz)[.-]\\d$", "recode": {"Control": "CTRL", "x1Hz": "F1", "x4Hz": "F4", "x10Hz": "F10"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\aligned\\design_metadata.csv", "sha256": "f1b50d19c26ae2e7764222cd5897f6a711735531034d424e625ca4a6c08e1dc2", "levels": {"grp": {"CTRL": 6, "F1": 6, "F4": 6, "F10": 6}}}}

reasoning: Matrix columns are condition labels (X1Hz.1 / x1Hz.1, Control.1); the GSM title carries the same label after 'Muscle.<n>mins.'. key = that suffix, matched ignoring case and separators ('x1Hz-1' = 'X1Hz.1'). Not positional. grp recoded to formula-safe levels CTRL/F1/F4/F10.

### matrix (valid, not_started)

final: {"paper_input": "nf-core/rnaseq output into DESeq2 (S5.6.p3-p4)", "matrix_type": "estimated counts (Salmon gene-level counts from nf-core/rnaseq)", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\aligned\\aligned_matrix.csv", "sha256": "5d7986df0fb1aa351fae7098b8aa72f21ec2f21f0b758619b1777b46a675fb35", "n_features": 56941, "n_samples": 24, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 256883.001, "median": 0.0, "integer_fraction": 0.9132, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name salmon.merged.gene_counts; data_processing: 'Gene-level raw counts and TPM generated by Salmon'; ~91% integer values, the rest fractional; 56,941 Ensembl genes: Salmon estimated counts. Rounded before DESeq2 (the paper does not state its import method).

rejected alternatives: [{"value": "GSE306842_salmon.merged.gene_tpm.tsv.gz", "reason_rejected": "TPM is length-normalized; DESeq2 needs counts"}]

### design (valid, not_started)

final: {"analysis_type": "one control, several stimulation levels (one model, planned contrasts vs control)", "design_column": "grp", "formula": "~ grp", "contrasts": [{"name": "grp_F1_vs_CTRL", "control": "CTRL", "treatment": "F1", "role": "primary"}, {"name": "grp_F4_vs_CTRL", "control": "CTRL", "treatment": "F4", "role": "primary"}, {"name": "grp_F10_vs_CTRL", "control": "CTRL", "treatment": "F10", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: Within one experiment, wells were assigned to control or one stimulation frequency; each frequency vs unstimulated control is the paper's estimand (FIG2 d). Controls twitch spontaneously (S3.1.p2): the contrast is optical stimulation vs none.

rejected alternatives: [{"value": "pool 1/4/10 Hz vs control", "reason_rejected": "paper reports each frequency separately (FIG2 d); levels must not be pooled"}, {"value": "30 min vs 60 min across GSE306842/GSE306857", "reason_rejected": "duration is aliased with experiment: separate cultures, harvest day 14 vs 16, media 0.6 vs 1.5 mL (S2.2.p3, S5.6.p1); the paper compares DE only within an experiment"}, {"value": "pairwise frequency contrasts (F1 vs F4 etc.)", "reason_rejected": "not a paper estimand; not run"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 24, "n_columns": 4, "columns": ["Intercept", "grp_F1", "grp_F10", "grp_F4"], "rank": 4, "full_rank": true, "residual_df": 20, "levels": {"grp": {"CTRL": 6, "F1": 6, "F4": 6, "F10": 6}}, "cells": [{"cell": ["CTRL"], "n": 6}, {"cell": ["F1"], "n": 6}, {"cell": ["F10"], "n": 6}, {"cell": ["F4"], "n": 6}], "min_cell_size": 6, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 24, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 24, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.cell line", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.cell type", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.genotype", "n_levels": 1, "status": "constant"}, {"column": "grow ... [1772 more characters]

reasoning: Each sample is an independent well; no plate, batch, lane or pairing recorded in GEO; the paper models none (S5.6.p4). No covariate added from column names.

### method (valid, not_started)

final: {"matrix_type": "estimated counts (Salmon gene-level counts from nf-core/rnaseq)", "method": "DESeq2 (R, Wald) with apeglm LFC shrinkage", "formula": "~ grp", "paper_route": {"method": "DESeq2 + apeglm (R)", "status": "reproduced"}, "rounding_documented": true, "deviations": ["Salmon estimated counts rounded to integers (paper's import method unstated)", "R 4.6 / DESeq2 1.51 instead of R 4.2.0", "results() alpha = 0.05 (paper FDR cutoff); the paper does not state it"]}

reasoning: S5.6.p4: DESeq2 with apeglm shrinkage; the matrix holds counts so the route runs as stated. One model on all 24 samples, contrasts vs CTRL; apeglm shrinks each grp coefficient (log2FoldChange = shrunken, MLE kept as log2FoldChange_mle). pydeseq2 joint model (MLE LFC) runs as a sensitivity check.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: FIG2 d caption and S2.3.p1: log2(FC) > 0.5 and padj < 0.05 (bars show up and down, so |log2FC| > 0.5), on the apeglm-shrunken LFC carried in log2FoldChange of the primary tables. Audit: padj < 0.05 alone.

### execution (valid, completed)

final: {"method": "run_r_de", "subset": "deseq2_apeglm", "role": "primary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 24, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\aligned\\aligned_matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\results\\deseq2_apeglm\\DEG_results_grp_F1_vs_CTRL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\results\\deseq2_apeglm\\DEG_results_grp_F4_vs_CTRL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\results\\deseq2_apeglm\\DEG_results_grp_F10_vs_CTRL.csv"], "counts": {"deseq2_apeglm/grp_F1_vs_CTRL": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 17426, "n_significant": 2337, "n_up": 1124, "n_down": 1213, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17426, "n_significant": 5019, "n_up": 2493, "n_down": 2526, "deg_sanity": "ok"}}, "deseq2_apeglm/grp_F4_vs_CTRL": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 18036, "n_significant": 2577, "n_up": 1327, "n_down": 1250, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 18036, "n_significant": 5506, "n_up": 2688, "n_down": 2818, "deg_sanity": "ok"}}, "deseq2_apeglm/grp_F10_vs_CTRL": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 12556, "n_significant": 197, "n_up": 137, "n_do ... [155 more characters]

reasoning: paper route: R DESeq2 ~ grp on all 24 samples, apeglm shrinkage per frequency coefficient

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "pydeseq2_mle", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 24, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\results\\pydeseq2_mle\\DEG_results_grp_F1_vs_CTRL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\results\\pydeseq2_mle\\DEG_results_grp_F4_vs_CTRL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\results\\pydeseq2_mle\\DEG_results_grp_F10_vs_CTRL.csv"], "counts": {"pydeseq2_mle/grp_F1_vs_CTRL": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 16816, "n_significant": 2739, "n_up": 1302, "n_down": 1437, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 16816, "n_significant": 5040, "n_up": 2502, "n_down": 2538, "deg_sanity": "ok"}}, "pydeseq2_mle/grp_F4_vs_CTRL": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 17424, "n_significant": 2980, "n_up": 1514, "n_down": 1466, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17424, "n_significant": 5503, "n_up": 2691, "n_down": 2812, "deg_sanity": "ok"}}, "pydeseq2_mle/grp_F10_vs_CTRL": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 12553, "n_significant": 285, ... [174 more characters]

reasoning: pydeseq2 joint model, MLE LFC (no shrinkage): shows how much the count depends on shrinkage and implementation

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2_apeglm/grp_F1_vs_CTRL", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\results\\enrichment_deseq2_apeglm_grp_F1_vs_CTRL\\gsea\\DEG_results_grp_F1_vs_CTRL_GSEA_Hallmark.csv"], "summary": "GSEA complete on 31086 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 46 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_MYOGENESIS | NES=2.73 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.38 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UV_RESPONSE_DN | NES=2.05 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=2.05 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.96 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=1.91 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=1.90 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.88 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=1.87 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.82 | NOM p=0.00e+00 | FDR q=3.30e-04 ### Top 7 DOWN (NES < 0, depleted in treatment): - HALLMARK_E2F_TARGETS | NES=-1.63 | NOM p=0.00e+00 | FDR q=5.85e-03 - HALLMARK_MYC_TARGETS_V1 | NES=-1.63 | NOM p=0.00e+00 | ... [416 more characters]

reasoning: S5.6.p4 / FIG3 / Fig. S5: preranked GSEA on Hallmark per condition vs control; Wald stat carries LFC sign and p

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2_apeglm/grp_F4_vs_CTRL", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\results\\enrichment_deseq2_apeglm_grp_F4_vs_CTRL\\gsea\\DEG_results_grp_F4_vs_CTRL_GSEA_Hallmark.csv"], "summary": "GSEA complete on 31086 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 32 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_MYOGENESIS | NES=2.72 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.57 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.91 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=1.88 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.78 | NOM p=0.00e+00 | FDR q=2.64e-04 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.77 | NOM p=0.00e+00 | FDR q=2.20e-04 - HALLMARK_PANCREAS_BETA_CELLS | NES=1.59 | NOM p=1.35e-02 | FDR q=6.03e-03 - HALLMARK_MTORC1_SIGNALING | NES=1.51 | NOM p=0.00e+00 | FDR q=2.22e-02 - HALLMARK_PEROXISOME | NES=1.50 | NOM p=5.96e-03 | FDR q=2.26e-02 - HALLMARK_BILE_ACID_METABOLISM | NES=1.48 | NOM p=3.83e-03 | FDR q=2.24e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=-1.53 | NOM p=1.98e-03 | FDR q=5.55e-02 - HALLMARK_INTERFERON_ALPHA_RESPON ... [416 more characters]

reasoning: S5.6.p4 / FIG3 / Fig. S5: preranked GSEA on Hallmark per condition vs control; Wald stat carries LFC sign and p

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2_apeglm/grp_F10_vs_CTRL", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42272974\\GSE306842\\results\\enrichment_deseq2_apeglm_grp_F10_vs_CTRL\\gsea\\DEG_results_grp_F10_vs_CTRL_GSEA_Hallmark.csv"], "summary": "GSEA complete on 31086 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 43 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.23 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYOGENESIS | NES=2.05 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=1.89 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=1.86 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.60 | NOM p=0.00e+00 | FDR q=6.28e-03 - HALLMARK_ADIPOGENESIS | NES=1.46 | NOM p=0.00e+00 | FDR q=2.59e-02 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.46 | NOM p=3.15e-02 | FDR q=2.25e-02 - HALLMARK_PANCREAS_BETA_CELLS | NES=1.37 | NOM p=5.94e-02 | FDR q=4.78e-02 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.25 | NOM p=5.70e-02 | FDR q=1.48e-01 - HALLMARK_UV_RESPONSE_UP | NES=1.23 | NOM p=7.55e-02 | FDR q=1.57e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_HYPOXIA | NES=-1.95 | NOM p=0.00e+00 | FDR q=1.46e-03 - HALLMARK_MITOTIC_SPINDLE | NES=-1.91 | NOM p=0.00e+00 | FDR ... [419 more characters]

reasoning: S5.6.p4 / FIG3 / Fig. S5: preranked GSEA on Hallmark per condition vs control; Wald stat carries LFC sign and p

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper DEG counts are only drawn as bars in Fig. 2d; no numeric comparison is possible, only the qualitative ordering (10 Hz fewest).", "Controls are unstimulated but twitch spontaneously (S3.1.p2): the estimand is optical stimulation vs none, not exercise vs sedentary.", "Duration (30 vs 60 min) is aliased with experiment/culture batch and is not compared.", "Contradiction (S2.3.p3): paper says 10 Hz 30 min had no significant effect on myogenic genes; our DESeq2 gives Myog (LFC 0.54, padj 0.002), Myod1 (0.53, 0.046) and Myh3 (0.74, 0.001) significant at 10 Hz, while Myh1/2/4/7/8 and Pax7 are not. The paper's Fig. 2e/f used two-way ANOVA (Prism), not DESeq2.", "Contradiction (S2.7.p1): paper says ROS pathway significantly down at 1 Hz 30 min; our Hallmark ROS NES +0.95, q 0.58 (not significant, opposite sign). Interferon alpha/gamma de-enrichment and Myogenesis as top set agree.", "Myog at 1 Hz 30 min: padj 0.010 but shrunken LFC 0.41, below the paper's 0.5 cutoff, so not a DEG under the paper rule although the paper calls it upregulated."], "results": {"deseq2_apeglm/grp_F1_vs_CTRL": {"n_deg": 2337, "up": 1124, "down": 1213, "rule": "padj < 0.05 and |log2FoldChange| > 0.5", "audit_n": 5019}, "deseq2_apeglm/grp_F4_vs_CTRL": {"n_deg": 2577, "up": 1327, "down": 1250, "rule": "padj < 0.05 and |log2FoldChange| > 0.5", "audit_n": 5506}, "deseq2_apeglm/grp_F10_vs_CTRL": {"n_deg": 197, "up": 137, "down": 60, "rule": "padj < 0.05 and |log2FoldCh ... [3698 more characters]

reasoning: Paper-aligned route: DESeq2 + apeglm, paper threshold, each frequency vs control.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "reference genome",
    "paper": "BWA-MEM against mm39 for QC (S5.6.p3)",
    "data": "GEO data_processing: bwa against mm10 for QC; counts from nf-core/rnaseq on GRCm39/Ensembl 110",
    "disposition": "executable_without_change"
  },
  {
    "item": "count import",
    "paper": "DESeq2 on nf-core output; import method not stated",
    "data": "Salmon estimated counts (fractional)",
    "disposition": "executable_with_declared_deviation: rounded"
  },
  {
    "item": "ChR2 transgene counts",
    "paper": "custom reference with ChR2-tdTomato-WPRE (S2.8.p1)",
    "data": "deposited matrix has Ensembl mouse genes only",
    "disposition": "ChR2 expression result not reproducible; not run"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 42272974 (PMC13247415), GSE306842 + GSE306857

Optogenetic exercise of C2C12 ChR2(H134R) myotube monolayers. There are two separate experiments, both under SuperSeries GSE306860 (S10.p1):
- GSE306842 runs daily 30-min stimulation.
- GSE306857 runs daily 60-min stimulation.

Each experiment has an unstimulated control and 1, 4 and 10 Hz arms, with n = 6 wells per arm and 24 samples in all (S2.2.p2, Fig. 2).

## What ran

- **Route:** case spec, `python -m tools.case_runner execute case_spec.json`. Both cases ran to `completed`, with `decision_status` valid and `route: paper_aligned`. The contract validator returned 0 errors on 28 records.
- **Matrix:** `<GSE>_salmon.merged.gene_counts.tsv.gz`. These are Salmon estimated counts from nf-core/rnaseq 3.11.1 (GRCm39, Ensembl 110), 56,941 genes, about 91% integer values. They were rounded to integers, and the rounding is documented. The TPM file was rejected.
- **Alignment:** the key is the title suffix after `Muscle.<n>mins.`. Keys were matched with `normalize_keys`, so `x1Hz-1` matches `X1Hz.1`. 24/24 samples matched in each case, with exact matches and no positional matching. The group variable `grp` has levels CTRL, F1, F4 and F10, with 6 samples each.
- **Design:** one model `~ grp` per experiment on all 24 samples, with planned contrasts F1/F4/F10 vs CTRL. Suitability was `analyzable`. Covariance is `not_required`: wells are independent, and no batch or pairing is recorded.
- **Primary analysis:** R DESeq2 1.51 (Wald test) with `lfcShrink(type="apeglm")`, via `tools.r_de_tools:run_r_de` with `alpha` = 0.05. This is the paper's route (S5.6.p4). `log2FoldChange` holds the shrunken LFC, and `log2FoldChange_mle` keeps the MLE.
- **Sensitivity analysis:** pydeseq2 joint model with MLE LFC (`tools.joint_contrasts:run_joint_deseq2`).
- **Threshold:** the paper's rule, padj < 0.05 and |log2FC| > 0.5 on the shrunken LFC (Fig. 2d caption, S2.3.p1). The audit rule is padj < 0.05 alone.
- **Enrichment:** GSEA prerank on Hallmark (mouse `mh.all` 2024.1), ranked by Wald stat, for all 6 contrasts. All 6 runs completed. No ORA was run, because the paper did none at the DEG threshold.
- **Not compared:** 30 vs 60 min. Duration is aliased with experiment: separate cultures, harvest on day 14 vs day 16, and 0.6 vs 1.5 mL of media (S2.2.p3, S5.6.p1). The paper does not compare DE across the two experiments either.

## DEG counts vs the paper (padj < 0.05 and |shrunken log2FC| > 0.5)

The paper gives its counts ... [4687 more characters]
