# Suitability: GSE58608

Verdict: **not_analyzable** (failed: sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | FPKM; route: limma on log2(x+1); count models are not valid |
| Grouping | pass |  |
| Covariance | pass | not_required; subject: omit (one sample per subject per factor level set: an identifier, not a block); data_processing: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_selection: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_source: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_strategy: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | fail | 0/0 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: yes |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |
