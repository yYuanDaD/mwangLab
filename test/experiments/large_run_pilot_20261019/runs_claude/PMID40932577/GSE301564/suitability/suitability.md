# Suitability: GSE301564

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | frail: 2 levels; run: 2 levels |
| Covariance | pass | not_required; animal: omit (one sample per subject per factor level set: an identifier, not a block); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| frail_high_vs_low_run-run | simple | run/high (4), run/low (4) | yes |
| frail_high_vs_low_run-sed | simple | sed/high (3), sed/low (4) | yes |
| run_run_vs_sed_frail-high | simple | high/run (4), high/sed (3) | yes |
| run_run_vs_sed_frail-low | simple | low/run (4), low/sed (4) | yes |
| frail_run_high_run_vs_low_sed | interaction | high/run (4), low/run (4), high/sed (3), low/sed (4) | yes |
