# Suitability: GSE325919

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 3 levels |
| Covariance | pass | not_required; sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_G6PD_vs_SED | simple | G6PD (10), SED (10) | yes |
| grp_TR_vs_G6PD | simple | TR (10), G6PD (10) | yes |
| grp_TR_vs_SED | simple | TR (10), SED (10) | yes |
