# Suitability: GSE312780

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | arm: 2 levels; time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); arm: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 32 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| arm_BFRT_vs_CREST_time-post | simple | post/BFRT (8), post/CREST (8) | yes |
| arm_BFRT_vs_CREST_time-pre | simple | pre/BFRT (8), pre/CREST (8) | yes |
| time_post_vs_pre_arm-BFRT | simple | BFRT/post (8), BFRT/pre (8) | yes |
| time_post_vs_pre_arm-CREST | simple | CREST/post (8), CREST/pre (8) | yes |
| arm_time_BFRT_post_vs_CREST_pre | interaction | BFRT/post (8), CREST/post (8), BFRT/pre (8), CREST/pre (8) | yes |
