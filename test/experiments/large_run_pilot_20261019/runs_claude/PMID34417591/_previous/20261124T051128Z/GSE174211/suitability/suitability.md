# Suitability: GSE174211

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 7/7 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 17 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_KO_Sed_vs_KO_Run | simple | KO_Sed (5), KO_Run (4) | yes |
| grp_WT_Run_vs_KO_Run | simple | WT_Run (4), KO_Run (4) | yes |
| grp_KO_Run_vs_WT_Sed | simple | KO_Run (4), WT_Sed (4) | yes |
| grp_WT_Run_vs_KO_Sed | simple | WT_Run (4), KO_Sed (5) | yes |
| grp_KO_Sed_vs_WT_Sed | simple | KO_Sed (5), WT_Sed (4) | yes |
| grp_WT_Run_vs_WT_Sed | simple | WT_Run (4), WT_Sed (4) | yes |
| grp_KO_Run_vs_KO_Sed | simple | KO_Run (4), KO_Sed (5) | yes |
