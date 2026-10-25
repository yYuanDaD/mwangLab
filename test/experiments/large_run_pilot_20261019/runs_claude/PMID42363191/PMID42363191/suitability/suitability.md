# Suitability: PMID42363191

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | tumor: 2 levels; ex: 2 levels |
| Covariance | pass | not_required; characteristics_ch1.3.batch: omit (constant: carries no batch information); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| tumor_yes_vs_no_ex-ex | simple | ex/yes (4), ex/no (4) | yes |
| tumor_yes_vs_no_ex-sed | simple | sed/yes (4), sed/no (4) | yes |
| ex_ex_vs_sed_tumor-no | simple | no/ex (4), no/sed (4) | yes |
| ex_ex_vs_sed_tumor-yes | simple | yes/ex (4), yes/sed (4) | yes |
| tumor_ex_yes_ex_vs_no_sed | interaction | yes/ex (4), no/ex (4), yes/sed (4), no/sed (4) | yes |
