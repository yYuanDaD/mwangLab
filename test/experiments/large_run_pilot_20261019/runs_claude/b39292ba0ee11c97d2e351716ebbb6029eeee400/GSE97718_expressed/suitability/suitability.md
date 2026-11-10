# Suitability: GSE97718_expressed

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 7/7 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_CONpost_vs_CONpre | simple | CONpost (4), CONpre (4) | yes |
| grp_HFDpost_vs_CONpost | simple | HFDpost (4), CONpost (4) | yes |
| grp_HFDpre_vs_CONpost | simple | HFDpre (4), CONpost (4) | yes |
| grp_HFDpost_vs_CONpre | simple | HFDpost (4), CONpre (4) | yes |
| grp_HFDpre_vs_CONpre | simple | HFDpre (4), CONpre (4) | yes |
| grp_HFDpre_vs_HFDpost | simple | HFDpre (4), HFDpost (4) | yes |
| grp_HFDpost_vs_HFDpre | simple | HFDpost (4), HFDpre (4) | yes |
