# Explicit multifactor designs

Write a design plan only after reading the paper and the aligned metadata and deciding the estimand. Name the factors and reference levels, the repeated-measure key, the blocking and covariance terms, the planned contrasts, and any interaction. Covariates and interactions are never inferred from column names.

## Choosing the executor

| Estimand | Executor | How |
|---|---|---|
| Two arms with additive covariates or subject blocking, raw counts | `run_deseq2_analysis` | `covariate_columns="subject"` (comma-separated). Interactions are refused because a main-effect contrast does not define one |
| Two arms with additive covariates or blocking, log-scale | `run_limma_analysis` | `covariate_columns=...`, or `design_formula` + `coefficient` for a custom model |
| Interaction on log-scale data | `run_limma_analysis` | `covariate_columns` + `interaction_terms="factor:factor"`, or `design_formula` with an explicit `coefficient` |
| Several levels, factorial cells, named contrasts | `run_multigroup_analysis` | patsy `formula` + `contrasts` with coefficient vectors (plan schema in native-execution.md) |
| Within-subject change, optionally compared between arms | `run_multigroup_analysis` | `analysis_type: paired_change` |
| Anything else (for example, random effects or crossed repeated measures across arms) | none | Keep the plan and mark the design `manual_review` |

For two-arm plans, `tools/multifactor_design.build_multifactor_plan` validates the plan before fitting: arm replication, missing covariate values, complete confounding, full rank, and residual df. `run_multigroup_analysis` validates rank and residual df for its formula. Use `native.design_check` before either call to record cells, rank, and df in the covariance or method decision.

A covariate must have complete values in the selected samples. A covariate with one level is dropped and recorded. Complete treatment-covariate confounding, rank deficiency, or zero residual df is a hard stop.

## Example semantic plan (disease by time with repeated subjects)

```json
{
  "factors": {"disease": ["ME/CFS", "Control"], "time": ["day1", "day2", "day3", "day7"]},
  "repeated_measure": "individual_id",
  "blocking": ["individual_id"],
  "interactions": [["disease", "time"]],
  "planned_contrasts": ["ME/CFS day2 vs day1", "Control day2 vs day1", "difference_in_differences"]
}
```

With subject blocking plus `disease × time`, the subject term absorbs the disease main effect. Parameterize so that the design is full rank: keep the subject term, the time effects, and the disease-by-time interaction, and drop the separate disease main effect. Check this with `design_check` before fitting.

## Recording

Record the plan in the `design` decision. Record the fitted formula in metadata column names, together with the coefficient or contrast vector, in the `method` decision. Record rank and residual df in `covariance` or `method`. A successful p-value never overrides a failed design gate.

The external-agent backend accepts the same kind of plan through `run_batch_geo_pipeline(design_plans_json=...)`. Native runs call the executors directly.
