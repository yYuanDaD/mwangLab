# Suitability: GSE280656_cartilage

Verdict: **not_analyzable** (failed: sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | fail | 0/12 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 11 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_R24_vs_Control | simple | R24 (2), Control (3) | no |
| grp_S1_vs_Control | simple | S1 (2), Control (3) | no |
| grp_S24_vs_Control | simple | S24 (2), Control (3) | no |
| grp_S4_vs_Control | simple | S4 (2), Control (3) | no |
| grp_S1_vs_R24 | simple | S1 (2), R24 (2) | no |
| grp_S24_vs_R24 | simple | S24 (2), R24 (2) | no |
| grp_S4_vs_R24 | simple | S4 (2), R24 (2) | no |
| grp_S24_vs_S1 | simple | S24 (2), S1 (2) | no |
| grp_S4_vs_S1 | simple | S4 (2), S1 (2) | no |
| grp_S4_vs_S24 | simple | S4 (2), S24 (2) | no |
| grp_R24_vs_S24 | simple | R24 (2), S24 (2) | no |
| grp_S24_vs_S4 | simple | S24 (2), S4 (2) | no |
