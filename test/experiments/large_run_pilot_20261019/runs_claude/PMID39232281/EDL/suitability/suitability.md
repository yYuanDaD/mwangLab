# Suitability: EDL

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | sex: 2 levels; trt: 2 levels; zt: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 18/18 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| sex_M_vs_F_trt-ctrl_zt-zt05 | simple | ctrl/zt05/M (3), ctrl/zt05/F (3) | yes |
| sex_M_vs_F_trt-ctrl_zt-zt17 | simple | ctrl/zt17/M (3), ctrl/zt17/F (3) | yes |
| sex_M_vs_F_trt-def_zt-zt05 | simple | def/zt05/M (3), def/zt05/F (3) | yes |
| sex_M_vs_F_trt-def_zt-zt17 | simple | def/zt17/M (3), def/zt17/F (3) | yes |
| trt_def_vs_ctrl_sex-F_zt-zt05 | simple | F/zt05/def (3), F/zt05/ctrl (3) | yes |
| trt_def_vs_ctrl_sex-F_zt-zt17 | simple | F/zt17/def (3), F/zt17/ctrl (3) | yes |
| trt_def_vs_ctrl_sex-M_zt-zt05 | simple | M/zt05/def (3), M/zt05/ctrl (3) | yes |
| trt_def_vs_ctrl_sex-M_zt-zt17 | simple | M/zt17/def (3), M/zt17/ctrl (3) | yes |
| zt_zt17_vs_zt05_sex-F_trt-ctrl | simple | F/ctrl/zt17 (3), F/ctrl/zt05 (3) | yes |
| zt_zt17_vs_zt05_sex-F_trt-def | simple | F/def/zt17 (3), F/def/zt05 (3) | yes |
| zt_zt17_vs_zt05_sex-M_trt-ctrl | simple | M/ctrl/zt17 (3), M/ctrl/zt05 (3) | yes |
| zt_zt17_vs_zt05_sex-M_trt-def | simple | M/def/zt17 (3), M/def/zt05 (3) | yes |
| sex_trt_M_def_vs_F_ctrl_zt-zt05 | interaction | zt05/M/def (3), zt05/F/def (3), zt05/M/ctrl (3), zt05/F/ctrl (3) | yes |
| sex_trt_M_def_vs_F_ctrl_zt-zt17 | interaction | zt17/M/def (3), zt17/F/def (3), zt17/M/ctrl (3), zt17/F/ctrl (3) | yes |
| sex_zt_M_zt17_vs_F_zt05_trt-ctrl | interaction | ctrl/M/zt17 (3), ctrl/F/zt17 (3), ctrl/M/zt05 (3), ctrl/F/zt05 (3) | yes |
| sex_zt_M_zt17_vs_F_zt05_trt-def | interaction | def/M/zt17 (3), def/F/zt17 (3), def/M/zt05 (3), def/F/zt05 (3) | yes |
| trt_zt_def_zt17_vs_ctrl_zt05_sex-F | interaction | F/def/zt17 (3), F/ctrl/zt17 (3), F/def/zt05 (3), F/ctrl/zt05 (3) | yes |
| trt_zt_def_zt17_vs_ctrl_zt05_sex-M | interaction | M/def/zt17 (3), M/ctrl/zt17 (3), M/def/zt05 (3), M/ctrl/zt05 (3) | yes |
