# Suitability: GSE123961

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | log2 CPM (edgeR cpm, low-expression filtered), normalized expression; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | tissue: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| tissue_DG_vs_SVZ | simple | DG (5), SVZ (4) | yes |
