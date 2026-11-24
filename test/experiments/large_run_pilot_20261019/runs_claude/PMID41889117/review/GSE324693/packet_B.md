# Review packet B (the analysis' decisions): GSE324693

## Mechanical flags

- none

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: GSE324693 holds only Vehicle (water) vs EtOH WAT samples (6/6). Exercise appears in the paper only as a treadmill performance test given to all mice (S2.4.2.p1), so the data cannot identify an exercise effect on gene expression.

## Samples per design level

### `grp`
- **CTRL** (6): GSM9583069 / S1 ctrl / Library name: Sample1; GSM9583070 / S2 ctrl / Library name: Sample2; GSM9583071 / S3 ctrl / Library name: Sample3; GSM9583072 / S4 ctrl / Library name: Sample4; GSM9583073 / S5 ctrl / Library name: Sample5; GSM9583074 / S6 ctrl / Library name: Sample6
- **ETOH** (6): GSM9583075 / S7 EtOH / Library name: Sample7; GSM9583076 / S8 EtOH / Library name: Sample8; GSM9583077 / S9 EtOH / Library name: Sample9; GSM9583078 / S10 EtOH / Library name: Sample10; GSM9583079 / S11 EtOH / Library name: Sample11; GSM9583080 / S12 EtOH / Library name: Sample12

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE324693"], "assay": "bulk RNA-seq, subcutaneous white adipose tissue (S2.4.16.p1)", "primary_estimand": "Effect of 60 weeks of 20% EtOH in drinking water vs water (control) on subcutaneous WAT gene expression in aged female C57BL/6 mice (S2.2.p1, S3.4.p3). There is no exercise intervention: the treadmill was used only as a time-to-fatigue performance test (S2.4.2.p1, week 55), given to every mouse in both groups.", "factors": {"treatment": ["Control (water/Vehicle)", "EtOH"]}, "inclusion": "17 female mice (7 control, 10 EtOH); RNA-seq on 6 vs 6 (GEO); paper figure n 5-6 control / 6-9 EtOH (FIG7)", "planned_contrasts": ["EtOH vs Control in WAT (S3.4.p3; paper: 61 DEGs, 47 down / 14 up)"], "exercise_contrasts": [], "repeated_measure_unit": "none (one WAT sample per mouse at sacrifice)", "paper_method": "Rsubread featureCounts; keep genes mapped in >= 6 samples; DESeq2 v1.44.0 (S2.4.16.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "inclusive": true, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.4.16.p1"}, "paper_results": {"EtOH_vs_Control": {"n_deg": 61, "down": 47, "up": 14, "named_genes": ["Cyp2e1"], "locator": "S3.4.p3"}}}

reasoning: S2.2.p1: mice were randomized to 20% EtOH or water. S2.4.2.p1: treadmill endurance was an outcome test, not a training stimulus. S2.4.16.p1: WAT RNA-seq, DESeq2, FDR <= 0.1. S3.4.p3: 61 DEGs (47 down). The paper never compares exercised and non-exercised animals.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE324693\\GSE324693_counts_matrix.csv.gz", "owned": true, "checks": ["S2.4.16.p1 names GSE324693", "GEO tissue = subcutaneous WAT, C57BL/6, Mus musculus, matching the paper", "treatment Vehicle/EtOH, 6/6, matching the paper's two groups", "data_processing: Rsubread + featureCounts raw counts, matching S2.4.16.p1"], "accession": "GSE324693", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE324693\\GSE324693_metadata.csv"}

reasoning: The accession, tissue, strain, groups and processing all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:skey", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41889117\\GSE324693\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.2.treatment", "recode": {"Vehicle": "CTRL", "EtOH": "ETOH"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41889117\\GSE324693\\aligned\\design_metadata.csv", "sha256": "d51ed25e4e42e226fe475ac620ff198b6dc1ff82b421e711d0c8ceb17ead41b4", "levels": {"grp": {"CTRL": 6, "ETOH": 6}}}}

reasoning: Matrix columns S1.bam..S12.bam; the GEO titles are 'S1 ctrl'..'S12 EtOH'. The key is the S<n> token, an exact match on a named field, not position.

### matrix (valid, not_started)

final: {"source": "GSE324693_counts_matrix.csv.gz", "paper_input": "featureCounts raw counts into DESeq2 (S2.4.16.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41889117\\GSE324693\\aligned\\aligned_matrix.csv", "sha256": "8bf2263e87dcdbc3e0dfd654a56428a9b08a6d8c3ee1314289062f6ec97a4b4d", "n_features": 56941, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 5814667.0, "median": 2.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Values are 100% integers, from 0 to 5.8e6; GEO data_processing says 'Raw counts matrix' from Rsubread/featureCounts. This matches the paper's DESeq2 input.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "grp", "contrasts": [], "exercise_factor_present": false, "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41889117\\GSE324693\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: The only grouping column is treatment (Vehicle 6 / EtOH 6). The task's estimand, an exercise effect, has no arm in the paper or the data.

rejected alternatives: [{"value": "grp_ETOH_vs_CTRL as an exercise contrast", "reason_rejected": "EtOH vs water is an alcohol exposure, not exercise; reporting it as an exercise effect would change the estimand"}, {"value": "treadmill-tested vs untested animals", "reason_rejected": "every mouse took the same treadmill endurance test (S2.4.2.p1, FIG2 week 55); there is no unexercised comparison group and no exercise column in GEO"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample size",
    "paper": "17 mice (7 control/10 EtOH); FIG7 n 5-6 control / 6-9 EtOH",
    "data": "12 RNA-seq samples (6/6)",
    "disposition": "not_relevant_case_refused"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID41889117 / GSE324693

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE324693 --data-root E:/agent/mwangLab_pdf/data`: the data were already cached. It found one matrix, `GSE324693_counts_matrix.csv.gz` (56,941 Ensembl genes × 12 samples, all integers, raw featureCounts output). The only grouping column is `characteristics_ch1.2.treatment` (Vehicle 6 / EtOH 6). Tissue: subcutaneous WAT.
- I wrote `case_spec.json` with the gates paper_reconstruction → ownership → alignment → matrix → design, where design is refused. `python -m tools.case_runner execute` completed, and the validator wrote 5 records with 0 errors.
- Alignment: an exact match on the `S<n>` key, taken from the GEO title (`S1 ctrl`) and from the matrix column (`S1.bam`). All 12 of 12 samples aligned. Suitability: analyzable for EtOH vs control, which is not an exercise comparison.

## Why it was refused
The paper is a chronic-ethanol study: 20% EtOH in drinking water vs water for 60 weeks in female C57BL/6 mice (S2.2.p1). Exercise appears only as a treadmill time-to-fatigue *performance test*, and every mouse in both groups took it (S2.4.2.p1, FIG2 week 55). The paper has no exercise intervention or unexercised comparison group, and neither does GEO. Reporting EtOH vs control as an exercise effect would change the estimand.

## DEG counts vs the paper
- The paper's contrast is EtOH vs control in WAT, using DESeq2 with genes kept if they map in ≥6 samples, at a threshold of FDR ≤ 0.1 with no fold-change cutoff (S2.4.16.p1). It reports 61 DEGs: 47 down and 14 up, with Cyp2e1 among them (S3.4.p3).
- Ours: none were computed, because the case was refused before any execution. The data could support the paper's EtOH contrast (6 vs 6 raw counts), but that contrast is not about exercise.

## Deviations
- None. No analysis ran.
- Discrepancy noted: the paper had 7 control and 10 EtOH mice, and FIG7 gives RNA-seq n as 5–6 / 6–9. GEO holds 6 / 6.

## Tool problems
- None blocking.
- Minor: inspect reported `alignment_keys: []` because the matrix columns carry a `.bam` suffix (`S1.bam`) and the titles carry a group suffix (`S1 ctrl`). I needed both `key_patterns` and `matrix_column_pattern` to align them. Inspect could suggest stripping a `.bam` suffix.

