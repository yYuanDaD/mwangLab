# Suitability: GSE126962

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | linear normalized (CPM, pre-filtered); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | trt: 2 levels; phase: 2 levels; hpe: 6 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 110/110 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 137 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| trt_EX_vs_SED_phase-ACT_hpe-h0 | simple | ACT/h0/EX (6), ACT/h0/SED (6) | yes |
| trt_EX_vs_SED_phase-ACT_hpe-h12 | simple | ACT/h12/EX (6), ACT/h12/SED (6) | yes |
| trt_EX_vs_SED_phase-ACT_hpe-h16 | simple | ACT/h16/EX (6), ACT/h16/SED (5) | yes |
| trt_EX_vs_SED_phase-ACT_hpe-h20 | simple | ACT/h20/EX (6), ACT/h20/SED (6) | yes |
| trt_EX_vs_SED_phase-ACT_hpe-h4 | simple | ACT/h4/EX (5), ACT/h4/SED (6) | yes |
| trt_EX_vs_SED_phase-ACT_hpe-h8 | simple | ACT/h8/EX (5), ACT/h8/SED (6) | yes |
| trt_EX_vs_SED_phase-REST_hpe-h0 | simple | REST/h0/EX (4), REST/h0/SED (5) | yes |
| trt_EX_vs_SED_phase-REST_hpe-h12 | simple | REST/h12/EX (6), REST/h12/SED (6) | yes |
| trt_EX_vs_SED_phase-REST_hpe-h16 | simple | REST/h16/EX (6), REST/h16/SED (6) | yes |
| trt_EX_vs_SED_phase-REST_hpe-h20 | simple | REST/h20/EX (6), REST/h20/SED (6) | yes |
| trt_EX_vs_SED_phase-REST_hpe-h4 | simple | REST/h4/EX (6), REST/h4/SED (6) | yes |
| trt_EX_vs_SED_phase-REST_hpe-h8 | simple | REST/h8/EX (6), REST/h8/SED (5) | yes |
| phase_ACT_vs_REST_trt-EX_hpe-h0 | simple | EX/h0/ACT (6), EX/h0/REST (4) | yes |
| phase_ACT_vs_REST_trt-EX_hpe-h12 | simple | EX/h12/ACT (6), EX/h12/REST (6) | yes |
| phase_ACT_vs_REST_trt-EX_hpe-h16 | simple | EX/h16/ACT (6), EX/h16/REST (6) | yes |
| phase_ACT_vs_REST_trt-EX_hpe-h20 | simple | EX/h20/ACT (6), EX/h20/REST (6) | yes |
| phase_ACT_vs_REST_trt-EX_hpe-h4 | simple | EX/h4/ACT (5), EX/h4/REST (6) | yes |
| phase_ACT_vs_REST_trt-EX_hpe-h8 | simple | EX/h8/ACT (5), EX/h8/REST (6) | yes |
| phase_ACT_vs_REST_trt-SED_hpe-h0 | simple | SED/h0/ACT (6), SED/h0/REST (5) | yes |
| phase_ACT_vs_REST_trt-SED_hpe-h12 | simple | SED/h12/ACT (6), SED/h12/REST (6) | yes |
| phase_ACT_vs_REST_trt-SED_hpe-h16 | simple | SED/h16/ACT (5), SED/h16/REST (6) | yes |
| phase_ACT_vs_REST_trt-SED_hpe-h20 | simple | SED/h20/ACT (6), SED/h20/REST (6) | yes |
| phase_ACT_vs_REST_trt-SED_hpe-h4 | simple | SED/h4/ACT (6), SED/h4/REST (6) | yes |
| phase_ACT_vs_REST_trt-SED_hpe-h8 | simple | SED/h8/ACT (6), SED/h8/REST (5) | yes |
| hpe_h4_vs_h0_trt-EX_phase-ACT | simple | EX/ACT/h4 (5), EX/ACT/h0 (6) | yes |
| hpe_h8_vs_h0_trt-EX_phase-ACT | simple | EX/ACT/h8 (5), EX/ACT/h0 (6) | yes |
| hpe_h12_vs_h0_trt-EX_phase-ACT | simple | EX/ACT/h12 (6), EX/ACT/h0 (6) | yes |
| hpe_h16_vs_h0_trt-EX_phase-ACT | simple | EX/ACT/h16 (6), EX/ACT/h0 (6) | yes |
| hpe_h20_vs_h0_trt-EX_phase-ACT | simple | EX/ACT/h20 (6), EX/ACT/h0 (6) | yes |
| hpe_h8_vs_h4_trt-EX_phase-ACT | simple | EX/ACT/h8 (5), EX/ACT/h4 (5) | yes |
| hpe_h12_vs_h4_trt-EX_phase-ACT | simple | EX/ACT/h12 (6), EX/ACT/h4 (5) | yes |
| hpe_h16_vs_h4_trt-EX_phase-ACT | simple | EX/ACT/h16 (6), EX/ACT/h4 (5) | yes |
| hpe_h20_vs_h4_trt-EX_phase-ACT | simple | EX/ACT/h20 (6), EX/ACT/h4 (5) | yes |
| hpe_h12_vs_h8_trt-EX_phase-ACT | simple | EX/ACT/h12 (6), EX/ACT/h8 (5) | yes |
| hpe_h16_vs_h8_trt-EX_phase-ACT | simple | EX/ACT/h16 (6), EX/ACT/h8 (5) | yes |
| hpe_h20_vs_h8_trt-EX_phase-ACT | simple | EX/ACT/h20 (6), EX/ACT/h8 (5) | yes |
| hpe_h16_vs_h12_trt-EX_phase-ACT | simple | EX/ACT/h16 (6), EX/ACT/h12 (6) | yes |
| hpe_h20_vs_h12_trt-EX_phase-ACT | simple | EX/ACT/h20 (6), EX/ACT/h12 (6) | yes |
| hpe_h20_vs_h16_trt-EX_phase-ACT | simple | EX/ACT/h20 (6), EX/ACT/h16 (6) | yes |
| hpe_h4_vs_h0_trt-EX_phase-REST | simple | EX/REST/h4 (6), EX/REST/h0 (4) | yes |
| hpe_h8_vs_h0_trt-EX_phase-REST | simple | EX/REST/h8 (6), EX/REST/h0 (4) | yes |
| hpe_h12_vs_h0_trt-EX_phase-REST | simple | EX/REST/h12 (6), EX/REST/h0 (4) | yes |
| hpe_h16_vs_h0_trt-EX_phase-REST | simple | EX/REST/h16 (6), EX/REST/h0 (4) | yes |
| hpe_h20_vs_h0_trt-EX_phase-REST | simple | EX/REST/h20 (6), EX/REST/h0 (4) | yes |
| hpe_h8_vs_h4_trt-EX_phase-REST | simple | EX/REST/h8 (6), EX/REST/h4 (6) | yes |
| hpe_h12_vs_h4_trt-EX_phase-REST | simple | EX/REST/h12 (6), EX/REST/h4 (6) | yes |
| hpe_h16_vs_h4_trt-EX_phase-REST | simple | EX/REST/h16 (6), EX/REST/h4 (6) | yes |
| hpe_h20_vs_h4_trt-EX_phase-REST | simple | EX/REST/h20 (6), EX/REST/h4 (6) | yes |
| hpe_h12_vs_h8_trt-EX_phase-REST | simple | EX/REST/h12 (6), EX/REST/h8 (6) | yes |
| hpe_h16_vs_h8_trt-EX_phase-REST | simple | EX/REST/h16 (6), EX/REST/h8 (6) | yes |
| hpe_h20_vs_h8_trt-EX_phase-REST | simple | EX/REST/h20 (6), EX/REST/h8 (6) | yes |
| hpe_h16_vs_h12_trt-EX_phase-REST | simple | EX/REST/h16 (6), EX/REST/h12 (6) | yes |
| hpe_h20_vs_h12_trt-EX_phase-REST | simple | EX/REST/h20 (6), EX/REST/h12 (6) | yes |
| hpe_h20_vs_h16_trt-EX_phase-REST | simple | EX/REST/h20 (6), EX/REST/h16 (6) | yes |
| hpe_h4_vs_h0_trt-SED_phase-ACT | simple | SED/ACT/h4 (6), SED/ACT/h0 (6) | yes |
| hpe_h8_vs_h0_trt-SED_phase-ACT | simple | SED/ACT/h8 (6), SED/ACT/h0 (6) | yes |
| hpe_h12_vs_h0_trt-SED_phase-ACT | simple | SED/ACT/h12 (6), SED/ACT/h0 (6) | yes |
| hpe_h16_vs_h0_trt-SED_phase-ACT | simple | SED/ACT/h16 (5), SED/ACT/h0 (6) | yes |
| hpe_h20_vs_h0_trt-SED_phase-ACT | simple | SED/ACT/h20 (6), SED/ACT/h0 (6) | yes |
| hpe_h8_vs_h4_trt-SED_phase-ACT | simple | SED/ACT/h8 (6), SED/ACT/h4 (6) | yes |
| hpe_h12_vs_h4_trt-SED_phase-ACT | simple | SED/ACT/h12 (6), SED/ACT/h4 (6) | yes |
| hpe_h16_vs_h4_trt-SED_phase-ACT | simple | SED/ACT/h16 (5), SED/ACT/h4 (6) | yes |
| hpe_h20_vs_h4_trt-SED_phase-ACT | simple | SED/ACT/h20 (6), SED/ACT/h4 (6) | yes |
| hpe_h12_vs_h8_trt-SED_phase-ACT | simple | SED/ACT/h12 (6), SED/ACT/h8 (6) | yes |
| hpe_h16_vs_h8_trt-SED_phase-ACT | simple | SED/ACT/h16 (5), SED/ACT/h8 (6) | yes |
| hpe_h20_vs_h8_trt-SED_phase-ACT | simple | SED/ACT/h20 (6), SED/ACT/h8 (6) | yes |
| hpe_h16_vs_h12_trt-SED_phase-ACT | simple | SED/ACT/h16 (5), SED/ACT/h12 (6) | yes |
| hpe_h20_vs_h12_trt-SED_phase-ACT | simple | SED/ACT/h20 (6), SED/ACT/h12 (6) | yes |
| hpe_h20_vs_h16_trt-SED_phase-ACT | simple | SED/ACT/h20 (6), SED/ACT/h16 (5) | yes |
| hpe_h4_vs_h0_trt-SED_phase-REST | simple | SED/REST/h4 (6), SED/REST/h0 (5) | yes |
| hpe_h8_vs_h0_trt-SED_phase-REST | simple | SED/REST/h8 (5), SED/REST/h0 (5) | yes |
| hpe_h12_vs_h0_trt-SED_phase-REST | simple | SED/REST/h12 (6), SED/REST/h0 (5) | yes |
| hpe_h16_vs_h0_trt-SED_phase-REST | simple | SED/REST/h16 (6), SED/REST/h0 (5) | yes |
| hpe_h20_vs_h0_trt-SED_phase-REST | simple | SED/REST/h20 (6), SED/REST/h0 (5) | yes |
| hpe_h8_vs_h4_trt-SED_phase-REST | simple | SED/REST/h8 (5), SED/REST/h4 (6) | yes |
| hpe_h12_vs_h4_trt-SED_phase-REST | simple | SED/REST/h12 (6), SED/REST/h4 (6) | yes |
| hpe_h16_vs_h4_trt-SED_phase-REST | simple | SED/REST/h16 (6), SED/REST/h4 (6) | yes |
| hpe_h20_vs_h4_trt-SED_phase-REST | simple | SED/REST/h20 (6), SED/REST/h4 (6) | yes |
| hpe_h12_vs_h8_trt-SED_phase-REST | simple | SED/REST/h12 (6), SED/REST/h8 (5) | yes |
| hpe_h16_vs_h8_trt-SED_phase-REST | simple | SED/REST/h16 (6), SED/REST/h8 (5) | yes |
| hpe_h20_vs_h8_trt-SED_phase-REST | simple | SED/REST/h20 (6), SED/REST/h8 (5) | yes |
| hpe_h16_vs_h12_trt-SED_phase-REST | simple | SED/REST/h16 (6), SED/REST/h12 (6) | yes |
| hpe_h20_vs_h12_trt-SED_phase-REST | simple | SED/REST/h20 (6), SED/REST/h12 (6) | yes |
| hpe_h20_vs_h16_trt-SED_phase-REST | simple | SED/REST/h20 (6), SED/REST/h16 (6) | yes |
| trt_phase_EX_ACT_vs_SED_REST_hpe-h0 | interaction | h0/EX/ACT (6), h0/SED/ACT (6), h0/EX/REST (4), h0/SED/REST (5) | yes |
| trt_phase_EX_ACT_vs_SED_REST_hpe-h12 | interaction | h12/EX/ACT (6), h12/SED/ACT (6), h12/EX/REST (6), h12/SED/REST (6) | yes |
| trt_phase_EX_ACT_vs_SED_REST_hpe-h16 | interaction | h16/EX/ACT (6), h16/SED/ACT (5), h16/EX/REST (6), h16/SED/REST (6) | yes |
| trt_phase_EX_ACT_vs_SED_REST_hpe-h20 | interaction | h20/EX/ACT (6), h20/SED/ACT (6), h20/EX/REST (6), h20/SED/REST (6) | yes |
| trt_phase_EX_ACT_vs_SED_REST_hpe-h4 | interaction | h4/EX/ACT (5), h4/SED/ACT (6), h4/EX/REST (6), h4/SED/REST (6) | yes |
| trt_phase_EX_ACT_vs_SED_REST_hpe-h8 | interaction | h8/EX/ACT (5), h8/SED/ACT (6), h8/EX/REST (6), h8/SED/REST (5) | yes |
| trt_hpe_EX_h12_vs_SED_h0_phase-ACT | interaction | ACT/EX/h12 (6), ACT/SED/h12 (6), ACT/EX/h0 (6), ACT/SED/h0 (6) | yes |
| trt_hpe_EX_h16_vs_SED_h0_phase-ACT | interaction | ACT/EX/h16 (6), ACT/SED/h16 (5), ACT/EX/h0 (6), ACT/SED/h0 (6) | yes |
| trt_hpe_EX_h20_vs_SED_h0_phase-ACT | interaction | ACT/EX/h20 (6), ACT/SED/h20 (6), ACT/EX/h0 (6), ACT/SED/h0 (6) | yes |
| trt_hpe_EX_h4_vs_SED_h0_phase-ACT | interaction | ACT/EX/h4 (5), ACT/SED/h4 (6), ACT/EX/h0 (6), ACT/SED/h0 (6) | yes |
| trt_hpe_EX_h8_vs_SED_h0_phase-ACT | interaction | ACT/EX/h8 (5), ACT/SED/h8 (6), ACT/EX/h0 (6), ACT/SED/h0 (6) | yes |
| trt_hpe_EX_h12_vs_SED_h0_phase-REST | interaction | REST/EX/h12 (6), REST/SED/h12 (6), REST/EX/h0 (4), REST/SED/h0 (5) | yes |
| trt_hpe_EX_h16_vs_SED_h0_phase-REST | interaction | REST/EX/h16 (6), REST/SED/h16 (6), REST/EX/h0 (4), REST/SED/h0 (5) | yes |
| trt_hpe_EX_h20_vs_SED_h0_phase-REST | interaction | REST/EX/h20 (6), REST/SED/h20 (6), REST/EX/h0 (4), REST/SED/h0 (5) | yes |
| trt_hpe_EX_h4_vs_SED_h0_phase-REST | interaction | REST/EX/h4 (6), REST/SED/h4 (6), REST/EX/h0 (4), REST/SED/h0 (5) | yes |
| trt_hpe_EX_h8_vs_SED_h0_phase-REST | interaction | REST/EX/h8 (6), REST/SED/h8 (5), REST/EX/h0 (4), REST/SED/h0 (5) | yes |
| phase_hpe_ACT_h12_vs_REST_h0_trt-EX | interaction | EX/ACT/h12 (6), EX/REST/h12 (6), EX/ACT/h0 (6), EX/REST/h0 (4) | yes |
| phase_hpe_ACT_h16_vs_REST_h0_trt-EX | interaction | EX/ACT/h16 (6), EX/REST/h16 (6), EX/ACT/h0 (6), EX/REST/h0 (4) | yes |
| phase_hpe_ACT_h20_vs_REST_h0_trt-EX | interaction | EX/ACT/h20 (6), EX/REST/h20 (6), EX/ACT/h0 (6), EX/REST/h0 (4) | yes |
| phase_hpe_ACT_h4_vs_REST_h0_trt-EX | interaction | EX/ACT/h4 (5), EX/REST/h4 (6), EX/ACT/h0 (6), EX/REST/h0 (4) | yes |
| phase_hpe_ACT_h8_vs_REST_h0_trt-EX | interaction | EX/ACT/h8 (5), EX/REST/h8 (6), EX/ACT/h0 (6), EX/REST/h0 (4) | yes |
| phase_hpe_ACT_h12_vs_REST_h0_trt-SED | interaction | SED/ACT/h12 (6), SED/REST/h12 (6), SED/ACT/h0 (6), SED/REST/h0 (5) | yes |
| phase_hpe_ACT_h16_vs_REST_h0_trt-SED | interaction | SED/ACT/h16 (5), SED/REST/h16 (6), SED/ACT/h0 (6), SED/REST/h0 (5) | yes |
| phase_hpe_ACT_h20_vs_REST_h0_trt-SED | interaction | SED/ACT/h20 (6), SED/REST/h20 (6), SED/ACT/h0 (6), SED/REST/h0 (5) | yes |
| phase_hpe_ACT_h4_vs_REST_h0_trt-SED | interaction | SED/ACT/h4 (6), SED/REST/h4 (6), SED/ACT/h0 (6), SED/REST/h0 (5) | yes |
| phase_hpe_ACT_h8_vs_REST_h0_trt-SED | interaction | SED/ACT/h8 (6), SED/REST/h8 (5), SED/ACT/h0 (6), SED/REST/h0 (5) | yes |
