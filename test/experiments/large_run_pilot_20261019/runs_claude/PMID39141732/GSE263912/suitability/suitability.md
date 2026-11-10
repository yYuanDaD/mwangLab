# Suitability: GSE263912

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | linear normalized (TMM-normalized CPM); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | geno: 3 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 3/3 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| geno_AKO_vs_AGKO | simple | AKO (3), AGKO (3) | yes |
| geno_AGKO_vs_CTRL | simple | AGKO (3), CTRL (3) | yes |
| geno_AKO_vs_CTRL | simple | AKO (3), CTRL (3) | yes |
