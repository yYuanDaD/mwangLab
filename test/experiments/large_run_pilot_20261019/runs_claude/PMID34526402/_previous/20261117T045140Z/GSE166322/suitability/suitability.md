# Suitability: GSE166322

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | TPM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 3 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_Ctrl_vs_MDZ | simple | Ctrl (3), MDZ (3) | yes |
| grp_RunMDZ_vs_Ctrl | simple | RunMDZ (3), Ctrl (3) | yes |
| grp_RunMDZ_vs_MDZ | simple | RunMDZ (3), MDZ (3) | yes |
