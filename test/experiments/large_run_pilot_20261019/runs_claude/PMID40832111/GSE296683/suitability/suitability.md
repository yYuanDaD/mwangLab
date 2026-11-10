# Suitability: GSE296683

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | cohort: 2 levels; trt: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| cohort_OS_vs_YA_trt-tomatidine | simple | tomatidine/OS (3), tomatidine/YA (3) | yes |
| cohort_OS_vs_YA_trt-vehicle | simple | vehicle/OS (3), vehicle/YA (3) | yes |
| trt_tomatidine_vs_vehicle_cohort-OS | simple | OS/tomatidine (3), OS/vehicle (3) | yes |
| trt_tomatidine_vs_vehicle_cohort-YA | simple | YA/tomatidine (3), YA/vehicle (3) | yes |
| cohort_trt_OS_tomatidine_vs_YA_vehicle | interaction | OS/tomatidine (3), YA/tomatidine (3), OS/vehicle (3), YA/vehicle (3) | yes |
