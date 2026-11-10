# Review packet B (the analysis' decisions): GSE240131

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.4.treatment", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_T_vs_C | 2761 | 2629 | pvalue < 0.05 and |log2FoldChange| >= 0.584963 | 3 | 3 | 3 | 3 | 2726 | 2629 | 2058 | 550 | 0.044 | 0.16 |

## Samples per design level

### `grp`
- **C** (3): GSM7682807 / Heart, C1; GSM7682808 / Heart, C2; GSM7682809 / Heart, C3
- **E** (3): GSM7682810 / Heart, E1; GSM7682811 / Heart, E2; GSM7682812 / Heart, E3
- **T** (3): GSM7682813 / Heart, T1; GSM7682814 / Heart, T2; GSM7682815 / Heart, T3
- **TE** (3): GSM7682816 / Heart, TE1; GSM7682817 / Heart, TE2; GSM7682818 / Heart, TE3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE240131"], "assay": "bulk RNA-seq, whole heart, DNBSEQ-T7 PE150, HISAT2 + featureCounts (S2.4.p1)", "organism": "Mouse (male C57BL/6J, 8 weeks; S2.2.p1)", "factors": {"tumor": ["saline", "B16F10 i.v."], "exercise": ["sedentary", "treadmill low-intensity 4 wk"]}, "groups": "2x2: C (saline), E (exercise), T (B16F10), TE (B16F10 + exercise); n=3 libraries per group, each pooling hearts of two mice (FIG3 legend)", "inclusion": "all 12 heart libraries", "primary_estimand": "Effect of low-intensity exercise training on the heart transcriptome of tumor-bearing (B16F10 cachectic) mice: TE vs T (S3.3.p1, FIG4)", "planned_contrasts": ["T vs C (tumor effect; S3.3.p1: 2020 up, 741 genes in the heart-contraction set, stated as 'upregulated' but the named genes (Myh7b) are tumor-decreased)", "TE vs T (exercise effect in tumor-bearing mice; S3.3.p1: 318 of the 741 and 1447 of the 2020 reversed by exercise)", "E vs C (exercise effect in tumor-free mice; implied by FIG3 clusters and PCA, S3.2.p5; no DEG count)"], "repeated_measure_unit": "none; independent pooled libraries", "paper_method": "edgeR (S2.4.p1); test type and filtering not stated", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "effect_inclusive": true, "source_locator": "S2.4.p1", "text": "fold change >= 1.5 and p-value < 0.05"}, "paper_results": "T vs C: 2020 up, 741 (heart-contraction overlap set base); TE vs T revers ... [101 more characters]

reasoning: S2.2.p1 design (4 wk treadmill, B16F10 i.v. from week 2), S2.4.p1 edgeR FC>=1.5 & p<0.05, S3.3.p1 DEG counts, FIG3 n=3 pooled libraries. Primary estimand is exercise within tumor-bearing mice, as in the title and S3.3.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131_counts_by_symbol.csv", "owned": true, "checks": ["S7.p1 names GSE240131", "GEO samples: heart, male C57BL/6J, Saline/Exercise/B16F10 cells/B16F10 cells+Exercise, 3 each, matching the paper's 2x2 design and n=3", "contact Binbin Liu, Xiamen University = corresponding author/institution"], "accession": "GSE240131", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE240131\\GSE240131_metadata.csv"}

reasoning: Accession, tissue, groups and n all match the paper. GEO extract_protocol says 'livers' and data_processing says 'Assembly: mm10' vs paper GRCm39; recorded as discrepancies, not ownership failures.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^Heart, ([A-Z]+)\\d$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\aligned\\design_metadata.csv", "sha256": "283c214b688d3b78ac2aac9c23312226aa7a6b4c28c899f4bd40363eddccbe64", "levels": {"grp": {"C": 3, "E": 3, "T": 3, "TE": 3}}}}

