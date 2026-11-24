# Review packet B (the analysis' decisions): GSE164401_HC_RP_vs_CP

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_RP_vs_CP | 1952 | 1999 | pvalue < 0.05 | 280 | 109 | 53 | 442 | 1999 | 408 | 201 | 834 | 0.137 | 0.101 |

## Samples per design level

### `grp`
- **CP** (8): GSM5625033 / HC_CP1; GSM5625034 / HC_CP2; GSM5625035 / HC_CP3; GSM5625036 / HC_CP4; GSM5625037 / HC_CP5; GSM5625038 / HC_CP6; GSM5625039 / HC_CP7; GSM5625040 / HC_CP8
- **RP** (8): GSM5625041 / HC_RP1; GSM5625042 / HC_RP2; GSM5625043 / HC_RP3; GSM5625044 / HC_RP4; GSM5625045 / HC_RP5; GSM5625046 / HC_RP6; GSM5625047 / HC_RP7; GSM5625048 / HC_RP8

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE164401"], "assay": "bulk RNA-seq of whole hippocampus (SMART-seq v4 + Nextera XT, NovaSeq; STAR GeneCounts) (S6.9.p1)", "primary_estimand": "Effect of runner plasma (RP; pooled plasma from male C57BL/6 mice with 28 d voluntary wheel running) versus control plasma (CP; sedentary standard-cage donors) infused retro-orbitally every 3 d for 28 d into young non-running recipients, on the recipient hippocampal transcriptome (S1.p3, S6.3.p1, Fig. 1a,h)", "factors": {"grp": ["CP", "RP"]}, "inclusion": "n = 8 recipient mice per group (FIG12 Fig. 1h legend); male donors and sex/age matched recipients", "planned_contrasts": ["RP vs CP, hippocampus, no LPS (S1.p3, Fig. 1h; paper: 1,952 DEGs, 61% down / 39% up)", "LPS+RP vs LPS+CP, hippocampus (S2.p1, Fig. 2b; separate experiment, case GSE164401_HC_LPS)"], "repeated_measure_unit": "none; one hippocampus per recipient mouse", "paper_method": "DESeq2 v1.32 default (built-in) Wald test, ~ treatment (S6.9.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "FIG12 (Fig. 1h legend: 'Wald tests; P < 0.05')"}, "paper_results": {"RP_vs_CP_DEGs": 1952, "down_fraction": 0.61, "up_fraction": 0.39, "named_down": ["Tns4", "Igsf5", "Ehf"], "named_up": ["Foxo6", "Fam19a2"], "unchanged": ["Clu (S4.p2)"]}}

reasoning: S1.p3 and Fig. 1h define the exercise-plasma estimand on hippocampus with DESeq2 Wald P<0.05 (raw P, no FC rule; n=8/group). The design is a plasma-transfer experiment: recipients did not exercise, so the estimand is the effect of exercise-conditioned plasma, which is the paper's intended exercise comparison. S6.10.p1's padj<0.1 rule applies to the cortex clusterin experiment, not to this one.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\prepped\\GSE164401_HC_RNAseq_RP_vs_CP_clean.csv", "owned": true, "checks": ["DA.p1 names GSE164401 for the bulk RNA-seq", "GSE164401_HC_RNAseq_RP_vs_CP.csv columns CP1-8/RP1-8 match GEO titles HC_CP1-8/HC_RP1-8 (Whole HC, treatment CP/RP)", "16 samples = paper's n=8 per group"], "accession": "GSE164401", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE164401\\GSE164401_metadata.csv"}

