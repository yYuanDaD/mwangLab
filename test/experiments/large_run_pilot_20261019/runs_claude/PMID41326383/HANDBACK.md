# HANDBACK: PMID 41326383 / GSE302582

**Status: finished** (case `GSE302582`, route `paper_aligned`, decision contract validator: 16 records, 0 errors).

## What ran

- **Data:** I downloaded `GSE302582_RAW.tar` by hand (see tool problem 1). It holds 72 per-sample RSEM `genes.results` files. The runner merged the `expected_count` column into a 28,277 × 72 matrix, and I checked one value by hand (A1BG = 6.00 is `expected_count`, not TPM or FPKM). All 72 columns aligned exactly to the GSM ids.
- **Design** (from the paper: S2.1.p1, S2.2.p1-p2, S2.3.p1, S4.9.1.p1):
  - Parallel groups: MICE and SIE, 12 men each with RNA-seq.
  - Three biopsies per man: pre, +3 h (labelled +2.5h in GEO) and +24 h.
  - Participant numbers restart in each group, so the subject key is group plus number (24 subjects, 3 samples each).
- **Threshold:** the paper's rule, adjusted p < 0.05 with no fold-change cutoff (S4.10.p1). It was applied to every table.
- **Low-count filter:** CPM ≥ 1 in at least 12 samples of each fit. This keeps 12,955–13,509 genes, against the paper's 13,295 detected transcripts (S2.2.p1).
- **Executions:**
  - `deseq2_MICE` and `deseq2_SIE`: pydeseq2 on rounded RSEM counts, one model per group, `~ subject + time`. They give the within-group responses (h3 vs pre, h24 vs pre) plus h24 vs h3 as an exploratory comparison.
  - `limma_change_h3` and `limma_change_h24`: limma on per-participant changes in log2(CPM+1), formula `~ 0 + grp`. They give the SIE vs MICE difference in response (the group × time interaction), plus within-group limma responses as a sensitivity check.
  - `deseq2_between` (exploratory): cross-sectional SIE vs MICE at each timepoint, with no subject blocking.
- **Enrichment:**
  - ORA (up direction) on the +3 h interaction.
  - Hallmark GSEA on the +3 h interaction. This only stands in for the paper's GSEA: the paper used the 'mitostress' gene set (Quiros 2017), which is not available here.

## DEG counts vs the paper (padj < 0.05, no FC cutoff)

| Contrast | Ours | Paper |
|---|---|---|
| MICE +3h vs pre (DESeq2, subject-blocked) | 2421 (1342 up / 1079 down) | 1462 |
| SIE +3h vs pre | 2357 (1341 / 1016) | 1338 |
| MICE +24h vs pre | 7223 (3557 / 3666) | 5632 |
| SIE +24h vs pre | 5153 (2635 / 2518) | 3230 |
| SIE vs MICE response, +3h (limma paired change) | 102 (59 larger up in SIE / 43) | 207 (116 / 91) |
| SIE vs MICE response, +24h | 0 | 16 |

The pattern matches the paper:
- More DEGs at +24 h than at +3 h.
- MICE > SIE at +24 h.
- Group divergence mostly at +3 h.

**Sensitivity check:** limma within-group counts were 3525 / 3667 at +3 h and 6699 / 4007 at +24 h (MICE / SIE).

**Exploratory cross-sectional SIE vs MICE (DESeq2):** 0 at pre, 294 at +3 h, 74 at +24 h.

**Paper genes:**
- In the +3 h interaction, DDIT3 and HSPD1 rise more after SIE, as the paper reports (log2FC 0.56 and 0.42), but they are not significant (padj 0.19 and 0.23). HSPE1 and PPP1R15A are also not significant.
- In the cross-sectional +3 h comparison, DDIT3 (padj 0.018), HSPD1 (padj 0.0005) and HSPE1 (padj 0.013) are significant.
- In the SIE +3h vs pre comparison, all four genes are significantly up.
- So the paper's 207 may have been a between-group comparison at +3 h rather than a difference in change. This is recorded in the study caveats.

**Enrichment:**
- ORA on the SIE-larger-up genes gives heat acclimation, cellular response to heat and chaperone-mediated protein refolding (HSPA1A, HSPA1B, HSPA6, DNAJA4, BAG3). This matches the paper's protein-folding / UPR finding (Fig. 2B).
- Top Hallmark GSEA sets: MYOGENESIS (NES 1.76, FDR 0.03) and NOTCH_SIGNALING (NES 1.76, FDR 0.015).

## Deviations

- The paper says only "limma and DESeq2 ... following previously published guidelines". It gives no model, filter or package-to-result mapping, so the method is partly reconstructed.
- RSEM expected counts were rounded for DESeq2.
- I chose the CPM filter as a principled approximation, not to match the paper's count.
- The interaction uses limma on within-subject changes, not a DESeq2 interaction term. The runner's DESeq2 joint model (`~ covariates + cell`) cannot express subjects nested in group without becoming rank-deficient.
- pydeseq2 was used instead of R DESeq2.
- The paper's mitostress GSEA was not reproduced (gene set not available).

## Tool problems

1. **`tools/geo_tools.py:58-61`:** `download_supplementary_files` lists the series `suppl/` directory over HTTPS. NCBI returns 403 Forbidden for that listing, so `inspect` found no matrix. Meanwhile the SOFT file names `GSE302582_RAW.tar` directly, and fetching that URL worked (200). The tool should fall back to the `Series_supplementary_file` URLs.
2. **`tools/case_runner.py:871`:** `_tables` keys paired-change results by `r['name']` only and ignores `followup_level`. With `followup_levels: [h3, h24]` the h3 tables were silently overwritten by the h24 ones in the counts, comparison and enrichment records (both CSVs exist on disk). I worked around it with one execution per follow-up.
3. **Minor:** limma paired change on raw counts plus `filter_low_counts` writes `input/matrix_filtered_filtered.csv`, because `preprocess_counts`' own filter runs again after the runner's. No genes were lost here (13,509 → 13,509), but the double filter is implicit.
