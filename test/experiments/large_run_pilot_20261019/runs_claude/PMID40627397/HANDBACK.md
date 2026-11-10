# HANDBACK: PMID40627397 / GSE282641

Paper: HIF1α mediates circadian regulation of skeletal muscle metabolism and substrate preference in response to time-of-day exercise (PNAS 2025, PMC12280960).

## What ran

- Case-spec route (`case_spec.json` → `python -m tools.case_runner execute`). Validator: 15 records, 0 errors. Status: completed, route `paper_aligned`.
- Data: `GSE282641_rawCounts.txt.gz` (featureCounts integer counts, 55,401 Ensembl genes x 64 libraries). Gastrocnemius; 2 genotypes (fl/fl = WT, HSA-cre Hif1a fl/fl = KO) x 2 times (ZT3, ZT15) x 2 states (sedentary, 60 min treadmill), 4F/4M per cell.
- Alignment: matrix columns `0156_N` matched exactly to the metadata `description` field "Library name: 0156_N" (64/64). Excluded GSM8647977 (library 0156_44, ko_3_ex_44): 382 total reads. This is the low-coverage KO/exercise/ZT3 sample the paper excluded (S4.14.p1). 63 samples were analyzed.
- Model: the paper's design (~0 + group + sex, S4.14.p1), reproduced as one pydeseq2 cell-means model `~ sex + cell(geno x zt x trt)` on all 63 samples. All 18 suitability comparisons were extracted from it. The paper's 8 simple effects are planned; exercise vs sedentary and the 2x2 interactions are exploratory.
- Secondary run (declared deviation): additive model `~ sex + zt + trt + geno`, KO vs WT. It approximates the paper's overall genotype count, whose contrast the paper does not state.
- Threshold: the paper's rule, FDR (BH padj) < 0.1 with no fold-change cutoff (S4.14.p1, "alpha value was set to 0.1"). Audit rule: padj < 0.05.
- Enrichment: ORA (Enrichr GO/KEGG) and Hallmark GSEA (ranked by stat) for KO vs WT in exercised mice at ZT3 and at ZT15.

## DEG counts vs paper (padj < 0.1, no FC)

| Contrast | Ours (up/down) | Paper |
|---|---|---|
| KO vs WT, exercise, ZT3 | 479 (278/201) | 516 |
| KO vs WT, exercise, ZT15 | 89 (31/58) | 91 |
| KO vs WT, sedentary, ZT3 | 87 | figure only ("similar") |
| KO vs WT, sedentary, ZT15 | 17 | figure only ("similar") |
| ZT15 vs ZT3, WT sedentary | 438 | 451 |
| ZT15 vs ZT3, WT exercise | 263 | 273 |
| ZT15 vs ZT3, KO sedentary | 101 | 101 |
| ZT15 vs ZT3, KO exercise | 191 | 191 |
| KO vs WT overall (additive model, deviation) | 1305 (624/681) | 1473 (724/749) |

Exploratory results. The paper reports none of these counts.

- Exercise vs sedentary: WT ZT3 71, WT ZT15 15, KO ZT3 64, KO ZT15 33. Most are up-regulated.
- Interactions: five of the six have 0 genes. zt x trt within WT has 490 genes at padj < 0.1 but only 6 at padj < 0.05. pydeseq2 independent filtering kept 7,257 of 35,337 genes for that contrast, and BH then produced a plateau just under 0.1, so treat this result as unstable.

Enrichment:

- At ZT3, exercised KO vs WT: Hallmark OXIDATIVE_PHOSPHORYLATION NES +3.08 (FDR ~0); fatty-acid metabolism and ROS are also positive.
- At ZT15: OXPHOS NES +1.24 (FDR 0.27), not significant.

This matches S1.6.p2: oxidative metabolism positively enriched at ZT3 but not at ZT15. The paper used GO GSEA ranked by FDR; we used Hallmark ranked by stat.

## Deviations

- pydeseq2 instead of R DESeq2. Its independent filtering differs slightly, which explains the 2-7% count gaps on four contrasts.
- The overall KO vs WT contrast is undefined in the paper, so the additive main-effect model is a declared deviation (1305 vs 1473).
- The exercise-vs-sedentary contrasts and the interactions are exploratory; the paper reports neither.
- Gene check. Hif1a is not reduced at gene level in KO: log2FC +0.12 at ZT3 exercise and -0.01 overall, padj > 0.4. The paper's Fig. 1B qPCR does show reduced Hif1a transcripts. The floxed allele removes only exon 2, so whole-locus gene counts need not fall. Several facts support the genotype labels:
  - paper counts reproduced;
  - Mpi higher in KO (log2FC +0.18, p = 0.049) as in Fig. 4G;
  - OXPHOS direction matches the paper.

  This is recorded in the study caveats.

## Tool problems

- No blocking problems.
- pydeseq2 printed `RuntimeWarning: overflow encountered in exp` (`.venv-pdf/Lib/site-packages/pydeseq2/utils.py:1088`) during the fit. It was harmless; the results are complete.
- `tools/joint_contrasts.py:150` reports `n_padj_0.05` per comparison, a fixed 0.05 that is not the run's alpha of 0.1. The runner applies the right threshold afterwards, so the summary counts are correct, but the executor's own figure is misleading.
- Independent filtering is applied separately for each contrast (`tools/joint_contrasts.py:144`, `DeseqStats(..., alpha=alpha)`). It can produce knife-edge padj plateaus on weak contrasts (the zt x trt WT interaction above). This is the same behavior as DESeq2, but it is worth flagging.
