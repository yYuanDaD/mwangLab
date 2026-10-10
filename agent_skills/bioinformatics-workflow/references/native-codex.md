# Native Codex execution

For a request such as "run these 20 articles with this skill", the model serving the current Codex conversation reads the evidence and owns each scientific decision. A script which launches the old agent or its LLM validators does not test native Codex analysis.

## Separate decisions from calculations

1. Inspect article/GEO processing notes, candidate file headers, identifiers, numeric summaries, and sample metadata. Scripts may extract summaries without choosing the final scientific interpretation.
   Make the initial semantic decision from those source facts before consulting Python's type labels or keyword contrast picks. Those labels are optional diagnostics with no deciding weight; a disagreement requires checking source evidence, not defaulting to either answer. File ranking must not hide alternative plausible matrices from review.
2. Record a per-study plan: source files and hashes; matrix type and evidence; sample mapping with unmatched/ambiguous IDs; control, treatments and contrasts; method and transform; candidate covariates/pairing/confounding; confidence and stop/review reasons. For every semantic decision, preserve the decision inputs (metadata summary or matrix statistics/preview), the Python candidate if one existed, the selected answer, rejected alternatives, reason, confidence, and the final execution parameters that consumed it. Link the decision record to the executed contrast/method or to the explicit block/manual-review outcome. Record the decision-maker as the current Codex conversation and record the actual model only when it is available; do not invent a model/version.
3. Validate IDs, mapping uniqueness, arm coverage, numeric compatibility, and the planned model deterministically. Do not align by row position. Do not automatically map generic words or annotation columns to samples.
4. Execute local preprocessing, QC, DA, and enrichment for permitted cases. Preserve one artifact set per contrast. If a method/tool cannot fit the required covariates or pairing, record the limitation and stop or mark exploratory analysis for review; do not silently drop required adjustment.
5. Save actual execution parameters, artifacts and hashes, warnings, failures, and whether any scientific decision changed. A decision-only pass is a checkpoint, not a completed full workflow.

## Hidden LLM calls in this repository

- `main.build_agent` and `run_batch_geo_pipeline` invoke the configured external model. Do not use them as the native Codex decision engine.
- Matrix semantics and contrast validation in `batch_tools` delegate to `llm_helpers`.
- `llm_datatype_strict` and `llm_contrast_strict` force that external provider's review; they do not delegate decisions to the current Codex conversation. An explicit design plan bypasses contrast review even with strict mode enabled.
- `deseq2_tools`, `limma_tools`, and metadata-dependent QC may invoke `align_samples_with_llm_fallback` when sample IDs do not match.

Use Codex-reviewed mapping artifacts to create separate aligned matrix/metadata files with exact matching IDs before calling calculation tools. Preserve original inputs and the original-to-aligned mapping. Add fail-closed guards around external LLM entrypoints in the run process, and record attempted calls separately from completed calls. If a hidden fallback is attempted, stop that case and resolve its inputs; missing credentials or an exception swallowed by a heuristic fallback is not proof of native execution. No external-LLM call should be needed for the default skill workflow.

## Evaluation

Give the tested conversation only input data, article/metadata evidence, the user request, and this skill. Keep expected matrix types, methods, contrasts, mapping answers, and prior results on the scorer side. An existing conversation that has seen those answers is a migration/debugging run, not a blind accuracy evaluation.

Evaluate grouping, matrix/method compatibility, alignment and covariates separately from completion. Report valid refusal/manual review separately from wrong decisions. Keep Codex account usage separate from external API token charges; zero external API calls does not mean zero Codex usage.
