# HANDBACK: PMID42019489 / GSE312393

Paper: *A skeletal muscle atlas shows neuromuscular junction adaptations to growth and atrophy* (PMC13108521). The atlas itself is mouse sc/snRNA-seq data (GSE294765, GSE311567). GSE312393 holds the **human exercise bulk RNA-seq** shown in Figure 6J/K (S2.5.p5, S5.1.3.p1, S5.2.26.p1, S5.2.27.p1).

## What ran (case-spec route, `case_spec.json`; the validator reported 22 records and 0 errors)

| Case | Samples | Design | Method | Route |
|---|---|---|---|---|
| GSE312393_24h | 4 resting controls vs 3 men 24 h after eccentric downhill running (vastus lateralis) | two-group, between-subject, `~ trt` | limma eBayes on log2(TPM+1) | declared_deviation |
| GSE312393_6wk | 3 women before and after 6 weeks of resistance training | paired, `~ subject + trt` (subject is the blocking term) | limma eBayes on log2(TPM+1) | exploratory (residual df = 2 < 4) |

- **Matrix:** GEO deposits only TPM files (column sums about 1e6), so I used TPM. The paper used tximport counts with a DESeq2 VST, but the counts were not deposited, so a count model was blocked.
- **Prep (`prep/prep_tpm.py`):**
  - Re-indexed the 6-week file by Ensembl `gene_id`. The deposited file had a row-number index.
  - Applied a label-blind prefilter: keep genes with TPM >= 1 in at least 3 samples. This kept 11,874 of 62,703 genes for the 24 h set and 12,827 for the 6-week set.
- **Alignment:** exact match on the library name taken from the GEO `description` field, with 100% of matrix columns matched. The sex check passed: each set has a single sex.
- **Enrichment:** Hallmark GSEA (preranked by stat) completed for both cases. Top terms:
  - 24 h: OXPHOS, EMT, angiogenesis.
  - 6 weeks: EMT, myogenesis, apical junction, angiogenesis.

## DEG counts vs paper

The paper reports **no DE test, DEG count or threshold** for these bulk data, only heatmaps of VST expression for selected genes. Its S5.3.p1 rule (padj < 0.05, |log2FC| > 0.15, >= 5% of cells) applies to sc/snRNA-seq. I therefore applied the `workflow_default` threshold (BH padj < 0.05, no effect-size cutoff) and added the paper's single-cell rule as a separate audit threshold.

| Contrast | Applied (padj < 0.05) | Audit (+ abs(log2FC) > 0.15) | Paper |
|---|---|---|---|
| 24 h exercise vs control | 2 (2 up / 0 down) | 2 | none reported (heatmap only) |
| post-6 weeks vs pre | 9 (6 up / 3 down) | 9 | none reported (heatmap only) |

Paper-named genes. The paper reports them as up. All three are up in our data, but none reaches significance:

| Gene | 24 h log2FC | 24 h raw p | 24 h padj | 6 weeks log2FC | 6 weeks raw p | 6 weeks padj |
|---|---|---|---|---|---|---|
| BMP1 | +0.28 | 0.15 | 0.70 | +0.57 | 0.03 | 0.42 |
| BMPR2 | +0.09 | 0.48 | 0.86 | +0.44 | 0.08 | 0.50 |
| RFLNA | +0.02 | 0.91 | 0.98 | +0.63 | 0.02 | 0.39 |

## Deviations and discrepancies

- **Test and input:** the paper only displays VST heatmaps. I ran a limma test on TPM because no counts were deposited.
- **Controls in the 24 h set:** GEO has 4 control columns, but the paper says n = 3 (Figure 6 legend J). All 4 were kept because the paper does not say which 3 it used.
- **6-week design:** the paper's legend says "n=3 exercised and n=3 control". In GEO these are the same 3 participants before and after training, so I analyzed them as a paired design.
- **6-week tissue label:** GEO says quadriceps femoris; the paper says vastus lateralis. Vastus lateralis is part of the quadriceps, so this does not change the analysis.
- **Separate cases:** the two arms differ in batch, library kit and sex, so each was analyzed as its own case and never pooled.

## Tool problems

- `tools/limma_tools.py:102-106` has no low-expression filter; it drops only rows that are all NA or have zero variance. Running it on raw TPM would put about 50k near-zero genes into the moderation, so I had to filter in a prep script. It also has no `trend=True` option for log-TPM.
- `tools/limma_tools.py:189-193` prints its own summary at padj < 0.05 and |log2FC| > 1. This is not the applied rule; the runner's counts are correct.
- Minor: the execution record's `formula` field copies the spec's method formula. It does not record the formula `build_multifactor_plan` actually fit (`covariate_columns=subject`), so I could not check the blocking from the record alone. In the covariance design check, POST is the reference (`trt_PRE` column); this is cosmetic only.
- No failures. GSEA required network access and completed.
