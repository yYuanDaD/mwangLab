# Suitability: GSE237950

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | partial | 7/12 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference completed on 22 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_CE_vs_C_tissue-fat | simple | fat/CE (3), fat/C (3) | yes |
| grp_H_vs_C_tissue-fat | simple | fat/H (2), fat/C (3) | no |
| grp_HE_vs_C_tissue-fat | simple | fat/HE (2), fat/C (3) | no |
| grp_H_vs_CE_tissue-fat | simple | fat/H (2), fat/CE (3) | no |
| grp_HE_vs_CE_tissue-fat | simple | fat/HE (2), fat/CE (3) | no |
| grp_HE_vs_H_tissue-fat | simple | fat/HE (2), fat/H (2) | no |
| grp_CE_vs_C_tissue-muscle | simple | muscle/CE (3), muscle/C (3) | yes |
| grp_H_vs_C_tissue-muscle | simple | muscle/H (3), muscle/C (3) | yes |
| grp_HE_vs_C_tissue-muscle | simple | muscle/HE (3), muscle/C (3) | yes |
| grp_H_vs_CE_tissue-muscle | simple | muscle/H (3), muscle/CE (3) | yes |
| grp_HE_vs_CE_tissue-muscle | simple | muscle/HE (3), muscle/CE (3) | yes |
| grp_HE_vs_H_tissue-muscle | simple | muscle/HE (3), muscle/H (3) | yes |
