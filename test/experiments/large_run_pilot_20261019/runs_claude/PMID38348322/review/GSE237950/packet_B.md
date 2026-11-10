# Review packet B (the analysis' decisions): GSE237950

## Mechanical flags

- none

## Samples per design level

### `grp`
- **C** (6): GSM7656821 / FC1 (fat normoxia quiet1); GSM7656822 / FC2 (fat normoxia quiet2); GSM7656823 / FC3 (fat normoxia quiet3); GSM7656832 / MC1 (muscle normoxia quiet1); GSM7656833 / MC2 (muscle normoxia quiet2); GSM7656834 / MC3 (muscle normoxia quiet3)
- **CE** (6): GSM7656816 / FCE1 (fat normoxia exercise1); GSM7656817 / FCE2 (fat normoxia exercise2); GSM7656818 / FCE3 (fat normoxia exercise3); GSM7656826 / MCE1 (muscle normoxia exercise1); GSM7656827 / MCE2 (muscle normoxia exercise2); GSM7656828 / MCE3 (muscle normoxia exercise3)
- **H** (5): GSM7656824 / FH1 (fat hypoxic quiet1); GSM7656825 / FH3 (fat hypoxic quiet3); GSM7656835 / MH1 (muscle hypoxic quiet1); GSM7656836 / MH2 (muscle hypoxic quiet2); GSM7656837 / MH3 (muscle hypoxic quiet3)
- **HE** (5): GSM7656819 / FHE2 (fat hypoxia exercise2); GSM7656820 / FHE3 (fat hypoxia exercise3); GSM7656829 / MHE1 (muscle hypoxia exercise1); GSM7656830 / MHE2 (muscle hypoxia exercise2); GSM7656831 / MHE3 (muscle hypoxia exercise3)

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE237950"], "assay": "bulk RNA-seq (Illumina HiSeq), HISAT2 to Ensembl release-99 rat genome (S4.2.p2-p4)", "organism": "Rat (male Sprague Dawley, high-fat diet obese model; S4.1.p1)", "tissues": ["epididymal adipose tissue (F)", "gastrocnemius muscle (M)"], "factors": {"oxygen": ["normoxia (21% O2)", "hypoxia (13.6% O2)"], "exercise": ["quiet", "treadmill 1 h/d, 5 d/wk, 4 wk"]}, "groups": "FC 3, FCE 3, FH 2, FHE 2, MC 3, MCE 3, MH 3, MHE 3 (TAB1, S3.p1, TAB2)", "sample_inclusion": "22 samples; two adipose samples excluded for RNA quality (S4.1.p1); FH2 and FHE1 absent (TAB2)", "primary_estimand": "Effect of 4-week treadmill exercise on gene expression within each tissue, under normoxia (CE vs C) and under hypoxia (HE vs H)", "planned_contrasts": ["Adipose: FCE vs FC (normoxia exercise effect; no DEG count reported)", "Adipose: FHE vs FH (hypoxia exercise effect; no DEG count reported)", "Muscle: MCE vs MC (normoxia exercise effect; no DEG count reported)", "Muscle: MHE vs MH (hypoxia exercise effect; no DEG count reported)"], "repeated_measure_unit": "none within a tissue; muscle and adipose may come from the same rats but pairing is not given", "paper_method": "DESeq on read counts (ABS.p1); comparisons not enumerated", "paper_threshold": {"metric": "not stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "none (data article: ABS.p1, S3.p1 name DE analysis but give no rule)"}, "paper_results": "No DEG counts, gene lists ... [106 more characters]

reasoning: Data in Brief article. ABS.p1 says differential expression used DESeq on raw data; S4.1.p1/S4.1.p2 define a 2x2 oxygen x exercise design in obese rats; TAB2 maps GSM ids to sample names. The paper does not list contrasts, a threshold or results, so the exercise contrasts within oxygen level and tissue are the natural reading of 'how exercise affects gene expression' (S1.p1 bullets 2-3).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE237950\\GSE237950_gene_expression.csv", "owned": true, "checks": ["ABS.p1/TAB1/S3.p1 name GSE237950", "TAB2 GSM7656816-GSM7656837 equal the 22 metadata rows", "matrix columns Count (FC1)...Count (MHE3) carry the 22 TAB2 sample names"], "accession": "GSE237950", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE237950\\GSE237950_metadata.csv"}

