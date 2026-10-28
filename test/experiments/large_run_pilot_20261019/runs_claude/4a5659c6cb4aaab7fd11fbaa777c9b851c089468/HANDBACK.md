# HANDBACK: GSE129694 (PMC7093805, soleus after SCI, inactivity vs exercise)

## Outcome: refused at `design`

The case was refused at the design gate. No DE was run.

The paper's exercise question compares each exercise arm with the unexercised contused arm: CONT SCI + SWIM vs CONT SCI and CONT SCI + SWW vs CONT SCI (Fig. 1b, S2.1.p1, TAB2). That comparison cannot be estimated from these data. Sacrifice time after SCI is completely confounded with exercise:

- every SWIM and SWW animal was collected at 13.5 weeks;
- every CONT SCI animal was collected at 11.5 weeks.

This comes from GEO `characteristics_ch1.*.time` and from paper S2.3.p1 and TAB1. The delay is part of the protocol: exercise needed facility introduction plus 10 weeks of training. No model can therefore separate the exercise effect from two extra weeks of chronic SCI, tiny-cage restriction and age.

The runner's suitability report agrees. It fails the covariance check because time is nested with grp (`GSE129694/suitability/suitability.md`). The runner treats a `not_analyzable` suitability verdict as incompatible with a valid design, so the refusal is recorded at `design`, not `covariance`.

## What ran

- `inspect`:
  - matrix `GSE129694_GeneMatrix_RawCounts_InjuryActivity.txt.gz`: 24,613 Ensembl Rn6 genes x 20 samples, 100% integers, HTSeq raw counts;
  - alignment: exact match on GEO `description`, 20/20.
- Recorded gates: `paper_reconstruction`, `ownership`, `alignment` (grp from `source_name_ch1`; time from the same field, checked against both GEO time columns), `matrix` (raw counts, DESeq2) and `design` (refused).
- The contract validator reported 0 errors. Case status is `stopped:design`.

## Alternatives considered and not run

- **SWIM vs SWW:** both arms are at 13.5 weeks, so this comparison is time-matched. It compares exercise modalities, not exercise vs no exercise, so it does not answer the request. It could be run as an exploratory modality comparison if wanted.
- **Pooled exercise vs CONT:** this pools two distinct modalities, and it is still confounded with time.
- **Injury contrasts (CONT/TX vs No SCI):** these are not about exercise. TX is also confounded with time (8.5 weeks).

## DEG counts vs paper

There is nothing to compare. The paper is a Data in Brief descriptor. It reports no DE analysis, no DEG counts and no threshold (`paper_threshold` is not reported), only QC, PCA and mean expression by GO category. We have no counts because the case was refused.

## Deviations

- The paper's PCA drops CONT SCI rep 3, SWIM rep 2 and SWW rep 2 (S1.p2, Fig. 1c). These were not treated as an exclusion rule. This is moot because of the refusal.

## Tool problems

1. **`inspect` downloads the whole supplementary folder, including a huge `_RAW.tar`, even when a count matrix exists.**
   - The `_RAW.tar` here holds per-sample bigwig tracks of more than 11 GB. Code: `tools/case_runner.py:321-326` → `tools/geo_tools.py:69-78`.
   - `urlretrieve` writes straight to the final path, and skip-if-exists (`geo_tools.py:74-78`) only checks that the file exists. An interrupted download is therefore later treated as complete.
   - **Left in the cache:** my inspect hit its 900 s timeout and left a truncated `data/GSE129694/GSE129694_RAW.tar` (11,646,369,792 bytes). I did not delete it. It should be removed, because a later run would skip re-downloading it or try to merge it.
   - I re-ran inspect with `--no-download`.
2. **`metadata_summary` labels partly empty columns as constant** (`tools/case_runner.py:240-245`: `dropna()` before `nunique()`). `characteristics_ch1.3.time` = "13.5 weeks" exists only for the 8 exercise samples, but it was listed under `constant_columns`. That hides the exercise/time aliasing that decides this case. GEO also splits time across two shifted columns (`ch1.2.time` / `ch1.3.time`).
3. **`derive_columns` cannot recode missing values** (`tools/native.py:376`). In this pandas version, `astype(str)` leaves NaN as NA, so a `"nan"` recode key never matches ("leaves values unmapped: [nan]"). Because of this, two shifted metadata columns cannot be coalesced through `combine` + `recode`. Workaround: time was recoded from `source_name_ch1`.
4. **The suitability verdict is all-or-nothing.** The covariance check fails the whole design (`not_analyzable`) even though it lists 10/10 comparisons as analyzable, including the time-matched SWW vs SWIM. A confounded factor therefore forces refusal at `design`, while the skill's covariate gate rule says a refusal for an aliased covariate belongs at `covariance`.
