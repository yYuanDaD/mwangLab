# Suitability: GSE324257

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | TPM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | geno: 2 levels; stim: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_ko_vs_ctrl_stim-basal | simple | basal/ko (3), basal/ctrl (3) | yes |
| geno_ko_vs_ctrl_stim-eps | simple | eps/ko (3), eps/ctrl (3) | yes |
| stim_eps_vs_basal_geno-ctrl | simple | ctrl/eps (3), ctrl/basal (3) | yes |
| stim_eps_vs_basal_geno-ko | simple | ko/eps (3), ko/basal (3) | yes |
| geno_stim_ko_eps_vs_ctrl_basal | interaction | ko/eps (3), ctrl/eps (3), ko/basal (3), ctrl/basal (3) | yes |
