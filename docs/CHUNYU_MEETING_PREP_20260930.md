# Chunyu meeting preparation — 2026-09-30

## Meeting objective

Use the 30-minute discussion to freeze the single-cell analysis design before presenting the results as a biological conclusion. The key decision is whether the primary analysis should be **cell-type-specific, donor-level pseudobulk with a donor-paired model**, with cell-composition changes reported separately.

## 60-second opening

> I have a working single-cell pseudobulk pipeline on the Kang dataset. It aggregates cells within each donor × cell type × condition, so cells are not treated as independent biological replicates. The engineering run is stable and the expected interferon response appears across cell types. However, the current benchmark used `~ condition`; it has not yet included the donor blocking term required by the paired design. I would like to use today’s meeting to confirm the primary model, the rule for incomplete donor pairs, and which metadata/covariates we should freeze before rerunning the formal result.

## Evidence to show

### Dataset and current run

- Kang et al. 2018, GSE96583: 24,673 cells, 15,706 genes, 8 donors; paired control/stimulated PBMC design.
- Input: [`kang_2018.h5ad`](../data/scrna_demo/kang_2018.h5ad). The `.X` matrix is sparse integer-like counts and agrees with `nCount_RNA`, so it is suitable for count-level pseudobulk.
- Current summary: [`scrna_pseudobulk_summary.csv`](../output/scrna_kang_latest_20260923/scrna_pseudobulk_summary.csv).
- Current run output: [`scrna_kang_latest_20260923`](../output/scrna_kang_latest_20260923/).

### What the current run shows

| Cell type | Pseudobulk samples | Control / stim | DEG (`padj < 0.05`) | Status |
|---|---:|---:|---:|---|
| CD4 T cells | 16 | 8 / 8 | 973 | completed |
| CD14+ Monocytes | 16 | 8 / 8 | 3,428 | completed |
| B cells | 16 | 8 / 8 | 760 | completed |
| NK cells | 16 | 8 / 8 | 459 | completed |
| CD8 T cells | 14 | 6 / 8 | 164 | incomplete donor coverage |
| FCGR3A+ Monocytes | 16 | 8 / 8 | 1,162 | completed |
| Dendritic cells | 16 | 8 / 8 | 879 | completed |
| Megakaryocytes | 2 | 1 / 1 | — | correctly skipped: too few samples |

Across the seven analyzable cell types, IFN-γ and IFN-α Hallmark programs are among the strongest positive signals, which is directionally consistent with IFN-β stimulation. This supports the pipeline and biological direction; it is not yet a formal reproduction of the paper because the donor block has not been fitted.

### Separate bulk benchmark point, if Chunyu asks

For the MH-vs-MC benchmark, 88 shared significant genes have Pearson and Spearman correlations of 1.00 and 100% directional agreement. The lower all-gene Pearson is driven mainly by four sparse, high-leverage digestive-enzyme genes: `Try4`, `Ctrb1`, `Cpa1`, and `Prss2`. Keep this as a sensitivity-analysis example, not as a single-cell result. Diagnostic table: [`mh_vs_mc_88_gene_diagnostic.csv`](../output/rnaseq_zip_remote_ab/mh_vs_mc_88_gene_diagnostic.csv).

## Proposed analysis design to put on the table

1. **Primary differential analysis:** analyze each annotated cell type separately; sum raw counts within each donor × cell type × condition; use a donor-blocked paired model, conceptually `~ donor + condition` (the current implementation uses donor-blocked limma when `paired=True`).
2. **Pair eligibility:** primary result uses donors with both control and stimulated profiles and at least the agreed minimum number of cells in that cell type. Report the number of complete pairs for every cell type.
3. **CD8 sensitivity analysis:** keep the primary complete-pair rule explicit. Separately report the available 6/8 control and 8/8 stimulated coverage if Chunyu believes the imbalance is biologically acceptable; do not silently treat it as a complete paired design.
4. **Small cell types:** keep the fail-closed rule for Megakaryocytes (1 vs 1 is not enough for formal DA).
5. **Cell composition:** calculate/report donor-level cell-type proportions as a separate analysis. Do not mix composition changes with within-cell-type expression changes.
6. **Pooled result:** if desired, use a pooled result only as a secondary descriptive analysis. Do not run per-cell differential tests that treat cells as independent replicates.
7. **Annotation/QC scope:** the current run consumes the supplied `cell_type` labels; it does not independently perform cell calling, doublet detection, clustering, or annotation. Confirm whether that scope is acceptable for the benchmark.

