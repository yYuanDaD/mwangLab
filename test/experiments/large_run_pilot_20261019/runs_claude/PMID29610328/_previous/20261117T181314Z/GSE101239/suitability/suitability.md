# Suitability: GSE101239

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 3 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_VPA_vs_Ctrl | simple | VPA (3), Ctrl (3) | yes |
| grp_VPARun_vs_Ctrl | simple | VPARun (3), Ctrl (3) | yes |
| grp_VPARun_vs_VPA | simple | VPARun (3), VPA (3) | yes |
