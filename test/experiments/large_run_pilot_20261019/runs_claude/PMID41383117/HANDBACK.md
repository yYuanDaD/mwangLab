# HANDBACK: PMID41383117 / GSE304351

**Status: refused at `design`** (no exercise contrast). The decision contract validator passed: 5 records, 0 errors.

## What ran
- `case_runner inspect GSE304351` downloaded the series to `E:/agent/mwangLab_pdf/data/GSE304351`. It holds 8 quadriceps samples (D-gal+PBS 1-4, D-gal+MSCs 1-4) and one integer count matrix of 12171 genes x 8 samples (`*_PBS1..._vs_MSC1....all.csv`).
- `prep_strip_count_suffix.py` removes the `_Count` suffix from the matrix columns so they equal the GEO Library names. Values are unchanged. Output: `GSE304351_counts_renamed.csv`.
- `case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership, alignment (exact on Library name, 8/8 matched), matrix (raw counts; data_processing says "raw counts"), and design, which was **refused**. Suitability had found the MSC-vs-PBS contrast analyzable, but that contrast is not an exercise contrast.

## Why refused
- The paper studies D-galactose-induced muscle atrophy treated with intramuscular MSCs or NAD+-MSCs (S2.3.p1).
- Exercise appears only as an exhaustive treadmill endurance test (S2.4.p1). Every mouse took it as an outcome readout, so exercise is not a factor.
- The only RNA-seq contrast deposited is D-gal+MSCs vs D-gal+PBS in quadriceps (S3.2.p1). It estimates a cell-therapy effect.
- No exercise-vs-sedentary estimand can be identified from these samples.

## DEG counts vs paper
- No differential expression was run (refused).
- Paper: MSC vs PBS in quadriceps, 960 DEGs (525 up / 435 down) with DESeq2 v1.26.0. The paper does not state the DEG threshold (S2.7.p1). The p < 0.05 in S2.16.p1 refers to the GraphPad tests.
- The paper's second RNA-seq set (cultured MSCs with or without NAD+, FIG5A, n = 3) is not deposited in GSE304351.

## Deviations
- None in the analysis, because nothing was executed.
- The only preparation step was renaming the matrix columns (suffix strip, documented in `prep_scripts`).

## Tool problems
- `tools/case_runner.py:294` (`_contained_keys`): inspect reported `alignment_keys: []`. The matrix column names (`PBS1_Count`) are longer than the metadata token (`Library name: PBS1`), so the containment check in this direction never matches. A suffix-strip prep script was needed. Suggestion: also test the reverse containment, or strip a common suffix such as `_Count` or `_count`.
- Environment issue, not a repository tool: in this session's Bash tool, heredoc text containing `\\` reached the file as `\`, which produced invalid JSON escapes in the regexes. Worked around with backslash-free regexes (`[A-Za-z0-9]+`, `[+]`).
