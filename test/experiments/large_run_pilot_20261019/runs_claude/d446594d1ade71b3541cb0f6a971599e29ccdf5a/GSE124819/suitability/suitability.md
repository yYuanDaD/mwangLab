# Suitability: GSE124819

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | arm: 7 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 13/13 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference completed on 37 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| arm_CL_vs_CT_set-Ac | simple | Ac/CL (5), Ac/CT (5) | yes |
| arm_NSstd_vs_CL_set-Ac | simple | Ac/NSstd (5), Ac/CL (5) | yes |
| arm_NSstd_vs_CT_set-Ac | simple | Ac/NSstd (5), Ac/CT (5) | yes |
| arm_NStiny_vs_CT_set-Ex | simple | Ex/NStiny (4), Ex/CT (4) | yes |
| arm_SWIM_vs_CT_set-Ex | simple | Ex/SWIM (5), Ex/CT (4) | yes |
| arm_SWW_vs_CT_set-Ex | simple | Ex/SWW (5), Ex/CT (4) | yes |
| arm_TX_vs_CT_set-Ex | simple | Ex/TX (4), Ex/CT (4) | yes |
| arm_SWIM_vs_NStiny_set-Ex | simple | Ex/SWIM (5), Ex/NStiny (4) | yes |
| arm_SWW_vs_NStiny_set-Ex | simple | Ex/SWW (5), Ex/NStiny (4) | yes |
| arm_TX_vs_NStiny_set-Ex | simple | Ex/TX (4), Ex/NStiny (4) | yes |
| arm_SWW_vs_SWIM_set-Ex | simple | Ex/SWW (5), Ex/SWIM (5) | yes |
| arm_TX_vs_SWIM_set-Ex | simple | Ex/TX (4), Ex/SWIM (5) | yes |
| arm_TX_vs_SWW_set-Ex | simple | Ex/TX (4), Ex/SWW (5) | yes |
