# Suitability: GSE60591

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); batch: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 45 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_T2_vs_T1 | simple | T2 (22), T1 (23) | yes |
