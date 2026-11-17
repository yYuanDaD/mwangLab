# Suitability: GSE233485

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | TPM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | geno: 3 levels; agegrp: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 35 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_mKO_vs_WT_agegrp-O | simple | O/mKO (6), O/WT (6) | yes |
| geno_mTG_vs_WT_agegrp-O | simple | O/mTG (6), O/WT (6) | yes |
| geno_mTG_vs_mKO_agegrp-O | simple | O/mTG (6), O/mKO (6) | yes |
| geno_mKO_vs_WT_agegrp-Y | simple | Y/mKO (5), Y/WT (6) | yes |
| geno_mTG_vs_WT_agegrp-Y | simple | Y/mTG (6), Y/WT (6) | yes |
| geno_mTG_vs_mKO_agegrp-Y | simple | Y/mTG (6), Y/mKO (5) | yes |
| agegrp_O_vs_Y_geno-WT | simple | WT/O (6), WT/Y (6) | yes |
| agegrp_O_vs_Y_geno-mKO | simple | mKO/O (6), mKO/Y (5) | yes |
| agegrp_O_vs_Y_geno-mTG | simple | mTG/O (6), mTG/Y (6) | yes |
| geno_agegrp_mKO_O_vs_WT_Y | interaction | mKO/O (6), WT/O (6), mKO/Y (5), WT/Y (6) | yes |
| geno_agegrp_mTG_O_vs_WT_Y | interaction | mTG/O (6), WT/O (6), mTG/Y (6), WT/Y (6) | yes |
