# Suitability: GSE188236

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | normalized counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | trt: 3 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| trt_tgfb_vs_ctrl | simple | tgfb (5), ctrl (5) | yes |
| trt_tgfbsb_vs_ctrl | simple | tgfbsb (5), ctrl (5) | yes |
| trt_tgfbsb_vs_tgfb | simple | tgfbsb (5), tgfb (5) | yes |
