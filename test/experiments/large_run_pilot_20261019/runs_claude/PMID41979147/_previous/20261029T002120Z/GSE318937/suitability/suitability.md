# Suitability: GSE318937

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 3 levels; trt: 2 levels |
| Covariance | pass | not_required; subject: omit (one sample per subject per factor level set: an identifier, not a block); period: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); sequence: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 22/22 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 119 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_Post_vs_H24_ex-MICE_trt-OLE | simple | MICE/OLE/Post (10), MICE/OLE/H24 (10) | yes |
| time_H24_vs_Pre_ex-MICE_trt-OLE | simple | MICE/OLE/H24 (10), MICE/OLE/Pre (10) | yes |
| time_Post_vs_Pre_ex-MICE_trt-OLE | simple | MICE/OLE/Post (10), MICE/OLE/Pre (10) | yes |
| time_Post_vs_H24_ex-MICE_trt-PLA | simple | MICE/PLA/Post (10), MICE/PLA/H24 (10) | yes |
| time_H24_vs_Pre_ex-MICE_trt-PLA | simple | MICE/PLA/H24 (10), MICE/PLA/Pre (9) | yes |
| time_Post_vs_Pre_ex-MICE_trt-PLA | simple | MICE/PLA/Post (10), MICE/PLA/Pre (9) | yes |
| trt_OLE_vs_PLA_ex-MICE_time-H24 | simple | MICE/H24/OLE (10), MICE/H24/PLA (10) | yes |
| trt_OLE_vs_PLA_ex-MICE_time-Post | simple | MICE/Post/OLE (10), MICE/Post/PLA (10) | yes |
| trt_OLE_vs_PLA_ex-MICE_time-Pre | simple | MICE/Pre/OLE (10), MICE/Pre/PLA (9) | yes |
| time_trt_H24_OLE_vs_Pre_PLA_ex-MICE | interaction | MICE/H24/OLE (10), MICE/Pre/OLE (10), MICE/H24/PLA (10), MICE/Pre/PLA (9) | yes |
| time_trt_Post_OLE_vs_Pre_PLA_ex-MICE | interaction | MICE/Post/OLE (10), MICE/Pre/OLE (10), MICE/Post/PLA (10), MICE/Pre/PLA (9) | yes |
| time_Post_vs_H24_ex-SIE_trt-OLE | simple | SIE/OLE/Post (10), SIE/OLE/H24 (10) | yes |
| time_H24_vs_Pre_ex-SIE_trt-OLE | simple | SIE/OLE/H24 (10), SIE/OLE/Pre (10) | yes |
| time_Post_vs_Pre_ex-SIE_trt-OLE | simple | SIE/OLE/Post (10), SIE/OLE/Pre (10) | yes |
| time_Post_vs_H24_ex-SIE_trt-PLA | simple | SIE/PLA/Post (10), SIE/PLA/H24 (10) | yes |
| time_H24_vs_Pre_ex-SIE_trt-PLA | simple | SIE/PLA/H24 (10), SIE/PLA/Pre (10) | yes |
| time_Post_vs_Pre_ex-SIE_trt-PLA | simple | SIE/PLA/Post (10), SIE/PLA/Pre (10) | yes |
| trt_OLE_vs_PLA_ex-SIE_time-H24 | simple | SIE/H24/OLE (10), SIE/H24/PLA (10) | yes |
| trt_OLE_vs_PLA_ex-SIE_time-Post | simple | SIE/Post/OLE (10), SIE/Post/PLA (10) | yes |
| trt_OLE_vs_PLA_ex-SIE_time-Pre | simple | SIE/Pre/OLE (10), SIE/Pre/PLA (10) | yes |
| time_trt_H24_OLE_vs_Pre_PLA_ex-SIE | interaction | SIE/H24/OLE (10), SIE/Pre/OLE (10), SIE/H24/PLA (10), SIE/Pre/PLA (10) | yes |
| time_trt_Post_OLE_vs_Pre_PLA_ex-SIE | interaction | SIE/Post/OLE (10), SIE/Pre/OLE (10), SIE/Post/PLA (10), SIE/Pre/PLA (10) | yes |
