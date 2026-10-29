# Suitability: GSE289569

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | geno: 2 levels; train: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_KO_vs_WT_train-SED | simple | SED/KO (3), SED/WT (3) | yes |
| geno_KO_vs_WT_train-TR | simple | TR/KO (3), TR/WT (3) | yes |
| train_TR_vs_SED_geno-KO | simple | KO/TR (3), KO/SED (3) | yes |
| train_TR_vs_SED_geno-WT | simple | WT/TR (3), WT/SED (3) | yes |
| geno_train_KO_TR_vs_WT_SED | interaction | KO/TR (3), WT/TR (3), KO/SED (3), WT/SED (3) | yes |
