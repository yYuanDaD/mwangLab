# HANDBACK: GSE164890 (PMC9027771, elite speed skaters, whole blood before/after exercise at altitude)

## What ran
- Route: case spec (`case_spec.json`) through `python -m tools.case_runner execute`; validator: 12 records, 0 errors; status completed, route `paper_aligned`.
- Matrix: `GSE164890_rsem.genes.counts.tsv.gz` (RSEM expected counts, 94.5% integer, 58,233 genes x 14 samples), rounded to integers (`transform: round`, documented).
- Alignment: exact on GEO `description` (14/14). `subject` (S1-S7) and `time` (pre/post) parsed from the key.
- Design: paired, 7 donors x pre/post. DESeq2 (pydeseq2 Wald), `~ subject + time`, post vs pre. This is the paper's "donor + exercise" design (S2.5.p1, FIG1).
- Threshold: paper's FDR < 0.1, no fold-change cutoff (S2.5.p1, FIG1). Audit rule: padj < 0.05.
- Enrichment: Hallmark preranked GSEA (stat ranking) plus Enrichr ORA (GO/KEGG). The paper used Hallmark + MSigDB CP with clusterProfiler/fGSEA; the CP collection was not available, so it was not run.

## DEG counts vs the paper (FDR < 0.1)
| Contrast | Ours (up / down / total) | Paper (up / down / total) |
|---|---|---|
| post vs pre, paired | 2588 / 1655 / 4243 | 2516 / 1542 / 4058 (S3.2.p2) |

- Audit at padj < 0.05: 3238 DEGs.
- More than twofold (unshrunk LFC, among FDR < 0.1): 131 up / 93 down. Paper: 104 / 58 (S3.2.p2; the paper's LFC estimator is unknown).
- Named genes, all significant in the paper's direction:
  - MARC1 (ENSG00000186205): LFC +1.23, padj 1e-7
  - PHOSPHO1: +0.54, padj 0.004
  - PPBP: +0.53, padj 1e-4
  - MYC: -0.36, padj 0.004
  - TP53: -0.27, padj 0.029
- GSEA agrees with the paper's FIG2:
  - Up: TNFa/NF-kB, complement, inflammatory, apoptosis, IFN-gamma/alpha, IL6/JAK/STAT3, hypoxia and coagulation, all at FDR ~0.
  - Down: HALLMARK_MYC_TARGETS_V2 is the only strongly significant down set (NES -2.45, FDR 0), as the paper reports.

## Deviations
- RSEM expected counts were rounded before DESeq2. The paper does not state how it handled them.
- pydeseq2 was used instead of R DESeq2 v1.18.1. Differences in dispersion and independent filtering likely explain the roughly 5% higher DEG count.
- The paper's altitude-specific filtering against 7 public microarray datasets (S3.5) and its scRNA-based cell-type deconvolution (S3.4) were not reproduced; they are outside the DE route.
- The estimand is exercise at altitude (pre vs post). There is no sea-level arm, so no altitude effect can be estimated (S3.5.p1).

## Tool problems
- `tools/case_runner.py:422-434` (`_gene_lookup`): for an Ensembl-indexed table it maps IDs to symbols through MyGene's *current* symbols. It does not use the matrix's own `Symbol` annotation column. As a result, the paper gene MARC1 (now named MTARC1) came back `null` even though ENSG00000186205 is present and strongly significant. Using the deposited annotation column, or adding alias lookup, would fix it.
- Related: the DEG result table (`results/time_post_vs_pre/DEG_results_post_vs_pre.csv`) keeps only `Gene_id` and drops the matrix's `Symbol`/`Gene_type` annotation columns. A reader has to rejoin them by hand.
