# Suitability: GSE235942

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | treatment: 2 levels; age: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| treatment_HLU_vs_CTRL_age-m22 | simple | m22/HLU (3), m22/CTRL (13) | yes |
| treatment_HLU_vs_CTRL_age-m6 | simple | m6/HLU (5), m6/CTRL (9) | yes |
| age_m22_vs_m6_treatment-CTRL | simple | CTRL/m22 (13), CTRL/m6 (9) | yes |
| age_m22_vs_m6_treatment-HLU | simple | HLU/m22 (3), HLU/m6 (5) | yes |
| treatment_age_HLU_m22_vs_CTRL_m6 | interaction | HLU/m22 (3), CTRL/m22 (13), HLU/m6 (5), CTRL/m6 (9) | yes |
