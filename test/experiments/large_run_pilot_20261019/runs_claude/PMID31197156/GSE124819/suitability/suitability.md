# Suitability: GSE124819

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | set: 2 levels; cond: 6 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | partial | 16/41 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference completed on 37 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| set_act_vs_ex_cond-cont | simple | cont/act (5), cont/ex (4) | yes |
| set_act_vs_ex_cond-large | simple | large/act (5), large/ex (0) | no |
| set_act_vs_ex_cond-nosci | simple | nosci/act (5), nosci/ex (4) | yes |
| set_act_vs_ex_cond-swim | simple | swim/act (0), swim/ex (5) | no |
| set_act_vs_ex_cond-sww | simple | sww/act (0), sww/ex (5) | no |
| set_act_vs_ex_cond-tx | simple | tx/act (0), tx/ex (4) | no |
| cond_large_vs_cont_set-act | simple | act/large (5), act/cont (5) | yes |
| cond_nosci_vs_cont_set-act | simple | act/nosci (5), act/cont (5) | yes |
| cond_swim_vs_cont_set-act | simple | act/swim (0), act/cont (5) | no |
| cond_sww_vs_cont_set-act | simple | act/sww (0), act/cont (5) | no |
| cond_tx_vs_cont_set-act | simple | act/tx (0), act/cont (5) | no |
| cond_nosci_vs_large_set-act | simple | act/nosci (5), act/large (5) | yes |
| cond_swim_vs_large_set-act | simple | act/swim (0), act/large (5) | no |
| cond_sww_vs_large_set-act | simple | act/sww (0), act/large (5) | no |
| cond_tx_vs_large_set-act | simple | act/tx (0), act/large (5) | no |
| cond_swim_vs_nosci_set-act | simple | act/swim (0), act/nosci (5) | no |
| cond_sww_vs_nosci_set-act | simple | act/sww (0), act/nosci (5) | no |
| cond_tx_vs_nosci_set-act | simple | act/tx (0), act/nosci (5) | no |
| cond_sww_vs_swim_set-act | simple | act/sww (0), act/swim (0) | no |
| cond_tx_vs_swim_set-act | simple | act/tx (0), act/swim (0) | no |
| cond_tx_vs_sww_set-act | simple | act/tx (0), act/sww (0) | no |
| cond_large_vs_cont_set-ex | simple | ex/large (0), ex/cont (4) | no |
| cond_nosci_vs_cont_set-ex | simple | ex/nosci (4), ex/cont (4) | yes |
| cond_swim_vs_cont_set-ex | simple | ex/swim (5), ex/cont (4) | yes |
| cond_sww_vs_cont_set-ex | simple | ex/sww (5), ex/cont (4) | yes |
| cond_tx_vs_cont_set-ex | simple | ex/tx (4), ex/cont (4) | yes |
| cond_nosci_vs_large_set-ex | simple | ex/nosci (4), ex/large (0) | no |
| cond_swim_vs_large_set-ex | simple | ex/swim (5), ex/large (0) | no |
| cond_sww_vs_large_set-ex | simple | ex/sww (5), ex/large (0) | no |
| cond_tx_vs_large_set-ex | simple | ex/tx (4), ex/large (0) | no |
| cond_swim_vs_nosci_set-ex | simple | ex/swim (5), ex/nosci (4) | yes |
| cond_sww_vs_nosci_set-ex | simple | ex/sww (5), ex/nosci (4) | yes |
| cond_tx_vs_nosci_set-ex | simple | ex/tx (4), ex/nosci (4) | yes |
| cond_sww_vs_swim_set-ex | simple | ex/sww (5), ex/swim (5) | yes |
| cond_tx_vs_swim_set-ex | simple | ex/tx (4), ex/swim (5) | yes |
| cond_tx_vs_sww_set-ex | simple | ex/tx (4), ex/sww (5) | yes |
| set_cond_act_large_vs_ex_cont | interaction | act/large (5), ex/large (0), act/cont (5), ex/cont (4) | no |
| set_cond_act_nosci_vs_ex_cont | interaction | act/nosci (5), ex/nosci (4), act/cont (5), ex/cont (4) | yes |
| set_cond_act_swim_vs_ex_cont | interaction | act/swim (0), ex/swim (5), act/cont (5), ex/cont (4) | no |
| set_cond_act_sww_vs_ex_cont | interaction | act/sww (0), ex/sww (5), act/cont (5), ex/cont (4) | no |
| set_cond_act_tx_vs_ex_cont | interaction | act/tx (0), ex/tx (4), act/cont (5), ex/cont (4) | no |
