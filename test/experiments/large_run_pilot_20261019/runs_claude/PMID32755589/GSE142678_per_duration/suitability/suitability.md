# Suitability: GSE142678_per_duration

Verdict: **not_analyzable** (failed: sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | TPM (RSEM, linear scale); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | group_raw: 2 levels; time_raw: 3 levels |
| Covariance | pass | not_required; pair: omit (one sample per subject per factor level set: an identifier, not a block); pair: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); pair: omit (makes the design rank deficient) |
| Sample size | fail | 0/22 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| group_raw_Run_vs_Sed_frac_raw-IN_time_raw-D11 | simple | IN/D11/Run (2), IN/D11/Sed (2) | no |
| group_raw_Run_vs_Sed_frac_raw-IN_time_raw-D18 | simple | IN/D18/Run (2), IN/D18/Sed (2) | no |
| group_raw_Run_vs_Sed_frac_raw-IN_time_raw-D27 | simple | IN/D27/Run (2), IN/D27/Sed (2) | no |
| time_raw_D18_vs_D11_frac_raw-IN_group_raw-Run | simple | IN/Run/D18 (2), IN/Run/D11 (2) | no |
| time_raw_D27_vs_D11_frac_raw-IN_group_raw-Run | simple | IN/Run/D27 (2), IN/Run/D11 (2) | no |
| time_raw_D27_vs_D18_frac_raw-IN_group_raw-Run | simple | IN/Run/D27 (2), IN/Run/D18 (2) | no |
| time_raw_D18_vs_D11_frac_raw-IN_group_raw-Sed | simple | IN/Sed/D18 (2), IN/Sed/D11 (2) | no |
| time_raw_D27_vs_D11_frac_raw-IN_group_raw-Sed | simple | IN/Sed/D27 (2), IN/Sed/D11 (2) | no |
| time_raw_D27_vs_D18_frac_raw-IN_group_raw-Sed | simple | IN/Sed/D27 (2), IN/Sed/D18 (2) | no |
| group_raw_time_raw_Run_D18_vs_Sed_D11_frac_raw-IN | interaction | IN/Run/D18 (2), IN/Sed/D18 (2), IN/Run/D11 (2), IN/Sed/D11 (2) | no |
| group_raw_time_raw_Run_D27_vs_Sed_D11_frac_raw-IN | interaction | IN/Run/D27 (2), IN/Sed/D27 (2), IN/Run/D11 (2), IN/Sed/D11 (2) | no |
| group_raw_Run_vs_Sed_frac_raw-IP_time_raw-D11 | simple | IP/D11/Run (2), IP/D11/Sed (2) | no |
| group_raw_Run_vs_Sed_frac_raw-IP_time_raw-D18 | simple | IP/D18/Run (2), IP/D18/Sed (2) | no |
| group_raw_Run_vs_Sed_frac_raw-IP_time_raw-D27 | simple | IP/D27/Run (2), IP/D27/Sed (2) | no |
| time_raw_D18_vs_D11_frac_raw-IP_group_raw-Run | simple | IP/Run/D18 (2), IP/Run/D11 (2) | no |
| time_raw_D27_vs_D11_frac_raw-IP_group_raw-Run | simple | IP/Run/D27 (2), IP/Run/D11 (2) | no |
| time_raw_D27_vs_D18_frac_raw-IP_group_raw-Run | simple | IP/Run/D27 (2), IP/Run/D18 (2) | no |
| time_raw_D18_vs_D11_frac_raw-IP_group_raw-Sed | simple | IP/Sed/D18 (2), IP/Sed/D11 (2) | no |
| time_raw_D27_vs_D11_frac_raw-IP_group_raw-Sed | simple | IP/Sed/D27 (2), IP/Sed/D11 (2) | no |
| time_raw_D27_vs_D18_frac_raw-IP_group_raw-Sed | simple | IP/Sed/D27 (2), IP/Sed/D18 (2) | no |
| group_raw_time_raw_Run_D18_vs_Sed_D11_frac_raw-IP | interaction | IP/Run/D18 (2), IP/Sed/D18 (2), IP/Run/D11 (2), IP/Sed/D11 (2) | no |
| group_raw_time_raw_Run_D27_vs_Sed_D11_frac_raw-IP | interaction | IP/Run/D27 (2), IP/Sed/D27 (2), IP/Run/D11 (2), IP/Sed/D11 (2) | no |
