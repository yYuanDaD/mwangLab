# Matrix and method policy

## Classification evidence

Decide the matrix type from the numeric profile (`native.profile_matrix`) together with row identifiers, file name, GEO platform or assay hints, and processing notes. Numbers alone are not enough when any of these is plausible: estimated counts, normalized integer matrices, proteomics, or methylation.

## Valid routes

| Matrix type | Route |
|---|---|
| Raw non-negative integer counts | DESeq2, edgeR, or limma-voom; or limma on `log2(CPM+1)` from `preprocess_counts` (record the transform) |
| FPKM/TPM or other linear normalized expression | `log2(x+1)` (`native.log_transform`), then limma |
| Already log-transformed expression (RMA, log2 CPM, log2 FPKM) | limma as-is |
| Linear proteomics intensity | log2 transform, then limma |
| Already-log proteomics intensity | limma as-is |
| Methylation beta | beta-to-M (`run_methylation_da`), then limma |
| Estimated counts | Refuse integer-only methods unless the rounding recipe is documented (`rounding_documented`) |
| Ambiguous | Stop with `manual_review` |

The default raw-count method is DESeq2. edgeR, limma-voom, or a comparison of several raw-count methods must be requested or justified. Proving that the matrix really holds raw integer counts comes before choosing among valid raw-count methods.

When the paper's method needs an input that was not deposited (for example, DESeq2 when only FPKM is in GEO), the paper route is blocked. Keep the `method` decision `valid` for the alternative you will run, and add `paper_route: {"method": "DESeq2 on counts", "status": "blocked", "reason": ...}` to it. Run the alternative as a declared deviation, with `threshold_source: paper_on_deviation_route`, and label the study route `declared_deviation`. Never round FPKM or TPM into integers to satisfy a count method.

## Enforced checks

`tools/analysis_policy.enforce_method_matrix_compatibility` runs inside every executor:

- DESeq2, edgeR, and limma-voom reject missing values, negative values, and non-integer data.
- limma rejects raw-count-like matrices and any matrix with a maximum above 50, which is still on a linear scale.

These checks are a safety net, not the decision. Record the original matrix type and any transform in the `matrix` and `method` decisions; the validator checks that they agree.
