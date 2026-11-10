# HANDBACK: PMID35774589 / GSE198652

Paper: Muscle-Specific Cellular and Molecular Adaptations to Late-Life Voluntary Concurrent Exercise (PMC9233305).

## What ran

- Route: case spec (`case_spec.json`) through `python -m tools.case_runner execute`. Status: completed, validator found 17 records and 0 errors.
- Input: `GSE198652_Raw_gene_counts_matrix.txt.gz` (Partek/STAR gene counts, 23,011 genes x 34 samples). `prep_matrix.py` re-indexed it by the unique `Gene Symbol` column and wrote `prep/GSE198652_counts_by_symbol.csv`. The deposited first column is `Chromosome`.
- Alignment: matched on metadata `description` with `normalize_keys`, 34/34 samples. Two samples differ only in case (`Pow12_s` and `Pow15_p`).
- Matrix: estimated counts (74% integers, the rest fractional), rounded for DESeq2 (documented).
- Design: four separate two-group fits, PoWeR vs Sedentary, one per muscle x age stratum, as the paper describes (S2.8.p1, FIG7 A-H):
  - old soleus and old plantaris, 5 vs 4 each (primary);
  - young soleus and young plantaris, 4 vs 4 each (secondary; the re-analyzed Englund et al. cohort).
- Method: pydeseq2 Wald `~ grp`. Within each stratum, genes with a maximum count of 50 or less were dropped, matching the paper's and GEO's filter.
- Threshold: the paper's own rule, BH FDR < 0.10 with no fold-change cutoff (S2.10.p1, S2.8.p1). An audit count at FDR < 0.05 was also recorded.
- Enrichment: Enrichr ORA (GO + KEGG 2019) on up and down genes for the two old contrasts.

## DEG counts (FDR < 0.10; FDR < 0.05 audit in brackets)

| Contrast | n | up | down | paper |
|---|---|---|---|---|
| Old soleus PoW vs Sed | 1088 [775] | 509 | 579 | count only in Supp Table 2 (not available) |
| Old plantaris PoW vs Sed | 88 [62] | 61 | 27 | not available; paper says "very few" genes were down |
| Young soleus PoW vs Sed | 2601 [1764] | 1238 | 1363 | not available |
| Young plantaris PoW vs Sed | 668 [415] | 360 | 308 | not available |

## Named-gene check

- **Aldh1l1 and Lrrn1** (S3.7.p1): up in all four contrasts. Both pass FDR < 0.05 in three of the four. In old plantaris, Aldh1l1 has padj 0.086, which passes FDR < 0.10 but not the paper's stated FDR < 0.05.
- **Old soleus, genes the paper reports as up** (S3.8.p1): Agrn, Samd1 and Zfp598 are up and significant. Kat2a is up but only borderline (padj 0.056).
- **Old soleus, genes the paper reports as down**:
  - Gng5, Mylpf and Slc25a20 are down and significant.
  - "Ccnt", read as Ccnt1, is down but not significant (padj 0.60). The paper's symbol is ambiguous.
- Result: 9 of 10 named old-soleus genes agree. No gene goes in the opposite direction from the paper.

## Pathway check (qualitative, against FIG7)

- **Old soleus:** the up genes are enriched for KEGG "Pathways in cancer" (top term) and the down genes for oxidative phosphorylation and thermogenesis. Both match FIG7 B and D.
- **Old plantaris:** the up genes are enriched for Gap junction (top term), which matches FIG7F. The down genes have no KEGG term at adj p < 0.05, which matches FIG7H ("very few").

## Deviations

- pydeseq2 was used instead of Partek DESeq2, and the fractional counts were rounded.
- The max-count > 50 filter was applied within each stratum's samples. The paper's phrase "across all samples" does not say which sample set.
- Enrichment used Enrichr GO and KEGG 2019. The paper used gProfiler with KEGG, Reactome and WikiPathways.
- The young cohort's age is 4 mo at the start in the paper and 6 mo in the GEO tag (age at harvest). It was not treated as a problem.
- GEO titles call the aged plantaris samples "Aged Soleus". Tissue was taken from `source_name_ch1` and the `_p` suffix instead.

## Tool problems

- `tools/case_runner.py:393-399` and `tools/native.py:284` (inspect):
  - The matrix's first column was used as the feature ID. Here that column is `Chromosome`, so inspect reported `duplicated_feature_ids` 22989 and `feature_id_type` "entrez".
  - The unique `Gene Symbol` annotation column was ignored. A prep script was needed to re-index the matrix.
  - Inspect could detect a symbol-like annotation column and offer it as the index.
- `filter_low_counts.min_count` uses `>=` (`tools/case_runner.py:747`) and runs before rounding. A strict "max > 50" rule therefore needed `min_count: 50.0001`. A strict or max-count option would be cleaner.
