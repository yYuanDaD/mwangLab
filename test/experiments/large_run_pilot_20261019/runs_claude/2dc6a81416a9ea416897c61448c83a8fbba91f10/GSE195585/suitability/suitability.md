# Suitability: GSE195585

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | time: 4 levels; grp: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); grp: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
| Sample size | pass | 19/19 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 119 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_t1_vs_t0_grp-CP | simple | CP/t1 (15), CP/t0 (15) | yes |
| time_t4_vs_t0_grp-CP | simple | CP/t4 (15), CP/t0 (15) | yes |
| time_t24_vs_t0_grp-CP | simple | CP/t24 (14), CP/t0 (15) | yes |
| time_t4_vs_t1_grp-CP | simple | CP/t4 (15), CP/t1 (15) | yes |
| time_t24_vs_t1_grp-CP | simple | CP/t24 (14), CP/t1 (15) | yes |
| time_t24_vs_t4_grp-CP | simple | CP/t24 (14), CP/t4 (15) | yes |
| time_t1_vs_t0_grp-PLA | simple | PLA/t1 (15), PLA/t0 (15) | yes |
| time_t4_vs_t0_grp-PLA | simple | PLA/t4 (15), PLA/t0 (15) | yes |
| time_t24_vs_t0_grp-PLA | simple | PLA/t24 (15), PLA/t0 (15) | yes |
| time_t4_vs_t1_grp-PLA | simple | PLA/t4 (15), PLA/t1 (15) | yes |
| time_t24_vs_t1_grp-PLA | simple | PLA/t24 (15), PLA/t1 (15) | yes |
| time_t24_vs_t4_grp-PLA | simple | PLA/t24 (15), PLA/t4 (15) | yes |
| grp_CP_vs_PLA_time-t0 | simple | t0/CP (15), t0/PLA (15) | yes |
| grp_CP_vs_PLA_time-t1 | simple | t1/CP (15), t1/PLA (15) | yes |
| grp_CP_vs_PLA_time-t24 | simple | t24/CP (14), t24/PLA (15) | yes |
| grp_CP_vs_PLA_time-t4 | simple | t4/CP (15), t4/PLA (15) | yes |
| time_grp_t1_CP_vs_t0_PLA | interaction | t1/CP (15), t0/CP (15), t1/PLA (15), t0/PLA (15) | yes |
| time_grp_t24_CP_vs_t0_PLA | interaction | t24/CP (14), t0/CP (15), t24/PLA (15), t0/PLA (15) | yes |
| time_grp_t4_CP_vs_t0_PLA | interaction | t4/CP (15), t0/CP (15), t4/PLA (15), t0/PLA (15) | yes |
