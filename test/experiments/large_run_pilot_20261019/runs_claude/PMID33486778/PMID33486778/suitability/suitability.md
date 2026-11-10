# Suitability: PMID33486778

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | line: 2 levels; load: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| line_LRT_vs_HRT_load-CTRL | simple | CTRL/LRT (6), CTRL/HRT (6) | yes |
| line_LRT_vs_HRT_load-FO | simple | FO/LRT (6), FO/HRT (6) | yes |
| load_FO_vs_CTRL_line-HRT | simple | HRT/FO (6), HRT/CTRL (6) | yes |
| load_FO_vs_CTRL_line-LRT | simple | LRT/FO (6), LRT/CTRL (6) | yes |
| line_load_LRT_FO_vs_HRT_CTRL | interaction | LRT/FO (6), HRT/FO (6), LRT/CTRL (6), HRT/CTRL (6) | yes |
