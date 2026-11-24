# Suitability: GSE209880

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 3 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); sex: omit (makes the design rank deficient) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 120 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_h3_vs_h24_cohort-HITT | simple | HITT/h3 (19), HITT/h24 (19) | yes |
| time_h24_vs_pre_cohort-HITT | simple | HITT/h24 (19), HITT/pre (19) | yes |
| time_h3_vs_pre_cohort-HITT | simple | HITT/h3 (19), HITT/pre (19) | yes |
| time_h3_vs_h24_cohort-TRAD | simple | TRAD/h3 (21), TRAD/h24 (21) | yes |
| time_h24_vs_pre_cohort-TRAD | simple | TRAD/h24 (21), TRAD/pre (21) | yes |
| time_h3_vs_pre_cohort-TRAD | simple | TRAD/h3 (21), TRAD/pre (21) | yes |
