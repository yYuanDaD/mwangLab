# Suitability: GSE310849

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | linear_normalized (Partek DESeq2 median-of-ratios normalized counts); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 10/10 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Rat') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_REC_vs_CTRL | simple | REC (3), CTRL (12) | yes |
| grp_RTTX_vs_CTRL | simple | RTTX (3), CTRL (12) | yes |
| grp_SHAM_vs_CTRL | simple | SHAM (3), CTRL (12) | yes |
| grp_TTX_vs_CTRL | simple | TTX (3), CTRL (12) | yes |
| grp_RTTX_vs_REC | simple | RTTX (3), REC (3) | yes |
| grp_SHAM_vs_REC | simple | SHAM (3), REC (3) | yes |
| grp_TTX_vs_REC | simple | TTX (3), REC (3) | yes |
| grp_SHAM_vs_RTTX | simple | SHAM (3), RTTX (3) | yes |
| grp_TTX_vs_RTTX | simple | TTX (3), RTTX (3) | yes |
| grp_TTX_vs_SHAM | simple | TTX (3), SHAM (3) | yes |
