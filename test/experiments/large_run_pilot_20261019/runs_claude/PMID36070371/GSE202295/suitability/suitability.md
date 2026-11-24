# Suitability: GSE202295

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 3 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); subject: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); subject: omit (makes the design rank deficient) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 111 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_post_vs_basal_diag-NGT | simple | NGT/post (16), NGT/basal (17) | yes |
| time_rec_vs_basal_diag-NGT | simple | NGT/rec (17), NGT/basal (17) | yes |
| time_rec_vs_post_diag-NGT | simple | NGT/rec (17), NGT/post (16) | yes |
| time_post_vs_basal_diag-T2D | simple | T2D/post (20), T2D/basal (21) | yes |
| time_rec_vs_basal_diag-T2D | simple | T2D/rec (20), T2D/basal (21) | yes |
| time_rec_vs_post_diag-T2D | simple | T2D/rec (20), T2D/post (20) | yes |
