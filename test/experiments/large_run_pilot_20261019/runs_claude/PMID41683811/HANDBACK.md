# HANDBACK: PMID41683811 / GSE315228

Isometric-exercise (IE) rehabilitation after total hip arthroplasty (THA). 8 women aged 73-77. Control arm: standard IE protocol (n=4). Experimental arm: additional and longer IEs (n=4). Rectus femoris biopsies at d0 (pre-op), d1 and d12. Sequencing was Nanopore PromethION, with up to 3 sequencing runs per biopsy. GEO has 72 samples (24 biopsies x 3 runs).

## What ran (case-spec route, `python -m tools.case_runner execute case_spec.json`; validator: 30 records, 0 errors)

`prep_collapse_techreps.py` sums the technical runs of each biopsy into 24 biopsy libraries. Before summing it drops 3 failed runs with fewer than 1,000 reads: barcode01, barcode54 and barcode67.

**Case `GSE315228` (primary, declared deviation).** Raw featureCounts counts, analysed with DESeq2 (pydeseq2 Wald). Each comparison is paired on patient: `~ subject + time`.
| table | role | ours (padj <= 0.05) up/down | paper up/down |
|---|---|---|---|
| d1_vs_d0_pooled (paper 1vs0) | secondary | 196 (126/70) | 2579 (593/1986) |
| ctr_d12_vs_d0 (paper ctr12vs0) | secondary | 0 | 736 (546/190) |
| exp_d12_vs_d0 (paper exp12vs0) | primary | 0 | 4279 (3989/290) |
| ixn_change_d12 (exp minus ctr d12-d0 change; limma on per-patient log2CPM differences) | exploratory | 0 | not tested by paper |
| joint (unpaired DESeq2 ~ cell, 24 biopsies, 11 comparisons) | exploratory | ctr d12vs0 103 (84/19); exp d12vs0 10 (10/0); exp-vs-ctr at any time and interactions 0-1 | |

**Case `GSE315228_reps` (sensitivity: the paper's input, runs as samples, unpaired `~ time`).** 1vs0: 510 (305/205). ctr12vs0: 480 (341/139). exp12vs0: 189 (123/66).

Threshold: the paper's own rule, FDR <= 0.05 with no fold-change cutoff (S4.8.p1, FIG4). The audit rule adds |log2FC| > 1 and is reported in summary.csv.

GSEA (Hallmark, ranked by the Wald statistic):
- d1 vs d0: TNFA/NFKB and IL6-JAK-STAT3 up.
- ctr d12 vs d0 and exp d12 vs d0: inflammatory, IL6, TNFA and angiogenesis sets up; oxidative phosphorylation and myogenesis down. This matches the paper's FIG7 in both arms.
- The paper says inflammation is resolved in the experimental arm at d12 (FIG6b). We do not reproduce that: inflammatory sets are still significantly up in exp at d12 versus d0.
- The interaction GSEA does point the paper's way. INFLAMMATORY_RESPONSE (NES -1.92), IL6_JAK_STAT3 and TNFA_NFKB rise less in exp than in ctr (FDR < 0.01).
- Angiogenesis shows no difference between arms (NES 1.09, FDR 0.70).

Paper genes in exp12vs0 have padj = 1 in our results: BMP7, TGFB2, EGF, ANGPT1, FLT1, KDR, NRP2, TEK, VEGFA, VEGFC, EDNRA, PRKG1, BMP8A and ADORA2B.

## Interpretation
- No gene-level exercise effect survives FDR at the biopsy level. This holds within either arm and for the between-arm difference in change.
- The paper's large exp12vs0 count, and its claim that exp has 7 times more up-genes than ctr, are not reproduced, even with runs counted as samples: exp 189 vs ctr 480, the opposite direction.
- Within-arm time contrasts mix surgery recovery with rehabilitation. Only the interaction isolates the added IEs. The arms were allocated sequentially without randomization, so the arm difference is associational.

## Deviations
1. Technical runs were summed per biopsy. The paper included every run as a sample (FIG3 legend), which is pseudoreplication.
2. Patient was used as a blocking term. The paper does not state its DESeq2 formula; S4.6.p2 says comparisons are "relative to preoperative samples from the same patients".
3. The interaction was added as an exploratory analysis. Patient is nested in arm, so the runner cannot fit a paired DESeq2 interaction. It was run as limma paired_change on log2(CPM+1) instead.
4. pydeseq2 was used, not R DESeq2 1.38.3.
5. Three failed runs were excluded.

## Tool problems
- The paired within-arm DESeq2 fits have 8 samples and 3 residual df. Their p-values are very conservative: 66 genes have p < 0.01 out of 34,403, when about 344 would be expected by chance. This is a low-df dispersion issue, not a bug, but it explains the 0 counts.
- For an excluded sample, `tools/case_runner.py:517-522` reports alignment `n_aligned`/`n_metadata` before `exclude_samples` is applied (`:498-503`). The reps case shows 72/72 although 69 samples were analysed.
- `tools/decision_contract.py:65,338-343` detects pairing from the words in `design.final.analysis_type`. A deliberately unpaired sensitivity case had to avoid the words "repeated" and "paired" to pass.
- `tools/decision_contract.py:163` requires `design.final.formula` or `design_column` even when the design is a set of per-subset executions. This is not listed in case-spec.md's design row.
- pydeseq2 printed overflow RuntimeWarnings (`pydeseq2/utils.py:1088`). They are harmless.
