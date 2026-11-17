# Suitability: GSE180877

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (Partek Flow gene-level quantification; non-integer values); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 11/11 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_LD6_vs_DT9 | simple | LD6 (3), DT9 (3) | yes |
| grp_PoW6_vs_DT9 | simple | PoW6 (3), DT9 (3) | yes |
| grp_DT9_vs_UT6 | simple | DT9 (3), UT6 (3) | yes |
| grp_UT9_vs_DT9 | simple | UT9 (3), DT9 (3) | yes |
| grp_PoW6_vs_LD6 | simple | PoW6 (3), LD6 (3) | yes |
| grp_LD6_vs_UT6 | simple | LD6 (3), UT6 (3) | yes |
| grp_UT9_vs_LD6 | simple | UT9 (3), LD6 (3) | yes |
| grp_PoW6_vs_UT6 | simple | PoW6 (3), UT6 (3) | yes |
| grp_UT9_vs_PoW6 | simple | UT9 (3), PoW6 (3) | yes |
| grp_UT9_vs_UT6 | simple | UT9 (3), UT6 (3) | yes |
| grp_DT9_vs_UT9 | simple | DT9 (3), UT9 (3) | yes |
