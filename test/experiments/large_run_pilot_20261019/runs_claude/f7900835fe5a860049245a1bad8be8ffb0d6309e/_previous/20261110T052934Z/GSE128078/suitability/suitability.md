# Suitability: GSE128078

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM (linear; gene-level sum of Cufflinks isoform FPKM); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | day: 4 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 12/12 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 97 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| day_d2_vs_d1_dzraw-CFS | simple | CFS/d2 (14), CFS/d1 (14) | yes |
| day_d3_vs_d1_dzraw-CFS | simple | CFS/d3 (13), CFS/d1 (14) | yes |
| day_d7_vs_d1_dzraw-CFS | simple | CFS/d7 (12), CFS/d1 (14) | yes |
| day_d3_vs_d2_dzraw-CFS | simple | CFS/d3 (13), CFS/d2 (14) | yes |
| day_d7_vs_d2_dzraw-CFS | simple | CFS/d7 (12), CFS/d2 (14) | yes |
| day_d7_vs_d3_dzraw-CFS | simple | CFS/d7 (12), CFS/d3 (13) | yes |
| day_d2_vs_d1_dzraw-HC | simple | HC/d2 (11), HC/d1 (11) | yes |
| day_d3_vs_d1_dzraw-HC | simple | HC/d3 (11), HC/d1 (11) | yes |
| day_d7_vs_d1_dzraw-HC | simple | HC/d7 (11), HC/d1 (11) | yes |
| day_d3_vs_d2_dzraw-HC | simple | HC/d3 (11), HC/d2 (11) | yes |
| day_d7_vs_d2_dzraw-HC | simple | HC/d7 (11), HC/d2 (11) | yes |
| day_d7_vs_d3_dzraw-HC | simple | HC/d7 (11), HC/d3 (11) | yes |
