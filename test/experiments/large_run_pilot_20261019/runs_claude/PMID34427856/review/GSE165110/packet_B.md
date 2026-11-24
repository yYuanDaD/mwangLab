# Review packet B (the analysis' decisions): GSE165110

## Mechanical flags

- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"contact_department": ["Physical Therapy and Athletic Training"]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast in the sequenced samples. GSE165110 contains only C2C12 myotubes treated 24 h with 4% STEM secretome vs 4% horse serum (6 vs 6). The paper's in vivo manipulations are hindlimb unloading (disuse) and 7-day ambulatory recovery, not exercise, and those mice were not sequenced. A STEM-vs-serum contrast in cultured cells cannot estimate how exercise affects gene expression.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE165110"], "assay": "bulk total RNA-seq (Ribo-Zero, NovaSeq 150x150) of C2C12 myotubes only (S2.6.p2); in vivo mouse arms (PBS/STEM x CON/HU/Recovery, S2.1.p1) were analysed by histology, mass and grip strength only, not sequenced", "primary_estimand": "Transcriptional effect of 24 h 4% STEM secretome vs 4% horse serum (control) in differentiated C2C12 myotubes (S2.6.p2, S3.4.p1, Fig. 8B). No exercise or training factor exists anywhere in the study; the in vivo loading manipulation is hindlimb unloading (disuse) and 7-day ambulatory reloading, and those animals were not sequenced.", "factors": {"treatment": ["4% horse serum (control)", "4% STEM"]}, "sample_inclusion": "6 replicate wells per arm (12 samples) per GEO; paper S2.6.p1 states 6 replicates per condition", "planned_contrasts": ["STEM vs horse serum in C2C12 myotubes (S3.4.p1, Fig. 8B; DEG count not stated in the text, top-20 up/down table in Fig. 8B)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "inclusive": true, "source_locator": "S2.7.p1"}, "paper_method": "DESeq2 1.26.0, 5% FDR (adj. P <= 0.05) (S2.7.p1)", "paper_results": "Named genes regulated by STEM: Igfbp3, Col23a1, Col14a1, Mt2, Mt1, Fmod (S3.4.p1); total DEG count not given in the text"}

reasoning: The only sequenced experiment (S2.6.p2, GSE165110) is an in vitro secretome-vs-serum treatment of C2C12 myotubes. The in vivo arms (S2.1.p1, S2.3.p1) are disuse (hindlimb unloading) and recovery, not exercise, and have no RNA-seq. Threshold: S2.7.p1 '5% false discovery rate with DESeq2', adj. P <= 0.05, no fold-change cutoff.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE165110\\GSE165110_18294R_counts.txt.gz", "owned": true, "checks": ["S2.6.p2 names GSE165110", "GEO contact Micah J Drummond, University of Utah (paper lab, S2.1.p1 Utah IACUC)", "12 samples: 6 x 4% Horse Serum, 6 x 4% STEM, C2C12 myotubes, matching S2.6.p1-p2"], "accession": "GSE165110", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE165110\\GSE165110_metadata.csv"}

