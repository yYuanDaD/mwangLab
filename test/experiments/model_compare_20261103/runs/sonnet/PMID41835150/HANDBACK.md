# HANDBACK: PMID 41835150 / GSE319603 (sonnet run)

STATUS: finished (route paper_aligned; contract validator: VALID, 12 decision records)

## What ran
- Route: `tools.case_runner` case-spec (inspect, then `execute case_spec.json`), decisions written by me in `case_spec.json`. Native mode, 0 external LLM attempts (`run_manifest.json`). Preflight skipped as instructed.
- Paper: Frontiers Physiol 2026, mouse gastrocnemius, groups C, CM, H, HM (n=6 RNA-seq per group). Exercise estimand = HM vs H (8-week MICT within HFD). CM was not sequenced; GSE319603 holds 18 samples (C, H, HM x 6).
- Ownership: S8.p1 names GSE319603; GEO PMID 41835150; 3 x 6 samples; tissue/strain/pipeline match.
- Alignment: matrix columns (HM1.., C1.., H1..) do not match GEO titles; they equal the `Library name: X` string in the `description` field. Key derived by regex from `description`, exact match 18/18, no positional matching. `grp` (C/H/HM) derived from the same field.
- Matrix: raw integer counts (26166 genes, featureCounts). Method: pydeseq2 Wald, `~ grp`, one two-arm fit per contrast on its own two groups, alpha 0.05. Covariance not required (independent animals, no batch variable).
- Suitability verdict: analyzable.
- Enrichment: ORA (Enrichr GO BP/MF/CC, KEGG 2019 mouse) on the HM vs H DEGs (applied threshold, all directions): completed. Top KEGG terms include FoxO, insulin, MAPK signaling, as in the paper. Kept separate from the DE result.

## Threshold
Paper (S3.2.p1, S2.7.p1): adjusted P (BH) < 0.05 and |log2FC| >= 0.5. Applied identically (`threshold_source: paper`): padj < 0.05 strict, |log2FC| >= 0.5 inclusive. Audit rule (padj < 0.05, no effect cutoff) reported separately.

## DEGs vs paper
| Contrast | Ours (up/down) | Paper (up/down) | Audit (padj<0.05 only) |
|---|---|---|---|
| HM vs H (exercise, primary) | 534 (191/343) | 563 (213/350) | 1231 |
| H vs C (diet, secondary reference, not exercise) | 476 (296/180) | 458 (295/163) | 991 |

Paper genes in HM vs H: Fbxo32 -1.14, Trim63 -1.29, Foxo1 -1.37, Angptl7 -1.36, Txnip -0.78, Pdk4 -1.31, Cited4 +1.29 (paper log2FC: -1.136, -1.288, n/a, -1.356, -0.776, -1.306, +1.293), all padj ~0. Myogenic genes unchanged: Pax7 padj 0.77, Myod1 0.13, Myog 0.14 (matches "minimal effect on myogenic genes"). H vs C log2FC values (Cd36 0.717, Fabp3 1.741, Plin5 1.229) match Table 1.

## Deviations (declared)
- pydeseq2 instead of R DESeq2 v1.22.2; the paper does not report its model formula or low-count filtering, so the tool's default handling was used. Counts differ by about 5% (HM vs H) and 4% (H vs C), consistent with implementation and filtering differences.
- H vs C was run as a non-exercise reference contrast only, because the paper reports it and it checks the pipeline.
- Result files are stored under `PMID41835150/results/`; the runner placed per-contrast tables there.

## Tool problems
- None blocking. Notes: the first `execute` attempt via a bash heredoc failed on my side (quoting), no tool issue. `padj` and `pvalue` appear as 0.0 for strongly significant genes in the `paper_gene_check` lookup (rounded to 4 decimals in `reproduction_summary.json`), so the table gives no ordering among very small values. I did not locate the source line for this.
- Metadata CSV from GEO has mojibake in text fields (en dash shown as garbage), no effect on the analysis.
