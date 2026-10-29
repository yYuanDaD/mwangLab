# HANDBACK: PMID41775886 / GSE297515

Paper: Piezo1-dependent activation of stromal cells ignites muscle inflammation in exercise and injury (PMC13007780).
Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. The run completed and the validator passed (40 records, 0 errors).

## What ran

GSE297515 is a SuperSeries-like deposit with 90 samples (sorted MmSCs, whole muscle, heart, liver; exercise, CTX injury, Yoda1 culture). There are three exercise experiments, so I set them up as three cases on the same accession. In each case I excluded the samples from the other sub-series, with a reason recorded per sample.

| Case | Paper figure | Samples | Model | Paper threshold | Our DEGs (applied) | Audit |
|---|---|---|---|---|---|---|
| GSE297515_AEX | Fig.1c, AEX d1 vs SED, MmSC | 3 vs 3 | DESeq2 ~ grp, LFC shrink | padj<0.05 and abs(log2FC)>=1 | 226 (124 up / 102 down) | 449 at padj<0.05 alone |
| GSE297515_EXT | Fig.1k, 2-wk wheel EXT vs SED, MmSC | 3 vs 3 | DESeq2 ~ grp | padj<0.05 and abs(log2FC)>=1 | 53 (33/20) | 226 |
| GSE297515_PIEZO_AEX | Fig.4e, AEX vs SED within WT | 3 vs 3 | DESeq2 ~ cond (WT subset) | padj<0.05 | 502 (255/247) | 202 with abs(log2FC)>=1 |
| same | Fig.4e, AEX vs SED within Piezo1 cKO (FL) | 3 vs 3 | DESeq2 ~ cond (FL subset) | padj<0.05 | 86 (61/25) | 55 |

Additional runs:
- Sensitivity, AEX case: an additive sex term (~ sex + grp) gives 226 to 213 DEGs. The samples are mixed sex, 2F/1M per arm, inferred from X/Y genes. GEO has no sex field, so I recoded sex per title from the suitability sex check.
- Exploratory, AEX case: females only (2 vs 2) gives 138 DEGs. I did not run males, because 1 vs 1 leaves no residual df.
- Exploratory, Piezo case: one joint ~cell DESeq2 model fitted on all 12 samples.
  - AEX vs SED: WT 471, FL 80.
  - FL vs WT: 53 at SED, 3 at AEX.
  - AEX x genotype interaction: 10.
- Enrichment: ORA (Enrichr GO and KEGG) and GSEA Hallmark all completed, on AEX, EXT and the WT-within AEX table. I kept these separate from the DE results.

## Vs paper

The paper gives no numeric DEG counts in its text or legends. Volcano and cluster sizes appear only in the figures, so `paper_counts` is empty and I compared named genes instead.
- **Fig.1c:** every highlighted gene is significant and up (padj<=0.013, log2FC 2.5 to 7.0): Tnc (the top gene, log2FC 7.0), Ccn4, Postn, Timp1, F2rl1, Ccl2, Ccl7.
- **Fig.1k:** Cxcl5, H19 and Bdnf are all significant and up (log2FC 1.2 to 1.6). The paper says EXT changes fewer genes than AEX; our counts agree (53 vs 226).
- **Fig.4e:**
  - WT: 13 of the 14 named genes are significant at padj<0.05 (Cx3cl1, Cxcl5, Tnc, Timp1, Rplp0, Rps6, Eef1d, Eif3i, Gapdh, Pgam1, Eno1, Pkm, Mdh2). The exception is Cs (padj 0.051).
  - Piezo1 cKO: none of the 14 is significant.
  - This matches the paper's claim that the cKO shows impaired induction of "hundreds of genes" (502 DEGs in WT vs 86 in cKO).

## Deviations

- **GEO label shift (data problem, handled):** in GSM8993745 to GSM8993756, the genotype and treatment characteristics are shifted by one sample relative to the titles.
  - Examples: the sample titled WT_AEXd1#1 is labelled SED; WT_SED#1, listed last, is labelled FLOXED/AEX.
  - The titles equal the matrix column names and agree with Tnc and Timp1 induction, so I took the groups from the titles. This is recorded as a discrepancy and as a rejected candidate in the alignment gate.
- **DESeq2 implementation:** I used pydeseq2 instead of R DESeq2, with pydeseq2's lfc_shrink standing in for apeglm.
- **Low-count filter:** I implemented the paper's rule ("<10 reads within any condition removed") in `prep/filter_low_counts.py`. My reading: keep a gene when any condition sums to 10 reads or more.
- **Replicate QC:** the paper removes replicates with r<0.9. Every within-group r was 0.95 or higher, so none were removed.
- **Fold-change wording:** the legends say |FC| >= 2, which I applied; S2.1.p2 says |FC| > 2.
- **Fig.4e fit:** the paper does not say whether the two genotypes were fitted separately. I used separate per-genotype fits for the planned contrasts and the joint model as exploratory; their counts are close (502/86 vs 471/80).
- **Out of scope:** Fig.4a/b (genotype at steady state), Fig.5 (CTX injury), Yoda1 culture, and heart/liver samples are not exercise estimands. The only exception is the exploratory FL vs WT at SED inside the joint model.

## Tool problems

- `summary.csv` / finish record for the factorial case: `design_col` is filled with the design `formula` text, and `control` is empty. This happens when the design gate gives `formula` plus per-contrast `within` instead of a single `design_column`. The record is cosmetic, but it is misleading for the per-genotype subset contrasts.
- GEO metadata has no sex field. The suitability sex check (`tools/suitability.py:393` `check_sex`) infers sex but does not offer a derived column, so I hand-coded the per-title recode in the spec.
- There is no exact executor option for the paper's low-count rule. `filter_low_counts` is CPM-based, so I needed a prep script.
- Minor: the gseapy log warns about duplicated preranked stats (0.1 to 1.6% of genes).
