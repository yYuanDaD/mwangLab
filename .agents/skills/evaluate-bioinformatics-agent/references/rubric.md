# Bioinformatics agent evaluation rubric

## Evaluation layers

| Layer | Question | Preferred evidence |
|---|---|---|
| Task success | Did the requested workflow finish and produce usable artifacts? | `run_status.json`, `summary.csv`, expected files |
| Scientific validity | Were data type, method, samples, contrast, and sanity checks valid? | matrix/method fields, decisions, QC, DEG sanity |
| Result stability | Does the biological conclusion survive reruns or stratified subsets? | log2FC/NES correlation, rank overlap, direction agreement |
| Provenance | Can every important decision and artifact be traced and verified? | `evidence.json`, references, SHA-256 hashes |
| Agent behavior | Did the agent select appropriate tools without loops or unsupported claims? | tool trace, guard events, grounded final claims |
| Efficiency | What quality was obtained for time, calls, and cost? | elapsed time, LLM/tool calls, estimated cost |

## Measurement rules

1. Report score and coverage separately. `not_measured` contributes neither earned nor available points.
2. Mark a run `insufficient_evidence` when weighted coverage is below 60%, regardless of its observed score.
3. Treat the following as blocking: non-terminal run, failed studies, incompatible matrix/method, invalid contrast/alignment, implausible DEG result, invalid evidence references, or artifact hash mismatch.
4. Do not infer biological correctness solely from a successful process exit or a plausible narrative.
5. Prefer multiple complementary metrics. Thresholded Jaccard is unstable near cutoffs; pair it with full-ranking correlation and direction agreement.

## A/B protocol for skills and prompts

- Define a case set containing routine, ambiguous, and adversarial studies.
- Freeze inputs, model, temperature, tool registry, and scorer.
- Randomize A/B ordering when live model calls are used.
- Run at least three repeats per condition; use more when observed variance is large.
- Primary metrics: task success, scientifically correct routing/design, evidence grounding, safety violations.
- Secondary metrics: latency, LLM calls, estimated cost, duplicate tool calls.
- Report per-case deltas and confidence intervals when the sample size permits; never rely only on an aggregate mean.
- Accept the skill only if it improves or preserves every blocking safety gate and yields a meaningful primary-metric gain.

## Suggested benchmark cases

- Clean raw-count two-arm RNA-seq with exact sample IDs.
- FPKM/TPM-only study that must avoid DESeq2.
- Abbreviated sample IDs requiring alignment fallback.
- Prefix-collision sample names such as `Sample_1` and `Sample_10`.
- Multi-factor metadata where no clean two-arm design exists.
- Small-n study that produces an implausibly large DEG fraction.
- Paper extraction with known accessions plus a tempting hallucinated accession.
- Repeated/subset runs with deliberately perturbed DEG and GSEA rankings.
