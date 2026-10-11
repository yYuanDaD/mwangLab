# Native execution

In a native run, the agent session makes the decisions and calls repository code directly. Everything below is in `tools/native.py`, plus the executors it calls.

## External LLM calls are blocked

Several repository paths call an external model (DeepSeek or Claude) when they run without a decision:

- `main.build_agent` and `run_batch_geo_pipeline` (the external-agent backend);
- contrast and matrix-type validators in `tools/llm_helpers.py`;
- sample-name alignment fallback inside `run_deseq2_analysis`, `run_limma_analysis`, `run_edger_analysis`, `run_limma_voom_analysis`, and the QC tools, triggered when fewer than half the sample IDs match.

`native.enable_native_mode()` sets `BIOAGENT_DISABLE_EXTERNAL_LLM=1`. From then on, every client request is blocked and logged. `native.call_tool` raises if a tool made such an attempt, and `RunRecorder` writes the attempt count to `run_manifest.json`. Zero attempts is the expected result.

It also switches the console to UTF-8, so Windows needs no `PYTHONIOENCODING` setting inside a native run.

## Calling convention

```python
import math
from tools import native

native.enable_native_mode()
try:
    message = native.call_tool("tools.deseq2_tools:run_deseq2_analysis",
                               counts_csv=..., metadata_csv=..., design_column="time",
                               control_group="pre", treatment_group="post", output_dir=...,
                               covariate_columns="subject")
except native.NativeToolError as error:
    ...  # record execution: decision_status="valid", execution_status="failed",
         # final={"method": ..., "execution_error": str(error)}
deg = native.deg_outputs(output_dir)[0]
counts = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
# FC 1.5 in the paper: effect_cutoff=math.log2(1.5)
```

How `call_tool` behaves:
- It accepts a `"module:function"` string (preferred), a LangChain `@tool`, or a plain function. A string turns a missing package into a `NativeToolError` whose text is the `execution_error` to record.
- It runs the tool as a plain function. LangChain is optional: the analysis modules fall back to a plain decorator (`tools/tooling.py`), so preprocessing, QC, and executors need only their own scientific packages.
- It raises `NativeToolError` when the tool's return text reports a failure or refusal (`FATAL ERROR`, `POLICY BLOCKED`, `... failed`, `unavailable`, and similar).

Never write a substitute model for a missing executor.

## Formula-safe column names

GEO metadata columns such as `characteristics_ch1.1.time point` cannot appear in a patsy formula, and the validator checks blocking terms by name. After alignment, write a metadata copy with short columns and use only those names afterwards:

```python
derived = native.derive_columns(
    aligned_metadata, case.dir / "aligned" / "design_metadata.csv",
    aliases={"subject": "characteristics_ch1.0.subject", "time": "characteristics_ch1.1.time point"},
    patterns={"grp": ("title", r"soleus_(.+)_rep\d+")},
    recode={"grp": {"sedentary_control": "sed", "exercise_0_h_post": "ex0h"}})
```

- `aliases` copies a column under a new name.
- `patterns` extracts a regex group and fails unless every row matches.
- `recode` must map every value.

Record `derived` (sources, regexes, mappings, levels) as evidence in the alignment or design decision. Then write formulas, `blocking_terms`, and executor arguments with the short names, for example `~ subject + time` with `blocking_terms: ["subject"]`.

## Driver scripts

Keep driver scripts in `output/<run_name>/scripts/` so they stay with the run, and start each with:

```python
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))  # repository root
from tools import native
```

Repository tools return text. Find the files they wrote with `native.deg_outputs(dir)` or `native.find_outputs(dir, "*_normalized.csv")` instead of parsing the text.

## Continuing a run

`RunRecorder` and `CaseRecorder` write their state to disk after every call: `decisions.json`, `evidence.json`, and `case_state.json`. An agent that runs one command per gate continues with:

```python
run = native.RunRecorder.open("output/<run_name>")
case = run.case("case_01")
meta = case.evidence_item("metadata:GSE1_metadata.csv")  # reuse an evidence item registered earlier
```

Creating a new `RunRecorder` on an existing run directory raises, so nothing is overwritten.

## Evidence helpers

These summarize evidence; none of them decides.

