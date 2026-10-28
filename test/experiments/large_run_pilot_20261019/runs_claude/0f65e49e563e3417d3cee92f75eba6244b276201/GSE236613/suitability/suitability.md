# Suitability: GSE236613

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 3 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference completed on 9 samples.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_RE_vs_NE | simple | RE (3), NE (3) | yes |
| grp_Sham_vs_NE | simple | Sham (3), NE (3) | yes |
| grp_Sham_vs_RE | simple | Sham (3), RE (3) | yes |
