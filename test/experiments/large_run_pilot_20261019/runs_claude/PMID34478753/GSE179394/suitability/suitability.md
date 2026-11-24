# Suitability: GSE179394

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | grp: 5 levels |
| Covariance | pass | not_required; characteristics_ch1.0.donor.allergen.dose: omit (one sample per subject per factor level set: an identifier, not a block); platform: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 30/30 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 138 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_HC_vs_CC_tissue-ewat | simple | ewat/HC (8), ewat/CC (8) | yes |
| grp_HCrw_vs_CC_tissue-ewat | simple | ewat/HCrw (8), ewat/CC (8) | yes |
| grp_CC_vs_HH_tissue-ewat | simple | ewat/CC (8), ewat/HH (8) | yes |
| grp_HHrw_vs_CC_tissue-ewat | simple | ewat/HHrw (10), ewat/CC (8) | yes |
| grp_HCrw_vs_HC_tissue-ewat | simple | ewat/HCrw (8), ewat/HC (8) | yes |
| grp_HC_vs_HH_tissue-ewat | simple | ewat/HC (8), ewat/HH (8) | yes |
| grp_HHrw_vs_HC_tissue-ewat | simple | ewat/HHrw (10), ewat/HC (8) | yes |
| grp_HCrw_vs_HH_tissue-ewat | simple | ewat/HCrw (8), ewat/HH (8) | yes |
| grp_HHrw_vs_HCrw_tissue-ewat | simple | ewat/HHrw (10), ewat/HCrw (8) | yes |
| grp_HHrw_vs_HH_tissue-ewat | simple | ewat/HHrw (10), ewat/HH (8) | yes |
| grp_HC_vs_CC_tissue-liver | simple | liver/HC (10), liver/CC (10) | yes |
| grp_HCrw_vs_CC_tissue-liver | simple | liver/HCrw (10), liver/CC (10) | yes |
| grp_CC_vs_HH_tissue-liver | simple | liver/CC (10), liver/HH (10) | yes |
| grp_HHrw_vs_CC_tissue-liver | simple | liver/HHrw (10), liver/CC (10) | yes |
| grp_HCrw_vs_HC_tissue-liver | simple | liver/HCrw (10), liver/HC (10) | yes |
| grp_HC_vs_HH_tissue-liver | simple | liver/HC (10), liver/HH (10) | yes |
| grp_HHrw_vs_HC_tissue-liver | simple | liver/HHrw (10), liver/HC (10) | yes |
| grp_HCrw_vs_HH_tissue-liver | simple | liver/HCrw (10), liver/HH (10) | yes |
| grp_HHrw_vs_HCrw_tissue-liver | simple | liver/HHrw (10), liver/HCrw (10) | yes |
| grp_HHrw_vs_HH_tissue-liver | simple | liver/HHrw (10), liver/HH (10) | yes |
| grp_HC_vs_CC_tissue-muscle | simple | muscle/HC (9), muscle/CC (7) | yes |
| grp_HCrw_vs_CC_tissue-muscle | simple | muscle/HCrw (10), muscle/CC (7) | yes |
| grp_CC_vs_HH_tissue-muscle | simple | muscle/CC (7), muscle/HH (10) | yes |
| grp_HHrw_vs_CC_tissue-muscle | simple | muscle/HHrw (10), muscle/CC (7) | yes |
| grp_HCrw_vs_HC_tissue-muscle | simple | muscle/HCrw (10), muscle/HC (9) | yes |
| grp_HC_vs_HH_tissue-muscle | simple | muscle/HC (9), muscle/HH (10) | yes |
| grp_HHrw_vs_HC_tissue-muscle | simple | muscle/HHrw (10), muscle/HC (9) | yes |
| grp_HCrw_vs_HH_tissue-muscle | simple | muscle/HCrw (10), muscle/HH (10) | yes |
| grp_HHrw_vs_HCrw_tissue-muscle | simple | muscle/HHrw (10), muscle/HCrw (10) | yes |
| grp_HHrw_vs_HH_tissue-muscle | simple | muscle/HHrw (10), muscle/HH (10) | yes |
