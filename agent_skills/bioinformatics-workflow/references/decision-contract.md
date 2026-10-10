# Decision contract

Use one record for each decision gate and one final study record. The record is an audit object, not a copy of the model's prose.

## Required fields

```json
{
  "case_id": "GSE...",
  "stage": "paper_reconstruction|matrix|alignment|design|method|covariance|threshold|execution",
  "evidence": [{"id": "...", "kind": "metadata|matrix|paper|tool_output", "sha256": "..."}],
  "candidates": [{"value": "...", "reason_rejected": "..."}],
  "final": {},
  "paper": {},
  "confidence": "high|medium|low",
  "reasoning": "short evidence-grounded explanation",
  "decision_status": "valid|unresolved|manual_review|refused",
  "execution_status": "not_started|completed|failed|not_run",
  "stop_reason": null
}
```

The `final` object must contain the fields relevant to the stage:

- `paper_reconstruction`: `accessions`, `sample_inclusion`, `sample_exclusion`, `primary_estimand`, `planned_contrasts`, `paper_method`, `paper_formula`, `matrix_scale`, and `paper_threshold` with its evidence locator. Include `paper_data_discrepancies` and their disposition when the deposited data do not exactly match the article.
- `matrix`: `matrix_type`, `already_log_scale`, `recommended_method`.
- `alignment`: `method`, `n_aligned`, `n_metadata`, `coverage`, and any rejected or duplicated IDs.
- `design`: `analysis_type`, `design_column` or `formula`, control/treatment or named contrasts, and the user-intent match.
- `covariance`: `status` (`required|not_required|unresolved`), repeated-measure key, blocking terms, covariates, interactions, and confounding checks.
- `method`: method, matrix-method compatibility result, replication, design rank, and residual degrees of freedom.
- `threshold`: `paper_threshold`, optional `audit_threshold`, metric (`pvalue|padj|FDR`), cutoff, effect metric/cutoff, source evidence, and whether the threshold is contrast-specific.

Use canonical final statuses. `valid` means the plan may proceed; put a small-sample or exploratory limitation in `final` and `reasoning`. `manual_review` means a required fact or executor is unresolved but a review path exists. `refused` means no defensible estimand or safe route is available. Do not invent status strings such as `STOP_UNSAFE` or `plan_approved_no_DE`; use the canonical status and keep that wording in `stop_reason` or a warning field.

## Non-negotiable separation

Score these independently:

1. **Decision correctness**: matrix semantics, alignment, contrast, covariance, and method route are scientifically defensible.
2. **Execution correctness**: the selected tool completed and produced internally valid artifacts.

An execution failure after a valid decision is not an LLM decision error. A p-value produced after an invalid decision is a blocking safety failure even if the command succeeded.

## Paper-first precedence

When paper evidence exists, it is the primary source for the estimand, sample set, control/treatment, design, covariance, method, and threshold. GEO metadata, matrix values, and deterministic validators test whether that paper plan can be implemented. A keyword heuristic or generic workflow default may fill a field only when the paper leaves it unreported, and the record must label that field as a fallback. If paper and data disagree on a scientific gate, preserve both evidence items and record a discrepancy rather than silently choosing the more convenient route.

`paper_threshold` describes the rule used by the article. `audit_threshold` describes a separate common rule used for cross-study comparison or sensitivity analysis. They must never be merged into one unlabeled cutoff. Threshold changes cannot repair an incompatible method, invalid contrast, missing blocking term, or unsafe sample mapping.

## Manual-review rule

Use `manual_review` or `refused` only when a required fact cannot be resolved from the available evidence, the sample mapping is unsafe, the matrix semantics are ambiguous, a confound is completely aliased, or the executor cannot express the validated design. Complexity alone, small `n` alone, or a low confidence score alone is not enough. For a valid small study, run only the pre-specified bounded contrast and label it exploratory.

## Required stop checks

Do not proceed to differential expression if any of these is true:

- raw-count and log/normalized methods are incompatible;
- control/treatment is absent, reversed, or not aligned to the matrix;
- a repeated-measure or donor key is unresolved;
- a required interaction or blocking term is omitted;
- the design is rank-deficient or has no residual degrees of freedom;
- a matrix type or transform is ambiguous;
- the study is observational or otherwise has no defensible causal contrast.

The record must name the failed gate and preserve the evidence used to reach the stop decision.
