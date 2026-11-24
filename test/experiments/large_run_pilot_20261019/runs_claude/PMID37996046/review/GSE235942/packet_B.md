# Review packet B (the analysis' decisions): GSE235942

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.2.age level", "across": "characteristics_ch1.2.age", "pairs_or_sets": 11, "samples_linked": 22, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the series contains only control and hindlimb-unloaded (disuse) mice at 6 and 22 months (paper S2.1.p1, GEO treatment column control/HLU). Neither disuse nor aging can stand in for an exercise effect, so the requested estimand is not identifiable.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE235942"], "assay": "bulk RNA-seq, marrow-flushed tibia (S2.4.p1)", "factors": {"treatment": ["control", "HLU (hindlimb unloading, 3 weeks)"], "age": ["6 month", "22 month"], "sex": "paper analyses males; GEO also holds female controls"}, "primary_estimand": "Effect of disuse (hindlimb unloading) and of aging on tibial gene expression; no exercise intervention (ABS.p2, S2.1.p1)", "planned_contrasts": ["6mo HLU vs 6mo control (Fig 5C/H)", "22mo control vs 6mo control (Fig 5E/I)", "4mo HLU vs control (Fig 5A/G; from a prior study, not in this series)"], "paper_method": "BioJupies kallisto counts, logCPM, limma (S2.4.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "logFC", "effect_cutoff": 1.5, "source_locator": "S3.3.p2", "note": "'logFC > |1.5| and p-value < 0.05' (raw p, no FDR)"}, "paper_results": "No DEG counts stated in text; volcano plots only (Fig 5G-I). Exercise is mentioned only as a general countermeasure (S1.p1, S4.p8)."}

reasoning: Paper compares hindlimb unloading (disuse) with aging in male C57BL/6J mice (ABS.p2, S2.1.p1). DE: limma on kallisto counts, threshold raw p<0.05 & logFC>|1.5| (S3.3.p2). No exercise, training or loading arm anywhere in methods or Table 1; 'exercise' appears only in Introduction/Discussion as background (S1.p1, S4.p8).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE235942\\GSE235942_raw_counts.txt.gz", "owned": true, "checks": ["S2.6.p1 names GSE235942", "GEO tissue marrow-flushed tibia, BioJupies processing, C57BL/6 ages 6/22 months match S2.1.p1/S2.4.p1"], "accession": "GSE235942", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE235942\\GSE235942_metadata.csv"}

reasoning: Data availability statement S2.6.p1 deposits RNA-seq under GSE235942; metadata matches the paper's tissue, ages and HLU treatment.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 30, "n_metadata": 30, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37996046\\GSE235942\\aligned\\aligned_metadata.csv", "columns": {"treatment": {"alias_of": "characteristics_ch1.4.treatment", "recode": {"control": "CTRL", "HLU": "HLU"}}, "sex": {"alias_of": "characteristics_ch1.1.gender"}, "age": {"source": "characteristics_ch1.2.age", "regex": "^([0-9]+)-month", "recode": {"6": "m6", "22": "m22"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37996046\\GSE235942\\aligned\\design_metadata.csv", "sha256": "a7a11184365f52fdf9beb63df14cf42cd9bc3b4135b21a89c64a48a6ca5b255a", "levels": {"treatment": {"CTRL": 22, "HLU": 8}, "sex": {"Male": 23, "Female": 7}, "age": {"m22": 16, "m6": 14}}}}

reasoning: Matrix columns (A1, AM1, YM3, ...) equal the metadata 'description' field for all 30 samples (inspect alignment_keys). Derived formula-safe columns treatment, age, sex.

### matrix (valid, not_started)

final: {"source": "GSE235942_raw_counts.txt.gz", "paper_input": "kallisto gene counts via BioJupies (S2.4.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37996046\\GSE235942\\aligned\\aligned_matrix.csv", "sha256": "c2745ca11ccfcc7992b94b9493af30c11ecfdd65d863dc1641fc13b7957be360", "n_features": 32544, "n_samples": 30, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2640370.0, "median": 11.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (integer_fraction 1.0), median 11, max 2.6e6; data_processing: 'raw counts per Sample' from BioJupies. kallisto estimated counts rounded by BioJupies; type not in doubt for the gate since the case stops at design.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": null, "contrasts": [], "exercise_arm": "absent", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37996046\\GSE235942\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: The requested estimand (effect of exercise) has no arm in this study. Running HLU vs control and relabelling it as exercise would invert the biology; the paper itself frames exercise only as background (S1.p1, S4.p8).

rejected alternatives: [{"value": "treatment HLU vs CTRL (6mo males)", "reason_rejected": "Hindlimb unloading is disuse, the opposite of exercise; it does not identify an exercise effect"}, {"value": "age m22 vs m6", "reason_rejected": "Aging contrast, not exercise"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample set",
    "paper": "male mice analysed; 4mo HLU group from a prior study",
    "data": "GEO also holds 7 female 22mo/6mo controls and 3 male 22mo HLU samples not described in the paper; no 4mo samples",
    "disposition": "not_executed_case_refused"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID37996046 / GSE235942

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE235942` (cached data): 1 matrix `GSE235942_raw_counts.txt.gz`, 32,544 gene symbols × 30 samples, all integer values; metadata matched exactly on the `description` column (30/30).
- `python -m tools.case_runner execute case_spec.json`: I recorded gates paper_reconstruction → ownership → alignment → matrix → design. The design gate is `refused`. The contract validator passed (5 records, 0 errors). The suitability report gave `analyzable` for the 5 HLU/age comparisons with no sex warnings. That only describes the data; it is not an exercise estimand.
- No DE executions and no enrichment were run.

## Why refused
The paper (ABS.p2, S2.1.p1, Table 1) compares **hindlimb unloading (HLU, i.e. disuse)** with **aging** in C57BL/6J mice. GEO has `treatment` = control (22) / HLU (8) and age = 6 mo (14) / 22 mo (16); 7 of the samples are female controls. The study has no exercise, training or mechanical-loading arm. Exercise comes up only as background (S1.p1, S4.p8). Neither HLU vs control nor 22 mo vs 6 mo identifies an effect of exercise. Relabelling disuse as "the opposite of exercise" would replace the requested estimand with a different one.

## DEG counts vs paper
- Paper threshold (S3.3.p2): "logFC > |1.5| and p-value < 0.05". This is raw p with no FDR, run in limma on BioJupies kallisto counts with logCPM (S2.4.p1). The text gives no DEG counts; only volcano plots (Fig 5G–I) show them.
- Ours: none computed (case refused). 0/0 contrasts.

## Deviations / notes
- GEO holds samples the paper does not describe: 7 female controls (6 and 22 mo) and 3 male 22 mo HLU samples. The paper's 4 mo HLU group comes from a prior study and is not in this series. I recorded this as a discrepancy and did not act on it, because the case stops first.

## Tool problems
- No tool defects. One self-inflicted issue: a bash heredoc collapsed `\\d` into `\d` in the spec's regex, which made the JSON invalid (`tools/case_runner.py:1115` raised a bare JSONDecodeError traceback rather than a `spec_error`). I fixed it by using `[0-9]`. A small usability gap: `execute` could report a malformed spec as `spec_error` instead of a traceback.

