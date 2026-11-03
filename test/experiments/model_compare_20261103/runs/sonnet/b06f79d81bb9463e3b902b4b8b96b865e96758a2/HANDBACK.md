# HANDBACK: GSE164890 (PMC9027771), whole blood before vs after exercise at altitude

STATUS: finished (paper_aligned route; decision contract validator: VALID, 11 records; external LLM attempts: 0)

## What ran
- Paper reconstruction: 7 elite female skaters x (before, after) one ~1 h skating bout at 1850 m altitude, day 18. The paper ran DESeq2 v1.18.1 with design "donor + exercise" on RSEM per-gene counts and kept genes at FDR < 0.1 with no fold-change cutoff (S2.5.p1, FIG1). It reports 2516 up and 1542 down (4058 total, S3.2.p2).
- Ownership: the metadata series_id is GSE164890. The 14 samples are 7 skaters x before/after, as in S2.3.p1. The matrix is the supplementary `rsem.genes.counts.tsv.gz`.
- Alignment: exact match of matrix columns (`1before` ... `7after`) to the metadata `description` column. 14/14 matched, no positional alignment. The `subject` and `ex` columns were derived by regex from `title` and the time point column.
- Matrix: RSEM expected counts, so estimated counts (94.5% integer-valued, the rest fractional). I rounded them with numpy.rint (`results/counts_rounded.csv`) and recorded `rounding_documented`.
- Design and covariance: pairing_report shows 7/7 complete pairs. `~ subject + ex` is full rank with 6 residual df. Subject is a required blocking term. The suitability verdict is analyzable.
- Method: `tools.deseq2_tools:run_deseq2_analysis` (pydeseq2), `~ subject + ex`, contrast after vs before, `alpha=0.1`, `covariate_columns=subject`.
- Threshold: the paper's rule, padj < 0.1, no effect cutoff, counted with `native.apply_threshold`.
- Enrichment: Hallmark GSEA (gseapy prerank, ranked by the Wald statistic, Human h.all 2024.1.Hs).

## DEG counts vs the paper (threshold: DESeq2 padj/FDR < 0.1, no log2FC cutoff)
| | up | down | total |
|---|---|---|---|
| This run | 2588 | 1655 | 4243 |
| Paper | 2516 | 1542 | 4058 |

- The totals differ by about 4.6%. The 15,634 genes with a non-NA padj are the ones tested.
- Audit counts (not the paper rule):
  - padj < 0.1 and |log2FC| > 1: 131 up and 93 down (224 total). The paper says "more than twofold" for 104 up and 58 down, without stating the FDR rule for that count. With the apeglm-shrunk log2FC the count is 82 genes.
  - padj < 0.05: 3238 (2114 up, 1124 down).
  - padj < 0.1 and |log2FC| >= 0.5: 1423.
- Genes the paper highlights, all significant here:
  - MYC: log2FC -0.36, padj 0.0044
  - PPBP: log2FC +0.53, padj 6.7e-5
  - MARC1: log2FC +1.23, padj 1.1e-7
  - PHOSPHO1: log2FC +0.54, padj 0.0044
- Hallmark GSEA (kept separate from the DE counts):
  - Up: TNFA_SIGNALING_VIA_NFKB (NES 2.50), COMPLEMENT, INFLAMMATORY_RESPONSE, APOPTOSIS, interferon alpha/gamma, IL6_JAK_STAT3, HYPOXIA, all with q <= 1e-4.
  - Down: MYC_TARGETS_V2 (NES -2.45, q = 0).
  - This agrees with S3.3.p1-p2: inflammatory and immune pathways up, hypoxia up, and MYC_TARGETS_V2 as the standout down-regulated Hallmark set. MYC_TARGETS_V1 (q 0.065) and E2F_TARGETS (q 0.078) are also nominally down here; the paper does not discuss these two.
  - The tool's "significant" label uses q < 0.25; I did not apply a different cutoff.

## Deviations (declared)
1. Python pydeseq2 executor instead of R DESeq2 1.18.1 (different dispersion fit and independent-filtering details).
2. RSEM expected counts were rounded to integers; the paper's own rounding or tximport route is not documented in the paper.
3. The results-folder driver relabelled subject 1..7 as S1..S7 (`results/design_metadata_S.csv`; grouping identical to the derived `subject` column) to keep subject categorical.
4. Enrichment was Hallmark GSEA only. The paper's ORA (clusterProfiler) and fGSEA on H plus the CP collections were not run.
5. The paper's ComBat donor correction (PCA/heatmaps only) and the cell-type deconvolution and microarray comparisons (S2.6, S2.7, S3.4, S3.5) were out of scope. They need external datasets or are diagnostics, not GSE164890 DE.
6. There is no exercise-free arm and no altitude vs sea-level comparison; the paper says so in S3.5.p1. The result is the acute within-person after-vs-before response at altitude, not an altitude-specific effect.

## Tool problems
- `tools/deseq2_tools.py:187-195`: the returned summary text always says "padj < 0.05, |log2FC| > 1", whatever `alpha` is. With `alpha=0.1` the printed 116/69 do not describe the analysis; I counted with `native.apply_threshold` instead. The `alpha` argument works.
- `tools/joint_contrasts.py:70-72` (`_numeric_covariates`) fits all-numeric covariates as continuous. A numeric `subject` (1..7) would silently turn the blocking term into a slope in `run_joint_deseq2`/`run_joint_limma`. I did not use that path. The two-arm DESeq2 executor casts covariates to str (`deseq2_tools.py` ~l.147-158), which is correct.
- `native.derive_columns` returns numeric-looking regex captures as numbers, so `subject` comes out as 1..7. This is easy to miss, because it silently matters only for the joint path above.
- `native.align_to_metadata` drops the `Symbol` and `Gene_type` annotation columns and keeps only Ensembl IDs. GSEA therefore needs a MyGene.info network lookup (it worked here), and 12.6% of genes had duplicated ranking stats (a gseapy warning).
- Minor: passing the blocking subject column also as a `covariate_candidates` entry of `case.suitability` produced a spurious "omit - makes the design rank deficient" line. This is my input error, not a tool fault. I re-ran with an empty candidates list.

## Files
- `GSE164890/results/deseq2/DEG_results_after_vs_before.csv`, `GSE164890/results/threshold_counts.json`, `GSE164890/results/audit_counts.json`
- `GSE164890/results/gsea/DEG_results_after_vs_before_GSEA_Hallmark.csv`
- `decisions.json`, `evidence.json`, `summary.csv`, `run_manifest.json`, `scripts/g1.py`-`g9.py`
