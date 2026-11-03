# HANDBACK: PMID 39393048 / GSE267512 (sonnet, case-spec route)

STATUS: finished (decision_status valid, execution completed, validator 0 errors, route paper_aligned)

## What ran
- Paper (PMC12456396): 12-week resistance training in 27 untrained pre-menopausal females, vastus lateralis biopsies PRE/POST. RNA-seq (Kallisto, TruSeq Ribo-Zero), DESeq2 `Genes ~ ID + timepoint`, FDR < 0.05, no fold-change cutoff (S2.14.p6, S2.14.p7). Paper result: 214 DEGs, 122 up, 92 down (S3.6.p1, FIG7). Paper also filtered genes with mean <= 10 reads (14,979 retained, S2.12.6.p1).
- Matrix: `GSE267512_GeneCounts_RAW_DATA.csv.gz`, 40,514 genes x 57 samples, all integer (rounded Kallisto estimated counts). `3col.tsv.gz` is the same data in long format and was not used.
- Alignment: matrix columns equal GEO `title` exactly (57/57). `subject` = first 4 letters of title (33 participants: 24 with both biopsies, 9 with one), `time` = PRE/POST suffix.
- Prep script `prep_filter.py`: mean count across samples > 10 (14,828 genes kept).
- Primary: pydeseq2 `~ subject + time`, POST vs PRE, all 57 samples (31 PRE, 26 POST). Sensitivity: same model on the 24 complete pairs (48 samples).
- Enrichment: not run. The paper uses ChEA3 TF enrichment (not available in the executors) and reports no GO/KEGG/GSEA.
- Threshold: padj < 0.05, no effect cutoff (paper). Audit rule padj < 0.05 and |log2FC| > log2(1.5) gives 48 genes.

## DEG counts vs paper (padj < 0.05)
| table | ours | up/down | paper |
|---|---|---|---|
| time_POST_vs_PRE (primary) | 218 | 126 / 92 | 214 (122 / 92) |
| time_POST_vs_PRE_pairs_only (sensitivity) | 217 | 125 / 92 | - |

## Deviations (declared)
- Sample set: GEO has 31 PRE / 26 POST (57); the paper figure legend states 35 pre / 27 post (62). 4 PRE and 1 POST biopsies are not deposited.
- Gene filter: paper text says "mean <= 10 RPM" removed, but a mean RPM > 10 rule keeps only 6,084 genes; a mean raw count > 10 rule keeps 14,828, close to the paper's 14,979, so the count-scale filter was used.
- pydeseq2 Wald instead of R DESeq2.
- Paper reports no DEG gene list in the main text, so no named-gene comparison was possible.

## Tool problems
None blocking. Minor: `case_runner inspect` reports an error entry for `GSE267512_3col.tsv.gz` (long format, "must contain at least two numeric sample columns"), which is expected for a long-format table but gives no hint to pivot it.
