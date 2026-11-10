# Suitability: GSE207992

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 7/7 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 14 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_KO_nSVE_vs_KO_SVE | simple | KO_nSVE (3), KO_SVE (3) | yes |
| grp_WT_SVE_vs_KO_SVE | simple | WT_SVE (4), KO_SVE (3) | yes |
| grp_KO_SVE_vs_WT_nSVE | simple | KO_SVE (3), WT_nSVE (4) | yes |
| grp_WT_SVE_vs_KO_nSVE | simple | WT_SVE (4), KO_nSVE (3) | yes |
| grp_KO_nSVE_vs_WT_nSVE | simple | KO_nSVE (3), WT_nSVE (4) | yes |
| grp_WT_SVE_vs_WT_nSVE | simple | WT_SVE (4), WT_nSVE (4) | yes |
| grp_KO_SVE_vs_KO_nSVE | simple | KO_SVE (3), KO_nSVE (3) | yes |
