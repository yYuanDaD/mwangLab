# Suitability: GSE283691

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | log-scale (DESeq2 rlog-transformed values); route: limma |
| Grouping | pass | grp: 7 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 6/6 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 48 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: normalized log-scale intensity matrix (series matrix); platform annotation (probe -> gene). fields: sample ID; group / condition; subject ID for repeated samples; sex; batch |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_EXI_vs_HFD | simple | EXI (7), HFD (7) | yes |
| grp_KD_vs_HFD | simple | KD (7), HFD (7) | yes |
| grp_KDI_vs_HFD | simple | KDI (7), HFD (7) | yes |
| grp_KDIEXI_vs_HFD | simple | KDIEXI (6), HFD (7) | yes |
| grp_SD_vs_HFD | simple | SD (7), HFD (7) | yes |
| grp_SDI_vs_HFD | simple | SDI (7), HFD (7) | yes |
