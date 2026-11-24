# HANDBACK — PMID35689600 / GSE250520

**Status: refused at `design`** (decision_status `refused`, route `stopped`). The validator reported 0 errors across 5 records.

## What ran
- `python -m tools.case_runner inspect GSE250520` used the cached data in `E:/agent/mwangLab_pdf/data/GSE250520`.
- I read the paper (PMC9350263.paper.md): ABS.p1, S2.1.p2, S2.6.p2, S5.p1–p2, DA.p1.
- `case_spec.json` recorded these gates: paper_reconstruction → ownership → alignment → matrix → design (refused). `execute` completed.
- Alignment was an exact match on a key taken from the GEO title (`^cardiac organoids, (.+)$`). All 6 samples matched (6/6): VEH 3, IL1B 3. Suitability: analyzable for IL1B vs VEH, but that is not an exercise contrast.
- No DE executions and no enrichment were run.

## Why refused
- The RNA-seq in GSE250520 covers only 3 vehicle and 3 IL-1β organoid pools, at day 4 of treatment (COVID-19 cytokine-storm model).
- The paper's "simulated exercise" is a norepinephrine stress test (S2.6.p2, FIG7d–g). It measures beating rate and FAC only, and there is no transcriptome for it. GEO has no NE, D14 or exercise samples.
- No exercise estimand can be identified from these data. I deliberately did not run IL-1β vs vehicle as a substitute.

## DEG counts vs paper
- None computed.
- The paper gives no DEG count and no RNA-seq DEG threshold. It shows only the volcano plot in FIG2d. S5.p2 gives a generic t-test rule of p<0.05 for the non-omics assays.
- I recorded the paper threshold as "not stated".

## Deviations
None. The case stopped before any method was chosen.

## Tool problems / observations
- `data/GSE250520/GSE250520_il1b_rawcounts_041621.csv`, line 2: the xlsx→csv conversion kept a second header row as a data row. It holds `EnsembleID` and fastq names. Inspect still reported `integer_fraction 1.0` but also `missing_values: 6`, and listed `EnsembleID` as a feature ID. The matrix profile does not flag a non-numeric data row. If this matrix is ever used, it needs a prep script that drops that row. This did not affect the refusal.
- Nothing else to report.
