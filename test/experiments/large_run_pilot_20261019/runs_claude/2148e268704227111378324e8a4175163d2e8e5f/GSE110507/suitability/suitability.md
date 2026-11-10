# Suitability: GSE110507

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | vdr: 4 levels |
| Covariance | pass | not_required; subject: omit (one sample per subject per factor level set: an identifier, not a block); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 28 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| vdr_KDctrl_vs_KD | simple | KDctrl (7), KD (7) | yes |
| vdr_OE_vs_KD | simple | OE (7), KD (7) | yes |
| vdr_KD_vs_OEctrl | simple | KD (7), OEctrl (7) | yes |
| vdr_OE_vs_KDctrl | simple | OE (7), KDctrl (7) | yes |
| vdr_KDctrl_vs_OEctrl | simple | KDctrl (7), OEctrl (7) | yes |
| vdr_OE_vs_OEctrl | simple | OE (7), OEctrl (7) | yes |
