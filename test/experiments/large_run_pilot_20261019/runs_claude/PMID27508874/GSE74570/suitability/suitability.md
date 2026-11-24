# Suitability: GSE74570

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 6 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 15/15 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 23 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_OE_m24_vs_KO_m7 | simple | OE_m24 (4), KO_m7 (4) | yes |
| grp_OE_m4_vs_KO_m7 | simple | OE_m4 (3), KO_m7 (4) | yes |
| grp_WT_m24_vs_KO_m7 | simple | WT_m24 (4), KO_m7 (4) | yes |
| grp_WT_m4_vs_KO_m7 | simple | WT_m4 (4), KO_m7 (4) | yes |
| grp_KO_m7_vs_WT_m7 | simple | KO_m7 (4), WT_m7 (4) | yes |
| grp_OE_m4_vs_OE_m24 | simple | OE_m4 (3), OE_m24 (4) | yes |
| grp_WT_m24_vs_OE_m24 | simple | WT_m24 (4), OE_m24 (4) | yes |
| grp_WT_m4_vs_OE_m24 | simple | WT_m4 (4), OE_m24 (4) | yes |
| grp_OE_m24_vs_WT_m7 | simple | OE_m24 (4), WT_m7 (4) | yes |
| grp_WT_m24_vs_OE_m4 | simple | WT_m24 (4), OE_m4 (3) | yes |
| grp_WT_m4_vs_OE_m4 | simple | WT_m4 (4), OE_m4 (3) | yes |
| grp_OE_m4_vs_WT_m7 | simple | OE_m4 (3), WT_m7 (4) | yes |
| grp_WT_m4_vs_WT_m24 | simple | WT_m4 (4), WT_m24 (4) | yes |
| grp_WT_m24_vs_WT_m7 | simple | WT_m24 (4), WT_m7 (4) | yes |
| grp_WT_m4_vs_WT_m7 | simple | WT_m4 (4), WT_m7 (4) | yes |
