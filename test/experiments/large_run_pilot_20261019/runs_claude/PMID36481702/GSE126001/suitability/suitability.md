# Suitability: GSE126001

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | linear_normalized (RPKM, CLC Genomics Workbench); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | train: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 2/2 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| train_TR_vs_UT_geno-KO | simple | KO/TR (4), KO/UT (4) | yes |
| train_TR_vs_UT_geno-WT | simple | WT/TR (4), WT/UT (4) | yes |
