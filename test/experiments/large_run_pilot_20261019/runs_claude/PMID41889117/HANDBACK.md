# HANDBACK — PMID41889117 / GSE324693

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE324693 --data-root E:/agent/mwangLab_pdf/data`: the data were already cached. It found one matrix, `GSE324693_counts_matrix.csv.gz` (56,941 Ensembl genes × 12 samples, all integers, raw featureCounts output). The only grouping column is `characteristics_ch1.2.treatment` (Vehicle 6 / EtOH 6). Tissue: subcutaneous WAT.
- I wrote `case_spec.json` with the gates paper_reconstruction → ownership → alignment → matrix → design, where design is refused. `python -m tools.case_runner execute` completed, and the validator wrote 5 records with 0 errors.
- Alignment: an exact match on the `S<n>` key, taken from the GEO title (`S1 ctrl`) and from the matrix column (`S1.bam`). All 12 of 12 samples aligned. Suitability: analyzable for EtOH vs control, which is not an exercise comparison.

## Why it was refused
The paper is a chronic-ethanol study: 20% EtOH in drinking water vs water for 60 weeks in female C57BL/6 mice (S2.2.p1). Exercise appears only as a treadmill time-to-fatigue *performance test*, and every mouse in both groups took it (S2.4.2.p1, FIG2 week 55). The paper has no exercise intervention or unexercised comparison group, and neither does GEO. Reporting EtOH vs control as an exercise effect would change the estimand.

## DEG counts vs the paper
- The paper's contrast is EtOH vs control in WAT, using DESeq2 with genes kept if they map in ≥6 samples, at a threshold of FDR ≤ 0.1 with no fold-change cutoff (S2.4.16.p1). It reports 61 DEGs: 47 down and 14 up, with Cyp2e1 among them (S3.4.p3).
- Ours: none were computed, because the case was refused before any execution. The data could support the paper's EtOH contrast (6 vs 6 raw counts), but that contrast is not about exercise.

## Deviations
- None. No analysis ran.
- Discrepancy noted: the paper had 7 control and 10 EtOH mice, and FIG7 gives RNA-seq n as 5–6 / 6–9. GEO holds 6 / 6.

## Tool problems
- None blocking.
- Minor: inspect reported `alignment_keys: []` because the matrix columns carry a `.bam` suffix (`S1.bam`) and the titles carry a group suffix (`S1 ctrl`). I needed both `key_patterns` and `matrix_column_pattern` to align them. Inspect could suggest stripping a `.bam` suffix.
