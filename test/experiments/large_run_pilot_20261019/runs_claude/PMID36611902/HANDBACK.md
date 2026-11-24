# HANDBACK — PMID36611902 / GSE221003

**Status: refused at `design` (both cases).** No exercise contrast exists in the sequenced samples.

## What ran
- `case_runner inspect GSE221003` (cached in `data/GSE221003`): two featureCounts integer count matrices — `Acute_Doxo_Heart.csv.gz` (25,416 genes × 40) and `Chronic_Doxo_Heart.csv.gz` (54,658 × 17). There are 57 GSMs, and the only grouping column is `treatment` (Vehicle / Doxo / Doxo beta-NMN 180 or 500 mg/kg).
- `case_runner execute case_spec.json` with two cases, `GSE221003_acute` and `GSE221003_chronic`. The gates `paper_reconstruction`, `ownership`, `alignment` and `matrix` were recorded as valid. `design` was refused. The validator reported 10 records and 0 errors.
  - Acute alignment: an exact match on a key taken from the GEO `description` (`,Heart_<n>`) against the matrix columns `X<n>_counts`. It aligned 40/40 samples (14 Vehicle, 13 Doxo, 13 Doxo-NMN).
  - Chronic alignment: a normalised-key match (`CTRL-17-Heart` = `CTRL.17.Heart`). It aligned 17/17 samples (5 / 6 / 6).
  - Matrix: raw counts in both cases (all values are integers, and GEO `data_processing` says STAR + featureCounts). The paper also used counts with edgeR.

## Why it was refused
The paper is about doxorubicin cardiotoxicity and NMN protection. The heart RNA-seq groups are Ctrl, Doxo and Doxo-NMN only: acute cohort-1 (S2.2.p2) and chronic cohort-3 (S2.2.p4). Exercise appears only as a treadmill exhaustion **test**, used as a functional outcome in chronic cohort-2 (S2.5.p1, S3.7.p1). That cohort was not sequenced, and no group was given exercise or training as an intervention. So an effect of exercise on gene expression cannot be identified from these data. I rejected the drug contrasts (Doxo vs Ctrl, Doxo-NMN vs Doxo) as alternatives, because they do not answer the exercise question.

## DEG counts vs paper
None computed (refused). For reference, the paper reports:
- Acute (padj < 0.05 and FC 1.5, i.e. |log2FC| > 0.5849625; S3.3.p1): Doxo vs Ctrl 3874, Doxo-NMN vs Doxo 2207.
- Chronic (padj < 0.05, no fold-change rule; S3.6.p1): Doxo vs Ctrl 9, Doxo-NMN vs Doxo 0.
- Method in the paper: edgeR TMM with the QL F-test (S2.9.p1).

## Deviations
None. The case stopped before the method gate.

## Tool problems
1. `alignment.key_patterns` requires the regex to match **every** metadata row (`tools/native.py:392`, `derive_columns`). This holds even when the matrix covers only one of the two sub-studies deposited in the GSE. I first had to rerun with a single combined regex, `,(?:Heart_)?(.+?)$`. It would help to have a per-case option that restricts metadata to the matrix's own samples, or that allows non-matching rows.
2. When a refused design gives no `factors`, suitability still runs and reports `not_analyzable` (failed: sample_size, "0/0 comparisons"). That reads as if n were too small, but the real groups have 13–14 and 5–6 samples. It also flags constant library columns (`library_source`, `library_strategy`, ...) as "candidate_covariate crossed with the design factors" when there are no factors (`GSE221003_acute/suitability/suitability.md`). This is cosmetic and did not affect the decision.
3. A heredoc in Git Bash failed on the JSON spec ("unexpected EOF"), so I wrote the spec with the Write tool instead. This was an environment problem, not a repository problem.
