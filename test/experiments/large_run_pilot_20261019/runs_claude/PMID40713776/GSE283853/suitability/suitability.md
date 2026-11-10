# Suitability: GSE283853

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference completed on 12 samples.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_MAFA_vs_MAF | simple | MAFA (3), MAF (3) | yes |
| grp_MAFB_vs_MAF | simple | MAFB (3), MAF (3) | yes |
| grp_MAF_vs_mCherry | simple | MAF (3), mCherry (3) | yes |
| grp_MAFB_vs_MAFA | simple | MAFB (3), MAFA (3) | yes |
| grp_MAFA_vs_mCherry | simple | MAFA (3), mCherry (3) | yes |
| grp_MAFB_vs_mCherry | simple | MAFB (3), mCherry (3) | yes |
