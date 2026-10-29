# Suitability: GSE151066

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | cohort: 2 levels; time: 3 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); pool: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); cohort: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 45 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| cohort_act_vs_sed_time-h3 | simple | h3/act (8), h3/sed (7) | yes |
| cohort_act_vs_sed_time-ip | simple | ip/act (8), ip/sed (7) | yes |
| cohort_act_vs_sed_time-pre | simple | pre/act (8), pre/sed (7) | yes |
| time_ip_vs_h3_cohort-act | simple | act/ip (8), act/h3 (8) | yes |
| time_h3_vs_pre_cohort-act | simple | act/h3 (8), act/pre (8) | yes |
| time_ip_vs_pre_cohort-act | simple | act/ip (8), act/pre (8) | yes |
| time_ip_vs_h3_cohort-sed | simple | sed/ip (7), sed/h3 (7) | yes |
| time_h3_vs_pre_cohort-sed | simple | sed/h3 (7), sed/pre (7) | yes |
| time_ip_vs_pre_cohort-sed | simple | sed/ip (7), sed/pre (7) | yes |
| cohort_time_act_h3_vs_sed_pre | interaction | act/h3 (8), sed/h3 (7), act/pre (8), sed/pre (7) | yes |
| cohort_time_act_ip_vs_sed_pre | interaction | act/ip (8), sed/ip (7), act/pre (8), sed/pre (7) | yes |
