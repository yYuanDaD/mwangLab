# HANDBACK: PMID38686869 / GSE233004

Paper: Moderate Endurance Exercise Increases Arrhythmia Susceptibility and Modulates Cardiac Structure and Function in a Sexually Dimorphic Manner (PMC11179941).
Status: **finished**. The case spec ran with all gates `valid` and execution `completed`. The contract validator reported 0 errors on 17 records.

## What ran

- **Data.** Bulk RNA-seq of mouse left ventricle. The matrix is `GSE233004_countdata.csv.gz`: 55,401 Ensembl genes x 12 samples of integer STAR + featureCounts counts. The design is 3 sedentary (SED) and 3 exercised (EX) mice per sex; exercise was 6 weeks of treadmill running.
- **Alignment.** Matrix columns match the GEO `title` exactly (12/12). Sex and treatment come from the title prefixes (`FEX`, `FSE`, `MEX`, `MSE`).
- **Sex check.** The X/Y-gene check passed. Xist is high only in females, and Ddx3y, Eif2s3y and Uty are high only in males.
- **Paper route.** The paper used DESeq2 Wald with BH correction and reports DEGs at padj < 0.05 with no fold-change cutoff for the volcano/KEGG counts (S1.8.p3). It compares exercised with sedentary mice within each sex (FIG6).
- **Primary analysis (`joint4`).** One pydeseq2 model on all 12 samples with a 4-level sex x treatment cell (`~ cell`). Two contrasts were extracted from it: F/EX vs F/SED and M/EX vs M/SED.
- **Sensitivity analysis (`sepfit_*`).** Separate DESeq2 fits per sex, 6 samples each (`~ trt`).
- **Exploratory analysis (`trt_EX_vs_SED_pooled_sexadj`).** A pooled `~ sex + trt` model for the exercise main effect. The paper does not report this.
- **Enrichment.** On the `joint4` tables: ORA (Enrichr GO + KEGG 2019 Mouse) and GSEA (Hallmark, ranked by `stat`).

## DEG counts vs the paper (threshold padj < 0.05, no log2FC cutoff; source S1.8.p3)

| Contrast | Ours (joint4, primary) | Paper (S2.5.p2) | Separate fit (sensitivity) |
|---|---|---|---|
| Female EX vs SED | 1 (1 up) | 1 | 24 (17 up / 7 down) |
| Male EX vs SED | 26 (14 up / 12 down) | 22 | 0 |
| Pooled, sex-adjusted (exploratory) | 2 | n/a | n/a |

- **Female.** As in the paper, the only female DEG is Ddx3y, up in EX (padj 0.018).
- **Male.** Of the 5 male genes the paper names, Gpx1, Mrps24, Klf2 and Fth1 pass padj < 0.05, all up in EX. Mtmr14 has p = 1.5e-5 but padj = NA: pydeseq2's outlier/filtering step dropped it.
- **Labelled audit rule (padj < 0.05 and |log2FC| > 2, the paper's top-gene rule).** Female 1 (Ddx3y), male 0.
- **Pathways.**
  - Both sexes are enriched for oxidative phosphorylation in EX: Hallmark GSEA NES 3.17 (F) and 2.13 (M), plus KEGG ORA for males (FDR 0.011). This matches S2.5.p2 / FIG6E-F.
  - Male EX also shows TNFa/NF-kB, p53 and interferon Hallmark sets up.
  - The female KEGG "cardiac muscle contraction" result cannot be checked: female ORA had 1 gene, and Hallmark has no such set.

## Deviations

- **Fit layout.** The paper does not say whether each sex was fitted separately. I first ran separate per-sex fits, which gave F 24 / M 0, the reverse pattern of the paper's 1 / 22. One 4-group model reproduces both counts closely and the named genes, so I took it as the paper's route; the separate fits are kept as sensitivity. This is recorded in the design gate's reasoning and candidates.
- **Software.** pydeseq2 instead of R DESeq2, so independent filtering and Cook's handling can differ slightly. This probably explains 26 vs 22 and Mtmr14's NA.
- **Sign convention.** The paper's log2FC is Sedentary minus Exercised (S1.7.p1); our tables use EX vs SED. Directions agree after flipping.
- **Ddx3y caveat.** Ddx3y in female samples looks like low-level male-read contamination or cross-mapping, not a mislabel: female counts are 14-26 (EX) vs 0-5 (SED), against about 2000 in males, and Xist is uniformly high in females. The paper attributes it to cross-reactivity (S2.5.p2). It is recorded in the study caveats.
- **Not run.** The female-vs-male contrasts (FIG7: 896 / 174 DEGs) are sex comparisons, not exercise estimands, so they were rejected as out of scope.

## Tool problems

1. **Transient pydeseq2 failure.** In attempt 2 (`_previous/20261117T230237Z`), the per-sex female fit failed with joblib "A task has failed to un-serialize". `tools/deseq2_tools.py:164` and `:172` hardcode `n_cpus=8`, and the loky workers failed while other runs were using the machine. An identical rerun succeeded. `run_deseq2_analysis` exposes no `n_cpus` argument and has no retry.
2. **Run-level DEG count.** `summary.csv` / `finish.n_deg` reports 1 for this 2-contrast case, which is only the first table. A reader of `summary.csv` would miss the 26 male DEGs.
3. **Inconsistent enrichment status labels.** ORA on a 1-gene list is recorded as `failed` (raised at `tools/enrichment_tools.py:250`). With 0 genes it is recorded as `not_run: 0 input genes` (`tools/case_runner.py:942`). Both cases mean too few genes, so both should be `not_run`.
4. **Shared scratch file (environment, not repo).** A file I wrote in the shared session scratchpad (`exec2.json`) had another run's (PMID33513138) output appended. Final run output is kept in this run directory as `execute_stdout.json`.
