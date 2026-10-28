# Suitability: GSE178262_treadmill

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (tximport lengthScaledTPM gene-level pseudo-counts from kallisto); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | trt: 3 levels; zt: 4 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | partial | 13/36 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| trt_Ex3_vs_Ex0_zt-Z00 | simple | Z00/Ex3 (0), Z00/Ex0 (3) | no |
| trt_Ex0_vs_Sed_zt-Z00 | simple | Z00/Ex0 (3), Z00/Sed (3) | yes |
| trt_Ex3_vs_Sed_zt-Z00 | simple | Z00/Ex3 (0), Z00/Sed (3) | no |
| trt_Ex3_vs_Ex0_zt-Z04 | simple | Z04/Ex3 (3), Z04/Ex0 (0) | no |
| trt_Ex0_vs_Sed_zt-Z04 | simple | Z04/Ex0 (0), Z04/Sed (3) | no |
| trt_Ex3_vs_Sed_zt-Z04 | simple | Z04/Ex3 (3), Z04/Sed (3) | yes |
| trt_Ex3_vs_Ex0_zt-Z12 | simple | Z12/Ex3 (0), Z12/Ex0 (3) | no |
| trt_Ex0_vs_Sed_zt-Z12 | simple | Z12/Ex0 (3), Z12/Sed (3) | yes |
| trt_Ex3_vs_Sed_zt-Z12 | simple | Z12/Ex3 (0), Z12/Sed (3) | no |
| trt_Ex3_vs_Ex0_zt-Z16 | simple | Z16/Ex3 (3), Z16/Ex0 (0) | no |
| trt_Ex0_vs_Sed_zt-Z16 | simple | Z16/Ex0 (0), Z16/Sed (3) | no |
| trt_Ex3_vs_Sed_zt-Z16 | simple | Z16/Ex3 (3), Z16/Sed (3) | yes |
| zt_Z04_vs_Z00_trt-Ex0 | simple | Ex0/Z04 (0), Ex0/Z00 (3) | no |
| zt_Z12_vs_Z00_trt-Ex0 | simple | Ex0/Z12 (3), Ex0/Z00 (3) | yes |
| zt_Z16_vs_Z00_trt-Ex0 | simple | Ex0/Z16 (0), Ex0/Z00 (3) | no |
| zt_Z12_vs_Z04_trt-Ex0 | simple | Ex0/Z12 (3), Ex0/Z04 (0) | no |
| zt_Z16_vs_Z04_trt-Ex0 | simple | Ex0/Z16 (0), Ex0/Z04 (0) | no |
| zt_Z16_vs_Z12_trt-Ex0 | simple | Ex0/Z16 (0), Ex0/Z12 (3) | no |
| zt_Z04_vs_Z00_trt-Ex3 | simple | Ex3/Z04 (3), Ex3/Z00 (0) | no |
| zt_Z12_vs_Z00_trt-Ex3 | simple | Ex3/Z12 (0), Ex3/Z00 (0) | no |
| zt_Z16_vs_Z00_trt-Ex3 | simple | Ex3/Z16 (3), Ex3/Z00 (0) | no |
| zt_Z12_vs_Z04_trt-Ex3 | simple | Ex3/Z12 (0), Ex3/Z04 (3) | no |
| zt_Z16_vs_Z04_trt-Ex3 | simple | Ex3/Z16 (3), Ex3/Z04 (3) | yes |
| zt_Z16_vs_Z12_trt-Ex3 | simple | Ex3/Z16 (3), Ex3/Z12 (0) | no |
| zt_Z04_vs_Z00_trt-Sed | simple | Sed/Z04 (3), Sed/Z00 (3) | yes |
| zt_Z12_vs_Z00_trt-Sed | simple | Sed/Z12 (3), Sed/Z00 (3) | yes |
| zt_Z16_vs_Z00_trt-Sed | simple | Sed/Z16 (3), Sed/Z00 (3) | yes |
| zt_Z12_vs_Z04_trt-Sed | simple | Sed/Z12 (3), Sed/Z04 (3) | yes |
| zt_Z16_vs_Z04_trt-Sed | simple | Sed/Z16 (3), Sed/Z04 (3) | yes |
| zt_Z16_vs_Z12_trt-Sed | simple | Sed/Z16 (3), Sed/Z12 (3) | yes |
| trt_zt_Ex0_Z04_vs_Sed_Z00 | interaction | Ex0/Z04 (0), Sed/Z04 (3), Ex0/Z00 (3), Sed/Z00 (3) | no |
| trt_zt_Ex0_Z12_vs_Sed_Z00 | interaction | Ex0/Z12 (3), Sed/Z12 (3), Ex0/Z00 (3), Sed/Z00 (3) | yes |
| trt_zt_Ex0_Z16_vs_Sed_Z00 | interaction | Ex0/Z16 (0), Sed/Z16 (3), Ex0/Z00 (3), Sed/Z00 (3) | no |
| trt_zt_Ex3_Z04_vs_Sed_Z00 | interaction | Ex3/Z04 (3), Sed/Z04 (3), Ex3/Z00 (0), Sed/Z00 (3) | no |
| trt_zt_Ex3_Z12_vs_Sed_Z00 | interaction | Ex3/Z12 (0), Sed/Z12 (3), Ex3/Z00 (0), Sed/Z00 (3) | no |
| trt_zt_Ex3_Z16_vs_Sed_Z00 | interaction | Ex3/Z16 (3), Sed/Z16 (3), Ex3/Z00 (0), Sed/Z00 (3) | no |
