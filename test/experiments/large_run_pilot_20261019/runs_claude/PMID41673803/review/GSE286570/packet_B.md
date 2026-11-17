# Review packet B (the analysis' decisions): GSE286570

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.1.genotype", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "characteristics_ch1.2.treatment", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **other_rule_matches_paper**: {"table": "deseq2/grp_HRE_vs_HFD", "paper": 171, "applied": 467, "applied_rule": "pvalue < 0.01 and |log2FoldChange| > 1", "closest_rule": "padj<0.05 & |lfc|>0.584963", "closest_n": 182, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **other_rule_matches_paper**: {"table": "pairwise_HRE_vs_HFD", "paper": 171, "applied": 461, "applied_rule": "pvalue < 0.01 and |log2FoldChange| > 1", "closest_rule": "padj<0.05 & |lfc|>1", "closest_n": 181, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.1.genotype", "pairs_or_sets": 5, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deseq2/grp_HAE_vs_HFD | 1450 | 1488 | pvalue < 0.01 and |log2FoldChange| > 1 | 2082 | 1977 | 1232 | 3332 | 5325 | 4270 | 2381 | 2671 | 0.13 | 0.17 |
| deseq2/grp_HRE_vs_HFD | 171 | 467 | pvalue < 0.01 and |log2FoldChange| > 1 | 183 | 182 | 155 | 302 | 1891 | 1530 | 984 | 722 | 0.153 | 0.06 |
| deseq2/grp_NC_vs_HFD | 2746 | 2470 | pvalue < 0.01 and |log2FoldChange| > 1 | 4163 | 3914 | 2488 | 5745 | 7009 | 5917 | 3500 | 4106 | 0.116 | 0.224 |
| deseq2/grp_HAE_vs_HRE | 625 | 253 | pvalue < 0.01 and |log2FoldChange| > 1 | 24 | 24 | 20 | 33 | 1806 | 1415 | 758 | 447 | 0.16 | 0.058 |
| pairwise_HAE_vs_HFD | 1450 | 1551 | pvalue < 0.01 and |log2FoldChange| > 1 | 2448 | 2439 | 1390 | 3611 | 5214 | 4397 | 2271 | 2821 | 0.074 | 0.178 |
| pairwise_HRE_vs_HFD | 171 | 461 | pvalue < 0.01 and |log2FoldChange| > 1 | 198 | 198 | 181 | 282 | 1627 | 1443 | 904 | 641 | 0.103 | 0.055 |

## Samples per design level

### `grp`
- **HAE** (3): GSM8729509 / H-AE-1 / Library name: H-AE-1; GSM8729510 / H-AE-2 / Library name: H-AE-2; GSM8729511 / H-AE-3 / Library name: H-AE-3
- **HFD** (3): GSM8729506 / H-HFD-1 / Library name: H-HFD-1; GSM8729507 / H-HFD-2 / Library name: H-HFD-2; GSM8729508 / H-HFD-3 / Library name: H-HFD-3
- **HRE** (3): GSM8729512 / H-RE-3 / Library name: H-RE-3; GSM8729513 / H-RE-4 / Library name: H-RE-4; GSM8729514 / H-RE-5 / Library name: H-RE-5
- **NC** (3): GSM8729503 / H-NC-2 / Library name: H-NC-2; GSM8729504 / H-NC-4 / Library name: H-NC-4; GSM8729505 / H-NC-5 / Library name: H-NC-5

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE286570"], "assay": "bulk liver RNA-seq (DNBSEQ-T7), HISAT2 mm10 + featureCounts Gencode vM25 (S4.5.p1)", "organism": "Mouse, C57BL/6 male (S4.1.1.p1)", "factors": {"grp": ["NC (normal chow)", "HFD (high-fat diet, sedentary)", "HAE (HFD + 12 wk aerobic treadmill)", "HRE (HFD + 12 wk resistance ladder climbing)"]}, "sample_inclusion": "Paper animals: NC n=13, HFD/HAE/HRE n=8 each (S4.1.1.p1, S2.1.p1); RNA-seq n per group not stated in the text. GEO deposits 3 livers per group (12 samples).", "primary_estimand": "Effect of aerobic (HAE) and resistance (HRE) exercise on liver gene expression in HFD-fed NAFLD mice, each versus sedentary HFD mice", "planned_contrasts": ["HAE vs HFD (S2.6.p1, Fig. 6C; paper: 1,450 DEGs) - primary exercise contrast", "HRE vs HFD (S2.6.p1, Fig. 6D; paper: 171 DEGs) - primary exercise contrast", "HFD vs NC (S2.6.p1, Fig. 6B; paper: 2,746 DEGs) - diet model check, not an exercise effect", "HAE vs HRE (S2.6.p1, Fig. 6E; paper: 625 DEGs) - exercise-modality comparison"], "repeated_measure_unit": "none; one liver per mouse, independent animals", "normalization": "DESeq2 size factors (S4.5.p1)", "paper_method": "DESeq2 1.40.1 pairwise group comparisons (S4.5.p1); exact design formula and whether each pair was fitted separately not stated", "paper_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "S4.5.p1", "note": "text reads 'log2FC < 1 and a p-value < 1E-2'; inte ... [645 more characters]

