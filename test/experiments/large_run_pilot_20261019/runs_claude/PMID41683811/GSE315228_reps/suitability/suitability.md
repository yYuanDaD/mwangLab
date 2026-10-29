# Suitability: GSE315228_reps

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 2 levels; time: 3 levels |
| Covariance | pass | not_required; subject: omit (one sample per subject per factor level set: an identifier, not a block); subject: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); subject: omit (makes the design rank deficient) |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 69 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_exp_vs_ctr_time-d0 | simple | d0/exp (12), d0/ctr (11) | yes |
| grp_exp_vs_ctr_time-d1 | simple | d1/exp (11), d1/ctr (12) | yes |
| grp_exp_vs_ctr_time-d12 | simple | d12/exp (12), d12/ctr (11) | yes |
| time_d1_vs_d0_grp-ctr | simple | ctr/d1 (12), ctr/d0 (11) | yes |
| time_d12_vs_d0_grp-ctr | simple | ctr/d12 (11), ctr/d0 (11) | yes |
| time_d12_vs_d1_grp-ctr | simple | ctr/d12 (11), ctr/d1 (12) | yes |
| time_d1_vs_d0_grp-exp | simple | exp/d1 (11), exp/d0 (12) | yes |
| time_d12_vs_d0_grp-exp | simple | exp/d12 (12), exp/d0 (12) | yes |
| time_d12_vs_d1_grp-exp | simple | exp/d12 (12), exp/d1 (11) | yes |
| grp_time_exp_d1_vs_ctr_d0 | interaction | exp/d1 (11), ctr/d1 (12), exp/d0 (12), ctr/d0 (11) | yes |
| grp_time_exp_d12_vs_ctr_d0 | interaction | exp/d12 (12), ctr/d12 (11), exp/d0 (12), ctr/d0 (11) | yes |
