# HANDBACK — PMID34203013 / GSE141827

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
1. `python -m tools.case_runner inspect GSE141827 --data-root E:/agent/mwangLab_pdf/data` (data were already cached) → `inspect_GSE141827.json`.
2. `prep/prep_osc.py` (listed in `prep_scripts`): stripped the 139 `##` OSC header lines from `GSE141827_Level2_table.osc.txt.gz` and kept the 42 `raw.*` CAGE tag-count columns (dropped the `norm.*` columns and coordinates) → `prep/GSE141827_peak_raw_counts.csv` (9,971 TSS peaks × 42 samples).
3. `python -m tools.case_runner execute case_spec.json` → records for `paper_reconstruction`, `ownership`, `alignment` (exact on `title`, 42/42), `matrix` (raw counts, peak level), and `design` (refused). The validator reported 0 errors. The case route is `stopped`.

## Why it was refused
The paper (S2.2.p1) uses tail-suspension hindlimb **unloading** (disuse, 1/3/7 days) followed by **reloading**: the rats are released into their home cage after 7 days of unloading (recovery 1/3/7 days). These groups are compared with active cage controls, with soleus and EDL analysed separately. No group does exercise training or an acute exercise bout. The paper's estimand is disuse atrophy and recovery from it, so an exercise effect cannot be identified from these data. I considered recovery vs control, R1 vs D7 (reloading) and unloading vs control as alternatives and rejected all three (see `design.candidates`). The design itself is analyzable for the paper's own estimand: the suitability report lists 12 analyzable comparisons, 6 phases × 2 muscles, with n = 3 per group.

## DEG counts vs the paper
- None were computed, because the case was refused.
- Paper threshold (S2.7.8.p1): DESeq2 on TSS peaks, BH padj < 0.05 and |LFC| > 1.25. A gene counts as DE if any of its peaks is DE.
- The paper gives its per-phase DEG counts only graphically (Figure 3A, Supplementary ST4). The text states no number; it says only that soleus R1 has the most DEGs.

## Deviations
- The matrix was repaired by a prep script (header stripped, `raw.*` columns selected). Nothing else deviates, since no model was fitted.
- The deposited Level2 table is peak-level with no gene annotation. Even for the paper's own estimand, the paper's peak-to-gene DEG rule would need an annotation step (Ensembl v93 gene regions ±200 nt) that the runner does not have.

## Tool problems
- `case_runner inspect` profiled the `.osc.txt.gz` file wrongly:
  - Its `feature_examples` were header lines (`##ProtocolREF`, `##InputFile`), so the `##` header was not skipped on this path. The header skip in `tools/native.py:218-226` (`read_table`) looks correct, which suggests the inspect path reads the file a different way. I did not confirm which reader it uses.
  - It also reported `start.0base` and `pos` as sample columns, because only `start`/`end` are in `_ANNOTATION_NAMES` (`tools/native.py:239`).
  - It mixed the `raw.*` and `norm.*` columns into one profile (integer_fraction 0.525 → "linear_normalized or estimated_counts").
  - It returned empty `alignment_keys`, even though the titles sit inside the column names (`raw.Lane1.<title>.<barcode>`).
- I worked around this with `prep/prep_osc.py` plus `matrix_column_pattern`.
