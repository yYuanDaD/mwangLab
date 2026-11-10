# Review packet B (the analysis' decisions): GSE304351

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "grp", "pairs_or_sets": 4, "samples_linked": 8, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the deposited samples differ only by MSC vs PBS injection in D-gal mice. Treadmill running was an outcome test given to all mice (S2.4.p1), not a factor, so the exercise estimand the request asks for is not identifiable.

## Samples per design level

### `grp`
- **MSC** (4): GSM9148486 / the quadriceps of D-gal+MSCs mice 1 / Library name: MSC1; GSM9148487 / the quadriceps of D-gal+MSCs mice 2 / Library name: MSC2; GSM9148488 / the quadriceps of D-gal+MSCs mice 3 / Library name: MSC3; GSM9148489 / the quadriceps of D-gal+MSCs mice 4 / Library name: MSC4
- **PBS** (4): GSM9148482 / the quadriceps of D-gal+PBS mice 1 / Library name: PBS1; GSM9148483 / the quadriceps of D-gal+PBS mice 2 / Library name: PBS2; GSM9148484 / the quadriceps of D-gal+PBS mice 3 / Library name: PBS3; GSM9148485 / the quadriceps of D-gal+PBS mice 4 / Library name: PBS4

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE304351"], "assay": "bulk RNA-seq (Illumina NovaSeq X Plus), mouse quadriceps", "factors": {"injection": ["D-gal+PBS", "D-gal+MSCs"]}, "sample_inclusion": "QUAD muscle of D-gal-treated male C57BL/6J mice injected with PBS or MSCs, n = 4 per arm (S3.2.p1, FIG2 legend, Figure S3 legend)", "primary_estimand": "Effect of intramuscular MSC injection vs PBS on quadriceps gene expression in D-galactose-induced muscle atrophy (S3.2.p1). Not an exercise effect: treadmill running is only an outcome test given to all mice (S2.4.p1).", "planned_contrasts": ["D-gal+MSCs vs D-gal+PBS, QUAD (S3.2.p1; paper: 960 DEGs, 525 up / 435 down)", "NAD+-MSCs vs MSCs, cultured human MSCs (S3.5.p1, FIG5; not deposited in GSE304351)"], "repeated_measure_unit": "none (independent mice)", "paper_method": "DESeq2 v1.26.0 (S2.7.p1)", "paper_threshold": {"metric": "not_stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.7.p1 (DESeq2 named, DEG cutoff not given); S2.16.p1 p < 0.05 refers to GraphPad tests"}, "paper_results": {"QUAD MSC vs PBS": "960 DEGs (525 up, 435 down); up enriched in fatty-acid degradation, OXPHOS, PPAR"}, "exercise_role": "Exhaustive treadmill run (S2.4.p1) used once as a performance readout one week after the last injection, in every group; no exercise intervention or exercise-vs-sedentary arm"}

reasoning: Title, abstract (ABS.p2-p3) and methods (S2.3.p1, S2.4.p1, S2.7.p1) describe D-gal-induced atrophy treated with MSCs/NAD+-MSCs. The only exercise element is a treadmill endurance test applied to all mice as an outcome measure. RNA-seq of muscle compares D-gal+MSCs with D-gal+PBS (S3.2.p1). DA.p1 names GSE304351 as the RNA-seq deposit.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41383117\\GSE304351_counts_renamed.csv", "owned": true, "checks": ["DA.p1 names GSE304351", "8 GSM titles 'the quadriceps of D-gal+PBS/MSCs mice 1-4' match S3.2.p1 and n = 4 in the FIG2/Figure S3 legends", "matrix columns PBS1-4/MSC1-4 equal GEO Library names", "the MSC +/- NAD+ RNA-seq (FIG5A) is not in this series"], "accession": "GSE304351", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE304351\\GSE304351_metadata.csv"}

reasoning: Series, sample titles and group sizes match the paper's quadriceps RNA-seq; organism Mus musculus matches.

### alignment (valid, not_started)

