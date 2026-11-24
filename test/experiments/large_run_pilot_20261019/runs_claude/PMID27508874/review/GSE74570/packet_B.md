# Review packet B (the analysis' decisions): GSE74570

## Mechanical flags

- **unused_subject_like_column**: {"column": "grp", "n_values": 6, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"treatment_protocol_ch1": ["Mice were occassionally subjected to glucose and exercise tolerance tests before sacrifice."]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast exists in GSE74570: the sequenced groups differ only by Nampt genotype (WT/KO/OE) and age (4/7/24 months). Exercise was a phenotypic test applied to all mice (treatment_protocol_ch1), not a sequenced factor, so the requested estimand (effect of exercise on gene expression) is not identifiable. Running genotype or age contrasts and calling them exercise effects would misrepresent the study.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE74570"], "assay": "bulk polyA RNA-seq, quadriceps muscle, mouse (C57BL/6), HTSeq gene counts (GEO data_processing)", "primary_estimand": "Transcriptome effect of skeletal-muscle Nampt genotype (knockout or overexpression) and of age on quadriceps gene expression. Exercise is used only as a phenotypic readout (treadmill tolerance tests, S2.1.p3, S2.2.p2, S2.4.p1), never as an intervention whose transcriptional effect is measured.", "factors": {"genotype": ["WT", "mNKO (Mlc1f-Cre Nampt fl/fl)", "mNTG (MCK-Nampt overexpression)"], "age": ["4 months", "7 months", "24 months"]}, "planned_contrasts": ["mNKO vs WT at 7 months (S2.2.p3; paper: 33% of detectable genes significant, Table S1)", "mNTG vs WT at 24 months (S2.4.p1; paper: 18 genes, Table S2, FIG7 F)", "WT 24m vs WT 4m and mNTG 24m vs mNTG 4m age effects (S2.4.p1; 87 overlapping genes, FIG7 G-H)", "mNTG vs WT at 4 months (GEO supplementary DESeq table only)"], "exercise_arm": "none: no RNA-seq sample is labelled exercised/trained vs sedentary; treatment_protocol_ch1 says mice were only 'occasionally subjected to glucose and exercise tolerance tests before sacrifice' (applies to all groups alike)", "inclusion": "23 GSM samples: WT 7m (4), mNKO 7m (4), WT 4m (4), mNTG 4m (3), WT 24m (4), mNTG 24m (4)", "paper_method": "DESeq2 (GEO data_processing; RNA-seq statistics in Supplemental Information, not available here)", "paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": null, "effect_cutoff ... [299 more characters]

reasoning: Paper (S2.2.p3, S2.4.p1, S4.6.p1, FIG3, FIG7) sequenced quadriceps to study Nampt knockout, Nampt overexpression and aging. Treadmill exercise appears only as a functional endpoint (FIG1J, FIG2G, FIG4A, FIG5A-D, FIG7D). No sequenced group differs by exercise exposure.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID27508874\\GSE74570\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["S4.6.p1 names GSE74570", "GEO source quadriceps muscle, Mus musculus, genotypes and ages match FIG3/FIG7 groups", "RAW.tar holds 23 per-sample HTSeq gencode count files named by GSM"], "accession": "GSE74570", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE74570\\GSE74570_metadata.csv"}

reasoning: Accession named in paper methods; sample groups match the paper's RNA-seq groups.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 23, "n_metadata": 23, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID27508874\\GSE74570\\aligned\\aligned_metadata.csv", "columns": {"geno": {"source": "title", "regex": "^(WT|mNamptKO|MCK-NamptOE)_", "recode": {"WT": "WT", "mNamptKO": "KO", "MCK-NamptOE": "OE"}}, "age": {"source": "characteristics_ch1.2.age", "regex": "^([0-9]+) months$", "recode": {"4": "m4", "7": "m7", "24": "m24"}}, "grp": {"combine": ["geno", "age"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID27508874\\GSE74570\\aligned\\design_metadata.csv", "sha256": "7116cffb983ee71d5feb0c2b909a2985dc8cdaaefa4864e6cb98ef4aa11feaf7", "levels": {"geno": {"WT": 12, "OE": 7, "KO": 4}, "age": {"m7": 8, "m24": 8, "m4": 7}, "grp": {"WT_m7": 4, "KO_m7": 4, "WT_m4": 4, "WT_m24": 4, "OE_m24": 4, "OE_m4": 3}}}}

reasoning: Tar columns are GSM ids, matching the metadata index exactly. Genotype from title prefix, age from the age characteristic.

### matrix (valid, not_started)

final: {"source": "GSE74570_RAW.tar per-sample HTSeq counts (merged)", "paper_input": "HTSeq counts analysed with DESeq2 (GEO data_processing)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID27508874\\GSE74570\\aligned\\aligned_matrix.csv", "sha256": "e1668ad0b5e8e0f9cc5b08df69fc07b5de2c4bc84fa272263bf511c0961ee1e1", "n_features": 38924, "n_samples": 23, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1058988.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: GEO data_processing: HTSeq gene counts, DESeq2. The other supplementary files are DESeq2 result tables (baseMean/log2FoldChange/padj), not expression matrices.

### design (refused, not_started)

final: {"analysis_type": "none", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID27508874\\GSE74570\\suitability\\suitability.md", "n_comparisons": 15, "n_analyzable": 15}}

reasoning: Request asks for exercise effect; data hold no exercise vs non-exercise split (metadata grouping columns: genotype, age only).

rejected alternatives: [{"value": "grp OE_m24 vs WT_m24 (mNTG mice have better exercise capacity, S2.4.p1)", "reason_rejected": "genotype contrast; exercise capacity is a phenotype of the genotype, not an exercise intervention"}, {"value": "grp KO_m7 vs WT_m7 (mNKO exercise intolerance)", "reason_rejected": "genotype contrast, not an exercise effect"}, {"value": "WT_m24 vs WT_m4", "reason_rejected": "aging contrast, not exercise"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 23 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "exercise factor",
    "paper": "exercise tolerance tests used as functional readouts only",
    "data": "no exercise grouping column; all mice occasionally tested (treatment_protocol_ch1)",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID27508874 / GSE74570

**Status: refused at the `design` gate.** No exercise contrast exists in the data.

## What ran
- `python -m tools.case_runner inspect GSE74570 --data-root E:/agent/mwangLab_pdf/data`: the series was already cached. It holds 23 GSM samples in `_RAW.tar` (per-sample HTSeq gencode counts) plus 5 DESeq2 result tables. Those 5 tables are not expression matrices.
- `python -m tools.case_runner execute case_spec.json` recorded these gates:
  - `paper_reconstruction`
  - `ownership`
  - `alignment`: exact match on the GSM index, 23/23 samples.
  - `matrix`: raw counts, DESeq2.
  - `design`: `refused`.
- The validator passed with 5 records and 0 errors. Suitability came back `analyzable` with 15 comparisons, but every one is a genotype or age comparison.

## Why refused
- The sequenced groups are WT, mNKO and mNTG (Nampt knockout and overexpression) at 4, 7 and 24 months: WT_m7 4, KO_m7 4, WT_m4 4, OE_m4 3, WT_m24 4, OE_m24 4.
- The paper uses treadmill exercise only as a functional readout (S2.1.p3, S2.2.p2, S2.4.p1, FIG7D). It is never an intervention whose transcriptional effect was sequenced.
- GEO `treatment_protocol_ch1` says all mice were "occasionally subjected to glucose and exercise tolerance tests". That applies to every group, so it is not a factor.
- I considered and rejected three comparisons that link only indirectly to exercise; they are recorded as design candidates:
  - OE_m24 vs WT_m24: better exercise capacity.
  - KO_m7 vs WT_m7: exercise intolerance.
  - WT aging.
- Each of these is a genotype or age effect. Labelling any of them an exercise effect would misstate the estimand.

## DEG counts vs paper
None computed, because the run was refused. For reference, the paper's own RNA-seq results are:
- mNKO vs WT at 7 months: 33% of detected genes (S2.2.p3).
- mNTG vs WT at 24 months: 18 genes at Padj (S2.4.p1, FIG7F).

The paper's exact RNA-seq threshold is in Supplemental Information, which is not available here. The figure legend uses Padj, with "relaxed selection criteria".

## Deviations
None. No analysis was executed.

## Tool problems
- No runner defect was found.
- My first spec had an invalid JSON escape (`\d` inside a regex in a bash heredoc). I fixed it by using `[0-9]+`. This was my error, not the tool's.
- Side effect: the raw_tar merge writes `GSE74570_merged_from_tar.csv` into the shared `data/GSE74570/` cache, not only into the run directory. This is expected behaviour, noted for awareness.

