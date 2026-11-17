# Suitability: GSE152919

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | geno: 2 levels; time: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_KO_vs_WT_time-CT16 | simple | CT16/KO (4), CT16/WT (5) | yes |
| geno_KO_vs_WT_time-CT4 | simple | CT4/KO (3), CT4/WT (3) | yes |
| time_CT4_vs_CT16_geno-KO | simple | KO/CT4 (3), KO/CT16 (4) | yes |
| time_CT4_vs_CT16_geno-WT | simple | WT/CT4 (3), WT/CT16 (5) | yes |
| geno_time_KO_CT4_vs_WT_CT16 | interaction | KO/CT4 (3), WT/CT4 (3), KO/CT16 (4), WT/CT16 (5) | yes |
