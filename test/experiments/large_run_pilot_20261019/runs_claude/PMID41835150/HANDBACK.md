# HANDBACK — PMID41835150 / GSE319603

Paper: *Transcriptomic insights into aerobic exercise-mediated attenuation of high-fat diet-induced muscle wasting* (PMC12982024).
Route: case spec (`case_spec.json`) -> `python -m tools.case_runner execute`. Status: **finished**, contract validator 14 records, 0 errors.

## What ran

- Data: `GSE319603_All_gene_counts.csv` (featureCounts raw integer counts, 26,166 Ensembl genes x 18 samples), mouse gastrocnemius, male.
  Groups C (chow) / H (HFD) / HM (HFD + 8-wk MICT), n = 6 each. The paper's fourth arm CM (chow + MICT) was not sequenced (S2.7.p1, FIG3).
- Alignment: exact match on the library name taken from GEO `description` ("Library name: C1"), 18/18.
- Design: one factor `grp`, three levels; independent animals, no blocking (no batch recorded).
- Primary: one DESeq2 model (pydeseq2 Wald, `~ grp`) on all 18 samples with planned contrasts
  - `grp_HM_vs_H`: the exercise effect under HFD (the paper's primary exercise contrast)
  - `grp_C_vs_H`: the paper's diet contrast H vs C, reported with reference H, so the sign is reversed
- Sensitivity: separate two-group DESeq2 fits (H+HM only; C+H only).
- Enrichment (HM vs H, joint model): Enrichr ORA (GO BP/MF/CC, KEGG 2019 Mouse) on the applied-threshold DEGs, plus a preranked GSEA on MSigDB Hallmark.

## Threshold

- Paper threshold (Results S3.2.p1): adjusted P < 0.05 and |log2FC| >= 0.5. This is the threshold applied here.
- Applied: padj < 0.05 and |log2FC| > 0.5. The runner has one `inclusive` flag for both parts, so the fold-change cutoff is strict. That only matters for a gene sitting exactly at 0.5.
- Audit: padj < 0.05 with no fold-change cutoff (the Methods S2.7.p1 rule).

## DEG counts vs paper (paper threshold)

| Contrast | Ours (joint model) | Ours (pairwise fit) | Paper |
|---|---|---|---|
| HM vs H (exercise) | 580 (212 up / 368 down) | 534 (191 / 343) | 563 (213 / 350) |
| H vs C (diet) | 458 (295 up / 163 down; reported as C vs H 163/295) | 476 (296 / 180) | 458 (295 / 163) |

Audit counts (padj < 0.05 only): 1320 for HM vs H and 885 for H vs C (joint model).

- Our log2FC values match the paper's Tables 1 and 2 to 4 decimals. Examples: Angptl7 -1.3563 vs -1.35633, Fbxo32 -1.1359 vs -1.13592, Trim63 -1.2879 vs -1.28789, BC048679 2.8103 vs 2.810305.
- The H vs C count is identical (458) to the paper's. Both point to the paper having used one DESeq2 model on all three groups, like our primary fit.
- The remaining +17 difference for HM vs H is most likely padj differences between pydeseq2 and R DESeq2 1.22.2 (independent filtering and dispersion).
- Paper genes:
  - MICT down-regulates Foxo1 (-1.36), Fbxo32, Trim63, Txnip, Pdk4, Angptl4 and Ucp3.
  - Pax7, Myod1 and Myog are not significant. This matches S3.5.p1 and S4.p8.
- Enrichment (separate from the DE result):
  - KEGG ORA: 23 terms with adjusted p < 0.05. They include Aldosterone synthesis, Insulin signaling, Cushing syndrome, FoxO, Glucagon, Ras, Prolactin, PI3K-Akt and Insulin resistance, overlapping the paper's top 15 (S3.4.p2).
  - GO BP: insulin-response terms.
  - GSEA Hallmark: oxidative phosphorylation, adipogenesis and fatty-acid metabolism, positive NES in HM vs H.

## Deviations

- pydeseq2 is used instead of R DESeq2 1.22.2. The paper does not state the model scope; the joint model is primary and the pairwise fits are sensitivity runs.
- ORA uses Enrichr libraries, not clusterProfiler, and its q-value rule differs from the paper's (q < 0.01 for GO, q < 0.05 for KEGG). GSEA Hallmark is an addition the paper did not run.
- The exercise effect can be estimated only under HFD (no CM samples). A diet x exercise interaction is not identifiable.

## Tool problems

- The threshold rule has one `inclusive` flag for both the p-value and fold-change cutoffs (`tools/native.py:762-768`, read through `tools/case_runner.py:406`). It cannot express a strict p-value with an inclusive fold change (the paper's "< 0.05 and >= 0.5"). The effect here is negligible.
- `paper_gene_check` in the execute summary rounds padj to 4 decimals, so very small padj values print as 0.0. This is cosmetic; the result tables keep full precision.
- Otherwise none: execute ran first time, with no spec errors and no executor failures.