## Questions to resolve with Chunyu

### Statistical design

- Should the formal primary model be donor-blocked/paired for every cell type?
- Should incomplete donor pairs be excluded from the primary result and shown only in a sensitivity analysis?
- What minimum number of donors and minimum cells per donor × cell type should be required?
- Are batch, sequencing lane, sex, disease status, or other covariates available and required?

### Biological reporting

- Should the headline result be cell-type-specific, with pooled results secondary?
- Should cell-composition changes be a separate figure/table?
- Which cell types are biologically primary for the project, and which are exploratory?
- Should the benchmark compare DEG counts, log-fold changes, pathway NES, or all three?

### Input and validation

- Is the supplied `cell_type` annotation the accepted benchmark annotation, or should annotation/QC be redone?
- Is `.X` the frozen raw-count layer for comparison with the reference result?
- Is there a paper-level DEG/GSEA reference with fixed contrast direction, filtering, and thresholds?

## Recommended 30-minute agenda

| Time | Topic | Desired outcome |
|---:|---|---|
| 0–3 min | Goal and scope | Agree that the meeting is to freeze the formal single-cell design |
| 3–8 min | Current run | Confirm what the pseudobulk result does and does not establish |
| 8–18 min | Primary model | Decide cell-type-specific donor-paired model, pair rule, and covariates |
| 18–24 min | Composition and sensitivity | Decide whether to report composition separately and how to handle CD8 |
| 24–28 min | Reference and QC | Freeze annotation, count layer, thresholds, and comparison metrics |
| 28–30 min | Next actions | Assign rerun, plots, metadata cleanup, and follow-up with Meng/Bo |

## Papers to have open

- [Kang et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5784859/) — paired donor and cell-type-specific context.
- [Crowell et al. 2020, muscat](https://doi.org/10.1038/s41467-020-19894-4) — multi-sample, multi-condition differential-state analysis.
- [Squair et al. 2021](https://doi.org/10.1038/s41467-021-25960-2) — pseudoreplication and false positives from treating cells as independent replicates.
- [Zimmerman et al. 2021](https://doi.org/10.1038/s41467-021-21038-1) — practical handling of sample-level replication.

## Decision record to fill in during the meeting

- Primary estimand: ______________________________________________
- Primary model/formula: _________________________________________
- Complete-pair rule: ____________________________________________
- Minimum donors/cells: __________________________________________
- Covariates: ____________________________________________________
- Cell-composition analysis: ______________________________________
- Frozen annotation/count layer: _________________________________
- Reference metrics and thresholds: _______________________________
- Owner and date for paired rerun: ________________________________

## After-meeting deliverables

1. Record the decisions above in the benchmark protocol.
2. Rerun Kang with the agreed donor-paired model and complete-pair rule.
3. Produce one compact table per cell type with donor coverage, effect size, adjusted p-value, and pathway results.
4. Add a separate composition table/figure if requested.
5. Send Meng a short update that distinguishes the completed engineering benchmark from the formal paired analysis still in progress.

## Do not say yet

- Do not call the current `~ condition` output a formal Kang paired-design reproduction.
- Do not treat the DEG counts as directly comparable to the paper until contrast direction, annotation, filtering, donor rule, and reference thresholds are frozen.
- Do not interpret the absence of a result in Megakaryocytes as biological absence; it was skipped because replication was insufficient.
