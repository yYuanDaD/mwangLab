# Suitability: GSE315915_transcript

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_EHP_vs_SED | simple | EHP (5), SED (5) | yes |
