# Suitability: GSE297515_PIEZO_AEX

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | cond: 2 levels; geno: 2 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| cond_AEX_vs_SED_geno-FL | simple | FL/AEX (3), FL/SED (3) | yes |
| cond_AEX_vs_SED_geno-WT | simple | WT/AEX (3), WT/SED (3) | yes |
| geno_FL_vs_WT_cond-AEX | simple | AEX/FL (3), AEX/WT (3) | yes |
| geno_FL_vs_WT_cond-SED | simple | SED/FL (3), SED/WT (3) | yes |
| cond_geno_AEX_FL_vs_SED_WT | interaction | AEX/FL (3), SED/FL (3), AEX/WT (3), SED/WT (3) | yes |
