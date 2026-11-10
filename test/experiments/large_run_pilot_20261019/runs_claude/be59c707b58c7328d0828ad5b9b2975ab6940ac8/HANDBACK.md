# HANDBACK: GSE229755 (PMC10318136, chronic exercise and mouse liver)

## What ran
- `case_runner inspect GSE229755`: GEO holds only `GSE229755_RAW.tar` with 12 per-sample files (`GSM*_Con_L1..6`, `GSM*_Exe_L1..6`). Each file has one value column, `fpkm_<title>`, plus Entrez `gene_id` and `gene_symbol`. No read counts are deposited.
- `prep_merge_fpkm.py` (listed in `prep_scripts`) merged the 12 FPKM files into `data/GSE229755/GSE229755_fpkm_merged.csv`: 16,821 genes x 12 GSM columns, indexed by symbol, with duplicate symbols resolved by highest mean.
- `case_runner execute case_spec.json`: completed. The validator checked 13 records and found 0 errors.
  - Alignment: exact match on the metadata index, 12/12 samples.
  - Groups: grp from title, Con 6, Exe 6. Suitability verdict: analyzable.
  - Primary: limma-trend on log2(FPKM+1), `~ grp`, Exe vs Con. Genes kept only if FPKM >= 1 in at least 3 samples (10,558 genes).
  - Sensitivity: the same model without the filter (16,804 genes).
  - Enrichment: Hallmark GSEA on the primary table completed. ORA was not run because there were 0 DEGs.

## DEG counts vs paper
Paper threshold (S2.4.p1, S3.1.p1): Q-value <= 0.05 and |log2FC| > 1. The paper reports 88 DEGs (28 up, 60 down) from DESeq on counts.

| Table | Ours, paper rule | Ours, BH < 0.05 only | Paper |
|---|---|---|---|
| grp_Exe_vs_Con (primary, filtered) | 0 | 0 | 88 (28 up / 60 down) |
| grp_Exe_vs_Con_unfiltered (sensitivity) | 0 | 0 | 88 |

- In the primary table the smallest BH-adjusted p is 0.58. 645 genes have nominal p < 0.05, and 6 genes pass nominal p < 0.05 with |log2FC| > 1.
- Named genes:
  - Cyp4a10 is up, log2FC 1.17, p = 0.0012, padj 0.69.
  - Cyp4a14 is up, log2FC 2.13, p = 0.0018, padj 0.73.
  - Both have the same direction as the paper, but neither survives FDR.
  - Cyp1a1 was removed by the expression filter (FPKM < 1 in most samples). In the unfiltered table it is log2FC +0.39, p = 0.20.
- Sample correlations on log2 FPKM are uniformly 0.98–0.99. There is no outlier and no visible group separation.

## Deviations
- The paper's route is blocked: DESeq on read counts needs counts, and GEO deposits only FPKM. The run used limma-trend on log2(FPKM+1) instead, recorded as a declared deviation with `threshold_source: paper_on_deviation_route`. FPKM was not rounded into counts.
- An FPKM >= 1 in at least 3 samples filter stands in for DESeq's independent filtering. This is my choice; the unfiltered run is kept as a sensitivity check.
- "Q-value" is read as BH-adjusted p.
- GEO data_processing also mentions Bowtie2 and "Assembly: mm10", while the paper says GRCm39. This was recorded as a discrepancy and did not block the run.
- Only the transcriptome was analyzed. The proteomics deposit (PXD041538) and the metabolomics deposit (MTBLS7609) were not.

## Tool problems
- `tools/omics_semantics.py:33-49` (`choose_count_column`): integer ID columns (`st_gene_id`, `gene_id`) are counted as numeric value candidates. Every tar member was therefore reported as `count_column_ambiguous`.
  - Failing closed is correct here, because the files are FPKM.
  - However, the inspect note ("no mergeable per-sample count files") does not say the members hold FPKM.
  - There is no tar-merge path for per-sample FPKM files, so a prep script was needed.
- No other failures.
