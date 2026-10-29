# Suitability: GSE325919

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 3 levels; sex: 2 levels |
| Covariance | pass | not_required; sex: omit (same grouping as design factor sex (its source column)) |
| Sample size | partial | 11/11 comparisons have >= 3 per group; planned names not found: grp_TR_vs_SED, grp_G6PD_vs_SED |
| Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_G6PD_vs_SED_sex-F | simple | F/G6PD (5), F/SED (5) | yes |
| grp_TR_vs_G6PD_sex-F | simple | F/TR (5), F/G6PD (5) | yes |
| grp_TR_vs_SED_sex-F | simple | F/TR (5), F/SED (5) | yes |
| grp_G6PD_vs_SED_sex-M | simple | M/G6PD (5), M/SED (5) | yes |
| grp_TR_vs_G6PD_sex-M | simple | M/TR (5), M/G6PD (5) | yes |
| grp_TR_vs_SED_sex-M | simple | M/TR (5), M/SED (5) | yes |
| sex_M_vs_F_grp-G6PD | simple | G6PD/M (5), G6PD/F (5) | yes |
| sex_M_vs_F_grp-SED | simple | SED/M (5), SED/F (5) | yes |
| sex_M_vs_F_grp-TR | simple | TR/M (5), TR/F (5) | yes |
| grp_sex_G6PD_M_vs_SED_F | interaction | G6PD/M (5), SED/M (5), G6PD/F (5), SED/F (5) | yes |
| grp_sex_TR_M_vs_SED_F | interaction | TR/M (5), SED/M (5), TR/F (5), SED/F (5) | yes |
