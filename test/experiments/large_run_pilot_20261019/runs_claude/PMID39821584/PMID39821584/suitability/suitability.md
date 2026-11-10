# Suitability: PMID39821584

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 10/10 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_r50_vs_r25 | simple | r50 (6), r25 (6) | yes |
| grp_r75_vs_r25 | simple | r75 (6), r25 (6) | yes |
| grp_rU_vs_r25 | simple | rU (6), r25 (6) | yes |
| grp_r25_vs_sed | simple | r25 (6), sed (6) | yes |
| grp_r75_vs_r50 | simple | r75 (6), r50 (6) | yes |
| grp_rU_vs_r50 | simple | rU (6), r50 (6) | yes |
| grp_r50_vs_sed | simple | r50 (6), sed (6) | yes |
| grp_rU_vs_r75 | simple | rU (6), r75 (6) | yes |
| grp_r75_vs_sed | simple | r75 (6), sed (6) | yes |
| grp_rU_vs_sed | simple | rU (6), sed (6) | yes |
