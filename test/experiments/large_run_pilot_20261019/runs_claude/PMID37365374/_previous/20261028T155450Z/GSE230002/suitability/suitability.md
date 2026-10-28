# Suitability: GSE230002

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | log2 CPM (edgeR moderated log2CPM, prior count), gene symbols; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures) |
| Sample size | pass | 2/2 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 26 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_Post_vs_Pre_arm-DIET | simple | DIET/Post (6), DIET/Pre (6) | yes |
| time_Post_vs_Pre_arm-EX | simple | EX/Post (7), EX/Pre (7) | yes |
