# Suitability: GSE280656_synovium

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 12/12 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_R24_vs_Control | simple | R24 (3), Control (3) | yes |
| grp_S1_vs_Control | simple | S1 (3), Control (3) | yes |
| grp_S24_vs_Control | simple | S24 (3), Control (3) | yes |
| grp_S4_vs_Control | simple | S4 (3), Control (3) | yes |
| grp_S1_vs_R24 | simple | S1 (3), R24 (3) | yes |
| grp_S24_vs_R24 | simple | S24 (3), R24 (3) | yes |
| grp_S4_vs_R24 | simple | S4 (3), R24 (3) | yes |
| grp_S24_vs_S1 | simple | S24 (3), S1 (3) | yes |
| grp_S4_vs_S1 | simple | S4 (3), S1 (3) | yes |
| grp_S4_vs_S24 | simple | S4 (3), S24 (3) | yes |
| grp_R24_vs_S24 | simple | R24 (3), S24 (3) | yes |
| grp_S24_vs_S4 | simple | S24 (3), S4 (3) | yes |
