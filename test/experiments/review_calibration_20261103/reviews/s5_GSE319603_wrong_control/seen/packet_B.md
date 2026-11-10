# Review packet B (the analysis' decisions): GSE319603

## Mechanical flags

- **other_rule_matches_paper**: {"table": "deseq2_joint/grp_HM_vs_C", "paper": 563, "applied": 1182, "applied_rule": "padj < 0.05 and |log2FoldChange| > 0.5", "closest_rule": "pvalue<0.05 & |lfc|>1", "closest_n": 542, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deseq2_joint/grp_HM_vs_C | 563 | 1182 | padj < 0.05 and |log2FoldChange| > 0.5 | 3140 | 866 | 285 | 4161 | 5112 | 1320 | 542 | 3125 | 0.092 | 0.244 |
| deseq2_joint/grp_H_vs_C | 458 | 458 | padj < 0.05 and |log2FoldChange| > 0.5 | 885 | 378 | 157 | 1254 | 2620 | 747 | 352 | 1343 | 0.106 | 0.125 |

## Samples per design level

### `grp`
- **C** (6): GSM9521100 / control1 / Library name: C1; GSM9521101 / control2 / Library name: C2; GSM9521102 / control3 / Library name: C3; GSM9521103 / control4 / Library name: C4; GSM9521104 / control5 / Library name: C5; GSM9521105 / control6 / Library name: C6
- **H** (6): GSM9521106 / high-fat diet1 / Library name: H1; GSM9521107 / high-fat diet2 / Library name: H2; GSM9521108 / high-fat diet3 / Library name: H3; GSM9521109 / high-fat diet4 / Library name: H4; GSM9521110 / high-fat diet5 / Library name: H5; GSM9521111 / high-fat diet6 / Library name: H6
- **HM** (6): GSM9521112 / high-fat diet with MICT intervention1 / Library name: HM1; GSM9521113 / high-fat diet with MICT intervention2 / Library name: HM2; GSM9521114 / high-fat diet with MICT intervention3 / Library name: HM3; GSM9521115 / high-fat diet with MICT intervention4 / Library name: HM4; GSM9521116 / high-fat diet with MICT intervention5 / Library name: HM5; GSM9521117 / high-fat diet with MICT intervention6 / Library name: HM6

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE319603"], "assay": "bulk mRNA-seq (paired-end, Illumina NovaSeq 6000), mouse gastrocnemius muscle (S2.7.p1)", "design_in_paper": "4 groups randomized at 4 weeks of age, n=12/group: chow (C), chow+MICT (CM), HFD (H), HFD+MICT (HM); HFD weeks 1-21; MICT treadmill weeks 14-21, 45 min/day, 5 d/wk (S2.1.p1, S2.2.p1). RNA-seq on n=6/group for C, H, HM only; CM was not sequenced (S2.7.p1, S3.2.p1, FIG3).", "sample_inclusion": "18 GSMs = C1-6, H1-6, HM1-6; no exclusions stated", "factors": {"grp": ["C", "H", "HM"]}, "primary_estimand": "Effect of 8-week MICT on gastrocnemius gene expression in HFD-fed mice: HM vs H (exercise effect under HFD; S3.2.p1, S4.p7-p9). H vs C is the diet (non-exercise) effect reported alongside.", "planned_contrasts": ["HM vs H (S3.2.p1; paper: 563 DEGs, 213 up / 350 down) - exercise contrast", "H vs C (S3.2.p1; paper: 458 DEGs, 295 up / 163 down) - diet contrast, not exercise"], "repeated_measure_unit": "none; one sample per mouse, independent animals", "normalization": "DESeq2 median-of-ratios on featureCounts raw counts (S2.7.p1)", "paper_method": "DESeq2 v1.22.2 on raw counts, BH FDR (S2.7.p1); model scope (all samples vs pairwise subsets) not stated", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false, "source_locator": "S3.2.p1"}, "paper_results": "Table 1/2 top-50 DEGs; MICT downregulates Foxo1, Fbxo32, Trim63, Txnip, Pdk4, Angptl4; minimal change in Pax ... [33 more characters]

reasoning: Methods S2.7.p1 state DESeq2 on raw counts with FDR<0.05; Results S3.2.p1 state the DEG criteria actually used for the reported counts: adjusted P<0.05 and |log2FC| >= 0.5. The Results rule is the one that produced 458/563, so it is the paper threshold; the Methods FDR-only rule is kept as an audit rule. Only C, H, HM were sequenced, so the only exercise contrast available is HM vs H (exercise under HFD); there is no chow exercise (CM) arm in the data.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE319603\\GSE319603_All_gene_counts.csv", "owned": true, "checks": ["S8.p1 names GSE319603 as the RNA-seq deposit", "GEO metadata: 18 male C57BL/6J gastrocnemius samples, 6 each control / high-fat diet / high-fat diet with MICT intervention, matches S2.7.p1 n=6 per group and FIG3 groups C, H, HM", "GEO treatment_protocol text is the paper's S2.2.p1 exercise protocol; data_processing matches S2.7.p1 (Trim-galore, STAR, featureCounts, GRCm38.p6)", "matrix GSE319603_All_gene_counts.csv columns C1-6, H1-6, HM1-6 equal the GEO library names"], "accession": "GSE319603", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE319603\\GSE319603_metadata.csv"}

reasoning: Paper data availability statement S8.p1 names this accession; sample groups, tissue, protocol and processing all match.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 18, "n_metadata": 18, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "E:/agent/mwangLab_review/.review_queue/case_06/run/GSE319603\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "description", "regex": "^Library name: ([A-Z]+)\\d+$"}}, "output": "E:/agent/mwangLab_review/.review_queue/case_06/run/GSE319603\\aligned\\design_metadata.csv", "sha256": "1f6067952918e8a7874dc297f08f44ccaee65fc52ef0061cf3818ec7b347089e", "levels": {"grp": {"C": 6, "H": 6, "HM": 6}}}}

reasoning: inspect alignment_keys: the matrix column names are contained in the description field ('Library name: C1'); derive the exact key from it. Group letters C/H/HM are the library-name prefix, consistent with titles control / high-fat diet / high-fat diet with MICT intervention.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "E:/agent/mwangLab_review/.review_queue/case_06/run/GSE319603\\aligned\\aligned_matrix.csv", "sha256": "fba97030b0b43ed47d532aeea5b76362a1e1f050d68a35f20a82556d797114f1", "n_features": 26166, "n_samples": 18, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3346023.0, "median": 31.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 3.3e6, median 31; GEO data_processing: featureCounts, 'excel file includes raw counts for each sample'; paper S2.7.p1: DESeq2 with raw counts as input. The .csv is the converted copy of the deposited .xlsx; Ensembl IDs are unique, Symbol is an annotation column.

### design (valid, not_started)

final: {"analysis_type": "multi-group (one factor, three levels), planned pairwise contrasts from one model", "design_column": "grp", "contrasts": [{"name": "grp_HM_vs_C", "control": "C", "treatment": "HM", "role": "primary", "note": "exercise effect: exercised mice vs control mice"}, {"name": "grp_H_vs_C", "control": "C", "treatment": "H", "role": "secondary", "note": "diet effect"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "E:/agent/mwangLab_review/.review_queue/case_06/run/GSE319603\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: C is the control group; HM is the exercised group, H the high-fat group (FIG3).

rejected alternatives: [{"value": "HM vs C", "reason_rejected": "not a paper contrast; mixes diet and exercise; can be run only as exploratory"}, {"value": "exercise main effect / diet x exercise interaction", "reason_rejected": "CM arm not sequenced; 2x2 factorial not identifiable from the deposited samples"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 18, "n_columns": 3, "columns": ["Intercept", "grp_H", "grp_HM"], "rank": 3, "full_rank": true, "residual_df": 15, "levels": {"grp": {"C": 6, "H": 6, "HM": 6}}, "cells": [{"cell": ["C"], "n": 6}, {"cell": ["H"], "n": 6}, {"cell": ["HM"], "n": 6}], "min_cell_size": 6, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 18, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 18, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.Sex", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.time point", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.strain", "n_levels": 1, "status": "constant"}, {"column": "treatment_protocol_ch1", "n_levels": 1, "status": "constant"}, {"col ... [1431 more characters]

reasoning: Independent mice randomized to groups (S2.1.p1), one sample per mouse; all male, same tissue and time point; GEO records no batch or lane variable. No blocking unit.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "DESeq2 v1.22.2 (R) on raw counts", "status": "reproduced_with_python_port"}, "deviations": ["pydeseq2 instead of R DESeq2 1.22.2", "Paper does not state whether each comparison was fitted on its two groups only or on all samples; primary fit uses all 18 samples (one model, planned contrasts), pairwise two-group fits run as sensitivity"]}

reasoning: Raw featureCounts integers; paper used DESeq2 on raw counts (S2.7.p1).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper text is adjusted P < 0.05 and |log2FC| >= 0.5 (S3.2.p1); the runner's single inclusive flag cannot express strict-p with inclusive-FC, so |log2FC| > 0.5 is applied (differs only for genes exactly at 0.5). Audit rule = Methods S2.7.p1 FDR < 0.05 without fold-change cutoff."}

reasoning: S3.2.p1 gives the rule used for the reported DEG counts; S2.7.p1 gives FDR<0.05 only and is kept as audit.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2_joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 18, "matrix": "E:/agent/mwangLab_review/.review_queue/case_06/run/GSE319603\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_06/run/GSE319603\\results\\deseq2_joint\\DEG_results_grp_HM_vs_C.csv", "E:/agent/mwangLab_review/.review_queue/case_06/run/GSE319603\\results\\deseq2_joint\\DEG_results_grp_H_vs_C.csv"], "counts": {"deseq2_joint/grp_HM_vs_C": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 14470, "n_significant": 1182, "n_up": 574, "n_down": 608, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14470, "n_significant": 3140, "n_up": 1651, "n_down": 1489, "deg_sanity": "ok"}}, "deseq2_joint/grp_H_vs_C": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 14874, "n_significant": 458, "n_up": 295, "n_down": 163, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14874, "n_significant": 885, "n_up": 551, "n_down": 334, "deg_sanity": "ok"}}}}

