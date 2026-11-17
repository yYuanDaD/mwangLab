# HANDBACK: PMID 35847876 / GSE205173

## What ran
- Route: case spec (`tools.case_runner execute case_spec.json`). Status completed, decision contract validator reported 0 errors (13 records). The run was executed twice; the first attempt (same numbers, no gene-check caveats) is in `_previous/20261117T225315Z`.
- Data: `GSE205173_Raw_gene_counts_matrix.txt.gz`. Integer counts, 18,514 gene symbols, 12 samples (3 per group), 17.3-19.5M reads per sample. Aligned exactly on `title` (12/12). Group comes from the title prefix and agrees with the GEO treatment field: Ctrl, CtrlSwim, Model (AOM/DSS), ModelSwim (AOM/DSS plus swimming).
- Design: one DESeq2 (pydeseq2 Wald) `~ grp` model on all 12 samples with four planned pairwise contrasts. No blocking: the samples are independent animals, all male (the sex check passed, one sex only), with no batch recorded.
  - Primary: ModelSwim vs Model.
  - Secondary: CtrlSwim vs Ctrl, Model vs Ctrl, ModelSwim vs CtrlSwim.
- Sensitivity: a separate two-arm DESeq2 fit on only the 6 Model and ModelSwim samples.
- Enrichment on the primary table: ORA (GO BP/MF/CC, KEGG) on the paper-threshold DEGs, and GSEA (Hallmark) on the full ranking by stat. Both completed.

## Threshold
The paper's rule (S2.7.p1) is "q value < 0.05, fold change > 2, or fold change < 0.5". It was applied as padj < 0.05 and |log2FC| > 1, both strict (threshold_source = paper). The audit rule is padj < 0.05 with no fold-change cutoff.

## DEG counts vs the paper
The paper gives no per-contrast counts. It reports only the union of pairwise DEGs (1403), without saying which pairs went into it (S3.2.p1).

| Table | ours (paper rule) | up / down | audit (padj<0.05) | paper |
|---|---|---|---|---|
| de/grp_ModelSwim_vs_Model (primary) | 111 | 42 / 69 | 359 | not reported |
| de/grp_CtrlSwim_vs_Ctrl | 65 | 26 / 39 | 661 | not reported |
| de/grp_Model_vs_Ctrl | 1343 | 1139 / 204 | 5545 | not reported |
| de/grp_ModelSwim_vs_CtrlSwim | 270 | 239 / 31 | 1557 | not reported |
| pair_ModelSwim_vs_Model (sensitivity, per-pair fit) | 130 | 35 / 95 | 315 | - |
| Union of our 4 tables | 1442 | | | 1403 (union) |

- The joint and per-pair fits agree closely: log2FC r = 0.991, and 90 DEGs are shared.
- Genes reversed by swimming (comparable to the paper's STEM selection of 279):
  - 59 genes are up in Model vs Ctrl and down in ModelSwim vs Model.
  - 33 genes are down in Model vs Ctrl and up in ModelSwim vs Model.
- Named genes (S3.2.p1):
  - ModelSwim vs Model: Pla2g4f (-0.68) and Ptges (-0.46) are lower with swimming, and Fzd9, Cldn15 and Tfrc are higher. These directions agree with the paper, but none reaches padj < 0.05 (the closest is Tfrc, padj 0.077). Ptger2 is unchanged (+0.07), so the paper's swim-reduced Ptger2/EP2 is not reproduced.
  - Model vs Ctrl: Pla2g4f and Ptges are up (log2FC > 1.3), and Fzd9, Cldn15 and Tfrc are down. All are significant, which agrees with the paper. Ptger2 is not significantly up (+0.32, padj 0.42).
- Enrichment, kept separate from the DE result: the top KEGG ORA terms for the primary table are Pancreatic secretion, Protein, Fat and Carbohydrate digestion and absorption. These match the paper's digestion-and-absorption theme (S3.2.p1, Fig 3J). The top GSEA Hallmark sets are higher with swimming: oxidative phosphorylation, adipogenesis, fatty acid metabolism and xenobiotic metabolism (all FDR ~0). Pancreatic-enzyme genes found in colon tissue may reflect tissue composition. This is recorded as a caveat.

## Deviations (declared)
- One model was fitted on all 4 groups, so dispersions are shared. The paper most likely fitted each pair separately; the per-pair fit for the primary contrast is the sensitivity run above.
- The counts come from CLC Genomics Workbench, as stated in GEO `data_processing`. The paper describes HISAT2/HTSeq-count, and also says HiSeq X Ten where GEO says NovaSeq 6000. Recorded as discrepancies; executable without change.
- GEO has 3 of the 5 or 10 animals per group. The paper does not say how the sequenced animals were chosen.
- The paper's STEM clustering, the 279/48-gene selection and the Student t tests were not reproduced. No runner executor covers them.
- The 12 Excel-mangled symbols (1-Mar..11-Mar, 15-Sep) were kept as-is because they are unique and none is a paper-named gene.
- The two remaining pairs (Model vs CtrlSwim, ModelSwim vs Ctrl) were not run. The paper's union may include them.

## Tool problems
- pydeseq2 printed `RuntimeWarning: overflow encountered in exp` at `.venv-pdf/Lib/site-packages/pydeseq2/utils.py:1088` during the fit. The results look normal (deg_sanity ok).
- The case spec `paper_counts` only accepts per-table counts, so the paper's only reported number (a union across tables) cannot be entered. The runner's `comparison` block is therefore empty and the union comparison was done by hand here.
- No tool errors.
