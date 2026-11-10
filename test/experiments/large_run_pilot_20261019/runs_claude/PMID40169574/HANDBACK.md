# HANDBACK: PMID40169574 / GSE269020

**Status: refused at `design`.** The sequenced samples contain no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE269020`: the series was downloaded into `E:/agent/mwangLab_pdf/data/GSE269020`. It has one matrix, `GSE269020_gene_fpkm.txt.gz`: 54,532 Ensembl genes by 8 samples.
- The case spec (`case_spec.json`) recorded these gates, and `execute` passed with 5 records and 0 validator errors:
  - `paper_reconstruction`
  - `ownership`
  - `alignment` (exact match on a key built from `title`, 8 of 8 samples)
  - `matrix` (FPKM)
  - `design` (refused)
- No DE executor or enrichment ran.

## Why refused
- The paper's RNA-seq covers iWAT from HFD-fed **sedentary** WT and KLF10^AKO male mice, n = 4 per group. Sources: S4.18.p1, the Fig. 5a legend ("without exercise") and DA.p1.
- In GEO, `treatment` is constant (HFD-fed) and `genotype` is Wildtype or KLF10AKO.
- The treadmill Ex vs Sed groups (Fig. 4, Fig. 5d-g) were measured only by physiology, RT-qPCR and western blot. They were never sequenced.
- The only estimable contrast is genetic (KO vs WT). It does not answer the exercise question, so it was not run as a substitute.

## DEG counts vs paper
- Paper, KLF10AKO vs WT: 2907 up and 1639 down (Fig. 5a, Padj < 0.05).
- The methods section (S4.18.p1) gives a different rule: padj <= 0.05 and |log2FC| >= 1 (edgeR, BH).
- Ours: not run, because there is no exercise contrast.

## Deviations
- None were executed.
- The paper's route could not have been reproduced anyway. It used edgeR on read counts, but only FPKM was deposited, so limma on log2(FPKM+1) would have been a declared deviation.
- The paper is inconsistent on the threshold: the Fig. 5a legend says Padj only, while S4.18.p1 adds |log2FC| >= 1.

## Tool problems
- None blocking.
- Minor: the metadata title (`WT-1`) and the matrix column (`WT_1`) differ only in separator. `inspect` reported `alignment_keys: []` rather than suggesting a `key_patterns` derivation. The fix was `key_patterns {"key": ["title", "^(WT|KO)-(\\d+)$"]}`.
