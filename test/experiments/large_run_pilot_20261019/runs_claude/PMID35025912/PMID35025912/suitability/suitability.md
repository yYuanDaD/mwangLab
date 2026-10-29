# Suitability: PMID35025912

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | tis: 2 levels; line: 2 levels; trt: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 18/18 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 48 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| tis_SOL_vs_PLN_line-HRT_trt-CTRL | simple | HRT/CTRL/SOL (6), HRT/CTRL/PLN (6) | yes |
| tis_SOL_vs_PLN_line-HRT_trt-HI | simple | HRT/HI/SOL (6), HRT/HI/PLN (6) | yes |
| tis_SOL_vs_PLN_line-LRT_trt-CTRL | simple | LRT/CTRL/SOL (6), LRT/CTRL/PLN (6) | yes |
| tis_SOL_vs_PLN_line-LRT_trt-HI | simple | LRT/HI/SOL (6), LRT/HI/PLN (6) | yes |
| line_LRT_vs_HRT_tis-PLN_trt-CTRL | simple | PLN/CTRL/LRT (6), PLN/CTRL/HRT (6) | yes |
| line_LRT_vs_HRT_tis-PLN_trt-HI | simple | PLN/HI/LRT (6), PLN/HI/HRT (6) | yes |
| line_LRT_vs_HRT_tis-SOL_trt-CTRL | simple | SOL/CTRL/LRT (6), SOL/CTRL/HRT (6) | yes |
| line_LRT_vs_HRT_tis-SOL_trt-HI | simple | SOL/HI/LRT (6), SOL/HI/HRT (6) | yes |
| trt_HI_vs_CTRL_tis-PLN_line-HRT | simple | PLN/HRT/HI (6), PLN/HRT/CTRL (6) | yes |
| trt_HI_vs_CTRL_tis-PLN_line-LRT | simple | PLN/LRT/HI (6), PLN/LRT/CTRL (6) | yes |
| trt_HI_vs_CTRL_tis-SOL_line-HRT | simple | SOL/HRT/HI (6), SOL/HRT/CTRL (6) | yes |
| trt_HI_vs_CTRL_tis-SOL_line-LRT | simple | SOL/LRT/HI (6), SOL/LRT/CTRL (6) | yes |
| tis_line_SOL_LRT_vs_PLN_HRT_trt-CTRL | interaction | CTRL/SOL/LRT (6), CTRL/PLN/LRT (6), CTRL/SOL/HRT (6), CTRL/PLN/HRT (6) | yes |
| tis_line_SOL_LRT_vs_PLN_HRT_trt-HI | interaction | HI/SOL/LRT (6), HI/PLN/LRT (6), HI/SOL/HRT (6), HI/PLN/HRT (6) | yes |
| tis_trt_SOL_HI_vs_PLN_CTRL_line-HRT | interaction | HRT/SOL/HI (6), HRT/PLN/HI (6), HRT/SOL/CTRL (6), HRT/PLN/CTRL (6) | yes |
| tis_trt_SOL_HI_vs_PLN_CTRL_line-LRT | interaction | LRT/SOL/HI (6), LRT/PLN/HI (6), LRT/SOL/CTRL (6), LRT/PLN/CTRL (6) | yes |
| line_trt_LRT_HI_vs_HRT_CTRL_tis-PLN | interaction | PLN/LRT/HI (6), PLN/HRT/HI (6), PLN/LRT/CTRL (6), PLN/HRT/CTRL (6) | yes |
| line_trt_LRT_HI_vs_HRT_CTRL_tis-SOL | interaction | SOL/LRT/HI (6), SOL/HRT/HI (6), SOL/LRT/CTRL (6), SOL/HRT/CTRL (6) | yes |
