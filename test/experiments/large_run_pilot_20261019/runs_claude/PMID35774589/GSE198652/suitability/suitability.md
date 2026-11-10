# Suitability: GSE198652

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 4/4 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 34 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_PoW_vs_Sed_stratum-PlaOld | simple | PlaOld/PoW (4), PlaOld/Sed (5) | yes |
| grp_PoW_vs_Sed_stratum-PlaYoung | simple | PlaYoung/PoW (4), PlaYoung/Sed (4) | yes |
| grp_PoW_vs_Sed_stratum-SolOld | simple | SolOld/PoW (4), SolOld/Sed (5) | yes |
| grp_PoW_vs_Sed_stratum-SolYoung | simple | SolYoung/PoW (4), SolYoung/Sed (4) | yes |
