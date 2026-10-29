# Suitability: GSE129962

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | geno: 2 levels; act: 2 levels |
| Covariance | pass | not_required; batch: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); batch: omit (makes the design rank deficient) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_DH_vs_WT_age-M3_act-RA | simple | M3/RA/DH (5), M3/RA/WT (5) | yes |
| geno_DH_vs_WT_age-M6_act-EX | simple | M6/EX/DH (5), M6/EX/WT (5) | yes |
| geno_DH_vs_WT_age-M6_act-RA | simple | M6/RA/DH (5), M6/RA/WT (5) | yes |
| act_EX_vs_RA_age-M6_geno-DH | simple | M6/DH/EX (5), M6/DH/RA (5) | yes |
| act_EX_vs_RA_age-M6_geno-WT | simple | M6/WT/EX (5), M6/WT/RA (5) | yes |
| geno_act_DH_EX_vs_WT_RA_age-M6 | interaction | M6/DH/EX (5), M6/WT/EX (5), M6/DH/RA (5), M6/WT/RA (5) | yes |
