# HANDBACK — PMID37996046 / GSE235942

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE235942` (cached data): 1 matrix `GSE235942_raw_counts.txt.gz`, 32,544 gene symbols × 30 samples, all integer values; metadata matched exactly on the `description` column (30/30).
- `python -m tools.case_runner execute case_spec.json`: I recorded gates paper_reconstruction → ownership → alignment → matrix → design. The design gate is `refused`. The contract validator passed (5 records, 0 errors). The suitability report gave `analyzable` for the 5 HLU/age comparisons with no sex warnings. That only describes the data; it is not an exercise estimand.
- No DE executions and no enrichment were run.

## Why refused
The paper (ABS.p2, S2.1.p1, Table 1) compares **hindlimb unloading (HLU, i.e. disuse)** with **aging** in C57BL/6J mice. GEO has `treatment` = control (22) / HLU (8) and age = 6 mo (14) / 22 mo (16); 7 of the samples are female controls. The study has no exercise, training or mechanical-loading arm. Exercise comes up only as background (S1.p1, S4.p8). Neither HLU vs control nor 22 mo vs 6 mo identifies an effect of exercise. Relabelling disuse as "the opposite of exercise" would replace the requested estimand with a different one.

## DEG counts vs paper
- Paper threshold (S3.3.p2): "logFC > |1.5| and p-value < 0.05". This is raw p with no FDR, run in limma on BioJupies kallisto counts with logCPM (S2.4.p1). The text gives no DEG counts; only volcano plots (Fig 5G–I) show them.
- Ours: none computed (case refused). 0/0 contrasts.

## Deviations / notes
- GEO holds samples the paper does not describe: 7 female controls (6 and 22 mo) and 3 male 22 mo HLU samples. The paper's 4 mo HLU group comes from a prior study and is not in this series. I recorded this as a discrepancy and did not act on it, because the case stops first.

## Tool problems
- No tool defects. One self-inflicted issue: a bash heredoc collapsed `\\d` into `\d` in the spec's regex, which made the JSON invalid (`tools/case_runner.py:1115` raised a bare JSONDecodeError traceback rather than a `spec_error`). I fixed it by using `[0-9]`. A small usability gap: `execute` could report a malformed spec as `spec_error` instead of a traceback.
