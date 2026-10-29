# Suitability: GSE285114

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | normalized counts (DESeq2-style size-factor normalized featureCounts); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 1/1 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 8 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_KO_vs_WT | simple | KO (4), WT (4) | yes |
