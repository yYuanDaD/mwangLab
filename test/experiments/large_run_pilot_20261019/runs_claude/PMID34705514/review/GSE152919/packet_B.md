# Review packet B (the analysis' decisions): GSE152919

## Mechanical flags

- **unused_subject_like_column**: {"column": "source_name_ch1", "n_values": 4, "max_repeat": 5, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "title without the source_name_ch1 level", "across": "source_name_ch1", "pairs_or_sets": 6, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast exists. The series has two factors, genotype (SCN REV-ERB DKO vs control) and circadian time (CT4 vs CT16); every mouse was housed identically in constant darkness. No sample is exercised versus sedentary, and the paper's wheel running is a circadian activity readout given to all mice, not an intervention arm (S2.3.p1, FIG1, S4 methods). The requested estimand (effect of exercise on gene expression) is not identified by these data, and the paper itself never frames any transcriptomic comparison as an exercise effect; substituting the genotype or time contrast would manufacture an exercise result.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE152919"], "assay": "bulk RNA-seq (Illumina TruSeq Stranded Total RNA), SCN punches pooled 3-4 per biological replicate (FIG4, S4.14.p1)", "primary_estimand": "Effect of SCN-specific REV-ERBalpha/beta double knockout (SCN-DKO vs floxed control) on SCN gene expression, and the CT4-vs-CT16 circadian time difference within each genotype, in mice held 3 weeks in constant darkness (S2.3.p1). No exercise intervention is part of any RNA-seq experiment.", "factors": {"genotype": ["control", "SCN-DKO (REV-ERBs DKO)"], "time": ["CT4", "CT16"]}, "planned_contrasts": ["CT4 vs CT16 within control (S2.3.p1; paper: 807 DEGs)", "CT4 vs CT16 within SCN-DKO (S2.3.p1; paper: 406 DEGs)", "SCN-DKO vs control at CT4 (FIG4 E, S2.3.p2; paper: 286 DEGs, n=3 vs 3)", "SCN-DKO vs control at ZT4 (FIG4 D, S2.3.p2; paper: 56 DEGs, n=2 vs 2; LD-housed samples, not in this series)"], "sample_inclusion": "SCN of male control and SCN-DKO mice, 8-12 weeks, DD 3 weeks, harvested at CT4 or CT16 (S2.3.p1, S4 methods)", "repeated_measure_unit": "none; each replicate is a pool of 3-4 independent SCN punches from different animals (FIG4)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "expression_filter": "TPM > 0.1", "source_locator": "FIG4 B/D/E legend (FC > 1.5, FDR < 0.05, TPM > 0.1); S4.14.p1 (FDR < 0.05, > 0.1 TPM)"}, "paper_method": "STAR + featureCounts, TPM < 0.1 genes removed, DESeq2 (S4.14.p1)", "exercise_role": "Wheel ... [214 more characters]

reasoning: S2.3.p1 and S2.3.p2 define the only transcriptomic comparisons: time-of-day (CT4 vs CT16) within genotype and genotype (SCN-DKO vs control) at CT4/ZT4. S4.14.p1 gives DESeq2 with FDR < 0.05 and TPM > 0.1; the Fig. 4 legend adds FC > 1.5. The paper's only exercise-related element is home-cage wheel running, used as a circadian behavioural measurement in all mice.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE152919\\GSE152919_CT4_CT16_SCN_counts.txt.gz", "owned": true, "checks": ["GEO samples are SCN from C57BL/6 control vs REV-ERBS DKO mice at CT4/CT16, matching S2.3.p1", "CT4 group sizes 3 KO / 3 WT match FIG4 E (n = 3 vs 3)", "data_processing: STAR mm10 + featureCounts + DESeq2, matching S4.14.p1", "The paper markdown does not print the GEO accession; ownership rests on the sample-design match. The ZT4 (LD) samples of FIG4 D are not in this series."], "accession": "GSE152919", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE152919\\GSE152919_metadata.csv"}

reasoning: Design, tissue, genotype labels, time points, replicate numbers at CT4, and processing pipeline all match the paper's SCN RNA-seq; the series is the paper's CT4/CT16 dataset.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 15, "n_metadata": 15, "coverage": 1.0, "unmatched_matrix_columns": ["Start", "End", "Length"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34705514\\GSE152919\\aligned\\aligned_metadata.csv", "columns": {"geno": {"source": "title", "regex": "^CT\\d+_(KO|WT)\\d+$"}, "time": {"source": "title", "regex": "^(CT\\d+)_(?:KO|WT)\\d+$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34705514\\GSE152919\\aligned\\design_metadata.csv", "sha256": "f61d4dd9484e52dbfabd0a7ce377d35ef97371a96ead2c55358e9c561fc7ad74", "levels": {"geno": {"WT": 8, "KO": 7}, "time": {"CT16": 9, "CT4": 6}}}}

reasoning: inspect: title equals matrix column names for 15/15 samples (e.g. CT16_KO1). geno and time are parsed from the title; they agree with characteristics genotype and time point.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34705514\\GSE152919\\aligned\\aligned_matrix.csv", "sha256": "ca37a08478af004f700a918964d0073a811c2f02a7f6b7fb3190d991c144fdda", "n_features": 24419, "n_samples": 15, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 608230.0, "median": 204.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (integer_fraction 1.0, max 608230, median 204), featureCounts annotation columns (Chr/Start/End/Strand/Length) present, data_processing states featureCounts then DESeq2; this matches the paper's stated DESeq2 input. Note: some gene IDs are Excel-mangled dates (e.g. 4-Mar, 2-Sep), which would need repair before any gene-level reporting.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34705514\\GSE152919\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: The only paper-defined contrasts are genotype and circadian time. Wheel running appears only as a behavioural measurement of locomotor period. Refused at design per the skill rule that a sequenced sample set with no exercise arm is refused at design.

rejected alternatives: [{"value": "geno_KO_vs_WT (SCN-DKO vs control at CT4 or CT16)", "reason_rejected": "genetic knockout effect, not exercise"}, {"value": "time_CT4_vs_CT16 within genotype", "reason_rejected": "circadian time-of-day effect, not exercise"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "Requested estimand vs paper estimand",
    "paper": "Transcriptomic estimands are REV-ERB deletion and circadian time (S2.3.p1-p2)",
    "data": "GSE152919 factors: genotype x time point; no exercise variable",
    "disposition": "blocks_estimand"
  },
  {
    "item": "ZT4 samples",
    "paper": "FIG4 D: SCN-DKO vs control at ZT4 (n = 2 vs 2, 56 DEGs)",
    "data": "Not in GSE152919 (only CT4/CT16)",
    "disposition": "not_applicable_after_refusal"
  },
  {
    "item": "Gene identifiers",
    "paper": "gene symbols",
    "data": "Excel-mangled IDs in the count matrix (4-Mar, 2-Sep, ...)",
    "disposition": "not_applicable_after_refusal"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 34705514 / GSE152919

**Status: refused at `design`.** The data cannot answer "how exercise affects gene expression."

## What ran
- `python -m tools.case_runner inspect GSE152919` downloaded the series into `E:/agent/mwangLab_pdf/data/GSE152919`. It found one matrix, `GSE152919_CT4_CT16_SCN_counts.txt.gz`: 24,419 genes x 15 samples, all values integer, with featureCounts annotation columns.
- Wrote `case_spec.json` covering the gates `paper_reconstruction`, `ownership`, `alignment`, `matrix` and `design`. The `design` gate is `refused`.
- `python -m tools.case_runner execute case_spec.json` finished with status completed. The validator wrote 5 records with 0 errors, and the case route is `stopped:design`.
- Alignment matched exactly on `title` for 15/15 samples. Levels: geno WT 8 / KO 7; time CT16 9 / CT4 6.

## Why refused
- GSE152919 has two factors:
  - genotype: SCN-specific REV-ERBalpha/beta double knockout vs floxed control
  - circadian time: CT4 vs CT16, after 3 weeks in constant darkness
- There is no exercised vs sedentary arm. In this paper, wheel running only measures locomotor rhythm and free-running period, and every mouse had it (FIG1 C, FIG2 F, methods). It is not an intervention.
- The paper never presents any transcriptomic comparison as an effect of exercise (S2.3.p1-p2). Running the genotype or time contrast and calling it an exercise result would create an estimand the paper does not have.

## DEG counts vs paper
None were computed, because the case was refused. For reference, the paper's own comparisons and counts:

| Comparison | Paper DEGs | Notes |
|---|---|---|
| CT4 vs CT16, control | 807 | |
| CT4 vs CT16, DKO | 406 | |
| DKO vs control at CT4 | 286 | n = 3 vs 3 |
| DKO vs control at ZT4 | 56 | n = 2 vs 2; these samples are not in this series |

Paper threshold: DESeq2, FDR < 0.05, FC > 1.5 (|log2FC| > 0.5849625), TPM > 0.1. Sources: the FIG4 legend and S4.14.p1.

## Deviations
None. No analysis was run.

## Tool problems
- No tool failed.
- The count matrix contains Excel-mangled gene IDs, such as 4-Mar and 2-Sep. `inspect` correctly reports them under `excel_date_ids`. They would need repair before any gene-level reporting.
- The paper markdown (`PMC8550249.paper.md`) has no data-availability or GEO accession statement. Ownership therefore rests on matching the sample design (tissue, genotype, CT4/CT16, n = 3 vs 3 at CT4, STAR + featureCounts + DESeq2), and confidence is medium.
- With `planned: []` on a refu ... [267 more characters]
