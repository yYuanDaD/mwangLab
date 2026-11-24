# Suitability: GSE102284

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | age: 2 levels; cond: 3 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 36 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| age_O_vs_Y_cond-CON | simple | CON/O (9), CON/Y (9) | yes |
| age_O_vs_Y_cond-RL | simple | RL/O (4), RL/Y (4) | yes |
| age_O_vs_Y_cond-UN | simple | UN/O (6), UN/Y (4) | yes |
| cond_RL_vs_CON_age-O | simple | O/RL (4), O/CON (9) | yes |
| cond_UN_vs_CON_age-O | simple | O/UN (6), O/CON (9) | yes |
| cond_UN_vs_RL_age-O | simple | O/UN (6), O/RL (4) | yes |
| cond_RL_vs_CON_age-Y | simple | Y/RL (4), Y/CON (9) | yes |
| cond_UN_vs_CON_age-Y | simple | Y/UN (4), Y/CON (9) | yes |
| cond_UN_vs_RL_age-Y | simple | Y/UN (4), Y/RL (4) | yes |
| age_cond_O_RL_vs_Y_CON | interaction | O/RL (4), Y/RL (4), O/CON (9), Y/CON (9) | yes |
| age_cond_O_UN_vs_Y_CON | interaction | O/UN (6), Y/UN (4), O/CON (9), Y/CON (9) | yes |
