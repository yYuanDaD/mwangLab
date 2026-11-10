# Suitability: GSE237736

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 8/8 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_KOsed_vs_KOrun | simple | KOsed (4), KOrun (4) | yes |
| grp_WTrun_vs_KOrun | simple | WTrun (4), KOrun (4) | yes |
| grp_KOrun_vs_WTsed | simple | KOrun (4), WTsed (4) | yes |
| grp_WTrun_vs_KOsed | simple | WTrun (4), KOsed (4) | yes |
| grp_KOsed_vs_WTsed | simple | KOsed (4), WTsed (4) | yes |
| grp_WTrun_vs_WTsed | simple | WTrun (4), WTsed (4) | yes |
| grp_KOrun_vs_KOsed | simple | KOrun (4), KOsed (4) | yes |
| grp_KOrun_vs_WTrun | simple | KOrun (4), WTrun (4) | yes |
