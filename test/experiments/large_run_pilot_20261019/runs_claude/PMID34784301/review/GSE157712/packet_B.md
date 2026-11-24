# Review packet B (the analysis' decisions): GSE157712

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.0.subject id", "n_values": 15, "max_repeat": 2, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "subject", "n_values": 15, "max_repeat": 2, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the only factor is disease state (Control / CKD / Dialysis). The paper's planned contrasts are CKD vs Control and Dialysis vs CKD (S4.6.2.p2); no sample received an exercise intervention and both groups were sedentary (S2.1.p1). An exercise estimand cannot be identified from these data.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE157712"], "assay": "bulk RNA-seq, human vastus lateralis biopsies (S4.6.1.p1)", "primary_estimand": "Difference in muscle gene expression between non-dialysis CKD patients and healthy age-matched controls (disease state, associational); secondary: CKD pre- vs post-dialysis initiation. No exercise intervention or exercise arm exists; both groups were 'highly sedentary' (S2.1.p1).", "factors": {"group": ["Control", "CKD", "Dialysis"]}, "sample_inclusion": "7 CKD, 7 control (S2.5.p1); 4 dialysis samples, 3 paired with prior CKD biopsy, 1 unpaired (S2.6.p3)", "repeated_measure_unit": "patient (sample ID used as blocking variable for paired CKD/dialysis, S4.6.2.p2)", "planned_contrasts": ["CKD vs Control (S2.5.p1; paper: 967 DEGs, 464 up / 503 down, q < 0.05)", "Dialysis vs CKD pre-dialysis (S2.6.p3; paper: 0 DEGs, q < 0.05)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S4.6.2.p2"}, "paper_method": "edgeR TMM + limma-voom, CPM > 0.5 in >= 7 samples, patient as blocking variable, eBayes, BH q < 0.05 (S4.6.2.p2)", "exercise_content": "Exercise mentioned only as background (S2.3.p1, S3.p8 citing other studies); physical function tests (strength, endurance) are outcomes, not interventions."}

reasoning: Methods S4.6.2.p2 lists exactly two DE contrasts: CKD vs healthy controls and CKD pre- vs post-dialysis. Neither is an exercise contrast. The paper studies kidney disease and dialysis effects on muscle.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE157712\\GSE157712_Muscle_CKD_raw_counts.txt.gz", "owned": true, "checks": "S4.6.1.p1 names GSE157712; GEO samples are vastus lateralis Control 7 / CKD 7 / Dialysis 4, matching S2.5.p1 and S2.6.p3 (3 dialysis subjects 10,14,15 also have CKD samples; subject 13 unpaired).", "accession": "GSE157712", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE157712\\GSE157712_metadata.csv"}

reasoning: Accession cited in the paper's data availability; group sizes match exactly.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 18, "n_metadata": 18, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34784301\\GSE157712\\aligned\\aligned_metadata.csv", "columns": {"subject": {"alias_of": "characteristics_ch1.0.subject id"}, "grp": {"source": "title", "regex": "^(Control|CKD|Dialysis)_"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34784301\\GSE157712\\aligned\\design_metadata.csv", "sha256": "39e662bc313686af2455c60007e0a3e44f879c3cd4d25d24caa0d04fe030c6d9", "levels": {"subject": {"10": 2, "14": 2, "15": 2, "1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1, "8": 1, "9": 1, "11": 1, "12": 1, "13": 1}, "grp": {"Control": 7, "CKD": 7, "Dialysis": 4}}}}

reasoning: Matrix columns (C1, S15, ...) appear in brackets in the GEO title; inspect matched 18/18. Group taken from title prefix (equals characteristics group).

### matrix (valid, not_started)

final: {"source": "GEO data_processing: STAR + RSEM v1.3.0, 'raw counts (generated using RSEM)'", "paper_input": "raw counts, TMM + voom (S4.6.2.p2)", "matrix_type": "estimated counts", "recommended_method": "limma-voom", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34784301\\GSE157712\\aligned\\aligned_matrix.csv", "sha256": "0f14cb4217acfdcdc101127b5c76d24daebda49ade02601bbac6defe085bd4bb", "n_features": 58870, "n_samples": 18, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1401943.0, "median": 0.0, "integer_fraction": 0.9324, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Integer fraction 0.93 with non-integer values; data_processing states RSEM expected counts. Count-scale, consistent with the paper's voom route.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_contrast": null, "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34784301\\GSE157712\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: Request asks how exercise affects gene expression as the paper intends; the paper has no exercise comparison, so the case is refused at design.

rejected alternatives: [{"value": "grp CKD vs Control", "reason_rejected": "Disease-state comparison, not exercise; answering it would not address the requested exercise question."}, {"value": "grp Dialysis vs CKD (paired by subject)", "reason_rejected": "Treatment is dialysis initiation, not exercise."}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 18 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[]

## HANDBACK.md (start)

# HANDBACK — PMID34784301 / GSE157712

**Status: refused at `design`. There is no exercise contrast.**

## What ran
- `case_runner inspect GSE157712` (cached data): one matrix, `GSE157712_Muscle_CKD_raw_counts.txt.gz` (58,870 features × 18 samples, 93% integer values). Metadata has 18 samples: Control 7, CKD 7, Dialysis 4.
- `case_runner execute case_spec.json` recorded these gates: paper_reconstruction → ownership → alignment (exact on the bracketed title key, 18/18) → matrix (RSEM estimated counts, from data_processing) → design, which was **refused**. The suitability report ran and found 3 analyzable disease comparisons. The contract validator reported 0 errors. No DE was executed.

## Why refused
- The paper (S4.6.2.p2) plans two DE contrasts: CKD vs healthy controls, and CKD before vs after starting dialysis. Neither one involves exercise.
- Both groups were "highly sedentary" (S2.1.p1). Exercise appears only as background citing other studies (S2.3.p1, S3).
- Strength and endurance are measured outcomes, not interventions. No sample received an exercise intervention.
- The data cannot identify an exercise estimand. I rejected the CKD-vs-Control and Dialysis-vs-CKD comparisons as answers to the exercise question.

## DEG counts vs paper (paper threshold: BH q < 0.05, no fold-change cutoff; S4.6.2.p2)
- CKD vs Control: paper 967 (464 up / 503 down). Not run (out of scope).
- Dialysis vs CKD: paper 0. Not run (out of scope).
- Exercise contrasts: 0 in the paper and 0 here.

## Deviations
None. The case was stopped, so no later gates were recorded.

## Tool problems
- Inspect labels the matrix "linear_normalized or estimated_counts", even though GEO data_processing says RSEM counts. That is reasonable because the values are only 93% integers; I resolved it from the processing notes.
- No tool failures.

