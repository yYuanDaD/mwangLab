# HANDBACK — PMID40581981 / GSE298607

**Status: refused at `design`.** There is no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE298607 --data-root E:/agent/mwangLab_pdf/data`: downloaded the series (metadata plus `GSE298607_raw_counts.txt.gz`, 56,941 Ensembl genes × 20 samples, 100% integer).
- `python -m tools.case_runner execute case_spec.json`: recorded `paper_reconstruction`, `ownership`, `alignment`, `matrix` and `design` (refused). The validator reported 0 errors, and `summary.csv` reads `stopped:design`.
  - Alignment: `description` field `Library name: Sample N,S10xx` → key `S10xx`, exact match 20/20. `grp` comes from the title suffix: CONTROL 10, SPACE 10.
  - Matrix: featureCounts raw counts. The paper's method is edgeR (S2.6.p3).
  - Suitability: SPACE vs CONTROL is `analyzable` as a design. It was not run because it does not answer the request.

## Why refused
The mouse experiment has two arms (S2.3.p1):
- **SPACE:** 14 days of hindlimb unloading, plus 1 Gy whole-body X-ray on day 7, plus oral corticosterone.
- **CONTROL:** pair-fed and sham-irradiated.

This is a disuse/atrophy model. No group receives exercise, training or loading. Exercise appears only as background in the Introduction (S1.p4). Treating SPACE vs CONTROL as an exercise effect, or as its inverse, would change the estimand. Radiation and stress hormone are also aliased with unloading.

## DEG counts vs paper
- None computed (refused).
- Paper (for the record): SPACE vs CONTROL gave 6191 protein-coding DEGs (2666 up / 3525 down) at FDR < 0.01 with no fold-change cutoff (S3.1.p1). It also reported 465 lncRNAs (340 up / 125 down) at "P < 0.01" (S3.2.p1); the FIG2 legend says −log10FDR > 2.

## Deviations
None. No analysis route was executed.

## Paper inconsistencies recorded
- The lncRNA threshold is given as P < 0.01 in the text and as FDR < 0.01 in the FIG2 legend.
- The DEG total is 6191 in S3.1.p1 and 6195 in S4.p2.

## Tool problems
- No blocking problems.
- Minor: the inspect output shows the GEO `contact_address` mis-decoded as `Nobels v盲g` (UTF-8 "ä" read as GBK) in the metadata CSV or summary. It is cosmetic and has no effect on the analysis. I did not locate the file:line.
