# Suitability: GSE174785

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | muscle: 2 levels; genotype: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| muscle_R_vs_W_genotype-KO | simple | KO/R (5), KO/W (5) | yes |
| muscle_R_vs_W_genotype-WT | simple | WT/R (5), WT/W (5) | yes |
| genotype_KO_vs_WT_muscle-R | simple | R/KO (5), R/WT (5) | yes |
| genotype_KO_vs_WT_muscle-W | simple | W/KO (5), W/WT (5) | yes |
| muscle_genotype_R_KO_vs_W_WT | interaction | R/KO (5), W/KO (5), R/WT (5), W/WT (5) | yes |
