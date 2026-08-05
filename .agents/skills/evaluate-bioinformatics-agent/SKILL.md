---
name: evaluate-bioinformatics-agent
description: Audit mwangLab bioinformatics-agent runs and experiments for execution integrity, scientific validity, provenance, stability, and cost. Use when evaluating a run directory, comparing agent changes, reviewing run_status.json/evidence.json/summary.csv artifacts, designing an A/B evaluation, or deciding whether an agent result is trustworthy.
---

# Evaluate Bioinformatics Agent

Use evidence in generated artifacts before judging prose quality. Keep result quality, evaluation coverage, and operational cost separate.

## Workflow

1. Identify the evaluation unit: one run, one study/contrast, or an A/B change.
2. Read [references/rubric.md](references/rubric.md) and choose applicable checks.
3. For a completed run directory, execute:

   ```powershell
   $env:PYTHONIOENCODING = 'utf-8'
   .\.venv\Scripts\python.exe .agents\skills\evaluate-bioinformatics-agent\scripts\audit_run.py --run-dir <path>
   ```

4. Inspect `agent_evaluation.json` and `agent_evaluation.md`. Report both `score` and `coverage`; never present a high score with low coverage as strong evidence.
5. If repeated DEG/GSEA files exist, also use the project's `evaluate_repeated_subset_results` tool or `tools.evaluation_tools.evaluate_repeated_results_core`.
6. For a prompt, model, routing, or skill change, run paired A/B trials on the same cases. Hold model, temperature, inputs, and scoring fixed. Use at least three repeats for LLM-dependent behavior.
7. Recommend a change only when it improves the primary quality metric without violating scientific safety gates. Report cost and latency deltas as secondary metrics.

## Required gates

- Reject or flag raw-count methods on normalized/log-scale matrices and vice versa.
- Require a defensible contrast and adequate per-arm alignment before trusting DA output.
- Treat implausible DEG fractions, unresolved sample alignment, dangling evidence references, and artifact hash mismatches as blocking findings.
- Prefer deterministic checks for schemas, files, hashes, thresholds, and tool routing. Use an LLM judge only for semantic correctness that cannot be encoded reliably.
- Keep the judge independent from the agent under test; do not leak expected answers into the tested prompt.

## Output

Lead with the verdict, score, coverage, and blocking findings. Then list dimension scores, unmeasured checks, and the smallest next experiment that would reduce uncertainty.
