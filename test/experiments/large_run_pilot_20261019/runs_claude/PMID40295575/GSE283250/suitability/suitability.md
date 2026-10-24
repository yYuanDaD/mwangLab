# Suitability: GSE283250

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; animal_no: omit (one sample per subject per factor level set: an identifier, not a block); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_SER_vs_CON | simple | SER (3), CON (3) | yes |
| grp_SES_vs_CON | simple | SES (3), CON (3) | yes |
| grp_SS_vs_CON | simple | SS (3), CON (3) | yes |
| grp_SES_vs_SER | simple | SES (3), SER (3) | yes |
| grp_SS_vs_SER | simple | SS (3), SER (3) | yes |
| grp_SS_vs_SES | simple | SS (3), SES (3) | yes |
