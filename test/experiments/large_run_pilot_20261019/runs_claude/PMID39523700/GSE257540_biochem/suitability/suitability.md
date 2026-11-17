# Suitability: GSE257540_biochem

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (nf-core STAR/Salmon gene-level counts, deposited as integers); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 3 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 4/4 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 14 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_EX_vs_C | simple | EX (4), C (5) | yes |
| grp_SP_vs_C | simple | SP (5), C (5) | yes |
| grp_SP_vs_EX | simple | SP (5), EX (4) | yes |
| grp_EX_vs_SP | simple | EX (4), SP (5) | yes |
