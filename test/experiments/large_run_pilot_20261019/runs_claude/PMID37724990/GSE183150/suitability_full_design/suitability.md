# Suitability: GSE183150

Verdict: **not_analyzable** (failed: covariance)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 2 levels; visit: 2 levels |
| Covariance | fail | required; subject: block (same subject sampled at several levels: repeated measures); lane_gsms: omit (sample_identifier: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_ex_vs_uc_visit-base | simple | base/ex (9), base/uc (6) | yes |
| grp_ex_vs_uc_visit-eos | simple | eos/ex (9), eos/uc (6) | yes |
| visit_eos_vs_base_grp-ex | simple | ex/eos (9), ex/base (9) | yes |
| visit_eos_vs_base_grp-uc | simple | uc/eos (6), uc/base (6) | yes |
| grp_visit_ex_eos_vs_uc_base | interaction | ex/eos (9), uc/eos (6), ex/base (9), uc/base (6) | yes |
