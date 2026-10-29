# Suitability: GSE128078

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM (Cufflinks; gene-level sum of RefSeq isoform FPKM); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | time: 4 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 12/12 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 97 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| time_d2_vs_d1_grp-HC | simple | HC/d2 (11), HC/d1 (11) | yes |
| time_d3_vs_d1_grp-HC | simple | HC/d3 (11), HC/d1 (11) | yes |
| time_d7_vs_d1_grp-HC | simple | HC/d7 (11), HC/d1 (11) | yes |
| time_d3_vs_d2_grp-HC | simple | HC/d3 (11), HC/d2 (11) | yes |
| time_d7_vs_d2_grp-HC | simple | HC/d7 (11), HC/d2 (11) | yes |
| time_d7_vs_d3_grp-HC | simple | HC/d7 (11), HC/d3 (11) | yes |
| time_d2_vs_d1_grp-ME | simple | ME/d2 (14), ME/d1 (14) | yes |
| time_d3_vs_d1_grp-ME | simple | ME/d3 (13), ME/d1 (14) | yes |
| time_d7_vs_d1_grp-ME | simple | ME/d7 (12), ME/d1 (14) | yes |
| time_d3_vs_d2_grp-ME | simple | ME/d3 (13), ME/d2 (14) | yes |
| time_d7_vs_d2_grp-ME | simple | ME/d7 (12), ME/d2 (14) | yes |
| time_d7_vs_d3_grp-ME | simple | ME/d7 (12), ME/d3 (13) | yes |
