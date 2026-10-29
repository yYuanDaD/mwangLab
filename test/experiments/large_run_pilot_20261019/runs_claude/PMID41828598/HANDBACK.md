# HANDBACK: PMID41828598 / GSE299413

Paper: Moderate Aerobic Training Causes Muscle Wasting in a DMBA-Induced Sarcoma Rat Model (PMC12985970).
Route: case spec (`case_spec.json`), run with `python -m tools.case_runner execute`. The validator returned 0 errors, and both cases completed as `declared_deviation`.

## What ran
- **Data:** GEO deposits only Partek Flow outputs. These are DESeq2 median-ratio normalized counts (non-integer) and Partek DESeq2 result tables, one pair each for tibialis anterior and tumor. No raw counts or RAW.tar are deposited.
- **Prep script:** `prep_matrix.py` keeps the gene-symbol index (unique) and the `RNA230912TZ_*` sample columns. It does not change any values; it removes 20 annotation columns, including the numeric Start/Stop/Length.
- **Case GSE299413_tibialis:** 12 samples, NC/CA/CAEX with 4 each, aligned exactly on `title`. One limma model `~ grp` on log2(x+1). Planned contrasts: CAEX vs CA (primary, the exercise effect in tumor-bearing rats), CA vs NC and CAEX vs NC (secondary). There is no Non-Cancer + Ex arm, so the exercise effect in healthy rats and the exercise x cancer interaction cannot be identified.
- **Case GSE299413_tumor:** 8 samples, CA/CAEX with 4 each. Two-group limma on log2(x+1), CAEX vs CA (primary).
- **Sensitivity runs (`*_filtered`):** the same models after a low-expression filter (normalized CPM >= 1 in >= 4 samples). This approximates Partek's noise filter, whose exact rule the paper does not state.
- **Enrichment:** GSEA Hallmark (rat genes mapped to mouse sets) ran for both exercise contrasts. ORA was not run because there were 0 DEGs.

## DEG counts vs paper
Threshold: the paper's rule, FC >|2| and FDR < 0.05 (S4.9.p1, S2.2.p1). It was applied as padj < 0.05 and |log2FC| > 1, with `threshold_source = paper_on_deviation_route`.

| Contrast | Paper (up/down) | Ours, limma (up/down) | Ours, filtered sensitivity | Partek table deposited in GEO, same rule |
|---|---|---|---|---|
| Tibialis CA vs NC | 553 (523/30) | 59 (56/3) | 110 (105/5) | 553 (523/30) |
| Tibialis CAEX vs NC | 2020 (1276/744) | 852 (471/381) | 1132 (514/618) | 2025 (1278/747) |
| Tibialis CAEX vs CA (exercise) | 26 (10/16) | 0 | 0 | 18 (7/11) |
| Tumor CAEX vs CA (exercise) | 156 (24/132) | 0 | 0 | 156 (24/132) |

- **Effect sizes agree with the deposited Partek DESeq2 log2 ratios.**
  - Pearson r over all genes: 0.83 to 0.91.
  - On the paper-significant genes: r = 0.85 / 0.95 / 0.99 / 0.95 (table order), with 100% sign agreement in every contrast.
  - The count gap is therefore a difference in power or method (limma-trend on log normalized counts, n = 4, versus Partek DESeq2 on raw counts), not a difference in direction.
- **Named genes.**
  - Tumor genes keep the paper's directions: Tgfa up (log2FC 3.0, p = 0.019), Ccl19, Ccl11, Ccl21 and Cxcl14 down, Dlk1 up. None reach BH < 0.05 (padj about 0.67).
  - Tibialis: Fbxo32, Il6st and Casp3 are up in CAEX vs NC (padj about 0.044 to 0.046). log2FC is > 1 for Fbxo32 and Il6st and 1.19 for Casp3.
- **GSEA, kept separate from DE.**
  - Tibialis CAEX vs CA: OXPHOS (NES -4.35), myogenesis, fatty acid metabolism and adipogenesis are down; allograft rejection and IL6/JAK/STAT3 are up. This is consistent with the paper's statement that energy-producing pathways are reduced further with exercise.
  - Tumor CAEX vs CA: MYC, E2F and G2M are up.

## Deviations
1. **The paper's route is blocked.** The paper ran DESeq2 on raw featureCounts counts, and only normalized counts are deposited. We ran limma on log2(normalized+1) instead. We did not round normalized counts into DESeq2, because no documented recipe exists and rounding would discard the size factors.
2. **Low-expression filter.** No noise filter was applied in the primary runs. The filtered runs are sensitivity analyses only.
3. **Deposited Partek table disagrees with the paper text.** For tibialis CAEX vs CA it gives 7/11 at the paper's rule, while the text says 10/16. This is recorded as a discrepancy.

## Tool problems
- **`filter_low_counts` can compute CPM on the log-transformed matrix.**
  - Where: `tools/case_runner.py:631`, `:645` and `:660-662`.
  - When it happens: a case-level `method.transform` is set and the execution sets neither `transform` nor `matrix: "aligned"`. The filter then reads `self.analysis_path` and computes CPM on log values. The field description says "raw counts only", but nothing checks this.
  - Workaround used here: set `transform: "log2(x+1)"` on the execution, so that the aligned matrix is filtered first.
- **`inspect` counts numeric annotation columns as samples.**
  - Where: `tools/case_runner.py:363-364`, via `native.profile_matrix`.
  - What happens: for Partek exports, Start/Stop/Length/transl_table are counted as samples (16 instead of 12 for tibialis). The genomic coordinates also corrupt the profile: max = 2.6e8, and the integer fraction and median are skewed.
  - Duplicated-ID check: it reported 18,897 duplicated feature IDs because it used Chromosome as the index. A prep script was needed.