| Helper | Use |
|---|---|
| `profile_matrix(path)` | integer fraction, range, negatives, missing values, annotation columns, type candidates |
| `align_to_metadata(matrix, metadata, out_dir, key_column=None)` | exact alignment on the metadata index or one column; writes `aligned_matrix.csv` (columns renamed to sample IDs), `aligned_metadata.csv`, `alignment_map.csv` |
| `derive_columns(meta, out_csv, aliases, patterns, recode)` | formula-safe metadata columns with a recorded mapping (see below) |
| `log_transform(matrix, out_csv)` | `log2(x+1)` for linear FPKM/TPM/intensity; refuses data that already look log-scale |
| `beta_to_m(beta_csv, out_csv)` | methylation M-values for limma with covariates, blocking, or several levels |
| `feature_id_report(path)` | ID type (symbol, Ensembl gene or transcript, probe, UniProt, CpG, ...) and whether gene-set analysis can use it |
| `package_versions()` | installed versions of the numerical packages (also written to `run_manifest.json`) |
| `collapse_to_genes(table, out_csv, mapping_csv, mapping_column, rule)` | probe, transcript, or protein table to one row per gene (`max_mean` or `max_abs_score`), with a mapping record |
| `complete_pairs_subset(matrix, metadata, out_dir, subject_column, condition_column, levels)` | keep subjects with one sample at every level; reports excluded subjects |
| `find_outputs(dir, pattern)` | files a tool wrote, for example `*_normalized.csv` from `preprocess_counts` |
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
| one model, several levels / factorial / paired change | `tools.multigroup_tools:run_multigroup_analysis(expression_csv, metadata_csv, plan, output_dir)` (plain function; through `call_tool` a `PolicyViolation` becomes a `NativeToolError`) |
| log2(CPM+1) for raw counts before limma | `preprocess_counts(counts_csv, output_dir)` → `*_normalized.csv` |
| single-cell pseudobulk, native | `tools.scrna_tools:aggregate_pseudobulk(matrix_path, sample_col, celltype_col, condition_col, cell_metadata_path, min_cells, output_dir, report)` (plain function, returns a per-cell-type manifest), then a DE executor per cell type |
| single-cell pseudobulk, one call | `run_scrna_pseudobulk_da(matrix_path, sample_col, celltype_col, condition_col, control_group, treatment_group, ..., paired=False)` |
| proteomics | `aggregate_peptide_to_protein(quant_path, ...)` for peptide input, `preprocess_proteomics_matrix(quant_path, labeling, output_dir)`, then limma |
| methylation beta values | `run_methylation_da(beta_matrix_csv, metadata_csv, design_column, control_group, treatment_group, output_dir)`; with covariates use `native.beta_to_m` and limma |
| GSEA (Hallmark) | `run_gsea_analysis(deg_csv, organism, ranking_metric="stat", output_dir=...)` |
| ORA | `run_enrichment_analysis(deg_csv, organism, padj_cutoff, log2fc_cutoff, ...)`; pass the applied cutoffs explicitly (the default `log2fc_cutoff=1.0` adds an effect cutoff) |
| paper text | `tools.paper_tools:fetch_paper_text(pmcid=...)` (Europe PMC, needs network); otherwise read the paper file the user gave |

Module paths for `call_tool`: `tools.deseq2_tools`, `tools.limma_tools`, `tools.edger_tools`, `tools.limma_voom_tools`, `tools.preprocess_tools`, `tools.multigroup_tools`, `tools.scrna_tools`, `tools.proteomics_tools`, `tools.methylation_tools`, `tools.enrichment_tools`, `tools.paper_tools`. Modality-specific details are in [Modalities](modalities.md).

Blocking with DESeq2 or limma: pass the derived subject column in `covariate_columns`. The tool validates the design and fits `Treatment` plus the covariate; internally it renames covariates to safe names such as `Covariate0`. In the records, write the model with the derived names (for example `~ subject + time`) in `method.final.formula`, and the same subject name in `covariance.final.blocking_terms`. The validator checks that every required blocking term appears in the recorded formula.

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
- Coefficient names are patsy column names: `C(<column>)[<level>]` for `~ 0 + C(column)`, and `C(<column>)[T.<level>]` for treatment-coded terms. Create short, safe column names and level labels first with `native.derive_columns` (for example `grp` with levels `sed`, `ex6h`), and record the mapping.
- Check the plan with `native.design_check(design_metadata, ["grp"])` before calling the executor. Use the same derived file for both.
- The executor's own `derived_columns` (`{"name": {"source_column": ..., "regex": ...}}`) still works, but deriving beforehand lets every check see the same columns.
- Paired change writes `paired_change_pairs.json` with complete pairs and excluded subjects. Report the exclusions.
- Each contrast is BH-adjusted within itself, and the executor's `n_deg` uses `padj < 0.05`. Apply the paper threshold with `apply_threshold`.

## Run layout

`RunRecorder` writes this layout, which `validate_decision_contract.py` and the evaluator's `audit_run.py` read:

```text
<run_dir>/
  run_manifest.json    request, platform, decision maker, repo commit, Python/OS, package versions, external-LLM attempts
  run_status.json      tracker: status, stages, timing, failures
  summary.csv          one row per case: status, matrix_type, da_method, transform, contrast, covariance,
                       threshold, enrichment, stop_reason (blocked gates), execution_error (failed runs)
  workflow.log         one line per decision and case outcome
  preflight.json       output of scripts/preflight.py (write it here)
  <case_id>/
    decisions.json     decision-contract records, in gate order
    evidence.json      sources, decisions, artifacts with SHA-256
    case_state.json    recorder state (evidence ids, summary row) for RunRecorder.open
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
# ... matrix, design, covariance, method, threshold, execution, (enrichment), study
case.finish(n_deg=counts["n_significant"], deg_sanity=counts["deg_sanity"])
run.finish()
```

`case.decide` raises `NativeToolError` when a record misses a required field. `case.finish` raises when the case breaks an invariant, for example a completed execution after a blocked gate. Fix the record; do not bypass the recorder.
