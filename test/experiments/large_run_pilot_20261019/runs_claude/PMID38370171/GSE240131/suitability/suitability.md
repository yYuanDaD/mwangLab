# Suitability: GSE240131

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_E_vs_C | simple | E (3), C (3) | yes |
| grp_T_vs_C | simple | T (3), C (3) | yes |
| grp_TE_vs_C | simple | TE (3), C (3) | yes |
| grp_T_vs_E | simple | T (3), E (3) | yes |
| grp_TE_vs_E | simple | TE (3), E (3) | yes |
| grp_TE_vs_T | simple | TE (3), T (3) | yes |
