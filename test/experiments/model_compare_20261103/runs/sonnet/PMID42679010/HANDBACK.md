# HANDBACK PMID42679010 (GSE344550) - Claude Sonnet 5.5

STATUS: refused (at the design gate)

## What ran
- `case_runner inspect GSE344550` (cached data in mwangLab_pdf/data), then `case_runner execute case_spec.json`.
- Gates recorded in order: paper_reconstruction, ownership, alignment (exact on key derived from `description` "Library name: AMn", 30/30), matrix (RPKM), design = refused. Run route: stopped:design. No executions, no enrichment. Validator: 5 records, 0 errors.

## Why refused
- GSE344550 is human monocyte-derived macrophage RNA-seq after infection with four C. parapsilosis isolates (BP 1T/35B, LBP 29T/49B) vs uninfected control, at 3 h and 24 h (FN.p1, S2.7.p1, S4.13.p1). The paper has no exercise, training or physical-activity element; metadata only has strain and time. The requested estimand (exercise effect) is not identifiable; no contrast was manufactured.
- The paper's own question (BP- vs LBP-infected macrophages) is a different estimand and was not run as a substitute.

## DEG counts vs paper
- None computed (case stopped before execution). Paper reports no DEG counts in the text (S6-S9 tables are supplementary). Paper rule: edgeR, ~0 + group:time, |log2FC| > 1 (no FDR stated, S4.13.p1); fgsea on log2FC ranks with Hallmark/C2/GO/M1-M2 sets.

## Deviations
- None from the paper; the case was refused. Matrix note: the deposited file is RPKM (55% integer, GEO says "RPKM normalized transcripts"), whereas the paper used raw counts in edgeR, so even the paper's own contrast could not be reproduced exactly (would need limma-trend on log2 RPKM).
- Suitability report: not_analyzable (covariance, sample_size) on the generic key factor; informational only since the design gate was refused on the estimand.

## Tool problems
- tools/case_runner.py:993: an invalid-JSON spec (bad escape) makes `execute` crash with a raw JSONDecodeError traceback instead of a `spec_error` message (my spec had a bad `\d` escape from my own typing; not a data problem).
- Otherwise none.
