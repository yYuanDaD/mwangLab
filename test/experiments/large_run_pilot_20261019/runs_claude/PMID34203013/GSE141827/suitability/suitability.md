# Suitability: GSE141827

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | protocol: 7 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 12/12 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Rat') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| protocol_D1_vs_CTRL_tissue-EDL | simple | EDL/D1 (3), EDL/CTRL (3) | yes |
| protocol_D3_vs_CTRL_tissue-EDL | simple | EDL/D3 (3), EDL/CTRL (3) | yes |
| protocol_D7_vs_CTRL_tissue-EDL | simple | EDL/D7 (3), EDL/CTRL (3) | yes |
| protocol_R1_vs_CTRL_tissue-EDL | simple | EDL/R1 (3), EDL/CTRL (3) | yes |
| protocol_R3_vs_CTRL_tissue-EDL | simple | EDL/R3 (3), EDL/CTRL (3) | yes |
| protocol_R7_vs_CTRL_tissue-EDL | simple | EDL/R7 (3), EDL/CTRL (3) | yes |
| protocol_D1_vs_CTRL_tissue-Sol | simple | Sol/D1 (3), Sol/CTRL (3) | yes |
| protocol_D3_vs_CTRL_tissue-Sol | simple | Sol/D3 (3), Sol/CTRL (3) | yes |
| protocol_D7_vs_CTRL_tissue-Sol | simple | Sol/D7 (3), Sol/CTRL (3) | yes |
| protocol_R1_vs_CTRL_tissue-Sol | simple | Sol/R1 (3), Sol/CTRL (3) | yes |
| protocol_R3_vs_CTRL_tissue-Sol | simple | Sol/R3 (3), Sol/CTRL (3) | yes |
| protocol_R7_vs_CTRL_tissue-Sol | simple | Sol/R7 (3), Sol/CTRL (3) | yes |
