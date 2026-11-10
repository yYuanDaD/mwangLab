# HANDBACK: PMID36839405 / GSE222163

Paper: Transcriptomics Dissection of Calorie Restriction and Exercise Training in Brown Adipose Tissue and Skeletal Muscle (Nutrients 2023, PMC9966723).
Outcome: **finished**. The route is `paper_aligned`, and the decision-contract validator returned 0 errors over 17 records.

## What ran
- `case_runner inspect GSE222163`. Then `prep_matrix.py`: it lower-cases `Ctrl` to `ctrl` in the matrix column names so they match the GEO `description` field one to one, and it drops 4 rows with Excel-mangled duplicate symbols (`1-Mar`, `2-Mar`, two rows each). Then `case_runner execute case_spec.json`.
- Alignment: an exact match on `description` covers 29/29 samples. The derived columns are `tissue` (BAT/SkM) and `grp` (Ctrl/CR/EX/CREX). GEO's `CE` is recoded to CREX.
- Matrix: RSEM expected counts. About 94% of values are integers, column sums are about 21-25 M, and S2.7.p1 says RSEM fed DESeq2. The counts were rounded at case level, then run through DESeq2 (pydeseq2 Wald, `~ grp`). Each run used only the two compared groups of one tissue, which is the paper's "two groups" route (S2.7.p1).
- Suitability: analyzable. 12/12 comparisons have n >= 3. The sex check passed (all male).
- Covariance: none needed. Animals are independent and no batch is recorded.
- Enrichment: ORA (Enrichr GO + KEGG, all-direction DEGs) and Hallmark GSEA for EX vs control in both tissues.

## DEG counts vs the paper
Threshold (paper, S2.7.p1; also in GEO `data_processing`): padj < 0.05 and |log2FC| > log2(1.5) = 0.5849625.

| Contrast | Ours (up/down) | Paper (up/down) | Audit: padj < 0.05 only |
|---|---|---|---|
| BAT EX vs control (primary) | 39 (13/26) | 37 (13/24), S3.3.p1 | 74 |
| SkM EX vs control (primary) | 50 (20/30) | 48 (20/28), S3.6.p1 | 102 |
| BAT CREX vs CR | 30 (26/4) | 30 (25/5), S3.3.p1 | 62 |
| SkM CREX vs CR | 29 (10/19) | 15 (6/9), S3.6.p1 | 29 |

Three of the four counts are close to the paper's. SkM CREX vs CR gives about twice the paper's count (n = 3 vs 3, so the count is unstable).

Enrichment, reported separately from DE:
- SkM EX vs control, KEGG ORA:
  - Top term is "Circadian rhythm" (Per2, Per3, Arntl; adj p = 0.007).
  - "PPAR signaling" is next (Fabp3, Ehhadh, Plin5, all down; adj p = 0.058, just above 0.05).
  - This matches the paper's statement in S3.6.p1: circadian rhythm among up genes, PPAR among down genes. Arntl is down while Per2/Per3 are up, as expected for clock-phase genes.
- SkM Hallmark GSEA: nothing reaches FDR < 0.25 except weak E2F and OXPHOS signals (FDR about 0.19-0.31).
- BAT EX vs control: the paper reports no pathways for this contrast. KEGG ORA gives AMPK/FoxO/longevity terms (Igf1, Prkag2, Pik3r1). GSEA has Myogenesis up (NES 2.70, FDR < 0.001).

## Deviations
- pydeseq2 was used instead of R DESeq2 1.38.0, on rounded RSEM expected counts.
- 4 rows with ambiguous Excel-mangled symbols were dropped.
- The non-exercise contrasts the paper reports (CR vs control, CREX vs EX) were not run because they are out of scope for the exercise request.
- Discrepancies recorded in the spec:
  - The figure legends (FIG2/FIG4) colour volcano points by raw p < 0.05, while the methods state padj. The methods rule was applied.
  - The RSEM version differs: v2.0.1 in the paper, v1.2.28 in GEO.

## Tool problems
- `tools/case_runner.py:300-323` (`_contained_keys` / alignment-key inspect):
  - It reported `description` matching 22/29 and did not say that the 7 misses differ only by letter case (`BAT_Ctrl1` vs `BAT_ctrl1`).
  - The suggested `key_patterns` fix cannot change case, and the alignment block has no case-insensitive option. A prep script was needed.
- Duplicated feature IDs (`1-Mar`, `2-Mar`) are flagged by inspect, but the runner has no built-in way to drop or collapse them, so the same prep script handled them.
- pydeseq2 printed "overflow encountered in exp" RuntimeWarnings (`.venv-pdf/Lib/site-packages/pydeseq2/utils.py:1088`) during fitting. They did not stop the run.

## Files
- `case_spec.json`, `prep_matrix.py`, `input/GSE222163_exp_all_repaired.csv`
- `summary.csv`, `case_runner.log`, `GSE222163/suitability/suitability.md`
- `GSE222163/results/<contrast>/DEG_results_*.csv`
- `GSE222163/results/enrichment_*`
