# HANDBACK — PMID41736525 (GSE310344, GSE310849)

## Outcome: refused (both cases, at `design`)

The paper studies **disuse**, not exercise:

- **Human (GSE310344):** 9 young adults, 36 vastus lateralis biopsies. Timepoints: Baseline → 2 wk knee-brace immobilization (Atrophy) → ~7 wk return to *normal ambulatory activity* (Recovery) → 2 wk repeated immobilization (Repeated Atrophy). Source: S2.3.p1.
  - Participants were told to avoid strenuous exercise for 24 h before each biopsy.
  - The supervised resistance-training programme was offered only after the study ended and was never biopsied (S2.3.p1).
- **Aged rat (GSE310849):** tetrodotoxin (TTX) block of the common peroneal nerve. Groups: TTX atrophy, recovery after the TTX ran out (habitual cage activity), repeated TTX, sham, and the contralateral right-limb controls (S2.8.p1, S2.9.p1).

No sampled arm receives an exercise bout or a training programme. Calling "recovery" (return to habitual activity) an exercise effect would change the paper's estimand, so both cases were refused at `design`.

Gates recorded in order: `paper_reconstruction`, `ownership`, `alignment`, `matrix`, `design` (refused). No executions or enrichment ran. The contract validator passed: 10 records, 0 errors.

## What ran

- `python -m tools.case_runner inspect` for both series (data downloaded to `data/`).
- `python -m tools.case_runner execute case_spec.json`.
  - Alignment: exact match on the `Library name` key, 36/36 human samples and 24/24 rat samples.
  - The suitability report was generated for both cases (verdict "analyzable" for 6 and 10 non-exercise comparisons). No comparison was run.

## DEG counts vs the paper

Not computed, because both cases were refused. For reference, the paper's threshold is FDR ≤ 0.05 and fold change ≥ 20% (|log2FC| ≥ log2(1.2) = 0.2630344), from S2.14.p1. Its counts:

- **Human (S3.3.p1):**
  - Atrophy vs Baseline: 381
  - Repeated Atrophy vs Baseline: 103
  - Repeated Atrophy vs Recovery: 82
  - Recovery vs Atrophy: 536
  - Recovery vs Baseline: 0
- **Aged rat (S3.5.p1):**
  - Atrophy vs Control: 2106
  - Recovery vs Control: 2008
  - Repeated Atrophy vs Control: 3937

## Deviations and notes (would apply if anyone reruns this as a disuse analysis)

- Neither series deposits raw counts:
  - GSE310344 has Partek CPM only.
  - GSE310849 has Partek DESeq2-normalized counts only.
- So the paper's DESeq2 route cannot be reproduced exactly. limma on log2(x+1) would be a declared deviation.
- Human samples are repeated measures, so `subject` must be a blocking term.
- For the rat data, the paper pools the right contralateral limbs as control and drops sham.

## Tool problems

- **Chromosome column mistaken for gene IDs.** In both Partek matrices the first column is the chromosome. `inspect` reported it as `feature_id_type: "entrez"` with about 28k duplicated IDs. The cause is the rule that treats any all-digit ID as Entrez (`tools/native.py:609`, pattern `^\d+$`). The real gene IDs are in the `Gene Symbol` / `gene_id` columns, so any execution would need `feature_column`.
- **Annotation column counted as a sample.** In the GSE310344 CPM matrix, the `level` column was listed as a sample column: 40 "samples" against 36 in the metadata. The annotation-name list at `tools/native.py:239-242` does not include `level`. This was harmless here because alignment drops unmatched columns.
- **Not a repository problem:** my first attempt to write the spec through a bash heredoc failed on a shell quoting error. I rewrote it with the file-write tool.
