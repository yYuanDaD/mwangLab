# Suitability: PMID42277794

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | ex: 2 levels; exo: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| ex_EXT_vs_SED_exo-ctrl | simple | ctrl/EXT (3), ctrl/SED (3) | yes |
| ex_EXT_vs_SED_exo-exo | simple | exo/EXT (3), exo/SED (3) | yes |
| exo_exo_vs_ctrl_ex-EXT | simple | EXT/exo (3), EXT/ctrl (3) | yes |
| exo_exo_vs_ctrl_ex-SED | simple | SED/exo (3), SED/ctrl (3) | yes |
| ex_exo_EXT_exo_vs_SED_ctrl | interaction | EXT/exo (3), SED/exo (3), EXT/ctrl (3), SED/ctrl (3) | yes |
