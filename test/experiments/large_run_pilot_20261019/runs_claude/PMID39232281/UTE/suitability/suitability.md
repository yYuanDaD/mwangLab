# Suitability: UTE

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | trt: 2 levels; zt: 2 levels |
| Covariance | pass | not_required; libstyle: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| trt_def_vs_ctrl_zt-zt05 | simple | zt05/def (3), zt05/ctrl (3) | yes |
| trt_def_vs_ctrl_zt-zt17 | simple | zt17/def (3), zt17/ctrl (3) | yes |
| zt_zt17_vs_zt05_trt-ctrl | simple | ctrl/zt17 (3), ctrl/zt05 (3) | yes |
| zt_zt17_vs_zt05_trt-def | simple | def/zt17 (3), def/zt05 (3) | yes |
| trt_zt_def_zt17_vs_ctrl_zt05 | interaction | def/zt17 (3), ctrl/zt17 (3), def/zt05 (3), ctrl/zt05 (3) | yes |
