# Suitability: GSE142678_across_durations

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | TPM (RSEM, linear scale); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | group_raw: 2 levels |
| Covariance | pass | not_required; pair: omit (one sample per subject per factor level set: an identifier, not a block); time_raw: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); pair: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); time_raw: omit (makes the design rank deficient); pair: omit (makes the design rank deficient) |
| Sample size | pass | 2/2 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| group_raw_Run_vs_Sed_frac_raw-IN | simple | IN/Run (6), IN/Sed (6) | yes |
| group_raw_Run_vs_Sed_frac_raw-IP | simple | IP/Run (6), IP/Sed (6) | yes |
