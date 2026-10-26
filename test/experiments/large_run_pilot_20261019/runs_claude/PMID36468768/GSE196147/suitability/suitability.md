# Suitability: GSE196147

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | DESeq2-normalized counts; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; animal: omit (one sample per subject per factor level set: an identifier, not a block); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 10/10 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Rat') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_d10_vs_ctrl | simple | d10 (3), ctrl (12) | yes |
| grp_d2_vs_ctrl | simple | d2 (3), ctrl (12) | yes |
| grp_d20_vs_ctrl | simple | d20 (3), ctrl (12) | yes |
| grp_d30_vs_ctrl | simple | d30 (3), ctrl (12) | yes |
| grp_d2_vs_d10 | simple | d2 (3), d10 (3) | yes |
| grp_d20_vs_d10 | simple | d20 (3), d10 (3) | yes |
| grp_d30_vs_d10 | simple | d30 (3), d10 (3) | yes |
| grp_d20_vs_d2 | simple | d20 (3), d2 (3) | yes |
| grp_d30_vs_d2 | simple | d30 (3), d2 (3) | yes |
| grp_d30_vs_d20 | simple | d30 (3), d20 (3) | yes |
