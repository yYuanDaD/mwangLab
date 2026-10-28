# Suitability: GSE302911

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | TPM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 7 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | partial | 4/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 19 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_T0_vs_SED | simple | T0 (2), SED (3) | no |
| grp_T6_vs_SED | simple | T6 (3), SED (3) | yes |
| grp_T72_vs_SED | simple | T72 (3), SED (3) | yes |
| grp_U0_vs_SED | simple | U0 (2), SED (3) | no |
| grp_U6_vs_SED | simple | U6 (3), SED (3) | yes |
| grp_U72_vs_SED | simple | U72 (3), SED (3) | yes |
