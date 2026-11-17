# HANDBACK: PMID 34252634 / GSE144133

Paper: Epigenetic rewiring of skeletal muscle enhancers after exercise training (PMC8355925). GSE144133 is the RNA-seq SubSeries of the SuperSeries GSE144134 that the paper names (S4.1.p1).

## What ran
- Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Status: completed, contract validator 13 records, 0 errors. Route label: `declared_deviation`.
- Design: 8 participants (P1-P8), vastus lateralis biopsies before and after 6 weeks of endurance training. P6_2 (GSM4281963) and P8_2 (GSM4281967) were excluded as the paper did for dermis contamination (S2.4.p1). That leaves 14 samples: 8 pre and 6 post, 6 complete pairs.
- Alignment: matrix columns `P1_1..P8_2` matched exactly to the title prefix (`key_patterns`); 16/16 matched.
- Matrix: deposited `GSE144133_abundance_full.csv.gz` (semicolon-delimited, 12,900 Ensembl genes; the paper reports 13,108 detected). I read it as **sleuth-normalized linear abundances, not counts**, for three reasons:
  - median-of-ratios size factors are 0.93-1.17;
  - variance/mean in the pre samples is 0.21-0.88 for means under 10, which is sub-Poisson;
  - only 1.3% of values are integers.
- Method: limma (moderated t) on log2(x+0.5), `~ subject + train`, contrast post vs pre. Pseudocount 0.5 matches sleuth's log(x+0.5). The paper's sleuth LRT is blocked because the kallisto bootstraps / abundance.h5 files were not deposited.
- Sensitivity run: the same model on the 6 complete pairs only (12 samples).
- Enrichment: ORA (Enrichr GO/KEGG) on the up genes, plus Hallmark GSEA on the full ranking.

## DEG counts vs paper (paper threshold FDR < 0.1, no fold-change cutoff; S3.1.p2, Fig 1C)
| contrast | ours (up/down) | paper (up/down) |
|---|---|---|
| post vs pre, 14 samples (primary) | 16 (16/0) | 817 (641/176) |
| post vs pre, 6 complete pairs (sensitivity) | 16 (16/0) | - |
| audit padj < 0.05 | 0 | - |

- Direction agrees with the paper. At raw p < 0.01 there are 494 genes, 464 of them up; the paper also reports mostly up-regulation.
- The qPCR-validated paper genes are all up with p of 4e-5 to 1.3e-3 (log2FC 0.8-2.1), but padj is 0.086-0.17:
  - padj < 0.1: FSCN1 (0.086) and COL4A2 (0.086);
  - padj 0.1-0.17: COL5A1, NID1, SLC9C1, RASSF2, EMILIN1.
- The gap is power: limma on 6 informative pairs (residual df 5) versus sleuth's LRT with bootstrap technical variance.
- GSEA themes agree with the paper's GO themes (ECM, immune, angiogenesis): EMT NES 2.52, coagulation 2.17, IFN-alpha/gamma, angiogenesis, IL6-JAK-STAT3, all at FDR ~0.
- ORA on 16 genes is thin: actin filament bundle assembly and extracellular structure organization.

## Deviations
1. sleuth LRT replaced by limma on log2(x+0.5) (bootstraps not deposited).
2. The paper's methods say "Bonferroni corrected q-values", but its results and Fig 1C say FDR < 0.1. I applied BH FDR < 0.1 and recorded this as a discrepancy.
3. Gene universe: 12,900 deposited genes vs 13,108 in the paper.
4. A first attempt read the matrix as estimated counts and ran round + DESeq2 (15 DEGs; baseMean around 1-5 for COL5A1/FSCN1). I rejected it after the variance/mean check. It is kept in `_previous/20261117T225607Z/` and recorded as a rejected matrix candidate.

## Tool problems
- `tools/native.py:268`: the matrix profile offers "linear_normalized ... or estimated_counts" with no dispersion check. The runner then accepted `transform: round` + DESeq2 on sub-Poisson normalized values and reported `deg_sanity: ok`. A variance/mean (or size-factor ~1) check would flag "not counts" before DESeq2.
- `tools/case_runner.py:654-655`: the method record and summary.csv store `transform: "log2(x+1)"` even when `pseudocount: 0.5` was applied. The real transform, log2(x+0.5), is visible only in the matrix values (min = -1).
- The `tools.limma_tools:run_limma_analysis` executor has no `trend=TRUE` option; with many low-abundance genes limma-trend would be a closer analogue of sleuth's mean-variance shrinkage. Not run.
