# Suitability: GSE132520

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 7/7 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_MMEX_vs_MMSED | simple | MMEX (4), MMSED (4) | yes |
| grp_VVEX_vs_MMEX | simple | VVEX (4), MMEX (4) | yes |
| grp_VVSED_vs_MMEX | simple | VVSED (4), MMEX (4) | yes |
| grp_VVEX_vs_MMSED | simple | VVEX (4), MMSED (4) | yes |
| grp_VVSED_vs_MMSED | simple | VVSED (4), MMSED (4) | yes |
| grp_VVSED_vs_VVEX | simple | VVSED (4), VVEX (4) | yes |
| grp_VVEX_vs_VVSED | simple | VVEX (4), VVSED (4) | yes |
