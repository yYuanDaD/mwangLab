# Review packet B (the analysis' decisions): GSE294565

## Mechanical flags

- **unused_subject_like_column**: {"column": "grp", "n_values": 8, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "grp (without inj) + suffix of title", "across": "inj", "pairs_or_sets": 12, "samples_linked": 32, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast in the sequenced samples. GSE294565 holds only TA muscle after PBS or BaCl2 chemical injury (young/old, vehicle/BI01). The paper's exercise-like stimulus, 28-d synergist-ablation mechanical overload of plantaris (S2.6.p1, S4.3.p1), was not sequenced (FIG8-9 are histology/mass only). Injury-induced regeneration is not exercise, and BI01 vs vehicle is a drug effect, so no group comparison here answers how exercise affects gene expression.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE294565 (GEO lists PMID 37872294; paper DA.p1 names BioProject PRJNA1029003)"], "assay": "bulk mRNA-seq of tibialis anterior (TA), Novogene; plus NanoString GeoMx spatial RNA-seq (not in this GEO series)", "factors": {"age": ["Young (5-6 mo)", "Old (24-25 mo)"], "treatment": ["Vehicle (OV/YV)", "BI01 p53-MDM2 inhibitor (OS)"], "injury": ["PBS-injected control", "BaCl2 7 dpi", "BaCl2 35 dpi"]}, "primary_estimand": "Effect of BI01 (OS) vs vehicle (OV) on the TA transcriptome of old mice 7 and 35 days after BaCl2 injury (S2.5.p1, FIG6). The only exercise-like stimulus in the paper, 28-day mechanical overload of plantaris by synergist ablation (S2.6.p1, S4.3.p1, FIG8-9), was assessed by histology and muscle mass only; no RNA-seq was done on overloaded muscle.", "planned_contrasts": ["OS vs OV, 7 d post-BaCl2, n=4/group (S2.5.p1, FIG6a-b; paper: 'hundreds of genes', no count given)", "OS vs OV, 35 d post-BaCl2, n=4/group (S2.5.p1, FIG6d-e; no count given)"], "sample_inclusion": "32 TA libraries: YV/OV PBS, YV/OV/OS 7 dpi and 35 dpi (no OS PBS libraries deposited)", "repeated_measure_unit": "PBS and BaCl2 were injected unilaterally (ABS.p1), but the library names give no animal ID, so contralateral pairing is not recorded", "paper_method": "Partek Flow: STAR to GRCm39, Partek E/M (Ensembl 103), min 10 counts filter, DESeq2 (S4.11.p1)", "paper_threshold": {"metric": "not_stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "S4.1 ... [145 more characters]

reasoning: S2.5.p1 and S4.11.p1 describe the only bulk RNA-seq: TA after BaCl2 injury, OV vs OS at 7 and 35 d (with YV reference). Mechanical overload (S2.6.p1, S4.3.p1) is the resistance-exercise model, but FIG8-9 report only muscle mass, fiber CSA and senescence staining; S4.11/S4.12 list no sequencing of plantaris. The paper's estimand for the deposited data is a drug effect after chemical injury, not exercise.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37872294\\GSE294565_counts_gsm.csv", "owned": true, "checks": ["GEO series lists Series_pubmed_id 37872294 (and 40259517) and reuses the paper's title and abstract", "Series design (young/old TA, PBS vs BaCl2 7/35 dpi, BI01 cohort) matches S2.5.p1 and FIG6 (n=4/group)", "Paper DA.p1 names BioProject PRJNA1029003 while the GEO series links PRJNA1250510 (recorded as a discrepancy; GEO was released Apr 2025, after the paper)", "GEO data_processing says HISAT2/mm10 while the paper says STAR/GRCm39 Partek E/M (recorded as a discrepancy)"], "accession": "GSE294565", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE294565\\GSE294565_metadata.csv"}

reasoning: The PMID link, title, abstract and exact group structure tie GSE294565 to this paper; the BioProject and aligner differences do not change which samples these are.

### alignment (valid, not_started)

