---
name: bioinformatics-workflow
description: "Paper-first, auditable differential-expression and pathway-enrichment workflow for GEO and omics studies (bulk RNA-seq, microarray, single-cell pseudobulk, proteomics, methylation). Use when analyzing one study or a cohort from papers or GEO accessions, reproducing a paper's DE or pathway result, or reviewing whether an analysis used a valid contrast, covariance, matrix-method route, and threshold. Requires the mwangLab repository and its Python environment. Not for literature search alone or SEA-CDM extraction."
---

# Bioinformatics workflow

Skill version 2.0, decision contract v2. Works in any agent that loads Agent Skills (Codex, Claude Code, others) on Windows, macOS, or Linux.

The agent session running this skill is the scientific decision-maker. It reads the evidence and decides the matrix type, sample mapping, contrast, covariance, method, and threshold. Repository code only summarizes evidence, validates decisions, executes approved calculations, and records them. A p-value never shows that a decision was right.

`<skill_dir>` below is the folder that contains this file. Use `python` or `python3`, whichever runs the repository's environment.

## Before the first study

1. Work from the repository root. Choose a new run directory, `output/<run_name>`.
2. Run `python <skill_dir>/scripts/preflight.py --out output/<run_name>/preflight.json`. Add `--network` when the run needs GEO download, paper fetch, PRIDE, or enrichment.
   - If the repository is not found or packages are missing, follow [Setup](references/setup.md).
   - Each capability (`deseq2`, `limma_two_group`, `limma_multigroup`, `methylation`, `proteomics_preprocess`, `single_cell_aggregation`, `gsea_and_ora`, ...) says whether its route can run here.
   - If no differential-analysis capability is available (`de_capable: false`), tell the user the run will be decision-only. Each valid plan is then recorded with its `execution_error`. Never replace a missing executor with a hand-written statistical model.
3. Read [Native execution](references/native-execution.md) for the calling convention, the external-LLM block, formula-safe column names, and the run layout. For single-cell, proteomics, methylation, or enrichment, also read [Modalities](references/modalities.md).
4. Start the run:

```python
from tools import native
native.enable_native_mode()  # blocks hidden external LLM calls inside repository tools
run = native.RunRecorder("output/<run_name>", request="<user request>",
                         platform_name="<codex | claude-code | ...>",
                         decision_maker="<this agent and model, if known>", case_ids=[...])
case = run.case("<case_id>", accession="<GSE...>")
```

The recorder saves its state after every call. To continue the run from a later command, use `run = native.RunRecorder.open("output/<run_name>")` and `case = run.case("<case_id>")`.

Save driver scripts in `output/<run_name>/scripts/`, so they stay with the run, and start each one with:

```python
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))  # repository root
```

Do not use `main.py`, `run_batch_geo_pipeline`, or the validators in `tools/llm_helpers.py` for decisions unless the user asks for that external-agent backend.

## Core rules

- **Paper first.** When an article is available, it defines the estimand, sample inclusion, contrast, design and blocking unit, method, and threshold. GEO metadata and the matrix test whether that plan can be carried out. Keyword matches are only supporting evidence. If paper and data disagree, record both and stop when the disagreement changes the estimand, sample set, covariance, or method. Details: [Paper reconstruction](references/paper-reconstruction.md).
- **Thresholds keep their meaning.**
  - `paper_threshold` is the article's exact rule. Do not turn FDR into raw p, and do not add `|log2FC| > 1` when the paper has none. Convert a fold change with its exact value: FC 1.5 becomes `|log2FC| > log2(1.5)` = 0.5849625, not a rounded number.
  - `audit_threshold` is a separate, labelled comparison rule.
  - When the paper states nothing, use `workflow_default` (BH-adjusted p < 0.05, no effect-size cutoff) and say so.
  - Repository tools print their own `n_deg` summaries. Count with `native.apply_threshold` instead.
- **Decisions and execution are separate.**
  - `decision_status` says whether the route is scientifically valid; `execution_status` says whether the tool ran.
  - A valid plan whose tool failed is acceptable.
  - A completed run on an invalid plan is a blocking failure.
- **Record before acting.** Write each gate with `case.decide(...)` before moving to the next one. `RunRecorder` rejects records that break the [Decision contract](references/decision-contract.md). Decision gates keep `execution_status="not_started"`; only the `execution` record carries `completed` or `failed`.

## Gates

Complete them in this order for every case:

1. `paper_reconstruction`: build the study map — accessions, assay, sample inclusion and exclusion, factors and levels, primary estimand, planned contrasts, repeated-measure unit, normalization, method, and paper threshold, each with a locator in the paper.
2. `ownership`: identify the matrix and metadata files and confirm they belong to the paper's accession and samples.
3. `alignment`: map the deposited matrix's columns to metadata samples with `native.align_to_metadata` (exact match on the index or on one named column, such as `title`). Never align by position. Record coverage and unmatched IDs. Then create short, formula-safe columns with `native.derive_columns` (for example `subject`, `time`, `grp`). Pass the aligned files to every later tool, so that no tool falls back to LLM alignment, and use the derived names in every formula and record.
   - Steps that change values (filters, imputation, transforms) are method decisions, run at execution.
   - A deterministic summary that a later gate needs, such as cells per donor and cell type from pseudobulk aggregation, may be computed earlier and registered as evidence.
