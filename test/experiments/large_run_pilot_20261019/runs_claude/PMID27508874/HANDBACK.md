# HANDBACK — PMID27508874 / GSE74570

**Status: refused at the `design` gate.** No exercise contrast exists in the data.

## What ran
- `python -m tools.case_runner inspect GSE74570 --data-root E:/agent/mwangLab_pdf/data`: the series was already cached. It holds 23 GSM samples in `_RAW.tar` (per-sample HTSeq gencode counts) plus 5 DESeq2 result tables. Those 5 tables are not expression matrices.
- `python -m tools.case_runner execute case_spec.json` recorded these gates:
  - `paper_reconstruction`
  - `ownership`
  - `alignment`: exact match on the GSM index, 23/23 samples.
  - `matrix`: raw counts, DESeq2.
  - `design`: `refused`.
- The validator passed with 5 records and 0 errors. Suitability came back `analyzable` with 15 comparisons, but every one is a genotype or age comparison.

## Why refused
- The sequenced groups are WT, mNKO and mNTG (Nampt knockout and overexpression) at 4, 7 and 24 months: WT_m7 4, KO_m7 4, WT_m4 4, OE_m4 3, WT_m24 4, OE_m24 4.
- The paper uses treadmill exercise only as a functional readout (S2.1.p3, S2.2.p2, S2.4.p1, FIG7D). It is never an intervention whose transcriptional effect was sequenced.
- GEO `treatment_protocol_ch1` says all mice were "occasionally subjected to glucose and exercise tolerance tests". That applies to every group, so it is not a factor.
- I considered and rejected three comparisons that link only indirectly to exercise; they are recorded as design candidates:
  - OE_m24 vs WT_m24: better exercise capacity.
  - KO_m7 vs WT_m7: exercise intolerance.
  - WT aging.
- Each of these is a genotype or age effect. Labelling any of them an exercise effect would misstate the estimand.

## DEG counts vs paper
None computed, because the run was refused. For reference, the paper's own RNA-seq results are:
- mNKO vs WT at 7 months: 33% of detected genes (S2.2.p3).
- mNTG vs WT at 24 months: 18 genes at Padj (S2.4.p1, FIG7F).

The paper's exact RNA-seq threshold is in Supplemental Information, which is not available here. The figure legend uses Padj, with "relaxed selection criteria".

## Deviations
None. No analysis was executed.

## Tool problems
- No runner defect was found.
- My first spec had an invalid JSON escape (`\d` inside a regex in a bash heredoc). I fixed it by using `[0-9]+`. This was my error, not the tool's.
- Side effect: the raw_tar merge writes `GSE74570_merged_from_tar.csv` into the shared `data/GSE74570/` cache, not only into the run directory. This is expected behaviour, noted for awareness.
