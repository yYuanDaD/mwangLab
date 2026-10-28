# Suitability: GSE124799

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 3 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_ExSed_vs_Ex | simple | ExSed (3), Ex (3) | yes |
| grp_Ex_vs_Sed | simple | Ex (3), Sed (3) | yes |
| grp_ExSed_vs_Sed | simple | ExSed (3), Sed (3) | yes |
