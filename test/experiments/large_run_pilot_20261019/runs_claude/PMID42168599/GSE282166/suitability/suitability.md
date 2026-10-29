# Suitability: GSE282166

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 2 levels |
| Covariance | pass | not_required; animal: omit (one sample per subject per factor level set: an identifier, not a block); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 2/2 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_IRISIN_vs_GFP_frac-NeuNneg | simple | NeuNneg/IRISIN (3), NeuNneg/GFP (3) | yes |
| grp_IRISIN_vs_GFP_frac-NeuNpos | simple | NeuNpos/IRISIN (3), NeuNpos/GFP (3) | yes |
