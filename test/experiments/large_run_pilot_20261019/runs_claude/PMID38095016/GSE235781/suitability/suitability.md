# Suitability: GSE235781

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 2 levels |
| Covariance | pass | not_required; subj: omit (one sample per subject per factor level set: an identifier, not a block) |
| Sample size | pass | 4/4 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_POST_vs_PRE_cell-FLLE | simple | FLLE/POST (8), FLLE/PRE (8) | yes |
| time_POST_vs_PRE_cell-FYE | simple | FYE/POST (8), FYE/PRE (8) | yes |
| time_POST_vs_PRE_cell-SLLE | simple | SLLE/POST (8), SLLE/PRE (8) | yes |
| time_POST_vs_PRE_cell-SYE | simple | SYE/POST (8), SYE/PRE (7) | yes |
