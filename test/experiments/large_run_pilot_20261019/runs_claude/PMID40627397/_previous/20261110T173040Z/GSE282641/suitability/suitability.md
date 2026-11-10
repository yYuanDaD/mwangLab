# Suitability: GSE282641

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | geno: 2 levels; zt: 2 levels; trt: 2 levels |
| Covariance | pass | not_required; sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 18/18 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 63 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_KO_vs_WT_zt-ZT15_trt-EX | simple | ZT15/EX/KO (8), ZT15/EX/WT (8) | yes |
| geno_KO_vs_WT_zt-ZT15_trt-SED | simple | ZT15/SED/KO (8), ZT15/SED/WT (8) | yes |
| geno_KO_vs_WT_zt-ZT3_trt-EX | simple | ZT3/EX/KO (7), ZT3/EX/WT (8) | yes |
| geno_KO_vs_WT_zt-ZT3_trt-SED | simple | ZT3/SED/KO (8), ZT3/SED/WT (8) | yes |
| zt_ZT15_vs_ZT3_geno-KO_trt-EX | simple | KO/EX/ZT15 (8), KO/EX/ZT3 (7) | yes |
| zt_ZT15_vs_ZT3_geno-KO_trt-SED | simple | KO/SED/ZT15 (8), KO/SED/ZT3 (8) | yes |
| zt_ZT15_vs_ZT3_geno-WT_trt-EX | simple | WT/EX/ZT15 (8), WT/EX/ZT3 (8) | yes |
| zt_ZT15_vs_ZT3_geno-WT_trt-SED | simple | WT/SED/ZT15 (8), WT/SED/ZT3 (8) | yes |
| trt_EX_vs_SED_geno-KO_zt-ZT15 | simple | KO/ZT15/EX (8), KO/ZT15/SED (8) | yes |
| trt_EX_vs_SED_geno-KO_zt-ZT3 | simple | KO/ZT3/EX (7), KO/ZT3/SED (8) | yes |
| trt_EX_vs_SED_geno-WT_zt-ZT15 | simple | WT/ZT15/EX (8), WT/ZT15/SED (8) | yes |
| trt_EX_vs_SED_geno-WT_zt-ZT3 | simple | WT/ZT3/EX (8), WT/ZT3/SED (8) | yes |
| geno_zt_KO_ZT15_vs_WT_ZT3_trt-EX | interaction | EX/KO/ZT15 (8), EX/WT/ZT15 (8), EX/KO/ZT3 (7), EX/WT/ZT3 (8) | yes |
| geno_zt_KO_ZT15_vs_WT_ZT3_trt-SED | interaction | SED/KO/ZT15 (8), SED/WT/ZT15 (8), SED/KO/ZT3 (8), SED/WT/ZT3 (8) | yes |
| geno_trt_KO_EX_vs_WT_SED_zt-ZT15 | interaction | ZT15/KO/EX (8), ZT15/WT/EX (8), ZT15/KO/SED (8), ZT15/WT/SED (8) | yes |
| geno_trt_KO_EX_vs_WT_SED_zt-ZT3 | interaction | ZT3/KO/EX (7), ZT3/WT/EX (8), ZT3/KO/SED (8), ZT3/WT/SED (8) | yes |
| zt_trt_ZT15_EX_vs_ZT3_SED_geno-KO | interaction | KO/ZT15/EX (8), KO/ZT3/EX (7), KO/ZT15/SED (8), KO/ZT3/SED (8) | yes |
| zt_trt_ZT15_EX_vs_ZT3_SED_geno-WT | interaction | WT/ZT15/EX (8), WT/ZT3/EX (8), WT/ZT15/SED (8), WT/ZT3/SED (8) | yes |
