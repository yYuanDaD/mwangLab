# HANDBACK: PMID42812173 / GSE320360

Paper: Acute aerobic exercise and serum EV-enriched miRNA in MDD (PMC13619381). Single arm, repeated measures: 30 participants sampled pre, mid, post and 75 min after one 30-min cycling bout. Small RNA-seq, miRBase mature counts.

Round 2 (after decision review): I added the paper's normalized-count filter and an R DESeq2 run. R DESeq2, the paper's software, is now the primary executor. pydeseq2 and edgeR QL are sensitivity runs.

## What ran

- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`). Status completed; the validator found no errors. Previous attempts are in `_previous/`.
- Ownership: DA.p1 names GSE320360. 115 samples = 30/29/28/28 (S2.5.p2). The matrix median library size (560,077) matches S3.2.p4.
- Alignment: exact match on the `Library name` in `description` (115/115).
  - `time` = suffix E1/E2/E3/E6 = pre/mid/post/post75, matching the GEO treatment field one to one.
  - `subject` = participant number with an `s` prefix, so it is a factor.
- Matrix: raw integer counts (GEO data_processing: "raw miRNA read counts").
- Low-count filter: the paper's rule (S2.7.p1), applied by `prep/paper_filter.py`.
  - DESeq2 median-of-ratios size factors are computed on the unfiltered matrix, and a miRNA is kept with at least 10 normalized counts in at least 3 samples.
  - 2,596 of 2,656 kept; the paper reports 2,609.
  - All 36 zero-free miRNAs are kept, so every executor's size factors equal those of the unfiltered matrix.
- Model: `~ subject + time` on all 115 samples, as in the paper's `~ ID + Treatment`. It is full rank with 82 residual df. Wald contrasts mid/post/post75 vs pre.
  - Primary: `tools.r_de_tools:run_r_de`, engine deseq2 (R DESeq2 1.51.7), default Cook's cutoff and independent filtering.
  - Sensitivity: pydeseq2 joint model (`tools.joint_contrasts:run_joint_deseq2`). It is also the only source of the exploratory between-timepoint comparisons.
  - Sensitivity: edgeR QL (TMM), same design.
- Threshold: the paper's rule, BH padj <= 0.05 with no fold-change cutoff (S2.7.p1, S3.3.p2). Audit rule: padj <= 0.10, the paper's "trending".
- Enrichment: not run. The paper used DIANA-microT target prediction followed by PANTHER GO. The repository's ORA/GSEA need gene symbols, not miRNA IDs.

## DEG counts vs paper (padj <= 0.05, no FC rule)

| Contrast | Paper | R DESeq2 (primary) | pydeseq2 | edgeR QL |
|---|---|---|---|---|
| mid vs pre | 15 (2 up/13 down) | 16 (2/14); 15/15 paper DEGs recovered | 45 (7/38); 15/15 | 9 (3/6); 5/15 |
| post vs pre | 33 (0/33) | 53 (1/52); 30/33 | 72 (3/69); 33/33 | 4 (1/3); 2/33 |
| post75 vs pre | 4 (4/0) | 15 (13/2); 4/4 | 28 (18/10); 4/4 | 0; 0/4 |

- In my first round, pydeseq2 produced 3-7x more DEGs than the paper. With the same matrix and model, R DESeq2 removes most of that gap:
  - mid vs pre is essentially reproduced (16 vs 15, all 15 recovered);
  - post vs pre is 53 vs 33;
  - post75 vs pre is 15 vs 4.
- So the inflation came mostly from the pydeseq2 port: its p-values are systematically smaller. For example, miR-3618 at mid vs pre has padj 0.0015 in pydeseq2 against 0.0055 in the paper. My guess is that dispersion estimation differs, but I did not establish it.
- The remaining excess at post and 75 min is not explained. Two candidates:
  - the paper removed the roughly 2% of genes that failed to converge (S2.7.p1); I could not replicate this because our R wrapper does not export `betaConv`;
  - DESeq2 1.44 vs 1.51.7.
- edgeR QL is much more conservative. QL F-tests on sparse miRNA counts are known to be stricter, so it is not a check of the paper's route.
- Directions: mid and post vs pre are predominantly down-regulated, as in the paper. At 75 min, R DESeq2 is mostly up (13/2). The 2 down-regulated calls include miR-1252-3p (also down at mid and post). The paper calls that miRNA persistent, but at 75 min it had FDR 0.071, below significance.

## Deviations (declared)

1. R DESeq2 1.51.7, not 1.44.0.
2. Genes that failed to converge were not excluded (not replicated).
3. Sequencing pool/lane is not in GEO and was not modelled. The paper did not model it either.

## Caveats

- There is no resting control (S4.5.p4). The changes are temporal and not attributable to exercise alone.
- Sex is not in the GEO metadata, and a miRNA matrix has no X/Y markers, so no sex check was possible.

## Tool problems

- `tools/joint_contrasts.py:71-73`: numeric subject IDs were fitted as a continuous covariate. I worked around it with a recode; the coordinator reports this is now fixed.
- pydeseq2 (`tools/joint_contrasts.py:run_joint_deseq2`) gives 2-4x more DEGs than R DESeq2 on the same matrix and model in this dataset. Its p-values are systematically smaller, and no padj are NA (no independent-filtering NA, unlike R's 1,107 NA at post vs pre). For paper reproduction with DESeq2, the R executor is more faithful.
- `tools/r_de.R:106-180`: the DESeq2 branch does not export `betaConv`, so a paper's "exclude non-converging genes" step cannot be reproduced.
- `tools/case_runner.py:740-745`: `filter_low_counts` has no DESeq2-normalized-count rule, so a prep script was needed.
- `tools/suitability.py:355-375`: a column given both as `design.subject` and as a covariate candidate is reported as both "block" and "omit (rank deficient)". The message is confusing but harmless.
