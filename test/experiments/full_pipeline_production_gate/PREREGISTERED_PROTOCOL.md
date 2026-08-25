# Preregistered Protocol: Full Pipeline Six-case Preflight

## Evaluation unit

One cached GEO study processed by the production batch pipeline from matrix selection through
QC, sample alignment, contrast detection, differential analysis, Hallmark GSEA, evidence, and
reporting. Acquisition is validated by frozen SHA-256 hashes rather than a live re-download.

## Frozen cases

Exactly six studies are selected before execution:

1. GSE279359 — raw counts, acute exercise versus pre-exercise.
2. GSE208615 — linear FPKM, trained condition versus sedentary baseline.
3. GSE297707 — raw counts with prefix-collision sample labels.
4. GSE163356 — human logCPM, post versus pre exercise.
5. GSE164798 — raw counts with chronic and acute contrasts versus sedentary.
6. GSE326587 — raw counts with semantic sample abbreviations requiring LLM alignment.

The generated manifest freezes the selected expression file, metadata file, SHA-256 hashes,
matrix type, contrast set, method, and expected sample count.

## Hard gates

A case fails if any of the following occurs:

- an input hash changes;
- the wrong expression matrix is selected;
- raw counts are not routed to DESeq2, or non-raw values are not routed to limma;
- the design column, control, treatment set, or contrast count differs from the frozen manifest;
- sample alignment fails, or GSE326587 does not exercise the semantic LLM fallback;
- the batch status is not `deg_gsea_ok`;
- DEG sanity is not `ok`;
- a required DEG, GSEA, QC, decision, or run-status artifact is missing;
- a root evidence reference dangles, an artifact is missing, or an artifact hash mismatches;
- an executed structured LLM call lacks measurable token usage or a priced cost estimate.

The following deterministic negative probes must also pass:

- DESeq2 rejects fractional normalized values;
- limma rejects obvious raw integer counts;
- a two-arm design with fewer than two replicates in either arm is rejected.

## Acceptance

The six-case preflight passes only when all six cases pass all hard gates, all three negative
probes reject correctly, root artifacts are complete, and the independent audit reports no
blocking findings with at least 85% evidence coverage.

This preflight alone does not qualify the whole pipeline for production. It is the required
entry gate for a frozen 20-study x 3-repeat cached benchmark plus a separate live-acquisition
integration gate.

