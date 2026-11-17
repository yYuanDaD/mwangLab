# Review packet B (the analysis' decisions): GSE77178

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| limma_joint/grp_OEx_vs_OSed | 248 | 1064 | padj < 0.1 | 652 | 68 | 10 | 1064 | 1694 | 89 | 14 | 863 | 0.056 | 0.261 |
| limma_joint/grp_YEx_vs_YSed | 35 | 442 | padj < 0.1 | 146 | 44 | 8 | 442 | 1217 | 83 | 14 | 520 | 0.065 | 0.188 |

## Samples per design level

### `grp`
- **OEx** (5): GSM2045582 / O(+Ex) replicate 1; GSM2045583 / O(+Ex) replicate 2; GSM2045584 / O(+Ex) replicate 3; GSM2045585 / O(+Ex) replicate 4; GSM2045586 / O(+Ex) replicate 5
- **OSed** (7): GSM2045575 / O(-Ex) replicate 1; GSM2045576 / O(-Ex) replicate 2; GSM2045577 / O(-Ex) replicate 3; GSM2045578 / O(-Ex) replicate 4; GSM2045579 / O(-Ex) replicate 5; GSM2045580 / O(-Ex) replicate 6; GSM2045581 / O(-Ex) replicate 7
- **YEx** (3): GSM2045593 / Y(+Ex) replicate 1; GSM2045594 / Y(+Ex) replicate 2; GSM2045595 / Y(+Ex) replicate 3
- **YSed** (6): GSM2045587 / Y(-Ex) replicate 1; GSM2045588 / Y(-Ex) replicate 2; GSM2045589 / Y(-Ex) replicate 3; GSM2045590 / Y(-Ex) replicate 4; GSM2045591 / Y(-Ex) replicate 5; GSM2045592 / Y(-Ex) replicate 6

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE77178"], "assay": "bulk RNA-seq (SMARTer Ultra Low Input, HiSeq 2000) of FACS-isolated quiescent MuSCs, one mouse per profile (S1.19.p1, FIG11 a)", "organism": "Mouse, male C57BL/6", "factors": {"age": ["young 3 mo", "old 18 mo"], "activity": ["-Ex (locked wheel)", "+Ex (3 weeks voluntary wheel running)"], "ccnd1": ["WT", "HET", "KO (separate young Ccnd1 genotype experiment, S0.p15)"]}, "sample_inclusion": "Exercise experiment: Y(-Ex), Y(+Ex), O(-Ex), O(+Ex) quiescent MuSCs (S0.p7, FIG11). The Ccnd1 genotype series (Y(WT)/Y(HET)/Y(KO)/O(WT), S0.p15) is a separate experiment and not an exercise estimand.", "primary_estimand": "Effect of voluntary wheel running on the quiescent MuSC transcriptome in old mice: O(+Ex) vs O(-Ex) (S0.p7, S0.p9, FIG11 c)", "planned_contrasts": ["O(+Ex) vs O(-Ex) (S0.p7; paper: 248 DEGs at 10% FDR; Ccnd1 top hit, up with exercise, S0.p9)", "Y(+Ex) vs Y(-Ex) (S0.p7; paper: 35 DEGs at 10% FDR)", "O(-Ex) vs Y(-Ex) aging reference used to call 130 of the 248 genes 'rejuvenated' (S0.p7; count not reported)"], "repeated_measure_unit": "none; each profile is an individual mouse (FIG11 a)", "normalization": "genes lacking Entrez ID or raw FPKM >= 1.5 in >= 3 samples removed (11,337 genes); raw counts normalized with RUVs k=6 for library prep and sample collection batch (S1.19.p3)", "paper_method": "edgeR negative binomial GLM likelihood ratio test, Cox-Reid tagwise dispersion, on RUVs-normalized raw counts, genes with normalized FPKM >= 6 ... [421 more characters]