reasoning: The series and its only supplementary matrix (gene_expression.xlsx/csv) belong to the paper; sample names match TAB2 exactly.

### alignment (valid, not_started)

final: {"method": "exact:sid", "n_aligned": 22, "n_metadata": 22, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^[FM](CE|HE|C|H)\\d"}, "tissue": {"source": "title", "regex": "^([FM])", "recode": {"F": "fat", "M": "muscle"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\aligned\\design_metadata.csv", "sha256": "33d114b2c4189181b80bd20ba9c7e67eddc1f09d3f735163f0d21f4aebaeadbb", "levels": {"grp": {"CE": 6, "C": 6, "HE": 5, "H": 5}, "tissue": {"muscle": 12, "fat": 10}}}}

reasoning: The matrix holds Count/TPM/FPKM per sample; only the 'Count (X)' columns are used. Sample key = sample name before the parenthesis in title (e.g. FCE1), matched exactly to the Count column name. grp = C/CE/H/HE from the name (S3.p2 defines C, CE, H, HE); tissue from the F/M prefix, cross-checked against characteristics tissue.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\aligned\\aligned_matrix.csv", "sha256": "92dbbea547ec9da79103e477cf96aa64bc56c249a948c8e726d6bd9e0b1c3655", "n_features": 32623, "n_samples": 22, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 15590411.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: The 22 'Count (...)' columns are all integers with library sums 27-44 M, consistent with exon read numbers in TAB3; TPM and FPKM columns are separate and ignored. ABS.p1 and S4.2.p4 state read-count based DE (DESeq).

### design (valid, not_started)

