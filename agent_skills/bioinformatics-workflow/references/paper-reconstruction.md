# Paper-first reconstruction

Use this reference whenever a paper, DOI, PDF, paper-derived GEO case, or article-specific validation question is available. The goal is to reproduce the paper's stated analysis and then test whether the available data and implementation support that reproduction.

## Study map

Before inspecting candidate contrasts, extract an evidence-backed study map:

```json
{
  "paper_id": "doi or local paper id",
  "accessions": [],
  "assay": "bulk RNA-seq|single-cell|spatial|proteomics|...",
  "sample_inclusion": [],
  "sample_exclusion": [],
  "factors": [{"name": "exercise", "levels": []}],
  "primary_estimand": "the biological effect the paper claims",
  "planned_contrasts": [],
  "blocking_or_covariance": {"status": "required|not_required|unresolved"},
  "matrix_scale": "raw counts|log2 FPKM|...",
  "paper_method": "DESeq2|limma|...",
  "paper_formula": null,
  "paper_threshold": {
    "metric": "FDR|padj|pvalue|null",
    "cutoff": null,
    "effect_metric": "log2FC|fold_change|null",
    "effect_cutoff": null,
    "source_locator": "Methods/Table/Figure/Supplement"
  }
}
```

Every non-null field must point to a paper or supplementary evidence item. If the paper does not state a field, write `unknown` or `not_reported`; do not infer it from a familiar workflow and present it as a paper fact.

Use the paper to choose which accession and samples answer the stated question. GEO metadata is then used to map that paper-defined set to actual sample IDs. A keyword match such as `exercise` or `control` is only supporting evidence when the article's study map is available.

## Reproduction versus validation

Keep two linked but separate outputs:

1. **Paper-aligned reproduction**: the accession, sample set, formula, method, contrast, normalization, and threshold as reported by the article, subject to explicit data availability checks.
2. **Validation review**: checks matrix/method compatibility, sample coverage, design rank, residual degrees of freedom, covariance/blocking, and whether the paper route can be executed safely on the available files.

If the paper's method cannot be reproduced because the deposited matrix has a different scale or an essential file is missing, preserve the paper route in the record and mark the deviation. A validated alternative may be run only as a separate analysis with its own method and threshold provenance. Never silently replace the paper's route and call it a reproduction.

## Paper/data discrepancies

Create a discrepancy record when any of these differ:

- accession ownership or study scope;
- paper sample inclusion/exclusion versus GEO metadata;
- control/treatment labels or factor levels;
- paired, donor, batch, time, or interaction structure;
- matrix scale or normalization;
- statistical method or formula;
- threshold metric or effect-size cutoff.

Classify each discrepancy as `executable_without_change`, `requires_explicit_deviation`, or `blocks_reproduction`. A discrepancy blocks the paper-aligned run when it changes the primary estimand, sample assignment, covariance/blocking, matrix-method compatibility, or the interpretation of the threshold.

## Threshold handling

Preserve the paper's exact threshold semantics:

- `FDR < 0.05` is not interchangeable with raw `p < 0.05`;
- `|log2FC| > 0.5`, `|log2FC| > 1`, and a fold-change cutoff are distinct rules;
- an article that reports only an adjusted-p-value cutoff has no implied effect-size cutoff;
- if the paper reports different thresholds for different contrasts, keep them contrast-specific.

For a paper-aligned result, use `paper_threshold`. For cross-study comparison or sensitivity analysis, optionally calculate a separate `audit_threshold` and report both. If the paper threshold is absent, use the workflow default only with `threshold_source=workflow_default` and mark the result as a fallback. Threshold choice cannot override a failed design, covariance, matrix, or sample-alignment gate.

## Minimum output

Save these artifacts when paper-first mode is used:

- `paper_reconstruction.json`: study map, evidence IDs, and paper threshold;
- `paper_data_discrepancies.json`: paper-versus-GEO/data differences and their disposition;
- `reproduction_plan.json`: exact paper-aligned route and any declared deviation;
- `reproduction_summary.json`: paper-aligned result, validation status, threshold used, and comparison to reported findings.

The final response should say which parts of the paper were reproduced, which were validated independently, which discrepancies remain, and whether any result is exploratory or blocked. Do not summarize success only by the number of p-values or DEGs.
