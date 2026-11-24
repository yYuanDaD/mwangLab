# Suitability: GSE280845

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | ex: 2 levels; geno: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| ex_EXE_vs_SED_geno-KO | simple | KO/EXE (3), KO/SED (3) | yes |
| ex_EXE_vs_SED_geno-WT | simple | WT/EXE (3), WT/SED (3) | yes |
| geno_KO_vs_WT_ex-EXE | simple | EXE/KO (3), EXE/WT (3) | yes |
| geno_KO_vs_WT_ex-SED | simple | SED/KO (3), SED/WT (3) | yes |
| ex_geno_EXE_KO_vs_SED_WT | interaction | EXE/KO (3), SED/KO (3), EXE/WT (3), SED/WT (3) | yes |
