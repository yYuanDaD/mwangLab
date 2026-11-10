# Review packet B (the analysis' decisions): GSE296683

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.3.treatment", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.3.treatment level", "across": "characteristics_ch1.3.treatment", "pairs_or_sets": 6, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast is identifiable. All 12 sequenced myobundles received exercise-like E-Stim (Table 1; GEO treatment field '( EStim)' on every sample); there is no unstimulated or pre-stimulation arm. The data support only tomatidine vs vehicle under E-Stim (a drug effect) and YA vs OS (donor age/activity, one donor source per cohort, aliased with donor), neither of which is an effect of exercise.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE296683"], "assay": "bulk RNA-seq (Illumina, STAR + RSEM) of 3D donor-derived human myobundles (S2.6.p1)", "sample_inclusion": "12 myobundle chips, all electrically stimulated (E-Stim, 3 V/mm, 2 ms, 2 Hz, 2x30 min/day, days 14-21): Young active (YA) vehicle n=3, YA tomatidine n=3, Old sedentary (OS) vehicle n=3, OS tomatidine n=3 (Table 1; S2.5.p1; S3.1.p1)", "factors": {"cohort": ["YA", "OS"], "treatment": ["vehicle (EtOH)", "tomatidine 5 uM"], "stimulation": ["E-Stim only; no unstimulated RNA-seq arm"]}, "primary_estimand": "Effect of tomatidine vs vehicle on gene expression in E-Stim myobundles, separately within YA- and OS-derived myobundles (S2.7.p1; S3.2.p1). The paper's RNA-seq does not estimate the effect of exercise-like stimulation itself: every sequenced sample was stimulated.", "planned_contrasts": ["YA tomatidine vs YA vehicle, both E-Stim (S3.2.p1; paper: 215 up / 219 down = 434 DEGs)", "OS tomatidine vs OS vehicle, both E-Stim (S3.2.p1; paper: 12 up / 2 down = 14 DEGs)"], "repeated_measure_unit": "none; each chip is one independent myobundle; donor cell lines pooled per cohort (one YA and one OS donor source)", "normalization": "RSEM gene quantification; low average counts excluded (S2.6.p1)", "paper_method": "DESeq2 on RSEM counts, tomatidine vs matched control per cohort (S2.6.p1; S2.7.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "S2.6.p1"}, "paper_resu ... [140 more characters]

reasoning: S2.6.p1 gives the pipeline (STAR, RSEM, DESeq2, FDR 0.05 and 2.0-fold change). S2.7.p1 and S3.2.p1 define the DE contrasts as tomatidine vs matched E-Stim control within each cohort. Table 1 lists 12 samples, all 'Young E-Stim' or 'Old E-Stim'. S3.1.p2 mentions unstimulated myotubes only for contractility displacement, not for RNA-seq.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE296683\\GSE296683_GE6461.genes.fpkm.tsv.gz", "owned": true, "checks": ["S2.9.p1 names GSE296683", "GEO series has 12 samples matching Table 1 (4 groups x 3)", "organism Homo sapiens, tissue muscle, CD56+ myoblasts", "matrix has 12 sample columns whose names equal the GEO library names"], "accession": "GSE296683", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE296683\\GSE296683_metadata.csv"}

reasoning: Data availability statement S2.9.p1 names GSE296683; sample count and group structure match Table 1.

### alignment (valid, not_started)

final: {"method": "exact:libkey", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40832111\\GSE296683\\aligned\\aligned_metadata.csv", "columns": {"cohort": {"source": "characteristics_ch1.3.treatment", "regex": "^(YA|OS) "}, "trt": {"source": "characteristics_ch1.3.treatment", "regex": "^(?:YA|OS) (control|treated) ", "recode": {"control": "vehicle", "treated": "tomatidine"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40832111\\GSE296683\\aligned\\design_metadata.csv", "sha256": "d4295da2c7187bcd33e54bbcf32d0a1b445fdfcc3b09e076409837dbec1cea43", "levels": {"cohort": {"YA": 6, "OS": 6}, "trt": {"vehicle": 6, "tomatidine": 6}}}}

reasoning: Matrix columns are '<library name>.genes.results'; GEO description holds 'Library name: <library name>'. Exact match after stripping the suffix and prefix. cohort and trt come from the treatment characteristic ('YA control ( EStim)' etc.).

### matrix (valid, not_started)

