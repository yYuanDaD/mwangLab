# Review packet B (the analysis' decisions): GSE228901

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.9.sum of_positive_frailty_criteria", "n_values": 5, "max_repeat": 5, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"extract_protocol_ch1": ["Total RNA was isolated using miRNeasy庐 Mini Kit (Qiagen) according to the manufacturer's protocol. Briefly, 50-60 mg of crushed frozen liver from female mice were homogenized in QIAzol lysis reagent (RNeasy Plus Mini Kit, Qiagen) and then transferred to a RNeasy庐 Mini column to be further processed with a genomic DNA elimination step by following the manufacturer鈥檚 RNA isolation protocol. Total isolated RNA was tested to fit high quality  ... [577 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the three arms (Adult vehicle, Old vehicle, Old PDX) differ by age and drug only. Treadmill distance and voluntary wheel km/d in the metadata are per-animal fitness test readouts, not an assigned exercise exposure; regressing expression on them would be an associational fitness analysis the paper never planned. The paper's own contrasts (aging, PDX) do not answer how exercise affects gene expression.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE228901"], "assay": "bulk polyA RNA-seq, female mouse liver (S2.8.p1, S2.9.p1)", "sample_inclusion": "15 female livers, 5 per group: Adult (6 mo, vehicle), Old (22 mo, vehicle), PDX (22 mo, Protectin DX gavage 9 wk) (S3.7.p1)", "factors": {"group": ["Adult", "Old", "PDX"]}, "primary_estimand": "Effect of aging (Old vs Adult) and of Protectin DX treatment (PDX vs Old) on liver gene expression. The study has no exercise intervention: treadmill exhaustion and voluntary wheel running are physical-performance assessments given to every mouse in every group (S2.2.p1, S2.4.p1, S2.4.p7, S2.4.p9).", "planned_contrasts": ["Old vs Adult (aging; S3.7.p2: 1,621 genes at FDR q < 0.05)", "PDX vs Old (drug; S3.7.p2: 0 genes at FDR q < 0.25)"], "exercise_contrast_in_paper": "none", "repeated_measure_unit": "none (one liver per animal)", "paper_method": "DESeq2 Wald test, pairwise groups, BH FDR; featureCounts Ensembl gene counts (S2.9.p1-p2)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.7.p2"}, "paper_results": "Old vs Adult 1,621 DEGs FDR<0.05; PDX vs Old 0 DEGs FDR<0.25; Hallmark GSEA (S3.7.p3)"}

reasoning: The paper is a pharmacological (PDX) and aging study. Exercise appears only as endpoint fitness tests (treadmill to exhaustion, 4-day voluntary wheel in activity cages) applied to all groups at baseline and endpoint (S2.4.p1-p9); no group was trained or kept sedentary. The words exercise/training do not occur in the article.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE228901\\GSE228901_counts.txt.gz", "owned": true, "checks": ["S2.9.p3 names GSE228901", "15 samples A1-A5/O1-O5/P1-P5 = paper's 5/group female liver", "data_processing matches S2.9.p1 (STAR, featureCounts, Ensembl 100)"], "accession": "GSE228901", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE228901\\GSE228901_metadata.csv"}

reasoning: Paper S2.9.p3 deposits GSE228901; GEO metadata (liver, female cohort, vehicle/PDX, 6 vs 22 months) matches S3.7.p1.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 15, "n_metadata": 15, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37059838\\GSE228901\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^([AOP])\\d+$", "recode": {"A": "Adult", "O": "Old", "P": "PDX"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37059838\\GSE228901\\aligned\\design_metadata.csv", "sha256": "72df1c1710c30a5242ba50ae43f40751beb7ad55b1e77cf097ac222916c31ddd", "levels": {"grp": {"Adult": 5, "Old": 5, "PDX": 5}}}}

reasoning: Matrix columns A1..P5 equal the metadata title column (inspect alignment_keys: 15/15). Group letter from title agrees with the age and treatment characteristics.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37059838\\GSE228901\\aligned\\aligned_matrix.csv", "sha256": "346352e89bfba8dea1b378606d4b44d0cdcc19a0444bb599d3fcb112d0b6e9f4", "n_features": 55450, "n_samples": 15, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 4241143.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 4.2e6; data_processing and S2.9.p1 state featureCounts gene-level counts. The VST file is a derived log-scale matrix and is not used.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_contrast": null, "available_contrasts": ["grp_Old_vs_Adult (aging)", "grp_PDX_vs_Old (drug)"], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37059838\\GSE228901\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: Paper S2.2.p1/S2.4 define treadmill and wheel as physical performance assessments in every group; there is no exercised vs sedentary arm. Refused at design.

rejected alternatives: [{"value": "grp_Old_vs_Adult", "reason_rejected": "aging estimand, not exercise"}, {"value": "grp_PDX_vs_Old", "reason_rejected": "drug estimand, not exercise"}, {"value": "regression on treadmill distance or voluntary wheel km/d", "reason_rejected": "fitness test outcome measured in all animals, confounded with age (Adult 67-101 m vs Old 34-79 m); not an exercise intervention and not planned by the paper"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "Requested estimand (exercise effect) vs study design",
    "paper": "Aging and Protectin DX study; exercise only as fitness testing in all groups (S2.4)",
    "data": "GEO groups: age (6 vs 22 months) and treatment (vehicle vs PDX); treadmill/wheel are continuous per-animal readouts",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID37059838 / GSE228901

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE228901`: the data were already cached. There are 15 female liver samples (A1-A5 Adult 6 mo vehicle, O1-O5 Old 22 mo vehicle, P1-P5 Old PDX). The matrix `GSE228901_counts.txt.gz` holds integer featureCounts counts, 55,450 Ensembl genes. There is also a derived VST file, which was not used.
- `python -m tools.case_runner execute case_spec.json` recorded these gates in order:
  - `paper_reconstruction`
  - `ownership`: owned (S2.9.p3 names GSE228901)
  - `alignment`: exact match on `title`, 15/15 samples
  - `matrix`: raw counts
  - `design`: refused
- The validator returned 0 errors. Suitability ran on the 3 groups and called it "analyzable", but the design was refused on the estimand, not on the data.
- No DE executions and no enrichment were run.

## Why refused
The paper is about aging and Protectin DX. Its arms are Adult vehicle, Old vehicle and Old PDX gavage for 9 weeks. Treadmill exhaustion and the 4-day voluntary wheel test are fitness assessments given to every animal in every group (S2.2.p1, S2.4.p1-p9). No group was exercise-trained or kept sedentary, and the words "exercise" and "training" never appear in the article.

The metadata columns for treadmill distance and wheel km/d are per-animal outcome readouts, and they are confounded with age. The paper's planned contrasts are Old vs Adult (aging) and PDX vs Old (drug). Neither one estimates an exercise effect.

## DEG counts vs the paper (paper threshold: FDR q < 0.05, no fold-change cutoff, S3.7.p2)
- Old vs Adult: paper reports 1,621 DEGs. Not run (not an exercise contrast).
- PDX vs Old: paper reports 0 genes at FDR < 0.25. Not run.
- No exercise contrast exists, so 0/0 contrasts were run.

## Deviations
None. The case was stopped before the method gate.

## Tool problems
None blocking. One minor point: the `treatment_protocol_ch1` and `growth_protocol_ch1` strings show mojibake (for example `渭L`, `庐`) in inspect's output. This is a UTF-8 file being decoded as GBK when the metadata CSV is read or written. It is cosmetic and did not affect any decision.

