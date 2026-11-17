# Suitability: GSE152347

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 2 levels; geno: 2 levels |
| Covariance | pass | not_required; sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | partial | 5/5 comparisons have >= 3 per group; planned names not found: time_ex60_vs_rest |
| Sex | pass | Sex inference completed on 25 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_ex60_vs_rest_geno-KO | simple | KO/ex60 (6), KO/rest (7) | yes |
| time_ex60_vs_rest_geno-WT | simple | WT/ex60 (7), WT/rest (5) | yes |
| geno_KO_vs_WT_time-ex60 | simple | ex60/KO (6), ex60/WT (7) | yes |
| geno_KO_vs_WT_time-rest | simple | rest/KO (7), rest/WT (5) | yes |
| time_geno_ex60_KO_vs_rest_WT | interaction | ex60/KO (6), rest/KO (7), ex60/WT (7), rest/WT (5) | yes |
