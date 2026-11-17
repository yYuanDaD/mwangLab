# Suitability: GSE302582

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (RSEM expected_count); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 2 levels; time: 3 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); grp: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 72 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_SIE_vs_MICE_time-h24 | simple | h24/SIE (12), h24/MICE (12) | yes |
| grp_SIE_vs_MICE_time-h3 | simple | h3/SIE (12), h3/MICE (12) | yes |
| grp_SIE_vs_MICE_time-pre | simple | pre/SIE (12), pre/MICE (12) | yes |
| time_h3_vs_h24_grp-MICE | simple | MICE/h3 (12), MICE/h24 (12) | yes |
| time_h24_vs_pre_grp-MICE | simple | MICE/h24 (12), MICE/pre (12) | yes |
| time_h3_vs_pre_grp-MICE | simple | MICE/h3 (12), MICE/pre (12) | yes |
| time_h3_vs_h24_grp-SIE | simple | SIE/h3 (12), SIE/h24 (12) | yes |
| time_h24_vs_pre_grp-SIE | simple | SIE/h24 (12), SIE/pre (12) | yes |
| time_h3_vs_pre_grp-SIE | simple | SIE/h3 (12), SIE/pre (12) | yes |
| grp_time_SIE_h24_vs_MICE_pre | interaction | SIE/h24 (12), MICE/h24 (12), SIE/pre (12), MICE/pre (12) | yes |
| grp_time_SIE_h3_vs_MICE_pre | interaction | SIE/h3 (12), MICE/h3 (12), SIE/pre (12), MICE/pre (12) | yes |
