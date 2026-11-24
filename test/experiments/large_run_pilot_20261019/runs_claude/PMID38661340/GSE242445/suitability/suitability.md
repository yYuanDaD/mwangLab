# Suitability: GSE242445

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | normalized counts (DESeq2 median-of-ratios); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | geno: 2 levels; sex: 2 levels; diet: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | partial | 12/18 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 23 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_KO_vs_WT_sex-F_diet-C | simple | F/C/KO (3), F/C/WT (3) | yes |
| geno_KO_vs_WT_sex-F_diet-LC | simple | F/LC/KO (2), F/LC/WT (3) | no |
| geno_KO_vs_WT_sex-M_diet-C | simple | M/C/KO (3), M/C/WT (3) | yes |
| geno_KO_vs_WT_sex-M_diet-LC | simple | M/LC/KO (3), M/LC/WT (3) | yes |
| sex_F_vs_M_geno-KO_diet-C | simple | KO/C/F (3), KO/C/M (3) | yes |
| sex_F_vs_M_geno-KO_diet-LC | simple | KO/LC/F (2), KO/LC/M (3) | no |
| sex_F_vs_M_geno-WT_diet-C | simple | WT/C/F (3), WT/C/M (3) | yes |
| sex_F_vs_M_geno-WT_diet-LC | simple | WT/LC/F (3), WT/LC/M (3) | yes |
| diet_LC_vs_C_geno-KO_sex-F | simple | KO/F/LC (2), KO/F/C (3) | no |
| diet_LC_vs_C_geno-KO_sex-M | simple | KO/M/LC (3), KO/M/C (3) | yes |
| diet_LC_vs_C_geno-WT_sex-F | simple | WT/F/LC (3), WT/F/C (3) | yes |
| diet_LC_vs_C_geno-WT_sex-M | simple | WT/M/LC (3), WT/M/C (3) | yes |
| geno_sex_KO_F_vs_WT_M_diet-C | interaction | C/KO/F (3), C/WT/F (3), C/KO/M (3), C/WT/M (3) | yes |
| geno_sex_KO_F_vs_WT_M_diet-LC | interaction | LC/KO/F (2), LC/WT/F (3), LC/KO/M (3), LC/WT/M (3) | no |
| geno_diet_KO_LC_vs_WT_C_sex-F | interaction | F/KO/LC (2), F/WT/LC (3), F/KO/C (3), F/WT/C (3) | no |
| geno_diet_KO_LC_vs_WT_C_sex-M | interaction | M/KO/LC (3), M/WT/LC (3), M/KO/C (3), M/WT/C (3) | yes |
| sex_diet_F_LC_vs_M_C_geno-KO | interaction | KO/F/LC (2), KO/M/LC (3), KO/F/C (3), KO/M/C (3) | no |
| sex_diet_F_LC_vs_M_C_geno-WT | interaction | WT/F/LC (3), WT/M/LC (3), WT/F/C (3), WT/M/C (3) | yes |
