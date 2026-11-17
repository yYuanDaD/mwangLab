# Suitability: GSE185154

Verdict: **not_analyzable** (failed: sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass |  |
| Covariance | pass | not_required; data_processing: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_selection: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_source: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_strategy: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | fail | 0/0 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |
