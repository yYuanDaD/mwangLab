# HANDBACK — PMID41225641 / GSE281210

**Status: refused at the `design` gate.** The data contain no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE281210` (data were already cached). Found one matrix, `GSE281210_Gene_count_for_all_bone_marrow_cell_samples.txt.gz`: 54,532 Ensembl genes × 6 samples, 100% integer values, counted with featureCounts. The series has 6 GSMs: `BM control 1-3` and `BM OP-HU1-3`.
- Paper read: `PMC12607142.paper.md`. The study uses 28-day hindlimb unloading (HU) to model disuse osteoporosis in male C57BL/6 mice (S2.1.p1, S3.1.p1). The bulk RNA-seq is whole bone marrow, OP-HU vs Con, n=3 per group (FIG3A), analyzed with DESeq2 1.20.0 (S2.6.p1). GSE281970 (scRNA-seq) is the other deposited series; it was not analyzed. The JQ-1 arm is not in the bulk data.
- `python -m tools.case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership (owned), alignment (6/6 samples, exact match after building keys from the titles and matrix columns and matching them ignoring case), matrix (raw counts → DESeq2), and design (refused). The contract validator returned 0 errors. Suitability rated OP-HU vs Con as analyzable, but that contrast measures disuse, not exercise.

## Why refused
The only intervention is mechanical unloading. There is no exercise, training or reloading arm. The control mice had ordinary cage activity, so reversing the sign of HU vs Con would not estimate an exercise effect. Nothing was executed, and enrichment was not run.

## DEG counts vs paper
- Ours: none (refused).
- Paper: no bulk DEG count is reported, and no DEG threshold is stated for the RNA-seq (S2.6.p1). The p<0.05 in S2.9.2.p1 applies to Prism t-tests. The paper reports only a heatmap, GO terms for down-regulated genes (leukocyte differentiation), Pf4 down, Tgfb1 slightly down, Ccl3 down and Ccl5 up.

## Deviations
None. No analysis was run.

## Tool problems
- None blocking.
- One difficulty: the metadata titles (`BM control 1`) and the matrix columns (`Con1`) use different words, so I had to combine `key_patterns`, `matrix_column_pattern` and `normalize_keys` (`tools/case_runner.py:550-585`). Inspect's `alignment_keys` reported only 3 of 6 matched via `title (contains the name)`, and it gave no hint for the control half.
- GEO metadata spells the treatment "hindlib unloading". That is a submitter typo and was handled.
