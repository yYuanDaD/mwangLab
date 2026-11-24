# HANDBACK — PMID36071599 / GSE211204

## What ran
- Paper: Monti et al., 10-d unilateral lower-limb suspension (ULLS) then 21-d resistance-exercise active recovery (AR), vastus lateralis biopsies from young men at LS0 / LS10 / AR21.
- Data: `GSE211204_RawCountFile_RSEM_genes.txt.gz`, RSEM expected counts. Feature IDs were re-keyed from `ENSG|SYMBOL` to symbols by `prep_feature_ids.py`; values are unchanged, and 1,733 rows whose symbol appears more than once kept their Ensembl IDs. 31 samples (11 subjects: 11 BL, 11 ULLS, 9 AR) aligned 31/31 by exact match on the `[S#]` key in the GEO title.
- Design: one model, `~ subject + time`, on all samples. Subject is a fixed blocking term, matching the paper's "adjusted for subject ID (paired)". Three pairwise contrasts as in Fig 4B–D. **The exercise contrast is AR vs ULLS** (primary).
- Method: limma-voom in R (`tools.r_de_tools:run_r_de`, engine voom). edgeR `filterByExpr` kept 23,336 of the 40,611 non-zero genes (the paper kept 20,555), then TMM, voom, lmFit and eBayes. The R versions are edgeR 4.10.7 / limma 3.67.3; the paper used edgeR 3.32.1 / limma 3.46.0.
- Threshold: the paper's own rule, q (BH FDR) < 0.05 with no fold-change cutoff (S3.3.p1). The audit rule is q < 0.01, which the paper also reports.
- Enrichment (exploratory): Hallmark GSEA on AR vs ULLS. The top sets were up with training: OXPHOS (NES 3.57), fatty-acid metabolism, adipogenesis and myogenesis. The paper's custom NMJ GSEA could not be reproduced.

## DEG counts vs paper (q < 0.05; q < 0.01 in brackets)
| Contrast | Ours (transcriptome-wide) | Paper (within 290 NMJ genes only) |
|---|---|---|
| LS10 vs LS0 (unloading) | 4,559 (2,370) | 95 (70) |
| AR21 vs LS10 (exercise) | 5,400 (3,088) | 114 (81) |
| AR21 vs LS0 | 734 (122) | 24 (7) |

The counts cannot be compared directly. The paper reports DE only within a 290-gene NMJ set built from 12 MSigDB v7.4 pathways (list in Data S1, not available here). The pattern does match: large changes at LS10, reversed at AR21, and little difference between AR21 and LS0.

Named genes go in the paper's directions (S3.3.p2, Fig 5):
- **COLQ:** −2.17 at LS10, +1.74 at AR vs LS10.
- **CHRNA1:** +2.34 at LS10, −2.24 at AR vs LS10.
- **CHRND:** +1.33 at LS10, −2.35 at AR vs LS10.
- All three are significant in both contrasts and none in AR vs LS0.
- GDNF and NTF4 are DE with unloading (the paper gives no direction for them).

## Deviations
1. TMM normalization instead of the paper's voom quantile normalization. The executor does not expose voom `normalize.method` (`tools/r_de.R:192`, `tools/r_de.R:214`).
2. Our DE universe is genome-wide; the paper's was the NMJ set. That is why route = `declared_deviation`.
3. Caveat for interpretation: AR vs ULLS mixes resistance training with spontaneous reloading after suspension. The study has no non-exercise recovery arm, so the "exercise effect" is training plus reloading.

## Tool problems
- The decision-contract validator requires `rounding_documented` for any count method on estimated counts. This includes voom, which takes fractional counts without rounding (rounding is only applied for deseq2/deseq1, `tools/r_de_tools.py:48,100`). The first execute failed at `tools/native.py:1127`. I set `rounding_documented: true` with a note saying no rounding was done.
- `tools/r_de.R`: the voom engine has no option for quantile normalization (see Deviation 1).
- The runner only gives `inspect` `feature_id_type: other` for the `ENSG.ver|SYMBOL` IDs and offers no built-in split, so a prep script was needed.
- The R run printed an unspecified `Warning message:`; only the first line is captured in `r_de_voom_paired_report.json`, so the warning text is lost.
