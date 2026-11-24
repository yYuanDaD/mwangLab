# HANDBACK: PMID 35813950 / GSE205907

Exercise in MPTP-induced Parkinson's disease mice. Bulk RNA-seq of 4 brain regions (cerebellum, cortex, SN, striatum), 3 groups (Saline, MPTP, MPTP+EX), n = 4 female mice per group. 48 samples in total.

## What ran
- Route: case spec (`case_spec.json`), then `python -m tools.case_runner execute`. Status `completed`. The validator checked 18 records and found 0 errors.
- Prep (`prep_GSE205907.py`, run with `-I`):
  - Dropped 27 gene IDs that Excel had turned into dates (`2019-03-xx` for Marchf genes, `2019-09-xx` for Septin genes; 2 of them duplicated).
  - Built a sample sheet from the matrix column names: prefix `E`/`M`/`S` gives the group, the suffix gives the region, and the number gives the animal.
  - The sheet's group x region table equals the GEO treatment x tissue table (4 per cell).
- Why a derived sample sheet: the matrix columns use animal IDs (E26–E29, M6/M16/M21/M23, S1–S4), while GEO titles use `rep1..rep4`. Nothing links the two except column order, and positional alignment is not allowed. The labels are backed by marker genes:
  - Region markers match (Pcp2/Gabra6, Satb2/Neurod6, Th/Slc6a3, Ppp1r1b/Penk).
  - Nigral Th/Slc6a3 is 4–7x lower in E and M animals than in S animals, which fits the MPTP lesion.
  - All samples are female (Xist present, no Y-linked genes).
- Matrix: FPKM (non-integer values, column sums 345k–621k, file named fpkm, paper says FPKM). Transformed with log2(x+1).
- Design: one limma model per region (stratum = tissue), `~ 0 + grp`, no blocking. Each animal contributes only one sample per region.
  - Primary contrast: EX vs MPTP, the effect of exercise within PD mice.
  - Secondary: MPTP vs SAL, the PD-model effect.
  - Exploratory: EX vs SAL.
- Expression filter: the paper's "FPKM > 1", applied as FPKM >= 1 in at least 4 of the 12 samples of each region.
- Threshold: the paper's rule, raw p < 0.05 with no fold-change cutoff (S2.7.p1, FIG3 legend). Source is `paper_on_deviation_route`. Audit rule: BH FDR < 0.05.
- Sensitivity run `limma_Stria_noE29`: striatum refit without E29Stria, a clear outlier (mean correlation 0.83 vs 0.97 for every other striatum sample, FPKM sum 621k, low Xist).
- Enrichment (ORA on GO/KEGG, GSEA on Hallmark) ran for EX vs MPTP in SN and striatum, and completed.
- Post-hoc reversal sets (`reversal_sets.py` -> `reversal_sets_summary.csv`, `reversal_sets.csv`, `reversal_sets_noE29.txt`): genes with p < 0.05 in both MPTP vs SAL and EX vs MPTP, with opposite directions. This is the only DEG count the paper reports.

## DEG counts vs paper (raw p < 0.05, no FC cutoff)

| Region | EX vs MPTP n (up/down) | MPTP vs SAL n | Reversal: down / up after exercise | Paper reversal: down / up |
|---|---|---|---|---|
| Cerebellum | 737 (434/303) | 1469 | 70 / 85 | not reported |
| Cortex | 773 (421/352) | 2586 | 112 / 176 | not reported |
| SN | 1015 (490/525) | 1516 | 124 / 81 | 155 / 66 |
| Striatum (all 12) | 509 (212/297) | 147 | 17 / 27 | 49 / 185 |
| Striatum without E29 (sensitivity) | 1284 (595/689) | 1319 | 174 / 157 | 49 / 185 |

- The paper gives no per-contrast DEG totals in the text; they appear only in the Venn diagrams of FIG2D.
- Audit rule (FDR < 0.05) for EX vs MPTP gives 0–2 genes in every region. The exercise effect does not survive multiplicity correction anywhere.
- SN is close to the paper (124/81 vs 155/66, same "more down than up" shape).
- The striatum does not reproduce the paper's strong up-bias (185 up), with or without E29.
- Reversal sets that share the MPTP arm are partly a regression-to-the-mean artefact: noise in the MPTP group pushes the two contrasts in opposite directions.

Named genes (EX vs MPTP):
- **SN, contradicts the paper.** Neurod2 has log2FC −1.60 (p = 0.005) and Rtn4rl2 has −1.72 (p = 0.015). Both go down with exercise, but the paper says they go up.
  - Both are cortex/cerebellum-enriched genes. Two MPTP nigra samples (M21, M23) carry cerebellar contamination (Pcp2 212 and 95 vs ≤53 elsewhere), which likely inflates these genes in the MPTP arm.
  - Cd5 is filtered out (FPKM about 0).
- **Striatum, same direction but not significant.** Nr4a2 has +1.10 (p = 0.25; +1.75, p = 0.058 without E29) and Ntn5 has +1.13 (p = 0.038). Bmp5 is filtered out (FPKM < 0.5).

Enrichment (kept separate from DE):
- SN GSEA: EMT, interferon and IL6-JAK-STAT3 up with exercise (FDR < 0.05). SN ORA: synaptic-transmission GO terms (adjusted p 1.6e-4). This partly matches the paper's synaptic themes.
- Striatum GSEA: oxidative phosphorylation, DNA repair and ROS up. ORA is not significant. This does not reproduce the paper's synaptogenesis signal, and E29 may drive it.

## Deviations (declared)
1. limma on log2(FPKM+1) replaces the paper's DESeq v1.14. Only FPKM was deposited; GEO `data_processing` mentions HTSeq counts, but no counts file exists.
2. The paper's "FPKM > 1" filter was turned into a concrete rule (>= 1 in at least 4 of 12 samples per region).
3. 27 Excel-mangled gene IDs were dropped.
4. GSM IDs are not attached to samples; labels were decoded from the matrix column names (alignment confidence: medium).
5. Quantification differs between paper and GEO (paper: Tophat2/Cufflinks/RSEM; GEO: hisat2/HTSeq, mm9). Recorded as a discrepancy.
6. The E29Stria exclusion is a sensitivity run only; the primary fit keeps all samples, as the paper does.

## Tool problems
- The `inspect` profile reports `duplicated_feature_ids: 2` (`tools/native.py:284`) but does not flag the 27 Excel date-mangled gene symbols. I found them by hand.
- The case runner cannot express an overlap between result tables (the reversal sets). `study.paper_counts` only compares single tables (`tools/case_runner.py:155`, `:969`), so I wrote a post-hoc script and left `paper_counts` empty.
- The alignment gate has no way to link a matrix that uses animal IDs to GEO rep-numbered samples except by position. A derived sample sheet was needed.
- Environment: a bash heredoc containing an apostrophe failed in the Bash tool, so I generated the spec from a scratch Python file instead. Not a repository bug.
