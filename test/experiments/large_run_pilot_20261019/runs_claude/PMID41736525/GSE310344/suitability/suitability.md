# Suitability: GSE310344

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | linear_normalized (Partek CPM); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | time: 4 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_AT_vs_BL | simple | AT (9), BL (9) | yes |
| time_RAT_vs_AT | simple | RAT (9), AT (9) | yes |
| time_REC_vs_AT | simple | REC (9), AT (9) | yes |
| time_RAT_vs_BL | simple | RAT (9), BL (9) | yes |
| time_REC_vs_BL | simple | REC (9), BL (9) | yes |
| time_REC_vs_RAT | simple | REC (9), RAT (9) | yes |
