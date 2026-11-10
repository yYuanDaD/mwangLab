# Suitability: GSE128078

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 2 levels; time: 4 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information); grp: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
| Sample size | pass | 19/19 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 97 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_CFS_vs_HC_time-d1 | simple | d1/CFS (14), d1/HC (11) | yes |
| grp_CFS_vs_HC_time-d2 | simple | d2/CFS (14), d2/HC (11) | yes |
| grp_CFS_vs_HC_time-d3 | simple | d3/CFS (13), d3/HC (11) | yes |
| grp_CFS_vs_HC_time-d7 | simple | d7/CFS (12), d7/HC (11) | yes |
| time_d2_vs_d1_grp-CFS | simple | CFS/d2 (14), CFS/d1 (14) | yes |
| time_d3_vs_d1_grp-CFS | simple | CFS/d3 (13), CFS/d1 (14) | yes |
| time_d7_vs_d1_grp-CFS | simple | CFS/d7 (12), CFS/d1 (14) | yes |
| time_d3_vs_d2_grp-CFS | simple | CFS/d3 (13), CFS/d2 (14) | yes |
| time_d7_vs_d2_grp-CFS | simple | CFS/d7 (12), CFS/d2 (14) | yes |
| time_d7_vs_d3_grp-CFS | simple | CFS/d7 (12), CFS/d3 (13) | yes |
| time_d2_vs_d1_grp-HC | simple | HC/d2 (11), HC/d1 (11) | yes |
| time_d3_vs_d1_grp-HC | simple | HC/d3 (11), HC/d1 (11) | yes |
| time_d7_vs_d1_grp-HC | simple | HC/d7 (11), HC/d1 (11) | yes |
| time_d3_vs_d2_grp-HC | simple | HC/d3 (11), HC/d2 (11) | yes |
| time_d7_vs_d2_grp-HC | simple | HC/d7 (11), HC/d2 (11) | yes |
| time_d7_vs_d3_grp-HC | simple | HC/d7 (11), HC/d3 (11) | yes |
| grp_time_CFS_d2_vs_HC_d1 | interaction | CFS/d2 (14), HC/d2 (11), CFS/d1 (14), HC/d1 (11) | yes |
| grp_time_CFS_d3_vs_HC_d1 | interaction | CFS/d3 (13), HC/d3 (11), CFS/d1 (14), HC/d1 (11) | yes |
| grp_time_CFS_d7_vs_HC_d1 | interaction | CFS/d7 (12), HC/d7 (11), CFS/d1 (14), HC/d1 (11) | yes |
