# HANDBACK: PMID34219410 / GSE159217

**Status: refused at the `design` gate.** The contract validator passed (5 records, 0 errors).

## What ran
- `case_runner inspect GSE159217`: the `_RAW.tar` was merged into a 60,676 Ensembl genes × 38 samples matrix. Every value is an integer (STAR + HTSeq raw counts). The only grouping column is `age group` (Young 20 / Older 18). The matrix has 38 samples, all male vastus lateralis.
- `case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership (owned), alignment (exact on the metadata index, 38/38), matrix (raw counts → DESeq2), design (**refused**). No DE executions and no enrichment were run.

## Why refused
- The paper compares older and young men and **matched the two groups for physical activity** (S1.p3, S2.2.p1, S4.p1). There is no exercise intervention, acute bout or active-vs-sedentary arm. Older vs Young is an ageing estimand, not an exercise effect.
- The paper's only physical-activity analysis correlates expression with continuous MVPA time within each age group (limma-voom, raw P < 0.05; S2.5.p2, S3.4.p4). It needs per-subject accelerometry MVPA, which is not in the GEO metadata (only title, sex, tissue and age group) or in the paper.
- The Older vs Young DESeq2 comparison could run (suitability: analyzable), but I rejected it as an answer to the exercise question. It is listed as a rejected candidate in the design gate.

## DEG counts vs paper
- Paper threshold: BH FDR < 0.05, no fold-change cutoff, genes with < 10 reads per row removed (S2.5.p2).
- Paper results:
  - Older vs Young: 4327 DEGs, of which 3797 are coding (1891 up / 1906 down in older).
  - MVPA association: 662 genes (older group) and 1058 genes (young group) at unadjusted P < 0.05.
- Ours: not run (refused), so there is no comparison.

## Deviations
None. The case stopped before the method gate.

## Tool problems
- **Merged-tar column naming is inconsistent between commands.** `inspect` reports the merged-tar sample columns as `GSM4823186_1_counts`, and the runner's `raw_tar` path silently renames them to bare GSM ids (`tools/case_runner.py:715`). A `matrix_column_pattern` written from inspect's output therefore matches 0 columns and the case fails (`tools/case_runner.py:561-562`). The case spec docs do not mention the rename. It cost one rerun.
- There is no other problem.
