# Suitability: PMID40650303

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | dis: 2 levels; ex: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| dis_CC_vs_Ctl_ex-Ex | simple | Ex/CC (6), Ex/Ctl (6) | yes |
| dis_CC_vs_Ctl_ex-Sed | simple | Sed/CC (6), Sed/Ctl (6) | yes |
| ex_Ex_vs_Sed_dis-CC | simple | CC/Ex (6), CC/Sed (6) | yes |
| ex_Ex_vs_Sed_dis-Ctl | simple | Ctl/Ex (6), Ctl/Sed (6) | yes |
| dis_ex_CC_Ex_vs_Ctl_Sed | interaction | CC/Ex (6), Ctl/Ex (6), CC/Sed (6), Ctl/Sed (6) | yes |
