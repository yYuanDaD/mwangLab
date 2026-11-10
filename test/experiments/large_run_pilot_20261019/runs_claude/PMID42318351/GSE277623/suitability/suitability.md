# Suitability: GSE277623

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 7 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | partial | 4/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 19 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_Con5W_vs_PBS9W | simple | Con5W (3), PBS9W (3) | yes |
| grp_Con9W_vs_PBS9W | simple | Con9W (3), PBS9W (3) | yes |
| grp_EMPA9W_vs_PBS9W | simple | EMPA9W (2), PBS9W (3) | no |
| grp_EMPAPFD9W_vs_PBS9W | simple | EMPAPFD9W (3), PBS9W (3) | yes |
| grp_HF5W_vs_PBS9W | simple | HF5W (3), PBS9W (3) | yes |
| grp_PFD9W_vs_PBS9W | simple | PFD9W (2), PBS9W (3) | no |
