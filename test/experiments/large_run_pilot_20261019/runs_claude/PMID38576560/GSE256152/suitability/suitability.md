# Suitability: GSE256152

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference completed on 12 samples.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_cur_vs_Tnm | simple | cur (3), Tnm (3) | yes |
| grp_swim_vs_Tnm | simple | swim (3), Tnm (3) | yes |
| grp_union_vs_Tnm | simple | union (3), Tnm (3) | yes |
| grp_swim_vs_cur | simple | swim (3), cur (3) | yes |
| grp_union_vs_cur | simple | union (3), cur (3) | yes |
| grp_union_vs_swim | simple | union (3), swim (3) | yes |
