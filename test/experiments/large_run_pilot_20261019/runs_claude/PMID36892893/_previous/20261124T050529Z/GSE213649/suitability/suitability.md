# Suitability: GSE213649

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 6 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 90/90 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 179 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_CONEx_vs_CONSed_tissue-COL | simple | COL/CONEx (6), COL/CONSed (6) | yes |
| grp_LPAEx_vs_CONEx_tissue-COL | simple | COL/LPAEx (6), COL/CONEx (6) | yes |
| grp_LPASed_vs_CONEx_tissue-COL | simple | COL/LPASed (6), COL/CONEx (6) | yes |
| grp_LPEx_vs_CONEx_tissue-COL | simple | COL/LPEx (6), COL/CONEx (6) | yes |
| grp_LPSed_vs_CONEx_tissue-COL | simple | COL/LPSed (6), COL/CONEx (6) | yes |
| grp_LPAEx_vs_CONSed_tissue-COL | simple | COL/LPAEx (6), COL/CONSed (6) | yes |
| grp_LPASed_vs_CONSed_tissue-COL | simple | COL/LPASed (6), COL/CONSed (6) | yes |
| grp_LPEx_vs_CONSed_tissue-COL | simple | COL/LPEx (6), COL/CONSed (6) | yes |
| grp_LPSed_vs_CONSed_tissue-COL | simple | COL/LPSed (6), COL/CONSed (6) | yes |
| grp_LPASed_vs_LPAEx_tissue-COL | simple | COL/LPASed (6), COL/LPAEx (6) | yes |
| grp_LPEx_vs_LPAEx_tissue-COL | simple | COL/LPEx (6), COL/LPAEx (6) | yes |
| grp_LPSed_vs_LPAEx_tissue-COL | simple | COL/LPSed (6), COL/LPAEx (6) | yes |
| grp_LPEx_vs_LPASed_tissue-COL | simple | COL/LPEx (6), COL/LPASed (6) | yes |
| grp_LPSed_vs_LPASed_tissue-COL | simple | COL/LPSed (6), COL/LPASed (6) | yes |
| grp_LPSed_vs_LPEx_tissue-COL | simple | COL/LPSed (6), COL/LPEx (6) | yes |
| grp_CONEx_vs_CONSed_tissue-HIP | simple | HIP/CONEx (6), HIP/CONSed (6) | yes |
| grp_LPAEx_vs_CONEx_tissue-HIP | simple | HIP/LPAEx (6), HIP/CONEx (6) | yes |
| grp_LPASed_vs_CONEx_tissue-HIP | simple | HIP/LPASed (6), HIP/CONEx (6) | yes |
| grp_LPEx_vs_CONEx_tissue-HIP | simple | HIP/LPEx (6), HIP/CONEx (6) | yes |
| grp_LPSed_vs_CONEx_tissue-HIP | simple | HIP/LPSed (6), HIP/CONEx (6) | yes |
| grp_LPAEx_vs_CONSed_tissue-HIP | simple | HIP/LPAEx (6), HIP/CONSed (6) | yes |
| grp_LPASed_vs_CONSed_tissue-HIP | simple | HIP/LPASed (6), HIP/CONSed (6) | yes |
| grp_LPEx_vs_CONSed_tissue-HIP | simple | HIP/LPEx (6), HIP/CONSed (6) | yes |
| grp_LPSed_vs_CONSed_tissue-HIP | simple | HIP/LPSed (6), HIP/CONSed (6) | yes |
| grp_LPASed_vs_LPAEx_tissue-HIP | simple | HIP/LPASed (6), HIP/LPAEx (6) | yes |
| grp_LPEx_vs_LPAEx_tissue-HIP | simple | HIP/LPEx (6), HIP/LPAEx (6) | yes |
| grp_LPSed_vs_LPAEx_tissue-HIP | simple | HIP/LPSed (6), HIP/LPAEx (6) | yes |
| grp_LPEx_vs_LPASed_tissue-HIP | simple | HIP/LPEx (6), HIP/LPASed (6) | yes |
| grp_LPSed_vs_LPASed_tissue-HIP | simple | HIP/LPSed (6), HIP/LPASed (6) | yes |
| grp_LPSed_vs_LPEx_tissue-HIP | simple | HIP/LPSed (6), HIP/LPEx (6) | yes |
| grp_CONEx_vs_CONSed_tissue-LIV | simple | LIV/CONEx (6), LIV/CONSed (6) | yes |
| grp_LPAEx_vs_CONEx_tissue-LIV | simple | LIV/LPAEx (6), LIV/CONEx (6) | yes |
| grp_LPASed_vs_CONEx_tissue-LIV | simple | LIV/LPASed (6), LIV/CONEx (6) | yes |
| grp_LPEx_vs_CONEx_tissue-LIV | simple | LIV/LPEx (5), LIV/CONEx (6) | yes |
| grp_LPSed_vs_CONEx_tissue-LIV | simple | LIV/LPSed (6), LIV/CONEx (6) | yes |
| grp_LPAEx_vs_CONSed_tissue-LIV | simple | LIV/LPAEx (6), LIV/CONSed (6) | yes |
| grp_LPASed_vs_CONSed_tissue-LIV | simple | LIV/LPASed (6), LIV/CONSed (6) | yes |
| grp_LPEx_vs_CONSed_tissue-LIV | simple | LIV/LPEx (5), LIV/CONSed (6) | yes |
| grp_LPSed_vs_CONSed_tissue-LIV | simple | LIV/LPSed (6), LIV/CONSed (6) | yes |
| grp_LPASed_vs_LPAEx_tissue-LIV | simple | LIV/LPASed (6), LIV/LPAEx (6) | yes |
| grp_LPEx_vs_LPAEx_tissue-LIV | simple | LIV/LPEx (5), LIV/LPAEx (6) | yes |
| grp_LPSed_vs_LPAEx_tissue-LIV | simple | LIV/LPSed (6), LIV/LPAEx (6) | yes |
| grp_LPEx_vs_LPASed_tissue-LIV | simple | LIV/LPEx (5), LIV/LPASed (6) | yes |
| grp_LPSed_vs_LPASed_tissue-LIV | simple | LIV/LPSed (6), LIV/LPASed (6) | yes |
| grp_LPSed_vs_LPEx_tissue-LIV | simple | LIV/LPSed (6), LIV/LPEx (5) | yes |
| grp_CONEx_vs_CONSed_tissue-MUS | simple | MUS/CONEx (6), MUS/CONSed (6) | yes |
| grp_LPAEx_vs_CONEx_tissue-MUS | simple | MUS/LPAEx (6), MUS/CONEx (6) | yes |
| grp_LPASed_vs_CONEx_tissue-MUS | simple | MUS/LPASed (6), MUS/CONEx (6) | yes |
| grp_LPEx_vs_CONEx_tissue-MUS | simple | MUS/LPEx (6), MUS/CONEx (6) | yes |
| grp_LPSed_vs_CONEx_tissue-MUS | simple | MUS/LPSed (6), MUS/CONEx (6) | yes |
| grp_LPAEx_vs_CONSed_tissue-MUS | simple | MUS/LPAEx (6), MUS/CONSed (6) | yes |
| grp_LPASed_vs_CONSed_tissue-MUS | simple | MUS/LPASed (6), MUS/CONSed (6) | yes |
| grp_LPEx_vs_CONSed_tissue-MUS | simple | MUS/LPEx (6), MUS/CONSed (6) | yes |
| grp_LPSed_vs_CONSed_tissue-MUS | simple | MUS/LPSed (6), MUS/CONSed (6) | yes |
| grp_LPASed_vs_LPAEx_tissue-MUS | simple | MUS/LPASed (6), MUS/LPAEx (6) | yes |
| grp_LPEx_vs_LPAEx_tissue-MUS | simple | MUS/LPEx (6), MUS/LPAEx (6) | yes |
| grp_LPSed_vs_LPAEx_tissue-MUS | simple | MUS/LPSed (6), MUS/LPAEx (6) | yes |
| grp_LPEx_vs_LPASed_tissue-MUS | simple | MUS/LPEx (6), MUS/LPASed (6) | yes |
| grp_LPSed_vs_LPASed_tissue-MUS | simple | MUS/LPSed (6), MUS/LPASed (6) | yes |
| grp_LPSed_vs_LPEx_tissue-MUS | simple | MUS/LPSed (6), MUS/LPEx (6) | yes |
| grp_CONEx_vs_CONSed_tissue-PFC | simple | PFC/CONEx (6), PFC/CONSed (6) | yes |
| grp_LPAEx_vs_CONEx_tissue-PFC | simple | PFC/LPAEx (6), PFC/CONEx (6) | yes |
| grp_LPASed_vs_CONEx_tissue-PFC | simple | PFC/LPASed (6), PFC/CONEx (6) | yes |
| grp_LPEx_vs_CONEx_tissue-PFC | simple | PFC/LPEx (6), PFC/CONEx (6) | yes |
| grp_LPSed_vs_CONEx_tissue-PFC | simple | PFC/LPSed (6), PFC/CONEx (6) | yes |
| grp_LPAEx_vs_CONSed_tissue-PFC | simple | PFC/LPAEx (6), PFC/CONSed (6) | yes |
| grp_LPASed_vs_CONSed_tissue-PFC | simple | PFC/LPASed (6), PFC/CONSed (6) | yes |
| grp_LPEx_vs_CONSed_tissue-PFC | simple | PFC/LPEx (6), PFC/CONSed (6) | yes |
| grp_LPSed_vs_CONSed_tissue-PFC | simple | PFC/LPSed (6), PFC/CONSed (6) | yes |
| grp_LPASed_vs_LPAEx_tissue-PFC | simple | PFC/LPASed (6), PFC/LPAEx (6) | yes |
| grp_LPEx_vs_LPAEx_tissue-PFC | simple | PFC/LPEx (6), PFC/LPAEx (6) | yes |
| grp_LPSed_vs_LPAEx_tissue-PFC | simple | PFC/LPSed (6), PFC/LPAEx (6) | yes |
| grp_LPEx_vs_LPASed_tissue-PFC | simple | PFC/LPEx (6), PFC/LPASed (6) | yes |
| grp_LPSed_vs_LPASed_tissue-PFC | simple | PFC/LPSed (6), PFC/LPASed (6) | yes |
| grp_LPSed_vs_LPEx_tissue-PFC | simple | PFC/LPSed (6), PFC/LPEx (6) | yes |
| grp_LPAEx_vs_LPASed_tissue-COL | simple | COL/LPAEx (6), COL/LPASed (6) | yes |
| grp_LPAEx_vs_LPEx_tissue-COL | simple | COL/LPAEx (6), COL/LPEx (6) | yes |
| grp_LPAEx_vs_LPSed_tissue-COL | simple | COL/LPAEx (6), COL/LPSed (6) | yes |
| grp_LPAEx_vs_LPASed_tissue-HIP | simple | HIP/LPAEx (6), HIP/LPASed (6) | yes |
| grp_LPAEx_vs_LPEx_tissue-HIP | simple | HIP/LPAEx (6), HIP/LPEx (6) | yes |
| grp_LPAEx_vs_LPSed_tissue-HIP | simple | HIP/LPAEx (6), HIP/LPSed (6) | yes |
| grp_LPAEx_vs_LPASed_tissue-LIV | simple | LIV/LPAEx (6), LIV/LPASed (6) | yes |
| grp_LPAEx_vs_LPEx_tissue-LIV | simple | LIV/LPAEx (6), LIV/LPEx (5) | yes |
| grp_LPAEx_vs_LPSed_tissue-LIV | simple | LIV/LPAEx (6), LIV/LPSed (6) | yes |
| grp_LPAEx_vs_LPASed_tissue-MUS | simple | MUS/LPAEx (6), MUS/LPASed (6) | yes |
| grp_LPAEx_vs_LPEx_tissue-MUS | simple | MUS/LPAEx (6), MUS/LPEx (6) | yes |
| grp_LPAEx_vs_LPSed_tissue-MUS | simple | MUS/LPAEx (6), MUS/LPSed (6) | yes |
| grp_LPAEx_vs_LPASed_tissue-PFC | simple | PFC/LPAEx (6), PFC/LPASed (6) | yes |
| grp_LPAEx_vs_LPEx_tissue-PFC | simple | PFC/LPAEx (6), PFC/LPEx (6) | yes |
| grp_LPAEx_vs_LPSed_tissue-PFC | simple | PFC/LPAEx (6), PFC/LPSed (6) | yes |
