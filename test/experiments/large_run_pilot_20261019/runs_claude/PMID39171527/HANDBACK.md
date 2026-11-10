# HANDBACK: PMID39171527 / GSE269016

## What ran
- Case spec route (`case_spec.json`); `python -m tools.case_runner execute` finished with status `completed` and 0 validator errors (12 records).
- Input: `GSE269016_raw_counts.txt.gz`. `prep_matrix.py` keeps the 12 `read_count_*` columns (RSEM expected counts), drops the `fpkm_*` columns, uses `gene_symbol` as the index (17,432 genes, all unique, none missing) and strips the `read_count_` prefix. Output: `GSE269016_read_counts_by_symbol.csv`.
- Alignment: the key comes from the GEO title code (`Liver, Sedentary 1(S1)` gives `S1`) and is matched exactly. 12 of 12 samples aligned: SED 6, EX 6.
- Matrix: estimated counts (RSEM v1.3.1, about 68% integer values). The method is DESeq2 (pydeseq2 Wald, `~ grp`) on rounded counts (`rounding_documented`).
- Design: postprandial single-bout exercise vs sedentary, wild-type male liver, two independent arms, no blocking (S4.3.p2, S2.3.p1). The suitability verdict is analyzable.
- Enrichment: ORA (GO and KEGG via Enrichr) and GSEA (Hallmark) both completed.

## DEG counts vs paper
- Paper threshold: none is stated for the transcriptome. S4.13.p1 says only "as described previously (27)" plus KEGG via BGI Dr.Tom. The P < 0.05 t-test rule in S4.14.p1 is for the bench assays. Because of this, `threshold_source = workflow_default` (BH padj < 0.05, no effect-size cutoff).
- grp_EX_vs_SED: 5,170 DEGs (2,569 up, 2,601 down). With the audit rule (padj < 0.05 and |log2FC| > 1) there are 626. The paper gives no DEG count, so the counts cannot be compared.
- Paper genes all go the same direction as the paper:
  - Angptl8: log2FC −2.65, padj ≈ 0 (paper: exercise suppresses it).
  - Angptl4: +1.64 (paper: up in liver, Supp Fig 4C).
  - Cebpa: −0.54 (paper: regulated by exercise).
  - Angptl3: +0.27, padj 0.007.
- Paper pathway: the paper says hepatic insulin signaling was the most strongly regulated pathway (S2.3.p1). In our KEGG ORA, "Insulin signaling pathway" (padj 7.4e-5) and "Insulin resistance" rank 4th and 5th, behind AMPK, FoxO and Longevity, which are also insulin-related. This is consistent with the paper but not an exact top-1 match.

## Deviations
- The paper does not state its DE method or threshold. DESeq2 on rounded RSEM counts and the workflow-default threshold are workflow choices (route `declared_deviation`).
- The `fpkm_*` columns in the same file were not used.

## Tool problems
- There is no spec option to choose an annotation column (`gene_symbol`) as the feature ID, or to select only some of a file's sample columns. The matrix index defaults to `st_gene_id` (`G10090_*`, feature_id_type "other"), which would block enrichment. Because of this a prep script was needed. The inspect report also lists annotation columns as dropped without offering a replacement (tools/case_runner.py:383).
- `inspect` profiles the read_count and fpkm columns together: 24 "samples" against 12 metadata rows, integer_fraction 0.41. It finds no alignment keys because of the `read_count_` prefix. This is minor, and `matrix_column_pattern` could cover the prefix.
- gseapy warning: 5.92% duplicated values in the preranked stats. This is benign.
