# Suitability: GSE226005

Verdict: **not_analyzable** (failed: sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | DESeq2 size-factor-normalized counts (non-integer), normalized separately per experiment batch; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 6 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | fail | 0/15 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_DG_vs_CTL1 | simple | DG (2), CTL1 (2) | no |
| grp_HYP_vs_CTL1 | simple | HYP (2), CTL1 (2) | no |
| grp_NOR_vs_CTL1 | simple | NOR (2), CTL1 (2) | no |
| grp_SEN_vs_CTL1 | simple | SEN (2), CTL1 (2) | no |
| grp_YNG_vs_CTL1 | simple | YNG (2), CTL1 (2) | no |
| grp_HYP_vs_DG | simple | HYP (2), DG (2) | no |
| grp_NOR_vs_DG | simple | NOR (2), DG (2) | no |
| grp_SEN_vs_DG | simple | SEN (2), DG (2) | no |
| grp_YNG_vs_DG | simple | YNG (2), DG (2) | no |
| grp_NOR_vs_HYP | simple | NOR (2), HYP (2) | no |
| grp_SEN_vs_HYP | simple | SEN (2), HYP (2) | no |
| grp_YNG_vs_HYP | simple | YNG (2), HYP (2) | no |
| grp_SEN_vs_NOR | simple | SEN (2), NOR (2) | no |
| grp_YNG_vs_NOR | simple | YNG (2), NOR (2) | no |
| grp_YNG_vs_SEN | simple | YNG (2), SEN (2) | no |
