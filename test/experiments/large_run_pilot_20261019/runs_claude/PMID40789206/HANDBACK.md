# HANDBACK: PMID40789206 / GSE297842

Status: **finished** (case `completed`, decision `valid`, route `paper_aligned`; validator 15 records, 0 errors).

## What ran
- Case spec route (`case_spec.json`, `python -m tools.case_runner execute`).
- Data: `GSE297842_htseq_rawCounts.txt.gz` (HTSeq raw counts, 55,414 Ensembl genes x 24 columns). Male C57BL/6J renal cortex, forced treadmill: Sed / 24 h / 1 wk / 2 wk, n=4 each (16 GSMs).
- Alignment: exact on the `STC804_<n>` key, taken from the metadata `description` ("Library name: ...") and the matrix column names; 16/16 aligned. The matrix's 8 extra columns (STC804_17..24, `D*_Run` / `D*_Sed`) have no GSM in the series and are not part of the paper's RNA-seq groups, so they were dropped.
- Primary: one pydeseq2 model `~ grp` on all 16 samples, with three planned contrasts vs Sed. Low-count filter: total count >= 10 across samples (mean >= 0.625; 21,923 genes kept; S2.9.p1).
- Sensitivity: a pairwise 2 wk vs Sed DESeq2 fit on 8 samples (total >= 10 over those 8).
- Enrichment: ORA (Enrichr GO/KEGG) and GSEA (Hallmark) on joint 2 wk and 24 h tables; both completed.

## Threshold
Paper threshold, applied unchanged: BH padj <= 0.05 with no fold-change cutoff (S2.9.p1; TAB1 "p<=0.05; q<=0.05; |log2FC|>=0").

## DEG counts vs paper (padj <= 0.05)
| Comparison | Ours (up/down) | Paper (up/down) |
|---|---|---|
| 2 wk vs Sed (joint, primary) | 29 (19/10) | 24 (17/7) |
| 1 wk vs Sed (joint) | 14 (6/8) | 0 |
| 24 h vs Sed (joint) | 74 (44/30) | 54 (34/20) |
| 2 wk vs Sed (pairwise sensitivity) | 93 (49/44) | 24 |

- 2 wk joint: 18 of the paper's 24 Table 2 genes are significant, including Scnn1a, Scnn1g, Foxi1, Cyp4a14, Mmp13, Cd209a, Hsd11b1 and Aplnr. Scnn1b (padj 0.10), Hsd11b2 (0.09), Cyp2d12, Lipo2, Plekhd1 and Ptges are not. All 24 paper genes change in the paper's direction. In the pairwise fit, 20 of 24 are significant, Scnn1b included.
- The joint model is much closer to the paper's count than the pairwise fit (29 vs 93), which suggests the paper fitted one 4-group model.
- 24 h: Lcn2 and Havcr1 are not significant (padj 0.45 and 0.34). This matches the paper's "non-significant increase".
- 1 wk: we find 14 DEGs where the paper found none. This is a real discrepancy, recorded here and not resolved.
- Effect sizes: our log2FC for the strongly changed genes are larger than the paper's (Cyp4a14 3.02 vs 0.93; Mmp13 -1.71 vs -0.99). pydeseq2's apeglm-type shrunk LFC is still about 2.7 for Cyp4a14, so the paper's LFC scaling is unexplained (possibly a different shrinkage or annotation). The direction is concordant.

## Deviations
1. The paper tested only "ENSEMBL protein-coding transcripts". The deposited matrix has no biotype, so we tested all genes that pass the count filter. This changes the BH denominator and adds non-coding hits such as Gm genes, pseudogenes and mt- genes in 24 h. It probably accounts for part of the count excess.
2. We used pydeseq2, not R DESeq2. The paper does not say whether it fitted one model or pairwise models, so we ran both: joint as primary, pairwise as sensitivity.

## Tool problems
- `tools/case_runner.py:489`: the paper-gene lookup rounds every value to 4 decimals, so small p-values print as `pvalue: 0.0` next to a non-zero padj. This is misleading; use significant-figure formatting instead.
- The DEG result tables (`results/*/DEG_results_*.csv`) keep only `ENSEMBL_ID`, with no symbol column. Comparing against the paper's gene list needed a manual `enrichment_tools._query_symbols` call, although the runner already maps symbols internally for the gene check (`tools/case_runner.py:472-480`).
- `case_spec.md` documents no filter rule for "total count >= N across samples" (the paper's wording). It had to be expressed as `min_mean_count = N / n_samples`, which depends on how many samples the execution has.
- A pydeseq2 RuntimeWarning (overflow in exp, `pydeseq2/utils.py:1088`) appeared during the fit. It was not fatal.
