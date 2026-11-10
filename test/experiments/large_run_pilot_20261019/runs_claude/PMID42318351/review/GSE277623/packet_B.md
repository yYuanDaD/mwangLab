# Review packet B (the analysis' decisions): GSE277623

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.5.treatment", "n_values": 6, "max_repeat": 6, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## Stop reasons

- design (refused; claim type: pairing, exercise_arm): No exercise contrast: every sequenced group is defined by disease induction (L-NAME + HFD), time point, or drug treatment (EMPA, PFD, EMPA+PFD, PBS vehicle). Exercise appears only as a treadmill exhaustion test used as a functional outcome (S3.5.p1, S4.1.p4); no animal was exercise-trained, so the data cannot identify an effect of exercise on gene expression.

## Samples per design level

### `grp`
- **Con5W** (3): GSM8526569 / Heart, control 5 weeks, biorep 1; GSM8526570 / Heart, control 5 weeks, biorep 2; GSM8526571 / Heart, control 5 weeks, biorep 3
- **Con9W** (3): GSM8526575 / Heart, control 9 weeks, biorep 1; GSM8526576 / Heart, control 9 weeks, biorep 2; GSM8526577 / Heart, control 9 weeks, biorep 3
- **EMPA9W** (2): GSM8526581 / Heart, EMPA treated 9 weeks, biorep 1; GSM8526582 / Heart, EMPA treated 9 weeks, biorep 2
- **EMPAPFD9W** (3): GSM8526585 / Heart, EMPA and PFD treated 9 weeks, bio; GSM8526586 / Heart, EMPA and PFD treated 9 weeks, bio; GSM8526587 / Heart, EMPA and PFD treated 9 weeks, bio
- **HF5W** (3): GSM8526572 / Heart, HFpEF 5 weeks, biorep 1; GSM8526573 / Heart, HFpEF 5 weeks, biorep 2; GSM8526574 / Heart, HFpEF 5 weeks, biorep 3
- **PBS9W** (3): GSM8526578 / Heart, untreated 9 weeks, biorep 1; GSM8526579 / Heart, untreated 9 weeks, biorep 2; GSM8526580 / Heart, untreated 9 weeks, biorep 3
- **PFD9W** (2): GSM8526583 / Heart, PFD treated 9 weeks, biorep 1; GSM8526584 / Heart, PFD treated 9 weeks, biorep 2

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE277623"], "assay": "bulk RNA-seq (DNBSEQ-T7, BGI) of rat left ventricle, male rats only, n = 3 per group (one EMPA and one PFD sample excluded for corrupted files -> 19 samples)", "factors": {"group": ["control 5w", "HFpEF 5w (L-NAME + HFD)", "control 9w", "untreated HFpEF 9w (PBS vehicle)", "EMPA 9w", "PFD 9w", "EMPA + PFD 9w"]}, "intervention": "pharmacological: empagliflozin (0.35 g/kg/d), pirfenidone (0.3 g/kg/d), or both, by oral gavage for 4 weeks after 5 weeks of L-NAME + high-fat diet (S3.1.p1-p2). Exercise appears only as an outcome readout (treadmill exhaustion test, S3.5.p1), never as an intervention or a sequenced group.", "primary_estimand": "Transcriptional effect of EMPA + PFD dual therapy versus untreated (PBS vehicle) HFpEF in rat left ventricle (S4.4.p1, S4.4.p4 'TE'). No exercise estimand exists in the paper.", "planned_contrasts": ["EMPA+PFD vs untreated 9w (TE; S4.4.p1: 717 DEGs, 421 up / 296 down)", "EMPA vs untreated 9w (S4.4.p1: 52 DEGs)", "PFD vs untreated 9w (S4.4.p1: 4 DEGs)", "control 9w vs untreated 9w (S4.4.p2: 295 DEGs)", "control 9w vs control 5w (PC; S4.4.p4)", "HFpEF 5w vs control 5w (DE; S4.4.p4)", "untreated 9w vs control 9w (UT; S4.4.p4)", "EMPA+PFD / PFD / EMPA / untreated vs HFpEF 5w (S4.4.p2: 2954 / 1492 / 439 / 439 DEGs)"], "repeated_measure_unit": "none (independent animals, one LV sample each)", "normalization": "htseq-count raw counts into iDEP.96 (S3.9.p1)", "paper_method": "DESeq2 (iDEP 0.96), pairwise two-grou ... [227 more characters]

reasoning: The paper (S3.1.p1-p2) is a drug-treatment study in a two-hit HFpEF rat model. The RNA-seq groups (S3.9.p1, S4.4.p1-p4, FIG5) are control/HFpEF at 5 weeks and control/untreated/EMPA/PFD/EMPA+PFD at 9 weeks. The only exercise element is a treadmill exhaustion test used to measure exercise tolerance as a functional endpoint (S3.5.p1, S4.1.p4); no group was exercise-trained and no sequenced sample is defined by exercise.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42318351\\GSE277623\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["Data availability S11.p1 and S3.9.p1 name GSE277623", "GEO series: Rattus norvegicus heart, male, RNA-Seq, htseq-count, rn6 (matches S3.9.p1)", "19 samples = 7 groups x 3 minus the 2 excluded monotherapy samples (S4.4.p1): EMPA n=2, PFD n=2", "_RAW.tar members are GSM-prefixed per-sample htseq-count files (GSM8526569_Con_5W_1 ... GSM8526587_EMPA_PFD_9W_3), giving an exact GSM key; the series-level GSE277623_raw_count.txt.gz carries the same labels without GSM ids"], "accession": "GSE277623", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE277623\\GSE277623_metadata.csv"}

