# HANDBACK — PMID34784301 / GSE157712

**Status: refused at `design`. There is no exercise contrast.**

## What ran
- `case_runner inspect GSE157712` (cached data): one matrix, `GSE157712_Muscle_CKD_raw_counts.txt.gz` (58,870 features × 18 samples, 93% integer values). Metadata has 18 samples: Control 7, CKD 7, Dialysis 4.
- `case_runner execute case_spec.json` recorded these gates: paper_reconstruction → ownership → alignment (exact on the bracketed title key, 18/18) → matrix (RSEM estimated counts, from data_processing) → design, which was **refused**. The suitability report ran and found 3 analyzable disease comparisons. The contract validator reported 0 errors. No DE was executed.

## Why refused
- The paper (S4.6.2.p2) plans two DE contrasts: CKD vs healthy controls, and CKD before vs after starting dialysis. Neither one involves exercise.
- Both groups were "highly sedentary" (S2.1.p1). Exercise appears only as background citing other studies (S2.3.p1, S3).
- Strength and endurance are measured outcomes, not interventions. No sample received an exercise intervention.
- The data cannot identify an exercise estimand. I rejected the CKD-vs-Control and Dialysis-vs-CKD comparisons as answers to the exercise question.

## DEG counts vs paper (paper threshold: BH q < 0.05, no fold-change cutoff; S4.6.2.p2)
- CKD vs Control: paper 967 (464 up / 503 down). Not run (out of scope).
- Dialysis vs CKD: paper 0. Not run (out of scope).
- Exercise contrasts: 0 in the paper and 0 here.

## Deviations
None. The case was stopped, so no later gates were recorded.

## Tool problems
- Inspect labels the matrix "linear_normalized or estimated_counts", even though GEO data_processing says RSEM counts. That is reasonable because the values are only 93% integers; I resolved it from the processing notes.
- No tool failures.
