# Suitability: GSE186045

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | TPM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 2 levels; time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); grp: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 26 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_ex_vs_con_time-post | simple | post/ex (7), post/con (6) | yes |
| grp_ex_vs_con_time-pre | simple | pre/ex (7), pre/con (6) | yes |
| time_post_vs_pre_grp-con | simple | con/post (6), con/pre (6) | yes |
| time_post_vs_pre_grp-ex | simple | ex/post (7), ex/pre (7) | yes |
| grp_time_ex_post_vs_con_pre | interaction | ex/post (7), con/post (6), ex/pre (7), con/pre (6) | yes |