final: {"matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40832111\\GSE296683\\aligned\\aligned_matrix.csv", "sha256": "586abc22d24c8592bf949b4b167ed5dbc138b1992d670ac9e5946994c602e5e1", "n_features": 60504, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 48780.03, "median": 0.0, "integer_fraction": 0.686, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GEO data_processing: 'tab-delimited matrix file, containing non-normalized FPKM values for all genes'; file name genes.fpkm.tsv.gz; values non-integer in 31% of cells. The paper ran DESeq2 on RSEM counts, which are not deposited, so the paper's method could not be reproduced exactly on this matrix (DESeq2 on FPKM is invalid).

### design (refused, not_started)

final: {"analysis_type": "none (refused)", "design_column": null, "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40832111\\GSE296683\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: The request asks how exercise affects gene expression. The paper's RNA-seq estimand is tomatidine vs vehicle within stimulated myobundles (S2.7.p1, S3.2.p1); stimulation is held constant. Candidate alternatives rejected: (1) trt tomatidine vs vehicle within cohort: analyzable but a pharmacological contrast, not exercise; (2) cohort OS vs YA: donor age/activity status confounded with the single donor cell source, not an exercise intervention, and not a paper DE contrast; (3) tomatidine x cohort interaction: not exercise. Small n is not the reason for stopping.

rejected alternatives: [{"value": "trt_tomatidine_vs_vehicle within cohort (paper's DE contrasts)", "reason_rejected": "drug effect under constant E-Stim, not an exercise effect"}, {"value": "cohort_OS_vs_YA", "reason_rejected": "donor age/activity, aliased with donor cell source; not an exercise contrast and not reported by the paper"}, {"value": "E-Stim vs unstimulated", "reason_rejected": "no unstimulated samples were sequenced"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix input",
    "paper": "DESeq2 on RSEM expected counts (S2.6.p1)",
    "data": "only an FPKM matrix is deposited",
    "disposition": "would require a declared deviation (limma on log2(FPKM+1)); moot because the case is refused at design"
  },
  {
    "item": "exercise estimand",
    "paper": "exercise-like E-Stim applied to every sequenced sample; DE contrasts are tomatidine vs vehicle",
    "data": "12/12 samples E-Stim",
    "disposition": "refused: no exercise contrast"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID40832111 / GSE296683

**Status: refused at `design`.** The data contain no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE296683` (the data were cached; nothing was downloaded).
- `python -m tools.case_runner execute case_spec.json`. Five gates were recorded: paper_reconstruction, ownership, alignment, matrix, and design (refused). The validator reported 0 errors.
- Alignment: exact match on the library name. The key came from GEO `description` ("Library name: X") and the matrix columns ("X.genes.results"). All 12 of 12 samples aligned.
- Matrix: FPKM. GEO data_processing says "non-normalized FPKM". The file is named genes.fpkm, and 31% of its values are non-integer. Suitability verdict: analyzable (two cohorts × two treatments, n=3 per cell, one sex).

## Why refused
- Table 1 and the GEO treatment field (`... ( EStim)`) show that all 12 sequenced myobundles received exercise-like electrical stimulation. No unstimulated or pre-stimulation sample was sequenced.
- The paper's RNA-seq contrasts are tomatidine vs vehicle within the E-Stim YA and OS myobundles (S2.7.p1, S3.2.p1). That is a drug effect measured while stimulation is held constant.
- YA vs OS is a donor age/activity contrast, aliased with the single donor cell source per cohort. It is not an exercise intervention.
- The unstimulated myotubes in S3.1.p2 were used only for contractility measurements, not for RNA-seq.
- So the request ("how exercise affects gene expression") cannot be identified from this dataset. Small n is not the reason for stopping.

## DEG counts vs paper
- Not run, because the case was refused.
- The paper reports 215 up / 219 down (434 DEGs) for YA tomatidine vs vehicle, and 12 up / 2 down (14 DEGs) for OS tomatidine vs vehicle.
- The paper's threshold is DESeq2 FDR < 0.05 and a 2.0-fold change, i.e. |log2FC| > 1 (S2.6.p1).

## Deviations (would have applied)
- The paper ran DESeq2 on RSEM counts, but only FPKM is deposited. Any rerun of the drug contrasts would need limma on log2(FPKM+1) as a declared deviation. This is moot here.

## Tool problems
- None that blocked the run.
- Cosmetic: the `matrix_column_keys` echo in the execute output lists only 10 of the 12 columns, while alignment reports 12/12.

