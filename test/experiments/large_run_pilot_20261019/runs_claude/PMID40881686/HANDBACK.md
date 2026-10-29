# HANDBACK: PMID40881686 / GSE272928

## What ran
- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`). Validator: 16 records, 0 errors. Case status: completed, route `declared_deviation`.
- Input: the only matrix deposited, `GSE272928_transformed_RNA_seq_Data` (csv copy of the series xlsx). 63,677 Ensembl genes x 36 samples (9 ALL-in-remission + 9 control children, baseline and peak exercise each).
- Prep: `prep/rename_columns.py` renames the matrix columns by name (`ALL02_BASELINE` -> `ALL_02_BASELINE`) so they equal a key built from the GEO title. Alignment was an exact match on that key, 36/36.
- Matrix decision: DESeq2 rlog-transformed log2 values. The evidence: the file is named "transformed", values are continuous from -4.38 to 18.9, all-zero genes are exactly 0, near-zero genes share a floor of about -4.375, and sum(2^x) per sample is stable at about 2.7e7. The raw-count file the submitter names in `data_processing` (`all_merged.txt`) was never deposited, so DESeq2 cannot run.
- Design: 2x2 mixed design (group between subjects, time within subjects), with subject as the blocking unit.
  - Exercise contrasts: per-child post minus pre deltas, then limma `~ 0 + C(grp)` with three contrasts: interaction (ALL change minus CON change), ALL post vs pre, and CON post vs pre.
  - Baseline ALL vs CON: limma on the pre samples.
  - Exploratory: post-exercise ALL vs CON, and a male-only paired change (7 vs 7). Females (2 per group) are too few to analyse separately.
- Threshold: the paper's own rule, raw p < 0.01 with no fold-change cut (S2.6.p2), applied as `paper_on_deviation_route`. Audit rule: BH FDR < 0.05.
- Enrichment: GSEA on MSigDB Hallmark completed for the interaction and for ALL post vs pre. ORA for the interaction was not run, because the audit rule (FDR < 0.05) leaves 0 genes.

## DEG counts vs paper (p < 0.01, no FC)
| Contrast | Ours (up/down) | Paper (up/down) |
|---|---|---|
| Interaction ALL change vs CON change (primary, S3.p3) | 194 (110/84) | 179 (16/163) |
| Baseline ALL vs CON (S3.p2, associational) | 265 (84/181) | 284 (124/160) |
| ALL post vs pre (Suppl. S6) | 5172 (2301/2871); FDR<0.05: 4490 | not stated in text |
| CON post vs pre (Suppl. S7) | 4260 (2091/2169); FDR<0.05: 3333 | not stated in text |
| Exploratory: post ALL vs CON | 454 | not reported |
| Exploratory, male only: interaction / ALL / CON | 276 / 4596 / 3199 | not reported |

- Totals are close to the paper's, but the direction split of the interaction does not match: the paper reports 91% negative, ours is 43% negative.
- Interaction and baseline have 0 genes at FDR < 0.05. The paper's raw-p rule has no multiple-testing control.
- Named genes, checked by Ensembl ID:
  - IL1B in ALL: -0.62 log2FC, p = 0.003 (paper -1.68, p < 0.001).
  - IL1B in CON: -0.08, p = 0.68 (paper -0.18, p = 0.59).
  - TREM1, S100A8, S100A9 and S100A12 drop in ALL (log2FC -1.37 to -1.51, p <= 0.0005). This agrees with S4.p4-p5.
  - Interaction genes IL1B, TREM1, TLR2, TLR8 and CD14 are all negative, as in the paper, with p 0.015-0.048. They reach p < 0.05 but not p < 0.01.
  - rlog shrinkage explains the smaller fold changes.
- Pathways: Hallmark inflammatory response is negatively enriched in both the interaction (NES -2.03, FDR 0.0005) and ALL post vs pre (NES -2.02). This matches the paper's inhibition of inflammatory pathways in IPA (S3.p3, Table 3). IPA itself is proprietary and was not reproduced.

## Deviations
1. limma on the deposited rlog matrix instead of DESeq2 on HTSeq counts. Raw counts are not in GEO; `paper_route` is recorded as blocked.
2. The interaction is fitted as paired deltas, which is equivalent to subject fixed effects. The paper used a DESeq2 interaction model.
3. The executor drops zero-variance rows (27,341 all-zero genes).
4. Exploratory additions not in the paper: a post-exercise group contrast, and the male-only split taken from the suitability `split_plan`.

## Tool problems
- `references/case-spec.md` (Executions table, limma row) says limma takes the same args as DESeq2, which include `alpha`. `tools/limma_tools.py:17` `run_limma_analysis` has no `alpha` parameter, so the first execute failed with a TypeError. Fixed by removing `alpha`.
- Suitability report (`GSE272928/suitability/suitability.md`) gives the data-type route as "limma on log2(x+1)" and asks for an "FPKM/RPKM/TPM matrix" for an rlog matrix that has negative values. The wording is misleading, but no transform was applied.
- Interaction ORA is `not_run: 0 input genes`. This is expected under the documented raw-p to audit-rule substitution, but it means no ORA can run under the paper's own threshold.
- `alignment.key_patterns` joins regex groups with `_` and cannot express `ALL02` next to `CONT 51`. A name-only column-rename prep script was needed.
