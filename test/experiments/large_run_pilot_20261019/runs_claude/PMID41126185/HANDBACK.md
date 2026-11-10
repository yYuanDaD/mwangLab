# HANDBACK: PMID41126185 / GSE289091

Paper: Lamin A/C protects chromatin accessibility during mechanical loading in human skeletal muscle (PMC12542426).
The exercise mimic is 4 h of equibiaxial cyclic stretch (10%, 0.5 Hz) applied to immortalized human myotubes (S2.3.p1). Abstract ABS.p2 calls it "mechanical stress mimicking acute muscle exercise". This is an in vitro model, not exercise in people.

## What ran

- `prep_merge_quant.py` merged the `NumReads` column of the 18 DRAGEN `*.quant.genes.sf.gz` files (Salmon format) in `GSE289091_RAW.tar` into `data/GSE289091/GSE289091_numreads_merged.csv`. Gene versions were stripped and the 44 `_PAR_Y` rows were dropped. The result is 60,607 genes x 18 samples.
- `case_spec.json` went through `python -m tools.case_runner execute`. The validator found 15 records and 0 errors, and the run status is completed. The route is `declared_deviation`.
- Alignment matched exactly on GSM ids. Derived columns: `geno` (Ctl/siLMNA), `cond` (static/stretch), `run` (r1 NovaSeq / r2 NextSeq), `grp`.
- Method: R DESeq2 LRT (`tools.r_de_tools:run_r_de`, engine deseq2), comparing full `~ cond` with reduced `~ 1` within each genotype. This is the paper's route (S2.6.p3). Estimated counts were rounded. Genes were kept if CPM >= 1 in at least 2 of each comparison's samples.
- Threshold: the paper contradicts itself. The Fig. 6 legend for the stretch volcanoes says log2FC > 0.5 & FDR < 0.05. The Methods (S2.6.p3) say |log2FC| > 1 & FDR < 0.05. Applied rule = Fig. 6 rule (`threshold_source: paper`). Audit rule = Methods rule.
- ORA (Enrichr GO/KEGG) ran on the up and down lists of the siLMNA primary table. GSEA was not run because the LRT statistic is unsigned.

## DEG counts vs paper (FDR < 0.05)

| Table | Samples (static/stretch) | Applied: abs(LFC) > 0.5 | Audit: abs(LFC) > 1 | Paper |
|---|---|---|---|---|
| ctl_stretch (primary) | 3 / 3, run 1 | 21 (20 up / 1 down) | 3 (3 / 0) | 7 |
| silmna_stretch_run2 (primary) | 4 / 4, run 2 | 2119 (1460 / 659) | 554 (429 / 125) | 634 (485 / 149) |
| silmna_stretch_all_runadj (sensitivity, ~run+cond) | 7 / 4 | 1963 (1325 / 638) | 564 (434 / 130) | 634 |
| silmna_stretch_all_naive (sensitivity, no batch term) | 7 / 4 | 1373 (742 / 631) | 296 (200 / 96) | 634 |

The paper's 634 = 485 up / 149 down is much closer to our Methods-rule (|log2FC| > 1) counts: 554 = 429 / 125 within run 2, and 564 with a run term. This suggests the paper actually applied |log2FC| > 1, not the 0.5 in the Fig. 6 legend.

The qualitative result is reproduced: the siLMNA stretch response is far larger than the control stretch response.

Paper-named genes in S-siLMNA vs siLMNA (run 2), log2FC / padj. All seven move in the paper's direction:

| Gene | log2FC | padj |
|---|---|---|
| HMGA2 | +1.80 | <1e-4 |
| TIMP3 | +1.09 | <1e-4 |
| PAWR | +1.04 | <1e-4 |
| HAS1 | +0.44 | 0.19 (not significant) |
| COL8A1 | +0.33 | 0.022 |
| EMP1 | +0.39 | 0.037 |
| CKMT2 | -0.95 | <1e-4 |

ORA was weak: only 1 GO BP term passed adjusted p < 0.05 for the up genes, and none for the down genes. Among the non-significant top terms, the up genes include cell-cell adhesion and the down genes include Histone Deacetylase Activity and collagen-containing ECM. That partly echoes Fig. 6f, but it is not a significant reproduction of it.

## Deviations

1. **GSM8783562 was excluded.** GEO labels it siControl stretch rep1 (Sctrl3). Its LMNA CPM is 249, close to the run-1 siLMNA samples (184-219) and far below the other six siControl samples (801-874). It also correlates best with the run-1 siLMNA static samples. I treated it as a genotype mislabel. The paper probably included it, which may explain part of the Ctl count difference (21/3 vs 7).
2. **Batch handling for siLMNA.** Sequencing run (run1 NovaSeq vs run2 NextSeq) is a strong batch: static siLMNA samples correlate at r ~0.97 across runs vs ~0.996 within run 2. All stretched siLMNA samples are in run 2, so the primary siLMNA contrast is restricted to run 2. A run-adjusted model on all 7 static samples is the sensitivity check. The paper does not describe its sample sets or any batch handling.
3. **Low-count filter.** CPM >= 1 (paper: > 1) in at least 2 samples, applied per comparison. The paper's filter set is not stated.
4. **GSM9181790 (ctrl1) was kept.** It was added to GEO in Aug 2025 and is labelled polyA RNA (the others say total RNA), but its profile matches the other siControl samples.
5. **Contrasts not run** (not exercise contrasts): the static genotype contrast (Fig. 3, 876 DEGs) and S-siLMNA vs S-Ctl. The latter would also be fully confounded with run. No genotype x stretch interaction was run: the paper did not test it, and each within-genotype contrast sits in a different run.

## Tool problems

- `tools/native.py:539` / `tools/geo_tar.py` (`unpack_and_merge_geo_tar`): the `_RAW.tar` merge does not recognize the Salmon/DRAGEN `quant.genes.sf` format (`Name, Length, EffectiveLength, TPM, NumReads`). Inspect reported "no mergeable per-sample count files", so I had to write a prep script.
- `tools/case_runner.py:877` (study comparison) and `tools/case_runner.py:801` (enrichment) need table names of the form `<execution>/<lrt_name>`, even for a single-output `run_r_de` execution. On the first attempt, plain execution names silently gave `"ours": null` and enrichment `not_run` instead of raising a spec error.
