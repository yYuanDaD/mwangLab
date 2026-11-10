# HANDBACK: PMID42812173 / GSE320360

Paper: Acute aerobic exercise and serum EV-enriched miRNA in MDD (PMC13619381). Single arm, repeated measures: 30 participants sampled pre, mid, post and 75 min after one 30-min cycling bout. Small RNA-seq, miRBase mature counts.

## What ran

- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`). Status completed, validator found 0 errors in 10 records.
- Ownership: DA.p1 names GSE320360. 115 samples = 30/29/28/28, matching S2.5.p2. The matrix median library size (560,077) matches S3.2.p4.
- Alignment: exact match on the `Library name` taken from `description` (115/115). `time` comes from suffix E1/E2/E3/E6 = pre/mid/post/post75, which matches the GEO treatment field one to one. `subject` is the participant number, recoded with an `s` prefix so it is a factor and not a numeric covariate.
- Matrix: raw integer counts (GEO data_processing says "raw miRNA read counts"). Method: DESeq2.
- Design: as in the paper (S2.7.p1), one joint model `~ subject + time` on all 115 samples. It is full rank with 82 residual df. Wald contrasts vs pre:
  - planned: mid, post and post75 vs pre;
  - exploratory, from the same model: post vs mid, post75 vs mid, post75 vs post.
- Low-count filter: at least 10 raw counts in at least 3 samples, which keeps 2,611 of 2,656 miRNAs (paper: 2,609).
- Threshold: the paper's own rule, BH padj <= 0.05 with no fold-change cutoff (S2.7.p1, S3.3.p2). Audit rule: padj <= 0.10, which the paper calls "trending".
- Enrichment: not run. The paper did miRNA target prediction (DIANA-microT) followed by PANTHER GO. The repository's ORA/GSEA work on gene symbols and cannot take miRNA IDs.

## DEG counts vs paper (padj <= 0.05, no FC rule)

| Contrast | Ours n (up/down) | Paper n (up/down) | Paper DEGs recovered at padj <= 0.05 |
|---|---|---|---|
| mid vs pre | 45 (7/38) | 15 (2/13) | 15/15 |
| post vs pre | 72 (3/69) | 33 (0/33) | 33/33 |
| post75 vs pre | 28 (18/10) | 4 (4/0) | 4/4 |

- baseMean and log2FC for the paper's Table 1 miRNAs match almost exactly. Two exceptions at mid vs pre:
  - miR-137-3p: ours -4.04, paper -3.19;
  - miR-329-5p: ours -3.15, paper -2.62.
  These are probably differences in Cook's outlier handling.
- Every paper DEG is significant in our run, and in the same direction. So our sets are supersets of the paper's.
- Our padj values are systematically smaller than the paper's. For example, miR-3618 at mid vs pre: ours 0.0015, paper 0.0055.
- Across the three contrasts there are 75 extra miRNAs.
  - Some of them are in the paper's trending list (FDR <= 0.10), for example miR-1267, miR-3182, miR-627-3p.
  - Others do not appear in the paper at all, including several of our top hits: miR-34a-3p, miR-3164, miR-12127, miR-548m, let-7g-5p.
  - The extras are not low-count artifacts (they pass the normalized-count filter) and are not driven by a single sample.
  - Likely causes: the paper excluded about 2% of genes that failed to converge in R (roughly 52 miRNAs, a list we cannot reproduce), plus differences in dispersion estimation between pydeseq2 and R DESeq2 1.44.
- Directional pattern:
  - mid and post vs pre are predominantly down-regulated, as in the paper.
  - At 75 min, ours is 18 up / 10 down; the paper's significant ones are all up.
  - miR-1252-3p is down at all three timepoints in our run, significant at 75 min (padj 0.043). The paper had it at 0.071 (trending) there. This matches the paper's "persistent down-regulation" claim.

## Deviations (declared in the method gate and the discrepancies)

1. Filter on raw counts instead of the paper's DESeq2-normalized counts (at least 10 in at least 3 samples). With our size factors the normalized rule would keep about 2,596 miRNAs. Only 36 miRNAs have no zero counts, so the size factors come from the same genes under either rule.
2. pydeseq2 instead of R DESeq2 1.44. The paper's step of excluding the roughly 2% of genes that did not converge is not replicated. This is the most likely cause of the inflated counts.
3. Sequencing pool/lane is not in GEO and was not modelled. The paper did not model it either.

## Caveats

- There is no resting control (S4.5.p4). The changes are temporal and not attributable to exercise alone.
- Sex is not in the GEO metadata, and a miRNA matrix has no X/Y marker genes, so no sex check was possible.

## Tool problems

- `tools/joint_contrasts.py:71-73` (`_numeric_covariates`) fits any all-numeric covariate as continuous. Numeric subject IDs, as here (352, 354, ...), would silently become one continuous slope instead of a blocking factor. I worked around it with a `subject` recode adding an `s` prefix. The runner or suitability check should force the declared `design.subject` to be a factor.
- `tools/case_runner.py:740-745`: `filter_low_counts` has no rule on DESeq2-normalized counts, which this paper (and DESeq2 vignette-style filters in general) use. Only raw count, CPM or mean raw count rules exist.
- `tools/suitability.py:355-375`: a column given both as `design.subject` and in `covariate_candidates` is added twice, as a block and as a candidate covariate. The report then says "subject: omit (makes the design rank deficient)" next to "subject: block". The message is confusing but harmless; the record is full rank.
- Minor: the sex-check message lists mouse-case markers (`tools/stats_tools.py:240`) for a human miRNA matrix. It is not applicable here.