final: {"analysis_type": "multi-group within tissue strata (4 oxygen x exercise groups), planned exercise contrasts", "design_column": "grp", "contrasts": [{"name": "fat_CE_vs_C", "control": "C", "treatment": "CE", "stratum": "fat", "role": "primary"}, {"name": "fat_HE_vs_H", "control": "H", "treatment": "HE", "stratum": "fat", "role": "primary"}, {"name": "muscle_CE_vs_C", "control": "C", "treatment": "CE", "stratum": "muscle", "role": "primary"}, {"name": "muscle_HE_vs_H", "control": "H", "treatment": "HE", "stratum": "muscle", "role": "primary"}, {"name": "fat_H_vs_C / fat_HE_vs_CE / muscle_H_vs_C / muscle_HE_vs_CE", "role": "exploratory"}], "suitability": {"verdict": "partially_analyzable", "failed": [], "warnings": ["sample_size"], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\suitability\\suitability.md", "n_comparisons": 12, "n_analyzable": 7}}

reasoning: The estimand is the exercise effect; the paper's four groups per tissue are kept as one 4-level factor fitted per tissue (tissues are different biology and possibly the same rats, so comparisons never cross tissue). Exercise is compared with the quiet group at the same oxygen level. Adipose hypoxia arms have n=2 (FH, FHE), so those contrasts are small-n and labelled exploratory-strength evidence. Oxygen effects and HE vs CE are exploratory. A 2x2 interaction model was rejected because the paper poses no interaction question and the adipose hypoxia cells have n=2.

rejected alternatives: [{"value": "pool tissues with tissue as covariate", "reason_rejected": "tissue differences dominate and adipose/muscle may be the same animals (unrecorded pairing); per-tissue fits match the paper's tissue-specific framing"}, {"value": "exercise main effect pooled over oxygen", "reason_rejected": "the paper treats normoxia and hypoxia exercise as separate interventions to compare (S1.p1)"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 22, "n_columns": 4, "columns": ["Intercept", "grp_CE", "grp_H", "grp_HE"], "rank": 4, "full_rank": true, "residual_df": 18, "levels": {"grp": {"CE": 6, "C": 6, "HE": 5, "H": 5}}, "cells": [{"cell": ["C"], "n": 6}, {"cell": ["CE"], "n": 6}, {"cell": ["H"], "n": 5}, {"cell": ["HE"], "n": 5}], "min_cell_size": 5, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 22, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 22, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 2, "status": "crossed", "crosstab": {"C": {"epididymal adipose tissue": 3, "gastrocnemius muscle": 3}, "CE": {"epididymal adipose tissue": 3, "gastrocnemius muscle": 3}, "H": {"epididymal adipose tissue": 2, "gastrocnemius muscle": 3}, "HE": {"epididymal adipose tissue": 2, "gastrocnemius muscle": 3}}}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"},  ... [3057 more characters]

reasoning: Within a tissue each sample is a different rat (randomized to groups, S4.1.p1); no batch, sex (all male) or other covariate recorded. Cross-tissue pairing is irrelevant because tissues are fitted separately.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq (R, original package) nbinomTest", "formula": "nbinomTest by grp, fitted per tissue (4 groups)", "paper_route": {"method": "DESeq", "status": "reproduced", "reason": "ABS.p1 names DESeq; the original package (1.38.0) runs here. Dispersion settings and whether all four groups were fitted together are not stated; package defaults (pooled, maximum, parametric) on the four groups of one tissue."}, "deviations": ["DESeq dispersion options and fitting set not stated by the paper; defaults used", "DESeq2 joint model per tissue run as sensitivity"]}

reasoning: Raw integer counts support the paper's named method. DESeq2 (pydeseq2) per tissue is a sensitivity analysis because many vendors say 'DESeq' when running DESeq2.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "not stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "deviation_note": "The paper gives no DEG rule; workflow default BH padj < 0.05 without fold-change cutoff; audit adds |log2FC| > 1."}

reasoning: No threshold anywhere in the paper (ABS.p1, S3, S4).

### execution (valid, completed)

final: {"method": "run_r_de", "subset": "fat_deseq1", "role": "primary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\fat_deseq1\\input\\matrix.csv", "formula": "nbinomTest by grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\fat_deseq1\\DEG_results_fat_CE_vs_C.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\fat_deseq1\\DEG_results_fat_HE_vs_H.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\fat_deseq1\\DEG_results_fat_H_vs_C.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\fat_deseq1\\DEG_results_fat_HE_vs_CE.csv"], "counts": {"fat_deseq1/fat_CE_vs_C": {"applied": {"rule": "padj < 0.05", "n_tested": 21556, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 21556, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}}, "fat_deseq1/fat_HE_vs_H": {"applied": {"rule": "padj < 0.05", "n_tested": 20948, "n_significant": 31, "n_up": 20, "n_down": 11, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 20948, "n_significant": 31, "n_up": 20, "n_down": 11, "deg_sanity": "ok"}}, "fat_deseq1/fat_H_vs_C": {"applied": {"rule": "padj < 0.05", "n_t ... [519 more characters]

reasoning: Paper's DESeq on adipose samples; CE vs C and HE vs H are the planned exercise contrasts, H vs C and HE vs CE exploratory.

### execution (valid, completed)

final: {"method": "run_r_de", "subset": "muscle_deseq1", "role": "primary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\muscle_deseq1\\input\\matrix.csv", "formula": "nbinomTest by grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\muscle_deseq1\\DEG_results_muscle_CE_vs_C.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\muscle_deseq1\\DEG_results_muscle_HE_vs_H.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\muscle_deseq1\\DEG_results_muscle_H_vs_C.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\muscle_deseq1\\DEG_results_muscle_HE_vs_CE.csv"], "counts": {"muscle_deseq1/muscle_CE_vs_C": {"applied": {"rule": "padj < 0.05", "n_tested": 17198, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 17198, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}}, "muscle_deseq1/muscle_HE_vs_H": {"applied": {"rule": "padj < 0.05", "n_tested": 17573, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 17573, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}}, "muscle_deseq1/muscle_H_vs_C" ... [561 more characters]

reasoning: Paper's DESeq on gastrocnemius samples; same contrasts.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "fat_deseq2", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\fat_deseq2\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\fat_deseq2\\DEG_results_grp_CE_vs_C_tissue-fat.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\fat_deseq2\\DEG_results_grp_HE_vs_H_tissue-fat.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\fat_deseq2\\DEG_results_grp_H_vs_C_tissue-fat.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\fat_deseq2\\DEG_results_grp_HE_vs_CE_tissue-fat.csv"], "counts": {"fat_deseq2/grp_CE_vs_C_tissue-fat": {"applied": {"rule": "padj < 0.05", "n_tested": 17419, "n_significant": 56, "n_up": 38, "n_down": 18, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 17419, "n_significant": 51, "n_up": 37, "n_down": 14, "deg_sanity": "ok"}}, "fat_deseq2/grp_HE_vs_H_tissue-fat": {"applied": {"rule": "padj < 0.05", "n_tested": 14851, "n_significant": 939, "n_up": 421, "n_down": 518, "deg_sanity": "tiny_n_per_group=2"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 14851, "n_significant": 834, "n_up": ... [694 more characters]

reasoning: DESeq2 Wald on all four adipose groups as a sensitivity check of the DESeq route.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "muscle_deseq2", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\muscle_deseq2\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\muscle_deseq2\\DEG_results_grp_CE_vs_C_tissue-muscle.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\muscle_deseq2\\DEG_results_grp_HE_vs_H_tissue-muscle.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\muscle_deseq2\\DEG_results_grp_H_vs_C_tissue-muscle.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38348322\\GSE237950\\results\\muscle_deseq2\\DEG_results_grp_HE_vs_CE_tissue-muscle.csv"], "counts": {"muscle_deseq2/grp_CE_vs_C_tissue-muscle": {"applied": {"rule": "padj < 0.05", "n_tested": 18458, "n_significant": 4, "n_up": 4, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 18458, "n_significant": 4, "n_up": 4, "n_down": 0, "deg_sanity": "ok"}}, "muscle_deseq2/grp_HE_vs_H_tissue-muscle": {"applied": {"rule": "padj < 0.05", "n_tested": 18458, "n_significant": 5, "n_up": 4, "n_down": 1, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 18458, "n_significant" ... [670 more characters]

reasoning: DESeq2 Wald on all four muscle groups as a sensitivity check.

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["The paper reports no DEG counts, genes or pathways, so nothing can be compared with its results.", "Adipose hypoxia arms (FH, FHE) have n=2; fat_HE_vs_H has little power.", "Threshold is the workflow default, not the paper's (none stated)."], "results": {"fat_deseq1/fat_CE_vs_C": {"n_deg": 1, "up": 1, "down": 0, "rule": "padj < 0.05", "audit_n": 1}, "fat_deseq1/fat_HE_vs_H": {"n_deg": 31, "up": 20, "down": 11, "rule": "padj < 0.05", "audit_n": 31}, "fat_deseq1/fat_H_vs_C": {"n_deg": 8, "up": 5, "down": 3, "rule": "padj < 0.05", "audit_n": 8}, "fat_deseq1/fat_HE_vs_CE": {"n_deg": 26, "up": 16, "down": 10, "rule": "padj < 0.05", "audit_n": 26}, "muscle_deseq1/muscle_CE_vs_C": {"n_deg": 1, "up": 1, "down": 0, "rule": "padj < 0.05", "audit_n": 1}, "muscle_deseq1/muscle_HE_vs_H": {"n_deg": 1, "up": 1, "down": 0, "rule": "padj < 0.05", "audit_n": 1}, "muscle_deseq1/muscle_H_vs_C": {"n_deg": 8, "up": 6, "down": 2, "rule": "padj < 0.05", "audit_n": 8}, "muscle_deseq1/muscle_HE_vs_CE": {"n_deg": 3, "up": 0, "down": 3, "rule": "padj < 0.05", "audit_n": 3}, "fat_deseq2/grp_CE_vs_C_tissue-fat": {"n_deg": 56, "up": 38, "down": 18, "rule": "padj < 0.05", "audit_n": 51}, "fat_deseq2/grp_HE_vs_H_tissue-fat": {"n_deg": 939, "up": 421, "down": 518, "rule": "padj < 0.05", "audit_n": 834}, "fat_deseq2/grp_H_vs_C_tissue-fat": {"n_deg": 115, "up": 52, "down": 63, "rule": "padj < 0.05", "audit_n": 94}, "fat_deseq2/grp_HE_vs_CE_tissue-fat": {"n_deg": 444, "up" ... [585 more characters]

reasoning: Method and contrasts follow the paper's stated DESeq analysis of its four-group design; the result side has no paper benchmark.

## Suitability report lines (sex, confounding, warnings)

- Verdict: **partially_analyzable**; check: sample_size
- | Check | Status | Detail |
- | Sample size | partial | 7/12 comparisons have >= 3 per group |
- | Sex | no_markers | Sex inference completed on 22 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "fat group sizes",
    "paper": "S4.1.p1 says 40 rats randomized, 24 met criteria, 22 sequenced",
    "data": "22 samples are 10 adipose + 12 muscle, not 22 rats; FH2 and FHE1 missing",
    "disposition": "executable_without_change"
  },
  {
    "item": "contrasts and threshold",
    "paper": "DESeq named, no contrasts/threshold/results",
    "data": "4 groups per tissue",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID38348322 / GSE237950

## What ran
- Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Validator: 13 records, 0 errors. Run status completed. The first attempt is in `_previous/20261110T124831Z`.
- Paper (Data in Brief, PMC10859296): male SD rats on a high-fat diet, 2x2 design (normoxia/hypoxia x quiet/treadmill exercise), with epididymal adipose (F) and gastrocnemius (M) samples. The groups are FC 3, FCE 3, FH 2, FHE 2, MC 3, MCE 3, MH 3, MHE 3 (TAB2). The paper names "DESeq" (ABS.p1). It lists no contrasts, no DEG threshold and no DEG results.
- Matrix: `GSE237950_gene_expression.csv`. Only the 22 integer `Count (X)` columns are used; the TPM and FPKM columns are ignored. Alignment is exact on the sample name taken from `title` (22/22).
- Design: a 4-level `grp` factor (C, CE, H, HE), fitted separately for each tissue (`tissue` stratum). Planned exercise contrasts are CE vs C and HE vs H in each tissue. H vs C and HE vs CE are exploratory.
- Primary method: the original DESeq package (R, 1.38.0), nbinomTest. One fit per tissue on all 4 groups, with defaults pooled/maximum/parametric.
- Sensitivity: pydeseq2 joint model per tissue (`tools.joint_contrasts:run_joint_deseq2`). The small-n adipose hypoxia contrasts (n=2) are included and labelled exploratory.
- Threshold: the paper states none, so the workflow default applies: BH padj < 0.05 with no fold-change cutoff. The audit rule adds |log2FC| > 1.
- Enrichment: not run, because the paper reports no pathway results to compare against.

## DEG counts (padj < 0.05; the paper reports no counts)
| Contrast | DESeq (primary) | DESeq2 (sensitivity) |
|---|---|---|
| fat CE vs C | 1 | 56 |
| fat HE vs H (n=2 vs 2) | 31 | 939 |
| muscle CE vs C | 1 | 4 |
| muscle HE vs H | 1 | 5 |
| fat H vs C (expl.) | 8 | 115 |
| fat HE vs CE (expl.) | 26 | 444 |
| muscle H vs C (expl.) | 8 | 104 |
| muscle HE vs CE (expl.) | 3 | 13 |

The paper gives no benchmark for any contrast. DESeq v1 (pooled dispersion, maximum sharing) is far more conservative than DESeq2. The paper's actual software may well have been DESeq2: vendors often write "DESeq" for it.

## Deviations
- The paper does not state DESeq dispersion options or the set of samples fitted together, so package defaults were used on the four groups of each tissue.
- The adipose hypoxia arms have n=2, so fat HE vs H, fat H vs C and fat HE vs CE are small-n results.
- Paper inconsistency: S4.1.p1 speaks of 22 rats, but the data are  ... [733 more characters]
