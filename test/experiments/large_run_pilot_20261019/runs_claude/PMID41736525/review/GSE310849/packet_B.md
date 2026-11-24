# Review packet B (the analysis' decisions): GSE310849

## Mechanical flags

- none

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: groups are TTX-induced disuse, recovery after TTX exhaustion (habitual cage activity), repeated TTX, sham and contralateral control limbs (S2.8.p1, S2.9.p1). No exercise intervention exists in the design.

## Samples per design level

### `grp`
- **CTRL** (12): GSM9309962 / 354_R / Library name: GC-AS-10656-54R_S7; GSM9309964 / 362_R / Library name: GC-AS-10656-62R_S15; GSM9309966 / 364_R / Library name: GC-AS-10656-64R_S24; GSM9309968 / 365_R / Library name: GC-AS-10656-65R_S1; GSM9309970 / 366_R / Library name: GC-AS-10656-66R_S4; GSM9309972 / 367_R / Library name: GC-AS-10656-67R_S13; GSM9309974 / 369_R / Library name: GC-AS-10656-69R_S14; GSM9309976 / 370_R / Library name: GC-AS-10656-70R_S6; GSM9309978 / 371_R / Library name: GC-AS-10656-71R_S5; GSM9309980 / 372_R / Library name: GC-AS-10656-72R_S2; GSM9309982 / 377_R / Library name: GC-AS-10656-77R_S12; GSM9309984 / 379_R / Library name: GC-AS-10656-79R_S17
- **REC** (3): GSM9309973 / 369_L / Library name: GC-AS-10656-69L_S22; GSM9309975 / 370_L / Library name: GC-AS-10656-70L_S20; GSM9309977 / 371_L / Library name: GC-AS-10656-71L_S23
- **RTTX** (3): GSM9309965 / 364_L / Library name: GC-AS-10656-64L_S16; GSM9309967 / 365_L / Library name: GC-AS-10656-65L_S18; GSM9309969 / 366_L / Library name: GC-AS-10656-66L_S10
- **SHAM** (3): GSM9309961 / 354_L / Library name: GC-AS-10656-54L_S8; GSM9309981 / 377_L / Library name: GC-AS-10656-77L_S3; GSM9309983 / 379_L / Library name: GC-AS-10656-79L_S21
- **TTX** (3): GSM9309963 / 362_L / Library name: GC-AS-10656-62L_S19; GSM9309971 / 367_L / Library name: GC-AS-10656-67L_S9; GSM9309979 / 372_L / Library name: GC-AS-10656-72L_S11

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE310344", "GSE310849"], "assay": "bulk RNA-seq, aged (23 mo) male F344 rat tibialis anterior", "factors": {"condition": ["contralateral control (right limb, pooled)", "sham", "TTX atrophy", "TTX+Recovery", "Repeated TTX"], "limb": ["Left", "Right"]}, "primary_estimand": "Effect of TTX nerve-block disuse atrophy, recovery after TTX exhaustion, and repeated TTX vs pooled contralateral control limb; no exercise intervention", "planned_contrasts": ["Atrophy vs Control (S3.5.p1; 2106 DEGs)", "Recovery vs Control (2008 DEGs)", "Repeated Atrophy vs Control (3937 DEGs)", "Recovery vs Atrophy", "Repeated Atrophy vs Recovery"], "inclusion": "sham excluded; right contralateral limbs pooled as control (S2.14.p1)", "paper_method": "DESeq2 median-of-ratios within Partek Flow (S2.14.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "inclusive": true, "effect_metric": "fold change", "effect_cutoff": 0.2630344, "effect_inclusive": true, "note": ">=20% FC", "source_locator": "S2.14.p1"}, "exercise_content": "Recovery = cessation of TTX with habitual cage activity; no exercise (S2.9.p1; S3.7.p1 return to habitual activity)"}

reasoning: S2.8-S2.9 define a TTX disuse model in aged rats; S2.14.p1 defines control pooling and threshold; S3.5.p1 gives counts. No exercise arm.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE310849\\GSE310849_Partek_GC-AS-10656_Normalization_Normalized_counts.txt.gz", "owned": true, "checks": ["Rattus norvegicus TA muscle from aged rats (extract_protocol)", "12 left/12 right limbs; sham/TTX/RTTX/TTX+Recovery n=3 + 12 CTRL matches S2.8.p1", "Partek/STAR rn7 pipeline matches S2.14.p1"], "accession": "GSE310849", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE310849\\GSE310849_metadata.csv"}

