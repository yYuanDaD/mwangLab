# HANDBACK — PMID39393048 / GSE267512

**Status: finished** (case-spec route, `tools.case_runner execute`; run `completed`, contract validator 12 records, 0 errors).

## What ran
- Paper: 12-week resistance training in 27 untrained pre-menopausal females, vastus lateralis biopsies at PRE and POST. Method: DESeq2 `~ ID + timepoint`, FDR < 0.05 with no fold-change cutoff (S2.14.p6–p7). Result: 214 DEGs, 122 up and 92 down (S3.6.p1, Fig 7).
- Data: `GSE267512_GeneCounts_RAW_DATA.csv.gz`. These are Kallisto gene counts deposited as integers, 40,514 genes × 57 samples (31 PRE, 26 POST). They come from 33 participants: 24 complete pairs, 7 with only PRE, 2 with only POST. Samples were aligned exactly on `title` (57/57). `subject` and `time` were taken from the title and the treatment field.
- Gene filter: I used the authors' GitHub script (`rowMeans(counts) >= 10`), implemented in `prep_filter_meancount.py`. It keeps 14,830 genes; the paper kept 14,979.
- Model: pydeseq2 Wald `~ subject + time`, POST vs PRE, with subject as a blocking factor. Suitability verdict: analyzable.

| table | role | DEGs (padj < 0.05) | up / down | paper |
|---|---|---|---|---|
| time_POST_vs_PRE (alpha 0.1, all 57 samples) | primary | 211 | 119 / 92 | 214 (122 / 92) |
| time_POST_vs_PRE_alpha005 (independent-filter alpha 0.05) | sensitivity | 218 | 126 / 92 | 214 |
| time_POST_vs_PRE_pairs_only (24 complete pairs, 48 samples) | sensitivity | 213 | 121 / 92 | 214 |

The genes the paper names match closely (primary table; full list in `paper_gene_lookup_by_symbol.csv`):

| gene | log2FC | our FDR | paper FDR |
|---|---|---|---|
| RPS6KC1 | +0.19 | 0.0101 | < 0.01 (up 11%) |
| TRIM63 | | 0.685 | 0.688 |
| FBXO32 | | 0.765 | 0.757 |
| TRAF6 | | 0.441 | 0.443 |
| FOXO1 | | 0.428 | 0.430 |
| FOXO3 | | 0.266 | 0.268 |
| AR | | 0.954 | 0.956 |

## Deviations (declared)
- **Sample set:** GEO has 57 samples; the paper used 35 PRE and 27 POST. All deposited samples were kept, because the paper's model also included the unpaired ones.
- **Gene filter:** the paper's text says "≤ 10 RPM removed (63%)". Taken literally, that rule keeps only 6,084 genes and removes 85%, which contradicts the paper's own 63%. The authors' code uses `rowMeans(counts) >= 10`. That rule removes 63.4% of genes, so I applied it.
- **Software:** pydeseq2 instead of R DESeq2 1.32.
- **Independent filtering:** the primary run uses alpha 0.1, which is R's `results()` default and what the authors' script relied on. Alpha 0.05 is the sensitivity run.
- **Not reproduced:** the ChEA3 transcription-factor enrichment (no executor for it) and the gene association with testosterone (no hormone values in GEO). No GO/GSEA enrichment was run, because the paper reports none.

## Tool problems
1. **`complete_pairs` crashes:** the call at `tools/case_runner.py:607` passes `subject` and `condition` positionally to `native.complete_pairs_subset`. That function (`tools/native.py:672`) takes keyword-only `subject_column`, `condition_column` and `levels`, so the run fails with `TypeError: complete_pairs_subset() takes 3 positional arguments but 6 were given`. Workaround: I listed the 24 complete-pair subjects in an explicit `subset`.
2. **Gene lookup returns null:** `_gene_lookup` (`tools/case_runner.py:400`) matches paper genes only against the DEG table's index. Here the index is Ensembl IDs, and the matrix's `SYMBOL` annotation column is dropped before the DEG output, so every `paper_genes` lookup came back null. I did the lookup by symbol by hand (`paper_gene_lookup_by_symbol.csv`).
3. **Minor:** the inspect output shows mojibake in GEO `treatment_protocol_ch1` ("23.5 卤 4.8" for "±"), a GBK decode of the metadata text. It is cosmetic.
