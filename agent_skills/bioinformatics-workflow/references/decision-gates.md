# Decision gates

## Contrast gate

Use the aligned metadata, not the full GEO metadata, to identify the design. The Python detector may use keyword-grounded columns and values, but a direct keyword match is only a candidate decision. Check that:

- the design column exists;
- control and treatment values are different and present in the expression matrix;
- each arm has adequate biological replication;
- alignment coverage is adequate in both arms;
- the selected column answers the user's biological intent rather than merely containing a familiar word.

The structured contrast validator may confirm, replace, or refuse a proposed triple `(design_column, control_value, treatment_value)`. Validate any returned triple against the metadata before execution. If no defensible contrast remains, stop differential analysis and record `preprocess_ok_no_design` or an equivalent review status.

## Multiple treatment levels

With one baseline and several treatment levels in the same design column, fit the factor with all observed levels, then run only the scientifically planned baseline-vs-level contrasts. Keep each DEG/GSEA artifact and decision record separate, apply a documented multiplicity correction, and do not pool biologically distinct levels into one treatment group. An omnibus test can be reported when the backend supports it; pairwise results do not replace that omnibus question.

With multiple plausible design columns or a factorial design, do not select one arbitrary two-arm contrast as a substitute for the design. Use an explicit multifactor plan naming factors, reference levels, the estimand, planned contrasts, and any interaction. A factor-by-factor pairwise expansion is acceptable only when it answers the stated question; an interaction requires a difference-in-differences or an explicit interaction coefficient.

## Longitudinal and covariance gate

For repeated samples from the same donor, subject, animal, or patient, identify the repeated-measure key and verify that the sample-to-key mapping is complete and unique. Do not treat repeated samples as independent biological replicates. Timepoint is a factor; it is not automatically a covariate to be ignored or pooled.

Use the design that matches the estimand:

- one factor with (k>2) levels: all levels in one model plus planned contrasts;
- factorial design: main effects plus the interaction required by the scientific question;
- repeated-measure time course: subject/donor blocking plus time and, when relevant, factor-by-time interaction;
- missing factorial cells: report the estimable effects and refuse non-estimable interactions.

Before fitting, check replication in every observed cell, missing levels, complete confounding, design-matrix rank, and residual degrees of freedom. If the current backend accepts only a two-arm interface or cannot represent the required covariance, preserve the plan and mark the study for review. Never infer that a successful pairwise p-value validates the original longitudinal or factorial question.

## Covariate gate

Inspect metadata for batch, donor, sex, age, tissue, time, genotype, library preparation, and pairing. Record each relevant candidate and whether it is:

- included in the model;
- excluded with a reason;
- aliased with the treatment;
- unresolved and requiring review.

`tools/multifactor_design.py` validates an explicit plan before fitting: selected-arm replication, missing covariate values, complete confounding, full design-matrix rank, and residual degrees of freedom. DESeq2 accepts additive categorical covariates; limma accepts additive covariates and interactions. edgeR/limma-voom batch dispatch currently fails closed for explicit multifactor plans. Do not describe a result as batch-, donor-, sex-, or time-adjusted unless the fitted tool received that covariate.

## Stop conditions

Stop or mark for review when any of these holds:

- no reliable two-arm contrast;
- sample alignment is unresolved or below coverage threshold;
- a matrix type is ambiguous;
- the requested method is incompatible with the numeric matrix;
- the treatment is completely confounded with a known batch or other covariate;
- the study is observational, prognostic, clustering, or validation-only and no causal contrast is defensible.

Low confidence by itself is not a stop condition. Stop when the unresolved fact changes the matrix route, estimand, sample independence, or method compatibility. For a small but otherwise valid study, keep the planned contrast, mark the result exploratory, and record the replication limitation instead of escalating automatically to `manual_review`.
