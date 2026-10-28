# Suitability: GSE344550

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | RPKM (linear normalized); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | bgrp: 3 levels; time: 3 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | partial | 7/22 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| bgrp_BP_vs_CTRL_time-T0 | simple | T0/BP (0), T0/CTRL (3) | no |
| bgrp_LBP_vs_BP_time-T0 | simple | T0/LBP (0), T0/BP (0) | no |
| bgrp_LBP_vs_CTRL_time-T0 | simple | T0/LBP (0), T0/CTRL (3) | no |
| bgrp_BP_vs_CTRL_time-h24 | simple | h24/BP (6), h24/CTRL (3) | yes |
| bgrp_LBP_vs_BP_time-h24 | simple | h24/LBP (6), h24/BP (6) | yes |
| bgrp_LBP_vs_CTRL_time-h24 | simple | h24/LBP (6), h24/CTRL (3) | yes |
| bgrp_BP_vs_CTRL_time-h3 | simple | h3/BP (4), h3/CTRL (2) | no |
| bgrp_LBP_vs_BP_time-h3 | simple | h3/LBP (6), h3/BP (4) | yes |
| bgrp_LBP_vs_CTRL_time-h3 | simple | h3/LBP (6), h3/CTRL (2) | no |
| time_h3_vs_T0_bgrp-BP | simple | BP/h3 (4), BP/T0 (0) | no |
| time_h24_vs_T0_bgrp-BP | simple | BP/h24 (6), BP/T0 (0) | no |
| time_h24_vs_h3_bgrp-BP | simple | BP/h24 (6), BP/h3 (4) | yes |
| time_h3_vs_T0_bgrp-CTRL | simple | CTRL/h3 (2), CTRL/T0 (3) | no |
| time_h24_vs_T0_bgrp-CTRL | simple | CTRL/h24 (3), CTRL/T0 (3) | yes |
| time_h24_vs_h3_bgrp-CTRL | simple | CTRL/h24 (3), CTRL/h3 (2) | no |
| time_h3_vs_T0_bgrp-LBP | simple | LBP/h3 (6), LBP/T0 (0) | no |
| time_h24_vs_T0_bgrp-LBP | simple | LBP/h24 (6), LBP/T0 (0) | no |
| time_h24_vs_h3_bgrp-LBP | simple | LBP/h24 (6), LBP/h3 (6) | yes |
| bgrp_time_BP_h24_vs_CTRL_T0 | interaction | BP/h24 (6), CTRL/h24 (3), BP/T0 (0), CTRL/T0 (3) | no |
| bgrp_time_BP_h3_vs_CTRL_T0 | interaction | BP/h3 (4), CTRL/h3 (2), BP/T0 (0), CTRL/T0 (3) | no |
| bgrp_time_LBP_h24_vs_CTRL_T0 | interaction | LBP/h24 (6), CTRL/h24 (3), LBP/T0 (0), CTRL/T0 (3) | no |
| bgrp_time_LBP_h3_vs_CTRL_T0 | interaction | LBP/h3 (6), CTRL/h3 (2), LBP/T0 (0), CTRL/T0 (3) | no |
