# Suitability: GSE174210

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | DESeq2-normalized counts (non-integer, linear scale); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | trt: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 10 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| trt_Irisin_vs_GFP | simple | Irisin (5), GFP (5) | yes |
