# Suitability: GSE324210

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 4 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); subject: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); subject: omit (makes the design rank deficient) |
| Sample size | pass | 12/12 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 83 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_T2_vs_T1_sex-female | simple | female/T2 (9), female/T1 (9) | yes |
| time_T3_vs_T1_sex-female | simple | female/T3 (9), female/T1 (9) | yes |
| time_T4_vs_T1_sex-female | simple | female/T4 (8), female/T1 (9) | yes |
| time_T3_vs_T2_sex-female | simple | female/T3 (9), female/T2 (9) | yes |
| time_T4_vs_T2_sex-female | simple | female/T4 (8), female/T2 (9) | yes |
| time_T4_vs_T3_sex-female | simple | female/T4 (8), female/T3 (9) | yes |
| time_T2_vs_T1_sex-male | simple | male/T2 (12), male/T1 (12) | yes |
| time_T3_vs_T1_sex-male | simple | male/T3 (12), male/T1 (12) | yes |
| time_T4_vs_T1_sex-male | simple | male/T4 (12), male/T1 (12) | yes |
| time_T3_vs_T2_sex-male | simple | male/T3 (12), male/T2 (12) | yes |
| time_T4_vs_T2_sex-male | simple | male/T4 (12), male/T2 (12) | yes |
| time_T4_vs_T3_sex-male | simple | male/T4 (12), male/T3 (12) | yes |
