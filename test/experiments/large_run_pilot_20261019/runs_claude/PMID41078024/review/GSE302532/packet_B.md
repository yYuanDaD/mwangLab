# Review packet B (the analysis' decisions): GSE302532

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.2.treatment level", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 4, "samples_linked": 8, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_EX_vs_SED | 27 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 610 | 87 | 45 | 118 | 0.062 | 0.034 |

## Samples per design level

### `grp`
- **EX** (4): GSM9105557 / Exercised a / Library name: 451P; GSM9105558 / Exercised b / Library name: 452P; GSM9105559 / Exercised c / Library name: 454P; GSM9105560 / Exercised d / Library name: 455P
- **SED** (4): GSM9105553 / Sedentary a / Library name: 437P; GSM9105554 / Sedentary b / Library name: 449P; GSM9105555 / Sedentary c / Library name: 450P; GSM9105556 / Sedentary d / Library name: 453P

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE302532"], "assay": "total RNA-seq (Takara SMARTer Pico v3) of plasma exosome RNA, NovaSeq X Plus (S2.13.p1, S2.14.p1)", "organism": "Rattus norvegicus, male Sprague Dawley (S2.1.p1)", "sample_inclusion": "Cohort 2 only (non-PD, age-matched rats): exercise treatment then exosome molecular biology (S2.1.p1, ABS.p1); n = 4 per group (S2.5.p1); S4.4.p1 states 5 per group (discrepancy). Cohort 1 (PFF histology) has no sequencing.", "factors": {"group": ["Sedentary (control)", "Exercise (1 month treadmill, 20 m/min, 30 min, 5 d/wk)"]}, "primary_estimand": "Difference in plasma exosomal RNA abundance, exercised vs sedentary non-PD rats, blood drawn within 30 min of last exercise (S2.4.p1, S3.4.p1)", "planned_contrasts": ["Exercise vs Sedentary (S2.5.p1, S3.4.p1; paper: 27 RNAs upregulated, Table 2; no downregulated list reported)"], "repeated_measure_unit": "none (independent animals, one sample each)", "normalization": "CLC Genomics Workbench v25 TPM (GEO data_processing); paper does not describe the DE normalization", "paper_method": "not_reported (GEO data_processing names CLC Genomics Workbench v25.0; the DE test is not named in the paper)", "paper_threshold": {"metric": "not_reported", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.4.p1, TAB2", "note": "No rule stated. Table 2 lists only upregulated RNAs with raw P-values 3.76E-04 to 0.05 and FC 3.09 to 142.31 (S3.4.p1: 'fold change ranging from 3 to 142'); implied rule r ... [166 more characters]

reasoning: Two-cohort study; only cohort 2 (exercise vs sedentary, non-PD) was sequenced (S2.1.p1, S2.5.p1). The RNA-seq result is Table 2 (S3.4.p1). The paper states no DE method or threshold; GEO names CLC Genomics Workbench.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41078024\\prep\\GSE302532_TPM_libnames.csv", "owned": true, "checks": ["Data availability S10.p1 names GSE302532", "GEO: Rattus norvegicus plasma, Sprague Dawley, 4 Sedentary + 4 Exercised, matches S2.5.p1 n=4", "TPM file ExerciseExosomeTPMs matches the exosome RNA-seq", "Table 2 named RNAs (Npy, Rgs4, Np4, LOC120093427, ...) present as matrix rows"], "accession": "GSE302532", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE302532\\GSE302532_metadata.csv"}

reasoning: S10.p1 names the accession; sample counts and organism match the methods.

### alignment (valid, not_started)

final: {"note": "matrix columns renamed to library names by prep_rename_columns.py (regex ' - (\\d+P)_S\\d+ (GE) - TPM'); matrix group label prefix (Sedentary/Exercise) agrees with GEO treatment for every library", "method": "exact:lib", "n_aligned": 8, "n_metadata": 8, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41078024\\GSE302532\\aligned\\aligned_metadata.csv", "columns": {"treatment": {"alias_of": "characteristics_ch1.2.treatment"}, "grp": {"source": "characteristics_ch1.2.treatment", "regex": "^(Sedentary|Exercised)$", "recode": {"Sedentary": "SED", "Exercised": "EX"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41078024\\GSE302532\\aligned\\design_metadata.csv", "sha256": "3c6e5498cc0d1301b6f53a8df8993fadbb2efbf3331d0da2d53b8b7ea02a7721", "levels": {"treatment": {"Sedentary": 4, "Exercised": 4}, "grp": {"SED": 4, "EX": 4}}}}