reasoning: Paper cites GSE165110 for the C2C12 RNA-seq; the counts file GSE165110_18294R_counts.txt.gz has 12 columns 18294X1..X12 that match the GEO titles.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34427856\\GSE165110\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "characteristics_ch1.2.treatment", "regex": "^24 hours of (4% Horse Serum|STEM)$", "recode": {"4% Horse Serum": "HS", "STEM": "STEM"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34427856\\GSE165110\\aligned\\design_metadata.csv", "sha256": "2ffaed34be4fac6d97a3570758b9bcebbcd6d703e9b9c329fb42e63caffce520", "levels": {"grp": {"HS": 6, "STEM": 6}}}}

reasoning: Matrix columns 18294X1..X12 sit at the start of the GEO title; exact match after extracting them. grp derived from the treatment characteristic.

### matrix (valid, not_started)

final: {"source": "GSE165110_18294R_counts.txt.gz (GEO supplementary)", "paper_input": "DESeq2 on gene counts (S2.7.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34427856\\GSE165110\\aligned\\aligned_matrix.csv", "sha256": "7d6250b2350a13ec4edfcdab9f460767439f807f3930bdf16d73943fd9a9a603", "n_features": 55487, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 434599.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values are integers (integer fraction 1.0, max 434599, median 0), Ensembl gene IDs; data_processing: STAR 2.7.3a two-pass alignment, reads assigned to annotated genes (featureCounts-style). Consistent with the paper's DESeq2 input.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34427856\\GSE165110\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: S2.6.p1-p2 and GEO metadata: the only sequenced factor is culture medium (STEM vs horse serum). S2.1.p1, S2.3.p1: in vivo arms are CON / hindlimb unloading / recovery, measured by histology and grip strength only. No exercise or training arm exists.

rejected alternatives: [{"value": "grp_STEM_vs_HS (C2C12, DESeq2)", "reason_rejected": "Valid pharmacological/secretome contrast the paper ran (Fig. 8B), but it is not an exercise estimand; running it would answer a different question than the one requested."}, {"value": "Recovery (reloading after HU) vs HU as an exercise-like contrast", "reason_rejected": "Not sequenced (no RNA-seq of mouse soleus in GSE165110 or any other accession in the paper); and reloading/ambulation after disuse is not an exercise intervention. ... [3 more characters]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "Requested estimand",
    "paper": "Effect of STEM secretome on aged muscle during disuse/recovery; RNA-seq only for STEM vs horse serum in C2C12 myotubes",
    "data": "12 C2C12 samples, STEM vs horse serum; no exercise factor",
    "disposition": "blocks_estimand"
  },
  {
    "item": "Paper extract protocol",
    "paper": "Qiazol + miRNeasy Mini Kit (S2.6.p2)",
    "data": "GEO extract_protocol: Trizol",
    "disposition": "recorded_only"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID34427856 / GSE165110

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE165110 --data-root E:/agent/mwangLab_pdf/data` downloaded the series. It holds one matrix, `GSE165110_18294R_counts.txt.gz`: 55,487 Ensembl genes × 12 samples, all integers. The GEO metadata has 12 samples.
- `python -m tools.case_runner execute case_spec.json` recorded these gates:
  - `paper_reconstruction`, `ownership`, `alignment` (exact match on a key taken from `title`, 12/12 samples), and `matrix` (raw counts, DESeq2-compatible).
  - `design`: `refused`.
- The validator found 0 errors in 5 records. The suitability report said the STEM-vs-HS split was analyzable (6 vs 6), but that split is not an exercise estimand.

## Why refused
- **What was sequenced:** GSE165110 contains only C2C12 myotubes treated for 24 h with 4% STEM secretome or 4% horse serum (S2.6.p1–p2, Fig. 8B).
- **The mouse experiments:** the paper's in vivo arms are ambulatory control, 14 days of hindlimb unloading (disuse), and unloading plus 7 days of recovery, each with PBS or STEM (S2.1.p1, S2.3.p1). They were assessed only by histology, muscle mass and grip strength, never by RNA-seq.
- **Conclusion:** no exercise or training factor exists in the study. A secretome-versus-serum contrast in cultured cells cannot estimate the effect of exercise.

## DEG counts vs paper
- None computed (refused).
- The paper's own threshold is DESeq2 at 5% FDR (adj. P ≤ 0.05), with no fold-change cutoff (S2.7.p1).
- The paper's text gives no total DEG count. It names Igfbp3, Col23a1, Col14a1, Mt2, Mt1 and Fmod as regulated genes (S3.4.p1), and shows the top-20 up and down genes in Fig. 8B.

## Deviations
- None. The paper's own contrast (STEM vs HS in C2C12, DESeq2) is executable on these data. It was deliberately not run because it does not answer the exercise request.
- It is recorded as a rejected candidate in the design gate.
- Minor metadata discrepancy, recorded only: the paper says RNA was extracted with Qiazol and the miRNeasy kit, while GEO says Trizol.

## Tool problems
- None blocking.
- Minor: `inspect` lists `characteristics_ch1.2.treatment` as the only grouping column. It gives no hint that the study has no exercise factor, so the agent has to judge that from the paper. This is expected behaviour, not a bug.

