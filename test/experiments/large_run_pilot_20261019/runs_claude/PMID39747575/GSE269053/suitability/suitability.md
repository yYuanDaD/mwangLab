# Suitability: GSE269053

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | diet: 2 levels; virus: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| diet_HFD_vs_chow_virus-Renin | simple | Renin/HFD (5), Renin/chow (6) | yes |
| diet_HFD_vs_chow_virus-novirus | simple | novirus/HFD (6), novirus/chow (4) | yes |
| virus_Renin_vs_novirus_diet-HFD | simple | HFD/Renin (5), HFD/novirus (6) | yes |
| virus_Renin_vs_novirus_diet-chow | simple | chow/Renin (6), chow/novirus (4) | yes |
| diet_virus_HFD_Renin_vs_chow_novirus | interaction | HFD/Renin (5), chow/Renin (6), HFD/novirus (6), chow/novirus (4) | yes |
