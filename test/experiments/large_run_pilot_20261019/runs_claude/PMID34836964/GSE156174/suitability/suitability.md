# Suitability: GSE156174

Verdict: **not_analyzable** (failed: sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 6 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | fail | 0/21 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_AMB_w14_vs_AMB_w8_cell-MSC | simple | MSC/AMB_w14 (1), MSC/AMB_w8 (1) | no |
| grp_HU_w14_vs_AMB_w14_cell-MSC | simple | MSC/HU_w14 (1), MSC/AMB_w14 (1) | no |
| grp_HU_w8_vs_AMB_w14_cell-MSC | simple | MSC/HU_w8 (1), MSC/AMB_w14 (1) | no |
| grp_HU_w14_vs_AMB_w8_cell-MSC | simple | MSC/HU_w14 (1), MSC/AMB_w8 (1) | no |
| grp_HU_w8_vs_AMB_w8_cell-MSC | simple | MSC/HU_w8 (1), MSC/AMB_w8 (1) | no |
| grp_HU_w8_vs_HU_w14_cell-MSC | simple | MSC/HU_w8 (1), MSC/HU_w14 (1) | no |
| grp_AMB_w14_vs_AMBR_w16_cell-SSC | simple | SSC/AMB_w14 (1), SSC/AMBR_w16 (1) | no |
| grp_AMBR_w16_vs_AMB_w8_cell-SSC | simple | SSC/AMBR_w16 (1), SSC/AMB_w8 (1) | no |
| grp_HUR_w16_vs_AMBR_w16_cell-SSC | simple | SSC/HUR_w16 (1), SSC/AMBR_w16 (1) | no |
| grp_HU_w14_vs_AMBR_w16_cell-SSC | simple | SSC/HU_w14 (1), SSC/AMBR_w16 (1) | no |
| grp_HU_w8_vs_AMBR_w16_cell-SSC | simple | SSC/HU_w8 (1), SSC/AMBR_w16 (1) | no |
| grp_AMB_w14_vs_AMB_w8_cell-SSC | simple | SSC/AMB_w14 (1), SSC/AMB_w8 (1) | no |
| grp_HUR_w16_vs_AMB_w14_cell-SSC | simple | SSC/HUR_w16 (1), SSC/AMB_w14 (1) | no |
| grp_HU_w14_vs_AMB_w14_cell-SSC | simple | SSC/HU_w14 (1), SSC/AMB_w14 (1) | no |
| grp_HU_w8_vs_AMB_w14_cell-SSC | simple | SSC/HU_w8 (1), SSC/AMB_w14 (1) | no |
| grp_HUR_w16_vs_AMB_w8_cell-SSC | simple | SSC/HUR_w16 (1), SSC/AMB_w8 (1) | no |
| grp_HU_w14_vs_AMB_w8_cell-SSC | simple | SSC/HU_w14 (1), SSC/AMB_w8 (1) | no |
| grp_HU_w8_vs_AMB_w8_cell-SSC | simple | SSC/HU_w8 (1), SSC/AMB_w8 (1) | no |
| grp_HU_w14_vs_HUR_w16_cell-SSC | simple | SSC/HU_w14 (1), SSC/HUR_w16 (1) | no |
| grp_HU_w8_vs_HUR_w16_cell-SSC | simple | SSC/HU_w8 (1), SSC/HUR_w16 (1) | no |
| grp_HU_w8_vs_HU_w14_cell-SSC | simple | SSC/HU_w8 (1), SSC/HU_w14 (1) | no |
