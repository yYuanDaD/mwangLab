# Runtime skill A/B — 2026-08-05

## Change under test

The LangChain bioinformatics agent now discovers repository skills under `agent_skills/`, exposes only their name/description initially, and adds a bounded `load_runtime_skill` tool. The first skill, `paper-workflow-safety`, targets paper dataset extraction and safe workflow planning.

## Controlled experiment

- Model: `claude-sonnet-4-6`
- Temperature: `0`
- Target: the same unseen AML multi-dataset paper in all conditions
- Condition A: existing base instructions
- Condition B: base instructions plus the runtime-loaded `paper-workflow-safety` bundle
- Repeats: 3 paired trials; A/B call order alternated
- Fixed: target text, output schema, gold target, scorer, and model
- Skill bundle SHA-256: `9d45d56b2fae73b93799602a1555cca8352cf154a27c7df9b768121d16662980`

## Iteration 1 — rejected

The initial scorer suggested a positive result, but forward testing found that the agent recommended limma-voom for normalized/log-scale values. After adding matrix/method compatibility to the scorer, the saved outputs rescored to:

- Mean A: 89.21
- Mean B: 89.76
- Mean delta: +0.55
- Method compatibility gate: failed in 2/3 B outputs
- Verdict: reject

The skill was hardened to state that FPKM/TPM, already log-transformed expression, microarray intensity, and processed proteomics use the project's plain `run_limma_analysis` path; limma-voom remains a raw-count method.

## Iteration 2 — accepted for this use case

| Metric | A | B |
|---|---:|---:|
| Mean total score | 89.99 | 92.25 |
| Mean workflow safety | 0.833 | 0.944 |
| Mean evidence grounding | 0.111 | 0.111 |
| Total estimated cost | $0.220284 | $0.212367 |

- Paired deltas: +3.00, +0.00, +3.79
- Mean delta: +2.26; sample SD: 2.00
- Wins/ties/losses: 2/1/0
- Matrix/method gate: 3/3 passed
- Hallucinated or copied accessions: 0
- Total experiment: 6 LLM calls, $0.432651, 280.23 seconds
- Verdict: accept

The skill added about 677 input tokens per B call but produced shorter answers, so measured B cost was slightly lower in this run.

## Runtime activation probe

`main.build_agent(..., enable_runtime_skills=True)` was invoked on a mixed bulk/single-cell observational planning request. The only tool call was:

```text
load_runtime_skill({"skill_name": "paper-workflow-safety"})
```

No search, download, or analysis tool was called. After hardening, the final plan routed FPKM/TPM/log-scale values to `run_limma_analysis` and did not route them to limma-voom.

## Limits

This is evidence for one paper-planning use case, not for all GEO, batch, proteomics, methylation, or single-cell workflows. Before enabling additional skills, add gold cases for clean raw counts, FPKM/TPM, abbreviation-based sample alignment, multifactor designs, and small-n implausible DEG output.
