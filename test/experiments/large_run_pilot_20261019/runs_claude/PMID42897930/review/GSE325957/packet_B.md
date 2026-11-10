# Review packet B (the analysis' decisions): GSE325957

## Mechanical flags

- **unused_subject_like_column**: {"column": "sample_group", "n_values": 4, "max_repeat": 5, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## Stop reasons

- covariance (refused; claim type: other): Exercise (activity) is completely aliased with study batch: all sedentary samples (NP_1-3, HP_1-3) are reused from GSE120958, a separate 2019 cohort (12-week HPD, different age/protocol), and all exercised samples (NPE, HPE) were sequenced for GSE325957 by Plasmidsaurus (S2.8.p1, S9.p1, S2.1.p1, S1.p2). No sample of either activity level exists in the other batch, so the exercise effect cannot be separated from cohort, library preparation, sequencing run, mouse age and diet duration. The paper's own PCA (S3.7.p1: exercised vs sedentary 'vastly different', exercised diets similar) is what a batch split would also produce. Refused at covariance; no model can identify the estimand from these data.

## Samples per design level

### `activity`
- **E** (9): NPE_1 / GSM9617808; NPE_2 / GSM9617809; NPE_3 / GSM9617810; NPE_4 / GSM9617811; NPE_5 / GSM9617812; HPE_1 / GSM9617813; HPE_2 / GSM9617814; HPE_3 / GSM9617815; HPE_5 / GSM9617816
- **S** (6): NP_1 / GSM3422122; NP_2 / GSM3422123; NP_3 / GSM3422124; HP_1 / GSM3422125; HP_2 / GSM3422126; HP_3 / GSM3422127

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE325957", "GSE120958"], "assay": "bulk polyA RNA-seq of gastrocnemius-plantaris (GP) muscle, male C57BL/6 mice (S2.8.p1)", "factors": {"diet": ["NPD (0.6% Pi)", "HPD (2.0% Pi)"], "activity": ["sedentary", "9 wk voluntary wheel running"]}, "sample_inclusion": "Exercised NPE (n=5) and HPE (n=4) sequenced in this study (GSE325957); sedentary NPS/HPS (n=3 each) are the previously published samples from GSE120958 (Peri-Okonny et al. 2019) (S2.8.p1, S9.p1, S3.7.p1, FIG6 n=3-5)", "primary_estimand": "Effect of exercise training on GP muscle gene expression within each diet (NPS vs NPE; HPS vs HPE), and the diet-dependence of that response", "planned_contrasts": ["NPE vs NPS (S3.7.p1; Table S2; paper: 9467 DEGs, 4540 up / 4927 down)", "HPE vs HPS (S3.7.p1; Table S3; paper: 8009 DEGs, 3883 up / 4126 down)", "HPS vs NPS (diet, sedentary; S3.7.p1; count not stated)", "HPE vs NPE (diet, exercised; S3.7.p2; Table S8; paper: 10 DEGs)"], "repeated_measure_unit": "none; one muscle per mouse", "paper_method": "featureCounts read counts; DESeq2 v1.50.2 Wald test, BH FDR, on NPE/HPE samples together with GSE120958 (S2.8.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false, "source_locator": "SUP5/SUP6/SUP11 (Tables S2, S3, S8: p_adj < 0.05 and |log2FC| > 0.5); S2.8.p1"}, "paper_results": {"NPE_vs_NPS": 9467, "HPE_vs_HPS": 8009, "HPE_vs_NPE": 10}}

