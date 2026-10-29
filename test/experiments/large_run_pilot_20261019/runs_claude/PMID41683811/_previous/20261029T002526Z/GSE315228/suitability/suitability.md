# Suitability: GSE315228

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 2 levels; time: 3 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); subject: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); grp: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model); subject: omit (makes the design rank deficient) |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_exp_vs_ctr_time-d0 | simple | d0/exp (4), d0/ctr (4) | yes |
| grp_exp_vs_ctr_time-d1 | simple | d1/exp (4), d1/ctr (4) | yes |
| grp_exp_vs_ctr_time-d12 | simple | d12/exp (4), d12/ctr (4) | yes |
| time_d1_vs_d0_grp-ctr | simple | ctr/d1 (4), ctr/d0 (4) | yes |
| time_d12_vs_d0_grp-ctr | simple | ctr/d12 (4), ctr/d0 (4) | yes |
| time_d12_vs_d1_grp-ctr | simple | ctr/d12 (4), ctr/d1 (4) | yes |
| time_d1_vs_d0_grp-exp | simple | exp/d1 (4), exp/d0 (4) | yes |
| time_d12_vs_d0_grp-exp | simple | exp/d12 (4), exp/d0 (4) | yes |
| time_d12_vs_d1_grp-exp | simple | exp/d12 (4), exp/d1 (4) | yes |
| grp_time_exp_d1_vs_ctr_d0 | interaction | exp/d1 (4), ctr/d1 (4), exp/d0 (4), ctr/d0 (4) | yes |
| grp_time_exp_d12_vs_ctr_d0 | interaction | exp/d12 (4), ctr/d12 (4), exp/d0 (4), ctr/d0 (4) | yes |
