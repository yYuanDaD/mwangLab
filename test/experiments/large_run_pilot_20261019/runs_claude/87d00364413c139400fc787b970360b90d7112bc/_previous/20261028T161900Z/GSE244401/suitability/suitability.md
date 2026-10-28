# Suitability: GSE244401

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 2 levels; time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); grp: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model); sex: omit (makes the design rank deficient) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 80 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_SCA_vs_CON_time-post | simple | post/SCA (23), post/CON (17) | yes |
| grp_SCA_vs_CON_time-pre | simple | pre/SCA (23), pre/CON (17) | yes |
| time_post_vs_pre_grp-CON | simple | CON/post (17), CON/pre (17) | yes |
| time_post_vs_pre_grp-SCA | simple | SCA/post (23), SCA/pre (23) | yes |
| grp_time_SCA_post_vs_CON_pre | interaction | SCA/post (23), CON/post (17), SCA/pre (23), CON/pre (17) | yes |
