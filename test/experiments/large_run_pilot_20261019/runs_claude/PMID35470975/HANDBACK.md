# HANDBACK: PMID 35470975 / GSE185957

**Status: finished.** The run completed as a declared deviation, and the decision-contract validator found no errors (16 records).

## What ran
- **Route:** the case spec route (`tools.case_runner execute case_spec.json`). Preflight was skipped as instructed.
- **Data:** `GSE185957_norm_cpm.txt.gz`, 64,253 Ensembl genes x 16 samples. The paper's sample set is 8 subjects (4 lean, 4 obese), each with a pre and a post biopsy.
- **Alignment:** exact match on the GEO `title` column, 16/16. `status` and `time` come from `characteristics_ch1.1.group`; `subject` comes from `characteristics_ch1.0.subject`.
- **Matrix:** edgeR-normalized CPM. It is linear and non-integer, column sums are 0.84-1.12e6, and GEO `data_processing` says `norm_cpm.txt`. It is not raw counts.
- **Design:** paired post vs pre (subject blocking, `~ subject + time`), with BMI status as a stratum. There is one fit per group: lean and obese. Suitability verdict: analyzable, 2/2 comparisons.
- **Method:** limma-trend on log2(CPM+1). Genes are filtered to CPM >= 1 in >= 4 of the stratum's 8 samples, which keeps about 13.5-13.7k genes; the paper reports 13,175 transcripts identified.
- **Threshold:** the paper's rule, BH-adjusted p < 0.05 and |log2FC| > 0.5 (S3.1.p1), applied on the deviation route. The audit rule is padj < 0.05 with no fold-change cutoff.
- **Sensitivity fits:**
  - unpaired limma within each group;
  - one pooled-variance paired-change limma on all 8 subjects (`~ 0 + C(status)` on the post-pre differences).
- **Enrichment:** GSEA preranked on MSigDB Hallmark for both primary tables.

## DEG counts vs the paper (padj < 0.05 and |log2FC| > 0.5)

| Contrast | Ours (up/down) | Paper (up/down) |
|---|---|---|
| Lean post vs pre, paired (primary) | 554 (432/122) | 551 (419/132) |
| Obese post vs pre, paired (primary) | 0 (0/0); minimum padj 0.32 | 104 (82/22) |
| Lean, unpaired (sensitivity) | 62 | - |
| Obese, unpaired (sensitivity) | 0 | - |
| Joint paired-change, lean (sensitivity) | 452 | - |
| Joint paired-change, obese (sensitivity) | 0 | - |

- **Lean:** reproduced closely. The top genes are NR4A3, PPARGC1A and NR4A1, all up.
- **Obese:** not reproduced on any limma route. The top obese hits are HBB and HBD, which suggests blood content varies between biopsies.
- **GSEA:**
  - Lean: OXIDATIVE_PHOSPHORYLATION is negatively enriched (FDR 0.002). This matches the paper's lean mitochondrial/OXPHOS downregulation, although the paper used a different gene-set library.
  - Obese: one set, INTERFERON_ALPHA_RESPONSE (negative), is enriched. The paper reports no transcript gene sets for obese.

## Deviations
1. **Method:** the paper's route (edgeR negative-binomial GLM on featureCounts counts) is blocked because only CPM was deposited and no library sizes are given. limma on log2(CPM+1) ran instead.
2. **Filter:** the paper's low-expression filter is not stated, so CPM >= 1 in >= 4 samples per stratum was used as an approximation.
3. **Subject blocking:** the paper does not state its GLM design, so blocking on subject was assumed. The unpaired fit was run as a sensitivity check.
4. **Threshold:** the paper states its rule (S3.1.p1) for the baseline comparison. It was assumed to apply to the exercise contrasts too (FIG2 uses FDR).
5. **Out of scope:** the baseline obese-vs-lean comparison was not run because it is not an exercise contrast.

## Caveats recorded in the study gate
- **Exercise is aliased with leg and day.** The rest biopsy is from the right leg and the post biopsy from the exercised left leg, on separate days, and this was not randomized (S2.2.p1, S2.3.p1).
- **The study is small.** There are n = 4 pairs per group, and the paper calls itself preliminary.
- **Sex in the data does not match the paper text.** X/Y inference gives lean subjects 1-4 all female and obese subjects 5-6 male, 7-8 female. The paper says lean 2M/2F and obese 4F (S2.1.p1), or 2F/2M in each group (Table 1).
  - Each subject's pre and post samples agree in sex, and the lean count matches the paper's, so the GEO labels were kept.
  - The per-sex split was not run. A female-only lean analysis would be identical to the lean analysis, and every other per-sex cell has 2 pairs, which is below 3.

## Tool problems
- **`tools/suitability.py:458`:** `sex_split_plan` calls `enumerate_comparisons(..., strata=["_sex"])` without the design's own `strata`. It therefore proposed `time_post_vs_pre__sex-female`, which pools lean and obese across the `status` stratum, and that does not match the stratified design. This is minor; it was not acted on.
- No executor failures.
