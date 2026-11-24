# HANDBACK — PMID29123172 / GSE99963

**Status: finished.** The case-spec route ran through `tools.case_runner execute`. The decision-contract validator passed: 15 records, 0 errors. Final route: `paper_aligned`.

## What ran
- **Data:** `GSE99963_GeneCoverage.tsv.gz`. This holds featureCounts raw integer counts for 60,675 Ensembl genes × 28 samples, from 14 men at Pre and Post. Columns were aligned exactly on `title` (28/28).
- **Exclusion:** subject **S3** (GSM2666603 Pre_S3 and GSM2666610 Post_S3) was dropped. Pre_S3 has 102,811 assigned reads, against a median of about 7.9M. The paper reports 13 subjects (Ex 7 / Sed 6, Table 1) while GEO deposits 7+7, so one Sed subject must have been dropped. S3 is the only failed library. This is an assumption: the paper does not name the dropped subject. Analysed: Ex 7 subjects, Sed 6 subjects.
- **Method:** the paper's route (S2.6.p1), run through `tools.r_de_tools:run_r_de` with engine `edger_ql`. That is R edgeR with TMM, `glmQLFit`/`glmQLFTest`, and the design `~ subject + time`, fitted separately in each group.
  - Primary: Ex-HFD Post vs Pre.
  - Secondary: Sed-HFD Post vs Pre.
  - Exploratory (not in the paper): the group × time interaction, `~ subject + time + ex_post` with coefficient `ex_post`. It estimates the exercise-specific change, (Ex Post−Pre) − (Sed Post−Pre).
- **Threshold:** the paper's rule, FDR < 0.1 with no fold-change cutoff (S2.6.p1). Audit rule: FDR < 0.05.
- **Enrichment** on the Ex-HFD table: GO/KEGG ORA up and down, plus Hallmark GSEA. All three completed.

## DEG counts vs paper (FDR < 0.1)
| Contrast | Ours (up/down) | Paper (up/down) | Audit FDR<0.05 |
|---|---|---|---|
| Ex-HFD Post vs Pre | 4256 (2292/1964) | 2617 (1561/1056) | 3114 |
| Sed-HFD Post vs Pre | 1487 (802/685) | 412 (264/148) | 873 |
| Interaction (exploratory) | 2 (1/1) | not tested | 2 |

- **Named genes:** every gene the paper names agrees in direction and is significant.
  - Sed: SLPI +2.75, IRAK2 +1.01, NUPR1 +0.76, MDH1 −0.80, FGF6 −1.04. These log2FC values almost exactly match Table 2.
  - CHAC1 goes up in Ex (+1.77) and down in Sed (−3.04), as S3.2.p1 reports.
  - ANGPTL4 goes up in Ex (+3.20; Fig 5I).
- **Interaction:** the formal test finds only 2 genes, and CHAC1 is the top one (FDR 0.013). So the paper's claim that thousands of genes respond to exercise rests on comparing two within-group lists. The data do not back it as a group × time difference at this n.
- **Ex-HFD enrichment:** genes going up are enriched for ECM, collagen, focal adhesion and cytokine terms. Genes going down are enriched for mitochondrial respiration and OXPHOS terms. Hallmark GSEA puts EMT, complement and IFN on top. The paper (S3.1.p2) highlighted muscle-structure and circadian terms. These sets are not directly comparable, because the paper ran GO only on the genes found in the Ex group alone, after Revigo summarising.

## Deviations
1. **Gene filter.** The paper keeps genes with rpkm > 0.1 in ≥ 5 samples (23,373 genes). Gene lengths are not deposited, so I used CPM ≥ 0.15 in ≥ 5 samples, applied within each execution's samples. That kept 20,940 genes for Ex, 20,230 for Sed and 23,198 for the interaction model.
2. **S3 exclusion:** inferred, as described above.
3. **Robust settings.** The executor uses `estimateDisp(robust=TRUE)` and `glmQLFit(robust=TRUE)` (`tools/r_de.R:201-202`); the paper does not state either setting. Together with the smaller gene universe, this is the most likely reason for our roughly 1.6× (Ex) and 3.6× (Sed) higher counts. The difference is larger in Sed, where n is smaller.
4. **Annotation:** used as deposited (Ensembl v84 per GEO), although the paper text says Gencode.
5. **Interaction model:** added as an exploratory analysis.

## Tool problems
- The runner's `edgeR` executor, `tools/edger_tools.py:38` (`run_edger_analysis`), has no covariate or blocking argument, so it cannot fit the paper's paired `~ Timepoint + Subject` design. I used `tools.r_de_tools:run_r_de` instead, which `references/case-spec.md` does not list.
- `tools/r_de.R:201-202` hard-codes `robust=TRUE`, so the paper's plain `glmQLFit` cannot be reproduced through the executor.
- Count-based filtering offers only CPM or count rules (`tools/case_runner.py:771-787`). There is no RPKM rule that takes gene lengths, so a paper's RPKM filter cannot be expressed.
- Minor: `filter_low_counts` is applied per execution subset (`tools/case_runner.py:771`), while the paper filtered across all samples. There is no option for a case-level filter.
