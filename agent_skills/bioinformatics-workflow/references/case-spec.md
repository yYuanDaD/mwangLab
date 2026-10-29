# Case spec route

The default route for bulk data (raw counts, estimated counts, FPKM/TPM/RPKM, log-scale arrays). You make the decisions in one JSON file; `tools/case_runner.py` runs alignment, checks, executors, thresholds, enrichment and the records. You do not write driver scripts or read `tools/native.py`.

```bash
python -m tools.case_runner inspect <GSE> --out <run_dir>/inspect_<GSE>.json   # facts, no records
python -m tools.case_runner template > <run_dir>/case_spec.json                 # starting point
python -m tools.case_runner execute <run_dir>/case_spec.json                    # runs and records everything
```

All three print compact JSON; the tools' own output goes to a log file. Run them from the repository root.

## 1. Inspect

`inspect` downloads the series when it is not cached, then reports:

- `matrices`: each candidate file with integer fraction, range, missing values, duplicated IDs, type `candidates`, annotation columns, example sample columns and feature IDs, and `alignment_keys` (which metadata column equals the matrix column names, and how many match; `<column> (contains the name)` means the names sit inside that field, as in `Library name: CN2`, so derive the key with `key_patterns`). A `_RAW.tar` is merged when no other matrix exists (or with `--merge-tar`).
- `metadata`: `grouping_columns` with level counts, `per_sample_columns` (keys such as `title`, `description`), `constant_columns` (including `data_processing`, which often states the matrix type), and the rest.

Read the paper next (`python -m tools.paper_structure section <paper.json> <block ids>` or the `.paper.md`), then write the spec.

## 2. Spec

One run holds one or more cases (normally one GEO series each):

```json
{"run_dir": "...", "request": "...", "decision_maker": "<agent and model>", "platform": "claude-code",
 "data_root": "data",
 "cases": [{"case_id": "GSE1", "accession": "GSE1",
            "inputs": {"paper": ["<paper.md>"], "metadata": "GSE1/GSE1_metadata.csv",
                       "matrix": "GSE1/<file>", "raw_tar": false, "prep_scripts": []},
            "gates": {...}, "discrepancies": [...], "executions": [...], "enrichment": [...]}]}
```

