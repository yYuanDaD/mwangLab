# Claim-evidence alignment benchmark protocol

## Objective

Test whether the agent distinguishes evidence that directly supports a paper's
primary conclusion from partial support, secondary findings, contradiction, and
claims that the target accession cannot evaluate.

## Gold-set rule

At least six and preferably eight cases must be reviewed by a domain expert.
Machine-generated drafts are never gold.  The reviewer must verify the primary
claim, verbatim source quote and locator, accession scope, contrast, evidence
trustworthiness, relation label, and rationale before setting
`annotation_status=gold` in both the card and manifest.

## Blind protocol

1. Freeze paper text, accession scope, analysis artifacts, model, temperature,
   prompts, tool registry, and gold cards.
2. Keep gold cards outside the tested agent's context.
3. Produce predictions for the same cases in three independent repeats under
   `repeat_01`, `repeat_02`, and `repeat_03`.
4. Score only after all predictions are complete.

## Primary acceptance gates

- relation-label accuracy >= 85%;
- zero false `direct_support` claims;
- 100% primary-claim mapping;
- 100% primary-claim provenance completeness;
- every article has a deliverable result card;
- identical claim/evidence relations across all three repeats;
- all existing matrix/method, alignment, DEG sanity, artifact, and evidence
  integrity gates remain blocking.

Cost and latency are secondary metrics and cannot compensate for a failed
scientific safety gate.