reasoning: Deposited TPM columns embed the GEO library name (437P etc.); the prep script renames them exactly and the metadata key is derived from description 'Library name: 437P'. Exact match, no positional alignment.

### matrix (valid, not_started)

final: {"source": "GEO data_processing: 'Excel file with TPM values for each sample', CLC Genomics Workbench v25; column headers end in '- TPM'; every column sums to 1e6", "paper_input": "not_reported (paper presents fold change and P-values only)", "matrix_type": "TPM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41078024\\GSE302532\\aligned\\aligned_matrix.csv", "sha256": "2f7b23cfef932570f17148eaac6046cf2b5c06cb195c21ac25ec3969c5d226ad", "n_features": 29541, "n_samples": 8, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 567439.5902172856, "median": 0.0, "integer_fraction": 0.6959, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Column sums are exactly 1,000,000 and headers say TPM; non-integer values. No raw counts are deposited, so count models cannot run.

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "SED", "treatment": "EX", "estimand_type": "causal (randomized, S2.5.p1)", "contrasts": [{"name": "grp_EX_vs_SED", "control": "SED", "treatment": "EX", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41078024\\GSE302532\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Randomized two-arm design, one sample per rat (S2.5.p1). Only male rats (S2.1.p1).

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 8, "n_columns": 2, "columns": ["Intercept", "grp_SED"], "rank": 2, "full_rank": true, "residual_df": 6, "levels": {"grp": {"SED": 4, "EX": 4}}, "cells": [{"cell": ["EX"], "n": 4}, {"cell": ["SED"], "n": 4}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 8, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 8, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.treatment", "n_levels": 2, "status": "complete_confounding", "crosstab": {"EX": {"Exercised": 4, "Sedentary": 0}, "SED": {"Exercised": 0, "Sedentary": 4}}}, {"column": "molecule_ch1", "n_levels": 1, "status": "constant"}, {"column": "extract_protocol ... [1717 more characters]

reasoning: Independent animals, no batch, sex, or pairing recorded in GEO or paper; no covariates added.

### method (valid, not_started)

final: {"matrix_type": "TPM", "method": "limma (moderated t, eBayes) on log2(TPM+1)", "formula": "~ grp", "paper_route": {"method": "CLC Genomics Workbench differential expression (not named in paper; GEO data_processing)", "status": "blocked", "reason": "CLC's DE test works on read counts; only TPM is deposited and the paper does not name the test"}, "deviations": ["limma on log2(TPM+1) replaces the unnamed CLC test; zero-variance features dropped by the executor"], "transform": "log2(x+1)"}

reasoning: TPM supports limma after log2(x+1) under the matrix policy; count methods are not valid on TPM.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "not_reported", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.4.p1, TAB2", "note": "implied by Table 2: raw P <= 0.05 and FC >= 3, up only"}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.5849625, "effect_cutoff_original": "FC 3", "inclusive": true, "label": "Table 2 implied rule (raw P <= 0.05, |FC| >= 3); paper reports up only"}}

reasoning: The paper states no significance rule; workflow default BH < 0.05 applied. The rule implied by Table 2 is reported as a labelled audit for comparison with the 27 upregulated RNAs.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_EX_vs_SED", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41078024\\GSE302532\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41078024\\GSE302532\\results\\grp_EX_vs_SED\\DEG_results_EX_vs_SED.csv"], "counts": {"grp_EX_vs_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17901, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue <= 0.05 and |log2FoldChange| >= 1.58496", "n_tested": 17901, "n_significant": 21, "n_up": 17, "n_down": 4, "deg_sanity": "ok"}}}}

