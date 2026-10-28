# Paper screening summary (1000 papers)

| Verdict | Papers |
|---|---:|
| excluded | 862 |
| analyzable | 124 |
| needs_inspection | 14 |

## Why papers were excluded (first failing layer)

| Reason | Papers |
|---|---:|
| no_full_text | 162 |
| off_topic | 145 |
| no_exercise_contrast | 71 |
| no_own_deposit | 312 |
| data_on_request | 55 |
| non_geo_repository | 23 |
| unsupported_data_type | 54 |
| unsupported_organism | 13 |
| no_processed_matrix | 10 |
| de_tables_only | 2 |
| single_group | 6 |
| group_too_small | 9 |

## Why papers need inspection

| Reason | Papers |
|---|---:|
| shared_gse | 8 |
| matrix_unlabelled_matrix | 4 |
| matrix_decimal_unexplained | 2 |

17 analyzable papers have their raw counts only inside a _RAW.tar.

## Verdicts by source

| Source | Papers | analyzable | needs_inspection |
|---|---:|---:|---:|
| geo | 173 | 75 | 6 |
| pubmed | 378 | 20 | 4 |
| semantic_scholar | 449 | 29 | 4 |

## Data types of the papers' own GEO series

| Data type | Papers |
|---|---:|
| rnaseq | 179 |
| microarray | 43 |
| scrnaseq | 20 |
| methylation | 10 |
| chromatin | 8 |
| ncrna_seq | 8 |
| rnaseq+methylation+chromatin | 5 |
| ncrna_array | 4 |
| rnaseq+ncrna_seq | 4 |
| rnaseq+methylation | 3 |
| rnaseq+chromatin | 2 |
| rnaseq+ncrna_array | 1 |
| microarray+ncrna_array | 1 |
| other | 1 |
| scrnaseq+chromatin | 1 |

## Analysable papers by route

| Route | Papers |
|---|---:|
| counts | 84 |
| limma | 37 |
| limma;counts | 2 |
| counts;limma | 1 |

## Checks for the analysable papers

| Flag | Papers |
|---|---:|
| female_arms_below_3 | 1 |
| male_arms_below_3 | 2 |
| sex:all_female | 7 |
| sex:all_male | 19 |
| sex:mixed | 13 |
| sex:unknown | 85 |
| small_groups | 2 |
| unlabelled_samples | 2 |

## What each data type needs

| Data type | Needed |
|---|---|
| bulk RNA-seq, counts (DESeq2/edgeR/limma-voom) | genes x samples raw count matrix, or one count table per sample (featureCounts/HTSeq/STAR, RSEM expected_count, salmon NumReads); sample groups; sex per sample or X/Y genes in the matrix |
| bulk RNA-seq, TPM/FPKM/log (limma) | genes x samples TPM/FPKM/CPM or log matrix; sample groups; sex per sample or X/Y genes in the matrix |
| microarray (not routed) | normalised log expression matrix (series matrix or CEL files) with the platform annotation; sample groups; sex |
| single-cell (not routed) | raw UMI counts per cell with a cell-to-sample map, for pseudobulk; sample groups; sex |
| methylation (not routed) | beta or M values per CpG; sample groups; sex |
