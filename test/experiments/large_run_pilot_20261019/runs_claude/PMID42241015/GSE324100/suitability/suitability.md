# Suitability: GSE324100

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | DESeq2 median-ratio normalized counts (linear normalized, non-integer); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 7/7 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 22 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_C26_SED_vs_C26_PoWeR | simple | C26_SED (5), C26_PoWeR (5) | yes |
| grp_PBS_PoWeR_vs_C26_PoWeR | simple | PBS_PoWeR (6), C26_PoWeR (5) | yes |
| grp_C26_PoWeR_vs_PBS_SED | simple | C26_PoWeR (5), PBS_SED (6) | yes |
| grp_PBS_PoWeR_vs_C26_SED | simple | PBS_PoWeR (6), C26_SED (5) | yes |
| grp_C26_SED_vs_PBS_SED | simple | C26_SED (5), PBS_SED (6) | yes |
| grp_PBS_PoWeR_vs_PBS_SED | simple | PBS_PoWeR (6), PBS_SED (6) | yes |
| grp_C26_PoWeR_vs_C26_SED | simple | C26_PoWeR (5), C26_SED (5) | yes |
