# Suitability: GSE60833

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | fpkm_or_tpm; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); location: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); sex: omit (makes the design rank deficient); location: omit (makes the design rank deficient) |
| Sample size | pass | 10/10 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 68 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_T4_vs_T3 | simple | T4 (10), T3 (13) | yes |
| grp_U2_vs_T3 | simple | U2 (21), T3 (13) | yes |
| grp_U3_vs_T3 | simple | U3 (12), T3 (13) | yes |
| grp_U4_vs_T3 | simple | U4 (12), T3 (13) | yes |
| grp_U2_vs_T4 | simple | U2 (21), T4 (10) | yes |
| grp_U3_vs_T4 | simple | U3 (12), T4 (10) | yes |
| grp_U4_vs_T4 | simple | U4 (12), T4 (10) | yes |
| grp_U3_vs_U2 | simple | U3 (12), U2 (21) | yes |
| grp_U4_vs_U2 | simple | U4 (12), U2 (21) | yes |
| grp_U4_vs_U3 | simple | U4 (12), U3 (12) | yes |
