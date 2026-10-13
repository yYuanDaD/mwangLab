# Stage H result (2026-10-13)

Run: Codex with the `bioinformatics-workflow` skill on Windows, `output/codex_hfpef_20261013_v2`
(repo commit `f9eb082`), inputs from `output/stage_h/repo/cases/GSE195482`. Reference: Bo's R
DESeq2 tables (`~ Group`, `rowSums >= 10`). Scored with `compare_to_reference.py` at Bo's
threshold (padj < 0.05 and |log2FC| > 0.5); padj < 0.05 alone gives the same numbers.

## Decisions

All 24 records are `VALID`; both cases completed. Every scientific decision matches the paper:

- two sex-stratified pairwise contrasts (HFpEF vs chow in WT), not pooled;
- raw counts, DESeq2, `~ condition`, no blocking (independent animals);
- threshold from the paper: BH-adjusted P < 0.05 with no fold-change cutoff;
- declared deviation: PyDESeq2 instead of the paper's edgeR scaling plus DESeq2 1.16.1;
- GO/KEGG ORA on the thresholded list and Hallmark GSEA on the Wald statistic, kept separate.

The decision trace analysis (decisions only; this run predates trace.jsonl) shows no revision,
no rejected record, and high confidence everywhere except the two enrichment records (medium).

## Agreement with Bo

| Contrast | Bo DEG | Skill DEG | Overlap | Jaccard | Direction on overlap | Bo DEG recovered | log2FC Pearson (all genes) |
|---|---:|---:|---:|---:|---:|---:|---:|
| WMF vs WCF (female) | 1,360 | 1,379 | 1,305 | 0.910 | 100% | 96.0% | 1.000 (17,148 genes) |
| WMM vs WCM (male) | 131 | 128 | 123 | 0.904 | 100% | 93.9% | 1.000 (16,800 genes) |

## Why the gene sets differ

Fold changes are identical; only genes at the significance boundary differ.

- Female: 74 genes significant only in the skill run have Bo padj 0.050 to 0.062; 55 significant
  only for Bo have skill padj 0.050 to 0.058.
- Male: 5 and 8 genes, almost all within the same band; two genes differ strongly (one each way,
  for example Bo padj 0.37 against skill padj 0.016), consistent with different outlier handling.

The causes are implementation differences between PyDESeq2 and R DESeq2, not analysis decisions:

- Bo filters genes with `rowSums >= 10` before fitting (about 17,000 genes); the skill's DESeq2
  tool keeps all 23,500 rows, and independent filtering then tests 13,924 (female) against Bo's
  15,146 genes, which changes the BH adjustment;
- PyDESeq2 standard errors are about 2% larger (median lfcSE ratio 1.02 to 1.03);
- Cook's distance outlier handling differs.

The executor deviation is recorded in the method decision; the pre-filter was not. Fixed after
this run: `run_deseq2_analysis(..., min_total_count=10)` reproduces Bo's `rowSums >= 10`, and the
skill now asks the method decision to record the filter as `prefilter`. A rerun with the filter
should move the Jaccard closer to 1; the remaining gap is PyDESeq2 against R DESeq2.

## Caveats

- Codex ran from the main repository, not the clean `output/stage_h/repo`. The main repository
  holds a handoff note with earlier DEG counts for these contrasts. Nothing in the run outputs
  refers to it, and the DE numbers come from PyDESeq2 directly, but the run is not strictly blind.
- The same counts (1,379 and 128) were produced by the earlier LangChain pipeline on these
  inputs, so the skill route and the legacy route agree.
