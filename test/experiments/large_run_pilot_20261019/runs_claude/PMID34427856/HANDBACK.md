# HANDBACK — PMID34427856 / GSE165110

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE165110 --data-root E:/agent/mwangLab_pdf/data` downloaded the series. It holds one matrix, `GSE165110_18294R_counts.txt.gz`: 55,487 Ensembl genes × 12 samples, all integers. The GEO metadata has 12 samples.
- `python -m tools.case_runner execute case_spec.json` recorded these gates:
  - `paper_reconstruction`, `ownership`, `alignment` (exact match on a key taken from `title`, 12/12 samples), and `matrix` (raw counts, DESeq2-compatible).
  - `design`: `refused`.
- The validator found 0 errors in 5 records. The suitability report said the STEM-vs-HS split was analyzable (6 vs 6), but that split is not an exercise estimand.

## Why refused
- **What was sequenced:** GSE165110 contains only C2C12 myotubes treated for 24 h with 4% STEM secretome or 4% horse serum (S2.6.p1–p2, Fig. 8B).
- **The mouse experiments:** the paper's in vivo arms are ambulatory control, 14 days of hindlimb unloading (disuse), and unloading plus 7 days of recovery, each with PBS or STEM (S2.1.p1, S2.3.p1). They were assessed only by histology, muscle mass and grip strength, never by RNA-seq.
- **Conclusion:** no exercise or training factor exists in the study. A secretome-versus-serum contrast in cultured cells cannot estimate the effect of exercise.

## DEG counts vs paper
- None computed (refused).
- The paper's own threshold is DESeq2 at 5% FDR (adj. P ≤ 0.05), with no fold-change cutoff (S2.7.p1).
- The paper's text gives no total DEG count. It names Igfbp3, Col23a1, Col14a1, Mt2, Mt1 and Fmod as regulated genes (S3.4.p1), and shows the top-20 up and down genes in Fig. 8B.

## Deviations
- None. The paper's own contrast (STEM vs HS in C2C12, DESeq2) is executable on these data. It was deliberately not run because it does not answer the exercise request.
- It is recorded as a rejected candidate in the design gate.
- Minor metadata discrepancy, recorded only: the paper says RNA was extracted with Qiazol and the miRNeasy kit, while GEO says Trizol.

## Tool problems
- None blocking.
- Minor: `inspect` lists `characteristics_ch1.2.treatment` as the only grouping column. It gives no hint that the study has no exercise factor, so the agent has to judge that from the paper. This is expected behaviour, not a bug.
