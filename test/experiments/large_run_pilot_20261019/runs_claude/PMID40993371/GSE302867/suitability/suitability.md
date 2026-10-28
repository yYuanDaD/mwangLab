# Suitability: GSE302867

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; characteristics_ch1.5.batch: omit (constant: carries no batch information); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | partial | 6/6 comparisons have >= 3 per group; planned names not found: grp_KOEx_vs_KOSed, grp_KOEx_vs_WTEx |
| Sex | pass | Sex inference completed on 20 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_KOSed_vs_KOEx | simple | KOSed (5), KOEx (5) | yes |
| grp_WTEx_vs_KOEx | simple | WTEx (5), KOEx (5) | yes |
| grp_KOEx_vs_WTSed | simple | KOEx (5), WTSed (5) | yes |
| grp_WTEx_vs_KOSed | simple | WTEx (5), KOSed (5) | yes |
| grp_KOSed_vs_WTSed | simple | KOSed (5), WTSed (5) | yes |
| grp_WTEx_vs_WTSed | simple | WTEx (5), WTSed (5) | yes |
