# HANDBACK: PMID41555288 / GSE310294

Run: `python -m tools.case_runner execute test/experiments/large_run_pilot_20261019/runs_claude/PMID41555288/case_spec.json`. Status `completed`, 13 records, 0 contract validator errors.

## What ran

- **Paper (PMC12896231):** 6-week moderate treadmill exercise vs sedentary control in adult male SD rats. RNA-seq on the left tibia, n = 3 per group (Fig. 5). Novogene used the DEGseq R package for DE (S2.6.p1). The DEG rule is only "Fold Change < -2 or > 2" (S3.3.p1); no p or q cutoff is stated. Paper result: 2076 DEGs (1552 up, 524 down).
- **Ownership:** DA.p1 names GSE310294. The series has 6 rat bone samples (3 control, 3 exercised) with ENSRNOG IDs.
- **Alignment:** a prep script, `prep_rename_columns.py`, renamed the matrix columns from `sampleN_FPKM` to `Sample_N`; the values are unchanged. `key_patterns` builds the same `Sample_N` key from the metadata field `description` ("Library name: Sample N"). Match is exact, 6/6. Groups come from the `treatment` field (no -> CTRL, exercise -> EX).
- **Matrix:** raw counts. The columns are named `_FPKM`, but every value is an integer and the column sums are 14.1-18.1 M, which are library sizes. GEO data_processing also says "raw fragment counts".
- **Design:** two groups, `~ grp`, EX vs CTRL, 3 vs 3. The suitability check returned "analyzable". No blocking or covariates.
- **Method:** DESeq2 (pydeseq2 Wald) as the primary analysis. This is a declared deviation: the paper's DEGseq route is blocked because the workflow has no DEGseq executor. edgeR (TMM) ran as a sensitivity analysis, because GEO data_processing names edgeR.
- **Threshold:** the paper's rule was applied exactly, on the deviation route: |log2FC| > 1 with no p-value filter. A separate audit rule adds BH padj < 0.05.
- **Enrichment** on the primary table:
  - ORA (Enrichr GO BP/MF/CC and KEGG_2019_Mouse, using rat gene symbols), on the FC-only list. Top KEGG terms include cytokine-receptor interaction, hematopoietic cell lineage and ECM-receptor interaction.
  - GSEA Hallmark, mouse sets. Enriched in exercise: E2F targets, G2M checkpoint, heme metabolism, allograft rejection and interferon responses, all at FDR about 0. This agrees in direction with the paper's GO findings: "chromosome, centromeric region" up and leukocyte immunity up.

## DEG counts vs paper (paper rule: |FC| > 2, no p filter)

| Table | Paper rule (FC-only) | Audit (padj < 0.05 and abs log2FC > 1) | Paper |
|---|---|---|---|
| DESeq2 EX vs CTRL (primary) | 4459 (2808 up / 1651 down) | 1 | 2076 (1552 up / 524 down) |
| edgeR EX vs CTRL (sensitivity) | 5321 (3266 up / 2055 down) | 0 | - |

Only 543 genes have raw p < 0.05. The FC-only count is driven by low-count, high-variance genes, and almost nothing passes FDR. Sample correlations on log2 CPM are low and uneven (Pearson 0.69-0.97). Sample_6 (exercise) is an outlier. This variation fits bone or marrow heterogeneity, and it swamps the group effect at n = 3.

**Paper-named genes contradict the paper.** The paper says Igf1r, Bglap, Sp7, Smad6, Runx2, Ctnnb1, Col1a1 and Pth1r go up with exercise. Here most show log2FC <= 0 and none is significant: Col1a1 -1.2, Sp7 -1.0, Bglap -0.52, Runx2 +0.28 (padj about 1). Acp5 (Trap) is -0.69, which agrees with the paper's direction, but its p-value is NA. Tnfsf11 (Rankl) was not found by the symbol lookup. These contradictions are also listed in the study caveats in the records.

## Deviations

1. DESeq2 (with an edgeR sensitivity run) replaces DEGseq. DEGseq's MA-plot test has no executor here.
2. The paper's FC-only threshold was applied as written; the padj audit is reported next to it.
3. The matrix's "FPKM" column labels were rejected as a mislabel and the values treated as raw counts (decided from the values and the GEO note).
4. GEO data_processing mentions hg38 and mm10 alignment. This is boilerplate: the IDs are rat Ensembl.

## Tool problems

- No blocking problems.
- pydeseq2 printed repeated `RuntimeWarning: overflow encountered in exp` (pydeseq2/utils.py:1088) during fitting. It was harmless; the run completed.
- `_gene_lookup` (tools/case_runner.py:428) returned null for Tnfsf11: the rat Ensembl-to-symbol mapping missed it. Minor.
- `inspect` reports `alignment_keys: []` when the metadata holds "Sample N" and the matrix holds "sampleN_FPKM". A small rename prep script was needed. This is expected behaviour, not a bug.
