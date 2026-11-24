# Suitability: GSE205891

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | log2 CPM (moderated, prior count; edgeR-style log-CPM); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 4/4 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 62 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_post_vs_pre_tissue-fat_arm-ILT | simple | fat/ILT/post (10), fat/ILT/pre (10) | yes |
| time_post_vs_pre_tissue-fat_arm-SC | simple | fat/SC/post (7), fat/SC/pre (7) | yes |
| time_post_vs_pre_tissue-muscle_arm-ILT | simple | muscle/ILT/post (8), muscle/ILT/pre (8) | yes |
| time_post_vs_pre_tissue-muscle_arm-SC | simple | muscle/SC/post (6), muscle/SC/pre (6) | yes |
