# Decision gates

## Contrast gate

Identify the design from the aligned metadata, not the full GEO table. A keyword match such as `exercise`/`control` is a candidate, not a decision. Check that:

- the design column exists;
- control and treatment values are different and present in the aligned samples;
- each arm has biological replication;
- alignment coverage is adequate in both arms;
- the selected column answers the requested biological question rather than merely containing a familiar word. For example, a genotype contrast does not answer an exercise question.

Record rejected alternatives in `candidates`. If no defensible contrast remains, the design gate is `refused`.

In the external-agent backend (`run_batch_geo_pipeline`), the structured validator in `tools/llm_helpers.py` may confirm, replace, or refuse a proposed triple. Native runs do not use it. The agent session makes this decision.

## Multiple treatment levels

With one baseline and several levels of the same factor, fit one model with all observed levels and run only the planned baseline-vs-level contrasts (`run_multigroup_analysis`). Rules:

- Keep each contrast's results and records separate.
- Apply BH within each contrast unless the paper states a family-wide rule.
- Never pool biologically distinct levels into one treatment group.
- No executor currently provides an omnibus F-test; do not claim one.

With several plausible design columns or a factorial design, do not choose one arbitrary two-arm contrast as a substitute. Write a plan naming the factors, reference levels, estimand, planned contrasts, and any interaction. An interaction requires an explicit interaction coefficient or a difference-in-differences.

## Longitudinal and covariance gate

For repeated samples from the same donor, subject, animal, or patient:

- Identify the repeated-measure key.
- Check that the mapping is complete and unique (`native.pairing_report`).
- Never treat repeated samples as independent biological replicates.
- Timepoint is a factor, not a covariate to ignore or pool.

Match the model to the estimand:

| Design | Model |
|---|---|
| One factor with k > 2 levels | All levels in one model, plus planned contrasts |
| Factorial | Main effects plus the interaction the question needs |
| Two-timepoint paired | Subject blocking (`covariate_columns=subject`) or `paired_change` |
| Repeated-measure time course | Subject blocking plus time and, when relevant, factor-by-time interaction |
| Missing factorial cells | Report estimable effects; refuse non-estimable interactions |

Before fitting, check replication in every cell, missing levels, complete confounding, rank, and residual df (`native.design_check`). If no executor can represent the required covariance, preserve the plan and mark the design `manual_review`. A successful pairwise p-value never validates a longitudinal or factorial question.

## Covariate gate

Inspect metadata for batch, donor, sex, age, tissue, time, genotype, library preparation, and pairing (`native.confounding_report`). When a covariate is aliased with the treatment, record the covariance gate as `refused` with `final.status: unresolved` and the covariate's disposition `aliased`. Record each relevant candidate and whether it is:

- included in the model;
- excluded, with a reason (for example, a single level);
- aliased with the treatment (complete confounding);
- nested in the treatment (for example, animals in between-animal arms; they cannot be blocked);
- unresolved and requiring review.

The executors handle adjustment as follows:
- DESeq2 accepts additive categorical covariates.
- limma accepts additive covariates, interactions, and explicit formulas.
- edgeR and limma-voom have no covariate interface, so use DESeq2 or limma when adjustment is required.

Do not describe a result as batch-, donor-, sex-, or time-adjusted unless the fitted tool received that term.

## Stop conditions

Stop (record a blocked status) when:

- no defensible contrast answers the request;
- sample alignment is unresolved or below coverage;
- the matrix type is ambiguous;
- the method is incompatible with the numeric matrix;
- the treatment is completely confounded with a known batch or other covariate;
- the study is prognostic, clustering, or validation-only, so no comparison answers the request.

A cross-sectional comparison that the paper defines (for example trained versus untrained people) is not a stop: keep it `valid`, set `design.final.estimand_type: associational`, and do not describe the result as an effect of the intervention. Refuse only when no group comparison answers the request.

Low confidence alone is not a stop condition. Stop when the unresolved fact changes the matrix route, estimand, sample independence, or method compatibility. For a small but otherwise valid study, keep the planned contrast and label it exploratory (rule in the decision contract).
