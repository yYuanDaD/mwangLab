# Decision contract (v2)

Write one record per gate per case, in gate order. A record is an audit object, not a transcript of reasoning. `RunRecorder.case(...).decide(...)` fills the common fields and rejects records that break this contract. `scripts/validate_decision_contract.py` applies the same checks to saved files (implementation: `tools/decision_contract.py`).

## Record

```json
{
  "contract_version": "2",
  "case_id": "case_01",
  "stage": "covariance",
  "evidence": [{"id": "metadata:GSE1_metadata.csv", "kind": "metadata", "sha256": "..."}],
  "candidates": [{"value": "~ time", "reason_rejected": "ignores within-subject pairing"}],
  "final": {"status": "required", "blocking_terms": ["subject"], "covariates": []},
  "paper": {"locator": "S2.4.p1"},
  "confidence": "high",
  "reasoning": "8 subjects each sampled pre and post; paper models ~ subject + time.",
  "decision_status": "valid",
  "execution_status": "not_started",
  "stop_reason": null
}
```

- `evidence`: a non-empty list. Every item is an object with `id` and `kind` (`paper`, `metadata`, `matrix`, `tool_output`, or `user`); add `sha256` and `path` when a file is involved.
- `paper.locator`: a block ID from the structured paper (`S2.4.p1`, `TAB1`, `FIG2`, `DA.p1`; see [Paper reconstruction](paper-reconstruction.md#reading-the-paper)). Use a free-text locator such as "Methods, paragraph 2" only when no structured copy exists.
- `confidence`: `high`, `medium`, or `low`.
- `decision_status`: `valid`, `unresolved`, `manual_review`, or `refused`.
- `execution_status`: `not_started`, `completed`, `failed`, or `not_run`.

## Required `final` fields for a valid decision

| Stage | Required fields | Notes |
|---|---|---|
| `paper_reconstruction` | `accessions`, `primary_estimand`, `planned_contrasts`, `paper_threshold` (object) | Write `not_reported` for absent facts; never fill them from a workflow default |
| `ownership` | `accession`, `matrix_file`, `metadata_file`, `owned` | `owned` is true only when the files belong to the paper's samples. Evidence: the accession or series ID in the metadata or file name, and sample counts, groups, and labels that match the paper's description. When the metadata carries no accession, record the checks that were possible and use `medium` confidence |
| `alignment` | `method`, `n_aligned`, `n_metadata`, `coverage` (0–1) | List unmatched IDs when coverage < 1 |
| `matrix` | `matrix_type`, `recommended_method` | Use the type words from the matrix policy (`raw counts`, `estimated counts`, `FPKM`, `TPM`, `log2 ...`, `RMA log2`, `beta`) |
| `design` | `analysis_type`, `formula` or `design_column`, `contrasts` or `control` + `treatment` | Use `paired`, `repeated`, or `paired_change` in `analysis_type` for within-subject designs. Add `estimand_type: associational` for cross-sectional group comparisons |
| `covariance` | `status`, `blocking_terms`, `covariates` | `status` is `required`, `not_required`, or `unresolved`. `covariates` lists each candidate with a disposition (`included`, `excluded: reason`, `aliased`, `nested`). Use the formula-safe names from `derive_columns` |
| `method` | `method`, `matrix_type`, plus `formula` when the model has more than one term | Start `method` with the method name (`DESeq2`, `edgeR`, `limma-voom`, `limma`). Add `transform` (for example `log2(x+1)`, `log2(CPM+1)`, `beta-to-M`) whenever limma runs on data that were not already log-scale. When the paper's own route cannot run, add `paper_route: {"method": ..., "status": "blocked", "reason": ...}`; the record itself stays `valid` for the alternative. Record the low-count gene filter as `prefilter` for count methods |
| `threshold` | `paper_threshold`, `threshold_source`, `applied_threshold` | `threshold_source`: `paper`, `paper_on_deviation_route`, `workflow_default`, `audit`. `metric` names: `FDR`, `padj`, and `qvalue` are all adjusted p-values; `pvalue` is raw. When the adjustment method changes (for example permutation FDR to BH), use `paper_on_deviation_route` and add `deviation_note` |
| `execution` | `method`; `outputs` when completed; `execution_error` when failed; `reason_not_run` when planned but not attempted | One record per analysis unit; add `subset` (for example a cell type) when a case runs several |
| `enrichment` (optional) | `method`, `gene_sets`, `organism`, `feature_id_type`; `outputs` or `execution_error` | ORA also needs `input_threshold` and `input_threshold_source` (`applied` or `audit`). IDs other than gene symbols or Ensembl gene IDs need `id_mapping`; species other than Mouse or Human need `ortholog_mapping`. See [Modalities](modalities.md) |
| `study` | `route` | `paper_aligned`, `declared_deviation`, or `exploratory`: the planned route, also when execution failed. Not written for stopped cases |

Other rules for these fields:
- A blocked decision (`unresolved`, `manual_review`, `refused`) needs only `stop_reason`. For a refused covariance gate, use `status: unresolved` and list the aliased covariate in `covariates` with disposition `aliased`.
- A requested `enrichment` that cannot run (no completed DE table, missing packages, no network) is recorded as `valid` + `not_run` with `final.reason_not_run`, so the plan is not lost.
- A valid decision never has a `stop_reason`. When a valid plan fails to run, the execution record is `valid` + `failed` with `final.execution_error`.
- Decision gates keep `execution_status: not_started` (or `not_run` when blocked). Only `execution` and `enrichment` records carry `completed` or `failed`.
- A refused or failed `enrichment` does not stop the case or change its DE result.
- A stopped case has no gates after the stop and no `study` record. `case.finish()` reports its route as `stopped`.

## Status rules

- **`valid`**: the gate is decided and the case may proceed.
- **`refused`**: the available data cannot identify the requested estimand, and no review would change that. Examples:
  - no exercise contrast in the sequenced samples;
  - treatment completely confounded with batch;
  - a prognostic, clustering, or validation-only design with no comparison that answers the request. A cross-sectional comparison defined by the paper stays `valid` with `estimand_type: associational`.
- **`manual_review`**: a specific fact or executor could unblock the gate. Examples:
  - unknown subject mapping;
  - ambiguous matrix scale;
  - a missing file;
  - a design the available executors cannot fit.
- **`unresolved`**: an interim state. Resolve it, or turn it into one of the two above, before the case ends.

Do not invent other status strings. Put the wording in `stop_reason`.

## Thresholds, small studies, and multiplicity

- `paper_threshold` copies the article's metric, cutoff, and effect rule exactly (`metric`, `adjustment`, `cutoff`, `effect_metric`, `effect_cutoff`, `inclusive`, `source_locator`). A fold change of 1.5 is `effect_cutoff: 0.5849625` (`log2(1.5)`, not rounded) on log2FC; keep the original in `effect_cutoff_original`.
- `threshold_source` and `applied_threshold`:
  - `paper`: the applied rule equals the paper rule.
  - `paper_on_deviation_route`: the paper rule applied to a declared alternative method.
  - `workflow_default`: BH-adjusted p < 0.05 and no effect-size cutoff, used only when the paper states nothing.
  - `audit`: a separate, labelled comparison rule.
- **Exploratory label:** apply it when any arm or cell has fewer than 3 biological replicates, or when residual df < 4. Record the rule in `study.final.exploratory_reason`. Small n alone is not a stop.
- **Multiplicity:** when the paper is silent, apply BH within each planned contrast (paper-aligned). A family-wide correction across contrasts can be reported as `audit`.

## Invariants the validator enforces per case

1. Nothing is `completed` when any gate of the case is blocked.
2. A completed execution needs valid `alignment`, `matrix`, `design`, `covariance`, `method`, and `threshold` records.
3. Method and matrix agree:
   - no DESeq2, edgeR, or voom on FPKM, TPM, log-scale, or beta data;
   - no count method on estimated counts without `rounding_documented`;
   - no limma on raw counts, linear data, or beta values without a `transform`;
   - no method at all when the matrix type is ambiguous.
4. A design described as paired, repeated, or longitudinal has covariance `required`.
5. Every required blocking term and included covariate appears in a recorded formula. Paired-change designs are exempt, because differencing removes the subject effect.
6. With `threshold_source` `paper` or `paper_on_deviation_route`, the applied rule equals the paper rule (metric names compared by kind). A changed adjustment method needs `paper_on_deviation_route` and `deviation_note`.
7. An enrichment is `completed` only after a completed execution. An ORA list marked `applied` uses the applied threshold. IDs and species need the mappings listed above.
8. Decision gates never carry `completed` or `failed` (the `study` record may mirror the execution outcome). A valid run stage marked `not_run` needs `reason_not_run`.

The validator cannot check whether a decision matches the paper; for example, it cannot detect a wrong effect cutoff that was copied into both fields. Use the evaluation protocol with a scorer-side answer key for that.

## Separation of decision and execution

Score these independently:

1. **Decision correctness**: matrix semantics, alignment, contrast, covariance, and method route are scientifically defensible.
2. **Execution correctness**: the selected tool completed and produced internally valid artifacts.

An execution failure after a valid decision is not a decision error. A p-value produced after an invalid decision is a blocking failure, even when the command succeeded.
