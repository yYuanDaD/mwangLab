# Suitability: GSE123879

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 3 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_MTG_vs_EX | simple | MTG (5), EX (5) | yes |
| grp_EX_vs_SED | simple | EX (5), SED (5) | yes |
| grp_MTG_vs_SED | simple | MTG (5), SED (5) | yes |