final: {"prep": "prep_rename_columns.py renamed matrix lab codes to GSM ids; group codes map exactly (YV35dPBS->Young Vehicle PBS, OS27dBa->Old Senolytic 7 DPI, ...); within-group replicate pairing is ordinal and assumed (matrix replicate numbers 6-9/4-7/7-10 do not match GEO 1-4). Map: GSE294565_column_map.csv", "method": "exact:metadata_index", "n_aligned": 32, "n_metadata": 32, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37872294\\GSE294565\\aligned\\aligned_metadata.csv", "columns": {"age": {"source": "description", "regex": "^Library name: (Young|Old) ", "recode": {"Young": "Y", "Old": "O"}}, "trt": {"source": "description", "regex": "^Library name: (?:Young|Old) (Vehicle|Senolytic) ", "recode": {"Vehicle": "V", "Senolytic": "S"}}, "inj": {"source": "description", "regex": "^Library name: (?:Young|Old) (?:Vehicle|Senolytic) (PBS|7 DPI|35 DPI) - \\d+$", "recode": {"PBS": "PBS", "7 DPI": "D7", "35 DPI": "D35"}}, "grp": {"combine": ["age", "trt", "inj"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37872294\\GSE294565\\aligned\\design_metadata.csv", "sha256": "ba99b234b6bb9fa6c31f4042e9b3edab290f7f1e18f29fe8ac4552eed902a3d7", "levels": {"age": {"O": 20, "Y": 12}, "trt": {"V": 24, "S": 8}, "inj": {"D7": 12, "D35": 12, "PBS": 8}, "grp": {"Y_V_PBS": 4, "Y_V_D7 ... [90 more characters]

reasoning: Matrix columns are lab codes with replicate numbers that differ from GEO; no shared per-sample key exists. The group part of every code is unambiguous, so group labels are exact; which animal within a group is which is assumed ordinal. This would matter only for per-sample covariates or pairing, and the case stops at design before any model.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37872294\\GSE294565\\aligned\\aligned_matrix.csv", "sha256": "7ae4ae684b1d716daa12261734096211079e147879e17e487b60964a5ffef00e", "n_features": 54532, "n_samples": 32, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2420634.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Integer fraction 1.0, max 2.4e6, GEO data_processing 'tab-delimited count matrix' after HISAT2; paper used DESeq2 on Partek E/M counts (S4.11.p1).

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37872294\\GSE294565\\suitability\\suitability.md", "n_comparisons": 7, "n_analyzable": 7}}

reasoning: Request asks for an exercise effect. The data identify injury, age and drug effects only; the paper never sequenced the overload model. Refused at design after recording paper, ownership, alignment and matrix.

rejected alternatives: [{"value": "grp O_S_D7 vs O_V_D7 and O_S_D35 vs O_V_D35 (paper's BI01 contrasts)", "reason_rejected": "drug effect after chemical injury, not an exercise effect"}, {"value": "BaCl2 7/35 dpi vs PBS (injury/regeneration)", "reason_rejected": "chemical myotoxic injury is not exercise or overload"}, {"value": "Old vs Young", "reason_rejected": "age effect, no exercise stimulus"}, {"value": "mechanical overload (MOV) vs sham", "reason_rejected": "no MOV or sham plantaris libraries in GSE294565 or any ... [28 more characters]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 32 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "BioProject",
    "paper": "PRJNA1029003 (DA.p1)",
    "data": "GEO GSE294565 links PRJNA1250510",
    "disposition": "recorded; ownership kept via PMID link and design match"
  },
  {
    "item": "Processing",
    "paper": "STAR v2.7.8a to GRCm39, Partek E/M Ensembl 103 (S4.11.p1)",
    "data": "GEO data_processing: HISAT2 to mm10",
    "disposition": "recorded; not consequential because the case stops at design"
  },
  {
    "item": "Exercise data",
    "paper": "mechanical overload experiment (S2.6.p1) with histology only",
    "data": "no overload/sham libraries",
    "disposition": "blocks the requested exercise estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID37872294 / GSE294565

**Outcome: refused at `design`.** No exercise comparison is possible with these data.

## What ran
- `tools.case_runner inspect GSE294565` (data were already cached under `E:/agent/mwangLab_pdf/data/GSE294565`).
- `prep_rename_columns.py`: renames the matrix's lab-code columns to GSM ids. Output files: `GSE294565_counts_gsm.csv` and `GSE294565_column_map.csv`.
- `tools.case_runner execute case_spec.json`. Five gate records were written (paper_reconstruction, ownership, alignment, matrix, design). The validator reported 0 errors. Status: `stopped:design`, `refused`.

## Why refused
- The bulk RNA-seq in the paper covers only tibialis anterior after PBS or BaCl2 chemical injury, at 7 and 35 dpi. Groups: YV, OV, OS (BI01, a p53-MDM2 inhibitor). Sources: S2.5.p1, S4.11.p1, FIG6.
- The paper's only exercise-like model is 28-day mechanical overload of the plantaris by synergist ablation (S2.6.p1, S4.3.p1). It was measured by muscle mass, fibre CSA and senescence staining only (FIG8-9). It was never sequenced, and GSE294565 has no overload or sham libraries.
- Rejected alternatives:
  - BI01 vs vehicle is a drug effect.
  - BaCl2 vs PBS is injury and regeneration, not exercise.
  - Old vs young is an age effect.

## DEG counts vs paper
- Not run, because no exercise contrast exists.
- The paper itself gives no DEG counts ("hundreds of genes" for OS vs OV at 7 d and 35 d) and no DEG threshold. Its method is DESeq2 in Partek Flow with a minimum 10-count filter (S4.11.p1).

## Deviations and discrepancies (recorded in the spec)
- **BioProject:** the paper (DA.p1) gives PRJNA1029003, but the GEO series links PRJNA1250510. Ownership was kept because GEO lists PMID 37872294, reuses the paper's title and abstract, and has the same group structure (n=4 per group).
- **Processing:** the paper used STAR to GRCm39 with Partek E/M. GEO `data_processing` says HISAT2 to mm10.
- **Alignment:**
  - The matrix columns' replicate numbers (for example OV35dPBS_6-9, OV7dBa_7-10) do not match the GEO library replicates 1-4. Group codes map exactly.
  - Within each group, replicates were paired in ascending order. This pairing is an assumption, and it is documented per column in `GSE294565_column_map.csv`.
  - It does not affect group labels, and the case stopped before any model was fitted.
- No OS PBS-control libraries were deposited (8 groups x 4 = 32 samples).

## Tool problems
- `tools/native.py:230-231`: `_ANNOTATION_NAMES` includes `chr` bu ... [543 more characters]
