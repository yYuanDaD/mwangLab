# Suitability: GSE216408

Verdict: **not_analyzable** (failed: sample_size)

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (RSEM expected counts); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass |  |
| Covariance | pass | not_required; data_processing: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_selection: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_source: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); library_strategy: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
| Sample size | fail | 0/0 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 7 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |
