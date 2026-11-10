# HANDBACK: GSE60833 / PMC5033478 (endurance training, skeletal muscle memory)

## What ran
- Inspect: `inspect_GSE60833.json`. GSE60833 has 68 samples: U2 (untrained leg after Period 1, 21), T3 (13) and U3 (12), both legs before Period 2, and T4 (10) and U4 (12), both legs after Period 2. T1 and T2 (Period 1, trained leg before and after) are deposited in GSE58608/GSE60590, not in this series.
- Matrix: the per-sample Cufflinks `genes.fpkm_tracking` files in `GSE60833_RAW.tar`, merged by `prep_merge_fpkm.py` into `GSE60833_gene_fpkm_merged.csv` (61,779 Ensembl genes x 68 GSM). 131 duplicated tracking_ids (genes Cufflinks split over several loci) were summed per gene.
- Spec: `case_spec.json`, run with `python -m tools.case_runner execute`. Status completed; validator: 21 records, 0 errors.
- Alignment: exact match on the GSM index. `subject` and `grp` (T3/T4/U2/U3/U4) were parsed from `original sample id`, for example 12T3. Each subject-leg has one biopsy side and each subject one sex. Suitability verdict: analyzable, and the sex check passed.
- Method (declared deviation): limma `~ subject + grp` on log2(FPKM+1), paired with complete pairs per comparison, keeping genes with mean FPKM >= 1 in the fitted samples (about 13.1k genes, close to the paper's 12,848).
  - The paper's route was blocked: OPLS (Simca) with jack-knife loading significance on ComBat-corrected FPKM. There is no executor for it, and the batch labels are not deposited.
- Threshold: `workflow_default`, BH padj < 0.05 with no fold-change rule.
  - The paper's gene rule is |OPLS loading| - |jack-knife 99% CI| > 0 (S4.6.p2), which cannot be converted to a p-value rule.
  - Audit rule: nominal p < 0.01.
- Enrichment: GSEA Hallmark and ORA on the two primary contrasts. ORA was not run for T4 vs T3 because it had 0 DEGs.

## DEG counts vs paper (ours at padj < 0.05; audit count at p < 0.01 in brackets)
| Contrast | n pairs | Ours | Paper (OPLS) |
|---|---|---|---|
| T4 vs T3, Period 2 previously trained leg (primary) | 10 | 0 [409] | 852 |
| U4 vs U3, Period 2 previously untrained leg (primary) | 11 | 6, all up [646] | 928 |
| T3 vs U3, memory before Period 2 (exploratory) | 12 | 0 [531] | 0 (no specific genes) |
| T4 vs U4, after Period 2 (exploratory) | 10 | 0 [36] | no OPLS difference |
| Per-sex splits of both primary contrasts (exploratory) | 5-6 | 0 each | paper: no sex-specific response |

- Direction agrees with the paper:
  - COL4A1, COL4A2, HADHB, PDHA1, COX4I1, COX5A, NDUFB5, SDHB and UQCRC2 all have positive log2FC in both Period 2 legs. HADHB reaches padj 0.048 in U4 vs U3.
  - In both legs, GSEA ranks HALLMARK_OXIDATIVE_PHOSPHORYLATION as the top up-regulated set (NES 3.7 and 3.2, FDR about 0), which matches the paper's OXPHOS finding (S2.5.p1).
- Counts are far below the paper's. The OPLS jack-knife rule has no multiple-testing control, and the paper's data were ComBat batch-corrected; ours were not.
- Period 1 (paper: 2,394 genes) was not analysed, because its samples are outside GSE60833.

## Deviations
- Limma paired moderated t replaces OPLS loading significance, and the workflow-default threshold replaces the OPLS rule.
- No ComBat batch correction, because the sequencing batches are not in GEO. T3 vs U3 has an excess of nominal hits (531 at p < 0.01 against about 130 expected under the null) but 0 at FDR. That pattern points to unmodelled batch, not memory; it is recorded in the study caveats.
- The gene filter is mean FPKM >= 1 per fit, against the paper's > 1 over its own sample set.

## Tool problems
- `tools/native.py:539`: `merge_raw_tar` does not recognise per-sample Cufflinks `*.fpkm.txt.gz` (`genes.fpkm_tracking`) members ("no mergeable per-sample count files"), so a prep script was needed. Cufflinks' duplicated tracking_ids would also need handling.
- `tools/case_runner.py:130-133` vs `:693`: the filter docs describe `min_mean_count` as a raw-count rule, and FPKM only gets `{min_value, min_samples}`. In practice `min_mean_count` computes a plain mean on the deposited values, and that is what was used for the paper's mean-FPKM > 1 rule. The docs and the behaviour disagree, and there is no named `min_mean_value` option for FPKM.
