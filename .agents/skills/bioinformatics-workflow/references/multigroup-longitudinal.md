# Multigroup and longitudinal designs

Use this reference when a paper has more than one treatment level, more than one biological factor, or repeated samples from the same subject.

## Decide which design is present

1. **One factor, several levels.**
   - Keep the factor as a k-level categorical variable.
   - Check replication at every level.
   - Run every analyzable comparison from the suitability report, not only one: the planned contrasts as the paper route, the rest as exploratory. Fit one model on all samples (`tools.joint_contrasts`); a two-arm executor refits on two groups and loses power.
   - If different animals were used at each level, there is no repeated measure: a unique animal ID per sample is an identifier, not a blocking term.
2. **Factorial design.**
   - Keep each factor separate.
   - Enumerate observed and missing cells (`native.design_check`).
   - State whether the target is a main effect, a simple effect, or an interaction.
   - A single cell-to-cell comparison is not an interaction.
3. **Longitudinal or repeated measures.**
   - Identify the subject key and verify a unique mapping (`native.pairing_report`).
   - Model time explicitly, with the subject as a blocking term, or difference within subjects (`paired_change`).
   - A pooled timepoint comparison is not a longitudinal analysis.

## Executors

`tools/multigroup_tools.run_multigroup_analysis` handles each design:

| Design | Plan |
|---|---|
| Multi-level | `"analysis_type": "multilevel"`, `"formula": "~ 0 + C(group)"`, one coefficient vector per planned contrast |
| Factorial | `"analysis_type": "factorial"`, a formula with the interaction, contrasts on the named coefficients |
| Paired change | `"analysis_type": "paired_change"` with `subject_column`, `time_column`, `baseline_level`, `followup_levels`, `group_column`, and a formula on the within-subject differences. Subjects without exactly one baseline and one follow-up sample are excluded and listed in `paired_change_pairs.json` |

Input requirements:
- The executor fits limma, so the input must be log-scale.
- For raw counts, use the `log2(CPM+1)` output of `preprocess_counts` and record the transform.
- For FPKM/TPM, use `native.log_transform`.
- The executor rejects raw-count-like or linear-scale input.

## GSE128078-style plan

For disease-by-time data, the usual question is whether trajectories differ between disease groups. The plan needs disease, time, subject blocking, and a disease-by-time interaction, parameterized to full rank (see multifactor-design.md). Useful contrasts include within-group time changes, between-group differences at selected timepoints, and a difference-in-differences. The exact contrasts must follow the paper's Methods.

## Safety checks

- Every observed cell needs enough biological replication for the chosen model.
- A missing cell can make an interaction non-estimable even when several pairwise contrasts are valid.
- Pairing uncertainty is a stop condition (`manual_review`). Adding more groups does not repair a wrong subject mapping.
- Multi-level pairwise results do not prove that the factor, the interaction, or the trajectory effect is valid.
- Record the formula, the coefficient or contrast vector, the blocking term, the multiplicity rule, and every rejected simplification.
