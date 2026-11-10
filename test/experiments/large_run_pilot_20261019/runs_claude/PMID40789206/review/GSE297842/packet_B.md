# Review packet B (the analysis' decisions): GSE297842

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.2.treatment", "n_values": 4, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **possible_reversed_contrast**: {"contrast": "grp_W2_vs_SED", "control": "SED", "treatment": "W2", "note": "the control side reads as exercise or the test side as control"}
- **possible_reversed_contrast**: {"contrast": "grp_W1_vs_SED", "control": "SED", "treatment": "W1", "note": "the control side reads as exercise or the test side as control"}
- **possible_reversed_contrast**: {"contrast": "grp_H24_vs_SED", "control": "SED", "treatment": "H24", "note": "the control side reads as exercise or the test side as control"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/grp_W2_vs_SED | 24 | 29 | padj <= 0.05 | 29 | 23 | 5 | 38 | 1363 | 439 | 232 | 422 | 0.097 | 0.062 |
| joint/grp_W1_vs_SED | 0 | 14 | padj <= 0.05 | 14 | 12 | 4 | 23 | 1128 | 423 | 195 | 336 | 0.108 | 0.051 |
| joint/grp_H24_vs_SED | 54 | 74 | padj <= 0.05 | 74 | 47 | 13 | 154 | 1646 | 535 | 229 | 547 | 0.098 | 0.075 |
| W2_vs_SED_pairwise | 24 | 93 | padj <= 0.05 | 93 | 53 | 8 | 170 | 1495 | 445 | 224 | 502 | 0.095 | 0.074 |

## Samples per design level

### `grp`
- **H24** (4): GSM9000791 / Ex_24h_F_Replicate1 / Library name: STC804_5_B7_24h_Re_L1_ds.d; GSM9000792 / Ex_24h_F_Replicate2 / Library name: STC804_6_B9_24h_Re_L1_ds.a; GSM9000793 / Ex_24h_F_Replicate3 / Library name: STC804_7_B10_24h_Re_L1_ds.; GSM9000794 / Ex_24h_F_Replicate4 / Library name: STC804_8_B11_24h_Re_L1_ds.
- **SED** (4): GSM9000799 / Sed_G_Replicate1 / Library name: STC804_13_B20_Control_Re_L; GSM9000800 / Sed_G_Replicate2 / Library name: STC804_14_B21_Control_Re_L; GSM9000801 / Sed_G_Replicate3 / Library name: STC804_15_B23_Control_Re_L; GSM9000802 / Sed_G_Replicate4 / Library name: STC804_16_B24_Control_Re_L
- **W1** (4): GSM9000795 / Ex_1w_F_Replicate1 / Library name: STC804_9_B13_1wk_Re_L1_ds.; GSM9000796 / Ex_1w_F_Replicate2 / Library name: STC804_10_B15_1wk_Re_L1_ds; GSM9000797 / Ex_1w_F_Replicate3 / Library name: STC804_11_B16_1wk_Re_L1_ds; GSM9000798 / Ex_1w_F_Replicate4 / Library name: STC804_12_B17_1wk_Re_L1_ds
- **W2** (4): GSM9000787 / Ex_2w_F_Replicate1 / Library name: STC804_1_B1_2wk_Re_L1_ds.7; GSM9000788 / Ex_2w_F_Replicate2 / Library name: STC804_2_B2_2wk_Re_L1_ds.3; GSM9000789 / Ex_2w_F_Replicate3 / Library name: STC804_3_B5_2wk_Re_L1_ds.e; GSM9000790 / Ex_2w_F_Replicate4 / Library name: STC804_4_B6_2wk_Re_L1_ds.0

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE297842"], "assay": "bulk poly-A RNA-seq, renal cortex, single-end NextSeq 2000 (S2.8.p1)", "organism": "Mus musculus C57BL/6J, 10-wk-old males (S2.1.p3)", "sample_inclusion": "forced treadmill experiment only: Sed, 24 h (pre/post ECT, no training), 1 wk and 2 wk training; n=4 per group (S3.4.p1, FIG6 n=4 per group). The voluntary-wheel experiment had no RNA-seq.", "factors": {"grp": ["SED", "H24", "W1", "W2"]}, "primary_estimand": "Effect of 2 wk forced treadmill training vs sedentary on renal cortex gene expression in male mice (S3.4.p1, TAB2)", "planned_contrasts": ["2 wk vs Sed (TAB1, TAB2: 24 DEGs, 17 up / 7 down)", "1 wk vs Sed (TAB1: 0 DEGs)", "24 h vs Sed (TAB1: 54 DEGs, 34 up / 20 down)"], "repeated_measure_unit": "none; independent animals per group", "normalization": "DESeq2 RLE; genes with fewer than ten counts across samples removed (S2.9.p1)", "paper_method": "DESeq2 on HTSeq raw counts of Ensembl protein-coding genes (S2.9.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": true, "source_locator": "S2.9.p1; TAB1 (p<=0.05; q<=0.05; |log2FC|>=0)"}, "paper_results": "2wk: 24 DEGs incl. Scnn1a/b/g up, Foxi1, Cyp4a14 up, Mmp13, Cd209a down; 1wk: 0; 24h: 54"}

reasoning: Methods S2.9.p1 give DESeq2 with BH-adjusted p<=0.05 and no fold-change cutoff; TAB1 lists the three comparisons vs Sed with counts; S3.4.p1 states RNA-seq was done on forced treadmill groups only.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE297842\\GSE297842_htseq_rawCounts.txt.gz", "owned": true, "checks": ["S2.9.p1 and DA.p1 name GSE297842", "GEO treatment protocol describes 1 day / 1 wk / 2 wk forced treadmill at 70% capacity for 40 min, matching S2.1.p3", "growth protocol: wild type C57BL/6J male mice", "16 GSM samples = 4 groups x 4, matching FIG6 n=4", "supplementary file is HTSeq raw counts, matching S2.9.p1"], "accession": "GSE297842", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE297842\\GSE297842_metadata.csv"}

reasoning: Series, protocol, and sample counts match the paper's treadmill RNA-seq experiment. The deposited matrix also holds 8 extra columns (STC804_17..24, D*_Run / D*_Sed) that have no GSM record in the series and are not described in the paper's RNA-seq section; they are not part of this accession's sample set and are dropped at alignment.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 16, "n_metadata": 16, "coverage": 1.0, "unmatched_matrix_columns": ["STC804_17", "STC804_18", "STC804_19", "STC804_20", "STC804_21", "STC804_22", "STC804_23", "STC804_24"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.2.treatment", "recode": {"Control": "SED", "24 h": "H24", "1 wk": "W1", "2 wk": "W2"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\aligned\\design_metadata.csv", "sha256": "bac73c91466e3fefc6201b4aa7ec0a160cc90531e7c8e54c52018bcd8200fb98", "levels": {"grp": {"W2": 4, "H24": 4, "W1": 4, "SED": 4}}}}

reasoning: Metadata description holds 'Library name: STC804_<n>_B<k>_<group>_Re_L1...'; matrix columns are 'STC804_<n>_B<k>_<group>_Re_S<n>'. Key = STC804_<n> on both sides (exact). Matrix columns STC804_17..24 (D-prefixed Run/Sed) have no GSM in the series and will be unmatched and dropped. Group from characteristics treatment, cross-checked by the group token in the library name.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\aligned\\aligned_matrix.csv", "sha256": "389f348c7ac3dae0247d42543b884291266bdb76d99bcfb6887c644ce2bf39fa", "n_features": 55414, "n_samples": 16, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2333644.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer fraction 1.0, max 2.3M, many zeros; GEO data_processing: HTSeq v0.10.0 read counts, 'raw counts for each sample'; file name htseq_rawCounts; paper S2.9.p1 uses HTSeq raw counts in DESeq2.

### design (valid, not_started)

final: {"analysis_type": "multi-group, one control", "design_column": "grp", "contrasts": [{"name": "grp_W2_vs_SED", "control": "SED", "treatment": "W2", "role": "primary"}, {"name": "grp_W1_vs_SED", "control": "SED", "treatment": "W1", "role": "secondary"}, {"name": "grp_H24_vs_SED", "control": "SED", "treatment": "H24", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: One control (Sed) with three exercise levels (TAB1). One DESeq2 model on all 16 samples with three planned contrasts vs Sed; 2 wk vs Sed is the primary estimand (TAB2, FIG6). The 24 h group is an acute bout response (S2.1.p3) rather than training.

rejected alternatives: [{"value": "pooled exercise (24h+1wk+2wk) vs Sed", "reason_rejected": "paper compares each exercise group to Sed separately (TAB1); pooling mixes acute and training estimands"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 16, "n_columns": 4, "columns": ["Intercept", "grp_SED", "grp_W1", "grp_W2"], "rank": 4, "full_rank": true, "residual_df": 12, "levels": {"grp": {"W2": 4, "H24": 4, "W1": 4, "SED": 4}}, "cells": [{"cell": ["H24"], "n": 4}, {"cell": ["SED"], "n": 4}, {"cell": ["W1"], "n": 4}, {"cell": ["W2"], "n": 4}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 16, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 16, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.genotype", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.treatment", "n_levels": 4, "status": "complete_confounding", "crosstab": {"H24": {"1 wk": 0, "2 wk": 0, "24 h": 4, "Control": 0}, "SED": {"1 wk": 0, "2  ... [1932 more characters]

reasoning: Independent animals, one sample each; no batch, sex (all male) or other covariate recorded in GEO or the paper.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald, one model ~ grp)", "formula": "~ grp", "paper_route": {"method": "DESeq2 on protein-coding genes, genes with < 10 counts across samples removed", "status": "reproduced_with_deviations"}, "deviations": ["No restriction to protein-coding genes: the deposited matrix has Ensembl gene IDs without biotype, so all genes passing the count filter are tested (this changes the BH denominator slightly).", "Low-count filter implemented as mean raw count >= 0.625 over the 16 samples, i.e. total count >= 10 across samples (S2.9.p1).", "pydeseq2 rather than R DESeq2; whether the paper fitted one 4-group model or pairwise models is not stated. A pairwise 2wk-vs-Sed DESeq2 run is added as a sensitivity analysis."]}

reasoning: Raw HTSeq counts support the paper's DESeq2 route directly.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": true}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": true}}

reasoning: S2.9.p1: BH-adjusted p<=0.05; TAB1 header 'p<=0.05; q<=0.05; |log2FC|>=0' (no fold-change cutoff; q<=0.05 implies p<=0.05).

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\joint\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\joint\\DEG_results_grp_W2_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\joint\\DEG_results_grp_W1_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\joint\\DEG_results_grp_H24_vs_SED.csv"], "counts": {"joint/grp_W2_vs_SED": {"applied": {"rule": "padj <= 0.05", "n_tested": 20208, "n_significant": 29, "n_up": 19, "n_down": 10, "deg_sanity": "ok"}}, "joint/grp_W1_vs_SED": {"applied": {"rule": "padj <= 0.05", "n_tested": 16813, "n_significant": 14, "n_up": 6, "n_down": 8, "deg_sanity": "ok"}}, "joint/grp_H24_vs_SED": {"applied": {"rule": "padj <= 0.05", "n_tested": 15966, "n_significant": 74, "n_up": 44, "n_down": 30, "deg_sanity": "ok"}}}}

reasoning: One DESeq2 model on all 16 samples, three planned contrasts vs Sed (TAB1); filter total count >= 10 across samples (S2.9.p1).

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "W2_vs_SED_pairwise", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\W2_vs_SED_pairwise\\input\\matrix_filtered.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\W2_vs_SED_pairwise\\DEG_results_W2_vs_SED.csv"], "counts": {"W2_vs_SED_pairwise": {"applied": {"rule": "padj <= 0.05", "n_tested": 13950, "n_significant": 93, "n_up": 49, "n_down": 44, "deg_sanity": "ok"}}}}

reasoning: Pairwise 2wk vs Sed fit on 8 samples (total count >= 10 over those 8), in case the paper fitted each comparison separately.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_W2_vs_SED", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": true}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\enrichment_joint_grp_W2_vs_SED\\ora\\DEG_results_grp_W2_vs_SED_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\enrichment_joint_grp_W2_vs_SED\\ora\\DEG_results_grp_W2_vs_SED_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\enrichment_joint_grp_W2_vs_SED\\ora\\DEG_results_grp_W2_vs_SED_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\enrichment_joint_grp_W2_vs_SED\\ora\\DEG_results_grp_W2_vs_SED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 29 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Inorganic Cation Import Across Plasma Membrane (GO:0098659) | padj=2.41e-06 | overlap=6/103 | genes=SCNN1G;SCNN1A;TRPV5;ATP2B4;CLU ... [1210 more characters]

reasoning: Paper ran clusterProfiler GO/KEGG on the 2 wk DEGs (S2.9.p1, FIG6A).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_W2_vs_SED", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\enrichment_joint_grp_W2_vs_SED\\gsea\\DEG_results_grp_W2_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 21742 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 39 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=2.11 | NOM p=0.00e+00 | FDR q=1.05e-03 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=2.07 | NOM p=0.00e+00 | FDR q=5.27e-04 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.74 | NOM p=0.00e+00 | FDR q=5.27e-03 - HALLMARK_HEME_METABOLISM | NES=1.71 | NOM p=0.00e+00 | FDR q=6.33e-03 - HALLMARK_MYC_TARGETS_V2 | NES=1.69 | NOM p=5.22e-03 | FDR q=6.96e-03 - HALLMARK_PEROXISOME | NES=1.68 | NOM p=1.69e-03 | FDR q=6.33e-03 - HALLMARK_MYOGENESIS | NES=1.62 | NOM p=1.66e-03 | FDR q=1.10e-02 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.54 | NOM p=3.23e-03 | FDR q=2.50e-02 - HALLMARK_ANDROGEN_RESPONSE | NES=1.53 | NOM p=8.59e-03 | FDR q=2.42e-02 - HALLMARK_KRAS_SIGNALING_DN | NES=1.50 | NOM p=6.43e-03 | FDR q=3.14e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=-2.62 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=-2.02 | NOM p=0.00e+00 | FDR q=0.00 ... [397 more characters]

reasoning: Paper ran clusterProfiler GO/KEGG on the 2 wk DEGs (S2.9.p1, FIG6A).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_H24_vs_SED", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": true}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\enrichment_joint_grp_H24_vs_SED\\ora\\DEG_results_grp_H24_vs_SED_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\enrichment_joint_grp_H24_vs_SED\\ora\\DEG_results_grp_H24_vs_SED_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\enrichment_joint_grp_H24_vs_SED\\ora\\DEG_results_grp_H24_vs_SED_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\enrichment_joint_grp_H24_vs_SED\\ora\\DEG_results_grp_H24_vs_SED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 73 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Response To Bile Acid (GO:1903412) | padj=4.98e-02 | overlap=2/5 | genes=CYP27B1;ALAS1 - tRNA Aminoacylation For Protein  ... [1219 more characters]

reasoning: Paper reports stress-response GO pathways for the 24 h DEGs (Supp Fig 7A).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_H24_vs_SED", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40789206\\GSE297842\\results\\enrichment_joint_grp_H24_vs_SED\\gsea\\DEG_results_grp_H24_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 21742 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 29 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=2.39 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UV_RESPONSE_UP | NES=2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=2.11 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=2.08 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.99 | NOM p=0.00e+00 | FDR q=2.09e-04 - HALLMARK_P53_PATHWAY | NES=1.98 | NOM p=0.00e+00 | FDR q=1.79e-04 - HALLMARK_GLYCOLYSIS | NES=1.88 | NOM p=0.00e+00 | FDR q=7.83e-04 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.87 | NOM p=0.00e+00 | FDR q=6.96e-04 - HALLMARK_MYC_TARGETS_V1 | NES=1.84 | NOM p=0.00e+00 | FDR q=8.77e-04 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_PROTEIN_SECRETION | NES=-1.25 | NOM p=7.35e-02 | FDR q=1.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=-1.22 | NOM p=5.60e-02 | FDR q=6. ... [400 more characters]

reasoning: Paper reports stress-response GO pathways for the 24 h DEGs (Supp Fig 7A).

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["All genes tested, not only protein-coding (no biotype in deposited matrix).", "n=4 per group."], "results": {"joint/grp_W2_vs_SED": {"n_deg": 29, "up": 19, "down": 10, "rule": "padj <= 0.05"}, "joint/grp_W1_vs_SED": {"n_deg": 14, "up": 6, "down": 8, "rule": "padj <= 0.05"}, "joint/grp_H24_vs_SED": {"n_deg": 74, "up": 44, "down": 30, "rule": "padj <= 0.05"}, "W2_vs_SED_pairwise": {"n_deg": 93, "up": 49, "down": 44, "rule": "padj <= 0.05"}}, "paper_counts": {"joint/grp_W2_vs_SED": 24, "joint/grp_W1_vs_SED": 0, "joint/grp_H24_vs_SED": 54, "W2_vs_SED_pairwise": 24}, "comparison": {"joint/grp_W2_vs_SED": {"ours": 29, "paper": 24}, "joint/grp_W1_vs_SED": {"ours": 14, "paper": 0}, "joint/grp_H24_vs_SED": {"ours": 74, "paper": 54}, "W2_vs_SED_pairwise": {"ours": 93, "paper": 24}}, "paper_gene_check": {"joint/grp_W2_vs_SED": {"Scnn1a": {"baseMean": 5594.1304, "log2FoldChange": 0.5323, "padj": 0.0257, "pvalue": 0.0}, "Scnn1b": {"baseMean": 2000.7276, "log2FoldChange": 0.5454, "padj": 0.1027, "pvalue": 0.0003}, "Scnn1g": {"baseMean": 1812.6569, "log2FoldChange": 0.5714, "padj": 0.0089, "pvalue": 0.0}, "Foxi1": {"baseMean": 1194.409, "log2FoldChange": 0.8169, "padj": 0.0001, "pvalue": 0.0}, "Cyp4a14": {"baseMean": 6029.8457, "log2FoldChange": 3.0257, "padj": 0.0369, "pvalue": 0.0}, "Phactr1": {"baseMean": 434.7209, "log2FoldChange": 0.8307, "padj": 0.0018, "pvalue": 0.0}, "Scd2": {"baseMean": 3552.5407, "log2FoldChange": 0.6152, "padj": 0.0002, "pv ... [1889 more characters]

reasoning: Paper-aligned DESeq2 route with the paper's threshold; deviations limited to gene universe and implementation.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "extra matrix columns",
    "paper": "RNA-seq on 4 treadmill groups, n=4 (S3.4.p1, FIG6)",
    "data": "matrix has 24 columns; 8 (STC804_17..24, D*_Run/D*_Sed) have no GSM record in GSE297842",
    "disposition": "executable_without_change"
  },
  {
    "item": "gene universe",
    "paper": "ENSEMBL protein-coding transcripts (S2.9.p1)",
    "data": "55,414 Ensembl gene IDs, no biotype column",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID40789206 / GSE297842

Status: **finished** (case `completed`, decision `valid`, route `paper_aligned`; validator 15 records, 0 errors).

## What ran
- Case spec route (`case_spec.json`, `python -m tools.case_runner execute`).
- Data: `GSE297842_htseq_rawCounts.txt.gz` (HTSeq raw counts, 55,414 Ensembl genes x 24 columns). Male C57BL/6J renal cortex, forced treadmill: Sed / 24 h / 1 wk / 2 wk, n=4 each (16 GSMs).
- Alignment: exact on the `STC804_<n>` key, taken from the metadata `description` ("Library name: ...") and the matrix column names; 16/16 aligned. The matrix's 8 extra columns (STC804_17..24, `D*_Run` / `D*_Sed`) have no GSM in the series and are not part of the paper's RNA-seq groups, so they were dropped.
- Primary: one pydeseq2 model `~ grp` on all 16 samples, with three planned contrasts vs Sed. Low-count filter: total count >= 10 across samples (mean >= 0.625; 21,923 genes kept; S2.9.p1).
- Sensitivity: a pairwise 2 wk vs Sed DESeq2 fit on 8 samples (total >= 10 over those 8).
- Enrichment: ORA (Enrichr GO/KEGG) and GSEA (Hallmark) on joint 2 wk and 24 h tables; both completed.

## Threshold
Paper threshold, applied unchanged: BH padj <= 0.05 with no fold-change cutoff (S2.9.p1; TAB1 "p<=0.05; q<=0.05; |log2FC|>=0").

## DEG counts vs paper (padj <= 0.05)
| Comparison | Ours (up/down) | Paper (up/down) |
|---|---|---|
| 2 wk vs Sed (joint, primary) | 29 (19/10) | 24 (17/7) |
| 1 wk vs Sed (joint) | 14 (6/8) | 0 |
| 24 h vs Sed (joint) | 74 (44/30) | 54 (34/20) |
| 2 wk vs Sed (pairwise sensitivity) | 93 (49/44) | 24 |

- 2 wk joint: 18 of the paper's 24 Table 2 genes are significant, including Scnn1a, Scnn1g, Foxi1, Cyp4a14, Mmp13, Cd209a, Hsd11b1 and Aplnr. Scnn1b (padj 0.10), Hsd11b2 (0.09), Cyp2d12, Lipo2, Plekhd1 and Ptges are not. All 24 paper genes change in the paper's direction. In the pairwise fit, 20 of 24 are significant, Scnn1b included.
- The joint model is much closer to the paper's count than the pairwise fit (29 vs 93), which suggests the paper fitted one 4-group model.
- 24 h: Lcn2 and Havcr1 are not significant (padj 0.45 and 0.34). This matches the paper's "non-significant increase".
- 1 wk: we find 14 DEGs where the paper found none. This is a real discrepancy, recorded here and not resolved.
- Effect sizes: our log2FC for the strongly changed genes are larger than the paper's (Cyp4a14 3.02 vs 0.93; Mmp13 -1.71 vs -0.99). pydeseq2's apeglm-type shrunk LFC is still about 2.7 for Cyp4a14, so the paper's LFC s ... [1459 more characters]
