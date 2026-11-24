# Suitability: GSE192982

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | log2(TMM-normalized count + 1) from Partek, low-count filtered; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | cond: 3 levels |
| Covariance | pass | required; donor: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| cond_SMG_vs_CHP | simple | SMG (8), CHP (8) | yes |
| cond_CHP_vs_Static | simple | CHP (8), Static (8) | yes |
| cond_SMG_vs_Static | simple | SMG (8), Static (8) | yes |
