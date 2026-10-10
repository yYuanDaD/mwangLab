# Native execution

In a native run, the agent session makes the decisions and calls repository code directly. Everything below is in `tools/native.py`, plus the executors it calls.

## External LLM calls are blocked

Several repository paths call an external model (DeepSeek or Claude) when they run without a decision:

- `main.build_agent` and `run_batch_geo_pipeline` (the external-agent backend);
- contrast and matrix-type validators in `tools/llm_helpers.py`;
- sample-name alignment fallback inside `run_deseq2_analysis`, `run_limma_analysis`, `run_edger_analysis`, `run_limma_voom_analysis`, and the QC tools, triggered when fewer than half the sample IDs match.

`native.enable_native_mode()` sets `BIOAGENT_DISABLE_EXTERNAL_LLM=1`. From then on, every client request is blocked and logged. `native.call_tool` raises if a tool made such an attempt, and `RunRecorder` writes the attempt count to `run_manifest.json`. Zero attempts is the expected result.

## Calling convention

```python
from tools import native
from tools.deseq2_tools import run_deseq2_analysis

native.enable_native_mode()
message = native.call_tool(run_deseq2_analysis, counts_csv=..., metadata_csv=..., design_column=...,
                           control_group=..., treatment_group=..., output_dir=...,
                           covariate_columns="subject")
deg = native.deg_outputs(output_dir)[0]
counts = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
```

How `call_tool` behaves:
- It unwraps LangChain `@tool` objects, so the tool runs as a plain function.
- It raises `NativeToolError` when the tool's return text reports a failure or refusal (`FATAL ERROR`, `POLICY BLOCKED`, `... failed`, `unavailable`, and similar).

When an import fails because a package is missing, record the execution as failed with the error text. Do not write a substitute model.

## Evidence helpers

These summarize evidence; none of them decides.

| Helper | Use |
|---|---|
| `profile_matrix(path)` | integer fraction, range, negatives, missing values, annotation columns, type candidates |
| `align_to_metadata(matrix, metadata, out_dir, key_column=None)` | exact alignment on the metadata index or one column; writes `aligned_matrix.csv` (columns renamed to sample IDs), `aligned_metadata.csv`, `alignment_map.csv` |
| `log_transform(matrix, out_csv)` | `log2(x+1)` for linear FPKM/TPM/intensity; refuses data that already look log-scale |
| `pairing_report(meta, subject_col, condition_col, levels)` | complete, incomplete, and duplicated subjects across levels |
| `confounding_report(meta, primary)` | each column's relation to the primary factor: `complete_confounding`, `nested_in_primary`, `crossed`, ... |
| `design_check(meta, terms, interactions)` | rank, residual df, cells, and missing values of a categorical design (same column space as `~ C(a) + C(b)`) |
| `apply_threshold(deg_csv, metric, cutoff, effect_cutoff)` | counts under a stated rule, plus `deg_sanity` flags |
| `deg_outputs(output_dir)` | result tables written by the DE tools |

## Executors

All executors read the aligned files. Raw-count executors require integer counts. limma requires log-scale input; `analysis_policy` rejects raw-count-like or linear-scale matrices.

| Route | Call |
|---|---|
| DESeq2, optional additive covariates or blocking | `run_deseq2_analysis(counts_csv, metadata_csv, design_column, control_group, treatment_group, output_dir, covariate_columns="", interaction_terms="")` |
| limma, two arms, optional formula | `run_limma_analysis(normalized_csv, metadata_csv, design_column, control_group, treatment_group, output_dir, design_formula="", coefficient="", covariate_columns="", interaction_terms="")` |
| edgeR, two arms, no covariates | `run_edger_analysis(counts_csv, metadata_csv, design_column, control_group, treatment_group, output_dir)` |
| limma-voom (needs R + limma) | `run_limma_voom_analysis(counts_csv, metadata_csv, design_column, control_group, treatment_group, output_dir)` |
| one model, several levels / factorial / paired change | `tools.multigroup_tools.run_multigroup_analysis(expression_csv, metadata_csv, plan, output_dir)` (plain function; raises `PolicyViolation`) |
| log2(CPM+1) for raw counts before limma | `preprocess_counts(counts_csv, output_dir)` → `*_normalized.csv` |
| single-cell pseudobulk | `run_scrna_pseudobulk_da(matrix_path, sample_col, celltype_col, condition_col, control_group, treatment_group, ..., paired=False)` |
| methylation beta values | `run_methylation_da(beta_matrix_csv, metadata_csv, design_column, control_group, treatment_group, output_dir)` |
| GSEA (Hallmark) | `run_gsea_analysis(deg_csv, organism, ranking_metric="stat", output_dir=...)` |
| ORA | `run_enrichment_analysis(deg_csv, organism, padj_cutoff, log2fc_cutoff, ...)`; pass the paper's cutoffs explicitly (default `log2fc_cutoff=1.0`) |

