# Suitability: GSE278016

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 75 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_CRI_vs_CR | simple | CRI (15), CR (15) | yes |
| grp_CRIS_vs_CR | simple | CRIS (15), CR (15) | yes |
| grp_CRS_vs_CR | simple | CRS (15), CR (15) | yes |
| grp_H_vs_CR | simple | H (15), CR (15) | yes |
| grp_CRIS_vs_CRI | simple | CRIS (15), CRI (15) | yes |
| grp_CRS_vs_CRI | simple | CRS (15), CRI (15) | yes |
| grp_H_vs_CRI | simple | H (15), CRI (15) | yes |
| grp_CRS_vs_CRIS | simple | CRS (15), CRIS (15) | yes |
| grp_H_vs_CRIS | simple | H (15), CRIS (15) | yes |
| grp_H_vs_CRS | simple | H (15), CRS (15) | yes |
| grp_CR_vs_H | simple | CR (15), H (15) | yes |
