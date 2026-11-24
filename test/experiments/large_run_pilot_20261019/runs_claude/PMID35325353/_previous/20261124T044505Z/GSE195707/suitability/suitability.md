# Suitability: GSE195707

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | trt: 2 levels; surg: 2 levels |
| Covariance | pass | not_required; no candidates |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 20 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| trt_DQ_vs_Veh_surg-MOV | simple | MOV/DQ (5), MOV/Veh (5) | yes |
| trt_DQ_vs_Veh_surg-Sham | simple | Sham/DQ (5), Sham/Veh (5) | yes |
| surg_MOV_vs_Sham_trt-DQ | simple | DQ/MOV (5), DQ/Sham (5) | yes |
| surg_MOV_vs_Sham_trt-Veh | simple | Veh/MOV (5), Veh/Sham (5) | yes |
| trt_surg_DQ_MOV_vs_Veh_Sham | interaction | DQ/MOV (5), Veh/MOV (5), DQ/Sham (5), Veh/Sham (5) | yes |
