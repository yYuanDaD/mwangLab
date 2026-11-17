# Suitability: GSE185957

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | linear normalized CPM (edgeR-normalized counts per million); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures) |
| Sample size | pass | 2/2 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_post_vs_pre_status-lean | simple | lean/post (4), lean/pre (4) | yes |
| time_post_vs_pre_status-obese | simple | obese/post (4), obese/pre (4) | yes |
