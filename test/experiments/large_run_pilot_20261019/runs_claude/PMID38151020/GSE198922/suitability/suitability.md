# Suitability: GSE198922

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | CPM (linear normalized counts); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | time: 3 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 143 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_POST_vs_PRE_dx-NGT | simple | NGT/POST (20), NGT/PRE (20) | yes |
| time_REC_vs_POST_dx-NGT | simple | NGT/REC (20), NGT/POST (20) | yes |
| time_REC_vs_PRE_dx-NGT | simple | NGT/REC (20), NGT/PRE (20) | yes |
| time_POST_vs_PRE_dx-T2D | simple | T2D/POST (27), T2D/PRE (28) | yes |
| time_REC_vs_POST_dx-T2D | simple | T2D/REC (28), T2D/POST (27) | yes |
| time_REC_vs_PRE_dx-T2D | simple | T2D/REC (28), T2D/PRE (28) | yes |
