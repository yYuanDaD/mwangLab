# Suitability: GSE299413_tumor

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | DESeq2 median-ratio normalized counts (linear, non-integer); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 8 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_CAEX_vs_CA | simple | CAEX (4), CA (4) | yes |
