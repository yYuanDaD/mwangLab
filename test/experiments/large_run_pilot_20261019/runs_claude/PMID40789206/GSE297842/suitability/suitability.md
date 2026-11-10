# Suitability: GSE297842

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_H24_vs_SED | simple | H24 (4), SED (4) | yes |
| grp_W1_vs_H24 | simple | W1 (4), H24 (4) | yes |
| grp_W2_vs_H24 | simple | W2 (4), H24 (4) | yes |
| grp_W1_vs_SED | simple | W1 (4), SED (4) | yes |
| grp_W2_vs_SED | simple | W2 (4), SED (4) | yes |
| grp_W2_vs_W1 | simple | W2 (4), W1 (4) | yes |