reasoning: S0.p7 defines the exercise comparisons and the 10% FDR counts; S1.19.p3 defines filtering, RUVs normalization, edgeR LRT and BH q-values; S0.p9 and FIG11 c name Ccnd1 as the top O(+Ex) vs O(-Ex) hit.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\input\\matrix_feature_ids.csv", "owned": true, "checks": ["GEO series GSE77178 contact lab Thomas A. Rando (paper's lab), MuSC RNA-seq, mouse male, titles O(-Ex)/O(+Ex)/Y(-Ex)/Y(+Ex) and Y(WT)/Y(HET)/Y(KO)/O(WT) match the paper's groups (S0.p7, S0.p15)", "the deposited file holds 11,337 genes, the exact number the paper states after filtering (S1.19.p3)", "metadata 36 samples = 36 matrix sample columns"], "accession": "GSE77178", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE77178\\GSE77178_metadata.csv"}

reasoning: The supplementary file is the paper's processed table (11,337 genes, normalized FPKM plus Ccnd1 correlation coefficients described in S1.19.p4); group labels and the 2016/2018 submission split match the exercise and Ccnd1 experiments.

### alignment (valid, not_started)

final: {"key": "title 'O(-Ex) replicate 1' -> 'O(-Ex)_1', equal to the matrix column names", "kept": "21 exercise-experiment samples", "method": "exact:key", "n_aligned": 36, "n_metadata": 36, "coverage": 1.0, "unmatched_matrix_columns": ["Mouse_EntrezID", "Ccnd1_Correlation_Coefficient"], "unmatched_metadata_samples": [], "excluded_samples": {"GSM3197069": "Ccnd1 genotype experiment (Y(WT), 2018 submission batch), not part of the exercise estimand (S0.p15)", "GSM3197070": "Ccnd1 genotype experiment (Y(WT), 2018 batch)", "GSM3197071": "Ccnd1 genotype experiment (Y(WT), 2018 batch)", "GSM3197072": "Ccnd1 genotype experiment (Y(HET), 2018 batch)", "GSM3197073": "Ccnd1 genotype experiment (Y(HET), 2018 batch)", "GSM3197074": "Ccnd1 genotype experiment (Y(HET), 2018 batch)", "GSM3197075": "Ccnd1 genotype experiment (Y(HET), 2018 batch)", "GSM3197076": "Ccnd1 genotype experiment (Y(KO), 2018 batch)", "GSM3197077": "Ccnd1 genotype experiment (Y(KO), 2018 batch)", "GSM3197078": "Ccnd1 genotype experiment (Y(KO), 2018 batch)", "GSM3197079": "Ccnd1 genotype experiment (Y(KO), 2018 batch)", "GSM3197080": "Ccnd1 genotype experiment (Y(KO), 2018 batch)", "GSM3197081": "Ccnd1 genotype experiment (O(WT), 2018 batch)", "GSM3197082": "Ccnd1 genotype experiment (O(WT), 2018 batch)", "GSM3197083": "Ccnd1 genotype experiment (O(WT), 2018 batch)"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\aligned\\aligned_metadata_kept.csv", "colum ... [421 more characters]

reasoning: Matrix columns are 'O(-Ex)_1' style; GEO titles are 'O(-Ex) replicate 1'. Deriving a key from title gives an exact match for all 36 samples. The 15 Ccnd1-genotype samples (submitted 2018, separate experiment S0.p15) are excluded so the exercise contrasts do not borrow variance from another batch; grp is the age x activity cell from the title.

### matrix (valid, not_started)

final: {"source": "GSE77178_ExerciseAgingCcnd1_MuSCRNASeq.txt.gz: 'Tab-delimited .txt file containing normalized FPKMs and Ccnd1 correlation coefficients for each gene' (GEO data_processing)", "paper_input": "edgeR on RUVs-normalized raw counts (S1.19.p3); raw counts are not deposited (supplementary_file NONE per sample)", "matrix_type": "normalized FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\aligned\\aligned_matrix.csv", "sha256": "a2083b980836e999d371e77b0ba4977059c27352aa4f17708c8df551f2fb7323", "n_features": 11332, "n_samples": 21, "annotation_columns_dropped": ["GSM3197069", "GSM3197070", "GSM3197071", "GSM3197072", "GSM3197073", "GSM3197074", "GSM3197075", "GSM3197076", "GSM3197077", "GSM3197078", "GSM3197079", "GSM3197080", "GSM3197081", "GSM3197082", "GSM3197083"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.00166076, "max": 9741.567347, "median": 6.039936715, "integer_fraction": 0.0, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Values are non-integer (integer fraction 0), positive, median ~5.8, max ~10,500, consistent with FPKM; GEO data_processing says normalized FPKMs after RUVs k=6. Not counts, so edgeR/DESeq2 cannot run; log2(x+1) limma is the supported route.

### design (valid, not_started)

final: {"analysis_type": "multi-group", "design_column": "grp", "contrasts": [{"name": "grp_OEx_vs_OSed", "control": "OSed", "treatment": "OEx", "role": "primary"}, {"name": "grp_YEx_vs_YSed", "control": "YSed", "treatment": "YEx", "role": "secondary"}, {"name": "grp_OSed_vs_YSed", "control": "YSed", "treatment": "OSed", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\suitability\\suitability.md", "n_comparisons": 8, "n_analyzable": 8}}

reasoning: Four age x activity cells from one experiment (S0.p7, FIG11 a); the paper compares O(+Ex) vs O(-Ex), Y(+Ex) vs Y(-Ex), and O(-Ex) vs Y(-Ex) pairwise. One cell-means model on the 21 samples with planned contrasts, no pooling of levels. ccnd1 column is constant WT in these samples; activity alone would pool ages and is rejected.

rejected alternatives: [{"value": "characteristics_ch1.3.activity alone (Exercise vs No Exercise)", "reason_rejected": "pools young and old, while the paper's estimand is exercise within age"}, {"value": "include the 2018 Ccnd1 samples as extra controls", "reason_rejected": "separate experiment and submission batch; paper analyzes them separately (S0.p15)"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "RUVs factors (k=6)", "disposition": "not available as columns; already removed in the deposited normalized FPKM, cannot be re-entered in the model"}], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 21, "n_columns": 4, "columns": ["Intercept", "grp_OSed", "grp_YEx", "grp_YSed"], "rank": 4, "full_rank": true, "residual_df": 17, "levels": {"grp": {"OSed": 7, "YSed": 6, "OEx": 5, "YEx": 3}}, "cells": [{"cell": ["OEx"], "n": 5}, {"cell": ["OSed"], "n": 7}, {"cell": ["YEx"], "n": 3}, {"cell": ["YSed"], "n": 6}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 21, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 21, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.gender", "n_levels": 1, "status": "constant"}, {"column": "charac ... [2255 more characters]

reasoning: Each profile is a separate mouse (FIG11 a), so no blocking unit. The paper's batch adjustment (RUVs, S1.19.p3) is already applied to the deposited values; its W factors are not deposited, so the residual degrees of freedom are not reduced for them (possible mild anti-conservatism). No batch column in GEO metadata for these 21 samples.

### method (valid, not_started)

final: {"matrix_type": "normalized FPKM", "method": "limma (moderated t, empirical Bayes) on log2(FPKM+1)", "formula": "~ 0 + grp", "paper_route": {"method": "edgeR NB GLM LRT with Cox-Reid tagwise dispersion on RUVs-normalized raw counts", "status": "blocked", "reason": "raw counts and RUVs W factors are not deposited; only RUVs-normalized FPKM is available"}, "deviations": ["limma-trend style moderated t on log2(normalized FPKM+1) instead of edgeR LRT on counts", "expression filter normalized FPKM >= 6 in >= 3 of the 21 exercise samples (paper: >= 3 samples, set unclear)", "5 duplicated gene symbols (same Entrez, different Ensembl locus) kept first occurrence"], "transform": "log2(x+1)"}

reasoning: Matrix policy: FPKM goes to limma on log scale. The paper's edgeR route needs counts that are not deposited, so it is a declared deviation.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Paper's 10% BH FDR applied to limma BH-adjusted p; audit rule is the workflow default BH < 0.05."}

reasoning: S0.p7: 'At a 10% false discovery rate'; S1.19.p3: Benjamini-Hochberg q-values; no fold-change cutoff stated.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "limma_joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 21, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\results\\limma_joint\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\results\\limma_joint\\DEG_results_grp_OEx_vs_OSed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\results\\limma_joint\\DEG_results_grp_YEx_vs_YSed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\results\\limma_joint\\DEG_results_grp_OSed_vs_YSed.csv"], "counts": {"limma_joint/grp_OEx_vs_OSed": {"applied": {"rule": "padj < 0.1", "n_tested": 6481, "n_significant": 1064, "n_up": 526, "n_down": 538, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 6481, "n_significant": 652, "n_up": 328, "n_down": 324, "deg_sanity": "ok"}}, "limma_joint/grp_YEx_vs_YSed": {"applied": {"rule": "padj < 0.1", "n_tested": 6481, "n_significant": 442, "n_up": 146, "n_down": 296, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 6481, "n_significant": 146, "n_up": 53, "n_down": 93, "deg_sanity": "ok"}}, "limma_joint/grp_OSed_vs_YSed": {"applied": {"rule": "padj < 0.1", "n_tested": 6481, "n_significant": 3521, "n_up": 2021, "n_down": 1500, "deg_sanity": "implausible_sig_ ... [153 more characters]

reasoning: One limma cell-means model on the 21 exercise-experiment samples with the paper's three pairwise contrasts; paper's FPKM >= 6 in >= 3 samples expression filter.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_joint/grp_OEx_vs_OSed", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\results\\enrichment_limma_joint_grp_OEx_vs_OSed\\gsea\\DEG_results_grp_OEx_vs_OSed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 6481 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 17 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.00 | NOM p=0.00e+00 | FDR q=3.21e-03 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.54 | NOM p=0.00e+00 | FDR q=1.00e-01 - HALLMARK_ADIPOGENESIS | NES=1.42 | NOM p=1.41e-02 | FDR q=1.96e-01 - HALLMARK_MYOGENESIS | NES=1.36 | NOM p=3.80e-02 | FDR q=2.26e-01 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.34 | NOM p=4.35e-02 | FDR q=2.22e-01 - HALLMARK_PEROXISOME | NES=1.25 | NOM p=1.29e-01 | FDR q=3.47e-01 - HALLMARK_PROTEIN_SECRETION | NES=1.09 | NOM p=2.82e-01 | FDR q=7.84e-01 - HALLMARK_ANGIOGENESIS | NES=1.09 | NOM p=3.48e-01 | FDR q=7.03e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=1.02 | NOM p=4.26e-01 | FDR q=8.61e-01 - HALLMARK_APOPTOSIS | NES=1.01 | NOM p=4.44e-01 | FDR q=8.07e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-2.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=-1.66 | NOM p=0.00e+00  ... [413 more characters]

reasoning: Paper ran Hallmark GSEA for O(+Ex) vs O(-Ex) (S0.p8, FIG5 b).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_joint/grp_YEx_vs_YSed", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\results\\enrichment_limma_joint_grp_YEx_vs_YSed\\gsea\\DEG_results_grp_YEx_vs_YSed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 6481 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 24 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_MYOGENESIS | NES=1.84 | NOM p=0.00e+00 | FDR q=9.28e-03 - HALLMARK_APOPTOSIS | NES=1.35 | NOM p=3.28e-02 | FDR q=3.75e-01 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.30 | NOM p=2.36e-02 | FDR q=3.33e-01 - HALLMARK_P53_PATHWAY | NES=1.28 | NOM p=2.87e-02 | FDR q=2.96e-01 - HALLMARK_ADIPOGENESIS | NES=1.26 | NOM p=4.42e-02 | FDR q=2.63e-01 - HALLMARK_PEROXISOME | NES=1.21 | NOM p=1.42e-01 | FDR q=3.15e-01 - HALLMARK_KRAS_SIGNALING_UP | NES=1.18 | NOM p=1.71e-01 | FDR q=3.43e-01 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.13 | NOM p=1.66e-01 | FDR q=4.17e-01 - HALLMARK_HYPOXIA | NES=1.12 | NOM p=2.02e-01 | FDR q=3.78e-01 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.06 | NOM p=3.22e-01 | FDR q=4.91e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-2.09 | NOM p=0.00e+00 | FDR q=9.39e-04 - HALLMARK_MYC_TARGETS_V2 | NES=-1.81 | NOM p=2.90e-03 | FDR q=7.04e-03 - HALLMARK_G2 ... [413 more characters]

reasoning: Paper ran Hallmark GSEA for Y(+Ex) vs Y(-Ex) (FIG5 b).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_joint/grp_OSed_vs_YSed", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32601609\\GSE77178\\results\\enrichment_limma_joint_grp_OSed_vs_YSed\\gsea\\DEG_results_grp_OSed_vs_YSed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 6481 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 19 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_MYC_TARGETS_V2 | NES=2.46 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=2.40 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.98 | NOM p=0.00e+00 | FDR q=6.58e-04 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.72 | NOM p=0.00e+00 | FDR q=6.74e-03 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.70 | NOM p=0.00e+00 | FDR q=6.58e-03 - HALLMARK_DNA_REPAIR | NES=1.68 | NOM p=0.00e+00 | FDR q=6.58e-03 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.48 | NOM p=1.35e-02 | FDR q=5.03e-02 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.41 | NOM p=2.07e-02 | FDR q=8.72e-02 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.38 | NOM p=8.32e-02 | FDR q=1.02e-01 - HALLMARK_E2F_TARGETS | NES=1.28 | NOM p=7.95e-02 | FDR q=1.99e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYOGENESIS | NES=-2.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=-1.95 | NOM p ... [416 more characters]

reasoning: Paper ran Hallmark GSEA for O(-Ex) vs Y(-Ex) (S0.p8, FIG5 b).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["limma on deposited RUVs-normalized FPKM instead of edgeR LRT on counts; the RUVs k=6 factors are not in the model, so residual df are overstated by 6 and DEG counts are inflated (1064 vs paper 248; 442 vs paper 35 at 10% FDR)", "Y(+Ex) has n=3", "Ccnd1 is the top O(+Ex) vs O(-Ex) hit (up, log2FC 1.14) and is lower in O(-Ex) than Y(-Ex) (log2FC -0.49), matching S0.p9", "GSEA direction contradicts the paper for cell cycle: paper says exercise restores (raises) E2F/cell-cycle sets in old MuSCs and aging lowers them (S0.p8, FIG11 b); our limma-t preranked GSEA gives O(+Ex) vs O(-Ex) E2F NES -0.96 (ns) and G2M NES -1.61 (q 0.04), and O(-Ex) vs Y(-Ex) E2F NES +1.28 (ns), G2M +0.97 (ns)", "Paper says IFN alpha/gamma not suppressed by exercise in old MuSCs; ours shows IFN gamma NES -1.52 (q 0.075), borderline suppression", "Agreeing GSEA directions: O(+Ex) vs O(-Ex) TNFA/NF-kB, IL6, TGF-beta, IL2 down and myogenesis, angiogenesis up; O(-Ex) vs Y(-Ex) IFN alpha/gamma, inflammatory, ROS up, myogenesis and Notch down. Hedgehog was not tested (size filter after expression filter). Paper ranked by Signal2Noise with gene permutation; ours by limma t (preranked)"], "results": {"limma_joint/grp_OEx_vs_OSed": {"n_deg": 1064, "up": 526, "down": 538, "rule": "padj < 0.1", "audit_n": 652}, "limma_joint/grp_YEx_vs_YSed": {"n_deg": 442, "up": 146, "down": 296, "rule": "padj < 0.1", "audit_n": 146}, "limma_joint/grp_OSed_vs_YSed": {"n_deg": 3521, "up": 2 ... [561 more characters]

reasoning: Paper's counts at 10% FDR (S0.p7) and its named top hit Ccnd1 (S0.p9: decreased with aging, restored by exercise).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 21 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method and input",
    "paper": "edgeR NB GLM LRT on RUVs-normalized raw counts (S1.19.p3)",
    "data": "only RUVs-normalized FPKM deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "sample set",
    "paper": "exercise experiment analyzed separately from Ccnd1 genotype series",
    "data": "one file holds both (36 samples)",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID32601609 / GSE77178

STATUS: finished (route `declared_deviation`, decision `valid`, execution `completed`, validator 13 records / 0 errors)

## What ran
- Case spec route: `python -m tools.case_runner inspect GSE77178`, then `execute case_spec.json`. I ran it twice; the second run only added study caveats. The first attempt is in `_previous/20261117T162509Z`.
- Paper: PMC7323974. Exercise experiment: quiescent MuSCs from Y(-Ex)/Y(+Ex)/O(-Ex)/O(+Ex) mice (S0.p7, FIG11). Method in the paper: RUVs k=6 normalization, then edgeR NB GLM LRT on genes with normalized FPKM >= 6 in >= 3 samples, BH q-values (S1.19.p3). Threshold: 10% FDR with no fold-change cutoff (S0.p7).
- Ownership: the GEO file is the paper's processed table. It has exactly 11,337 genes, matching S1.19.p3, and comes from the Rando lab.
- Alignment: I derived a key from the GEO title (`O(-Ex) replicate 1` -> `O(-Ex)_1`), giving an exact match for 36/36 samples. I excluded the 15 samples from the Ccnd1 genotype series (2018 submission, a separate experiment in S0.p15). The kept samples form grp = OSed 7, OEx 5, YSed 6, YEx 3.
- Matrix: RUVs-normalized FPKM (GEO data_processing). No raw counts were deposited.
- Model: one limma cell-means model `~ 0 + grp` on log2(FPKM+1), fitted on 21 samples. Expression filter: FPKM >= 6 in >= 3 samples, which kept 6,481 of 11,332 genes. Hallmark preranked GSEA ranked by limma t for all three contrasts.

## DEG counts vs paper (paper threshold: BH FDR < 0.10, no FC cutoff)
| Contrast | Ours (padj<0.10) | up/down | audit padj<0.05 | Paper |
|---|---|---|---|---|
| O(+Ex) vs O(-Ex) (primary) | 1064 | 526/538 | 652 | 248 |
| Y(+Ex) vs Y(-Ex) | 442 | 146/296 | 146 | 35 |
| O(-Ex) vs Y(-Ex) (aging reference) | 3521 | 2021/1500 | 2997 | not reported (130 of the 248 called "rejuvenated") |

- Named gene: Ccnd1 is rank 1 in O(+Ex) vs O(-Ex) (log2FC +1.14, padj 3.4e-5), as in the paper (S0.p9, FIG11 c). It is lower in O(-Ex) than in Y(-Ex) (log2FC -0.49, padj 0.0016), matching "decreased during aging and restored by exercise".
- GSEA, where it agrees with the paper:
  - Exercise in old MuSCs lowers TNFA/NF-kB (NES -2.28), IL6, TGF-beta and IL2, and raises myogenesis and angiogenesis (the last two not significant).
  - Aging raises IFN alpha/gamma, inflammatory response and ROS, and lowers myogenesis (NES -2.20) and Notch.
- GSEA, where it contradicts the paper (recorded in study caveats):
  - Cell-cycle sets. In O(+Ex) vs O(-Ex), E2F has NES -0.96 (not si ... [1867 more characters]
