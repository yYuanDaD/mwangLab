# Suitability: GSE193771_boys

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | log2 quantile-normalized (voom logCPM); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 2 levels; time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); grp: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 26 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_EX_vs_CON_time-t0 | simple | t0/EX (5), t0/CON (8) | yes |
| grp_EX_vs_CON_time-t1 | simple | t1/EX (5), t1/CON (8) | yes |
| time_t1_vs_t0_grp-CON | simple | CON/t1 (8), CON/t0 (8) | yes |
| time_t1_vs_t0_grp-EX | simple | EX/t1 (5), EX/t0 (5) | yes |
| grp_time_EX_t1_vs_CON_t0 | interaction | EX/t1 (5), CON/t1 (8), EX/t0 (5), CON/t0 (8) | yes |
