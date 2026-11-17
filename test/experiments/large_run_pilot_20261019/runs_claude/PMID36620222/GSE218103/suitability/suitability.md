# Suitability: GSE218103

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | geno: 2 levels; time: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_CP_vs_TD_time-post | simple | post/CP (3), post/TD (3) | yes |
| geno_CP_vs_TD_time-pre | simple | pre/CP (3), pre/TD (3) | yes |
| time_post_vs_pre_geno-CP | simple | CP/post (3), CP/pre (3) | yes |
| time_post_vs_pre_geno-TD | simple | TD/post (3), TD/pre (3) | yes |
| geno_time_CP_post_vs_TD_pre | interaction | CP/post (3), TD/post (3), CP/pre (3), TD/pre (3) | yes |