reasoning: Series supplementary file deposited by the authors; columns map one-to-one onto the 16 hippocampal CP/RP GSMs.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 16, "n_metadata": 73, "coverage": 0.2192, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM5009111", "GSM5009112", "GSM5009113", "GSM5009114", "GSM5009115", "GSM5009116", "GSM5009117", "GSM5464517", "GSM5464518", "GSM5464519", "GSM5464520", "GSM5464521", "GSM5464522", "GSM5464523", "GSM5464524", "GSM5464525", "GSM5464526", "GSM5464527", "GSM5464528", "GSM5464529", "GSM5464530", "GSM5464531", "GSM5464532", "GSM5464533", "GSM5464534", "GSM5464535", "GSM5625049", "GSM5625050", "GSM5625051", "GSM5625052", "GSM5625053", "GSM5625054", "GSM5625055", "GSM5625056", "GSM5625057", "GSM5625058", "GSM5625059", "GSM5625060", "GSM5625061", "GSM5625062", "GSM5625063", "GSM5625064", "GSM5625065", "GSM5625066", "GSM5625067", "GSM5625068", "GSM5625069", "GSM5625070", "GSM5625071", "GSM5625072", "GSM5625073", "GSM5625074", "GSM5625075", "GSM5625076", "GSM5625077", "GSM5625078", "GSM5625079"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_RP_vs_CP\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^HC_(CP|RP)\\d+$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_RP_vs_CP\\aligned\\design_metadata.csv", "sha256": "8946c8c5409941edbcd5cf417020e907270c4f2484104a25bb4f5871fd6f950e", "levels": {"grp": {"CP": 8, "RP": 8}}}}

