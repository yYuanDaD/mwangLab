# HANDBACK: PMID 31589602 / GSE123879

The paper is "Dynamic enhancers control skeletal muscle identity and reprogramming" (PLoS Biol 2019, PMC6799888).

**Status: finished (declared deviation).** The case spec is `case_spec.json`. The runner log is `case_runner.log`. The validator passed: 12 records, 0 errors.

## What ran
- **Data.** GSE123879 is a SuperSeries (RNA-seq, ChIP-seq and ATAC-seq). Its RNA-seq part is SubSeries **GSE123878**: 15 quadriceps samples, 5 sedentary WT (Control), 5 wheel-running WT (Exercise) and 5 sedentary Pgc1a muscle transgenic (mTg).
  - The only gene-level matrix deposited is `GSE123878_FpkmValues_AllSamples.xlsx`: FPKM, 12,529 genes, already pre-filtered by the authors.
  - `_RAW.tar` holds bedGraph tracks only, with no counts.
- **Prep.** `prep/prep_fpkm.py` dropped 21 gene IDs that Excel had turned into dates (Sept*/March* genes). `2018-03-02` occurs twice, so the original symbols cannot be recovered. 12,508 genes remain.
- **Alignment.** The key was taken from the metadata title (`<group>_<rep>`) and matched exactly: 15/15 samples. Groups are SED, EX and MTG, n = 5 each.
- **Model.** One limma model (`~0 + grp`) on log2(FPKM+1), with planned contrasts:
  - EX vs SED (primary, the exercise effect)
  - MTG vs SED (secondary, genetic and not exercise)
- **Covariance.** None needed: independent mice, randomly assigned.
- **Enrichment for EX vs SED.**
  - ORA (Enrichr GO and KEGG) completed.
  - GSEA Hallmark completed. Top sets are OXPHOS, angiogenesis, myogenesis, IFN-gamma/alpha and adipogenesis (all up); UPR and MYC targets are down (FDR < 0.05).

## DEG counts vs the paper
Paper threshold: DESeq2 BH padj < 0.05, no fold-change rule (S4.7.p1). We applied the same rule to the limma results (`paper_on_deviation_route`).

| Contrast | Ours (up/down) | Paper (up/down) | Audit: padj<0.05 & \|FC\|>1.5 |
|---|---|---|---|
| EX vs SED | 900 (520/380) | 1562 (779/783) | 141 (deposited DESeq2 list: 182) |
| MTG vs SED | 5878 (2883/2995) | 5582 (2843/2739) | 1513 (deposited: 2334) |

Comparison with the authors' deposited DESeq2 lists (`*_DifferentialGenes`):
- **EX vs SED:** 868 of our 900 DEGs are in the paper's list. On shared genes, log2FC r = 0.961 and sign agreement is 100%.
- **MTG vs SED:** 5362 of our 5878 DEGs are in the paper's list. r = 0.956, sign agreement 100%.
- **Named genes, all in the paper's direction:**
  - Acadl up (log2FC 0.35, padj 0.004)
  - Myh4 down (log2FC -0.43, padj 0.020)
  - Myh2 up (log2FC 1.87)
  - Ppargc1a up in mTg (log2FC 2.75)

Our limma-on-FPKM route is more conservative for the smaller exercise effect, so it finds fewer EX vs SED DEGs than the paper.

## Deviations
1. **Method.** We used limma on log2(FPKM+1) instead of DESeq2 on STAR counts. The paper route is blocked because no counts were deposited.
2. **Model.** We fitted one joint 3-group model instead of the paper's separate pairwise BaseSpace DESeq2 runs.
3. **Genes.** 21 date-mangled genes were dropped. The authors' FPKM matrix covers 12,529 genes, so 18 of the paper's 1562 exercise DEGs are absent.
4. **Threshold wording.** S2.6.p1 says "p-value < 0.05" for the 779/783 counts. The Methods (S4.7.p1) and the deposited list (max padj 0.04998, max raw p 0.006) show the rule was padj < 0.05, so padj < 0.05 was used. This is recorded as a discrepancy.

## Tool problems
1. **Date-mangled IDs not flagged.** `tools/native.py:616` (`_EXCEL_DATE`) only matches the `15-Sep` and `Sep-15` forms. After the xlsx-to-csv conversion in `geo_tools`, the IDs read as `2018-09-15 00:00:00`, so inspect reported no `excel_date_ids` (only `duplicated_feature_ids: 1`). The 21 mangled IDs had to be found by hand.
2. **Header-less files mis-profiled.** `tools/case_runner.py:395-410` (inspect) profiled the header-less `*_DifferentialGenes.csv` files as matrices with numeric "sample columns", because the first data row was read as the header. This is cosmetic but misleading.
3. **SuperSeries not resolved.** Inspecting SuperSeries GSE123879 returned `matrices: []` with no pointer to the SubSeries (GSE123878) that holds the data. It had to be found by hand from `series_id` and `Series_relation`.