reasoning: Matrix columns C1..TE3 equal the suffix of the GEO title 'Heart, C1'; exact match on the derived key. grp = C/E/T/TE agrees with characteristics treatment (Saline/Exercise/B16F10 cells/B16F10 cells+Exercise).

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\aligned\\aligned_matrix.csv", "sha256": "027f56bda9bb0301cfb6f46529c4e408ec97b6733a1e3e909c5449c843a4afda", "n_features": 17397, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 429898.7, "median": 108.0, "integer_fraction": 0.9259, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GEO data_processing: featureCounts, 'raw counts'. Library sizes 8.8-13.3 M, median 96-213, about 7% of cells are non-integer (e.g. Ccna2 19.47): featureCounts fractional multi-mapping counts, i.e. estimated counts on the count scale, not FPKM/TPM. Paper input is the same featureCounts table (S2.4.p1). Rounded to integers before edgeR.

### design (valid, not_started)

final: {"analysis_type": "multi-group pairwise", "design_column": "grp", "contrasts": [{"name": "grp_TE_vs_T", "control": "T", "treatment": "TE", "role": "primary"}, {"name": "grp_E_vs_C", "control": "C", "treatment": "E", "role": "secondary"}, {"name": "grp_T_vs_C", "control": "C", "treatment": "T", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: Paper (S3.3.p1, FIG4) uses T vs C and TE vs T DEG sets; E vs C is the exercise effect in tumor-free mice (FIG3, S3.2.p5). TE vs T is primary. Data check: melanoma markers (Pmel, Tyrp1, Dct, Mlana, plus Mki67/Top2a) are 10^3-10^4-fold higher in T1 and T2 than in all other libraries and absent from all TE libraries, so T1/T2 contain metastatic tumor tissue; the TE vs T and T vs C contrasts mix cardiac change with tumor-cell content. The contrast remains identifiable (no batch aliasing), so it is run with this caveat rather than refused; E vs C is unaffected.

rejected alternatives: [{"value": "pooled exercise (E+TE) vs sedentary (C+T)", "reason_rejected": "pools tumor levels; the paper compares exercise within tumor status"}, {"value": "2x2 factorial with tumor:exercise interaction as primary", "reason_rejected": "paper reports pairwise edgeR DEG sets and their overlaps, not an interaction test"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 12, "n_columns": 4, "columns": ["Intercept", "grp_E", "grp_T", "grp_TE"], "rank": 4, "full_rank": true, "residual_df": 8, "levels": {"grp": {"C": 3, "E": 3, "T": 3, "TE": 3}}, "cells": [{"cell": ["C"], "n": 3}, {"cell": ["E"], "n": 3}, {"cell": ["T"], "n": 3}, {"cell": ["TE"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 12, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 12, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.Sex", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.genotype", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.4.treatme ... [2044 more characters]

reasoning: Independent pooled libraries, one tissue, one sex, no batch or lane recorded. Tumor-tissue content in T1/T2 cannot be modelled as a covariate with n=3 (it is nearly a group property); recorded as a caveat instead.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "edgeR (TMM, GLM quasi-likelihood F-test, inmoose), pairwise two-group fits", "formula": "~ grp (two levels per fit)", "rounding_documented": true, "deviations": ["featureCounts fractional counts rounded to integers before edgeR (the executor requires integers)", "paper does not state its edgeR test (exactTest vs QL) or filtering; QL F-test on all non-zero genes, each pair fitted on its own 6 samples"], "transform": "round"}

reasoning: Paper used edgeR (S2.4.p1); edgeR runs on these count-scale data. Two-group executor per pair keeps the paper's pairwise DEG sets.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "effect_inclusive": true}, "threshold_source": "paper", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "effect_inclusive": true}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: S2.4.p1: FC >= 1.5 and p-value < 0.05 (raw p) -> p < 0.05 and |log2FC| >= log2(1.5) = 0.5849625. Audit: BH FDR < 0.05, no FC rule.

### execution (valid, completed)

final: {"method": "run_edger_analysis", "subset": "grp_TE_vs_T", "role": "primary", "tool": "tools.edger_tools:run_edger_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\grp_TE_vs_T\\input\\matrix.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\grp_TE_vs_T\\DEG_results_TE_vs_T.csv"], "counts": {"grp_TE_vs_T": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| >= 0.584963", "n_tested": 17023, "n_significant": 2619, "n_up": 675, "n_down": 1944, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17023, "n_significant": 2, "n_up": 0, "n_down": 2, "deg_sanity": "ok"}}}}

reasoning: exercise effect in tumor-bearing mice (S3.3.p1, FIG4); paper's edgeR

### execution (valid, completed)

final: {"method": "run_edger_analysis", "subset": "grp_E_vs_C", "role": "secondary", "tool": "tools.edger_tools:run_edger_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\grp_E_vs_C\\input\\matrix.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\grp_E_vs_C\\DEG_results_E_vs_C.csv"], "counts": {"grp_E_vs_C": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| >= 0.584963", "n_tested": 16445, "n_significant": 572, "n_up": 351, "n_down": 221, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 16445, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: exercise effect in tumor-free mice (FIG3, S3.2.p5)

### execution (valid, completed)

final: {"method": "run_edger_analysis", "subset": "grp_T_vs_C", "role": "secondary", "tool": "tools.edger_tools:run_edger_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\grp_T_vs_C\\input\\matrix.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\grp_T_vs_C\\DEG_results_T_vs_C.csv"], "counts": {"grp_T_vs_C": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| >= 0.584963", "n_tested": 17032, "n_significant": 2629, "n_up": 2028, "n_down": 601, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17032, "n_significant": 3, "n_up": 3, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: tumor effect; base set for the paper's reversal overlaps (S3.3.p1)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_TE_vs_T", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "effect_inclusive": true}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\enrichment_grp_TE_vs_T\\ora\\DEG_results_TE_vs_T_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\enrichment_grp_TE_vs_T\\ora\\DEG_results_TE_vs_T_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\enrichment_grp_TE_vs_T\\ora\\DEG_results_TE_vs_T_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\enrichment_grp_TE_vs_T\\ora\\DEG_results_TE_vs_T_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 2619 Mouse genes (direction=all, pvalue<0.05, |log2FC|>0.5849625). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Mitotic Sister Chromatid Segregation (GO:0000070) | padj=7.83e-09 | overlap=44/111 | genes=CDCA5;NCAPG2;KIF14;CDCA8;NCAPG;KIF11;NCAPH;NSL1;SMC2;CCNB1;D ... [1179 more characters]

reasoning: paper reports GO enrichment of exercise-reversed genes (FIG4B/F)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_TE_vs_T", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\enrichment_grp_TE_vs_T\\gsea\\DEG_results_TE_vs_T_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17023 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 39 significant at FDR q < 0.25. ### Top 9 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.04 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=1.77 | NOM p=0.00e+00 | FDR q=2.99e-03 - HALLMARK_UV_RESPONSE_DN | NES=1.72 | NOM p=0.00e+00 | FDR q=4.79e-03 - HALLMARK_BILE_ACID_METABOLISM | NES=1.38 | NOM p=2.38e-02 | FDR q=6.71e-02 - HALLMARK_MYOGENESIS | NES=1.21 | NOM p=5.17e-02 | FDR q=2.02e-01 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.19 | NOM p=1.02e-01 | FDR q=1.99e-01 - HALLMARK_HEME_METABOLISM | NES=0.97 | NOM p=5.22e-01 | FDR q=6.80e-01 - HALLMARK_PANCREAS_BETA_CELLS | NES=0.95 | NOM p=5.39e-01 | FDR q=6.71e-01 - HALLMARK_KRAS_SIGNALING_DN | NES=0.92 | NOM p=7.19e-01 | FDR q=6.77e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_E2F_TARGETS | NES=-3.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=-2.88 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=-2.62 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=-2.42 |  ... [374 more characters]

reasoning: paper reports GO enrichment of exercise-reversed genes (FIG4B/F)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_E_vs_C", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "effect_inclusive": true}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\enrichment_grp_E_vs_C\\ora\\DEG_results_E_vs_C_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\enrichment_grp_E_vs_C\\ora\\DEG_results_E_vs_C_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\enrichment_grp_E_vs_C\\ora\\DEG_results_E_vs_C_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\enrichment_grp_E_vs_C\\ora\\DEG_results_E_vs_C_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 572 Mouse genes (direction=all, pvalue<0.05, |log2FC|>0.5849625). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Negative Regulation Of Transcription By RNA Polymerase II (GO:0000122) | padj=4.39e-03 | overlap=46/763 | genes=CEBPB;CITED2;ZBTB49;ARID4B;GATA3;PRDM1;ZBTB2;IRF2 ... [1170 more characters]

reasoning: exercise effect in tumor-free hearts; exploratory pathway view

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_E_vs_C", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38370171\\GSE240131\\results\\enrichment_grp_E_vs_C\\gsea\\DEG_results_E_vs_C_GSEA_Hallmark.csv"], "summary": "GSEA complete on 16445 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 34 significant at FDR q < 0.25. ### Top 8 UP (NES > 0, enriched in treatment): - HALLMARK_E2F_TARGETS | NES=1.74 | NOM p=0.00e+00 | FDR q=6.18e-03 - HALLMARK_G2M_CHECKPOINT | NES=1.66 | NOM p=0.00e+00 | FDR q=7.52e-03 - HALLMARK_MITOTIC_SPINDLE | NES=1.35 | NOM p=1.64e-02 | FDR q=1.08e-01 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=1.24 | NOM p=1.64e-01 | FDR q=1.93e-01 - HALLMARK_DNA_REPAIR | NES=1.04 | NOM p=3.75e-01 | FDR q=5.91e-01 - HALLMARK_SPERMATOGENESIS | NES=0.90 | NOM p=6.82e-01 | FDR q=9.27e-01 - HALLMARK_MYC_TARGETS_V1 | NES=0.69 | NOM p=9.94e-01 | FDR q=1.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=0.38 | NOM p=1.00e+00 | FDR q=1.00e+00 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-3.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=-2.21 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TGF_BETA_SIGNALING | NES=-2.02 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=-2.01 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYOGENESIS | NES=-1.99 | ... [371 more characters]

reasoning: exercise effect in tumor-free hearts; exploratory pathway view

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["T1 and T2 heart libraries contain melanoma tumor tissue (Pmel, Tyrp1, Dct, Mlana 10^3-10^4-fold above all other libraries; none in TE). TE vs T and T vs C therefore mix exercise/tumor effects on the heart with tumor-cell content; the paper's 'cell cycle and DNA replication' genes up by tumor and reversed by exercise (S3.3.p1) are consistent with this contamination.", "Paper text says the tumor 'upregulated 741 genes' later reversed by exercise, but the named genes (Myh7b, Rnf207, Tmem65) are tumor-decreased; we read 741 as tumor-down genes.", "n=3 pooled libraries per group; raw p threshold without FDR control."], "results": {"grp_TE_vs_T": {"n_deg": 2619, "up": 675, "down": 1944, "rule": "pvalue < 0.05 and |log2FoldChange| >= 0.584963", "audit_n": 2}, "grp_E_vs_C": {"n_deg": 572, "up": 351, "down": 221, "rule": "pvalue < 0.05 and |log2FoldChange| >= 0.584963", "audit_n": 0}, "grp_T_vs_C": {"n_deg": 2629, "up": 2028, "down": 601, "rule": "pvalue < 0.05 and |log2FoldChange| >= 0.584963", "audit_n": 3}}, "paper_counts": {"grp_T_vs_C": 2761}, "comparison": {"grp_T_vs_C": {"ours": 2629, "paper": 2761}}, "paper_gene_check": {"grp_TE_vs_T": {"Myh7b": {"log2FoldChange": 2.3686, "padj": 0.2471, "pvalue": 0.0018}, "Pde4d": {"log2FoldChange": 0.7973, "padj": 0.2576, "pvalue": 0.026}, "Rnf207": {"log2FoldChange": 1.4339, "padj": 0.2475, "pvalue": 0.0146}, "Tmem65": {"log2FoldChange": 1.2352, "padj": 0.2471, "pvalue": 0.0103}, "Kcnj5": {"log2F ... [577 more characters]

reasoning: paper_counts T vs C = 2020 up + 741 down (S3.3.p1; 741 read as tumor-down). No total DEG count is given for TE vs T or E vs C; only overlaps 318/1447, computed post hoc from our tables.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "direction of the 741-gene set",
    "paper": "S3.3.p1 'tumor significantly upregulated 741 genes ... repressed by exercise'",
    "data": "named genes Myh7b/Rnf207/Tmem65 are lower in T than C and higher in TE",
    "disposition": "executable_without_change"
  },
  {
    "item": "tissue in GEO extract protocol",
    "paper": "whole heart (S2.4.p1)",
    "data": "GEO extract_protocol says 'livers'; title/source say heart",
    "disposition": "executable_without_change"
  },
  {
    "item": "genome assembly",
    "paper": "GRCm39 (S2.4.p1)",
    "data": "GEO data_processing 'Assembly: mm10'",
    "disposition": "executable_without_change"
  },
  {
    "item": "tumor tissue in T libraries",
    "paper": "heart transcriptome; no mention of cardiac metastasis",
    "data": "T1/T2 dominated by melanocyte/proliferation genes",
    "disposition": "executable_with_caveat"
  },
  {
    "item": "non-integer counts",
    "paper": "featureCounts read counts",
    "data": "~7% fractional values",
    "disposition": "executable_with_rounding"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID38370171 / GSE240131

Paper: Low-intensity exercise training improves systolic function of heart during metastatic melanoma-induced cachexia in mice (PMC10874746).
Status: finished (case `completed`, decision `valid`, route `declared_deviation`, validator 16 records with 0 errors).

## What ran
- `case_runner inspect`, then `prep_matrix.py`. The prep script indexes the deposited `GSE240131_raw_counts.txt.gz` by gene symbol and drops the `st_gene_id` and `gene_id` columns. Six rows with duplicated symbols (Excel-mangled 1-Mar/2-Mar, Plin2) get their st_gene_id appended. Output: `GSE240131_counts_by_symbol.csv`, 17397 x 12.
- Spec: `case_spec.json`. Alignment is an exact match on a key taken from the GEO title (`Heart, C1` -> `C1`): 12/12 samples. Groups are grp = C/E/T/TE, 3 libraries each. Each library pools 2 mice (FIG3).
- Matrix: these are estimated counts. They come from featureCounts and about 7% of values are fractional. They were rounded (`transform: round`) and then analysed with edgeR (inmoose, TMM, QL F-test). Each pair was fitted on its own 6 samples, matching the paper's edgeR (S2.4.p1).
- Executions:
  - `grp_TE_vs_T`, primary: the exercise effect in tumor-bearing mice.
  - `grp_E_vs_C`, secondary: the exercise effect in tumor-free mice.
  - `grp_T_vs_C`, secondary: the tumor effect. This is the base set for the paper's reversal overlaps.
- Enrichment (ORA GO/KEGG and Hallmark GSEA) on TE_vs_T and E_vs_C: completed.
- Post-hoc overlap with `overlap_posthoc.py`, written to `overlap_posthoc.json`.

## Threshold
The paper's rule is in S2.4.p1: FC >= 1.5 and raw p < 0.05. Applied as p < 0.05 and |log2FC| >= 0.5849625, with source `paper`. Audit rule: BH FDR < 0.05, no FC cutoff.

## DEG counts vs paper (paper threshold)
| Table | Ours (up/down) | Paper |
|---|---|---|
| T vs C | 2629 (2028 / 601) | 2020 up / 741 down (S3.3.p1) |
| TE vs T | 2619 (675 / 1944) | no total stated |
| E vs C | 572 (351 / 221) | no count stated |
| tumor-down AND exercise-up (TE vs T) | 236 | 318 of 741 |
| tumor-up AND exercise-down (TE vs T) | 1389 | 1447 of 2020 |

Audit counts (FDR < 0.05): T vs C 3, TE vs T 2, E vs C 0. None of the contrasts holds up under FDR control at n=3.

Named genes: Myh7b, Pde4d, Rnf207, Tmem65, Kcnj5 and Cacnb2 all go down with tumor and up with exercise in TE vs T, matching the paper. Myh7b +2.37 (p=0.0018), Rnf207 +1.43, Tmem65 +1.24, Cacnb2 +1.23 (p=0.048). Kcnj5 just misses (p=0.051). All of them have padj around 0.25.

 ... [2482 more characters]
