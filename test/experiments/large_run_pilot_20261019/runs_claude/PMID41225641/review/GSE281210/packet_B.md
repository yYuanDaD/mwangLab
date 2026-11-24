# Review packet B (the analysis' decisions): GSE281210

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of key", "across": "characteristics_ch1.3.treatment", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"characteristics_ch1.3.treatment": ["hindlib unloading"], "treatment_protocol_ch1": ["Mice were treated with or without hindlimb unloading for four weeks."]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the only comparison in GSE281210 is 4-week hindlimb unloading (disuse) vs normally loaded control. There is no exercise, training or reloading arm, so the requested exercise estimand cannot be identified. Reversing HU vs control would not be an exercise effect (normal cage activity is not an exercise intervention).

## Samples per design level

### `grp`
- **Con** (3): GSM8614889 / BM control 1; GSM8614890 / BM control 2; GSM8614891 / BM control 3
- **HU** (3): GSM8614892 / BM OP-HU1; GSM8614893 / BM OP-HU2; GSM8614894 / BM OP-HU3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE281210", "GSE281970"], "assay": "GSE281210: bulk RNA-seq of whole bone marrow cells (S2.6.p1, FIG3); GSE281970: scRNA-seq of Lin- c-kit+ HSPCs (S2.8.p1), not analyzed here", "factors": {"condition": ["Con (ground-loaded control)", "OP-HU (28-day hindlimb unloading)"]}, "sample_inclusion": "male C57BL/6, 8 weeks old, HU for 28 days (S2.1.p1); bulk RNA-seq 3 replicates per group (FIG3)", "primary_estimand": "Effect of 4-week hindlimb unloading (mechanical unloading / disuse osteoporosis) vs normally loaded control on bone marrow gene expression. No exercise or training arm exists anywhere in the study.", "planned_contrasts": ["OP-HU vs Con, whole bone marrow bulk RNA-seq (S3.3.p1, FIG3; DEG count not reported)"], "repeated_measure_unit": "none (independent mice)", "paper_method": "DESeq2 1.20.0 (S2.6.p1); GO by clusterProfiler", "paper_threshold": {"metric": null, "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "not stated for RNA-seq DEGs (S2.6.p1); S2.9.2.p1 p<0.05 refers to Prism t-tests"}, "paper_results": "heatmap of changed genes; GO of downregulated leukocyte-differentiation terms; Pf4 down (p=0.0002, FPKM t-test), Tgfb1 slightly down (FIG3C); Ccl3 down, Ccl5 up (FIG S2B)"}

reasoning: Paper studies hindlimb unloading (HU) as a disuse-osteoporosis model (ABS.p2, S2.1.p1, S3.1.p1). Bulk RNA-seq (GSE281210, DA.p1) compares OP-HU vs control whole bone marrow, n=3/group (FIG3A). JQ-1 arm (S3.6.p2) is not in the bulk dataset. No exercise, training or reloading intervention is described.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE281210\\GSE281210_Gene_count_for_all_bone_marrow_cell_samples.txt.gz", "owned": true, "checks": ["DA.p1 names GSE281210 for bulk RNA-seq", "GEO: femur bone marrow cells, Mus musculus, treatment_protocol 'with or without hindlimb unloading for four weeks'", "6 samples = 3 control + 3 OP-HU matches FIG3A", "featureCounts/HISAT2 on NovaSeq 6000 matches S2.6.p1 (Novogene)"], "accession": "GSE281210", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE281210\\GSE281210_metadata.csv"}

reasoning: Series, tissue, design and sample number all match the paper's bulk RNA-seq.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41225641\\GSE281210\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^BM (control|OP-HU) ?\\d$", "recode": {"control": "Con", "OP-HU": "HU"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41225641\\GSE281210\\aligned\\design_metadata.csv", "sha256": "196d48a10b2f8167aa728002a2585204e33f352fb9614b92801134d499eb6c7b", "levels": {"grp": {"Con": 3, "HU": 3}}}}

