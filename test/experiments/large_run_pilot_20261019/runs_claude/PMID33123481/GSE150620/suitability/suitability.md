# Suitability: GSE150620

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | linear normalized CPM (floored at 1); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | act_raw: 2 levels; lip_raw: 2 levels |
| Covariance | pass | not_required; lip_raw: omit (same grouping as design factor lip_raw (its source column)) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 22 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| act_raw_wheel_vs_sed_lip_raw-clo | simple | clo/wheel (5), clo/sed (5) | yes |
| act_raw_wheel_vs_sed_lip_raw-pbs | simple | pbs/wheel (6), pbs/sed (6) | yes |
| lip_raw_clo_vs_pbs_act_raw-sed | simple | sed/clo (5), sed/pbs (6) | yes |
| lip_raw_clo_vs_pbs_act_raw-wheel | simple | wheel/clo (5), wheel/pbs (6) | yes |
| act_raw_lip_raw_wheel_clo_vs_sed_pbs | interaction | wheel/clo (5), sed/clo (5), wheel/pbs (6), sed/pbs (6) | yes |
