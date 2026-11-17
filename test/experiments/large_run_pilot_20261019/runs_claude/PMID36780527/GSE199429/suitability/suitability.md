# Suitability: GSE199429

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | CPM normalized (linear scale); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | ex: 2 levels; time: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| ex_RUN_vs_SED_time-ZT15 | simple | ZT15/RUN (6), ZT15/SED (6) | yes |
| ex_RUN_vs_SED_time-ZT3 | simple | ZT3/RUN (6), ZT3/SED (6) | yes |
| time_ZT15_vs_ZT3_ex-RUN | simple | RUN/ZT15 (6), RUN/ZT3 (6) | yes |
| time_ZT15_vs_ZT3_ex-SED | simple | SED/ZT15 (6), SED/ZT3 (6) | yes |
| ex_time_RUN_ZT15_vs_SED_ZT3 | interaction | RUN/ZT15 (6), SED/ZT15 (6), RUN/ZT3 (6), SED/ZT3 (6) | yes |
