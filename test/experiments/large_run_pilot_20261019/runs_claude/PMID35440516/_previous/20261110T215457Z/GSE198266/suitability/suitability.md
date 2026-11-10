# Suitability: GSE198266

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | log-transformed (log2(FPKM+1), quantile-normalized); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; mouse: omit (one sample per subject per factor level set: an identifier, not a block) |
| Sample size | pass | 12/12 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_OE_vs_OC_tissue-GAS | simple | GAS/OE (3), GAS/OC (3) | yes |
| grp_OC_vs_YC_tissue-GAS | simple | GAS/OC (3), GAS/YC (3) | yes |
| grp_YE_vs_OC_tissue-GAS | simple | GAS/YE (3), GAS/OC (3) | yes |
| grp_OE_vs_YC_tissue-GAS | simple | GAS/OE (3), GAS/YC (3) | yes |
| grp_YE_vs_OE_tissue-GAS | simple | GAS/YE (3), GAS/OE (3) | yes |
| grp_YE_vs_YC_tissue-GAS | simple | GAS/YE (3), GAS/YC (3) | yes |
| grp_OE_vs_OC_tissue-SOL | simple | SOL/OE (3), SOL/OC (3) | yes |
| grp_OC_vs_YC_tissue-SOL | simple | SOL/OC (3), SOL/YC (3) | yes |
| grp_YE_vs_OC_tissue-SOL | simple | SOL/YE (3), SOL/OC (3) | yes |
| grp_OE_vs_YC_tissue-SOL | simple | SOL/OE (3), SOL/YC (3) | yes |
| grp_YE_vs_OE_tissue-SOL | simple | SOL/YE (3), SOL/OE (3) | yes |
| grp_YE_vs_YC_tissue-SOL | simple | SOL/YE (3), SOL/YC (3) | yes |
