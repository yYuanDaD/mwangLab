# Paper screening summary (199 papers)

| Verdict | Papers |
|---|---:|
| excluded | 166 |
| analyzable | 22 |
| needs_inspection | 11 |

## Why papers were excluded (first failing layer)

| Reason | Papers |
|---|---:|
| no_full_text | 1 |
| off_topic | 101 |
| no_exercise_contrast | 42 |
| unsupported_data_type | 7 |
| unsupported_organism | 9 |
| no_processed_matrix | 4 |
| group_too_small | 2 |

## Why papers need inspection

| Reason | Papers |
|---|---:|
| matrix_unlabelled_matrix | 5 |
| shared_gse | 4 |
| matrix_decimal_unexplained | 1 |
| matrix_raw_tar | 1 |

2 analyzable papers have their raw counts only inside a _RAW.tar.

## Data types of the papers' own GEO series

| Data type | Papers |
|---|---:|
| rnaseq | 47 |
| scrnaseq | 9 |
| chromatin | 2 |
| methylation | 1 |
| microarray | 1 |
| not_public | 1 |
| rnaseq+genome_variation | 1 |
| rnaseq+chromatin | 1 |
| other | 1 |

## Analysable papers by route

| Route | Papers |
|---|---:|
| counts | 14 |
| limma | 7 |
| limma;counts | 1 |

## Checks for the analysable papers

| Flag | Papers |
|---|---:|
| female_arms_below_3 | 3 |
| sex:all_male | 2 |
| sex:mixed | 7 |
| sex:unknown | 13 |
| small_groups | 2 |

## What each data type needs

| Data type | Needed |
|---|---|
| bulk RNA-seq, counts (DESeq2/edgeR/limma-voom) | genes x samples raw count matrix, or one count table per sample (featureCounts/HTSeq/STAR, RSEM expected_count, salmon NumReads); sample groups; sex per sample or X/Y genes in the matrix |
| bulk RNA-seq, TPM/FPKM/log (limma) | genes x samples TPM/FPKM/CPM or log matrix; sample groups; sex per sample or X/Y genes in the matrix |
| microarray (not routed) | normalised log expression matrix (series matrix or CEL files) with the platform annotation; sample groups; sex |
| single-cell (not routed) | raw UMI counts per cell with a cell-to-sample map, for pseudobulk; sample groups; sex |
| methylation (not routed) | beta or M values per CpG; sample groups; sex |
