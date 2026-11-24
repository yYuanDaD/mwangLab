# Review packet B (the analysis' decisions): GSE164401_HC_LPS

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/grp_LPSSAL_vs_SALSAL | 4936 | 4709 | pvalue < 0.05 | 2940 | 1035 | 622 | 3665 | 4709 | 1274 | 733 | 3052 | 0.097 | 0.225 |

## Samples per design level

### `grp`
- **LPSCP** (7): GSM5625049 / LPS_CP_L11_1; GSM5625050 / LPS_CP_L11_2; GSM5625051 / LPS_CP_L15_1; GSM5625052 / LPS_CP_L15_2; GSM5625053 / LPS_CP_L3_1; GSM5625054 / LPS_CP_L7_1; GSM5625055 / LPS_CP_L7_2
- **LPSRP** (8): GSM5625056 / LPS_RP_L12_1; GSM5625057 / LPS_RP_L12_2; GSM5625058 / LPS_RP_L16_1; GSM5625059 / LPS_RP_L16_2; GSM5625060 / LPS_RP_L4_1; GSM5625061 / LPS_RP_L4_2; GSM5625062 / LPS_RP_L8_1; GSM5625063 / LPS_RP_L8_2
- **LPSSAL** (8): GSM5625064 / LPS_SAL_L10_1; GSM5625065 / LPS_SAL_L10_2; GSM5625066 / LPS_SAL_L14_1; GSM5625067 / LPS_SAL_L14_2; GSM5625068 / LPS_SAL_L2_1; GSM5625069 / LPS_SAL_L2_2; GSM5625070 / LPS_SAL_L6_1; GSM5625071 / LPS_SAL_L6_2
- **SALSAL** (8): GSM5625072 / SAL_SAL_L13_1; GSM5625073 / SAL_SAL_L13_2; GSM5625074 / SAL_SAL_L1_1; GSM5625075 / SAL_SAL_L1_2; GSM5625076 / SAL_SAL_L5_1; GSM5625077 / SAL_SAL_L5_2; GSM5625078 / SAL_SAL_L9_1; GSM5625079 / SAL_SAL_L9_2

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE164401"], "assay": "bulk RNA-seq of whole hippocampus (S6.9.p1)", "primary_estimand": "Effect of runner plasma versus control plasma on the hippocampal transcriptome of LPS-inoculated mice (LPS+RP vs LPS+CP), read against the LPS effect (LPS+SAL vs SAL+SAL) (S2.p1, Fig. 2a,b)", "factors": {"grp": ["SALSAL", "LPSSAL", "LPSCP", "LPSRP"]}, "inclusion": "SAL+SAL n=8, LPS+SAL n=8, LPS+CP n=7, LPS+RP n=8 (FIG13 Fig. 2b legend)", "planned_contrasts": ["LPS+RP vs LPS+CP (S2.p1, Fig. 2b; count not stated in text, Supplementary Table 4)", "LPS+SAL vs SAL+SAL (S2.p1; paper: 4,936 DEGs; LPS effect, non-exercise reference for the reversal)"], "repeated_measure_unit": "none", "paper_method": "DESeq2 Wald (S6.9.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "FIG13 (Fig. 2b legend: 'Wald test, P < 0.05')"}, "paper_results": {"LPS_DEGs": 4936, "reversal_correlation_r": -0.78, "RP_reduced_genes_qPCR": ["Myd88", "Tlr1", "Tlr2", "Irak3", "Irf9", "Ifngr1", "Stat1", "Stat3", "Gfap"]}}

reasoning: S2.p1 / Fig. 2: RP reverses LPS-induced hippocampal genes (r=-0.78); DESeq2 Wald P<0.05.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\prepped\\GSE164401_HC_RNAseq_LPS_SAL_RP_CP_clean.csv", "owned": true, "checks": ["DA.p1 names GSE164401", "31 columns equal GEO titles of GSM5625049-79 exactly", "group sizes 8/8/7/8 match Fig. 2b legend"], "accession": "GSE164401", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE164401\\GSE164401_metadata.csv"}

