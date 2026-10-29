# Paper screening summary (2000 papers)

| Verdict | Papers |
|---|---:|
| excluded | 1885 |
| analyzable | 105 |
| needs_inspection | 10 |

## Why papers were excluded (first failing layer)

| Reason | Papers |
|---|---:|
| no_full_text | 628 |
| off_topic | 248 |
| no_exercise_contrast | 174 |
| no_own_deposit | 625 |
| data_on_request | 119 |
| non_geo_repository | 13 |
| unsupported_data_type | 36 |
| unsupported_organism | 19 |
| no_processed_matrix | 6 |
| de_tables_only | 3 |
| single_group | 7 |
| group_too_small | 7 |

## Why papers need inspection

| Reason | Papers |
|---|---:|
| matrix_unlabelled_matrix | 4 |
| shared_gse | 4 |
| matrix_decimal_unexplained | 1 |
| error | 1 |

13 analyzable papers have their raw counts only inside a _RAW.tar.

## Verdicts by source

| Source | Papers | analyzable | needs_inspection |
|---|---:|---:|---:|
| geo | 409 | 104 | 9 |
| pubmed | 1591 | 1 | 1 |

## Data types of the papers' own GEO series

| Data type | Papers |
|---|---:|
| rnaseq | 155 |
| microarray | 28 |
| scrnaseq | 21 |
| methylation | 10 |
| chromatin | 6 |
| rnaseq+methylation | 6 |
| rnaseq+chromatin | 5 |
| microarray+chromatin | 1 |
| not_public | 1 |
| rnaseq+ncrna_seq | 1 |
| microarray+methylation | 1 |

## Analysable papers by route

| Route | Papers |
|---|---:|
| counts | 69 |
| limma | 35 |
| limma;counts | 1 |

## Checks for the analysable papers

| Flag | Papers |
|---|---:|
| sex:all_female | 3 |
| sex:all_male | 26 |
| sex:mixed | 6 |
| sex:unknown | 70 |
| small_groups | 5 |

## What each data type needs

| Data type | Needed |
|---|---|
| bulk RNA-seq, counts (DESeq2/edgeR/limma-voom) | genes x samples raw count matrix, or one count table per sample (featureCounts/HTSeq/STAR, RSEM expected_count, salmon NumReads); sample groups; sex per sample or X/Y genes in the matrix |
| bulk RNA-seq, TPM/FPKM/log (limma) | genes x samples TPM/FPKM/CPM or log matrix; sample groups; sex per sample or X/Y genes in the matrix |
| microarray (not routed) | normalised log expression matrix (series matrix or CEL files) with the platform annotation; sample groups; sex |
| single-cell (not routed) | raw UMI counts per cell with a cell-to-sample map, for pseudobulk; sample groups; sex |
| methylation (not routed) | beta or M values per CpG; sample groups; sex |