reasoning: one model on all 18 samples

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["pydeseq2 vs R DESeq2 1.22.2"], "results": {"deseq2_joint/grp_HM_vs_C": {"n_deg": 1182, "up": 574, "down": 608, "rule": "padj < 0.05 and |log2FoldChange| > 0.5", "audit_n": 3140}, "deseq2_joint/grp_H_vs_C": {"n_deg": 458, "up": 295, "down": 163, "rule": "padj < 0.05 and |log2FoldChange| > 0.5", "audit_n": 885}}, "paper_counts": {"deseq2_joint/grp_HM_vs_C": 563, "deseq2_joint/grp_H_vs_C": 458}, "comparison": {"deseq2_joint/grp_HM_vs_C": {"ours": 1182, "paper": 563}, "deseq2_joint/grp_H_vs_C": {"ours": 458, "paper": 458}}, "paper_gene_check": {"deseq2_joint/grp_HM_vs_C": {"Angptl7": {"baseMean": 3767.977, "log2FoldChange": -1.0006, "padj": 0.0, "pvalue": 0.0}, "Txnip": {"baseMean": 35223.7998, "log2FoldChange": -0.6903, "padj": 0.0, "pvalue": 0.0}, "Pkp4": {"baseMean": 2745.0664, "log2FoldChange": -0.7774, "padj": 0.0, "pvalue": 0.0}, "Fbxo32": {"baseMean": 13279.6206, "log2FoldChange": -0.9939, "padj": 0.0, "pvalue": 0.0}, "Sec14l5": {"baseMean": 828.6847, "log2FoldChange": 0.8665, "padj": 0.0, "pvalue": 0.0}, "Dach1": {"baseMean": 450.6647, "log2FoldChange": 0.6721, "padj": 0.0, "pvalue": 0.0}, "Pdk4": {"baseMean": 57051.3341, "log2FoldChange": -0.5933, "padj": 0.0166, "pvalue": 0.0024}, "Trim63": {"baseMean": 12568.0717, "log2FoldChange": -0.9411, "padj": 0.0003, "pvalue": 0.0}, "Foxo1": {"baseMean": 3295.2428, "log2FoldChange": -0.9778, "padj": 0.0109, "pvalue": 0.0014}, "Angptl4": {"baseMean": 1075.7099, "log2FoldChange": 0.2226, "pad ... [666 more characters]

reasoning: Paper-aligned DESeq2 on the paper's samples and contrasts with the paper's Results threshold. Note C vs H is reported as named by the runner (reference H); the paper's H vs C has the opposite sign, so its up/down counts swap.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 18 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DEG threshold",
    "paper": "Methods S2.7.p1: FDR < 0.05; Results S3.2.p1: adjusted P < 0.05 and |log2FC| >= 0.5",
    "data": "n/a",
    "disposition": "executable_without_change"
  },
  {
    "item": "CM (chow + MICT) arm",
    "paper": "four groups randomized (S2.1.p1), RNA-seq on C, H, HM only (FIG3)",
    "data": "GEO has 18 samples C/H/HM, no CM",
    "disposition": "executable_without_change"
  }
]