reasoning: The accession, organism, tissue, sex, pipeline and sample counts all match the paper. The per-sample tar is used because its file names carry GSM ids, which allows exact alignment instead of decoding label abbreviations.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 19, "n_metadata": 19, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42318351\\GSE277623\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^Heart, (control|HFpEF|untreated|EMPA treated|PFD treated|EMPA and PFD treated) ([59]) weeks, biorep \\d+$", "recode": {"control_5": "Con5W", "HFpEF_5": "HF5W", "control_9": "Con9W", "untreated_9": "PBS9W", "EMPA treated_9": "EMPA9W", "PFD treated_9": "PFD9W", "EMPA and PFD treated_9": "EMPAPFD9W"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42318351\\GSE277623\\aligned\\design_metadata.csv", "sha256": "d074e59cf1e11ac239b593b0ea595a4826db467412d26f14c02d20c80042e411", "levels": {"grp": {"Con5W": 3, "HF5W": 3, "Con9W": 3, "PBS9W": 3, "EMPAPFD9W": 3, "EMPA9W": 2, "PFD9W": 2}}}}

reasoning: Tar columns are GSM ids, matching the metadata index exactly. grp is derived from the GEO title (group + week), cross-checked against characteristics 'disease state', 'time' and 'treatment'.

### matrix (valid, not_started)

final: {"source": "GSE277623_RAW.tar (per-sample htseq-count)", "paper_input": "htseq-count raw counts into DESeq2 via iDEP (S3.9.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42318351\\GSE277623\\aligned\\aligned_matrix.csv", "sha256": "1c6c6fbe5c9abebfdd6f1afb2a7e9461bb3590b762bf78e6aff71cae3b12c8e4", "n_features": 17455, "n_samples": 19, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 329596.0, "median": 99.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values are integers (inspect: integer_fraction 1.0, max 329596); GEO data_processing and S3.9.p1 state HISAT2 + htseq-count, i.e. raw read counts, the input the paper fed to DESeq2.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "grp", "contrasts": [], "suitability": {"verdict": "partially_analyzable", "failed": [], "warnings": ["sample_size"], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42318351\\GSE277623\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 4}}

reasoning: S3.1.p1-p2 and S4.4.p1-p4 define seven groups by disease, time and drug; none by exercise. The treadmill test in S3.5.p1 measures exercise capacity as an endpoint and is not a sequenced factor. Refused at design.

rejected alternatives: [{"value": "grp EMPAPFD9W vs PBS9W (paper's primary TE contrast)", "reason_rejected": "drug-treatment effect, not an exercise effect; outside the request's estimand"}, {"value": "any group vs Con9W / Con5W", "reason_rejected": "disease or age effects; no group differs by exercise exposure"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **partially_analyzable**; check: sample_size
- | Check | Status | Detail |
- | Sample size | partial | 4/6 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 19 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "request vs paper estimand",
    "paper": "drug-treatment study (EMPA, PFD, EMPA+PFD vs vehicle in HFpEF rats); exercise only as a treadmill tolerance endpoint",
    "data": "19 LV samples in 7 groups defined by disease/time/drug; no exercise factor",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID42318351 / GSE277623

**Status: refused at `design`. The data contain no exercise contrast.**

## What ran
- `python -m tools.case_runner inspect GSE277623` (cached data): `GSE277623_raw_count.txt.gz` (17,455 genes x 19 samples, all integers) plus a per-sample `_RAW.tar`.
- `python -m tools.case_runner execute case_spec.json`. Five gates were recorded: paper_reconstruction, ownership, alignment, matrix and design (refused). The validator reported 0 errors and the case route is `stopped`.
  - Alignment: `raw_tar: true`. The tar member names carry GSM ids, so all 19/19 samples matched exactly on the metadata index. `grp` was taken from the GEO title, giving Con5W 3, HF5W 3, Con9W 3, PBS9W 3, EMPAPFD9W 3, EMPA9W 2, PFD9W 2.
  - Matrix: raw counts (HISAT2 + htseq-count, as in S3.9.p1 and GEO data_processing), which is the input the paper gave DESeq2 through iDEP.
  - The suitability report (`GSE277623/suitability/suitability.md`) came back as `partially_analyzable`, with a sample-size warning for the n=2 monotherapy arms. The refusal is about the estimand, not about analyzability.

## Why refused
This paper tests drugs (empagliflozin, pirfenidone, and the two combined, against PBS vehicle) in an L-NAME + high-fat-diet HFpEF rat model (S3.1.p1-p2). All seven sequenced groups are defined by disease, time point or drug. Exercise appears only as a treadmill exhaustion test, used as a functional outcome (S3.5.p1, S4.1.p4). No animal was exercise-trained, so these data cannot estimate an effect of exercise on gene expression.

## DEG counts vs paper
No DE was run. The paper's threshold is FDR < 0.05 and |FC| > 2, i.e. |log2FC| > 1 (S3.9.p1, FIG5 legend). The paper reports these DEG counts (none of them exercise contrasts):
- EMPA+PFD vs untreated: 717 (421 up, 296 down)
- EMPA vs untreated: 52
- PFD vs untreated: 4
- control 9w vs untreated: 295
- vs HFpEF 5w: EMPA+PFD 2954, PFD 1492, EMPA 439, untreated 439

## Deviations
- I used the per-sample `_RAW.tar` (GSM-keyed) rather than the series-level `GSE277623_raw_count.txt.gz`. Both carry the same sample labels, and the tar gives exact GSM alignment without decoding abbreviations.

## Tool problems
- No blocking problems.
- Minor: the series-level matrix column names (for example `Con_5W_1`, `PBS_9W_1`) do not match any metadata field. Inspect reported `alignment_keys: []`, and its vocabulary differs from the GEO titles ("control", "untreated"). One column has a typo (`EMPA_PFD9W_1` against `EMPA_PFD_ ... [191 more characters]
