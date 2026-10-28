# Suitability: GSE178262_wheel

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (tximport lengthScaledTPM gene-level pseudo-counts from kallisto); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | act: 2 levels; zt: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| act_DA_vs_CTRL_zt-Z04 | simple | Z04/DA (4), Z04/CTRL (4) | yes |
| act_DA_vs_CTRL_zt-Z16 | simple | Z16/DA (4), Z16/CTRL (4) | yes |
| zt_Z16_vs_Z04_act-CTRL | simple | CTRL/Z16 (4), CTRL/Z04 (4) | yes |
| zt_Z16_vs_Z04_act-DA | simple | DA/Z16 (4), DA/Z04 (4) | yes |
| act_zt_DA_Z16_vs_CTRL_Z04 | interaction | DA/Z16 (4), CTRL/Z16 (4), DA/Z04 (4), CTRL/Z04 (4) | yes |
