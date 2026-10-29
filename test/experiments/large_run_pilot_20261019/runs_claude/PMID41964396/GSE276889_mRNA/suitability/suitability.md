# Suitability: GSE276889_mRNA

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (kallisto, gene-aggregated; deposited as integers); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 3 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 33 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_post3h_vs_post0h | simple | post3h (11), post0h (12) | yes |
| time_post0h_vs_pre | simple | post0h (12), pre (10) | yes |
| time_post3h_vs_pre | simple | post3h (11), pre (10) | yes |
