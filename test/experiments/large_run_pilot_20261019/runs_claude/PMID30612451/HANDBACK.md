# HANDBACK — PMID30612451 / GSE120958

**Status: refused at `design`** (decision_status `refused`, execution `not_run`). The contract validator ran on 5 records and reported 0 errors.

## What ran
- `case_runner inspect GSE120958`: downloaded the series to `data/GSE120958`. It has two matrices: raw counts (`GSE120958_countTable.txt.gz`, 100% integer) and FPKM. There are 6 samples, NP_1-3 and HP_1-3.
- `case_runner execute case_spec.json`: recorded these gates:
  - `paper_reconstruction`
  - `ownership`: owned.
  - `alignment`: exact match on `title`, 6/6 samples.
  - `matrix`: raw counts, so DESeq2 would be the method.
  - `design`: refused.
- The suitability report found the diet contrast HP vs NP analyzable. That contrast is not the requested estimand.

## Why it was refused
The request was how exercise affects gene expression. GSE120958 contains only a dietary phosphate contrast:
- 12 weeks of high-phosphate diet (2% Pi) vs normal-phosphate diet (0.6% Pi).
- Gastrocnemius muscle, n=3 per group (S4.4.p1, FIG5).

In the paper, exercise is a phenotypic outcome (treadmill VO2 and duration, S4.2.p2), not a factor of the sequenced design. No arm is exercised or trained, there is no pre/post-exercise sample, and GEO has no exercise variable. Running HP vs NP as an "exercise" comparison would misstate the estimand.

## DEG counts vs the paper
- Not run, so there are 0 contrasts to compare.
- The paper reports "over 5,000" DEGs for HP vs NP using DESeq2 with |FC| ≥ 1.5 and raw P < 0.05 (FIG5). That rule is recorded as `paper_threshold`: pvalue < 0.05 and |log2FC| ≥ 0.5849625.
- Genes the paper names:
  - Down: Fabp4, Fabp5, Lipe (Hsl), Fasn, Pparg, Adipoq, Pnpla3.
  - Up: Gck, Hk2, Pgk1, Irs2, Ldha, Slc2a4.

## Deviations
None. No analysis was run.

## Tool problems
None. Inspect, the runner and the validator all behaved as expected.
