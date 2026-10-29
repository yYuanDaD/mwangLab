# Suitability: GSE123865

Verdict: **not_analyzable** (failed: data_type, sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | fail | RPM; route: matrix type unknown or ambiguous |
| Grouping | pass |  |
| Covariance | pass | not_required; characteristics_ch1.1.donor gender: omit (one sample per subject per factor level set: an identifier, not a block); data_processing: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_selection: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_source: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_strategy: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | fail | 0/0 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: yes |
