# Suitability: GSE114062

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | library-size-normalized counts (Cuffnorm count table: fragment counts divided by a per-sample size factor; file labelled FPKM); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | line: 2 levels; region: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| line_Hi_vs_Co_region-Ce | simple | Ce/Hi (4), Ce/Co (4) | yes |
| line_Hi_vs_Co_region-St | simple | St/Hi (3), St/Co (4) | yes |
| region_St_vs_Ce_line-Co | simple | Co/St (4), Co/Ce (4) | yes |
| region_St_vs_Ce_line-Hi | simple | Hi/St (3), Hi/Ce (4) | yes |
| line_region_Hi_St_vs_Co_Ce | interaction | Hi/St (3), Co/St (4), Hi/Ce (4), Co/Ce (4) | yes |
