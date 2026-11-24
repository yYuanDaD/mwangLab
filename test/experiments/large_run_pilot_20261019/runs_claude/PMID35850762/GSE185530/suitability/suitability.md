# Suitability: GSE185530

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 6 levels |
| Covariance | pass | not_required; exp: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 15/15 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 36 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_KDeps3_vs_KDeps0 | simple | KDeps3 (6), KDeps0 (6) | yes |
| grp_KDrest_vs_KDeps0 | simple | KDrest (6), KDeps0 (6) | yes |
| grp_NCeps0_vs_KDeps0 | simple | NCeps0 (6), KDeps0 (6) | yes |
| grp_NCeps3_vs_KDeps0 | simple | NCeps3 (6), KDeps0 (6) | yes |
| grp_KDeps0_vs_NCrest | simple | KDeps0 (6), NCrest (6) | yes |
| grp_KDrest_vs_KDeps3 | simple | KDrest (6), KDeps3 (6) | yes |
| grp_NCeps0_vs_KDeps3 | simple | NCeps0 (6), KDeps3 (6) | yes |
| grp_NCeps3_vs_KDeps3 | simple | NCeps3 (6), KDeps3 (6) | yes |
| grp_KDeps3_vs_NCrest | simple | KDeps3 (6), NCrest (6) | yes |
| grp_NCeps0_vs_KDrest | simple | NCeps0 (6), KDrest (6) | yes |
| grp_NCeps3_vs_KDrest | simple | NCeps3 (6), KDrest (6) | yes |
| grp_KDrest_vs_NCrest | simple | KDrest (6), NCrest (6) | yes |
| grp_NCeps3_vs_NCeps0 | simple | NCeps3 (6), NCeps0 (6) | yes |
| grp_NCeps0_vs_NCrest | simple | NCeps0 (6), NCrest (6) | yes |
| grp_NCeps3_vs_NCrest | simple | NCeps3 (6), NCrest (6) | yes |