`data_root` (the same folder as inspect's `--data-root`) makes relative `metadata` and `matrix` paths resolve inside it; absolute paths are used as given. `inputs`: give `matrix` or `"raw_tar": true` (merges `data/<GSE>/<GSE>_RAW.tar`; tar columns become GSM ids). When the deposited file must be repaired first (Excel-mangled gene names, broken rows, lanes to merge), write one small script, save its output, point `matrix` at it and list the script in `prep_scripts`.

Every gate has `final` (your decision), `reasoning` (with paper locators), `confidence` (`high`/`medium`/`low`), optional `locator`, `candidates` (rejected alternatives: `{"value", "reason_rejected"}`), and `decision_status` (`valid` by default; `refused`/`manual_review`/`unresolved` with `stop_reason` stops the case there — omit the later gates). The runner adds the computed facts to each record; you cannot overwrite them.

| Gate | Your fields | `final` must hold | The runner adds |
|---|---|---|---|
| `paper_reconstruction` | | `accessions`, `primary_estimand`, `planned_contrasts`, `paper_threshold` (object), plus factors, inclusion, method, paper results | |
| `ownership` | | `owned` (true/false), checks | accession, files |
| `alignment` | `key_column` (null = metadata index), `aliases`, `patterns` (`{"grp": ["title", "regex"]}`; several groups are joined with `_`), `combine` (`{"tgrp": ["diet", "time"]}`, joins the recoded source values with `_`), `recode` (every value mapped; a combined column is recoded after it is built, so its keys use the recoded source values, e.g. `HC_BL`), `key_patterns` (derive the key column itself first), `exclude_samples` (`{id: reason}`) | | method, coverage, unmatched IDs, derived columns and levels |
| `matrix` | `matrix_type`, `recommended_method` | source, paper input | profile |
| `design` | `factors`, `references`, `subject`, `organism` (`Mouse`/`Human`/`Rat`), `planned` (suitability names `<factor>_<test>_vs_<ref>`, plus `_<stratum>-<level>` per stratum), `covariate_candidates`, `strata` (columns analyzed separately, such as sorted fractions or tissues: comparisons never cross them) | `analysis_type`, `design_column` or `formula`, `contrasts` or `control`+`treatment` | suitability verdict |
| `covariance` | `confounding_candidates` | `status` (`required`/`not_required`), `blocking_terms`, `covariates` (`{"name", "disposition"}`) | design check, confounding report |
| `method` | `transform` (`log2(x+1)`, `log2(CPM+1)`, `beta_to_m`, `round`) | `method` (named first: `DESeq2`, `limma`, `edgeR`, ...), `formula`, `paper_route`, `deviations`; `rounding_documented: true` for estimated counts | `matrix_type` |
| `threshold` | | `paper_threshold`, `threshold_source` (`paper`, `paper_on_deviation_route`, `workflow_default`), `applied_threshold`, optional `audit_threshold`, `deviation_note` | |
| `study` | `paper_counts` (`{table: paper's DEG count}`), `paper_genes` (`{table: [genes]}`) | `route` (`paper_aligned`, `declared_deviation`, `exploratory`), caveats | our counts vs paper, gene lookups |

Derived column names must be formula-safe (`grp`, `time`, `subject`); use them in every formula and argument.

Thresholds: `{"metric": "padj"|"pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}`. `effect_cutoff: null` means no fold-change rule. `inclusive` covers both cutoffs unless `effect_inclusive` is set ("P < 0.05 and |log2FC| >= 0.5": `inclusive: false, effect_inclusive: true`); an asymmetric rule ("FC > 1.2 or < 0.83") sets `effect_cutoff` for up and `effect_cutoff_down` (a positive magnitude) for down. The applied rule must equal `paper_threshold` when the source is `paper` or `paper_on_deviation_route`.

## 3. Executions

Each execution: `name` (also the result-table name), `tool`, `args`, `role` (`primary` for the main contrast, `secondary`, `sensitivity`, `exploratory`), `reasoning`. The runner passes the matrix, `metadata_csv` and `output_dir` itself.

| Route | `tool` | `args` |
|---|---|---|
| DESeq2 two arms, optional blocking | `tools.deseq2_tools:run_deseq2_analysis` | `design_column`, `control_group`, `treatment_group`, `covariate_columns` (e.g. `"subject"`), `alpha` (= paper FDR) |
| every comparison from one DESeq2 model | `tools.joint_contrasts:run_joint_deseq2` | `comparisons`: `"planned"`, `"all"` or a list of suitability names; `covariates`; `include` (small-n planned contrasts, label exploratory); `round_estimated_counts` |
| limma two arms (log-scale input) | `tools.limma_tools:run_limma_analysis` | as DESeq2, plus `design_formula`, `coefficient` |
| every comparison from one limma model | `tools.joint_contrasts:run_joint_limma` | `comparisons`, `covariates` |
| limma multilevel / factorial / paired change | `tools.multigroup_tools:run_multigroup_analysis` | `plan` (see [Native execution](native-execution.md#multigroup-plan)) |
| edgeR (TMM), two arms | `tools.edger_tools:run_edger_analysis` | `design_column`, `control_group`, `treatment_group` |
| limma-voom (needs R) | `tools.limma_voom_tools:run_limma_voom_analysis` | as edgeR |

For separate fits per fraction, put the fraction column in `strata`, the treatment in `factors`, and give each execution a `subset` of one fraction.

Per execution, optionally: `subset` (`{"tissue": ["soleus"]}` keeps those samples), `complete_pairs` (`{"subject": "subject", "condition": "time", "levels": ["pre", "post"]}`), `filter_low_counts` (`{"min_cpm": 1, "min_samples": 3}`: keep genes with CPM >= min_cpm in at least min_samples of this execution's samples, for a paper that filters low counts; raw counts only), `transform` (this execution only, for example `log2(CPM+1)` for a limma sensitivity run next to DESeq2), `matrix: "aligned"` (skip the case-level transform).

Joint and multigroup executions return one table per comparison, named `<execution>/<comparison>`; use those names in `paper_counts`, `paper_genes` and `enrichment`.

## 4. Enrichment

`{"execution": "<table name>", "ora": true, "gsea": true, "direction": "all", "ranking_metric": "stat", "reasoning": "..."}`. ORA uses the applied threshold (recorded as an audit rule when the applied metric is raw p); GSEA uses the full ranking. Up and down ORA for one table are two entries (`"direction": "up"` / `"down"`); each writes to its own folder. IDs that are not gene symbols or Ensembl genes are recorded as `not_run`. Rat runs on mouse gene sets by symbol.

## 5. Execute and fix

`execute` prints, per case: alignment, levels, suitability verdict, each table's counts (`n`, `up`, `down`, `audit_n`), enrichment status, our counts vs the paper's, the gene lookups, and the contract validator's errors.

- `spec_error`: a field is missing or malformed; fix the spec.
- `cases[i].error`: a step raised (for example a regex that does not match every row, an unmapped recode value, a `not_analyzable` suitability verdict on a valid design). Fix the spec and run `execute` again. The previous attempt moves to `<run_dir>/_previous/`; nothing is deleted.
- A failed executor is recorded as `valid` + `failed` with its error; that is an acceptable outcome, not a reason to write your own model.

When the runner cannot express the analysis (single-cell, proteomics, methylation pipelines, an extra analysis such as DEG-set overlaps), use the scripted route in [Native execution](native-execution.md) for that case.
