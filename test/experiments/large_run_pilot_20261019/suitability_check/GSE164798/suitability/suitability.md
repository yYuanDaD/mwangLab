# Suitability: GSE164798

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | genotype: 2 levels; activity: 3 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| genotype_tg_vs_wt_activity-acu | simple | acu/tg (4), acu/wt (4) | yes |
| genotype_tg_vs_wt_activity-chr | simple | chr/tg (4), chr/wt (4) | yes |
| genotype_tg_vs_wt_activity-sed | simple | sed/tg (4), sed/wt (4) | yes |
| activity_chr_vs_acu_genotype-tg | simple | tg/chr (4), tg/acu (4) | yes |
| activity_acu_vs_sed_genotype-tg | simple | tg/acu (4), tg/sed (4) | yes |
| activity_chr_vs_sed_genotype-tg | simple | tg/chr (4), tg/sed (4) | yes |
| activity_chr_vs_acu_genotype-wt | simple | wt/chr (4), wt/acu (4) | yes |
| activity_acu_vs_sed_genotype-wt | simple | wt/acu (4), wt/sed (4) | yes |
| activity_chr_vs_sed_genotype-wt | simple | wt/chr (4), wt/sed (4) | yes |
| genotype_activity_tg_acu_vs_wt_sed | interaction | tg/acu (4), wt/acu (4), tg/sed (4), wt/sed (4) | yes |
| genotype_activity_tg_chr_vs_wt_sed | interaction | tg/chr (4), wt/chr (4), tg/sed (4), wt/sed (4) | yes |
