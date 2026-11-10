# Review packet B (the analysis' decisions): GSE198266

## Mechanical flags

- **unused_subject_like_column**: {"column": "source_name_ch1", "n_values": 8, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "mouse", "n_values": 12, "max_repeat": 2, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "grp (without tissue) + suffix of title", "across": "tissue", "pairs_or_sets": 12, "samples_linked": 24, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tissue_SOL/grp_YE_vs_YC_tissue-SOL | 31 | 68 | pvalue < 0.05 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 36 | 1706 | 68 | 9 | 531 | 0.122 | 0.093 |
| tissue_SOL/grp_OE_vs_OC_tissue-SOL | 20 | 29 | pvalue < 0.05 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 1137 | 29 | 4 | 270 | 0.125 | 0.062 |
| tissue_GAS/grp_YE_vs_YC_tissue-GAS | 13 | 40 | pvalue < 0.05 and |log2FoldChange| > 0.584963 | 2 | 1 | 1 | 2 | 743 | 40 | 8 | 167 | 0.139 | 0.042 |
| tissue_GAS/grp_OE_vs_OC_tissue-GAS | 13 | 31 | pvalue < 0.05 and |log2FoldChange| > 0.584963 | 2 | 2 | 1 | 3 | 830 | 31 | 10 | 172 | 0.119 | 0.047 |

## Samples per design level

### `grp`
- **OC** (6): GSM5942482 / soleus of old control 3 / N_SOL_OC-3; GSM5942483 / soleus of old control 4 / N_SOL_OC-4; GSM5942484 / soleus of old control 5 / N_SOL_OC-5; GSM5942494 / gastrocnemius of old control 3 / N_GAS_OC-3; GSM5942495 / gastrocnemius of old control 4 / N_GAS_OC-4; GSM5942496 / gastrocnemius of old control 5 / N_GAS_OC-5
- **OE** (6): GSM5942485 / soleus of old exercise 1 / N_SOL_OE-1; GSM5942486 / soleus of old exercise 2 / N_SOL_OE-2; GSM5942487 / soleus of old exercise 3 / N_SOL_OE-3; GSM5942497 / gastrocnemius of old exercise 1 / N_GAS_OE-1; GSM5942498 / gastrocnemius of old exercise 2 / N_GAS_OE-2; GSM5942499 / gastrocnemius of old exercise 3 / N_GAS_OE-3
- **YC** (6): GSM5942476 / soleus of young control 1 / N_SOL_YC-1; GSM5942477 / soleus of young control 2 / N_SOL_YC-2; GSM5942478 / soleus of young control 3 / N_SOL_YC-3; GSM5942488 / gastrocnemius of young control 1 / N_GAS_YC-1; GSM5942489 / gastrocnemius of young control 2 / N_GAS_YC-2; GSM5942490 / gastrocnemius of young control 3 / N_GAS_YC-3
- **YE** (6): GSM5942479 / soleus of young exercise 1 / N_SOL_YE-1; GSM5942480 / soleus of young exercise 2 / N_SOL_YE-2; GSM5942481 / soleus of young exercise 4 / N_SOL_YE-4; GSM5942491 / gastrocnemius of young exercise 1 / N_GAS_YE-1; GSM5942492 / gastrocnemius of young exercise 2 / N_GAS_YE-2; GSM5942493 / gastrocnemius of young exercise 4 / N_GAS_YE-4

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE198266"], "assay": "bulk RNA-seq (Illumina NovaSeq, TruSeq stranded mRNA), HISAT2 alignment, FPKM (S5.4.p1, GEO data_processing)", "samples": "male C57BL/6 mice, young (9 wk) and old (84 wk), control or 4 weeks treadmill exercise; n=3 mice per group; soleus (SOL) and gastrocnemius (GAS) from each mouse; 24 libraries (S5.1.p1)", "factors": {"tissue": ["SOL", "GAS"], "age": ["young", "old"], "intervention": ["control", "exercise"]}, "primary_estimand": "Effect of 4 weeks of treadmill exercise on gene expression within each muscle (SOL, GAS) and age group: YE vs YC and OE vs OC, separately in SOL and GAS", "planned_contrasts": ["SOL YE/YC (S2.3.p1; paper: 31 DEGs, 11 up / 20 down)", "GAS YE/YC (S2.3.p1; paper: 13 DEGs, 7 up / 6 down)", "SOL OE/OC (S2.4.p1; paper: 20 DEGs, 10 up / 10 down)", "GAS OE/OC (S2.4.p1; paper: 13 DEGs, 6 up / 7 down)"], "non_exercise_contrasts_in_paper": "OC/YC per tissue (aging, S2.2.p1: 196 SOL, 119 GAS) and SOL vs GAS per group (S2.5.p1, p<0.05 & FC>2); not part of the exercise estimand", "normalization": "FPKM -> +1, log2, quantile normalization with preprocessCore (S5.5.p1)", "paper_method": "independent t-test per gene on the pre-processed data, Bioconductor genefilter (S5.6.2.p1); each comparison uses only its two groups", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "source_locator": "S5.6.2.p1"}, "repeated_measure_unit": "mouse (SOL  ... [329 more characters]

reasoning: Methods S5.5.p1 and S5.6.2.p1 give the preprocessing, test and threshold (p < 0.05, FC > 1.5 for within-tissue comparisons). Results S2.3.p1 and S2.4.p1 give the exercise DEG counts. The aging and SOL-vs-GAS comparisons are not exercise effects and are left out.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266_N_log2qn_symbol.csv", "owned": true, "checks": ["paper S4.p3 names GSE198266", "GEO series has 24 samples = 2 tissues x 4 groups x 3 mice, matching S5.1.p1", "matrix N_* columns match metadata description 24/24"], "accession": "GSE198266", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE198266\\GSE198266_metadata.csv"}

reasoning: S4.p3 deposits GSE198266. The supplementary file GSE198266_preprocessed_data2.csv carries 24 FPKM columns and 24 N_* pre-processed columns whose names equal the metadata description field.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 24, "n_metadata": 24, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\aligned\\aligned_metadata.csv", "columns": {"tissue": {"source": "description", "regex": "^N_(SOL|GAS)_[YO][CE]-\\d$"}, "grp": {"source": "description", "regex": "^N_(?:SOL|GAS)_([YO][CE])-\\d$"}, "mouse": {"source": "description", "regex": "^N_(?:SOL|GAS)_([YO][CE])-(\\d)$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\aligned\\design_metadata.csv", "sha256": "7a9259b65306f76c921749ebad9ca9859243ec27b3e12cddb10007c5f9f9f9e3", "levels": {"tissue": {"SOL": 12, "GAS": 12}, "grp": {"YC": 6, "YE": 6, "OC": 6, "OE": 6}, "mouse": {"YC_1": 2, "YC_2": 2, "YC_3": 2, "YE_1": 2, "YE_2": 2, "YE_4": 2, "OC_3": 2, "OC_4": 2, "OC_5": 2, "OE_1": 2, "OE_2": 2, "OE_3": 2}}}}

reasoning: Exact match of matrix column names to the metadata description (N_SOL_YC-1 ...), as inspect reported 24/24. tissue, group (YC/YE/OC/OE) and mouse id are parsed from the description; groups agree with source_name_ch1 (e.g. 'soleus of young control').

### matrix (valid, not_started)

final: {"source": "GSE198266_preprocessed_data2.csv, N_* columns, re-indexed by repaired gene symbol (prep_matrix.py)", "paper_input": "pre-processed data: FPKM +1, log2, quantile normalized (S5.5.p1)", "matrix_type": "log-transformed (log2(FPKM+1), quantile-normalized)", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\aligned\\aligned_matrix.csv", "sha256": "11a7156004e04d851117e2dfa1e3ac520a55f0ddb5f247f014ed11d4234155bd", "n_features": 18795, "n_samples": 24, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 14.72078666, "median": 1.46938487, "integer_fraction": 0.1678, "candidates": ["log_scale"]}}

reasoning: N_* values range 0-14.7, every column has the same sorted distribution (quantile normalization; max spread 0.03 from ties), and the deposited group .mean columns equal means of the N_* columns. They are the paper's pre-processed input to the t-test. The raw *_FPKM columns in the same file are not used because the repository has no quantile-normalization transform and the authors' normalized values are deposited.

### design (valid, not_started)

final: {"analysis_type": "multi-group within strata (tissue), planned exercise contrasts per age", "design_column": "grp", "formula": "~ 0 + grp (fitted separately within SOL and within GAS)", "contrasts": [{"name": "grp_YE_vs_YC_tissue-SOL", "control": "YC", "treatment": "YE", "stratum": "SOL", "role": "primary"}, {"name": "grp_OE_vs_OC_tissue-SOL", "control": "OC", "treatment": "OE", "stratum": "SOL", "role": "primary"}, {"name": "grp_YE_vs_YC_tissue-GAS", "control": "YC", "treatment": "YE", "stratum": "GAS", "role": "primary"}, {"name": "grp_OE_vs_OC_tissue-GAS", "control": "OC", "treatment": "OE", "stratum": "GAS", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\suitability\\suitability.md", "n_comparisons": 12, "n_analyzable": 12}}

reasoning: The paper's exercise question is YE vs YC and OE vs OC within each muscle (S2.3.p1, S2.4.p1). grp has four levels within a tissue; one limma model per tissue with planned contrasts uses all 12 samples of that tissue for variance estimation, never pooling levels. Tissue is a stratum. n = 3 per group.

rejected alternatives: [{"value": "pool young and old (exercise vs control per tissue)", "reason_rejected": "paper analyses age groups separately (S2.3, S2.4); pooling changes the estimand"}, {"value": "one model on all 24 samples with tissue x grp cells", "reason_rejected": "SOL and GAS come from the same mice; fitting each tissue separately keeps one sample per mouse per fit and matches the paper's within-tissue comparisons"}, {"value": "age x exercise interaction", "reason_rejected": "paper does not test it; not pl ... [8 more characters]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 24, "n_columns": 4, "columns": ["Intercept", "grp_OE", "grp_YC", "grp_YE"], "rank": 4, "full_rank": true, "residual_df": 20, "levels": {"grp": {"YC": 6, "YE": 6, "OC": 6, "OE": 6}}, "cells": [{"cell": ["OC"], "n": 6}, {"cell": ["OE"], "n": 6}, {"cell": ["YC"], "n": 6}, {"cell": ["YE"], "n": 6}], "min_cell_size": 6, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 24, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 24, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 8, "status": "nested_in_primary", "crosstab": {"OC": {"gastrocnemius of old control": 3, "gastrocnemius of old exercise": 0, "gastrocnemius of young control": 0, "gastrocnemius of young exercise": 0, "soleus of old control": 3, "soleus of old exercise": 0, "soleus of young control": 0, "soleus of young exercise": 0}, "OE": {"gastrocnemius of old control": 0, "gastrocnemius of old exercise": 3, "gastrocnemius of young control": 0, "gastrocnemius of young exercise": 0, "soleus of old control": 0, "soleus  ... [3883 more characters]

reasoning: Within a tissue every mouse contributes one sample, so there is no repeated measure to block; the mouse key only links SOL and GAS, which are never compared here. No batch, sex (all male) or other covariate is recorded; the paper adjusts for none.

### method (valid, not_started)

final: {"matrix_type": "log-transformed (log2(FPKM+1), quantile-normalized)", "method": "limma (moderated t, empirical Bayes) on the authors' log2(FPKM+1) quantile-normalized values, one fit per tissue", "formula": "~ 0 + grp", "paper_route": {"method": "independent two-sample t-test per gene (genefilter) on the 6 samples of each comparison", "status": "blocked", "reason": "the repository has no per-gene t-test executor; limma on the same log-scale input is the validated alternative"}, "deviations": ["limma moderated t instead of an ordinary t-test (variance shrinkage, residual variance from all 12 samples of the tissue in the primary runs)", "sensitivity runs use only the two compared groups (6 samples), closer to the paper's per-comparison t-test"]}

reasoning: Matrix is already log-scale (matrix-method policy: limma as-is). The paper's ordinary t-test cannot be run by a repository executor; the moderated t on identical input is the closest validated route and is declared as a deviation.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "paper rule (raw p < 0.05 and FC > 1.5) applied to limma moderated-t p-values; FDR < 0.05 reported as a separate audit rule"}

reasoning: S5.6.2.p1: p-value < 0.05 and fold change > 1.5 for within-tissue comparisons; FC 1.5 = |log2FC| > 0.5849625.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "tissue_SOL", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\tissue_SOL\\input\\matrix.csv", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\tissue_SOL\\DEG_results_grp_YE_vs_YC_tissue-SOL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\tissue_SOL\\DEG_results_grp_OE_vs_OC_tissue-SOL.csv"], "counts": {"tissue_SOL/grp_YE_vs_YC_tissue-SOL": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 18328, "n_significant": 68, "n_up": 30, "n_down": 38, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 18328, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "tissue_SOL/grp_OE_vs_OC_tissue-SOL": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 18328, "n_significant": 29, "n_up": 11, "n_down": 18, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 18328, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: one limma fit on the 12 SOL samples (~0+grp), planned exercise contrasts per age

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "tissue_GAS", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\tissue_GAS\\input\\matrix.csv", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\tissue_GAS\\DEG_results_grp_YE_vs_YC_tissue-GAS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\tissue_GAS\\DEG_results_grp_OE_vs_OC_tissue-GAS.csv"], "counts": {"tissue_GAS/grp_YE_vs_YC_tissue-GAS": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17751, "n_significant": 40, "n_up": 22, "n_down": 18, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17751, "n_significant": 2, "n_up": 1, "n_down": 1, "deg_sanity": "ok"}}, "tissue_GAS/grp_OE_vs_OC_tissue-GAS": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17751, "n_significant": 31, "n_up": 12, "n_down": 19, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17751, "n_significant": 2, "n_up": 0, "n_down": 2, "deg_sanity": "ok"}}}}

reasoning: one limma fit on the 12 GAS samples (~0+grp), planned exercise contrasts per age

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "SOL_YE_vs_YC_2grp", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\SOL_YE_vs_YC_2grp\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\SOL_YE_vs_YC_2grp\\DEG_results_YE_vs_YC.csv"], "counts": {"SOL_YE_vs_YC_2grp": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17484, "n_significant": 53, "n_up": 21, "n_down": 32, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17484, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: two-group fit on only the 6 compared samples, as the paper's per-comparison t-test

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "SOL_OE_vs_OC_2grp", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\SOL_OE_vs_OC_2grp\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\SOL_OE_vs_OC_2grp\\DEG_results_OE_vs_OC.csv"], "counts": {"SOL_OE_vs_OC_2grp": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17782, "n_significant": 34, "n_up": 15, "n_down": 19, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17782, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: two-group fit on only the 6 compared samples

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "GAS_YE_vs_YC_2grp", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\GAS_YE_vs_YC_2grp\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\GAS_YE_vs_YC_2grp\\DEG_results_YE_vs_YC.csv"], "counts": {"GAS_YE_vs_YC_2grp": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 16949, "n_significant": 38, "n_up": 20, "n_down": 18, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 16949, "n_significant": 1, "n_up": 0, "n_down": 1, "deg_sanity": "ok"}}}}

reasoning: two-group fit on only the 6 compared samples

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "GAS_OE_vs_OC_2grp", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\GAS_OE_vs_OC_2grp\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\GAS_OE_vs_OC_2grp\\DEG_results_OE_vs_OC.csv"], "counts": {"GAS_OE_vs_OC_2grp": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17250, "n_significant": 31, "n_up": 11, "n_down": 20, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17250, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: two-group fit on only the 6 compared samples

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "tissue_SOL/grp_YE_vs_YC_tissue-SOL", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\enrichment_tissue_SOL_grp_YE_vs_YC_tissue-SOL\\gsea\\DEG_results_grp_YE_vs_YC_tissue-SOL_GSEA_Hallmark.csv"], "summary": "GSEA complete on 18328 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 36 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.46 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.78 | NOM p=0.00e+00 | FDR q=2.51e-03 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.72 | NOM p=2.03e-03 | FDR q=4.81e-03 - HALLMARK_BILE_ACID_METABOLISM | NES=1.61 | NOM p=2.16e-03 | FDR q=9.87e-03 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.45 | NOM p=1.14e-02 | FDR q=4.28e-02 - HALLMARK_MYC_TARGETS_V2 | NES=1.44 | NOM p=3.26e-02 | FDR q=4.11e-02 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.42 | NOM p=6.52e-03 | FDR q=4.42e-02 - HALLMARK_PEROXISOME | NES=1.22 | NOM p=1.17e-01 | FDR q=2.16e-01 - HALLMARK_E2F_TARGETS | NES=1.22 | NOM p=7.74e-02 | FDR q=2.00e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-2.63 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MY ... [436 more characters]

reasoning: paper runs Hallmark GSEA for SOL YE/YC (Table 12)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "tissue_SOL/grp_OE_vs_OC_tissue-SOL", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\enrichment_tissue_SOL_grp_OE_vs_OC_tissue-SOL\\gsea\\DEG_results_grp_OE_vs_OC_tissue-SOL_GSEA_Hallmark.csv"], "summary": "GSEA complete on 18328 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 11 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_BILE_ACID_METABOLISM | NES=1.52 | NOM p=9.57e-03 | FDR q=1.59e-01 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.40 | NOM p=1.34e-02 | FDR q=2.56e-01 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.39 | NOM p=9.83e-03 | FDR q=1.92e-01 - HALLMARK_HEME_METABOLISM | NES=1.37 | NOM p=7.61e-03 | FDR q=1.68e-01 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.20 | NOM p=9.54e-02 | FDR q=5.61e-01 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.20 | NOM p=1.44e-01 | FDR q=4.77e-01 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.15 | NOM p=1.32e-01 | FDR q=6.17e-01 - HALLMARK_MITOTIC_SPINDLE | NES=1.11 | NOM p=1.99e-01 | FDR q=7.00e-01 - HALLMARK_COMPLEMENT | NES=1.11 | NOM p=2.12e-01 | FDR q=6.29e-01 - HALLMARK_ADIPOGENESIS | NES=1.10 | NOM p=2.34e-01 | FDR q=6.01e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-1.60 | NOM p=0.00e+00 | FDR q=7.84e-02 - HALLMARK_UNFOLDED_PROTEI ... [436 more characters]

reasoning: paper runs Hallmark GSEA for SOL OE/OC (Table 13)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "tissue_GAS/grp_YE_vs_YC_tissue-GAS", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\enrichment_tissue_GAS_grp_YE_vs_YC_tissue-GAS\\gsea\\DEG_results_grp_YE_vs_YC_tissue-GAS_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17751 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 18 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.85 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.24 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.13 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=1.96 | NOM p=0.00e+00 | FDR q=5.59e-04 - HALLMARK_BILE_ACID_METABOLISM | NES=1.82 | NOM p=0.00e+00 | FDR q=1.40e-03 - HALLMARK_PEROXISOME | NES=1.60 | NOM p=5.85e-03 | FDR q=1.28e-02 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.29 | NOM p=3.12e-02 | FDR q=1.72e-01 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.27 | NOM p=1.06e-01 | FDR q=1.82e-01 - HALLMARK_COAGULATION | NES=1.23 | NOM p=8.72e-02 | FDR q=2.14e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=-1.62 | NOM p=3.12e-03 | FDR q=7.13e-02 - HALLMARK_G ... [436 more characters]

reasoning: paper runs Hallmark GSEA for GAS YE/YC (Table 11)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "tissue_GAS/grp_OE_vs_OC_tissue-GAS", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35440516\\GSE198266\\results\\enrichment_tissue_GAS_grp_OE_vs_OC_tissue-GAS\\gsea\\DEG_results_grp_OE_vs_OC_tissue-GAS_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17751 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 16 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.54 | NOM p=4.42e-03 | FDR q=1.78e-01 - HALLMARK_DNA_REPAIR | NES=1.51 | NOM p=6.88e-03 | FDR q=1.07e-01 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.48 | NOM p=2.70e-03 | FDR q=9.17e-02 - HALLMARK_NOTCH_SIGNALING | NES=1.37 | NOM p=7.09e-02 | FDR q=2.13e-01 - HALLMARK_MYOGENESIS | NES=1.26 | NOM p=5.76e-02 | FDR q=4.17e-01 - HALLMARK_GLYCOLYSIS | NES=1.24 | NOM p=8.31e-02 | FDR q=4.10e-01 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.20 | NOM p=1.22e-01 | FDR q=4.86e-01 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.14 | NOM p=1.81e-01 | FDR q=6.52e-01 - HALLMARK_KRAS_SIGNALING_DN | NES=1.05 | NOM p=3.68e-01 | FDR q=1.00e+00 - HALLMARK_APICAL_JUNCTION | NES=1.00 | NOM p=4.73e-01 | FDR q=1.00e+00 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MTORC1_SIGNALING | NES=-1.82 | NOM p=0.00e+00 | FDR q=1.77e-02 - HALLMARK_TNFA_SIGNALING_VIA_NFKB  ... [436 more characters]

reasoning: paper runs Hallmark GSEA for GAS OE/OC (Table 9)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["paper used an ordinary t-test; counts from limma's moderated t on the same input are not expected to match exactly", "raw-p threshold without multiple-testing control, n = 3 per group: the paper-rule DEG lists are expected to contain many false positives", "fold change taken as the difference of group means on the log2 quantile-normalized scale", "direction vs paper: HALLMARK_MYOGENESIS in SOL OE/OC has NES +0.95 (p = 0.59, not significant) whereas the paper reports it enriched in SOL OC (Table 13); all paper-named genes keep the paper direction"], "results": {"tissue_SOL/grp_YE_vs_YC_tissue-SOL": {"n_deg": 68, "up": 30, "down": 38, "rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 0}, "tissue_SOL/grp_OE_vs_OC_tissue-SOL": {"n_deg": 29, "up": 11, "down": 18, "rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 0}, "tissue_GAS/grp_YE_vs_YC_tissue-GAS": {"n_deg": 40, "up": 22, "down": 18, "rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 2}, "tissue_GAS/grp_OE_vs_OC_tissue-GAS": {"n_deg": 31, "up": 12, "down": 19, "rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 2}, "SOL_YE_vs_YC_2grp": {"n_deg": 53, "up": 21, "down": 32, "rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 0}, "SOL_OE_vs_OC_2grp": {"n_deg": 34, "up": 15, "down": 19, "rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 0}, "GAS_YE_vs_YC_2grp": {"n_deg": 38, "up": 20, " ... [1757 more characters]

reasoning: Method deviation (limma vs t-test) with the paper's threshold on the paper's own pre-processed matrix.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE test",
    "paper": "independent t-test (genefilter), S5.6.2.p1",
    "data": "no t-test executor; limma moderated t used",
    "disposition": "declared_deviation"
  },
  {
    "item": "matrix",
    "paper": "pre-processed FPKM (log2 +1, quantile)",
    "data": "deposited N_* columns are those values; gene symbols Excel-mangled for 25 genes, repaired from Description",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID35440516 / GSE198266

## What ran
- Route: case spec (`case_spec.json`) through `python -m tools.case_runner execute`. Status: completed. The decision-contract validator reported 0 errors across 19 records. Preflight was skipped, as instructed.
- Matrix: the `N_*` columns of `GSE198266_preprocessed_data2.csv`. These hold the authors' pre-processed values: FPKM+1, log2, then quantile normalization (paper S5.5.p1). Checks:
  - every column has the same sorted distribution;
  - the deposited group `.mean` columns equal the means of these columns.
- Prep script: `prep_matrix.py` keeps the 24 `N_*` columns and indexes the rows by gene symbol. It repairs 25 gene symbols that Excel had turned into dates (`02-Sep` became Septin2, `01-Mar` became Mtarc1 or Marchf1, `15-Sep` became Selenof), using the Description column. Output: `GSE198266_N_log2qn_symbol.csv`.
- Alignment: exact match on the metadata `description` field (24 of 24). From it the prep parsed the tissue (SOL/GAS), the group (YC/YE/OC/OE) and the mouse ID. SOL and GAS come from the same 12 mice.
- Design: tissue is a stratum, and each tissue gets its own limma fit (`~ 0 + grp`, 12 samples). The planned exercise contrasts are YE vs YC and OE vs OC. No blocking is needed: each mouse appears once per tissue, and tissues are never compared with each other. n = 3 per group. Suitability: analyzable.
- Sensitivity runs: two-group limma on only the 6 samples being compared, which is closer to the paper's per-comparison t-test.
- GSEA: Hallmark, ranked by the moderated t, for the 4 primary tables, all completed. ORA was not run, because the paper used DAVID only for SOL vs GAS.

## DEG counts vs paper
Paper threshold (S5.6.2.p1): raw p < 0.05 and FC > 1.5, i.e. |log2FC| > 0.5849625.

| Contrast | Ours, primary (up/down) | Ours, 6-sample sensitivity | Paper (up/down) | FDR < 0.05 audit |
|---|---|---|---|---|
| SOL YE/YC | 68 (30/38) | 53 | 31 (11/20) | 0 |
| GAS YE/YC | 40 (22/18) | 38 | 13 (7/6) | 2 |
| SOL OE/OC | 29 (11/18) | 34 | 20 (10/10) | 0 |
| GAS OE/OC | 31 (12/19) | 31 | 13 (6/7) | 2 |

Our counts are 1.5 to 3 times the paper's.

**Paper-named genes.** All 9 lookups keep the paper's direction of change. Six of them meet the paper rule here:
- Nr1d1 in SOL and in GAS;
- Pik3r1 in GAS;
- Hbb-b1 in SOL (p = 0.0496) and in GAS;
- Chtop in SOL and in GAS;
- Pnpla3 in SOL.

Three miss on p alone:
- Pik3r1 in SOL YE/YC (p = 0.067);
- Pnpla3 in GAS OE/OC (p = 0.068).

**GSEA against the paper. ... [1897 more characters]
