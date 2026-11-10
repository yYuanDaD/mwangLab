# Suitability: GSE183239

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (tximport gene-level counts from Salmon, UMI-deduplicated; deposited as integers); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 4 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 18/18 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 60 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_CDtr_vs_CDsed_tissue-SkM | simple | SkM/CDtr (5), SkM/CDsed (5) | yes |
| grp_HFDsed_vs_CDsed_tissue-SkM | simple | SkM/HFDsed (5), SkM/CDsed (5) | yes |
| grp_HFDtr_vs_CDsed_tissue-SkM | simple | SkM/HFDtr (5), SkM/CDsed (5) | yes |
| grp_HFDsed_vs_CDtr_tissue-SkM | simple | SkM/HFDsed (5), SkM/CDtr (5) | yes |
| grp_HFDtr_vs_CDtr_tissue-SkM | simple | SkM/HFDtr (5), SkM/CDtr (5) | yes |
| grp_HFDtr_vs_HFDsed_tissue-SkM | simple | SkM/HFDtr (5), SkM/HFDsed (5) | yes |
| grp_CDtr_vs_CDsed_tissue-scWAT | simple | scWAT/CDtr (5), scWAT/CDsed (5) | yes |
| grp_HFDsed_vs_CDsed_tissue-scWAT | simple | scWAT/HFDsed (5), scWAT/CDsed (5) | yes |
| grp_HFDtr_vs_CDsed_tissue-scWAT | simple | scWAT/HFDtr (5), scWAT/CDsed (5) | yes |
| grp_HFDsed_vs_CDtr_tissue-scWAT | simple | scWAT/HFDsed (5), scWAT/CDtr (5) | yes |
| grp_HFDtr_vs_CDtr_tissue-scWAT | simple | scWAT/HFDtr (5), scWAT/CDtr (5) | yes |
| grp_HFDtr_vs_HFDsed_tissue-scWAT | simple | scWAT/HFDtr (5), scWAT/HFDsed (5) | yes |
| grp_CDtr_vs_CDsed_tissue-vWAT | simple | vWAT/CDtr (5), vWAT/CDsed (5) | yes |
| grp_HFDsed_vs_CDsed_tissue-vWAT | simple | vWAT/HFDsed (5), vWAT/CDsed (5) | yes |
| grp_HFDtr_vs_CDsed_tissue-vWAT | simple | vWAT/HFDtr (5), vWAT/CDsed (5) | yes |
| grp_HFDsed_vs_CDtr_tissue-vWAT | simple | vWAT/HFDsed (5), vWAT/CDtr (5) | yes |
| grp_HFDtr_vs_CDtr_tissue-vWAT | simple | vWAT/HFDtr (5), vWAT/CDtr (5) | yes |
| grp_HFDtr_vs_HFDsed_tissue-vWAT | simple | vWAT/HFDtr (5), vWAT/HFDsed (5) | yes |
