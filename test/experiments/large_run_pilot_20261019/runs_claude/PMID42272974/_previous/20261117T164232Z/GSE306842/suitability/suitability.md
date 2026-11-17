# Suitability: GSE306842

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (Salmon gene-level counts from nf-core/rnaseq); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_F1_vs_CTRL | simple | F1 (6), CTRL (6) | yes |
| grp_F10_vs_CTRL | simple | F10 (6), CTRL (6) | yes |
| grp_F4_vs_CTRL | simple | F4 (6), CTRL (6) | yes |
| grp_F10_vs_F1 | simple | F10 (6), F1 (6) | yes |
| grp_F4_vs_F1 | simple | F4 (6), F1 (6) | yes |
| grp_F4_vs_F10 | simple | F4 (6), F10 (6) | yes |
