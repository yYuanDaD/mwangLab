# Suitability: GSE144109

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 12/12 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_MHS_vs_MHE | simple | MHS (3), MHE (3) | yes |
| grp_MHE_vs_NCS | simple | MHE (3), NCS (3) | yes |
| grp_PHE_vs_MHE | simple | PHE (3), MHE (3) | yes |
| grp_PHS_vs_MHE | simple | PHS (3), MHE (3) | yes |
| grp_MHS_vs_NCS | simple | MHS (3), NCS (3) | yes |
| grp_PHE_vs_MHS | simple | PHE (3), MHS (3) | yes |
| grp_PHS_vs_MHS | simple | PHS (3), MHS (3) | yes |
| grp_PHE_vs_NCS | simple | PHE (3), NCS (3) | yes |
| grp_PHS_vs_NCS | simple | PHS (3), NCS (3) | yes |
| grp_PHS_vs_PHE | simple | PHS (3), PHE (3) | yes |
| grp_MHE_vs_MHS | simple | MHE (3), MHS (3) | yes |
| grp_PHE_vs_PHS | simple | PHE (3), PHS (3) | yes |
