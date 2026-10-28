# Suitability: GSE324036

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 7/7 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_SCAsed_vs_SCAex | simple | SCAsed (3), SCAex (3) | yes |
| grp_WTex_vs_SCAex | simple | WTex (3), SCAex (3) | yes |
| grp_SCAex_vs_WTsed | simple | SCAex (3), WTsed (3) | yes |
| grp_WTex_vs_SCAsed | simple | WTex (3), SCAsed (3) | yes |
| grp_SCAsed_vs_WTsed | simple | SCAsed (3), WTsed (3) | yes |
| grp_WTex_vs_WTsed | simple | WTex (3), WTsed (3) | yes |
| grp_SCAex_vs_SCAsed | simple | SCAex (3), SCAsed (3) | yes |
