# Suitability: GSE236402

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | disease: 2 levels; time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information); disease: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| disease_ME_vs_HC_time-BL | simple | BL/ME (3), BL/HC (3) | yes |
| disease_ME_vs_HC_time-PC | simple | PC/ME (3), PC/HC (3) | yes |
| time_PC_vs_BL_disease-HC | simple | HC/PC (3), HC/BL (3) | yes |
| time_PC_vs_BL_disease-ME | simple | ME/PC (3), ME/BL (3) | yes |
| disease_time_ME_PC_vs_HC_BL | interaction | ME/PC (3), HC/PC (3), ME/BL (3), HC/BL (3) | yes |