final: {"method": "exact:libname", "n_aligned": 8, "n_metadata": 8, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41383117\\GSE304351\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "D-gal[+](PBS|MSCs) mice", "recode": {"PBS": "PBS", "MSCs": "MSC"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41383117\\GSE304351\\aligned\\design_metadata.csv", "sha256": "2a43e7dd92592809ae9b3e5001b5422adcf0eaa23c63774fe8c6aac6ba9fc451", "levels": {"grp": {"PBS": 4, "MSC": 4}}}}

reasoning: Deposited matrix columns are '<Library name>_Count'; prep_strip_count_suffix.py drops only the suffix (values unchanged). Key derived from description 'Library name: PBS1'. Group from title.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "source": "GEO data_processing: Hisat2 to GRCm39; 'xlsx file including raw counts for each sample'", "paper_input": "DESeq2 on read counts (S2.7.p1)", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41383117\\GSE304351\\aligned\\aligned_matrix.csv", "sha256": "8147106abce199e33ac0ffcb3c71f5ac5f3094f83bc5f6f56622bf6117a6be51", "n_features": 12171, "n_samples": 8, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 4541514.0, "median": 552.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integers (integer_fraction 1.0), 0 to 4.5e6, column suffix _Count, data_processing states raw counts. 12171 genes (submitter-filtered list).

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "grp", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41383117\\GSE304351\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Request is how exercise affects gene expression. Paper (S2.3.p1, S2.4.p1, S3.2.p1) has no exercise intervention; the single RNA-seq factor is MSC vs PBS injection. Refused at design.

rejected alternatives: [{"value": "grp MSC vs PBS (paper's 960-DEG contrast)", "reason_rejected": "Valid paper contrast but it estimates a cell-therapy effect, not an exercise effect; outside the requested exercise estimand"}, {"value": "exercise vs sedentary", "reason_rejected": "No such factor: every mouse did the same exhaustive treadmill test and no sedentary/untested arm was sequenced"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 8 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "MSC +/- NAD+ RNA-seq",
    "paper": "FIG5A volcano, n = 3 per arm",
    "data": "not deposited in GSE304351 (8 quadriceps samples only)",
    "disposition": "not_executable"
  },
  {
    "item": "DEG threshold",
    "paper": "not stated for the 960 DEGs",
    "data": "n/a",
    "disposition": "recorded"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID41383117 / GSE304351

**Status: refused at `design`** (no exercise contrast). The decision contract validator passed: 5 records, 0 errors.

## What ran
- `case_runner inspect GSE304351` downloaded the series to `E:/agent/mwangLab_pdf/data/GSE304351`. It holds 8 quadriceps samples (D-gal+PBS 1-4, D-gal+MSCs 1-4) and one integer count matrix of 12171 genes x 8 samples (`*_PBS1..._vs_MSC1....all.csv`).
- `prep_strip_count_suffix.py` removes the `_Count` suffix from the matrix columns so they equal the GEO Library names. Values are unchanged. Output: `GSE304351_counts_renamed.csv`.
- `case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership, alignment (exact on Library name, 8/8 matched), matrix (raw counts; data_processing says "raw counts"), and design, which was **refused**. Suitability had found the MSC-vs-PBS contrast analyzable, but that contrast is not an exercise contrast.

## Why refused
- The paper studies D-galactose-induced muscle atrophy treated with intramuscular MSCs or NAD+-MSCs (S2.3.p1).
- Exercise appears only as an exhaustive treadmill endurance test (S2.4.p1). Every mouse took it as an outcome readout, so exercise is not a factor.
- The only RNA-seq contrast deposited is D-gal+MSCs vs D-gal+PBS in quadriceps (S3.2.p1). It estimates a cell-therapy effect.
- No exercise-vs-sedentary estimand can be identified from these samples.

## DEG counts vs paper
- No differential expression was run (refused).
- Paper: MSC vs PBS in quadriceps, 960 DEGs (525 up / 435 down) with DESeq2 v1.26.0. The paper does not state the DEG threshold (S2.7.p1). The p < 0.05 in S2.16.p1 refers to the GraphPad tests.
- The paper's second RNA-seq set (cultured MSCs with or without NAD+, FIG5A, n = 3) is not deposited in GSE304351.

## Deviations
- None in the analysis, because nothing was executed.
- The only preparation step was renaming the matrix columns (suffix strip, documented in `prep_scripts`).

## Tool problems
- `tools/case_runner.py:294` (`_contained_keys`): inspect reported `alignment_keys: []`. The matrix column names (`PBS1_Count`) are longer than the metadata token (`Library name: PBS1`), so the containment check in this direction never matches. A suffix-strip prep script was needed. Suggestion: also test the reverse containment, or strip a common suffix such as `_Count` or `_count`.
- Environment issue, not a repository tool: in this session's Bash tool, heredoc text containing `\\` reached the file as `\` ... [121 more characters]