reasoning: S2.8.p1: only NPE and HPE GP samples were sequenced in this study (Plasmidsaurus, 2026); DE was run on these together with GSE120958 (the 2019 study's sedentary NPD/HPD GP samples). S9.p1 names both accessions. S3.7.p1 gives the four pairwise comparisons and counts; Tables S2/S3/S8 state padj < 0.05 and |log2FC| > 0.5. S2.1.p1: this study's mice were 25-week-old males fed diet for 14 weeks; the sedentary arm comes from a different cohort (prior study: 12-week HPD, S1.p2), and S2.4.p1 notes that the earlier study used different exercise testing equipment.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42897930\\GSE325957_CPM_clean.csv", "owned": true, "checks": ["GSE325957 supplementary CPM file is the series' own deposit; its NPE_1-5/HPE_1,2,3,5 columns match GSE325957 sample descriptions (Library name ...,NPE_1 etc.) one to one", "Its NP_1-3/HP_1-3 columns are the GSE120958 samples GSM3422122-GSM3422127, as listed in the series' own GSE325957_reanalysis_samples file", "Paper S9.p1 names GSE325957 as this study's data and GSE120958 as reused data", "No raw count matrix is deposited: data_processing says the supplement holds CPM values plus DESeq2 output"], "accession": "GSE325957", "metadata_file": "E:/agent/mwangLab_pdf/test/experiments/large_run_pilot_20261019/runs_claude/PMID42897930/GSE325957_combined_samples.csv"}

reasoning: The CPM matrix and both sample sets belong to the paper's design (S2.8.p1, S9.p1). The sedentary arm is owned through the reanalysis listing, not through GSE325957 sample records; the combined sample sheet was built by prep_inputs.py from those two GEO-deposited sources.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 15, "n_metadata": 15, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42897930\\GSE325957\\aligned\\aligned_metadata.csv", "columns": {}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42897930\\GSE325957\\aligned\\design_metadata.csv", "sha256": "ffad43b7e209d4f6bacd923baca2a712bfc1dc2eff88c6a8f7f06563f0cc7640", "levels": {}}}

reasoning: Combined sample sheet is indexed by the matrix column names (NP_1 ... HPE_5); exact match on the index. Exercised IDs come from GSE325957 description field ('Library name: ...,NPE_1'), sedentary IDs from GSE325957_reanalysis_samples ('Processed Data Column Header'). diet (NP/HP) and activity (S/E) are already formula-safe columns; series records origin.

### matrix (valid, not_started)

final: {"matrix_type": "CPM (linear normalized, library-size scaled)", "recommended_method": "limma on log2(CPM+1) (DESeq2 not applicable: no raw counts deposited)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42897930\\GSE325957\\aligned\\aligned_matrix.csv", "sha256": "77d22db1a72971668d27128333be3cf98176395cc1bcccf5f085caa7793a198b", "n_features": 55401, "n_samples": 15, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 70166.7982664921, "median": 0.0, "integer_fraction": 0.5832, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GEO data_processing: 'excel file containing CPM values and pairwise comparison output from DESeq2'; column header group 'CPM'; inspect: 58% integer fraction driven by zeros, max 70167, non-integer positives. The paper's DESeq2 input was featureCounts counts (S2.8.p1), which are not deposited, so the paper route cannot be reproduced from this matrix regardless of design.

### design (valid, not_started)

final: {"analysis_type": "two-group per diet stratum (exercise effect within NPD and within HPD)", "design_column": "activity", "contrasts": [{"name": "activity_E_vs_S_diet-NP", "control": "S", "treatment": "E", "role": "primary"}, {"name": "activity_E_vs_S_diet-HP", "control": "S", "treatment": "E", "role": "primary"}], "suitability": {"verdict": "partially_analyzable", "failed": [], "warnings": ["covariance"], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42897930\\GSE325957\\suitability\\suitability.md", "n_comparisons": 2, "n_analyzable": 2}}

reasoning: The paper's exercise estimand is sedentary vs trained within each diet (S3.7.p1, Tables S2/S3). The diet comparisons (HPS vs NPS, HPE vs NPE) are diet effects, not exercise effects, and are not the requested estimand. Group sizes: NP S=3/E=5, HP S=3/E=4.

rejected alternatives: [{"value": "2x2 factorial diet*activity interaction", "reason_rejected": "the interaction is the paper's narrative question (diet-dependence of the exercise response) but it inherits the same activity-batch aliasing; not a separately identifiable estimand"}, {"value": "HPE vs NPE within exercised", "reason_rejected": "within-batch but a diet effect, not the requested exercise effect"}]

### covariance (refused, not_started)

final: {"status": "unresolved", "blocking_terms": [], "covariates": [{"name": "series", "disposition": "aliased: every sedentary sample is GSE120958 and every exercised sample is GSE325957"}], "design_check": {"formula_equivalent": "~ C(activity)", "n_samples": 15, "n_columns": 2, "columns": ["Intercept", "activity_S"], "rank": 2, "full_rank": true, "residual_df": 13, "levels": {"activity": {"E": 9, "S": 6}}, "cells": [{"cell": ["E"], "n": 9}, {"cell": ["S"], "n": 6}], "min_cell_size": 6, "missing_values": {}}, "confounding": [{"column": "series", "n_levels": 2, "status": "complete_confounding", "crosstab": {"E": {"GSE120958": 0, "GSE325957": 9}, "S": {"GSE120958": 6, "GSE325957": 0}}}]}

reasoning: Per decision gates, a covariate completely confounded with the treatment stops the case. series is a cohort/batch key, not an annotation chosen by name: it captures a different experiment, sequencing provider and time. Diet stratification does not help, since within each diet the activity split equals the series split.

## Suitability report lines (sex, confounding, warnings)

- Verdict: **partially_analyzable**; check: covariance
- | Check | Status | Detail |
- | Covariance | partial | not_required; series: check (splits the samples exactly like a design factor: if it is that factor's own column, ignore it; if it is a batch, the comparison cannot be separated from it and the case stops) |
- | Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "sedentary control arm",
    "paper": "NPS/HPS from GSE120958 analysed together with new NPE/HPE samples (S2.8.p1)",
    "data": "series column is identical to activity in every diet stratum",
    "disposition": "blocks_estimand"
  },
  {
    "item": "matrix input",
    "paper": "featureCounts read counts into DESeq2 (S2.8.p1)",
    "data": "only CPM values and the authors' DESeq2 output tables are deposited; no raw counts",
    "disposition": "blocks_paper_method"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID42897930 / GSE325957

**Status: refused at the `covariance` gate** (decision_status `refused`, execution `not_run`, route `stopped`). The decision contract validator reported 6 records and 0 errors.

## What ran
1. `python -m tools.case_runner inspect GSE325957` (data were already cached). This found a CPM file (15 columns), 4 author DESeq2 result tables, GEO metadata for only 9 samples (NPE x5, HPE x4), and the series' own `GSE325957_reanalysis_samples.csv`, which maps NP_1-3/HP_1-3 to GSE120958 GSM3422122-7.
2. `prep_inputs.py` (listed in `prep_scripts`). It strips the spurious first header row from the CPM CSV, drops `gene_symbol`, and writes `GSE325957_CPM_clean.csv` (55,401 genes x 15 samples, values unchanged). It also writes `GSE325957_combined_samples.csv`, which indexes each matrix column with `diet` (NP/HP), `activity` (S/E) and `series`.
3. `python -m tools.case_runner execute case_spec.json`. Alignment was an exact index match, 15/15. The suitability verdict was `partially_analyzable`. Its covariance check flagged `series` because it "splits the samples exactly like a design factor".

## Why refused
The paper (S2.8.p1, S9.p1) sequenced only the exercised mice (NPE n=5, HPE n=4; Plasmidsaurus, 2026). The sedentary controls (NPS, HPS n=3 each) are reused from GSE120958, the 2019 study (Peri-Okonny et al.). That was a different cohort, with a 12-week HPD (S1.p2) versus 14 weeks here at 25 weeks of age (S2.1.p1). It also had a different library prep and sequencing run. In both diet strata, activity (sedentary vs exercised) is therefore identical to series/batch, so the exercise estimand (NPE vs NPS, HPE vs HPS) cannot be identified. The gates were recorded in order: paper_reconstruction, ownership, alignment, matrix, design, covariance (refused, with `series` marked `aliased`).

Second blocker: the paper route also cannot be reproduced. No raw counts are deposited, only CPM values plus the authors' DESeq2 output (GEO data_processing). DESeq2 on featureCounts output is therefore impossible, and the only valid route would be limma on log2(CPM+1).

## DEG counts vs the paper
The paper's threshold is padj < 0.05 and |log2FC| > 0.5 (Tables S2/S3/S8).
- NPE vs NPS: paper 9,467 (4,540 up / 4,927 down). Ours: not run (refused).
- HPE vs HPS: paper 8,009 (3,883 up / 4,126 down). Ours: not run (refused).
- HPE vs NPE (diet within exercised, within one batch): paper 10. Not run, because it is a diet effect, not the requested exercise estimand. ... [1040 more characters]
