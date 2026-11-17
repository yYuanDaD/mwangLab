# Suitability: GSE144133

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | linear normalized abundance (sleuth-normalized gene-level kallisto estimates, scaled reads per base); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | train: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); subject: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); subject: omit (makes the design rank deficient) |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 14 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| train_post_vs_pre | simple | post (6), pre (8) | yes |
