# Suitability: GSE293163

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | age: 2 levels; time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information); age: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| age_Old_vs_Young_time-Post | simple | Post/Old (8), Post/Young (7) | yes |
| age_Old_vs_Young_time-Pre | simple | Pre/Old (8), Pre/Young (7) | yes |
| time_Post_vs_Pre_age-Old | simple | Old/Post (8), Old/Pre (8) | yes |
| time_Post_vs_Pre_age-Young | simple | Young/Post (7), Young/Pre (7) | yes |
| age_time_Old_Post_vs_Young_Pre | interaction | Old/Post (8), Young/Post (7), Old/Pre (8), Young/Pre (7) | yes |