4. `matrix`: decide the matrix type from `native.profile_matrix` values plus file name, platform, and processing notes. Compare it with the paper's stated input. An ambiguous type stops the case.
5. `design`: decide the estimand structure.
   - First run the suitability report: `rep, item, summary = case.suitability(matrix_type=..., metadata=<aligned metadata DataFrame>, factors=[...], matrix_csv=<aligned matrix>, organism=..., subject=<subject column or None>, planned=[...])`; `planned` uses the report's comparison names (`<factor>_<test>_vs_<reference>`, for example `grp_O_vs_Y`), so list them with `references=` set and copy the names. It checks data type and required data, that the groups are determinable, covariance candidates, n >= 3 per group, lists every sensible comparison, and compares sex from X/Y genes with the metadata. Put `summary` in `final.suitability` and `item` in the evidence. A `not_analyzable` verdict stops the case at this gate; read `<case>/suitability/suitability.md` for the reason.
   - A sex mismatch is a labelling problem: fix or exclude the samples (record which) before any model. When both sexes are present, add per-sex analyses as exploratory even if the paper pooled them (the report's `split_plan`).
   - Time series and multi-factor designs: run every analyzable comparison the report lists, from one model fitted on all samples (`tools.joint_contrasts`). The paper's planned contrasts keep their route; the others are exploratory.
   - One control with several levels: one model with planned contrasts, never pooled levels.
   - Factorial: keep every factor and the interaction the question needs.
   - Repeated measures: time as a factor plus the subject key.
   - Clustering, prognostic, or validation-only studies get no manufactured contrast.
   - A cross-sectional comparison defined by the paper (for example trained versus untrained people) stays valid with `estimand_type: associational`; do not describe it as an effect of the intervention.
   - When several columns could define the contrast, decide from the paper and record the rejected alternatives.
6. `covariance`: use `native.pairing_report`, `native.confounding_report`, and `native.design_check`.
   - Treat donor, subject, and animal keys as blocking decisions, not annotations.
   - Do not add covariates because of their column names.
   - A covariate completely confounded with the treatment stops the case. A design that is not full rank, or that has no residual degrees of freedom, also stops it.
7. `method`: choose a route the matrix supports ([Matrix and method policy](references/matrix-method-policy.md)). Reproduce the paper's method when the data allow it. Otherwise the method decision stays `valid`, carries `paper_route: {"method": ..., "status": "blocked", "reason": ...}`, and names the validated alternative that runs as a declared deviation.
8. `threshold`: record `paper_threshold`, `threshold_source`, and the `applied_threshold`.
9. `execution`: run the approved route with `native.call_tool("tools.<module>:<function>", ...)`, which turns an import failure into a recordable `NativeToolError`. Apply the threshold with `native.apply_threshold` and register outputs with `case.add_output`. A failure is recorded as `valid` + `failed` with `final.execution_error`.
10. `enrichment` (optional): only when the request or paper calls for pathway results.
    - Check IDs with `native.feature_id_report`. Map probes or proteins to genes with `native.collapse_to_genes`.
    - GSEA uses the full ranking; an ORA gene list uses the applied threshold.
    - It runs only after a completed execution. Without one, record the plan as `valid` + `not_run` with `reason_not_run`.
    - A refused or failed enrichment does not stop the case. Details: [Modalities](references/modalities.md).
11. `study`: record the planned route (`paper_aligned`, `declared_deviation`, or `exploratory`) even when execution failed. Then call `case.finish(n_deg=..., deg_sanity=...)`.

After all cases:

- Call `run.finish()`.
- Validate with `python <skill_dir>/scripts/validate_decision_contract.py <run_dir>`.
- If the evaluator skill is installed, audit with `evaluate-bioinformatics-agent`.

## When to stop

Use `refused` when the available data cannot identify the estimand, such as no exercise contrast or treatment aliased with batch. Use `manual_review` when a specific fact or executor could unblock it, such as unknown pairing, an ambiguous matrix scale, or a missing file.

Record every gate in order up to and including the one that stops the case. For example, a sequenced sample set with no exercise arm is refused at `design`, after `paper_reconstruction`, `ownership`, `alignment`, and `matrix` are recorded. Do not record later gates or a `study` record for a stopped case; `case.finish()` marks its route `stopped`.

Small n alone is not a reason to stop: run the planned contrast and label it exploratory under the rule in the decision contract.

## Final response

Reply in the user's language. For each case, report:

- what was reproduced exactly;
- what ran as a declared deviation or exploratory analysis;
- what was stopped, and why;
- what failed to execute, and what to install;
- the threshold used and its source;
- enrichment results, if run, kept separate from the DE result.

Do not summarize success by DEG or p-value counts.

## References

- [Setup](references/setup.md): installing the repository and environment on a new machine; installing the skill for Codex and Claude Code; self-test.
- [Modalities](references/modalities.md): single-cell pseudobulk, proteomics, methylation, and the enrichment gate.
- [Native execution](references/native-execution.md): calling convention, executor signatures, multigroup plan schema, run layout.
- [Decision contract](references/decision-contract.md): record fields per stage, status rules, invariants the validator enforces.
- [Decision gates](references/decision-gates.md): contrast, multi-group, covariance, and stop conditions.
- [Paper reconstruction](references/paper-reconstruction.md): study maps, discrepancies, thresholds.
- [Explicit multifactor designs](references/multifactor-design.md) and [Multigroup and longitudinal designs](references/multigroup-longitudinal.md).
- [Matrix and method policy](references/matrix-method-policy.md).
- [Evaluation protocol](references/evaluation-protocol.md): blind paired tests of this skill.
- [Tool map](references/tool-map.md).
