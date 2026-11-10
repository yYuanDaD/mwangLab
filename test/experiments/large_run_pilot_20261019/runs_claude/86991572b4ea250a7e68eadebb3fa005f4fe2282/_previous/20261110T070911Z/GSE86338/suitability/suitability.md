# Suitability: GSE86338

Verdict: **not_analyzable** (failed: sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM (linear, Cufflinks); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | fail | 0/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 8 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_CL_vs_CNT | simple | CL (2), CNT (2) | no |
| grp_COLD_vs_CL | simple | COLD (2), CL (2) | no |
| grp_SWIM_vs_CL | simple | SWIM (2), CL (2) | no |
| grp_COLD_vs_CNT | simple | COLD (2), CNT (2) | no |
| grp_SWIM_vs_CNT | simple | SWIM (2), CNT (2) | no |
| grp_SWIM_vs_COLD | simple | SWIM (2), COLD (2) | no |
