# HANDBACK — PMID36892893 / GSE213649

## What ran
- `case_runner inspect` then `case_runner execute case_spec.json` (final attempt; earlier attempts are in `_previous/`). Validator: 19 records, 0 errors. Status: completed, route `paper_aligned`.
- Data: `GSE213649_ang1_7_all_tissues_read_counts__1_.csv`: STAR raw integer counts, 32,545 Ensembl rat genes × 179 samples (5 tissues × 6 groups). Samples were aligned exactly on `title` (179/179).
- Design, following the paper (S2.4.3.2.p1): DESeq2 (pydeseq2 Wald) with `~ grp` (6 levels: CONSed, CONEx, LPSed, LPEx, LPASed, LPAEx), fitted separately for each tissue. The paper's planned contrasts are LPAEx vs each of the other 5 groups in each tissue (25 contrasts).
- LPAEx vs LPASed is the contrast that isolates exercise. Two exercise contrasts the paper does not report ran as exploratory analyses from the same fits: CONEx vs CONSed and LPEx vs LPSed.
- Sensitivity run `deseq2_LIV_noAE11`: liver refitted without L_AE11.
- Threshold (paper, S2.4.3.2.p1): BH FDR < 0.10 and |log2FC| > 1.0. The audit rule is padj < 0.05 with no fold-change cutoff.
- Enrichment: ORA on up-regulated genes (Enrichr GO and KEGG) and Hallmark GSEA, for PFC and liver LPAEx vs LPASed. The paper used Enrichr BioPlanet 2019, which is not available here.

## Sample QC decision (labelling fix before modelling)
A check of each sample against the per-tissue median profile (Spearman correlation) found that two columns labelled liver are other tissues:
- L_AE7 / GSM6591471 is colon (r = 0.94 to colon vs 0.72 to liver).
- L_PE4 / GSM6591458 is skeletal muscle (r = 0.96 to muscle vs 0.68 to liver).
- Neither is a byte-copy of another column.

Both are excluded. L_AE11 / GSM6591473 is liver with a colon component (r = 0.94 to liver vs about 0.98 for the other liver samples, and 0.75 to colon). It was kept in the primary run and dropped in the sensitivity run.

With all liver samples included, the liver LPAEx contrasts gave about 1,000–1,300 DEGs, nearly all higher in LPAEx. After the two exclusions the liver counts match the paper, so the authors probably dropped these samples too (they report n = 4–6 per group).

PFC_AE9, PFC_CS7 and HippoPS7 correlate slightly better with the other brain region. They were kept, because PFC and hippocampus have similar profiles.

## DEGs vs paper (FDR<0.10 & |LFC|>1; ours / paper)
| Tissue | vs LPASed (exercise) | vs LPSed | vs CONSed | vs CONEx | vs LPEx |
|---|---|---|---|---|---|
| PFC | 295 (246↑/49↓) / 317 (262/55) | 169 / 203 | 59 / 170 | 2 / 4 | 8 / 14 |
| Liver | 97 (91/6) / 112 (105/7) | 150 / 143 | 71 / 73 | 287 / 258 | 15 / 19 |
| Muscle | 4 / – | 6 / – | 7 / – | 22 (13/9) / 15 (9/6) | 0 / – |
| Hippocampus | 0 / – | 0 / – | 8 (1/7) / 19 (5/14) | 2 / – | 0 / – |
| Colon | 3 / – | 8 / – | 8 / – | 2 / – | 5 / – |

"–" means the paper says only "2–14" (S3.4.p1); those counts are in supplementary tables that are not available here. Our counts agree in direction with the paper: most DEGs are higher in LPAEx. The one large shortfall is PFC vs CONSed (59 vs 170).

Exploratory exercise-only contrasts (Ex vs Sed within one probiotic arm):

| Contrast | PFC | HIP | LIV | COL | MUS |
|---|---|---|---|---|---|
| CONEx vs CONSed | 4 | 25 | 2 | 7 | 2 |
| LPEx vs LPSed | 0 | 0 | 3 | 25 | 5 |

Exercise on its own changes little; the large PFC effect appears only within the LPA arm.

Gene checks: the paper's named Ensembl IDs that are present agree in sign. In PFC vs LPASed, ENSRNOG00000050660 has LFC −3.77 (paper: down). In liver vs LPASed, ENSRNOG00000037549 has LFC +5.9 (paper: up). Genes the paper names by symbol could not be looked up, because the matrix has Ensembl IDs only.

Liver sensitivity run (without L_AE11): the LPAEx contrasts fall to 2–13 DEGs (vs LPASed: 6). The paper's liver result for LPAEx ("inflammation", IL signalling) depends on this one partly colon-contaminated sample. This is recorded in the study caveats.

Enrichment (separate from the DE result):
- PFC up-regulated genes: ORA points to cytosolic calcium regulation, in line with the paper's "calcium signaling". GSEA top sets are angiogenesis and EMT.
- Liver: ORA gives cytokine and IL-6 production; GSEA gives IL6/JAK/STAT3, allograft rejection and inflammatory response. This agrees with the paper, with the L_AE11 caveat above.

## Deviations
- pydeseq2 instead of R DESeq2 4.1.2.
- Two mislabelled liver samples excluded; the paper does not state which samples it excluded.
- GO, KEGG and Hallmark instead of BioPlanet 2019.

## Tool problems
1. `tools/case_runner.py:588-594`: `alignment.exclude_samples` is matched only against the aligned metadata index (GSM ids). Keys given as the alignment `key_column` (here `title`) are silently ignored. The runner only stores `exclude_samples_not_aligned` in the result and prints nothing in the summary, so the first exclusion attempt ran with no samples excluded and still validated. It should accept `key_column` values or fail loudly.
2. `paper_gene_check` looks genes up by literal ID. On an Ensembl-ID matrix, every symbol the paper names returns null and no symbol→Ensembl mapping is tried.
3. Enrichment, PFC ORA: the GO_Biological_Process CSV header contains an HTML document (`<!doctype html>...`) as an extra column, apparently an Enrichr error page merged into the table. No KEGG file was written for PFC, and the run still reports ORA "completed". This is in `tools/enrichment_tools.py`; I did not locate the line.
4. The runner has no tissue-identity check. Sex is checked, but samples swapped between tissues in a multi-tissue series go undetected; this changed liver results about 10-fold.
