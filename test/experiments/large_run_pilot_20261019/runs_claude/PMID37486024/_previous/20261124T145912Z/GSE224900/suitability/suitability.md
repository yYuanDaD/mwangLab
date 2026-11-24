# Suitability: GSE224900

Verdict: **not_analyzable** (failed: covariance); check: sex

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 3 levels |
| Covariance | fail | required; subject: block (same subject sampled at several levels: repeated measures); characteristics_ch1.4.Sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); run: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | mismatch | Sex inference completed on 57 samples.; mismatch: GSM7035293, GSM7035296, GSM7035299, GSM7035301, GSM7035305, GSM7035307; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_POST_vs_PRE_trt-Met | simple | Met/POST (10), Met/PRE (10) | yes |
| time_REC_vs_POST_trt-Met | simple | Met/REC (10), Met/POST (10) | yes |
| time_REC_vs_PRE_trt-Met | simple | Met/REC (10), Met/PRE (10) | yes |
| time_POST_vs_PRE_trt-Pla | simple | Pla/POST (9), Pla/PRE (9) | yes |
| time_REC_vs_POST_trt-Pla | simple | Pla/REC (9), Pla/POST (9) | yes |
| time_REC_vs_PRE_trt-Pla | simple | Pla/REC (9), Pla/PRE (9) | yes |