reasoning: Exercise vs sedentary, limma on log2(TPM+1)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper's DE method (CLC) cannot be rerun from TPM; limma on log2(TPM+1) is a declared deviation.", "Paper reports only upregulated RNAs; compare audit up count with 27.", "Sample size: GEO and S2.5.p1 give 4 per group, S4.4.p1 says 5 per group.", "Exosome libraries are dominated by a few small RNAs (max TPM ~5.7e5), so TPM compositional effects are strong.", "No feature passes BH < 0.05 (min padj 0.47); the paper's 27 RNAs rest on raw P without multiple-testing correction.", "Direction contradiction: LOC120098346 (snRNA) is up 3.25-fold in Table 2 but log2FC -0.49 (p = 0.82) here; the other 26 Table 2 RNAs are positive.", "log2FoldChange is on log2(TPM+1), which shrinks fold changes of low-TPM RNAs relative to the paper's FC."], "results": {"grp_EX_vs_SED": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 21}}, "paper_counts": {"grp_EX_vs_SED": 27}, "comparison": {"grp_EX_vs_SED": {"ours": 0, "paper": 27}}, "paper_gene_check": {"grp_EX_vs_SED": {"Npy": {"AveExpr": 1.868, "log2FoldChange": 1.9211, "padj": 0.8101, "pvalue": 0.0406}, "Rgs4": {"AveExpr": 1.3183, "log2FoldChange": 1.61, "padj": 0.8101, "pvalue": 0.0776}, "Mt-atp6": {"AveExpr": 2.4232, "log2FoldChange": 1.7889, "padj": 0.8101, "pvalue": 0.0263}, "rno-mir-486": {"AveExpr": 2.0302, "log2FoldChange": 1.4783, "padj": 0.8101, "pvalue": 0.0368}, "B2m": {"AveExpr": 2.3594, "log2FoldChange": 1.8364, "padj": 0.8101, "pvalue": 0.0159}, "Np4": {"AveExpr": 1.2709, " ... [889 more characters]

reasoning: Route is a declared deviation (method). Paper count 27 is upregulated-only.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference completed on 8 samples.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "sample size",
    "paper": "S2.5.p1 n = 4 per group; S4.4.p1 '5 male rats in each of the exosomal RNA sequencing groups'",
    "data": "GEO: 4 Sedentary + 4 Exercised",
    "disposition": "executable_without_change"
  },
  {
    "item": "DE method and threshold",
    "paper": "not reported; Table 2 shows raw P and FC >= 3",
    "data": "TPM only (CLC)",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID41078024 / GSE302532

## What ran
- Case spec route (`tools.case_runner execute case_spec.json`); validator: 10 records, 0 errors; status completed.
- Data: `GSE302532_ExerciseExosomeTPMs.csv` (CLC Genomics Workbench v25 TPM, 29,541 features x 8 samples; every column sums to 1e6). Rat plasma exosome total RNA-seq, 4 Sedentary vs 4 Exercised (non-PD cohort 2, S2.1.p1, S2.5.p1).
- Prep: `prep_rename_columns.py` renames columns `Sedentary - 437P_S7 (GE) - TPM` to the GEO library name `437P` (values unchanged, Ensembl `Identifier` column dropped). Alignment exact on the key derived from `description` ("Library name: 437P"), 8/8.
- Design: two-group `~ grp`, EX vs SED, independent animals, no covariates. Suitability: analyzable.
- Method: limma (moderated t, eBayes) on log2(TPM+1); 17,901 features after the executor drops zero-variance rows. No enrichment (paper reports none).

## DEG counts vs paper
- Paper: 27 RNAs upregulated (Table 2, S3.4.p1); no downregulated list. The paper states no rule; Table 2 implies raw P <= 0.05 and FC >= 3 (FC 3.09 to 142.31).
- Applied (workflow_default, BH padj < 0.05, no FC cutoff): 0 DEGs (min padj 0.47).
- Audit (Table 2 implied rule, raw p <= 0.05 and |log2FC| >= log2(3) on log2(TPM+1)): 21 (17 up, 4 down: Alb, Tf, Hpx, LOC120101153). 11 of the 27 Table 2 RNAs pass (Npy, B2m, Mt-atp6, Anp32e, Pf4, Snora81_1, SNORA73, Snord89, Y_RNA_6, LOC120095472, LOC120102095). 14/27 have raw p < 0.05 and positive log2FC.
- Direction: 26/27 Table 2 RNAs positive here. Contradiction: LOC120098346 (paper up 3.25-fold, P 0.04) has log2FC -0.49, p 0.82 (recorded in study caveats). Rgs4 (paper FC 12.9) p = 0.078 here, driven by one exercise sample (452P).

## Deviations
- Paper DE test not named (GEO says CLC Genomics Workbench, which tests counts); only TPM deposited, so limma on log2(TPM+1) is a declared deviation (route `declared_deviation`).
- Threshold: paper states none, so workflow_default applied; Table 2 rule kept as a labelled audit. Paper's 27 rest on uncorrected P.
- log2(TPM+1) compresses fold changes for low-TPM RNAs relative to the paper's FC, so the audit FC filter is stricter than the paper's.
- Sample size discrepancy: S2.5.p1 and GEO give 4 per group; S4.4.p1 says 5 per group. Ran on the 4+4 deposited.

## Tool problems
- `tools/case_runner.py:504` (`native.align_to_metadata`) needs matrix column names to equal a metadata value exactly; when the key is embedded in the matrix column name (`Sedentary - 437P_S7  ... [339 more characters]
