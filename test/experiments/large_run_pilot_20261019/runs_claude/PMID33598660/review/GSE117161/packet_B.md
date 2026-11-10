# Review packet B (the analysis' decisions): GSE117161

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.1.time level", "across": "characteristics_ch1.1.time", "pairs_or_sets": 9, "samples_linked": 18, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Samples per design level

### `run`
- **Basal** (6): GSM3272710 / Basal_Early_A; GSM3272711 / Basal_Early_B; GSM3272712 / Basal_Early_C; GSM3272713 / Basal_Late_A; GSM3272714 / Basal_Late_B; GSM3272715 / Basal_Late_C
- **High** (6): GSM3272716 / High_Early_A; GSM3272717 / High_Early_B; GSM3272718 / High_Early_C; GSM3272719 / High_Late_A; GSM3272720 / High_Late_B; GSM3272721 / High_Late_C
- **Moderate** (6): GSM3272722 / Moderate_Early_A; GSM3272723 / Moderate_Early_B; GSM3272724 / Moderate_Early_C; GSM3272725 / Moderate_Late_A; GSM3272726 / Moderate_Late_B; GSM3272727 / Moderate_Late_C

### `time`
- **ZT14** (9): GSM3272710 / Basal_Early_A; GSM3272711 / Basal_Early_B; GSM3272712 / Basal_Early_C; GSM3272716 / High_Early_A; GSM3272717 / High_Early_B; GSM3272718 / High_Early_C; GSM3272722 / Moderate_Early_A; GSM3272723 / Moderate_Early_B; GSM3272724 / Moderate_Early_C
- **ZT22** (9): GSM3272713 / Basal_Late_A; GSM3272714 / Basal_Late_B; GSM3272715 / Basal_Late_C; GSM3272719 / High_Late_A; GSM3272720 / High_Late_B; GSM3272721 / High_Late_C; GSM3272725 / Moderate_Late_A; GSM3272726 / Moderate_Late_B; GSM3272727 / Moderate_Late_C

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE117161"], "paper_type": "STAR Protocols method paper; the transcriptome data come from the companion study Ezagouri et al. 2019 (S1.1.p2, S7.3.p2). No DE analysis, method, threshold or DEG count is reported in this article.", "primary_estimand": "Effect of a moderate-intensity treadmill run versus the sedentary (basal) condition on gastrocnemius gene expression, evaluated separately at the two active-phase times of day the protocol compares, ZT14 (early) and ZT22 (late) (S3.3.p2, S4.p1, FIG4).", "factors": {"running protocol": ["Basal (sedentary)", "Moderate", "High"], "time of day": ["ZT14 (Early)", "ZT22 (Late)"]}, "inclusion": "C57BL/6J males, 3 months old, gastrocnemius (S4.p1, S3.3; GEO source_name). All 18 deposited samples are used; the High intensity arm is outside this protocol's scope (moderate intensity only, S3.p1) and is analysed as exploratory.", "planned_contrasts": ["Moderate run vs Basal (sedentary) at ZT14 (S3.3.p2 running vs sedentary; S4.p1 ZT14; paper: no DEG count reported)", "Moderate run vs Basal (sedentary) at ZT22 (S3.3.p2; S4.p1 ZT22; paper: no DEG count reported)"], "repeated_measure_unit": "none: one muscle per mouse, independent animals", "normalization": "not stated", "paper_method": "not stated (protocol paper, no DE analysis)", "paper_threshold": {"metric": null, "cutoff": null, "effect_metric": null, "effect_cutoff": null, "stated": false, "source_locator": null}, "paper_results": "none for gene expression; only running ca ... [40 more characters]

reasoning: The article is a protocol for a moderate-intensity treadmill test at different ZTs and for muscle dissection comparing running versus sedentary mice (S3.3.p2). It names GSE117161 as the transcriptome data of Ezagouri et al. 2019 (TAB1, S7.3.p2) but contains no DE method, threshold or results. The intended exercise question is therefore moderate run vs sedentary, at ZT14 and ZT22 separately, since daytime dependence is the paper's theme (S1.1.p2, S4.p1).

