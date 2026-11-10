# HANDBACK: PMID39609254 / GSE281849

## What ran
- Case spec route (`case_spec.json`, `python -m tools.case_runner execute`). Status: completed. Contract validator: 16 records, 0 errors.
- Matrix: `GSE281849_Gastroc_RawCounts.csv.gz`, raw featureCounts counts (21 female gastrocnemius samples, 40,853 genes). The NormalizedCounts file was rejected.
- Alignment: exact on the metadata `description` field (M304 to M325), 21/21 matched. grp = SED (Inactive), ACT (Active, treadmill 6 wk), AR (Activity Reduction, 4 wk treadmill then 2 wk inactive), 7 per group. Suitability: analyzable. Sex check: all one sex, consistent with the paper's female-only RNA-seq.
- Method: DESeq2 (pydeseq2 Wald), `~ grp`, one fit per pairwise comparison on that pair's 14 samples. This copies the authors' own Figure 3.Rmd, which is linked from DA.p1 and was read through a web fetch: column subsets, `design = ~group`, no lfcShrink. Primary contrast: ACT vs SED (the exercise effect). Secondary contrasts: AR vs SED and AR vs ACT.
- Sensitivity check: one joint 3-group DESeq2 model on all 21 samples (`joint/*`).
- Enrichment: preranked Hallmark GSEA on the stat ranking for all three pairwise tables, all completed.

## DEG counts vs paper
Paper rule (S2.11.p1): FDR < 0.05 and |log2FC| > 0.25. Audit rule (the authors' code): padj <= 0.05 and |log2FC| >= 0.27. The FIG3 legend's ">= 20%" (log2 0.263) falls between these two.

| Contrast | Paper (S3.7.p1) | Ours, paper rule | Ours, audit rule (code) | Joint model, paper rule |
|---|---|---|---|---|
| Active vs Inactive (primary) | 71 | 76 (54 up / 22 down) | 71 | 61 |
| Activity Reduction vs Inactive | 40 | 45 (27 / 18) | 41 | 15 |
| Activity Reduction vs Active | 124 | 134 (29 / 105) | 126 | 115 |

Under the authors' code threshold the counts match the paper almost exactly: 71/41/126 against 71/40/124.

Named genes from S3.7.p1 were all significant, in the paper's direction:
- Igfbp5 is down in both ACT and AR vs SED.
- Smyd2, En1 and Hoxa11os are up in AR vs both controls.
- Ostn, Ak4, Srrm4os and Zfhx4 are down in AR vs both controls.
- The Active-unique genes Acly, Elovl6, F13a1, Folr2, Gfpt2, Il1r1, Lama4 and Nrp2 are up, and Ctxn3, Dglucy and Gstp2 are down, in ACT vs SED. Acly and Elovl6 are down in AR vs ACT.

The joint 3-group model gives fewer AR vs SED DEGs (15). It pools dispersion across all three groups, which is why the paper's pairwise-subset route was kept as primary.

## Deviations
- pydeseq2 was used instead of R DESeq2. The authors' rowSums > 0 prefilter is not applied explicitly. It does not affect results for genes that are kept, but small count differences remain (76 vs 71 under the text rule).
- The paper states the threshold three slightly different ways (text 0.25, legend 20%, code 0.27). The text rule was applied and the code rule was recorded as the audit rule.
- GSEA differs from the paper. The paper ran fgsea on GO BP (FDR < 0.25); this run used Hallmark.
  - The paper reports no enrichment for AR vs Inactive. Hallmark gives 21 sets at FDR < 0.25 for that contrast (top: myogenesis, TGF-beta, Notch).
  - ACT vs SED: 46 sets (coagulation, EMT, interferon alpha). This is consistent with the immune, vasculature and wound-repair themes in S3.7.p2.
  - AR vs ACT: 44 sets. The top sets are positive (MYC targets, OXPHOS), whereas the paper describes the ACT-up pathways as negatively enriched in AR vs ACT.
  - These pathway results are not directly comparable with the paper's because the gene sets differ.
- Females only, so no exercise effect in males can be assessed from this dataset.

## Tool problems
- Repeated pydeseq2 `RuntimeWarning: overflow encountered in exp` at `.venv-pdf/Lib/site-packages/pydeseq2/utils.py:1088` (it went to the console, not only the log). Harmless; the run completed.
- No other tool problems.
