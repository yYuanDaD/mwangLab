# Suitability: GSE320360

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 4 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); subject: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); subject: omit (makes the design rank deficient) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_post_vs_mid | simple | post (28), mid (29) | yes |
| time_post75_vs_mid | simple | post75 (28), mid (29) | yes |
| time_mid_vs_pre | simple | mid (29), pre (30) | yes |
| time_post75_vs_post | simple | post75 (28), post (28) | yes |
| time_post_vs_pre | simple | post (28), pre (30) | yes |
| time_post75_vs_pre | simple | post75 (28), pre (30) | yes |
