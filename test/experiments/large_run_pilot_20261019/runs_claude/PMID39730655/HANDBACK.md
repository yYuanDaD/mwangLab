# HANDBACK: PMID39730655 / GSE280324

## What ran
- Paper: PMC11680863 (Sci Rep 2024). Exercise (6-week moderate-intensity treadmill training) vs sedentary control. Tissue: male C57BL/6J liver, n=3 per group (S2.1.p1).
- `case_runner inspect GSE280324` downloaded the series. `GSE280324_FPKM.txt.gz` holds FPKM, TPM, read_count and group-average blocks side by side.
- `prep_tpm.py` kept only the six `tpm_*` columns, which match the paper's input (S3.p1). Each column sums to 1e6. Rows are indexed by the unique gene symbol, and the columns are renamed to the sample tag. Output: `GSE280324_TPM.csv`.
- Alignment: an exact match on a key taken from GEO `description` (`fpkm_<tag>`), 6/6 samples. The group (C→SED, E→EX) comes from the tag. It agrees with the title and the treatment characteristic.
- Method: limma (inmoose port) on log2(TPM+1), `~ grp`, EX vs SED. This is the paper's route (S3.p1, TAB1). Suitability: analyzable. The validator found 0 errors.
- Enrichment: ORA (Enrichr GO/KEGG) and GSEA (Hallmark) both completed.

## DEG counts vs paper
Paper threshold (S3.p1, TAB1): raw p < 0.05 & (FC > 1.2 or FC < 0.83).

| Rule | Ours (total / up / down) | Paper |
|---|---|---|
| Exact paper rule, recomputed post hoc (up log2FC > log2 1.2 = 0.2630; down log2FC < log2 0.83 = -0.2688) | **2034 / 1456 / 578** | 2034 / 1456 / 578 |
| Runner's applied rule (symmetric \|log2FC\| > 0.2630344) | 2047 / 1456 / 591 | — |
| Audit rule (BH padj < 0.05, no FC cutoff) | 4218 | — |

- Under the paper's exact rule, the counts match exactly.
- Named genes: Aldoa (log2FC +0.276, p=2e-4), Acsl1 (+0.322), Hadhb (+0.299) and Fasn (+0.378) are all up in EX with p < 0.001. This matches S8.3.p1 and S9.p3.
- Hallmark GSEA: FATTY_ACID_METABOLISM NES 1.96 (FDR < 0.001), HYPOXIA NES 1.45 (FDR 0.035), GLYCOLYSIS NES 1.35 (FDR 0.084). KEGG ORA includes PPAR signaling and fatty acid degradation. This is consistent with S8.1.p1. Enrichment is reported separately from the DE result.

## Deviations
- The inmoose limma port was used instead of R limma 3.46.0. No expression filter was applied (the paper states none). limma dropped 13 rows: 10 all-zero, 3 others.
- The paper's down cutoff, FC < 0.83, is asymmetric. The runner applied a symmetric cutoff, so the exact count was recomputed from `GSE280324/results/grp_EX_vs_SED/DEG_results_EX_vs_SED.csv`.
- GEO `data_processing` gives a different rule (p < 0.05, |log2FC| > 1). The paper's rule was used.
- The paper's raw-p rule is permissive with n=3 per group. The BH audit count is reported above.

## Tool problems
- The threshold schema accepts only one symmetric `effect_cutoff` (`tools/case_runner.py:406`, `:775`). It cannot express an asymmetric fold-change rule such as FC > 1.2 / FC < 0.83. The runner's count is therefore 13 down-regulated genes too high, and the exact count needed a post-hoc recomputation.
- Minor: GSEA warned "Duplicated values found in preranked stats: 6.29% of genes" (`case_runner.log:13`). This is expected for limma t-statistics with tied low-expression genes, and it is not a failure.
