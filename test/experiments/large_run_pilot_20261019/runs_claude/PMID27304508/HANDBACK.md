# HANDBACK — PMID27304508 / GSE75919

**Status: refused at `design`** (validator: 5 records, 0 errors).

## What ran
- `case_runner inspect GSE75919` (series downloaded into `data/GSE75919`): 9 GSMs, one grouping column (genotype: Gprc6a fl/fl = 5, Gprc6a fl/fl;Mck-Cre = 4). `source_name_ch1` is the same for every sample: "gastrocnemius muscles of 3 month old mice after exercise".
- `prep_counts.py` converted the deposited `GSE75919_Gpc6arna_seq_raw.xlsx.gz` (sheet `Gpc6acounts.txt`, 23,284 genes × 9, integer HTSeq counts) to `GSE75919_counts.csv`. Values were not changed.
- `case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership, alignment (exact match on `description`, 9/9), matrix (raw counts), and design, where the case was refused. Suitability rated the only possible comparison (genotype KO vs WT) analyzable, but I refused it on scope.

## Why refused
The paper's RNA-seq (S2.5.p1, S4.3.p1) compares Gprc6a_Mck−/− with Gprc6a fl/fl mice, and all of them were sampled after a single treadmill bout. No rested or sedentary group was sequenced. That means the effect of exercise on gene expression, and any genotype × exercise interaction, cannot be estimated from this series. The only contrast available is genotype within exercised mice, and that is not an exercise effect. The paper studied the exercise effect itself (Il6 induction) only by qPCR and ELISA (Fig 6B–G), not by RNA-seq.

## DEG counts vs paper
- No DE was run. The paper gives no DEG count and no threshold in the main text: the RNA-seq methods are in the supplemental information, which was not available. Its named results are Il6 (most decreased, about 80%, in KO after exercise) and Il6ra (modest decrease), Fig 6A/S6A.
- Paper threshold: not stated. No threshold was applied.

## Deviations
- None executed. The genotype-under-exercise contrast was rejected as a candidate (recorded in design `candidates`) because it does not answer the exercise question.

## Tool problems
- `tools/case_runner.py:54` / `:360-363`: `inspect` reported `matrices: []` for this series. `_EXTENSIONS` lists `.xlsx` and `.xls.gz` but not `.xlsx.gz`, so GEO's gzipped Excel supplement (`*_raw.xlsx.gz`) is never profiled. I needed a manual prep script to get the matrix. Fix: add `.xlsx.gz` and read it through gzip + `pd.read_excel`.
- Minor: the GEO title/genotype strings have typos ("Gprc5a-/-", "Grpc6a", "b3Gprc5a-/-" with no dot). Alignment used `description`, which is clean, so nothing was affected.
