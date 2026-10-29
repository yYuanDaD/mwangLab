# Suitability: GSE319603

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 3 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 18 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_C_vs_H | simple | C (6), H (6) | yes |
| grp_HM_vs_C | simple | HM (6), C (6) | yes |
| grp_HM_vs_H | simple | HM (6), H (6) | yes |
