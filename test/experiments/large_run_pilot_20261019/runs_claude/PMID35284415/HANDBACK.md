# HANDBACK — PMID35284415 / GSE192982

**Status: refused at `design`. No exercise contrast exists.**

## What ran
- `python -m tools.case_runner inspect GSE192982` (cached data). One processed matrix: `GSE192982_ACS_CHP_ProcessedData_NormalizedCount.txt.gz`. It is deposited as samples x genes (24 x 13,361) with 4 annotation columns.
- `prep_transpose.py` removes the annotation columns and transposes the matrix to genes x samples. Values are unchanged. Output: `GSE192982_log2TMM_genes_x_samples.csv`.
- `python -m tools.case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership, alignment, matrix, design (refused). Contract validator: 5 records, 0 errors. Suitability report: `analyzable`, 3/3 comparisons.

## Decisions
- **Ownership:** S7.p1 names GSE192982. The matrix has 13,361 genes, the same number as S3.1.p1. It has 24 libraries (8 donors x 3 conditions). Processing is Partek STAR/E-M/TMM/log2, as in S2.7.p1.
- **Alignment:** exact match on `title`, 24/24 samples. `donor` is parsed from the title. `cond` and `sex` come from the GEO characteristics.
- **Matrix:** log2(TMM+1) from Partek with low counts filtered. This is non-integer, log-scale data, so the valid route is limma, not DESeq2.
- **Design: refused.** The paper's interventions are all in vitro:
  - cyclic hydrostatic pressure (CHP: 0.9 MPa, 1 Hz, 1 h/day for 3 weeks in a bioreactor);
  - simulated microgravity (SMG) unloading;
  - static culture as control.

  These are applied to engineered meniscus constructs grown from fibrochondrocytes (S2.3.p1). The paper frames them as mechanical loading/unloading for an osteoarthritis and sex-difference model (S1.p6). No organism exercises, so an exercise effect is not identifiable. I rejected treating CHP as an exercise surrogate; the reason is recorded in `candidates`.

## DEG counts vs paper
- None computed, because the case was refused.
- Paper threshold: fold change > 2 (|log2FC| > 1) and q < 0.05 (S3.2.p1).
- Paper counts: CHP vs Static 236 DEGs, SMG vs Static 388 DEGs, 52 shared. Per-sex counts appear only in Fig 5A.

## Deviations
- None executed.
- If mechanical loading itself is wanted, the data could answer it: limma on the deposited log2-TMM matrix with `~ cond` and donor blocking, n = 8 per arm. The paper's method was a Partek ANOVA with donor as a random effect within sex (S2.7.p1).

## Tool problems
- Inspect reports a transposed matrix without flagging it. It reads the deposited file as 24 "features" x 13,361 "samples" and reports `feature_examples` as sample names, gene symbols as `sample_columns`, and `alignment_keys: []`. Inspect could detect the orientation (the feature IDs match metadata titles), or the runner could offer a `transpose` input option. As it is, a prep script is needed.
- Inspect's `constant_columns.data_processing` shows a mojibake character ("maximum 鈮 50.0", where the GEO text is "≤"). The text is decoded with the wrong codec somewhere upstream, in the metadata CSV write or read. This is cosmetic.