rejected alternatives: [{"value": "Pool ZT14 and ZT22 into one Moderate vs Basal contrast", "reason_rejected": "the paper's theme is daytime difference; pooling hides the ZT dependence it studies."}, {"value": "High vs Basal as a planned contrast", "reason_rejected": "this protocol covers moderate intensity only (S3.p1); High is an arm of the companion study, kept exploratory."}]

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\prep\\GSE117161_counts_fixed.csv", "owned": true, "checks": ["TAB1 and S7.3.p2 name GSE117161 as the transcriptome data of Ezagouri et al. 2019, which this protocol details", "GEO: gastrocnemius muscle, C57bl6 male, 3 months old (growth_protocol), Asher lab Weizmann", "GEO factors (time Early ZT14 / Late ZT22; protocol Basal/Moderate/High) match the paper's ZT14/ZT22 running design"], "accession": "GSE117161", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE117161\\GSE117161_metadata.csv"}

reasoning: Accession is stated in the paper; tissue, strain, sex, age and ZTs match. The single deposited supplementary file is a raw count matrix with 18 columns matching all 18 GSM titles.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 18, "n_metadata": 18, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\aligned\\aligned_metadata.csv", "columns": {"run": {"source": "title", "regex": "^(Basal|Moderate|High)_(?:Early|Late)_[A-C]$"}, "time": {"source": "title", "regex": "^(?:Basal|Moderate|High)_(Early|Late)_[A-C]$", "recode": {"Early": "ZT14", "Late": "ZT22"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\aligned\\design_metadata.csv", "sha256": "eed048f355b03b8a5271cf2cbc68060bcca05dfe038b087ffe8043e2e4419a13", "levels": {"run": {"Basal": 6, "High": 6, "Moderate": 6}, "time": {"ZT14": 9, "ZT22": 9}}}}

reasoning: Matrix columns equal the GEO title field exactly (inspect alignment_keys: title 18/18). run and time are parsed from the title and agree with the characteristics fields running protocole and time (Early (ZT14)/Late (ZT22)).

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\aligned\\aligned_matrix.csv", "sha256": "a6fc03be080d6d6ea77815c1534df41a46279db0b71fa9031a9efd3ffffcc2db", "n_features": 14034, "n_samples": 18, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 587781.0, "median": 89.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: 100% integers, range 0-587781, median 89; GEO data_processing: STAR mapping and STAR gene counting, Raw read count for each gene in each sample. Excel-mangled symbols (Mar-0N/Sep-0N) repaired to MarchfN/SeptinN by prep/fix_excel_genes.py; 4 ambiguous duplicated rows (Mar-01 x2, Mar-02 x2: March1/2 vs Marc1/2) dropped. The paper states no input type.

### design (valid, not_started)

