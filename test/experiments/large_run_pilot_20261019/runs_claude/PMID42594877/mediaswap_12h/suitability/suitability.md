# Suitability: mediaswap_12h

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | intensity: 2 levels; time: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information); intensity: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 22 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| intensity_SIE_vs_MIE_time-post | simple | post/SIE (5), post/MIE (6) | yes |
| intensity_SIE_vs_MIE_time-pre | simple | pre/SIE (5), pre/MIE (6) | yes |
| time_post_vs_pre_intensity-MIE | simple | MIE/post (6), MIE/pre (6) | yes |
| time_post_vs_pre_intensity-SIE | simple | SIE/post (5), SIE/pre (5) | yes |
| intensity_time_SIE_post_vs_MIE_pre | interaction | SIE/post (5), MIE/post (6), SIE/pre (5), MIE/pre (6) | yes |
