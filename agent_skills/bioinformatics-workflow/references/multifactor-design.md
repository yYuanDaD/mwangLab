# Explicit multifactor plans

Use a plan only after inspecting the aligned metadata and deciding what the biological estimand is. A plan is per accession and may be passed to `run_batch_geo_pipeline` through `design_plans_json`:

```json
{
  "GSE123": {
    "design_column": "condition",
    "control": "vehicle",
    "treatment": "drug",
    "covariates": ["batch", "sex"],
    "interactions": [["condition", "sex"]]
  }
}
```

For a multi-level or longitudinal study, extend the plan conceptually before choosing any pairwise contrast. Record the factors and levels, the repeated-measure key, the covariance/blocking term, the primary estimand, and the planned contrasts. For example:

```json
{
  "GSE_TIMECOURSE": {
    "factors": {
      "disease": ["ME/CFS", "Control"],
      "time": ["day1", "day2", "day3", "day7"]
    },
    "repeated_measure": "individual_identifier",
    "blocking": ["individual_identifier"],
    "interactions": [["disease", "time"]],
    "planned_contrasts": [
      "ME/CFS day2 vs day1",
      "Control day2 vs day1",
      "difference_in_differences"
    ]
  }
}
```

This is a semantic design record. The current two-arm `build_multifactor_plan` helper and batch dispatcher cannot yet execute every such plan. When the backend cannot represent the factors or repeated-measure covariance, fail closed and retain the plan for an implementation or manual-review path; do not silently convert it to one control-vs-treatment comparison.

`design_column`, `control`, and `treatment` are optional when keyword-based contrast detection is already reliable. `covariates` and `interactions` are never inferred from column names. A covariate must have complete values in the selected contrast; a one-level covariate is omitted from the fitted design and recorded. Complete treatment-covariate confounding, rank deficiency, or no residual degrees of freedom is a hard stop.

DESeq2 fits additive categorical covariates and tests the primary treatment contrast. It refuses interaction terms because a main-effect pairwise contrast does not define an interaction estimand. limma can fit additive covariates and interaction terms; pass an explicit `coefficient` when the interaction, rather than the primary treatment effect, is the target. For repeated measures, a donor/subject blocking term is part of the estimand and must be validated as such. The batch dispatcher fails closed for explicit plans sent to edgeR or limma-voom until those backends expose the same validated design interface.

Record the plan, the fitted formula, the backend, and the coefficient in the decision log. A successful p-value does not override a failed design gate.
