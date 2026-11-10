# Suitability: GSE194193

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | train: 2 levels; nr: 2 levels; pt: 2 levels |
| Covariance | pass | not_required; rin: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 18/18 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 62 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| train_VWR_vs_SED_nr-NR_pt-PT | simple | NR/PT/VWR (8), NR/PT/SED (8) | yes |
| train_VWR_vs_SED_nr-NR_pt-noPT | simple | NR/noPT/VWR (7), NR/noPT/SED (8) | yes |
| train_VWR_vs_SED_nr-Sal_pt-PT | simple | Sal/PT/VWR (8), Sal/PT/SED (8) | yes |
| train_VWR_vs_SED_nr-Sal_pt-noPT | simple | Sal/noPT/VWR (7), Sal/noPT/SED (8) | yes |
| nr_NR_vs_Sal_train-SED_pt-PT | simple | SED/PT/NR (8), SED/PT/Sal (8) | yes |
| nr_NR_vs_Sal_train-SED_pt-noPT | simple | SED/noPT/NR (8), SED/noPT/Sal (8) | yes |
| nr_NR_vs_Sal_train-VWR_pt-PT | simple | VWR/PT/NR (8), VWR/PT/Sal (8) | yes |
| nr_NR_vs_Sal_train-VWR_pt-noPT | simple | VWR/noPT/NR (7), VWR/noPT/Sal (7) | yes |
| pt_PT_vs_noPT_train-SED_nr-NR | simple | SED/NR/PT (8), SED/NR/noPT (8) | yes |
| pt_PT_vs_noPT_train-SED_nr-Sal | simple | SED/Sal/PT (8), SED/Sal/noPT (8) | yes |
| pt_PT_vs_noPT_train-VWR_nr-NR | simple | VWR/NR/PT (8), VWR/NR/noPT (7) | yes |
| pt_PT_vs_noPT_train-VWR_nr-Sal | simple | VWR/Sal/PT (8), VWR/Sal/noPT (7) | yes |
| train_nr_VWR_NR_vs_SED_Sal_pt-PT | interaction | PT/VWR/NR (8), PT/SED/NR (8), PT/VWR/Sal (8), PT/SED/Sal (8) | yes |
| train_nr_VWR_NR_vs_SED_Sal_pt-noPT | interaction | noPT/VWR/NR (7), noPT/SED/NR (8), noPT/VWR/Sal (7), noPT/SED/Sal (8) | yes |
| train_pt_VWR_PT_vs_SED_noPT_nr-NR | interaction | NR/VWR/PT (8), NR/SED/PT (8), NR/VWR/noPT (7), NR/SED/noPT (8) | yes |
| train_pt_VWR_PT_vs_SED_noPT_nr-Sal | interaction | Sal/VWR/PT (8), Sal/SED/PT (8), Sal/VWR/noPT (7), Sal/SED/noPT (8) | yes |
| nr_pt_NR_PT_vs_Sal_noPT_train-SED | interaction | SED/NR/PT (8), SED/Sal/PT (8), SED/NR/noPT (8), SED/Sal/noPT (8) | yes |
| nr_pt_NR_PT_vs_Sal_noPT_train-VWR | interaction | VWR/NR/PT (8), VWR/Sal/PT (8), VWR/NR/noPT (7), VWR/Sal/noPT (7) | yes |
