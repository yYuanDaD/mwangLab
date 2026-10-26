# Suitability: GSE129962

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | geno: 2 levels; cond: 3 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_DH_vs_WT_cond-EX6 | simple | EX6/DH (5), EX6/WT (5) | yes |
| geno_DH_vs_WT_cond-RA3 | simple | RA3/DH (5), RA3/WT (5) | yes |
| geno_DH_vs_WT_cond-RA6 | simple | RA6/DH (5), RA6/WT (5) | yes |
| cond_RA3_vs_EX6_geno-DH | simple | DH/RA3 (5), DH/EX6 (5) | yes |
| cond_EX6_vs_RA6_geno-DH | simple | DH/EX6 (5), DH/RA6 (5) | yes |
| cond_RA3_vs_RA6_geno-DH | simple | DH/RA3 (5), DH/RA6 (5) | yes |
| cond_RA3_vs_EX6_geno-WT | simple | WT/RA3 (5), WT/EX6 (5) | yes |
| cond_EX6_vs_RA6_geno-WT | simple | WT/EX6 (5), WT/RA6 (5) | yes |
| cond_RA3_vs_RA6_geno-WT | simple | WT/RA3 (5), WT/RA6 (5) | yes |
| geno_cond_DH_EX6_vs_WT_RA6 | interaction | DH/EX6 (5), WT/EX6 (5), DH/RA6 (5), WT/RA6 (5) | yes |
| geno_cond_DH_RA3_vs_WT_RA6 | interaction | DH/RA3 (5), WT/RA3 (5), DH/RA6 (5), WT/RA6 (5) | yes |
