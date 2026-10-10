# Matrix and method policy

## Classification evidence

Use numeric profile, row identifiers, filename, GEO platform/assay hints, and nearby processing notes. Numeric appearance alone is insufficient when estimated counts, normalized integer matrices, proteomics, or methylation are plausible.

## Valid routes

| Matrix type | Route |
|---|---|
| Raw non-negative integer counts | DESeq2, edgeR, or limma-voom |
| FPKM/TPM or other linear normalized expression | log2(x+1), then limma |
| Already log-transformed expression | limma as-is |
| Linear proteomics intensity | log2 transform, then limma |
| Already-log proteomics intensity | limma as-is |
| Methylation beta | beta-to-M transformation, then limma |
| Estimated counts | Refuse integer-only methods unless the exact rounding/count recipe is documented and validated |
| Ambiguous | Stop and request evidence or manual review |

The default raw-count method is DESeq2. `edgeR`, `limma-voom`, or a multi-method raw-count comparison must be explicitly requested or selected by the configured method policy. Method choice among valid raw-count backends is secondary to proving that the matrix is raw integer counts.

## Required checks

Before fitting, apply the shared analysis policy. Raw-count backends must reject missing/non-finite values, negative values, and non-integer-like values. Plain limma must reject clearly raw-count-like matrices. Record both the original matrix type and any generated transform artifact.

If an LLM classification is used, record its confidence, reasoning, provenance snippet, and whether it changed the heuristic route. Low-confidence or ambiguous semantic classifications must not be silently routed to a method.
