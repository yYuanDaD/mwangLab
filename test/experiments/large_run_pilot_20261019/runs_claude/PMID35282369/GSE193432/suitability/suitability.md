# Suitability: GSE193432

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_HFExe_vs_HFBAIBA | simple | HFExe (3), HFBAIBA (3) | yes |
| grp_HFBAIBA_vs_HFSed | simple | HFBAIBA (3), HFSed (3) | yes |
| grp_Sham_vs_HFBAIBA | simple | Sham (3), HFBAIBA (3) | yes |
| grp_HFExe_vs_HFSed | simple | HFExe (3), HFSed (3) | yes |
| grp_Sham_vs_HFExe | simple | Sham (3), HFExe (3) | yes |
| grp_Sham_vs_HFSed | simple | Sham (3), HFSed (3) | yes |
