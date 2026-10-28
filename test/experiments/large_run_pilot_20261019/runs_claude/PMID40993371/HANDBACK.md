# HANDBACK: PMID40993371 / GSE302867

Paper: Cardiac adaptation to endurance exercise training requires suppression of GDF15 via PGC-1α (PMC13158892).
Run status: completed (case_runner `execute`, validator 12 records, 0 errors). Route: `declared_deviation`.

## What ran

- Data: GSE302867 (downloaded to `E:/agent/mwangLab_pdf/data/GSE302867`): 20 male mouse hearts, 2x2 genotype (WT vs cardiomyocyte PGC-1a KO) x exercise (sedentary vs 6-week voluntary wheel running), n=5 per group. It matches the paper's Fig 2e-f and Fig 4a (n=5/group) and DA.p1.
- The only deposited matrix is `GSE302867_processed_data_fpkm.txt.gz` (FPKM; GEO data_processing: featureCounts, then FPKM). The paper used DESeq2 on counts (S4.10.p1). Raw counts are not on GEO, so the DESeq2 route is blocked.
- Alignment: matrix columns G1-1..G4-5 match the GEO `description` library names exactly (20/20). The group comes from the title: WTSed, KOSed, WTEx, KOEx.
- Method (declared deviation): limma on log2(FPKM+1), one cell-means model `~ 0 + grp` on all 20 samples, with 4 planned contrasts (`tools.multigroup_tools:run_multigroup_analysis`). No covariates: the batch, sex and age fields each hold a single value for all samples.
- Threshold: the paper's rule (S4.10.p1), BH padj < 0.05 and |log2FC| > 1, applied on the deviation route (`paper_on_deviation_route`). Audit rule: padj < 0.05 with no fold-change cutoff.
- Enrichment: preranked GSEA on MSigDB Hallmark (ranked by the limma t statistic) for the two exercise contrasts, as in the paper's Fig 2e.

## DEG counts vs paper (padj<0.05 & |log2FC|>1; audit padj<0.05 only)

| Contrast | Role | DEGs (up/down) | audit n | Paper |
|---|---|---|---|---|
| WT_Ex vs WT_Sed | primary (exercise) | 24 (22/2) | 466 | no count reported |
| KO_Ex vs KO_Sed | primary (exercise) | 164 (130/34) | 4061 | no count reported |
| KO_Sed vs WT_Sed | secondary (genotype) | 111 (74/37) | 1676 | no count reported (Fig 4a volcano) |
| KO_Ex vs WT_Ex | secondary (genotype) | 318 (191/127) | 4215 | no count reported (Fig 4a volcano) |

The paper gives no DEG counts in its text or figure legends, so the counts cannot be compared with it.

Named-gene and pathway checks:
- Gdf15 KO vs WT: log2FC +2.94 (padj 1e-4) in the sedentary state and +3.44 (padj <1e-4) after exercise. This agrees with the paper's claim that Gdf15 is the most upregulated gene in KO hearts in both states (S2.4.p2, Fig 4a).
- Hallmark OXPHOS, KO_Ex vs KO_Sed: NES -3.54, FDR ~0. This agrees in direction with the paper (NES -10.22).
- Hallmark OXPHOS, WT_Ex vs WT_Sed: NES -2.64, FDR ~0. This is the opposite direction to the paper (NES +5.14, Fig 2e). The discordance remains on our route. Possible causes: limma on log FPKM versus DESeq2-normalized counts, preranked t-statistic GSEA versus the paper's phenotype-permutation GSEA, or a difference in the samples themselves. It is not resolved.
- Heart-failure markers in KO_Ex vs WT_Ex: Myh7 +2.20 (padj <1e-4) and Nppb +2.02 (padj 0.005). Both are consistent with Fig 2b (qPCR).

## Deviations

1. DESeq2 on counts was replaced by limma on log2(FPKM+1), because only FPKM was deposited. Fold changes are on the log FPKM scale, so the |log2FC|>1 rule is not exactly the paper's DESeq2 fold change.
2. GSEA: the paper ran classic GSEA with phenotype permutation on DESeq2 normalized expression, and excluded low-expression genes. We ran gseapy prerank on the limma t statistic over all genes. We did not run the paper's M8 or ISR gene sets, or its WebGestalt GO ORA.
3. Ppargc1a FPKM is higher in KO than in WT (log2FC +0.86, padj 0.011, sedentary state). A cardiomyocyte-specific floxed-exon deletion can still produce transcript reads from the remaining exons, and Gdf15 and the heart-failure markers agree with the labels. The samples were therefore not treated as mislabelled, but this is worth noting.

## Tool problems

1. `tools/suitability.py:201-203`: for pairs that do not involve the reference, the comparison direction is set by the alphabetical order of the levels ("later vs earlier"). In this run that gave `grp_KOSed_vs_KOEx` and `grp_WTEx_vs_KOEx`, the reverse of the paper's KO_Ex vs KO_Sed and KO_Ex vs WT_Ex. `run_joint_limma` accepts only these enumerated names (`tools/case_runner.py:691`, "comparisons not in the suitability report"), so the paper-direction contrasts could not be requested. The first execute attempt failed; the attempt is saved in `_previous/`. The workaround was `run_multigroup_analysis` with explicit contrast coefficients. The same naming issue makes the suitability verdict `partially_analyzable` ("planned names not found"), even though all 6 comparisons have n=5 per group.
2. `run_multigroup_analysis` fits plain eBayes (`tools/multigroup_tools.py:124`) with no limma-trend option for log-FPKM data. This is minor; it is recorded in the method name.

## Key files

- `case_spec.json`, `run_status.json`, `summary.csv`
- `GSE302867/decisions.json`, `GSE302867/evidence.json`, `GSE302867/suitability/suitability.md`
- `GSE302867/results/joint/DEG_results_grp_*.csv`
- `GSE302867/results/enrichment_joint_grp_*/gsea/*_GSEA_Hallmark.csv`
