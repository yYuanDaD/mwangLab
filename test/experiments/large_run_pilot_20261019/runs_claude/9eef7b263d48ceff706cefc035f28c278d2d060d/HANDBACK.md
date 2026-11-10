# HANDBACK: GSE124676 / PMC6997272 (exercise in Parkinson's disease leukocytes)

## What ran
- Case spec route (`tools.case_runner execute case_spec.json`); validator: 13 records, 0 errors. Status: completed, route `declared_deviation`.
- Data: `GSE124676_genes.fpkm_table.txt.gz` (Cuffnorm FPKM, 26,111 genes x 42 samples); matrix columns aligned exactly to metadata `description` (42/42).
- Design: 21 PD patients, before vs after 12 weeks of exercise. Tai chi and MET pooled as in the paper (S3.3.p1). Subject (patient code from title, e.g. a19 / a19f) is a blocking factor.
- Method: log2(FPKM+1), then limma `~ C(subject) + Treatment` (moderated paired test). limma removed 4,863 zero-variance (all-constant) genes, leaving 21,248 tested.
- Threshold: the paper's rule, raw P < 0.05 with no fold-change cutoff (S2.4.p1), source `paper_on_deviation_route`. BH FDR < 0.05 is recorded as the audit threshold.
- Enrichment: Enrichr ORA (GO BP/MF/CC, KEGG 2021) separately for up and down DEGs, plus Hallmark GSEA on the limma t ranking.

## DEG counts vs paper (raw P < 0.05, no FC)
| Contrast | Ours | Paper |
|---|---|---|
| after vs before (all) | 1,984 | 1,873 |
| higher after (up) | 529 | 417 |
| higher before (down) | 1,455 | 1,453 |

- Audit rule (BH FDR < 0.05): 0 genes; the minimum padj is 0.14. The paper's DEG list rests on uncorrected P values.
- All 14 named genes change in the paper's direction. Down after exercise: ODC1 (our 3rd-smallest P), CD3E, GRAP2, FOS, ZAP70, IL2RA, IL2RB, TNFRSF18, RTP5, CCL5, CD28. Up after: TRAF3, TNF, AGAP2.
- 13 of the 14 genes pass P < 0.05. AGAP2 does not (P = 0.065), although the paper calls it significantly upregulated.
- KEGG ORA reproduces the paper's headline pathways. Down DEGs: T cell receptor signaling pathway is top (adj P 3.8e-4), then primary immunodeficiency (adj P 0.044). Up DEGs: osteoclast differentiation is top (adj P 2.6e-7). Paper S3.4.p1 reports the same.
- Hallmark GSEA (exploratory, not in the paper): interferon alpha/gamma, IL6-JAK-STAT3 and inflammatory response are shifted up after exercise.

## Deviations
- The paper used an ordinary paired Student t-test on FPKM and did not state the scale. We ran a limma moderated paired test on log2(FPKM+1). There is no paired-t executor, and a hand-written test is not allowed. The paper route is recorded as blocked.
- No expression filter was applied, because the paper states none. limma's own drop of zero-variance genes is the only filtering.
- The paper's numbers do not add up: 1,453 + 417 = 1,870, not the stated 1,873 (S3.3.p1).
- GEO metadata labels subject a22 MET at before and Tai chi at after. This does not affect the pooled contrast, but it is recorded as a discrepancy.
- There is no non-exercise control arm, so season, medication and other time effects are confounded with exercise. The paper notes climate (S4.p7). This is recorded in the study caveats.

## Tool problems
- None that blocked the run.
- Minor: `tools/limma_tools.py:106-107` silently drops zero-variance features (26,111 to 21,248). This is printed only in `case_runner.log` and not recorded in the method decision record.
