# HANDBACK: PMID40695537 / GSE293163

## What ran
- Case spec route (`case_spec.json`, `python -m tools.case_runner execute`), run completed, decision-contract validator: 18 records, 0 errors. (Executed twice: the second run fixed the method record and added study caveats. The first attempt is in `_previous/`.)
- Data: `GSE293163_PBMC_raw_counts.txt.gz` (featureCounts integers, 62,754 Ensembl genes x 30 libraries). Aligned exactly on the library ID from the GEO title (30/30). Subject, time (Pre/Post) and age (Young/Old) come from the title: 7 Young + 8 Old participants, each with Pre and Post.
- DESeq2 (pydeseq2 Wald), one fit per contrast, as the paper describes (S4.2.p1 says the age groups were analysed separately):
  - `young_post_vs_pre`: `~ subject + time`, 7 complete pairs (primary)
  - `old_post_vs_pre`: `~ subject + time`, 8 complete pairs (primary)
  - `baseline_old_vs_young`: `~ age` on the Pre samples (secondary, associational)
  - Unpaired `~ time` sensitivity fits for Young and for Old
- Low-count filter: the paper drops genes with fewer than 5 reads in every sample. Here it is approximated per execution as CPM >= 0.4 in at least 1 sample (5 reads / 12.7M median library size).
- Enrichment: ORA (Enrichr GO/KEGG) and Hallmark GSEA on both exercise tables, all completed.

## Threshold
- Paper threshold (S2.8.p1): DEGs at p < 0.01 and FDR < 0.01, which is applied as padj < 0.01. The paper then keeps, for g:Profiler/IPA, only the genes whose log2FC is beyond the mean log2FC of their direction.
- S2.7.p2 states 5% FDR, which conflicts with S2.8.p1. It is used here as the audit rule (padj < 0.05).

## DEG counts vs paper
| Contrast | Ours padj<0.01 (up/down) | Ours padj<0.05 | Ours mean-LFC subset (MLE / shrunk) | Paper |
|---|---|---|---|---|
| Young Post vs Pre | 99 (97/2) | 179 | 44 (43/1) / 43 (42/1) | 53 (52/1), of 13,695 genes |
| Old Post vs Pre | 3,613 (1,195/2,418) | 5,740 | 1,301 (376/925) / 1,267 (386/881) | 1,026 (359 up / 572 down as printed) |
| Baseline Old vs Young | 1,589 (1,063/526) | 3,634 | 634 (459/175) / 639 (467/172) | 665 (446/199) |

- The paper's counts match our padj < 0.01 genes after its mean-log2FC subset step (the FIG1 legend colours genes ">mean Log2 fold-change"). The plain FDR rule overcounts by 2-3.5x. The runner's recorded counts are the plain rule. The subset comparison is recorded in the study caveats.
- Direction agrees with the paper:
  - Young is almost all up, with 1 down gene. That gene is SH2D3A (ENSG00000125731, log2FC -0.46, padj 0.004), exactly as the paper says.
  - Old is mostly down.
  - At baseline, Old has more genes up than down.
- Genes tested: Young 14,178 vs the paper's 13,695, close. Old 24,541 vs 19,101 and baseline 21,665 vs 19,762 are looser; the paper's filter or independent filtering probably differed.
- The unpaired Young fit gives 0 DEGs, so the paper's 53 implies a paired (subject-blocked) model. Unpaired Old gives 2,274.
- Young ORA reproduces the paper's NK-cell processes: Regulation of NK cell mediated immunity GO:0002715 and NK cell activation. Old ORA run on all 3,613 DEGs together has no GO BP term at FDR < 0.05; the paper ran up- and down-regulated genes separately. Old GSEA: protein secretion, OXPHOS and interferon/inflammatory Hallmarks are positive.

## Deviations
- pydeseq2 instead of R DESeq2 1.40.2. The shrunken LFC comes from pydeseq2 `lfc_shrink` (`log2FoldChange_shrunk`); padj is unaffected.
- The low-count filter is CPM-based, not read-based (see above).
- The paper does not state whether it modelled pairing. Paired is primary, unpaired is a sensitivity run.
- The paper's mean-LFC subset step is not applied in the runner. It was computed post hoc from the result tables.
- No sex covariate: sex is not in the GEO metadata.

## Paper inconsistencies
- Old: 359 + 572 = 931, not the stated 1,026.
- Baseline: 446 + 199 = 645, not the stated 665.
- 5% FDR (S2.7.p2) vs FDR < 0.01 (S2.8.p1).

## Tool problems
- The case runner cannot express a data-dependent post-hoc DEG rule such as "log2FC beyond the per-direction mean of significant genes". The paper's reported counts can only be compared by hand.
- `filter_low_counts` supports only CPM. There is no raw-read rule ("< N reads in every sample"), so the paper's filter is approximated (tools/case_runner.py:668).
- No functional errors. pydeseq2 prints overflow RuntimeWarnings in `pydeseq2/utils.py:1088` (harmless).
