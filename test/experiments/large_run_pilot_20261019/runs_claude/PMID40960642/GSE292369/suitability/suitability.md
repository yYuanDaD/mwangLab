# Suitability: GSE292369

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | cond: 2 levels; time: 2 levels |
| Covariance | pass | not_required; subject: omit (one sample per subject per factor level set: an identifier, not a block) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 34 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| cond_KME_vs_PLA_time-POST | simple | POST/KME (9), POST/PLA (9) | yes |
| cond_KME_vs_PLA_time-PRE | simple | PRE/KME (8), PRE/PLA (8) | yes |
| time_POST_vs_PRE_cond-KME | simple | KME/POST (9), KME/PRE (8) | yes |
| time_POST_vs_PRE_cond-PLA | simple | PLA/POST (9), PLA/PRE (8) | yes |
| cond_time_KME_POST_vs_PLA_PRE | interaction | KME/POST (9), PLA/POST (9), KME/PRE (8), PLA/PRE (8) | yes |
