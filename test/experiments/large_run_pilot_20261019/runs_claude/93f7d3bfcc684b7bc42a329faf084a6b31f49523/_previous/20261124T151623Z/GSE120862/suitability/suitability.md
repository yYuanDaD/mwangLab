# Suitability: GSE120862

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 12 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); subject: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); instrument_model: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); subject: omit (makes the design rank deficient); instrument_model: omit (makes the design rank deficient) |
| Sample size | partial | 11/11 comparisons have >= 3 per group; planned names not found: grp_Uh1Ex_vs_Uh1NE, grp_Uh4Ex_vs_Uh4NE, grp_Th1Ex_vs_Th1NE, grp_Th4Ex_vs_Th4NE, grp_TbEx_vs_UbEx |
| Sex | pass | Sex inference completed on 84 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_TbEx_vs_UbNE | simple | TbEx (7), UbNE (7) | yes |
| grp_TbNE_vs_UbNE | simple | TbNE (7), UbNE (7) | yes |
| grp_Th1Ex_vs_UbNE | simple | Th1Ex (7), UbNE (7) | yes |
| grp_Th1NE_vs_UbNE | simple | Th1NE (7), UbNE (7) | yes |
| grp_Th4Ex_vs_UbNE | simple | Th4Ex (7), UbNE (7) | yes |
| grp_Th4NE_vs_UbNE | simple | Th4NE (7), UbNE (7) | yes |
| grp_UbEx_vs_UbNE | simple | UbEx (7), UbNE (7) | yes |
| grp_Uh1Ex_vs_UbNE | simple | Uh1Ex (7), UbNE (7) | yes |
| grp_Uh1NE_vs_UbNE | simple | Uh1NE (7), UbNE (7) | yes |
| grp_Uh4Ex_vs_UbNE | simple | Uh4Ex (7), UbNE (7) | yes |
| grp_Uh4NE_vs_UbNE | simple | Uh4NE (7), UbNE (7) | yes |
