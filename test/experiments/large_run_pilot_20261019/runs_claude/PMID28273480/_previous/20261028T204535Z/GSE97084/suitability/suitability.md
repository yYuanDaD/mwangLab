# Suitability: GSE97084

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); batch: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); batch: omit (makes the design rank deficient) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 103 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_Post_vs_Pre_cohort-Old_CT | simple | Old_CT/Post (7), Old_CT/Pre (7) | yes |
| time_Post_vs_Pre_cohort-Old_HIIT | simple | Old_HIIT/Post (8), Old_HIIT/Pre (8) | yes |
| time_Post_vs_Pre_cohort-Old_RT | simple | Old_RT/Post (8), Old_RT/Pre (8) | yes |
| time_Post_vs_Pre_cohort-Young_CT | simple | Young_CT/Post (7), Young_CT/Pre (8) | yes |
| time_Post_vs_Pre_cohort-Young_HIIT | simple | Young_HIIT/Post (11), Young_HIIT/Pre (11) | yes |
| time_Post_vs_Pre_cohort-Young_RT | simple | Young_RT/Post (10), Young_RT/Pre (10) | yes |
