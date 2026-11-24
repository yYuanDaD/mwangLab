# Suitability: GSE198229_heart

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | trt: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 4/4 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 48 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| trt_EX_vs_SED_strain-ANT1 | simple | ANT1/EX (6), ANT1/SED (6) | yes |
| trt_EX_vs_SED_strain-CO1 | simple | CO1/EX (6), CO1/SED (6) | yes |
| trt_EX_vs_SED_strain-ND5 | simple | ND5/EX (6), ND5/SED (6) | yes |
| trt_EX_vs_SED_strain-ND6 | simple | ND6/EX (6), ND6/SED (6) | yes |
