# Suitability: GSE217155

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 3 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 4/4 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_EXE_vs_CON | simple | EXE (3), CON (3) | yes |
| grp_NASH_vs_CON | simple | NASH (3), CON (3) | yes |
| grp_NASH_vs_EXE | simple | NASH (3), EXE (3) | yes |
| grp_EXE_vs_NASH | simple | EXE (3), NASH (3) | yes |
