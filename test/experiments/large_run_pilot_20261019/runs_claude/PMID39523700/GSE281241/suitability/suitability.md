# Suitability: GSE281241

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (nf-core Salmon gene_counts, non-integer); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_ChR2_vs_WT | simple | ChR2 (6), WT (6) | yes |
