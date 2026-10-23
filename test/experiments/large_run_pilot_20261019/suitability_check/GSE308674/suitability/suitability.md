# Suitability: GSE308674

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; batch: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 10/10 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 28 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_H_vs_C | simple | H (6), C (4) | yes |
| grp_HM_vs_C | simple | HM (6), C (4) | yes |
| grp_L_vs_C | simple | L (6), C (4) | yes |
| grp_M_vs_C | simple | M (6), C (4) | yes |
| grp_HM_vs_H | simple | HM (6), H (6) | yes |
| grp_L_vs_H | simple | L (6), H (6) | yes |
| grp_M_vs_H | simple | M (6), H (6) | yes |
| grp_L_vs_HM | simple | L (6), HM (6) | yes |
| grp_M_vs_HM | simple | M (6), HM (6) | yes |
| grp_M_vs_L | simple | M (6), L (6) | yes |
