# Suitability: GSE310858

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 2 levels |
| Covariance | pass | not_required; subject: omit (one sample per subject per factor level set: an identifier, not a block) |
| Sample size | pass | 2/2 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 48 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_after_vs_before_tissue-Sol | simple | Sol/after (12), Sol/before (12) | yes |
| time_after_vs_before_tissue-Vas | simple | Vas/after (12), Vas/before (12) | yes |
