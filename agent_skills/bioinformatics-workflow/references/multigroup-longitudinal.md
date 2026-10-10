# Multigroup and longitudinal designs

Use this reference when a paper contains more than one treatment level, more than one biological factor, or repeated samples from the same subject.

## Decide which design is present

1. **One factor, several levels.** Keep the factor as a (k)-level categorical variable. Require a replication check for every observed level. Use an omnibus model when available and run only planned contrasts, with one FDR procedure covering the declared family.
2. **Factorial design.** Keep each factor separate. Enumerate observed cells, identify missing cells, and state whether the target is a main effect, a simple effect, or an interaction. Do not call a single cell-to-cell comparison an interaction.
3. **Longitudinal/repeated measures.** Identify the subject/donor/animal key and verify that each sample maps uniquely. Model time explicitly and use the subject key as a blocking or covariance term. A pooled timepoint comparison is not a longitudinal analysis.

## GSE128078-style plan

For disease-by-time data, the question is usually whether trajectories differ between disease groups. The plan should contain disease, time, subject blocking, and a disease-by-time interaction. Useful planned contrasts may include within-group time changes, between-group differences at selected timepoints, and a difference-in-differences. The exact contrasts must follow the paper's Methods and stated hypothesis.

## Safety checks

- Every observed cell must have enough biological replication for the chosen model.
- A missing cell can make an interaction non-estimable even when several pairwise contrasts are valid.
- Pairing uncertainty is a stop condition; adding more groups does not repair incorrect subject mapping.
- Multi-level pairwise results must not be interpreted as proof that the factor, interaction, or trajectory effect was valid.
- Record the formula, coefficient/contrast vector, covariance or blocking term, multiplicity family, and rejected simplifications.

The current batch path supports sibling contrasts from one design column and explicit two-arm additive plans. It does not yet provide a universal executor for arbitrary crossed factors and repeated-measure covariance. Preserve such a plan and stop or route to a validated backend rather than reducing it silently.
