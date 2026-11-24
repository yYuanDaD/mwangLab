# Review packet B (the analysis' decisions): GSE159217

## Mechanical flags

- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"extract_protocol_ch1": ["Subjects were fasted and refrained from exercise and alcohol 24 hours prior to testing. Biopsies from vastus lateralis were collected using the suction modified Bergstr枚m technique from the non-dominant leg under local anaesthesia using a using a 5-mm Bergstr枚m o needle. Collected tissue was snap frozen in liquid nitrogen and stored at -80掳C until further analysis. Total RNA was extracted by grinding frozen muscle tissue and dissolving ap ... [892 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast identifiable. The only grouping factor is age (Young/Older), and the paper matched the groups on physical activity (S2.2.p1, S1.p3), so Older vs Young estimates ageing, not exercise. The paper's physical-activity analysis (expression vs continuous MVPA, S3.4.p4) needs per-subject accelerometry MVPA, which GSE159217 metadata does not contain (only title, sex, tissue, age group); it is not in the paper's supplement either. An exercise effect therefore cannot be estimated from the deposited data.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE159217"], "primary_estimand": "Cross-sectional age effect: older (65-71 y, n=18) vs young (19-27 y, n=20) male vastus lateralis, groups deliberately MATCHED for physical activity (ABS.p2, S1.p3, S2.2.p1). No exercise intervention, no acute bout, no active-vs-sedentary arm.", "planned_contrasts": ["Older vs Young, DESeq2 (S2.5.p2; paper: 4327 DEGs, 3797 coding: 1891 up / 1906 down in older; S3.1.p1) - age contrast, not exercise", "Within-group association of expression with continuous MVPA time, limma-voom (S2.5.p2, S3.4.p4; paper: 662 genes older, 1058 young at unadjusted P<0.05) - the only physical-activity analysis; needs per-subject MVPA"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S2.5.p2"}, "paper_method": "DESeq2 ~ age group after removing genes with <10 reads per row; limma-voom (TMM) with MVPA as continuous covariate within each age group", "factors": {"age group": ["Young", "Older"]}, "sample_inclusion": "38 males with high-quality RNA; two older subjects excluded before deposition (S2.2.p1)", "repeated_measure_unit": "none (one biopsy per subject)"}

reasoning: Paper design is an age comparison under matched physical activity (S1.p3, S2.2.p1, S4.p1). Its only physical-activity analysis is a correlation with accelerometry-measured MVPA within each age group (S3.4.p4, FIG5F, Figure S3A) at raw P<0.05.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34219410\\GSE159217\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["S2.9.p1 names GSE159217", "38 samples = 20 Young + 18 Older matches Table 1", "all male vastus lateralis, BGISEQ-500, STAR+HTSeq matches S2.5.p1"], "accession": "GSE159217", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE159217\\GSE159217_metadata.csv"}

reasoning: Data availability statement and sample counts match.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 38, "n_metadata": 38, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34219410\\GSE159217\\aligned\\aligned_metadata.csv", "columns": {"age": {"alias_of": "characteristics_ch1.2.age group"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34219410\\GSE159217\\aligned\\design_metadata.csv", "sha256": "652708b63565c342e8e9b669b247ab9318fd389155311d60e23d6a8e09df45c3", "levels": {"age": {"Young": 20, "Older": 18}}}}

reasoning: Runner renames merged-tar columns to GSM ids; exact match on metadata index exactly. age alias from 'age group' characteristic.

### matrix (valid, not_started)

final: {"source": "GSE159217_RAW.tar per-sample HTSeq count files merged", "paper_input": "HTSeq counts (S2.5.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34219410\\GSE159217\\aligned\\aligned_matrix.csv", "sha256": "ea9066063fbc0cbf31cdbbcde1d4c5ece28f73e4596e2ebd31e03b91cf15eeb3", "n_features": 60676, "n_samples": 38, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2063459.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max ~2.06M, Ensembl IDs; data_processing: STAR + HTSeq; matches paper input.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": null, "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34219410\\GSE159217\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Request asks for the exercise effect as the paper intends; the paper intends no exercise contrast and its activity association cannot be reconstructed.

rejected alternatives: [{"value": "age_Older_vs_Young (associational, DESeq2)", "reason_rejected": "Executable, but it is an ageing estimand with activity held equal by design; running it would not answer how exercise affects gene expression."}, {"value": "expression ~ MVPA within each age group (limma-voom)", "reason_rejected": "MVPA per subject not deposited in GEO metadata or the paper; covariate unavailable."}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 38 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "MVPA covariate",
    "paper": "per-subject accelerometry MVPA used in limma-voom association (S2.5.p2, S3.4.p4)",
    "data": "absent from GEO metadata",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID34219410 / GSE159217

**Status: refused at the `design` gate.** The contract validator passed (5 records, 0 errors).

## What ran
- `case_runner inspect GSE159217`: the `_RAW.tar` was merged into a 60,676 Ensembl genes × 38 samples matrix. Every value is an integer (STAR + HTSeq raw counts). The only grouping column is `age group` (Young 20 / Older 18). The matrix has 38 samples, all male vastus lateralis.
- `case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership (owned), alignment (exact on the metadata index, 38/38), matrix (raw counts → DESeq2), design (**refused**). No DE executions and no enrichment were run.

## Why refused
- The paper compares older and young men and **matched the two groups for physical activity** (S1.p3, S2.2.p1, S4.p1). There is no exercise intervention, acute bout or active-vs-sedentary arm. Older vs Young is an ageing estimand, not an exercise effect.
- The paper's only physical-activity analysis correlates expression with continuous MVPA time within each age group (limma-voom, raw P < 0.05; S2.5.p2, S3.4.p4). It needs per-subject accelerometry MVPA, which is not in the GEO metadata (only title, sex, tissue and age group) or in the paper.
- The Older vs Young DESeq2 comparison could run (suitability: analyzable), but I rejected it as an answer to the exercise question. It is listed as a rejected candidate in the design gate.

## DEG counts vs paper
- Paper threshold: BH FDR < 0.05, no fold-change cutoff, genes with < 10 reads per row removed (S2.5.p2).
- Paper results:
  - Older vs Young: 4327 DEGs, of which 3797 are coding (1891 up / 1906 down in older).
  - MVPA association: 662 genes (older group) and 1058 genes (young group) at unadjusted P < 0.05.
- Ours: not run (refused), so there is no comparison.

## Deviations
None. The case stopped before the method gate.

## Tool problems
- **Merged-tar column naming is inconsistent between commands.** `inspect` reports the merged-tar sample columns as `GSM4823186_1_counts`, and the runner's `raw_tar` path silently renames them to bare GSM ids (`tools/case_runner.py:715`). A `matrix_column_pattern` written from inspect's output therefore matches 0 columns and the case fails (`tools/case_runner.py:561-562`). The case spec docs do not mention the rename. It cost one rerun.
- There is no other problem.

