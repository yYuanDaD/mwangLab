# HANDBACK: PMID 36620222 (PMC9811128)

**Run label:** PMID36620222  
**Decision maker:** Claude Code session (claude-opus-5-5) using the bioinformatics-workflow skill, case-spec route.  
**Spec:** `case_spec.json`. **Runner output:** `_execute_out.json`, `case_runner.log`, `summary.csv`. The decision contract validator passed: 20 records, 0 errors. The first attempt is kept in `_previous/`.

## What ran

| Case | Outcome | Why |
|---|---|---|
| GSE218103: plasma-EV small RNA-seq, human, 12 pooled samples | **completed**, paper_aligned | This is the only accession that contains an exercise contrast. |
| GSE219099: C2C12 cells, miR-486 mimic vs scramble, mouse, 6 samples | **refused at design** | No exercise factor. It is an in-vitro test of what one miRNA does. |
| GSE219100: SuperSeries of the two above, 18 samples | **refused at design** | Its samples are the union of GSE218103 (human miRNA) and GSE219099 (mouse mRNA). No single design spans the two species and assays, and its exercise contrast is the same as GSE218103's. |

### GSE218103: decisions
- **Sample groups.** In GEO, "CON" (treatment: control) means the **pre-exercise sample**, not the paper's separate TD CON no-exercise group. Evidence: only TD EX and CP EX were sequenced, as 3 pools per timepoint (S2.6.p1); the study has no "CP CON" group (S2.1.p1); and treatment_protocol reads "before and 30 minutes after a bout". So CON is pre and EX is post.
- **Model.** One DESeq2 model (pydeseq2) over the 4 genotype x time cells, 3 pools per cell. This matches the paper's genotype + activity model (S2.9.p2).
  - Planned: post vs pre within TD; post vs pre within CP.
  - Associational: CP vs TD at pre; CP vs TD at post.
  - Exploratory: the genotype x time interaction.
- **Low-count filter.** "MicroRNAs with less than 10 counts were removed" was read as a row total of at least 10 across the 12 samples. It was encoded as `min_mean_count` 0.8333 and keeps 298 of 399 miRNAs.
- **Covariance.** No pool blocking. The pre and post pools come from the same participants, but GEO does not say which pre pool matches which post pool. The pre/post correlations do not peak on matching indices, and the paper's model has no pool term. Ignoring this positive pairing makes the exercise tests conservative. It is recorded as a caveat and was not guessed.
- **Threshold.** The paper's own rule (S2.9.p2): BH-adjusted p < 0.05, no fold-change cutoff. Raw p < 0.05 is reported only as a labelled audit count.
- **Enrichment.** Not run. The IDs are miRNAs, not genes, and the paper's enrichment was on predicted miR-486 targets and the C2C12 data, not on an exercise result.

## DEG counts vs the paper (paper threshold: FDR (BH) < 0.05, no FC cutoff)

| Contrast | Ours (up/down) | Paper | Audit, raw p < 0.05 |
|---|---|---|---|
| TD post vs pre (**exercise**) | 0 | 0 ("exercise did not affect EV cargo", S3.3.p1, S4.p7) | 10 |
| CP post vs pre (**exercise**) | 0 | 0 | 9 |
| CP vs TD, pre | 4 (1/3): miR-486-5p up; let-7a-5p, let-7b-5p, let-7e-5p down | 4 named, the same miRNAs in the same directions (ABS.p1, FIG2A/B) | 20 |
| CP vs TD, post | 1 (1/0): miR-486-5p up (log2FC 2.0) | 4 named: miR-486, miR-100 up; miR-877, miR-4433 down | 13 |
| geno x time interaction (exploratory) | 0 | not reported | 4 |

In the post-exercise CP vs TD comparison, miR-100-5p (+2.13), miR-877-5p (-4.03) and miR-4433b-5p (-2.25) go in the paper's direction, but their padj values are 0.056, 0.056 and 0.067, just above 0.05. The paper's counts for the CP vs TD comparisons are the miRNAs it names in the text; its full lists are in Supplementary Table S1, which was not available.

## Deviations
- pydeseq2 was used instead of Bioconductor DESeq2 (R 3.6.2).
- The low-count rule was read as a row-total rule; the paper's wording is ambiguous.
- Pre and post pools were treated as independent because their pairing is undocumented. This is the same as the paper's model and is conservative for the exercise contrasts.
- The paper says both datasets are in GSE219100 (S2.6.p1, S2.8.p1). That is the SuperSeries; the data were analysed through its sub-series GSE218103 and GSE219099.

## Tool problems
1. **The interaction comparison's name reads like a simple contrast** (`tools/suitability.py:234`). Name sanitisation turns `geno:time_CP:post_vs_TD:pre` into `geno_time_CP_post_vs_TD_pre`. That reads as "CP-post vs TD-pre", but it is the 2x2 difference-in-differences. Only the suitability report's `kind` column shows what it is.
2. **Refused designs still get a sample-size failure** (`tools/case_runner.py:628`). Suitability runs for a design gate that is refused with no `factors`. It then reports `not_analyzable` with `sample_size` failed and 0 comparisons for GSE219099 and GSE219100. That is misleading: GSE219099 has 3 vs 3.
3. **Minor: wrong ID type on the mixed matrix.** `inspect` labels the GSE219100 merged-tar matrix, which mixes human miRNA IDs and mouse Ensembl IDs, as `feature_id_type: ensembl_gene` (`tools/case_runner.py:405`). It does not flag that the matrix is mixed.
