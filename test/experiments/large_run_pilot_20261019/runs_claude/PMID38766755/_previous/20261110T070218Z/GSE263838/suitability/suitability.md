# Suitability: GSE263838

Verdict: **analyzable**

| Check | Status | Detail |
|---|---|---|
| Data type | pass | estimated counts (Kallisto gene-level counts, deposited as integers); route: DESeq2 / edgeR / limma-voom |
| Grouping | pass | cond: 2 levels; day: 2 levels |
| Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); subject: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); subject: omit (makes the design rank deficient) |
| Sample size | pass | 5/5 comparisons have >= 3 per group |
| Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| cond_SR_vs_NS_day-D3 | simple | D3/SR (10), D3/NS (9) | yes |
| cond_SR_vs_NS_day-D9 | simple | D9/SR (9), D9/NS (10) | yes |
| day_D9_vs_D3_cond-NS | simple | NS/D9 (10), NS/D3 (9) | yes |
| day_D9_vs_D3_cond-SR | simple | SR/D9 (9), SR/D3 (10) | yes |
| cond_day_SR_D9_vs_NS_D3 | interaction | SR/D9 (9), NS/D9 (10), SR/D3 (10), NS/D3 (9) | yes |
