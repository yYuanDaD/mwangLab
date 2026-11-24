# Suitability: GSE269698_young_vehicle

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | rlog (DESeq2 regularized log2 counts); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | stim: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| stim_S_vs_N | simple | S (6), N (6) | yes |
