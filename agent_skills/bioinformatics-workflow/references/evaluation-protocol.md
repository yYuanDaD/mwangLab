# Paired article evaluation

The primary question is whether the system can reproduce and validate the article's stated workflow. A plausible DEG table produced under a different design or threshold is not a reproduction.

Use a frozen case manifest and identical source data for every system under comparison. Each case should include the article, target accession(s), downloaded-data snapshot or hashes, the exact user request including the primary estimand, paper-defined sample inclusion/exclusion, planned contrasts, expected design, matrix type, valid method, covariance expectations, paper threshold, and expected refusal/manual-review status. Validate that every referenced matrix and metadata path exists before starting a trial; a missing input is a protocol failure, not an agent failure.

Stratify cases across clean two-arm RNA-seq, multiple treatment levels, FPKM/TPM, log-scale data, abbreviated sample IDs, incomplete metadata, batch/donor confounding, multi-factor designs, observational studies, and papers with multiple accessions.

Compare the current agent and native Codex+skill on the same cases. In the Codex arm, the current conversation must make the scientific decisions; launching the existing external-LLM harness from a Codex window is only orchestration validation. Use the native execution reference to prevent hidden external LLM calls. Keep expected answers and prior results out of the tested conversation; input manifests must omit expected fields. Mark any already-exposed conversation as non-blind.

Run at least three independently decided repeats per condition; rerunning one saved plan only tests computational reproducibility. Use five or more when model variance is material. If isolating the skill effect matters, add current-agent+skill and Codex-without-skill arms. Hold inputs, tools, scoring and biological requests fixed; document each arm's actual model and configuration. Hold model/settings fixed only when evaluating the skill effect within the same model, not when comparing Codex with the external-model agent.

Primary metrics:

- paper reconstruction: accession ownership, sample inclusion, primary estimand, planned contrasts, design/covariance terms, method, and threshold;
- paper/data discrepancy detection and safe disposition;
- fidelity of the executed route to the paper-aligned reproduction plan;
- correct control/treatment and allowed contrasts;
- correct matrix type and compatible statistical method;
- covariance/confounding decision;
- safe refusal or manual-review routing;
- scientifically valid completed analyses;
- evidence and provenance completeness.

Report paper-aligned results using the article's threshold semantics. If an audit threshold is used for cross-study comparison or subset stability, report it as a separate secondary analysis. Do not score systems by whether they happen to match a universal `padj < 0.05`/`|log2FC| >= 1` rule when the article used another rule.

Record `decision_status` and `execution_status` separately. A valid scientific plan followed by a tool failure is a decision pass/execution failure; an incompatible method, invalid contrast, or unresolved covariance presented as complete is a blocking decision failure.

Blocking failures include incompatible matrix/method, invalid contrast, unresolved alignment presented as complete, an unhandled treatment-batch confound, or a p-value-producing run that violates a required method gate. Report completion, latency, tool/LLM calls, and estimated cost as secondary metrics. Score deterministic checks first; use an independent semantic judge only for questions that cannot be encoded reliably.

Report paired per-case outcomes and aggregate confidence intervals or exact paired tests. Treat DEG/p-value counts as descriptive outputs under a named threshold, not as correctness scores. Do not rank systems by DEG count, p-value count, or fluent narrative quality.
