# Suitability: GSE228869

Verdict: **not_analyzable** (failed: sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 3 levels; diff: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | fail | 0/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_HS14_vs_C_diff-d0 | simple | d0/HS14 (2), d0/C (2) | no |
| grp_HS7_vs_C_diff-d0 | simple | d0/HS7 (2), d0/C (2) | no |
| grp_HS7_vs_HS14_diff-d0 | simple | d0/HS7 (2), d0/HS14 (2) | no |
| grp_HS14_vs_C_diff-d3 | simple | d3/HS14 (2), d3/C (2) | no |
| grp_HS7_vs_C_diff-d3 | simple | d3/HS7 (2), d3/C (2) | no |
| grp_HS7_vs_HS14_diff-d3 | simple | d3/HS7 (2), d3/HS14 (2) | no |
| diff_d3_vs_d0_grp-C | simple | C/d3 (2), C/d0 (2) | no |
| diff_d3_vs_d0_grp-HS14 | simple | HS14/d3 (2), HS14/d0 (2) | no |
| diff_d3_vs_d0_grp-HS7 | simple | HS7/d3 (2), HS7/d0 (2) | no |
| grp_diff_HS14_d3_vs_C_d0 | interaction | HS14/d3 (2), C/d3 (2), HS14/d0 (2), C/d0 (2) | no |
| grp_diff_HS7_d3_vs_C_d0 | interaction | HS7/d3 (2), C/d3 (2), HS7/d0 (2), C/d0 (2) | no |