final: {"analysis_type": "factorial (3 running protocols x 2 times of day), cell-means joint model", "formula": "~ cell (run x time cell means)", "contrasts": [{"name": "run_Moderate_vs_Basal_time-ZT14", "control": "Basal at ZT14", "treatment": "Moderate at ZT14", "role": "primary"}, {"name": "run_Moderate_vs_Basal_time-ZT22", "control": "Basal at ZT22", "treatment": "Moderate at ZT22", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\suitability\\suitability.md", "n_comparisons": 11, "n_analyzable": 11}}

reasoning: Six cells of n=3 independent mice. The protocol's question is the moderate-run effect at each ZT, so the two within-ZT Moderate vs Basal contrasts are planned, estimated from one model fitted on all 18 samples. All other analyzable comparisons (High vs Basal, time-of-day effects within each protocol) are exploratory.

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(run) + C(time)", "n_samples": 18, "n_columns": 4, "columns": ["Intercept", "run_High", "run_Moderate", "time_ZT22"], "rank": 4, "full_rank": true, "residual_df": 14, "levels": {"run": {"Basal": 6, "High": 6, "Moderate": 6}, "time": {"ZT14": 9, "ZT22": 9}}, "cells": [{"cell": ["Basal", "ZT14"], "n": 3}, {"cell": ["Basal", "ZT22"], "n": 3}, {"cell": ["High", "ZT14"], "n": 3}, {"cell": ["High", "ZT22"], "n": 3}, {"cell": ["Moderate", "ZT14"], "n": 3}, {"cell": ["Moderate", "ZT22"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 18, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 18, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.time", "n_levels": 2, "status": "crossed", "crosstab": {"Basal" ... [2311 more characters]

reasoning: One gastrocnemius per mouse; no subject, batch or lane information is deposited; all samples are male, same strain and age. Time of day is a design factor, not a nuisance covariate.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald, joint cell-means model)", "formula": "~ cell (run x time cells)", "paper_route": {"method": "not stated", "status": "not_stated", "reason": "protocol paper reports no DE method"}, "deviations": []}

reasoning: Raw counts support DESeq2. The paper states no method, so the workflow's standard raw-count route is used.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": null, "cutoff": null, "effect_metric": null, "effect_cutoff": null, "stated": false}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}}

reasoning: The article states no DE threshold, so the workflow default (BH padj < 0.05, no fold-change rule) applies. Audit rule padj < 0.05 and |log2FC| > 1 is reported separately and labelled.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "planned", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 18, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\results\\planned\\DEG_results_run_Moderate_vs_Basal_time-ZT14.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\results\\planned\\DEG_results_run_Moderate_vs_Basal_time-ZT22.csv"], "counts": {"planned/run_Moderate_vs_Basal_time-ZT14": {"applied": {"rule": "padj < 0.05", "n_tested": 11040, "n_significant": 734, "n_up": 425, "n_down": 309, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 11040, "n_significant": 93, "n_up": 46, "n_down": 47, "deg_sanity": "ok"}}, "planned/run_Moderate_vs_Basal_time-ZT22": {"applied": {"rule": "padj < 0.05", "n_tested": 10768, "n_significant": 533, "n_up": 337, "n_down": 196, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 10768, "n_significant": 92, "n_up": 71, "n_down": 21, "deg_sanity": "ok"}}}}

reasoning: Moderate vs Basal within ZT14 and within ZT22 from one DESeq2 model on all 18 samples.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "exploratory", "role": "exploratory", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 18, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\results\\exploratory\\DEG_results_run_High_vs_Basal_time-ZT14.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\results\\exploratory\\DEG_results_run_Moderate_vs_Basal_time-ZT14.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\results\\exploratory\\DEG_results_run_Moderate_vs_High_time-ZT14.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\results\\exploratory\\DEG_results_run_High_vs_Basal_time-ZT22.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\results\\exploratory\\DEG_results_run_Moderate_vs_Basal_time-ZT22.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\results\\exploratory\\DEG_results_run_Moderate_vs_High_time-ZT22.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\results\\exploratory\\DEG_results_time_ZT22_vs_ZT14_run-Basal.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33598660\\GSE117161\\results\\exploratory\\DEG_results_t ... [3981 more characters]

reasoning: Every analyzable comparison the suitability report lists (High vs Basal, time-of-day effects), same model; exploratory.

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["The paper is a protocol with no reported DE results; there are no paper DEG counts or genes to compare against.", "GEO says the moderate group ran the moderate test for 1 hour (final speed 20 cm/s), while the protocol describes running at 22-25 cm/s until fatigue (several hours). The deposited samples therefore reflect a 1 h moderate bout, not run-to-fatigue.", "The sacrifice time of the Basal (sedentary) controls relative to the run is not recorded (S3.3.p2 lists two options), so elapsed-time effects cannot be separated from the exercise effect.", "n = 3 per cell."], "results": {"planned/run_Moderate_vs_Basal_time-ZT14": {"n_deg": 734, "up": 425, "down": 309, "rule": "padj < 0.05", "audit_n": 93}, "planned/run_Moderate_vs_Basal_time-ZT22": {"n_deg": 533, "up": 337, "down": 196, "rule": "padj < 0.05", "audit_n": 92}, "exploratory/run_High_vs_Basal_time-ZT14": {"n_deg": 86, "up": 81, "down": 5, "rule": "padj < 0.05", "audit_n": 30}, "exploratory/run_Moderate_vs_Basal_time-ZT14": {"n_deg": 734, "up": 425, "down": 309, "rule": "padj < 0.05", "audit_n": 93}, "exploratory/run_Moderate_vs_High_time-ZT14": {"n_deg": 557, "up": 260, "down": 297, "rule": "padj < 0.05", "audit_n": 11}, "exploratory/run_High_vs_Basal_time-ZT22": {"n_deg": 183, "up": 175, "down": 8, "rule": "padj < 0.05", "audit_n": 59}, "exploratory/run_Moderate_vs_Basal_time-ZT22": {"n_deg": 533, "up": 337, "down": 196, "rule": "padj < 0.05", "audit_n": 92}, "exploratory/run_Mode ... [775 more characters]

reasoning: Planned contrasts follow the protocol's running-vs-sedentary design at each ZT; nothing to compare quantitatively.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 18 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "moderate run duration and speed",
    "paper": "22-25 cm/s until fatigue, a few hours (S3.p1, S3.2)",
    "data": "GEO treatment_protocol: moderate intensity test for 1 hour, final speed 20 cm/s",
    "disposition": "executable_without_change"
  },
  {
    "item": "sedentary control sacrifice time",
    "paper": "start or end of run time are both valid options (S3.3.p2)",
    "data": "not recorded in GEO",
    "disposition": "executable_without_change"
  },
  {
    "item": "High intensity arm",
    "paper": "not part of this moderate-intensity protocol",
    "data": "6 High samples deposited",
    "disposition": "executable_without_change"
  },
  {
    "item": "Excel-mangled gene symbols",
    "paper": "n/a",
    "data": "Mar-0N/Sep-0N date strings, 2 duplicated IDs",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID33598660 / GSE117161

## What ran
- Paper: STAR Protocols method paper (PMC7868630). It names GSE117161 as the transcriptome data of the companion study Ezagouri et al. 2019 (TAB1, S7.3.p2). It reports **no DE method, no threshold, and no DEG counts or genes**.
- Data: one raw-count matrix (STAR gene counts, 14,038 genes x 18 samples), gastrocnemius, male C57BL/6. Six cells (Basal/Moderate/High running x ZT14/ZT22), n=3 each. Samples aligned exactly on `title`, 18/18.
- Prep: `prep/fix_excel_genes.py` fixed Excel-mangled symbols (19 `Mar-0N`/`Sep-0N` renamed to `MarchfN`/`SeptinN`). It dropped 4 ambiguous duplicated rows, `Mar-01` x2 and `Mar-02` x2: each pair is March1/2 vs Marc1/2, and the file cannot tell which is which.
- Route: case spec. One DESeq2 (pydeseq2 Wald) cell-means model on all 18 samples, run through `tools.joint_contrasts:run_joint_deseq2`. No blocking: animals are independent and no batch is recorded. Sex check passed (all male).
- Planned (paper_aligned): Moderate run vs Basal (sedentary) within ZT14 and within ZT22. This is the protocol's running-vs-sedentary dissection (S3.3.p2) at the two ZTs it compares (S4.p1).
- Exploratory: all 11 analyzable comparisons. These cover High vs Basal, Moderate vs High, and time of day (ZT22 vs ZT14) within each protocol.
- Enrichment: not run, because the paper reports no pathway results.
- Contract validator: 11 records, 0 errors.

## DEG counts (threshold: workflow_default, BH padj < 0.05, no FC rule. The paper states no threshold.)
| Contrast | DEGs (up/down) | audit padj<0.05 and abs(log2FC)>1 | Paper |
|---|---|---|---|
| Moderate vs Basal, ZT14 | 734 (425/309) | 93 | not reported |
| Moderate vs Basal, ZT22 | 533 (337/196) | 92 | not reported |

Exploratory: High vs Basal gave 86 DEGs at ZT14 and 183 at ZT22. ZT22 vs ZT14 gave 705 in Basal, 433 in Moderate and 612 in High.

Sanity check: exercise-response genes go up with the moderate run at both ZTs. Nr4a3 log2FC is 3.4 at ZT14 and 3.0 at ZT22; Hspa1a is 2.7 and 3.0; Atf3 is 1.6 and 1.4. Ppargc1a is up only at ZT14 (0.61, padj 3e-5); at ZT22 it is 0.12 and not significant. Per1 rises strongly at ZT22 only. There are no paper results, so nothing contradicts the paper.

## Deviations and caveats
- The paper has no DE results, so there is no quantitative comparison with the paper. Because no method was stated, the method used (DESeq2) is the workflow's standard raw-count route.
- **Duration mismatch.** GEO says the moderate arm ra ... [1016 more characters]