reasoning: Metadata titles 'BM control N' / 'BM OP-HUN' correspond to matrix columns ConN / OP-HUN; keys built as con_N / OP-HU_N on both sides and matched ignoring case. grp = Con / HU.

### matrix (valid, not_started)

final: {"source": "GSE281210_Gene_count_for_all_bone_marrow_cell_samples.txt.gz", "paper_input": "DESeq2 on gene counts (S2.6.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41225641\\GSE281210\\aligned\\aligned_matrix.csv", "sha256": "b2e3b152c8d3a4770b37d8742e40aaaff0cee7ec75b19ada8b7fc15be1922783", "n_features": 54532, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 224759.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: 100% integer values, max 224759; data_processing states featureCounts v1.5.0-p3 read counts; file named Gene_count.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "grp", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41225641\\GSE281210\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: S2.1.p1/S3.1.p1: intervention is hindlimb unloading; GEO characteristics treatment='hindlib unloading', treatment_protocol 'with or without hindlimb unloading'. The paper's own contrast (OP-HU vs Con) is analyzable (n=3/group) but answers a disuse question, not the requested exercise question.

rejected alternatives: [{"value": "grp_HU_vs_Con as an exercise proxy", "reason_rejected": "unloading/disuse is not exercise; control is ordinary cage activity, not training; would mislabel the estimand"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "requested estimand",
    "paper": "hindlimb unloading vs control (disuse osteoporosis)",
    "data": "Con x3, OP-HU x3; no exercise samples",
    "disposition": "refused"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID41225641 / GSE281210

**Status: refused at the `design` gate.** The data contain no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE281210` (data were already cached). Found one matrix, `GSE281210_Gene_count_for_all_bone_marrow_cell_samples.txt.gz`: 54,532 Ensembl genes × 6 samples, 100% integer values, counted with featureCounts. The series has 6 GSMs: `BM control 1-3` and `BM OP-HU1-3`.
- Paper read: `PMC12607142.paper.md`. The study uses 28-day hindlimb unloading (HU) to model disuse osteoporosis in male C57BL/6 mice (S2.1.p1, S3.1.p1). The bulk RNA-seq is whole bone marrow, OP-HU vs Con, n=3 per group (FIG3A), analyzed with DESeq2 1.20.0 (S2.6.p1). GSE281970 (scRNA-seq) is the other deposited series; it was not analyzed. The JQ-1 arm is not in the bulk data.
- `python -m tools.case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership (owned), alignment (6/6 samples, exact match after building keys from the titles and matrix columns and matching them ignoring case), matrix (raw counts → DESeq2), and design (refused). The contract validator returned 0 errors. Suitability rated OP-HU vs Con as analyzable, but that contrast measures disuse, not exercise.

## Why refused
The only intervention is mechanical unloading. There is no exercise, training or reloading arm. The control mice had ordinary cage activity, so reversing the sign of HU vs Con would not estimate an exercise effect. Nothing was executed, and enrichment was not run.

## DEG counts vs paper
- Ours: none (refused).
- Paper: no bulk DEG count is reported, and no DEG threshold is stated for the RNA-seq (S2.6.p1). The p<0.05 in S2.9.2.p1 applies to Prism t-tests. The paper reports only a heatmap, GO terms for down-regulated genes (leukocyte differentiation), Pf4 down, Tgfb1 slightly down, Ccl3 down and Ccl5 up.

## Deviations
None. No analysis was run.

## Tool problems
- None blocking.
- One difficulty: the metadata titles (`BM control 1`) and the matrix columns (`Con1`) use different words, so I had to combine `key_patterns`, `matrix_column_pattern` and `normalize_keys` (`tools/case_runner.py:550-585`). Inspect's `alignment_keys` reported only 3 of 6 matched via `title (contains the name)`, and it gave no hint for the control half.
- GEO metadata spells the treatment "hindlib unloading". That is a submitter typo and was handled.

