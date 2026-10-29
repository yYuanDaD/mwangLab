# Suitability: GSE242354_HIPPOC

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 10/10 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 50 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_W1_vs_SED | simple | W1 (10), SED (10) | yes |
| grp_W2_vs_SED | simple | W2 (10), SED (10) | yes |
| grp_W4_vs_SED | simple | W4 (10), SED (10) | yes |
| grp_W8_vs_SED | simple | W8 (10), SED (10) | yes |
| grp_W2_vs_W1 | simple | W2 (10), W1 (10) | yes |
| grp_W4_vs_W1 | simple | W4 (10), W1 (10) | yes |
| grp_W8_vs_W1 | simple | W8 (10), W1 (10) | yes |
| grp_W4_vs_W2 | simple | W4 (10), W2 (10) | yes |
| grp_W8_vs_W2 | simple | W8 (10), W2 (10) | yes |
| grp_W8_vs_W4 | simple | W8 (10), W4 (10) | yes |