reasoning: Metadata matches the aged-rat arm of the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 24, "n_metadata": 24, "coverage": 1.0, "unmatched_matrix_columns": ["Start", "Stop", "Length", "BLGCSEQ0311-Control-2_S26", "BLGCSEQ0311-Control-1_S25", "BLGCSEQ0311-Control-3_S27"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41736525\\GSE310849\\aligned\\aligned_metadata.csv", "columns": {"limb": {"alias_of": "characteristics_ch1.1.limb"}, "grp": {"alias_of": "characteristics_ch1.2.condition", "recode": {"control (CTRL)": "CTRL", "sham": "SHAM", "TTX": "TTX", "Repeated TTX (RTTX)": "RTTX", "TTX+Recovery": "REC"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41736525\\GSE310849\\aligned\\design_metadata.csv", "sha256": "67e736a4c70316b33ece4fbc760d254b370df946ce6144dba8edde64413c3671", "levels": {"limb": {"Left": 12, "Right": 12}, "grp": {"CTRL": 12, "SHAM": 3, "TTX": 3, "RTTX": 3, "REC": 3}}}}

reasoning: Matrix columns equal the description Library name (24/24). grp from condition.

### matrix (valid, not_started)

final: {"source": "GSE310849_Partek_GC-AS-10656_Normalization_Normalized_counts.txt.gz", "paper_input": "raw counts into DESeq2; only normalized counts deposited", "matrix_type": "linear_normalized (Partek DESeq2 median-of-ratios normalized counts)", "recommended_method": "limma on log2(x+1) as a declared deviation (raw counts not deposited)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41736525\\GSE310849\\aligned\\aligned_matrix.csv", "sha256": "64c3151bd17ca02b107b21298584a85baaeeffd499d1201a9fe9a250dae00c29", "n_features": 14271, "n_samples": 24, "annotation_columns_dropped": [], "duplicated_feature_ids": 14249, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 70311.5, "median": 7.91564, "integer_fraction": 0.0814, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name says Normalized_counts; 11% integers; no raw counts deposited.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "grp", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41736525\\GSE310849\\suitability\\suitability.md", "n_comparisons": 10, "n_analyzable": 10}}

reasoning: No exercise arm; refused at design.

rejected alternatives: [{"value": "grp_REC_vs_TTX as reloading", "reason_rejected": "Recovery is spontaneous return of nerve function with cage activity, not exercise."}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Rat') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix input",
    "paper": "DESeq2 on counts",
    "data": "only normalized counts deposited",
    "disposition": "moot because refused at design"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID41736525 (GSE310344, GSE310849)

## Outcome: refused (both cases, at `design`)

The paper studies **disuse**, not exercise:

- **Human (GSE310344):** 9 young adults, 36 vastus lateralis biopsies. Timepoints: Baseline → 2 wk knee-brace immobilization (Atrophy) → ~7 wk return to *normal ambulatory activity* (Recovery) → 2 wk repeated immobilization (Repeated Atrophy). Source: S2.3.p1.
  - Participants were told to avoid strenuous exercise for 24 h before each biopsy.
  - The supervised resistance-training programme was offered only after the study ended and was never biopsied (S2.3.p1).
- **Aged rat (GSE310849):** tetrodotoxin (TTX) block of the common peroneal nerve. Groups: TTX atrophy, recovery after the TTX ran out (habitual cage activity), repeated TTX, sham, and the contralateral right-limb controls (S2.8.p1, S2.9.p1).

No sampled arm receives an exercise bout or a training programme. Calling "recovery" (return to habitual activity) an exercise effect would change the paper's estimand, so both cases were refused at `design`.

Gates recorded in order: `paper_reconstruction`, `ownership`, `alignment`, `matrix`, `design` (refused). No executions or enrichment ran. The contract validator passed: 10 records, 0 errors.

## What ran

- `python -m tools.case_runner inspect` for both series (data downloaded to `data/`).
- `python -m tools.case_runner execute case_spec.json`.
  - Alignment: exact match on the `Library name` key, 36/36 human samples and 24/24 rat samples.
  - The suitability report was generated for both cases (verdict "analyzable" for 6 and 10 non-exercise comparisons). No comparison was run.

## DEG counts vs the paper

Not computed, because both cases were refused. For reference, the paper's threshold is FDR ≤ 0.05 and fold change ≥ 20% (|log2FC| ≥ log2(1.2) = 0.2630344), from S2.14.p1. Its counts:

- **Human (S3.3.p1):**
  - Atrophy vs Baseline: 381
  - Repeated Atrophy vs Baseline: 103
  - Repeated Atrophy vs Recovery: 82
  - Recovery vs Atrophy: 536
  - Recovery vs Baseline: 0
- **Aged rat (S3.5.p1):**
  - Atrophy vs Control: 2106
  - Recovery vs Control: 2008
  - Repeated Atrophy vs Control: 3937

## Deviations and notes (would apply if anyone reruns this as a disuse analysis)

- Neither series deposits raw counts:
  - GSE310344 has Partek CPM only.
  - GSE310849 has Partek DESeq2-normalized counts only.
- So the paper's DESeq2 route cannot be reproduced exactly. limma on log2(x+1) would be a declared deviation.
- Human sa ... [1056 more characters]
