# HANDBACK: PMID36695573 (GSE198826, GSE198827)

Paper: LSD1 defines the fiber type-selective responsiveness to environmental stress in skeletal muscle (PMC9876571). SuperSeries GSE198911 (S12.p1).

## Outcome: refused (both cases, at the design gate)

| Case | What it holds | Paper's DE analysis | Decision |
|---|---|---|---|
| GSE198826 | 16 Dex-treated samples: gastrocnemius and soleus, WT 3 vs LSD1-mKO 5 each (featureCounts raw counts) | edgeR mKO vs WT, FDR < 0.05; Gas 150 up / 117 down (S2.3.p1, S4.10.p1) | refused: no exercise factor (all samples dexamethasone-treated, sedentary) |
| GSE198827 | 6 soleus samples, all VWR-trained: WT 3 vs LSD1-mKO 3 (estimated counts) | DESeq2, then top 1000 MAD genes (mean TPM > 1) with k-means; no DEG count or significance threshold (S2.6.p1, S4.10.p1) | refused: exercise is constant; there is no sedentary RNA-seq arm |

The only exercise experiment in the paper is voluntary wheel running (S2.5, S4.4). Exercise vs sedentary appears only in phenotype and qPCR data (Fig 4B; Fig 5, figure supplement 1A). The RNA-seq covers trained mice only, so the one contrast available is genotype with exercise held constant. A genotype contrast does not tell us how exercise affects gene expression, and the exercise x genotype interaction cannot be estimated.

## What ran

- `inspect` on both series. Data were already cached.
- `prep/prep_GSE198826_counts.py` merges the Gas and Sol featureCounts files. It skips the `#` command line and renames BAM-path columns to the library labels (araki1, a1, ...) found in brackets in the GEO titles. Output: `prep/GSE198826_counts_merged.csv` (24421 x 16).
- `case_runner execute case_spec.json`. Gates recorded: paper_reconstruction, ownership, alignment, matrix, design (refused).
  - Alignment: exact match on a derived key, 16/16 and 6/6.
  - Suitability: "analyzable" for the genotype comparisons only. This verdict does not affect the refusal.
  - The validator ran on 10 records with 0 errors.
- No DE executions and no enrichment were run.

## DEG counts vs paper

None computed, because both cases were refused before execution.
- Paper threshold for Dex (GSE198826): FDR < 0.05 with no fold-change cutoff. Paper count for Gas: 267 (150 up / 117 down).
- Paper threshold for VWR (GSE198827): none. The paper ranks genes by MAD instead of applying a threshold.

## Deviations

- The GSE198826 matrix had to be rebuilt by a prep script (listed in `prep_scripts`) because the deposited file has a featureCounts comment header. It was not modelled, since the case was refused.
- GSE198827 matrix type was recorded as estimated counts with medium confidence. Column sums are 8.9-13.8 M and 14% of non-zero values are fractional.

## Tool problems

1. `inspect` cannot read featureCounts output that starts with a `#` comment line. `tools/native.py:217` (`read_table` fallback `pd.read_csv(..., sep=None, engine="python")`) does not pass `comment="#"`. The whole file then reads as non-numeric, and `tools/analysis_policy.py:46` raises "must contain at least two numeric sample columns; found 0... may be metadata". The message is misleading. Both `GSE198826_counts_*.txt.gz` files were affected, and a prep script was needed.
2. Minor: the deposited matrices contain Excel-mangled gene symbols (`1-Mar`, `2-Sep`, ...). `inspect` flags them correctly. This is a data problem, not a tool problem, and it does not matter for a refusal.
