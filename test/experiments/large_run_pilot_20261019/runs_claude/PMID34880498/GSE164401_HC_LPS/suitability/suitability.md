# Suitability: GSE164401_HC_LPS

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 7/7 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 31 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_LPSRP_vs_LPSCP | simple | LPSRP (8), LPSCP (7) | yes |
| grp_LPSSAL_vs_LPSCP | simple | LPSSAL (8), LPSCP (7) | yes |
| grp_SALSAL_vs_LPSCP | simple | SALSAL (8), LPSCP (7) | yes |
| grp_LPSSAL_vs_LPSRP | simple | LPSSAL (8), LPSRP (8) | yes |
| grp_SALSAL_vs_LPSRP | simple | SALSAL (8), LPSRP (8) | yes |
| grp_SALSAL_vs_LPSSAL | simple | SALSAL (8), LPSSAL (8) | yes |
| grp_LPSSAL_vs_SALSAL | simple | LPSSAL (8), SALSAL (8) | yes |
