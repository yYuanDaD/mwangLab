# Suitability: GSE117161

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | run: 3 levels; time: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 18 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| run_High_vs_Basal_time-ZT14 | simple | ZT14/High (3), ZT14/Basal (3) | yes |
| run_Moderate_vs_Basal_time-ZT14 | simple | ZT14/Moderate (3), ZT14/Basal (3) | yes |
| run_Moderate_vs_High_time-ZT14 | simple | ZT14/Moderate (3), ZT14/High (3) | yes |
| run_High_vs_Basal_time-ZT22 | simple | ZT22/High (3), ZT22/Basal (3) | yes |
| run_Moderate_vs_Basal_time-ZT22 | simple | ZT22/Moderate (3), ZT22/Basal (3) | yes |
| run_Moderate_vs_High_time-ZT22 | simple | ZT22/Moderate (3), ZT22/High (3) | yes |
| time_ZT22_vs_ZT14_run-Basal | simple | Basal/ZT22 (3), Basal/ZT14 (3) | yes |
| time_ZT22_vs_ZT14_run-High | simple | High/ZT22 (3), High/ZT14 (3) | yes |
| time_ZT22_vs_ZT14_run-Moderate | simple | Moderate/ZT22 (3), Moderate/ZT14 (3) | yes |
| run_time_High_ZT22_vs_Basal_ZT14 | interaction | High/ZT22 (3), Basal/ZT22 (3), High/ZT14 (3), Basal/ZT14 (3) | yes |
| run_time_Moderate_ZT22_vs_Basal_ZT14 | interaction | Moderate/ZT22 (3), Basal/ZT22 (3), Moderate/ZT14 (3), Basal/ZT14 (3) | yes |
