# Suitability: GSE222163

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 12/12 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 29 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_CREX_vs_CR_tissue-BAT | simple | BAT/CREX (4), BAT/CR (4) | yes |
| grp_CR_vs_Ctrl_tissue-BAT | simple | BAT/CR (4), BAT/Ctrl (3) | yes |
| grp_EX_vs_CR_tissue-BAT | simple | BAT/EX (4), BAT/CR (4) | yes |
| grp_CREX_vs_Ctrl_tissue-BAT | simple | BAT/CREX (4), BAT/Ctrl (3) | yes |
| grp_EX_vs_CREX_tissue-BAT | simple | BAT/EX (4), BAT/CREX (4) | yes |
| grp_EX_vs_Ctrl_tissue-BAT | simple | BAT/EX (4), BAT/Ctrl (3) | yes |
| grp_CREX_vs_CR_tissue-SkM | simple | SkM/CREX (3), SkM/CR (3) | yes |
| grp_CR_vs_Ctrl_tissue-SkM | simple | SkM/CR (3), SkM/Ctrl (4) | yes |
| grp_EX_vs_CR_tissue-SkM | simple | SkM/EX (4), SkM/CR (3) | yes |
| grp_CREX_vs_Ctrl_tissue-SkM | simple | SkM/CREX (3), SkM/Ctrl (4) | yes |
| grp_EX_vs_CREX_tissue-SkM | simple | SkM/EX (4), SkM/CREX (3) | yes |
| grp_EX_vs_Ctrl_tissue-SkM | simple | SkM/EX (4), SkM/Ctrl (4) | yes |
