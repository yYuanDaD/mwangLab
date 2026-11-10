# Suitability: GSE304653

Verdict: **partially_analyzable**; check: sample_size

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | cgrp: 4 levels |
| Covariance | pass | not_required; data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information) |
| Sample size | partial | 6/6 comparisons have >= 3 per group; planned names not found: cgrp_TMEEX_vs_TMESED |
| Sex | pass | Sex inference completed on 23 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| cgrp_CCEX_vs_CCSED | simple | CCEX (7), CCSED (8) | yes |
| cgrp_TMEEX_vs_CCEX | simple | TMEEX (4), CCEX (7) | yes |
| cgrp_TMESED_vs_CCEX | simple | TMESED (4), CCEX (7) | yes |
| cgrp_TMEEX_vs_CCSED | simple | TMEEX (4), CCSED (8) | yes |
| cgrp_TMESED_vs_CCSED | simple | TMESED (4), CCSED (8) | yes |
| cgrp_TMESED_vs_TMEEX | simple | TMESED (4), TMEEX (4) | yes |
