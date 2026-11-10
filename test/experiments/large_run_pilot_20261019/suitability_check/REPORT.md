# Suitability checks on papers from the large run (2026-10-22)

Todo section 2 (2026-10-16 meeting). Code: `tools/suitability.py`, `tools/joint_contrasts.py`, `tools/paper_screen.py`.

## Joint model vs two-arm fits

One DESeq2 model on all samples, each comparison extracted as a contrast (`run_check.py`, `results.csv`). Same thresholds as the run.

| Paper | Comparison | Joint fit | Earlier two-arm fit | Paper |
|---|---|---:|---:|---:|
| GSE308674 | H vs C | 480 | 328 | 474 |
| GSE308674 | HM vs C | 417 | 399 | 414 |
| GSE308674 | L vs C | 858 | 764 | 857 |
| GSE308674 | M vs C | 36 | 49 | 40 |
| GSE164798 | WT acute vs sedentary | 828 | 3828 | 835 |
| GSE164798 | WT acute vs chronic | 1602 | 2028 | 1617 |
| GSE255280 | exercise vs control, vehicle | 189 | 200 | 989 |
| GSE255280 | exercise vs control, KO | 0 | 5 | 517 |

The joint fit reproduces the paper's counts for GSE308674 and GSE164798. GSE255280 stays far below the paper; the joint model does not explain that gap (see PROBLEMS.md).

The report also lists the comparisons the papers did not make (6 extra pairs for GSE308674; genotype contrasts and interactions for GSE164798 and GSE255280). They are in `results.csv` and would run as exploratory.

## Sex check

X/Y genes vs metadata on every aligned matrix (`sex_check_all.py`, `sex_check_all.csv`). 18 of 19 cases agree. GSE179302 has one sample labelled female with high Y-gene expression and no XIST (GSM5413976): a likely mislabel or swap. PMID32625117 has both sexes (31 male, 10 female), so it would get per-sex analyses.

## Screen fixes

On the 46 papers the 2026-10-19 screen called analyzable (`../../paper_screen_20261019/rescreen_suitability.csv`):

- The exercise-design check drops GSE152133 (aging; exercise capacity only measured), GSE253612/GSE252513 (ketogenic diet) and GSE297824 (vessel stretch).
- The value check moves GSE273041 to `normalized_only` (its `raw_counts` file is RPKM) and GSE196147 to `needs_inspection` (decimals that the GEO processing text does not explain). Salmon, RSEM, tximport and fractional featureCounts files stay analyzable as estimated counts.

41 of 46 remain analyzable.

## Gate

The report is part of the `design` gate (contract v3) rather than a new gate: `case.suitability(...)` writes `<case>/suitability/` and a valid design must carry its verdict; `not_analyzable` cannot be valid.
