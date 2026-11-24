# Suitability: GSE208615

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass | grp: 6 levels |
| Covariance | pass | not_required; cohort: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | pass | 15/15 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 60 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| grp_EX14D14_vs_EX14 | simple | EX14D14 (10), EX14 (10) | yes |
| grp_EX14D7_vs_EX14 | simple | EX14D7 (10), EX14 (10) | yes |
| grp_EX14D7RE2_vs_EX14 | simple | EX14D7RE2 (10), EX14 (10) | yes |
| grp_RE2_vs_EX14 | simple | RE2 (10), EX14 (10) | yes |
| grp_EX14_vs_SED | simple | EX14 (10), SED (10) | yes |
| grp_EX14D7_vs_EX14D14 | simple | EX14D7 (10), EX14D14 (10) | yes |
| grp_EX14D7RE2_vs_EX14D14 | simple | EX14D7RE2 (10), EX14D14 (10) | yes |
| grp_RE2_vs_EX14D14 | simple | RE2 (10), EX14D14 (10) | yes |
| grp_EX14D14_vs_SED | simple | EX14D14 (10), SED (10) | yes |
| grp_EX14D7RE2_vs_EX14D7 | simple | EX14D7RE2 (10), EX14D7 (10) | yes |
| grp_RE2_vs_EX14D7 | simple | RE2 (10), EX14D7 (10) | yes |
| grp_EX14D7_vs_SED | simple | EX14D7 (10), SED (10) | yes |
| grp_RE2_vs_EX14D7RE2 | simple | RE2 (10), EX14D7RE2 (10) | yes |
| grp_EX14D7RE2_vs_SED | simple | EX14D7RE2 (10), SED (10) | yes |
| grp_RE2_vs_SED | simple | RE2 (10), SED (10) | yes |
