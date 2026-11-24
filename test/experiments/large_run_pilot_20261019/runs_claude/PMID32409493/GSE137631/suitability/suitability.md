# Suitability: GSE137631

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; subject: omit (one sample per subject per factor level set: an identifier, not a block) |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_ETpost_vs_ETpre | simple | ETpost (6), ETpre (6) | yes |
| grp_LEAN_vs_ETpost | simple | LEAN (6), ETpost (6) | yes |
| grp_RYpost_vs_ETpost | simple | RYpost (6), ETpost (6) | yes |
| grp_RYpre_vs_ETpost | simple | RYpre (6), ETpost (6) | yes |
| grp_LEAN_vs_ETpre | simple | LEAN (6), ETpre (6) | yes |
| grp_RYpost_vs_ETpre | simple | RYpost (6), ETpre (6) | yes |
| grp_RYpre_vs_ETpre | simple | RYpre (6), ETpre (6) | yes |
| grp_RYpost_vs_LEAN | simple | RYpost (6), LEAN (6) | yes |
| grp_RYpre_vs_LEAN | simple | RYpre (6), LEAN (6) | yes |
| grp_RYpre_vs_RYpost | simple | RYpre (6), RYpost (6) | yes |
| grp_RYpost_vs_RYpre | simple | RYpost (6), RYpre (6) | yes |
