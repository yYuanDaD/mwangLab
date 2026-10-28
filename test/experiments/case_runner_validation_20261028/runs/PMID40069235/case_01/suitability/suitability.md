# Suitability: case_01

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | RPKM (linear, filtered/floored by submitter); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | tgrp: 5 levels |
| Covariance | pass | not_required; subject: omit (one sample per subject per factor level set: an identifier, not a block); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | pass | 10/10 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 60 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| tgrp_HC_H0_vs_BL | simple | HC_H0 (10), BL (20) | yes |
| tgrp_HC_H2_vs_BL | simple | HC_H2 (10), BL (20) | yes |
| tgrp_LC_H0_vs_BL | simple | LC_H0 (10), BL (20) | yes |
| tgrp_LC_H2_vs_BL | simple | LC_H2 (10), BL (20) | yes |
| tgrp_HC_H2_vs_HC_H0 | simple | HC_H2 (10), HC_H0 (10) | yes |
| tgrp_LC_H0_vs_HC_H0 | simple | LC_H0 (10), HC_H0 (10) | yes |
| tgrp_LC_H2_vs_HC_H0 | simple | LC_H2 (10), HC_H0 (10) | yes |
| tgrp_LC_H0_vs_HC_H2 | simple | LC_H0 (10), HC_H2 (10) | yes |
| tgrp_LC_H2_vs_HC_H2 | simple | LC_H2 (10), HC_H2 (10) | yes |
| tgrp_LC_H2_vs_LC_H0 | simple | LC_H2 (10), LC_H0 (10) | yes |
