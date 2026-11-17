# Suitability: GSE286570

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 7/7 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_HAE_vs_HFD | simple | HAE (3), HFD (3) | yes |
| grp_HRE_vs_HAE | simple | HRE (3), HAE (3) | yes |
| grp_NC_vs_HAE | simple | NC (3), HAE (3) | yes |
| grp_HRE_vs_HFD | simple | HRE (3), HFD (3) | yes |
| grp_NC_vs_HFD | simple | NC (3), HFD (3) | yes |
| grp_NC_vs_HRE | simple | NC (3), HRE (3) | yes |
| grp_HAE_vs_HRE | simple | HAE (3), HRE (3) | yes |
