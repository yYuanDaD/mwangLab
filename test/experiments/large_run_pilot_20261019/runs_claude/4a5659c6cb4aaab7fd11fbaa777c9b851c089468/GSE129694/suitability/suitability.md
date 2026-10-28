# Suitability: GSE129694

Verdict: **not_analyzable** (failed: covariance)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | fail | not_required; time: stop (primary_nested_in_candidate with a design factor: its effect cannot be separated) |
| Sample size | pass | 10/10 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference completed on 20 samples.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_NoSCI_vs_CONT | simple | NoSCI (4), CONT (4) | yes |
| grp_SWIM_vs_CONT | simple | SWIM (4), CONT (4) | yes |
| grp_SWW_vs_CONT | simple | SWW (4), CONT (4) | yes |
| grp_TX_vs_CONT | simple | TX (4), CONT (4) | yes |
| grp_SWIM_vs_NoSCI | simple | SWIM (4), NoSCI (4) | yes |
| grp_SWW_vs_NoSCI | simple | SWW (4), NoSCI (4) | yes |
| grp_TX_vs_NoSCI | simple | TX (4), NoSCI (4) | yes |
| grp_SWW_vs_SWIM | simple | SWW (4), SWIM (4) | yes |
| grp_TX_vs_SWIM | simple | TX (4), SWIM (4) | yes |
| grp_TX_vs_SWW | simple | TX (4), SWW (4) | yes |
