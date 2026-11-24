# Suitability: GSE240814_female

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | DESeq2 median-ratio normalized counts (linear, non-integer); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | time: 5 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 10/10 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_h24_vs_h0 | simple | h24 (8), h0 (8) | yes |
| time_h48_vs_h0 | simple | h48 (8), h0 (8) | yes |
| time_h72_vs_h0 | simple | h72 (8), h0 (8) | yes |
| time_h168_vs_h0 | simple | h168 (7), h0 (8) | yes |
| time_h48_vs_h24 | simple | h48 (8), h24 (8) | yes |
| time_h72_vs_h24 | simple | h72 (8), h24 (8) | yes |
| time_h168_vs_h24 | simple | h168 (7), h24 (8) | yes |
| time_h72_vs_h48 | simple | h72 (8), h48 (8) | yes |
| time_h168_vs_h48 | simple | h168 (7), h48 (8) | yes |
| time_h168_vs_h72 | simple | h168 (7), h72 (8) | yes |
