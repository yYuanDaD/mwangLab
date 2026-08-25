# Large-scale SEA-CDM Production Gate v1

This protocol is frozen before paid model calls. The evaluation unit is one target GEO
accession in one paper, not the whole paper and not one LLM call.

## Objective

Test whether DeepSeek V4 Pro staged SEA-CDM extraction is sufficiently safe, stable,
traceable, and inexpensive for GEO-metadata-backed accession-scoped production use.

## Frozen design

- 30 GEO-backed exercise-response cases.
- Three independent repeats per case (90 planned runs).
- DeepSeek V4 Pro, temperature 0, staged extraction, 16,384 structured-output tokens,
  one targeted retry per failed stage, and at most 100,000 paper characters.
- Deterministically shuffled execution order using seed `20260819`.
- Same code commit, prompt/schema implementation, scorer, paper text, metadata, and
  target-accession policy for every repeat.
- No prompt or scorer changes after the first paid call.
- DeepSeek-stage spend cap: USD 4.50. Opus fallback is a separate, later phase capped by
  the remaining experiment budget and is invoked only for naturally failing hard gates.

## Per-run blocking gates

- Unhandled exception or non-terminal run.
- SEA-CDM schema violation or foreign-key violation.
- Missing required study, experiment, subject, sample, groups, interventions, assay, or
  documentation table.
- Group construction error or target metadata/sample-count mismatch.
- A foreign GEO accession attached to target design relations.
- An accession not present in the frozen source paper or target accession.
- Exercise semantics missing when required by target GEO metadata.
- Provenance unavailable or verified provenance below 90%.
- Input paper or metadata hash mismatch.

## Pre-registered aggregate acceptance criteria

- At least 90% of cases pass all three repeats.
- At least 95% of routine single-accession cases pass all three repeats.
- Zero schema, FK, input-hash, unsupported-accession, or cross-accession design failures.
- Mean verified provenance at least 95%.
- At least 90% of cases have identical structural-count signatures across repeats.
- False fallback requirement on clean three-of-three cases at most 5%.
- Independent audit score and coverage are reported separately; coverage below 60% is
  insufficient evidence regardless of score.

## Reporting rules

- Report per-run and per-case results, not only aggregate means.
- Report Wilson 95% confidence intervals for case-level pass proportions.
- Separate quality, audit coverage, stability, latency, calls, and cost.
- Preserve every failed run and every billable failed parse in the cost total.
- Do not repair outputs manually during the frozen experiment.

