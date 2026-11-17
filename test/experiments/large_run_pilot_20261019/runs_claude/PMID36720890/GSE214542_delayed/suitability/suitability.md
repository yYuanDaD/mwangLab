# Suitability: GSE214542_delayed

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_IRIS_vs_CTRL | simple | IRIS (3), CTRL (3) | yes |
| grp_CTRL_vs_MPTP | simple | CTRL (3), MPTP (3) | yes |
| grp_MPTPIRIS_vs_CTRL | simple | MPTPIRIS (3), CTRL (3) | yes |
| grp_IRIS_vs_MPTP | simple | IRIS (3), MPTP (3) | yes |
| grp_MPTPIRIS_vs_IRIS | simple | MPTPIRIS (3), IRIS (3) | yes |
| grp_MPTPIRIS_vs_MPTP | simple | MPTPIRIS (3), MPTP (3) | yes |
