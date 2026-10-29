# HANDBACK: PMID41979147 / GSE318937

Status: finished. The case-spec route ran; the validator reported 17 records and 0 errors. The final attempt is in this directory. The first attempt is under `_previous/`.

## What ran
- **Paper.** Acute exercise in humans, 2x2 crossover of olive leaf extract (OLE) vs placebo. Exercise type is between-subject: MICE (10 people) or SIE (10 people). Biopsies were taken Pre, Post and 24h. The exercise DEGs the paper reports (S3.3.p1, FIG4) are within the placebo arm: Post vs Pre and 24h vs Pre, for each exercise type. Threshold is FDR < 0.05 with no fold-change rule. The paper's method is edgeR filterByExpr + TMM, then voomWithQualityWeights + duplicateCorrelation on donor (S2.5.5.3.p2), with all 119 biopsies in one model.
- **Data.** `GSE318937_genePerSampleOrder_FortitudeUnil.csv.gz`: 62,754 Ensembl genes x 119 samples of integer raw counts.
  - Alignment is exact, 119/119. The key is `Library name: <n>` from the metadata `description` field.
  - Subject S05 (MICE) has no placebo Pre biopsy, as the paper describes (one participant with 5 biopsies).
- **Design.** Factors are time (Pre/Post/H24) and trt (PLA/OLE), with strata = exercise type and subject blocking. Suitability: analyzable, 22/22 comparisons.
- **Primary model.** One DESeq2 joint model per exercise group, `~ subject + cell`, using all 59 MICE or 60 SIE biopsies.
  - The 4 planned placebo contrasts are primary.
  - The other 7 comparisons per group are exploratory: OLE-arm time effects, OLE vs PLA at each time, and the time x trt interactions.
- **Sensitivity model.** limma on log2(CPM+1) with subject as a fixed effect, planned contrasts only.
- **Enrichment.** GSEA Hallmark (stat ranking) on the 4 planned DESeq2 tables.

## DEG counts vs paper (FDR < 0.05, no FC cutoff; paper S3.3.p1)
| Contrast (placebo) | Paper | DESeq2 joint (primary) | limma log-CPM (sensitivity) |
|---|---|---|---|
| MICE Post vs Pre | 3883 | 1138 (733 up / 405 down) | 695 |
| MICE 24h vs Pre | 3608 | 2081 (1114 / 967) | 2346 |
| SIE Post vs Pre | 190 | 206 (186 / 20) | 125 |
| SIE 24h vs Pre | 2967 | 1053 (669 / 384) | 238 |

- **Where we match.** SIE Post matches closely. The pattern "SIE Post is much smaller than the other three" is reproduced.
- **Where we fall short.** The other three contrasts have about 30-60% of the paper's counts. The likely cause is the method: a mixed model with duplicateCorrelation and quality weights, fitted on 119 samples, uses information between subjects. Our fixed-subject DESeq2 model, fitted within one exercise group, does not.
- **OLE vs PLA (exploratory).** These comparisons find almost no DEGs: 0-6 per time point.

### GSEA Hallmark
- **Inflammation.** TNFA/NFKB and inflammatory response are strongly up at Post for both exercise types. This matches FIG6.
- **OXPHOS (paper S3.5.p1):**

| Contrast | Paper | Ours | Agreement |
|---|---|---|---|
| MICE 24h | up, FDR 0.047 | up, NES 1.14, FDR 0.24 | same direction, not significant |
| SIE Post | down, FDR < 0.001 | down, NES -2.32, FDR ~0 | agrees |
| SIE 24h | down, FDR 0.022 | up, NES 1.58, FDR 0.005 | opposite direction |

The paper used CAMERA; we used preranked GSEA on DESeq2 stat.

## Deviations (declared)
1. **Method.** We used DESeq2 with subject as a fixed blocking effect instead of limma voomWithQualityWeights + duplicateCorrelation. That paper route is recorded as blocked because no executor implements duplicateCorrelation or quality weights in a multi-level model.
2. **Model scope.** Each exercise group was fitted separately instead of in one 119-sample model, because a fixed subject term is aliased with the between-subject exercise type.
3. **Filtering.** No filterByExpr/TMM filtering; DESeq2 does its own normalisation and independent filtering.
4. **Period.** Crossover period was not adjusted, as in the paper. The planned contrasts compare biopsies from the same session.

## Tool problems
- **`tools/case_runner.py:709` (`_comparisons`).** `"comparisons": "all"` returns every suitability comparison across all strata. It ignores the execution's `subset`, so a joint executor subset to one stratum fails with `POLICY BLOCKED: no samples in cell {'ex': 'SIE', ...}` (first attempt, `_previous/`). The workaround was to list each stratum's comparison names explicitly.
- **No executor for the paper's route.** No executor offers limma-voom with `duplicateCorrelation` or `voomWithQualityWeights` in a multi-level design. `tools/limma_voom_tools.py` is two-arm only, with no blocking or random effect. This is why the paper route is blocked.