reasoning: Matrix column CP1 equals the GEO title HC_CP1 without the HC_ prefix (inspect alignment_keys); group from title, consistent with characteristics treatment CP/RP for these 16 GSMs. Other GSMs (BEC scRNA, cortex, LPS experiment) are not in this matrix. key = title with the HC_ prefix stripped (other titles pass through unchanged and do not match the matrix).

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_RP_vs_CP\\aligned\\aligned_matrix.csv", "sha256": "d4f311dedf2ad570e6c669020866748796953c94ea2e986b58a7b638c6495d96", "n_features": 24384, "n_samples": 16, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 192354.0, "median": 43.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (integer_fraction 1.0), library sums 2.2-37.9 M; data_processing for the 47 HC samples: STAR GeneCounts; paper S6.9.p1 runs DESeq2 on these counts. 27 Excel-mangled date IDs (Mar/Sep genes) dropped by prep script because the original symbols collide (e.g. March1/Marc1).

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "CP", "treatment": "RP", "estimand_type": "causal (randomized plasma infusion)", "contrasts": [{"name": "grp_RP_vs_CP", "control": "CP", "treatment": "RP", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_RP_vs_CP\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Two independent recipient groups, n=8 each (Fig. 1h). Reference CP (control plasma).

rejected alternatives: [{"value": "characteristics_ch1.1.treatment as group column", "reason_rejected": "mislabels all 31 LPS-experiment samples as RP; title is the reliable label"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 16, "n_columns": 2, "columns": ["Intercept", "grp_RP"], "rank": 2, "full_rank": true, "residual_df": 14, "levels": {"grp": {"CP": 8, "RP": 8}}, "cells": [{"cell": ["CP"], "n": 8}, {"cell": ["RP"], "n": 8}], "min_cell_size": 8, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 16, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 16, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.treatment", "n_levels": 2, "status": "complete_confounding", "crosstab": {"CP": {"CP": 8, "RP": 0}, "RP": {"CP": 0, "RP": 8}}}, {"column": "characteristics_ch1.2.cell type", "n_levels": 1, "status": "constant"}, {"column": "molecule_ch1", "n_levels": 1, "status": "constant"}, {"column": "extract_protocol_ch1", "n_levels": 1, "st ... [1586 more characters]

reasoning: Independent recipient mice, one sample each; no batch, sex or litter recorded in GEO; paper model has treatment only.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "DESeq2 v1.32 Wald ~ treatment", "status": "reproduced"}, "deviations": ["pydeseq2 instead of R DESeq2", "27 Excel-mangled gene rows removed"]}

reasoning: Paper's DESeq2 default Wald on raw counts (S6.9.p1). No independent pre-filter stated, so none applied.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "threshold_source": "paper", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: Fig. 1h legend (FIG12): 'Wald tests; P < 0.05' with 1,952 DEGs; raw P kept as stated. BH padj<0.05 reported separately as audit.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_RP_vs_CP", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_RP_vs_CP\\aligned\\aligned_matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_RP_vs_CP\\results\\grp_RP_vs_CP\\DEG_results_RP_vs_CP.csv"], "counts": {"grp_RP_vs_CP": {"applied": {"rule": "pvalue < 0.05", "n_tested": 19883, "n_significant": 1999, "n_up": 759, "n_down": 1240, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 16028, "n_significant": 280, "n_up": 18, "n_down": 262, "deg_sanity": "ok"}}}}

reasoning: Paper's two-group DESeq2 Wald (S6.9.p1, Fig. 1h).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_RP_vs_CP", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34880498\\GSE164401_HC_RP_vs_CP\\results\\enrichment_grp_RP_vs_CP\\gsea\\DEG_results_RP_vs_CP_GSEA_Hallmark.csv"], "summary": "GSEA complete on 19883 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 31 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_PANCREAS_BETA_CELLS | NES=1.28 | NOM p=9.79e-02 | FDR q=5.87e-01 - HALLMARK_PI3K_AKT_MTOR_SIGNALING | NES=1.28 | NOM p=5.32e-02 | FDR q=3.06e-01 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.23 | NOM p=1.62e-01 | FDR q=3.18e-01 - HALLMARK_PROTEIN_SECRETION | NES=1.18 | NOM p=1.40e-01 | FDR q=3.45e-01 - HALLMARK_E2F_TARGETS | NES=1.14 | NOM p=1.37e-01 | FDR q=3.71e-01 - HALLMARK_TGF_BETA_SIGNALING | NES=1.14 | NOM p=2.20e-01 | FDR q=3.12e-01 - HALLMARK_MYC_TARGETS_V1 | NES=1.06 | NOM p=2.88e-01 | FDR q=4.87e-01 - HALLMARK_DNA_REPAIR | NES=0.88 | NOM p=8.19e-01 | FDR q=1.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=0.86 | NOM p=7.45e-01 | FDR q=1.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=0.84 | NOM p=8.97e-01 | FDR q=9.43e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-2.03 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=-2.02 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERF ... [389 more characters]

reasoning: Paper reports downregulated acute inflammatory response (S1.p3); GSEA on the full Wald ranking tests the inflammation direction. ORA skipped: paper's ORA used the top 250 DEGs, not the threshold list.

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Recipients did not exercise: the estimand is the effect of runner plasma, not of running itself.", "Paper's DEG rule is raw P<0.05 without multiple-testing correction; the audit padj count is the stricter figure."], "results": {"grp_RP_vs_CP": {"n_deg": 1999, "up": 759, "down": 1240, "rule": "pvalue < 0.05", "audit_n": 280}}, "paper_counts": {"grp_RP_vs_CP": 1952}, "comparison": {"grp_RP_vs_CP": {"ours": 1999, "paper": 1952}}, "paper_gene_check": {"grp_RP_vs_CP": {"Tns4": {"baseMean": 15.004, "log2FoldChange": -2.6778, "padj": 6.02e-05, "pvalue": 3.75e-09}, "Igsf5": {"baseMean": 8.9252, "log2FoldChange": -2.0111, "padj": 0.000571, "pvalue": 1.07e-07}, "Ehf": {"baseMean": 3.9119, "log2FoldChange": -2.977, "padj": 0.00708, "pvalue": 3.17e-05}, "Foxo6": {"baseMean": 319.3651, "log2FoldChange": 0.2677, "padj": 0.000831, "pvalue": 8.3e-07}, "Fam19a2": {"baseMean": 854.9183, "log2FoldChange": 0.2466, "padj": 0.00985, "pvalue": 5.64e-05}, "Clu": {"baseMean": 13854.9081, "log2FoldChange": -0.1332, "padj": 0.142, "pvalue": 0.00553}}}}

reasoning: Direct reproduction of Fig. 1h.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "GEO treatment annotation",
    "paper": "LPS experiment has SAL+SAL, LPS+SAL, LPS+CP, LPS+RP groups",
    "data": "characteristics_ch1.1.treatment = RP for all 31 LPS-experiment hippocampus GSMs",
    "disposition": "executable_without_change"
  },
  {
    "item": "Excel-mangled gene IDs",
    "paper": "n/a",
    "data": "27 rows named 2019-03-xx / 2019-09-xx (March/Sept genes) with 2 duplicated IDs",
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
