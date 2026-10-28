# HANDBACK: PMID42356398 / GSE319093

**Status: refused at the `design` gate.** The series has no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE319093` downloaded the series into `E:/agent/mwangLab_pdf/data/GSE319093`. It has 62 GSMs and four FPKM-type matrices: `fpkm.anno` (basal GC/SOL F/F vs ChMKO), `ChMKO_Expression_FPKM` (normoxia/hypoxia/HFrD), `AAV-ChREBP` and `C2C12_OE`.
- I read the paper (`PMC13305853.paper.md`). RNA-seq is described in S2.13.p1: DESeq2, |log2FC| >= 1 and p < 0.05, no FDR correction (also S4.3.p4).
  - The sequenced sets are: genotype (S3.2.p2), 2-week hypoxia (S2.3, S3.4.p4-p5), long-term high-fructose diet (S2.4, S3.4.p7-p8), AAV-ChREBP after cardiotoxin injury (S3.3.p2) and C2C12 ChREBP overexpression (S3.5.p2).
  - The only exercise in the paper is a weighted exhaustive swimming test (S2.5; S3.1.p4, Fig 2D-E), read out as swim time and plasma LDH. It was never sequenced.
  - GEO metadata confirm this. The treatment levels are none, Hypoxia, high-fructose diet, AAV and C2C12 OE, and no field mentions exercise, swimming or training.
- `case_spec.json` records these gates:
  - `paper_reconstruction`, `ownership`: owned (DA.p1).
  - `alignment`: exact match on the matrix column name in GEO `description`, through `key_patterns`. 20/20 fpkm.anno columns aligned.
  - `matrix`: FPKM.
  - `design`: **refused**. Each non-exercise contrast is listed as a rejected candidate.
- `execute` finished with 5 records and no contract-validator errors. Case status is `stopped:design`, decision `refused`, execution `not_run`.

## DEG counts vs paper
- None computed, because there is no exercise contrast.
- The paper's threshold is p < 0.05 and |log2FC| >= 1 (raw p, S2.13.p1). Its reported non-exercise counts are 483 HFrD_F/F vs Norm_F/F DEGs, 187 Hypo_F/F vs Norm_F/F DEGs (S3.4.p8) and 224 upregulated C2C12 Ch-OE DEGs (Fig 6E).

## Deviations
- None executed. Recorded discrepancies:
  - **No exercise transcriptomics.** This blocks the estimand.
  - **GSM9510547 mislabel.** Its title says `SOL-WT-59`, but its description maps it to matrix column `SOL_WT_69`. The description was used.
  - **No counts in GEO.** The paper ran DESeq2 on counts, but only FPKM matrices are deposited.

## Tool problems
- `tools/case_runner.py:297` (`_contained_keys`): the match threshold `max(2, len(meta)//2)` is relative to all metadata rows. Here there are 62 GSMs, but the series is split over four matrices, so the 20-column fpkm.anno matrix (20 matched) falls below 31. As a result, inspect reported `alignment_keys: []` for every matrix, even though `description` holds each column name ("Column name in fpkm.anno.csv:GC_KO_59"). The threshold should be relative to `len(cols)`. Workaround: I wrote `key_patterns` by hand.
