# HANDBACK — PMID31700184 / GSE124799

**Status:** finished. Route `declared_deviation`. The contract validator passed: 15 records, 0 errors.

## What ran
- **Paper (PMC6858591):** RNA-seq of FACS-sorted bone-marrow LSK cells from male C57BL/6 mice in three groups of 3: Sed (igloo), Ex (6-week wheel) and ExSed (6-week wheel, then 3 weeks with an igloo). Sources: S2.3.p3, S4.13.p1-p2 and Fig. 3o-r. Quantification was Salmon 0.11.3, then tximport, then edgeR. GSEA used the edgeR fold-change ranking against MSigDB Reactome. ORA used clusterProfiler GO/Reactome on genes at least 2-fold down in Ex vs Sed.
- **Ownership:** GSE124799 is named in S4.13.p2 and S4.23.p1. Its 9 libraries map 1:1 to the GSM titles. GSE110639 is the ATAC-seq series and was not used.
- **Alignment:** matrix columns are `Sed_1`…, while GEO titles are `Sed 1`…. `prep_matrix.py` replaces `_` with a space and checks each name against the titles, so the match is by name, never by position. Alignment is then exact on `title`, 9/9.
- **Matrix:** tximport gene-level estimated counts, deposited already rounded to integers (integer fraction 1.0, Ensembl IDs). They were treated as count-model input, with `rounding_documented: true`. The `round_estimated_counts` step was a no-op.
- **Design:** one factor `grp` with 3 levels and reference Sed. One model `~ grp` was fitted on all 9 samples, with two planned contrasts: Ex vs Sed (primary) and ExSed vs Sed (secondary). Suitability was `analyzable` (3/3 comparisons). No covariates: independent animals, all male, no batch recorded.
- **Executions:**
  - Primary: `run_joint_deseq2` (pydeseq2 Wald), planned contrasts.
  - Sensitivity: `run_edger_analysis` two-arm QL fit for each contrast. This is the paper's tool family, but fitted on two-group subsets.
- **Threshold:** the paper states no DEG cutoff, and its DEG list is only in Supplementary Table 2, which is not available here. Applied rule is `workflow_default`: BH padj < 0.05, no FC rule. Audit rule: padj < 0.05 and |log2FC| > 1, labelled as a comparison only; it mirrors the 2-fold ORA input in Fig. 3p,q.
- **Enrichment:**
  - Hallmark GSEA on both joint contrasts, ranked by log2FoldChange.
  - Enrichr ORA on the Ex vs Sed down genes.

## DEG counts vs paper (padj < 0.05, workflow default; paper threshold not stated)
| Table | n (up/down) | audit n (\|log2FC\|>1) | Paper |
|---|---|---|---|
| joint/grp_Ex_vs_Sed (primary, DESeq2) | 28 (12/16) | 27 | Supp. Table 2, count not in text |
| joint/grp_ExSed_vs_Sed (DESeq2) | 14 (3/11) | 14 | Supp. Table 2, count not in text |
| edgeR_Ex_vs_Sed (sensitivity) | 0 (min padj 0.99997) | 0 | — |
| edgeR_ExSed_vs_Sed (sensitivity) | 0 (min padj 0.126) | 0 | — |

The log2FC of DESeq2 and edgeR correlate at r = 0.955 (Ex) and r = 0.847 (ExSed). Most DESeq2 hits are low-to-moderate CPM genes that drop to 0 in one group, so they are on/off patterns. In ExSed, Igkc-like immunoglobulin genes (e.g. ENSMUSG00000076609) vary widely within Sed and Ex, which may point to B-cell carry-over in the sort. Treat the DESeq2 hits at n=3 as fragile.

**Pathway comparison with the paper.** The paper reports Reactome Cell Cycle down in Ex (FDR 0.004) and in ExSed (FDR 0.01). Our Hallmark GSEA is **not concordant**: no set reaches FDR < 0.25 in either contrast. In Ex vs Sed, E2F targets and G2M checkpoint have small positive NES (0.61 and 0.53, NOM p ≈ 1). In ExSed vs Sed they are weakly negative (non-significant). ORA on the Ex down genes gives only Peptide cross-linking (GO:0018149, adj p 0.014; EPB42, TGM5).

## Deviations
1. DESeq2 one-model planned contrasts replace the paper's edgeR. The edgeR executor fits two-arm subsets only, so a three-level edgeR model cannot be run, and the paper's exact edgeR model is not stated.
2. The workflow-default threshold is used because the paper gives none.
3. The paper's pooled "All Ex" (Ex+ExSed) vs Sed GSEA (Fig. 3o) was not reproduced, because pooling would merge two distinct levels.
4. GSEA used Hallmark instead of the paper's Reactome (410 sets), ranked by unshrunk DESeq2 log2FC instead of edgeR FC. Only the direction of the cell-cycle/proliferation sets is comparable.

## Tool problems
- **`tools/edger_tools.py:106-107`:** the only filter drops all-zero genes; there is no `filterByExpr`-style low-count filter. Low-count genes stay in the QL dispersion/prior estimation and in the BH family. The result is 0 DEGs, even though the DESeq2 top genes have edgeR nominal p ≈ 1e-4 to 1e-3. This likely makes the edgeR route systematically over-conservative compared with a standard edgeR workflow.
- **`tools/edger_tools.py:122-125` (inmoose `glmQLFit`) is very slow:** the 6-sample Ex vs Sed fit took 13.4 min and ExSed 3.2 min. The joint DESeq2 on 9 samples took ~25 s (workflow.log, 16:00:44 → 16:14:08 → 16:17:21).
- **`tools/case_runner.py:84` (`key_patterns`, one regex group only) and `:283` (`_contained_keys`):** the runner cannot express a `_`↔space difference between matrix columns and titles, and inspect reported `alignment_keys: []` for a near-exact match. A one-line prep script (`prep_matrix.py`) was needed.
- **Minor, `tools/edger_tools.py:145-148`:** the tool prints its own summary using padj < 0.05 and |log2FC| > 1. The runner ignores it, but the printed counts use a different rule from the applied one.

## Files
- Spec: `case_spec.json`
- Prep script: `prep_matrix.py`, which writes `GSE124799_counts_titled.csv`
- Records: `GSE124799/decisions.json`, `GSE124799/evidence.json`, `summary.csv`
- Results: `GSE124799/results/{joint,edgeR_*,enrichment_*}/`
- Suitability: `GSE124799/suitability/suitability.md`
