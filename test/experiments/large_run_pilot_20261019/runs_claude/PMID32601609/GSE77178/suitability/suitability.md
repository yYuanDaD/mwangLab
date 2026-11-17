# Suitability: GSE77178

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | normalized FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 8/8 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 21 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_OEx_vs_OSed | simple | OEx (5), OSed (7) | yes |
| grp_YEx_vs_OEx | simple | YEx (3), OEx (5) | yes |
| grp_YSed_vs_OEx | simple | YSed (6), OEx (5) | yes |
| grp_YEx_vs_OSed | simple | YEx (3), OSed (7) | yes |
| grp_YSed_vs_OSed | simple | YSed (6), OSed (7) | yes |
| grp_YSed_vs_YEx | simple | YSed (6), YEx (3) | yes |
| grp_OSed_vs_YSed | simple | OSed (7), YSed (6) | yes |
| grp_YEx_vs_YSed | simple | YEx (3), YSed (6) | yes |
