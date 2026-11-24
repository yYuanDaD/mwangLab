# Suitability: GSE205907

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 3 levels |
| Covariance | pass | not_required; animal: omit (one sample per subject per factor level set: an identifier, not a block) |
| Sample size | pass | 16/16 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 48 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_EX_vs_MPTP_tissue-Cereb | simple | Cereb/EX (4), Cereb/MPTP (4) | yes |
| grp_SAL_vs_EX_tissue-Cereb | simple | Cereb/SAL (4), Cereb/EX (4) | yes |
| grp_SAL_vs_MPTP_tissue-Cereb | simple | Cereb/SAL (4), Cereb/MPTP (4) | yes |
| grp_EX_vs_MPTP_tissue-Cortex | simple | Cortex/EX (4), Cortex/MPTP (4) | yes |
| grp_SAL_vs_EX_tissue-Cortex | simple | Cortex/SAL (4), Cortex/EX (4) | yes |
| grp_SAL_vs_MPTP_tissue-Cortex | simple | Cortex/SAL (4), Cortex/MPTP (4) | yes |
| grp_EX_vs_MPTP_tissue-Nigra | simple | Nigra/EX (4), Nigra/MPTP (4) | yes |
| grp_SAL_vs_EX_tissue-Nigra | simple | Nigra/SAL (4), Nigra/EX (4) | yes |
| grp_SAL_vs_MPTP_tissue-Nigra | simple | Nigra/SAL (4), Nigra/MPTP (4) | yes |
| grp_EX_vs_MPTP_tissue-Stria | simple | Stria/EX (4), Stria/MPTP (4) | yes |
| grp_SAL_vs_EX_tissue-Stria | simple | Stria/SAL (4), Stria/EX (4) | yes |
| grp_SAL_vs_MPTP_tissue-Stria | simple | Stria/SAL (4), Stria/MPTP (4) | yes |
| grp_MPTP_vs_SAL_tissue-Cereb | simple | Cereb/MPTP (4), Cereb/SAL (4) | yes |
| grp_MPTP_vs_SAL_tissue-Cortex | simple | Cortex/MPTP (4), Cortex/SAL (4) | yes |
| grp_MPTP_vs_SAL_tissue-Nigra | simple | Nigra/MPTP (4), Nigra/SAL (4) | yes |
| grp_MPTP_vs_SAL_tissue-Stria | simple | Stria/MPTP (4), Stria/SAL (4) | yes |
