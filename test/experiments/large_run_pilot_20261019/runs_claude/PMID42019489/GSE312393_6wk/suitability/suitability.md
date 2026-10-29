# Suitability: GSE312393_6wk

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | TPM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | trt: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures) |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| trt_POST_vs_PRE | simple | POST (3), PRE (3) | yes |
