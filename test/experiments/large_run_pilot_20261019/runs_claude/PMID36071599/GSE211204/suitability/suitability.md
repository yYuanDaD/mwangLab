# Suitability: GSE211204

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 3 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 4/4 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 31 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_AR_vs_BL | simple | AR (9), BL (11) | yes |
| time_ULLS_vs_AR | simple | ULLS (11), AR (9) | yes |
| time_ULLS_vs_BL | simple | ULLS (11), BL (11) | yes |
| time_AR_vs_ULLS | simple | AR (9), ULLS (11) | yes |