Blocking with DESeq2 or limma: pass the subject column in `covariate_columns`. The tool validates the design and fits `Treatment` plus the covariate; internally it renames covariates to safe names such as `Covariate0`. In the records, write the model in metadata column names (for example `~ subject + time`) in `method.final.formula`, and the subject column in `covariance.final.blocking_terms`. The validator checks that every required blocking term appears in the recorded formula.

### Multigroup plan

`run_multigroup_analysis` fits limma on a log-scale matrix. For raw counts, pass the `*_normalized.csv` from `preprocess_counts` and record `transform: log2(CPM+1)`.

Multi-level or factorial analysis:

```json
{"analysis_type": "multilevel",
 "formula": "~ 0 + C(group)",
 "contrasts": [{"name": "ex6h_vs_sed", "coefficients": {"C(group)[ex6h]": 1, "C(group)[sed]": -1}}]}
```

Paired change (follow-up minus baseline within each subject, then a group model on the differences):

```json
{"analysis_type": "paired_change",
 "subject_column": "subject", "time_column": "time", "baseline_level": "pre",
 "followup_levels": ["post"], "group_column": "arm", "formula": "~ C(arm)",
 "contrasts": [{"name": "trained_vs_control", "coefficients": {"C(arm)[T.trained]": 1}}]}
```

Plan rules:
- Coefficient names are patsy column names. Create short, safe level labels first (for example `sed`, `ex6h`) when the original values contain spaces or punctuation, and record the mapping.
- `derived_columns` (`{"name": {"source_column": ..., "regex": ...}}`) extracts labels from titles deterministically.
- Paired change writes `paired_change_pairs.json` with complete pairs and excluded subjects. Report the exclusions.
- Each contrast is BH-adjusted within itself, and the executor's `n_deg` uses `padj < 0.05`. Apply the paper threshold with `apply_threshold`.

## Run layout

`RunRecorder` writes this layout, which `validate_decision_contract.py` and the evaluator's `audit_run.py` read:

```text
<run_dir>/
  run_manifest.json    request, platform, decision maker, repo commit, Python/OS, external-LLM attempts
  run_status.json      tracker: status, stages, timing, failures
  summary.csv          one row per case: status, matrix_type, da_method, contrast, covariance, threshold
  workflow.log         one line per decision and case outcome
  preflight.json       output of scripts/preflight.py (write it here)
  <case_id>/
    decisions.json     decision-contract records, in gate order
    evidence.json      sources, decisions, artifacts with SHA-256
    paper_reconstruction.json, paper_data_discrepancies.json,
    reproduction_plan.json, reproduction_summary.json
    aligned/ results/  files produced for this case
```

Minimal per-case flow:

```python
paper = case.add_input("cases/x/paper.md", "paper")
meta = case.add_input("cases/x/GSE1_metadata.csv", "metadata")
mat = case.add_input("cases/x/GSE1_counts.csv", "matrix")
case.decide("paper_reconstruction", final={...}, evidence=[paper], reasoning="...", confidence="high")
aln = native.align_to_metadata(mat["path"], meta["path"], case.dir / "aligned", key_column="title")
aligned = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"],
            "n_metadata": aln["n_metadata"], "coverage": aln["coverage"]},
            evidence=[mat, meta, aligned], reasoning="...", confidence="high")
# ... matrix, design, covariance, method, threshold, execution, study
case.finish(n_deg=counts["n_significant"], deg_sanity=counts["deg_sanity"])
run.finish()
```

`case.decide` raises `NativeToolError` when a record misses a required field. `case.finish` raises when the case breaks an invariant, for example a completed execution after a blocked gate. Fix the record; do not bypass the recorder.
