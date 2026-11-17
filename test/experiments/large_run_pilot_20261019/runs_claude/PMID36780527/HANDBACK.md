# HANDBACK: PMID 36780527 / GSE199429

Paper: Time of day determines postexercise metabolism in mouse adipose tissue (PMC9974500).
Status: **finished** (route `declared_deviation`). The validator reported no errors in 12 records.

## What ran
- `case_runner inspect GSE199429` downloaded the series into `E:/agent/mwangLab_pdf/data/GSE199429`. One matrix was there, `GSE199429_processed.data.csv.gz`, with 16,233 Ensembl genes and 24 samples.
- `case_runner execute case_spec.json`:
  - **Alignment:** matched on `title` with `normalize_keys` (for example `13Run_e` = `13RUN_E`). All 24/24 samples aligned.
  - **Factors:** `ex` (SED/RUN) and `time` (ZT3/ZT15), with 6 samples per cell.
  - **Matrix:** CPM after the authors' filterByExpr. GEO `data_processing` says "processed.data.csv contains cpm after filtering". The profile agrees: 0.17% of values are integers and column sums run from 0.84M to 1.19M.
  - **Method:** limma on log2(CPM+1). It is one joint cell-means model `~ 0 + C(cell)` fitted on all 24 samples, the same parameterization as the paper's `~0 + group`. It produced the 4 planned contrasts plus the exercise×time interaction as an exploratory contrast.
  - **Threshold:** BH FDR < 0.05 with no fold-change rule. This is the paper's rule (S3.6.p1), applied on the deviation route.
  - **Enrichment:** ORA (Enrichr GO BP/MF/CC and KEGG) and Hallmark GSEA, run on the ZT15 RUN-vs-SED contrast only.

## DEG counts vs paper (FDR < 0.05, no FC cutoff)
| Contrast | Ours (up/down) | Paper |
|---|---|---|
| RUN vs SED at ZT15 (early active), primary | 113 (81/32) | 121, "most up-regulated" |
| RUN vs SED at ZT3 (early rest), primary | 0 | 0 |
| ZT15 vs ZT3 within SED | 187 (95/92) | 192 |
| ZT15 vs ZT3 within RUN | 682 (408/274) | 744 |
| Interaction ex×time, exploratory | 0 | not tested |

**Named genes, ZT15 exercise:** all 15 have a positive log2FC, the same direction as the paper.
- 8 pass FDR < 0.05: Nr4a1, Nr4a3, Cpeb2, Cyp2b10, Gadd45g, Irf4, Zfp516, Crem.
- 4 fall just short (padj 0.053–0.079): Adrb2, Slc25a25, Pdk4, Vegfa.
- 3 are clearly not significant: Ppargc1a (padj 0.21), Dio2 (0.51), Ucp1 (0.92, log2FC 0.49).

The paper shows these genes as up-regulated in the FIG2F heatmap.

**GO MF (ORA):** the top terms are nuclear glucocorticoid receptor binding (padj 0.0013), MAPK binding, DNA-binding transcription activator activity (RNA Pol II), and CREB binding. This agrees with the paper's FIG2D, which reports glucocorticoid receptor binding and DNA-binding transcription activator activity. Hallmark GSEA (exploratory, not in the paper) has TNFA/NFKB, hypoxia, adipogenesis and OXPHOS positive.

## Deviations
1. The paper used edgeR QL NB GLM on featureCounts counts. That route is blocked: GEO has only filtered CPM, and neither raw counts nor library sizes were deposited. I ran limma on log2(CPM+1) instead, and did not reconstruct counts.
2. I did no extra low-expression filtering. The deposited CPM is already filtered by the authors' filterByExpr.
3. The paper's ORA used clusterProfiler GO MF with all detected genes as background. Here ORA ran through Enrichr with its default library background.
4. The paper's fry signature tests against GSE43658/GSE62635/GSE55934 (FIG2E) were not reproduced.
5. Caveats recorded:
   - S3.1.p1 says the 0 h protocol was repeated in a 24-mouse subset. GEO does not record which cohort each library came from, so no cohort term could be modelled.
   - The GEO processing note (STAR 2.7.2b, Ensembl release 99, filterByExpr min.count 15 with `+ sex`) differs from the paper's Methods (STAR 2.5.3a, release 92, min count 10). All mice are male.

## Tool problems
- `tools/suitability.py:75-81` (`_TYPE_TO_KEY`) has no `cpm` key. With `matrix_type: "CPM"`, the data-type check failed as "matrix type unknown or ambiguous", the verdict became `not_analyzable`, and the design record was rejected. The workaround was to name the type `"CPM normalized (linear scale)"`, which hits the `normali` key. CPM (and log-CPM) should map to `bulk_rnaseq_normalized` (or microarray/log for log-CPM).
- `tools/enrichment_tools.py:257`: `gp.enrichr(...)` is called without a `background`. ORA cannot use the "all detected genes" background that papers such as this one specify.

## Files
- Spec: `case_spec.json`; inspect output: `inspect_GSE199429.json`
- Results: `GSE199429/results/` (per-contrast tables and enrichment); summary: `summary.csv`, `run_status.json`
- Suitability: `GSE199429/suitability/suitability.md`
- First failed attempt (CPM not recognized): `_previous/20261117T230957Z/`
