# Suitability: GSE120862

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | tr: 2 levels; time: 3 levels; leg: 2 levels |
| Covariance | pass | not_required; subject: omit (one sample per subject per factor level set: an identifier, not a block); subject: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); instrument_model: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); subject: omit (makes the design rank deficient); instrument_model: omit (makes the design rank deficient) |
| Sample size | pass | 35/35 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 84 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| tr_T_vs_U_time-b_leg-Ex | simple | b/Ex/T (7), b/Ex/U (7) | yes |
| tr_T_vs_U_time-b_leg-NE | simple | b/NE/T (7), b/NE/U (7) | yes |
| tr_T_vs_U_time-h1_leg-Ex | simple | h1/Ex/T (7), h1/Ex/U (7) | yes |
| tr_T_vs_U_time-h1_leg-NE | simple | h1/NE/T (7), h1/NE/U (7) | yes |
| tr_T_vs_U_time-h4_leg-Ex | simple | h4/Ex/T (7), h4/Ex/U (7) | yes |
| tr_T_vs_U_time-h4_leg-NE | simple | h4/NE/T (7), h4/NE/U (7) | yes |
| time_h1_vs_b_tr-T_leg-Ex | simple | T/Ex/h1 (7), T/Ex/b (7) | yes |
| time_h4_vs_b_tr-T_leg-Ex | simple | T/Ex/h4 (7), T/Ex/b (7) | yes |
| time_h4_vs_h1_tr-T_leg-Ex | simple | T/Ex/h4 (7), T/Ex/h1 (7) | yes |
| time_h1_vs_b_tr-T_leg-NE | simple | T/NE/h1 (7), T/NE/b (7) | yes |
| time_h4_vs_b_tr-T_leg-NE | simple | T/NE/h4 (7), T/NE/b (7) | yes |
| time_h4_vs_h1_tr-T_leg-NE | simple | T/NE/h4 (7), T/NE/h1 (7) | yes |
| time_h1_vs_b_tr-U_leg-Ex | simple | U/Ex/h1 (7), U/Ex/b (7) | yes |
| time_h4_vs_b_tr-U_leg-Ex | simple | U/Ex/h4 (7), U/Ex/b (7) | yes |
| time_h4_vs_h1_tr-U_leg-Ex | simple | U/Ex/h4 (7), U/Ex/h1 (7) | yes |
| time_h1_vs_b_tr-U_leg-NE | simple | U/NE/h1 (7), U/NE/b (7) | yes |
| time_h4_vs_b_tr-U_leg-NE | simple | U/NE/h4 (7), U/NE/b (7) | yes |
| time_h4_vs_h1_tr-U_leg-NE | simple | U/NE/h4 (7), U/NE/h1 (7) | yes |
| leg_Ex_vs_NE_tr-T_time-b | simple | T/b/Ex (7), T/b/NE (7) | yes |
| leg_Ex_vs_NE_tr-T_time-h1 | simple | T/h1/Ex (7), T/h1/NE (7) | yes |
| leg_Ex_vs_NE_tr-T_time-h4 | simple | T/h4/Ex (7), T/h4/NE (7) | yes |
| leg_Ex_vs_NE_tr-U_time-b | simple | U/b/Ex (7), U/b/NE (7) | yes |
| leg_Ex_vs_NE_tr-U_time-h1 | simple | U/h1/Ex (7), U/h1/NE (7) | yes |
| leg_Ex_vs_NE_tr-U_time-h4 | simple | U/h4/Ex (7), U/h4/NE (7) | yes |
| tr_time_T_h1_vs_U_b_leg-Ex | interaction | Ex/T/h1 (7), Ex/U/h1 (7), Ex/T/b (7), Ex/U/b (7) | yes |
| tr_time_T_h4_vs_U_b_leg-Ex | interaction | Ex/T/h4 (7), Ex/U/h4 (7), Ex/T/b (7), Ex/U/b (7) | yes |
| tr_time_T_h1_vs_U_b_leg-NE | interaction | NE/T/h1 (7), NE/U/h1 (7), NE/T/b (7), NE/U/b (7) | yes |
| tr_time_T_h4_vs_U_b_leg-NE | interaction | NE/T/h4 (7), NE/U/h4 (7), NE/T/b (7), NE/U/b (7) | yes |
| tr_leg_T_Ex_vs_U_NE_time-b | interaction | b/T/Ex (7), b/U/Ex (7), b/T/NE (7), b/U/NE (7) | yes |
| tr_leg_T_Ex_vs_U_NE_time-h1 | interaction | h1/T/Ex (7), h1/U/Ex (7), h1/T/NE (7), h1/U/NE (7) | yes |
| tr_leg_T_Ex_vs_U_NE_time-h4 | interaction | h4/T/Ex (7), h4/U/Ex (7), h4/T/NE (7), h4/U/NE (7) | yes |
| time_leg_h1_Ex_vs_b_NE_tr-T | interaction | T/h1/Ex (7), T/b/Ex (7), T/h1/NE (7), T/b/NE (7) | yes |
| time_leg_h4_Ex_vs_b_NE_tr-T | interaction | T/h4/Ex (7), T/b/Ex (7), T/h4/NE (7), T/b/NE (7) | yes |
| time_leg_h1_Ex_vs_b_NE_tr-U | interaction | U/h1/Ex (7), U/b/Ex (7), U/h1/NE (7), U/b/NE (7) | yes |
| time_leg_h4_Ex_vs_b_NE_tr-U | interaction | U/h4/Ex (7), U/b/Ex (7), U/h4/NE (7), U/b/NE (7) | yes |