reasoning: Results S2.6.p1 lists four liver RNA-seq comparisons with DEG counts; methods S4.5.p1 give DESeq2 and the threshold; DA.p1 names GSE286570. The exercise estimand is each exercise arm versus the sedentary HFD arm; HFD vs NC is the disease-model contrast and HAE vs HRE compares modalities.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE286570\\GSE286570_mRNA_Expression_Profiling.txt.gz", "owned": true, "checks": ["DA.p1 names GSE286570 as the transcriptomic deposit", "GEO tissue = Liver, organism Mus musculus, matches S2.6.p1 liver RNA-seq", "GEO groups NC/HFD/HFD+AE/HFD+RE match the paper's four groups", "data_processing text (Fastp params, HISAT2 mm10, featureCounts vM25, DESeq2 1.40.1) is verbatim the paper's S4.5.p1", "contact Mingliang Wei, Wuhan University = paper author who did RNA-seq analysis (BK1.p1)"], "accession": "GSE286570", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE286570\\GSE286570_metadata.csv"}

reasoning: Paper and GEO series agree on accession, tissue, groups and processing pipeline.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": ["start", "end", "length"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.2.treatment", "recode": {"NC": "NC", "HFD": "HFD", "HFD+AE": "HAE", "HFD+RE": "HRE"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\aligned\\design_metadata.csv", "sha256": "5e7e38faf98df4f85a3d97f3c9875c1cf06d220191fb2f73961481534e5bf794", "levels": {"grp": {"NC": 3, "HFD": 3, "HAE": 3, "HRE": 3}}}}

reasoning: inspect alignment_keys: matrix columns (H-AE1) equal metadata title (H-AE-1) after separator normalization, 12/12. Group from characteristics treatment (identical to the 'genotype' field), recoded to the paper's labels.

### matrix (valid, not_started)

final: {"paper_input": "featureCounts read counts into DESeq2 (S4.5.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\aligned\\aligned_matrix.csv", "sha256": "24a816a610f7d15ca50d7e5aeb5eb8d5fcb6a320c70c0ec99a9d4cbb78377ce7", "n_features": 55291, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 7627011.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 7.6e6, featureCounts layout (Geneid, Chr, Start, End, Strand, Length + 12 sample columns); GEO data_processing: 'table-delimited txt file includes raw counts for each samples'. Matches the paper's DESeq2 input.

### design (valid, not_started)

final: {"analysis_type": "multi-group", "design_column": "grp", "contrasts": [{"name": "grp_HAE_vs_HFD", "control": "HFD", "treatment": "HAE", "role": "primary"}, {"name": "grp_HRE_vs_HFD", "control": "HFD", "treatment": "HRE", "role": "primary"}, {"name": "grp_NC_vs_HFD", "control": "HFD", "treatment": "NC", "role": "secondary"}, {"name": "grp_HAE_vs_HRE", "control": "HRE", "treatment": "HAE", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\suitability\\suitability.md", "n_comparisons": 7, "n_analyzable": 7}}

reasoning: Four independent groups, n=3 each, one factor. Exercise effect = HAE vs HFD and HRE vs HFD (both on HFD background, sedentary HFD reference) per S2.6.p1. HFD vs NC (diet) and HAE vs HRE (modality) are the paper's other two comparisons, kept as secondary. One DESeq2 model on all 12 samples with planned contrasts, not pooled exercise arms. The diet comparison is extracted as NC vs HFD in the model (HFD reference); its DEG count is sign-symmetric to the paper's HFD vs NC.

rejected alternatives: [{"value": "pooled exercise (HAE+HRE) vs HFD", "reason_rejected": "paper analyses each modality separately; pooling mixes two estimands"}, {"value": "exercise vs NC", "reason_rejected": "confounds diet with exercise; paper's exercise contrasts are versus HFD"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 12, "n_columns": 4, "columns": ["Intercept", "grp_HFD", "grp_HRE", "grp_NC"], "rank": 4, "full_rank": true, "residual_df": 8, "levels": {"grp": {"NC": 3, "HFD": 3, "HAE": 3, "HRE": 3}}, "cells": [{"cell": ["HAE"], "n": 3}, {"cell": ["HFD"], "n": 3}, {"cell": ["HRE"], "n": 3}, {"cell": ["NC"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 12, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 12, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.genotype", "n_levels": 4, "status": "complete_confounding", "crosstab": {"HAE": {"HFD": 0, "HFD+AE": 3, "HFD+RE": 0, "NC": 0}, "HFD": {"HFD": 3, "HFD+AE": 0, "HFD+RE": 0, "NC": 0}, "HRE": {"HFD": 0, "HFD+AE": 0, "HFD+RE": 3, "NC": 0} ... [1890 more characters]

reasoning: One liver per independent mouse; no batch, lane, or sex variation recorded (all male, S4.1.1.p1); no blocking unit.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald), one model ~ grp on all 12 samples", "formula": "~ grp", "paper_route": {"method": "DESeq2 1.40.1 (R)", "status": "reproduced_approximately", "reason": "pydeseq2 Wald test reproduces DESeq2; the paper does not say whether each pair was fitted separately, so pairwise two-group fits are run as sensitivity"}, "deviations": ["pydeseq2 instead of R DESeq2 1.40.1", "joint 4-group model (shared dispersion) rather than possibly separate pairwise fits; pairwise fits run as sensitivity"]}

reasoning: Raw counts support the paper's DESeq2 route directly.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0}, "threshold_source": "paper", "applied_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper text 'log2FC < 1 and p-value < 1E-2' read as |log2FC| > 1 and raw p < 0.01 (typo). Raw p, as stated; BH padj < 0.05 reported as audit."}

reasoning: S4.5.p1 threshold, applied exactly as interpreted; raw p kept as the paper states it.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\deseq2\\DEG_results_grp_HAE_vs_HFD.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\deseq2\\DEG_results_grp_HRE_vs_HFD.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\deseq2\\DEG_results_grp_NC_vs_HFD.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\deseq2\\DEG_results_grp_HAE_vs_HRE.csv"], "counts": {"deseq2/grp_HAE_vs_HFD": {"applied": {"rule": "pvalue < 0.01 and |log2FoldChange| > 1", "n_tested": 31338, "n_significant": 1488, "n_up": 420, "n_down": 1068, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 18575, "n_significant": 2082, "n_up": 952, "n_down": 1130, "deg_sanity": "ok"}}, "deseq2/grp_HRE_vs_HFD": {"applied": {"rule": "pvalue < 0.01 and |log2FoldChange| > 1", "n_tested": 31338, "n_significant": 467, "n_up": 120, "n_down": 347, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 19183, "n_significant": 183, "n_up": 68, "n_down": 115, "deg_sanity": "ok"}}, "deseq2/grp_NC_vs_HFD": {"applied": {"rule": "pvalue ... [551 more characters]

reasoning: One DESeq2 model ~ grp on all samples; the paper's four comparisons as contrasts.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pairwise_HAE_vs_HFD", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\pairwise_HAE_vs_HFD\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\pairwise_HAE_vs_HFD\\DEG_results_HAE_vs_HFD.csv"], "counts": {"pairwise_HAE_vs_HFD": {"applied": {"rule": "pvalue < 0.01 and |log2FoldChange| > 1", "n_tested": 29352, "n_significant": 1551, "n_up": 503, "n_down": 1048, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 16831, "n_significant": 2448, "n_up": 1202, "n_down": 1246, "deg_sanity": "ok"}}}}

reasoning: Separate two-group DESeq2 fit, in case the paper fitted each pair alone.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pairwise_HRE_vs_HFD", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\pairwise_HRE_vs_HFD\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\pairwise_HRE_vs_HFD\\DEG_results_HRE_vs_HFD.csv"], "counts": {"pairwise_HRE_vs_HFD": {"applied": {"rule": "pvalue < 0.01 and |log2FoldChange| > 1", "n_tested": 29441, "n_significant": 461, "n_up": 110, "n_down": 351, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 16311, "n_significant": 198, "n_up": 65, "n_down": 133, "deg_sanity": "ok"}}}}

reasoning: Separate two-group DESeq2 fit, in case the paper fitted each pair alone.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2/grp_HAE_vs_HFD", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\enrichment_deseq2_grp_HAE_vs_HFD\\ora_up\\DEG_results_grp_HAE_vs_HFD_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\enrichment_deseq2_grp_HAE_vs_HFD\\ora_up\\DEG_results_grp_HAE_vs_HFD_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\enrichment_deseq2_grp_HAE_vs_HFD\\ora_up\\DEG_results_grp_HAE_vs_HFD_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\enrichment_deseq2_grp_HAE_vs_HFD\\ora_up\\DEG_results_grp_HAE_vs_HFD_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 420 Mouse genes (direction=up, pvalue<0.01, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cellular Response To Growth Factor Stimulus (GO:0071363) | padj=2.72e-01 | overlap=11/155 | genes=TMEM ... [1236 more characters]

reasoning: Paper reports KEGG terms for genes up in HAE vs HFD (Fig. 6H).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2/grp_HAE_vs_HFD", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\enrichment_deseq2_grp_HAE_vs_HFD\\gsea\\DEG_results_grp_HAE_vs_HFD_GSEA_Hallmark.csv"], "summary": "GSEA complete on 31348 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 42 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_PROTEIN_SECRETION | NES=2.77 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_BILE_ACID_METABOLISM | NES=2.44 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANDROGEN_RESPONSE | NES=2.11 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=2.08 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UV_RESPONSE_DN | NES=2.04 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TGF_BETA_SIGNALING | NES=1.99 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HEME_METABOLISM | NES=1.97 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_PEROXISOME | NES=1.86 | NOM p=0.00e+00 | FDR q=8.51e-04 - HALLMARK_COAGULATION | NES=1.84 | NOM p=0.00e+00 | FDR q=7.66e-04 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=-1.98 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-1.69 | NOM p=1.80e-03 | FDR q=4.45e-03 - HAL ... [401 more characters]

reasoning: Paper reports KEGG terms for genes up in HAE vs HFD (Fig. 6H).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2/grp_HRE_vs_HFD", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\enrichment_deseq2_grp_HRE_vs_HFD\\ora_up\\DEG_results_grp_HRE_vs_HFD_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\enrichment_deseq2_grp_HRE_vs_HFD\\ora_up\\DEG_results_grp_HRE_vs_HFD_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\enrichment_deseq2_grp_HRE_vs_HFD\\ora_up\\DEG_results_grp_HRE_vs_HFD_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\enrichment_deseq2_grp_HRE_vs_HFD\\ora_up\\DEG_results_grp_HRE_vs_HFD_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 120 Mouse genes (direction=up, pvalue<0.01, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Positive Regulation Of Vascular Permeability (GO:0043117) | padj=3.19e-01 | overlap=2/11 | genes=OCLN; ... [1236 more characters]

reasoning: Paper reports KEGG terms for genes up in HRE vs HFD (Fig. 6I).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2/grp_HRE_vs_HFD", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41673803\\GSE286570\\results\\enrichment_deseq2_grp_HRE_vs_HFD\\gsea\\DEG_results_grp_HRE_vs_HFD_GSEA_Hallmark.csv"], "summary": "GSEA complete on 31348 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 36 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_BILE_ACID_METABOLISM | NES=2.37 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_PROTEIN_SECRETION | NES=2.15 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.87 | NOM p=0.00e+00 | FDR q=7.71e-04 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.86 | NOM p=0.00e+00 | FDR q=5.78e-04 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.75 | NOM p=0.00e+00 | FDR q=2.78e-03 - HALLMARK_ANDROGEN_RESPONSE | NES=1.69 | NOM p=0.00e+00 | FDR q=6.17e-03 - HALLMARK_ADIPOGENESIS | NES=1.43 | NOM p=7.44e-03 | FDR q=5.82e-02 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=1.41 | NOM p=5.64e-02 | FDR q=5.87e-02 - HALLMARK_HEME_METABOLISM | NES=1.40 | NOM p=7.71e-03 | FDR q=5.83e-02 - HALLMARK_MYC_TARGETS_V1 | NES=1.40 | NOM p=7.92e-03 | FDR q=5.44e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=-2.62 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-2.22 | NOM p=0 ... [401 more characters]

reasoning: Paper reports KEGG terms for genes up in HRE vs HFD (Fig. 6I).

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["GEO holds 3 livers per group while the paper's animal groups are n=8 (NC n=13); the RNA-seq n is not stated in the text, so 3/group is assumed to be what the paper sequenced", "n=3 per group: DEG counts at raw p < 0.01 are sensitive to the model (joint vs pairwise dispersion)", "threshold text in S4.5.p1 is internally inconsistent ('log2FC < 1'); interpretation recorded"], "results": {"deseq2/grp_HAE_vs_HFD": {"n_deg": 1488, "up": 420, "down": 1068, "rule": "pvalue < 0.01 and |log2FoldChange| > 1", "audit_n": 2082}, "deseq2/grp_HRE_vs_HFD": {"n_deg": 467, "up": 120, "down": 347, "rule": "pvalue < 0.01 and |log2FoldChange| > 1", "audit_n": 183}, "deseq2/grp_NC_vs_HFD": {"n_deg": 2470, "up": 914, "down": 1556, "rule": "pvalue < 0.01 and |log2FoldChange| > 1", "audit_n": 4163}, "deseq2/grp_HAE_vs_HRE": {"n_deg": 253, "up": 66, "down": 187, "rule": "pvalue < 0.01 and |log2FoldChange| > 1", "audit_n": 24}, "pairwise_HAE_vs_HFD": {"n_deg": 1551, "up": 503, "down": 1048, "rule": "pvalue < 0.01 and |log2FoldChange| > 1", "audit_n": 2448}, "pairwise_HRE_vs_HFD": {"n_deg": 461, "up": 110, "down": 351, "rule": "pvalue < 0.01 and |log2FoldChange| > 1", "audit_n": 198}}, "paper_counts": {"deseq2/grp_HAE_vs_HFD": 1450, "deseq2/grp_HRE_vs_HFD": 171, "deseq2/grp_NC_vs_HFD": 2746, "deseq2/grp_HAE_vs_HRE": 625, "pairwise_HAE_vs_HFD": 1450, "pairwise_HRE_vs_HFD": 171}, "comparison": {"deseq2/grp_HAE_vs_HFD": {"ours": 1488, "paper": 1450}, "deseq2/grp_HRE_ ... [1869 more characters]

reasoning: Paper-aligned DESeq2 on the paper's deposited counts and comparisons with the paper's threshold.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample size",
    "paper": "HFD/HAE/HRE n=8, NC n=13 animals (S4.1.1.p1)",
    "data": "GEO: 3 livers per group (NC 2,4,5; HFD 1,2,3; AE 1,2,3; RE 3,4,5)",
    "disposition": "executable_without_change"
  },
  {
    "item": "threshold wording",
    "paper": "'log2FC < 1 and a p-value < 1E-2' (S4.5.p1)",
    "data": "n/a",
    "disposition": "executable_without_change"
  },
  {
    "item": "diet contrast direction",
    "paper": "HFD vs NC",
    "data": "extracted as NC vs HFD from the joint model with HFD reference; |log2FC| and counts are symmetric",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 41673803 / GSE286570

The paper studies NAFLD mice on a high-fat diet (HFD) that did aerobic exercise (HAE) or resistance exercise (HRE). The data are liver RNA-seq: featureCounts raw counts, 12 samples, 3 per group (NC, HFD, HAE, HRE).

## What ran
- Case-spec route (`tools.case_runner execute case_spec.json`). Preflight was skipped as instructed. The run completed and the decision contract validated with 0 execution failures.
- **Gates.**
  - Ownership: DA.p1 names GSE286570. The GEO data_processing text matches S4.5.p1 word for word.
  - Alignment: the matrix columns matched the metadata `title` exactly after key normalization (`H-AE1` = `H-AE-1`), 12/12.
  - Groups: `grp` comes from the treatment characteristic, recoded to NC/HFD/HAE/HRE.
  - Matrix: raw counts, so DESeq2.
  - Covariance: not required, since every sample is an independent male mouse.
- **Primary execution.** One pydeseq2 model, `~ grp`, on all 12 samples, with HFD as the reference. It gave four contrasts:
  - HAE vs HFD and HRE vs HFD: primary, the exercise effect.
  - NC vs HFD: secondary, the diet check, which is the mirror of the paper's HFD vs NC.
  - HAE vs HRE: secondary, the comparison between exercise types.
- **Sensitivity.** Separate two-group DESeq2 fits for HAE vs HFD and HRE vs HFD, because the paper does not say whether it fitted each pair on its own.
- **Enrichment.** ORA on up-regulated genes (Enrichr GO and KEGG) and Hallmark GSEA, for both exercise contrasts.

## Threshold
The paper's threshold (S4.5.p1) is written as "log2FC < 1 and p-value < 1E-2". I read this as **raw p < 0.01 and |log2FC| > 1**. The literal wording cannot be right, because the paper reports both up- and down-regulated DEGs. This rule was applied as the paper's threshold. A second count at BH padj < 0.05 with no fold-change cutoff is kept as an audit.

## DEG counts vs the paper (paper's rule)
| Contrast | Ours (joint model) | Up/Down | Pairwise sensitivity | Paper | Audit (padj<0.05) |
|---|---|---|---|---|---|
| HAE vs HFD | 1488 | 420/1068 | 1551 | 1450 (Fig 6C) | 2082 |
| HRE vs HFD | 467 | 120/347 | 461 | 171 (Fig 6D) | 183 |
| HFD vs NC (run as NC vs HFD) | 2470 | 1556/914 as HFD vs NC | n/a | 2746 (Fig 6B) | 4163 |
| HAE vs HRE | 253 | 66/187 | n/a | 625 (Fig 6E) | 24 |

- **Closely reproduced:** HAE vs HFD and HFD vs NC.
- **Not reproduced:** we find about 2.7x the paper's DEGs for HRE vs HFD, and about 0.4x for HAE vs HRE.
- **Same ordering as the paper:** HAE changes live ... [2457 more characters]