reasoning: Author-deposited series file; exact title match for all 31 columns.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 31, "n_metadata": 73, "coverage": 0.4247, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM5009111", "GSM5009112", "GSM5009113", "GSM5009114", "GSM5009115", "GSM5009116", "GSM5009117", "GSM5464517", "GSM5464518", "GSM5464519", "GSM5464520", "GSM5464521", "GSM5464522", "GSM5464523", "GSM5464524", "GSM5464525", "GSM5464526", "GSM5464527", "GSM5464528", "GSM5464529", "GSM5464530", "GSM5464531", "GSM5464532", "GSM5464533", "GSM5464534", "GSM5464535", "GSM5625033", "GSM5625034", "GSM5625035", "GSM5625036", "GSM5625037", "GSM5625038", "GSM5625039", "GSM5625040", "GSM5625041", "GSM5625042", "GSM5625043", "GSM5625044", "GSM5625045", "GSM5625046", "GSM5625047", "GSM5625048"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_LPS\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(SAL_SAL|LPS_SAL|LPS_CP|LPS_RP)_L\\d+_\\d$", "recode": {"SAL_SAL": "SALSAL", "LPS_SAL": "LPSSAL", "LPS_CP": "LPSCP", "LPS_RP": "LPSRP"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_LPS\\aligned\\design_metadata.csv", "sha256": "989f70b77846e784730d949233e04272a38adb5aefff97af0869f877d02dd33c", "levels": {"grp": {"LPSRP": 8, "LPSSAL": 8, "SALSAL": 8, "LPSCP": 7}}}}

reasoning: Exact match of matrix columns to GEO title. Group from title prefix; GEO treatment field is wrong (all 'RP') and is not used. _1/_2 suffix columns are not technical replicates (log-CPM Spearman: a column's nearest neighbour is usually another L index), consistent with the paper counting them as separate mice.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_LPS\\aligned\\aligned_matrix.csv", "sha256": "abf2205aea5354b34937d48eba5042def340729f7ca5c73b24791e85ee3454fa", "n_features": 24384, "n_samples": 31, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 248736.0, "median": 78.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Integer counts (integer_fraction 1.0), library sums 5.5-50.9 M, STAR GeneCounts (data_processing), DESeq2 in paper. Same 27 Excel-mangled rows dropped.

### design (valid, not_started)

final: {"analysis_type": "multi-group, planned contrasts from one model", "formula": "~ grp", "estimand_type": "causal (randomized plasma infusion under LPS)", "contrasts": [{"name": "grp_LPSRP_vs_LPSCP", "control": "LPSCP", "treatment": "LPSRP", "role": "secondary"}, {"name": "grp_LPSSAL_vs_SALSAL", "control": "SALSAL", "treatment": "LPSSAL", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_LPS\\suitability\\suitability.md", "n_comparisons": 7, "n_analyzable": 7}}

reasoning: Four-arm one-way design; the exercise-plasma contrast is LPS+RP vs LPS+CP (CP is the paper's plasma control). LPS vs saline is the paper's reference contrast for the reversal analysis, not an exercise effect. Fitted from one model on all 31 samples.

rejected alternatives: [{"value": "LPS+RP vs LPS+SAL", "reason_rejected": "paper's exercise comparison uses CP as control (Fig. 2b)"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 31, "n_columns": 4, "columns": ["Intercept", "grp_LPSRP", "grp_LPSSAL", "grp_SALSAL"], "rank": 4, "full_rank": true, "residual_df": 27, "levels": {"grp": {"LPSRP": 8, "LPSSAL": 8, "SALSAL": 8, "LPSCP": 7}}, "cells": [{"cell": ["LPSCP"], "n": 7}, {"cell": ["LPSRP"], "n": 8}, {"cell": ["LPSSAL"], "n": 8}, {"cell": ["SALSAL"], "n": 8}], "min_cell_size": 7, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 31, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 31, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.treatment", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.cell type", "n_levels": 1, "status": "constant"}, {"column": "molecule_ch1", "n_levels": 1, "status": "constant"}, {" ... [1571 more characters]

reasoning: The L index (L1-L16) in titles is nested within group (each L belongs to one arm), so it cannot be adjusted for as a fixed effect without absorbing the treatment; the paper does not model it. Independent mice treated as units. (Not passed to the confounding report because it is not a metadata column; nesting checked by hand from titles: L1,5,9,13=SAL+SAL; L2,6,10,14=LPS+SAL; L3,7,11,15=LPS+CP; L4,8,12,16=LPS+RP.)

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald, joint model)", "formula": "~ grp", "paper_route": {"method": "DESeq2 Wald", "status": "reproduced"}, "deviations": ["pydeseq2; one dispersion fit across all four arms (paper likely did the same with a 4-level factor; not stated)", "27 Excel-mangled gene rows removed"]}

reasoning: Raw counts, paper DESeq2 Wald.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "threshold_source": "paper", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: Fig. 2b legend: Wald test, P < 0.05.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "secondary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 31, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_LPS\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_LPS\\results\\joint\\DEG_results_grp_LPSRP_vs_LPSCP.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_LPS\\results\\joint\\DEG_results_grp_LPSSAL_vs_SALSAL.csv"], "counts": {"joint/grp_LPSRP_vs_LPSCP": {"applied": {"rule": "pvalue < 0.05", "n_tested": 20907, "n_significant": 1395, "n_up": 533, "n_down": 862, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 20907, "n_significant": 3, "n_up": 1, "n_down": 2, "deg_sanity": "ok"}}, "joint/grp_LPSSAL_vs_SALSAL": {"applied": {"rule": "pvalue < 0.05", "n_tested": 20907, "n_significant": 4709, "n_up": 2420, "n_down": 2289, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17664, "n_significant": 2940, "n_up": 1663, "n_down": 1277, "deg_sanity": "ok"}}}}

reasoning: Both planned contrasts from one DESeq2 model on all four arms.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_LPSRP_vs_LPSCP", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_LPS\\results\\enrichment_joint_grp_LPSRP_vs_LPSCP\\gsea\\DEG_results_grp_LPSRP_vs_LPSCP_GSEA_Hallmark.csv"], "summary": "GSEA complete on 20907 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 38 significant at FDR q < 0.25. ### Top 8 UP (NES > 0, enriched in treatment): - HALLMARK_HEDGEHOG_SIGNALING | NES=1.64 | NOM p=9.50e-03 | FDR q=1.47e-02 - HALLMARK_KRAS_SIGNALING_DN | NES=1.53 | NOM p=0.00e+00 | FDR q=2.03e-02 - HALLMARK_MYOGENESIS | NES=1.16 | NOM p=1.15e-01 | FDR q=4.04e-01 - HALLMARK_MITOTIC_SPINDLE | NES=1.07 | NOM p=2.80e-01 | FDR q=5.88e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=0.98 | NOM p=4.77e-01 | FDR q=7.85e-01 - HALLMARK_PANCREAS_BETA_CELLS | NES=0.95 | NOM p=5.48e-01 | FDR q=7.86e-01 - HALLMARK_HEME_METABOLISM | NES=0.94 | NOM p=6.76e-01 | FDR q=7.15e-01 - HALLMARK_SPERMATOGENESIS | NES=0.88 | NOM p=7.37e-01 | FDR q=7.69e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=-3.05 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-2.84 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=-2.78 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-2.7 ... [418 more characters]

reasoning: Paper: RP reduces cytokine/innate immune pathways under LPS (S2.p1).

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["LPS+SAL vs SAL+SAL is the LPS effect, reported only as the paper's reference for reversal, not as an exercise effect.", "Paper does not state the LPS+RP vs LPS+CP DEG count in the text."], "results": {"joint/grp_LPSRP_vs_LPSCP": {"n_deg": 1395, "up": 533, "down": 862, "rule": "pvalue < 0.05", "audit_n": 3}, "joint/grp_LPSSAL_vs_SALSAL": {"n_deg": 4709, "up": 2420, "down": 2289, "rule": "pvalue < 0.05", "audit_n": 2940}}, "paper_counts": {"joint/grp_LPSSAL_vs_SALSAL": 4936}, "comparison": {"joint/grp_LPSSAL_vs_SALSAL": {"ours": 4709, "paper": 4936}}, "paper_gene_check": {"joint/grp_LPSRP_vs_LPSCP": {"Myd88": {"baseMean": 235.4116, "log2FoldChange": -0.5041, "padj": 0.135, "pvalue": 0.00028}, "Tlr1": {"baseMean": 34.0187, "log2FoldChange": -0.8108, "padj": 0.336, "pvalue": 0.00389}, "Tlr2": {"baseMean": 127.8578, "log2FoldChange": -1.5306, "padj": 0.118, "pvalue": 8.64e-05}, "Irak3": {"baseMean": 80.1162, "log2FoldChange": -0.6226, "padj": 0.268, "pvalue": 0.00212}, "Irf9": {"baseMean": 386.0699, "log2FoldChange": -0.4695, "padj": 0.121, "pvalue": 0.000144}, "Ifngr1": {"baseMean": 480.2428, "log2FoldChange": -0.0607, "padj": 0.999, "pvalue": 0.331}, "Stat1": {"baseMean": 978.4749, "log2FoldChange": -0.3184, "padj": 0.27, "pvalue": 0.00216}, "Stat3": {"baseMean": 2557.7853, "log2FoldChange": -0.2871, "padj": 0.695, "pvalue": 0.0364}, "Gfap": {"baseMean": 22059.9368, "log2FoldChange": -0.3686, "padj": 0.416, "pvalue": 0.00661}}}}

reasoning: Reproduction of Fig. 2b contrasts.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 31 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "GEO treatment annotation",
    "paper": "four arms SAL+SAL / LPS+SAL / LPS+CP / LPS+RP",
    "data": "characteristics treatment = RP for all 31 samples; titles carry the true arm",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 34880498 / GSE164401

Paper: *Exercise plasma boosts memory and dampens brain inflammation via clusterin* (PMC9721468).
Status: **finished**. The spec is `case_spec.json`, the records are written by `tools.case_runner execute`, and the contract validator reported 22 records with 0 errors.

## Estimand
This is a plasma-transfer design. Plasma was pooled from male mice that ran on a wheel for 28 d (runner plasma, RP) or from sedentary mice (control plasma, CP). It was infused into young recipients that did not exercise. The exercise comparison the paper intends is RP vs CP, measured in the recipients' hippocampus (S1.p3, Fig. 1h). The result is the effect of exercise-conditioned plasma, not of running itself. That caveat is recorded in the study gate.

## What ran
| Case | Matrix | Model | Contrast | Role |
|---|---|---|---|---|
| GSE164401_HC_RP_vs_CP | `GSE164401_HC_RNAseq_RP_vs_CP.csv` (16 samples, STAR GeneCounts raw counts) | pydeseq2 Wald `~ grp` | RP vs CP | primary, paper_aligned |
| GSE164401_HC_LPS | `GSE164401_HC_RNAseq_LPS_SAL_RP_CP.csv` (31 samples) | one pydeseq2 Wald model `~ grp`, 4 arms | LPS+RP vs LPS+CP | secondary (exercise plasma under LPS) |
| | | | LPS+SAL vs SAL+SAL | secondary (the paper's LPS reference, not an exercise effect) |

Enrichment: GSEA (MSigDB Hallmark, Wald stat ranking) on both RP contrasts. ORA was not run, because the paper's GO analysis used the top 250 or 500 DEGs, not a threshold list.

## Threshold
The paper's rule is DESeq2 Wald **raw P < 0.05 with no fold-change cutoff** (Fig. 1h and Fig. 2b legends), and that is what was applied. The audit rule, BH padj < 0.05, is reported separately. The padj < 0.1 rule in S6.10.p1 covers only the cortex clusterin experiment, so it was not used.

## DEG counts vs paper (raw P < 0.05)
| Contrast | Ours (up/down) | Paper | Audit padj<0.05 |
|---|---|---|---|
| RP vs CP (Fig. 1h) | **1,999** (759 up / 1,240 down = 38% / 62%) | **1,952** (39% / 61%) | 280 |
| LPS+SAL vs SAL+SAL | **4,709** | **4,936** | 2,940 |
| LPS+RP vs LPS+CP | 1,395 (533 / 862) | not stated in text (Supp. Table 4) | 3 |

Gene checks:
- **RP vs CP:** the genes the paper names all go in the stated direction. Tns4, Igsf5 and Ehf are down; Foxo6 and Fam19a2 are up (all P < 1e-4). The paper says Clu does not change with RP; here it has raw P = 0.0055 but padj = 0.14 and log2FC −0.13, so it is a marginal hit under the paper's raw-P rule.
- **LPS+RP vs LPS+CP:** all 9 qPCR-validated genes are down. ... [2708 more characters]
