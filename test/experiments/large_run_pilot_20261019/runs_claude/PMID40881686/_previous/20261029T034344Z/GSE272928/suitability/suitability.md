# Suitability: GSE272928

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | DESeq2 rlog-transformed (log2-scale, library-size normalized) expression; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 2 levels; time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); grp: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model); sex: omit (makes the design rank deficient) |
| Sample size | partial | 5/5 comparisons have >= 3 per group; planned names not found: time_post_vs_pre, grp_ALL_vs_CON |
| Sex | pass | Sex inference completed on 36 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_ALL_vs_CON_time-post | simple | post/ALL (9), post/CON (9) | yes |
| grp_ALL_vs_CON_time-pre | simple | pre/ALL (9), pre/CON (9) | yes |
| time_post_vs_pre_grp-ALL | simple | ALL/post (9), ALL/pre (9) | yes |
| time_post_vs_pre_grp-CON | simple | CON/post (9), CON/pre (9) | yes |
| grp_time_ALL_post_vs_CON_pre | interaction | ALL/post (9), CON/post (9), ALL/pre (9), CON/pre (9) | yes |
