# Suitability: GSE255280

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | geno: 2 levels; ex: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 20 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_ko_vs_veh_ex-ctrl | simple | ctrl/ko (5), ctrl/veh (5) | yes |
| geno_ko_vs_veh_ex-ex | simple | ex/ko (5), ex/veh (5) | yes |
| ex_ex_vs_ctrl_geno-ko | simple | ko/ex (5), ko/ctrl (5) | yes |
| ex_ex_vs_ctrl_geno-veh | simple | veh/ex (5), veh/ctrl (5) | yes |
| geno_ex_ko_ex_vs_veh_ctrl | interaction | ko/ex (5), veh/ex (5), ko/ctrl (5), veh/ctrl (5) | yes |
