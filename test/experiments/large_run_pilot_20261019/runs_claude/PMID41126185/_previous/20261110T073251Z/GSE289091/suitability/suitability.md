# Suitability: GSE289091

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | cond: 2 levels |
| Covariance | pass | not_required; run: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 2/2 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 17 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| cond_stretch_vs_static_geno-Ctl | simple | Ctl/stretch (3), Ctl/static (3) | yes |
| cond_stretch_vs_static_geno-siLMNA | simple | siLMNA/stretch (4), siLMNA/static (7) | yes |
