# Suitability: GSE279359

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 4 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_h24_vs_h1 | simple | h24 (5), h1 (5) | yes |
| time_ipe_vs_h1 | simple | ipe (5), h1 (5) | yes |
| time_h1_vs_pre | simple | h1 (5), pre (5) | yes |
| time_ipe_vs_h24 | simple | ipe (5), h24 (5) | yes |
| time_h24_vs_pre | simple | h24 (5), pre (5) | yes |
| time_ipe_vs_pre | simple | ipe (5), pre (5) | yes |
