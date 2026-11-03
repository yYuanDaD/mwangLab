# Suitability: GSE164890

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | ex: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures) |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| ex_after_vs_before | simple | after (7), before (7) | yes |
