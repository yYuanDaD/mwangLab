# HANDBACK: PMID42318351 / GSE277623

**Status: refused at `design`. The data contain no exercise contrast.**

## What ran
- `python -m tools.case_runner inspect GSE277623` (cached data): `GSE277623_raw_count.txt.gz` (17,455 genes x 19 samples, all integers) plus a per-sample `_RAW.tar`.
- `python -m tools.case_runner execute case_spec.json`. Five gates were recorded: paper_reconstruction, ownership, alignment, matrix and design (refused). The validator reported 0 errors and the case route is `stopped`.
  - Alignment: `raw_tar: true`. The tar member names carry GSM ids, so all 19/19 samples matched exactly on the metadata index. `grp` was taken from the GEO title, giving Con5W 3, HF5W 3, Con9W 3, PBS9W 3, EMPAPFD9W 3, EMPA9W 2, PFD9W 2.
  - Matrix: raw counts (HISAT2 + htseq-count, as in S3.9.p1 and GEO data_processing), which is the input the paper gave DESeq2 through iDEP.
  - The suitability report (`GSE277623/suitability/suitability.md`) came back as `partially_analyzable`, with a sample-size warning for the n=2 monotherapy arms. The refusal is about the estimand, not about analyzability.

## Why refused
This paper tests drugs (empagliflozin, pirfenidone, and the two combined, against PBS vehicle) in an L-NAME + high-fat-diet HFpEF rat model (S3.1.p1-p2). All seven sequenced groups are defined by disease, time point or drug. Exercise appears only as a treadmill exhaustion test, used as a functional outcome (S3.5.p1, S4.1.p4). No animal was exercise-trained, so these data cannot estimate an effect of exercise on gene expression.

## DEG counts vs paper
No DE was run. The paper's threshold is FDR < 0.05 and |FC| > 2, i.e. |log2FC| > 1 (S3.9.p1, FIG5 legend). The paper reports these DEG counts (none of them exercise contrasts):
- EMPA+PFD vs untreated: 717 (421 up, 296 down)
- EMPA vs untreated: 52
- PFD vs untreated: 4
- control 9w vs untreated: 295
- vs HFpEF 5w: EMPA+PFD 2954, PFD 1492, EMPA 439, untreated 439

## Deviations
- I used the per-sample `_RAW.tar` (GSM-keyed) rather than the series-level `GSE277623_raw_count.txt.gz`. Both carry the same sample labels, and the tar gives exact GSM alignment without decoding abbreviations.

## Tool problems
- No blocking problems.
- Minor: the series-level matrix column names (for example `Con_5W_1`, `PBS_9W_1`) do not match any metadata field. Inspect reported `alignment_keys: []`, and its vocabulary differs from the GEO titles ("control", "untreated"). One column has a typo (`EMPA_PFD9W_1` against `EMPA_PFD_9W_*`). Using the tar avoided this.
- Side effect: the `raw_tar` merge writes `GSE277623_merged_from_tar.csv` into the shared data cache (`data/GSE277623/`), not only into the run directory.
