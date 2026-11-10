# Suitability: GSE267512

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (Kallisto gene-level, deposited as integers); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | timepoint: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); subject: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); subject: omit (makes the design rank deficient) |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference completed on 57 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| timepoint_POST_vs_PRE | simple | POST (26), PRE (31) | yes |
