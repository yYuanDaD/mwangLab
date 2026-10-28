# Suitability: GSE214282

Verdict: **not_analyzable** (failed: sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | raw counts; route: DESeq2 / edgeR / limma-voom |
| Grouping | pass |  |
| Covariance | pass | not_required; data_processing: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_selection: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_source: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_strategy: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | fail | 0/0 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |
