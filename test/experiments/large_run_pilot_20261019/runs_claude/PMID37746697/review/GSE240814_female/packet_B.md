# Review packet B (the analysis' decisions): GSE240814_female

## Mechanical flags

- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"characteristics_ch1.2.treatment": ["Hindlimb Unloading"], "trt": ["Hindlimb Unloading"]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the study compares hindlimb unloading (disuse) durations with 0 h ambulatory controls. Unloading is the opposite of an exercise/loading stimulus, and no exercise or training group exists in the paper or in GEO (treatment levels: Control, Hindlimb Unloading). The requested estimand (effect of exercise on gene expression) cannot be identified from these data.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE240814"], "primary_estimand": "Effect of hindlimb unloading (disuse) duration (24, 48, 72, 168 h vs 0 h control) on gastrocnemius transcriptome, analysed separately in male and female C57BL/6J mice. No exercise or training arm.", "planned_contrasts": ["Female HU 24h/48h/72h/168h vs 0h control (abstract; GEO supplementary DE files per sex and time)"], "factors": {"time_HU": ["0h", "24h", "48h", "72h", "168h"], "sex": ["Male", "Female"]}, "inclusion": "n=8/group per abstract; GEO has 7 male / 8 female controls and 7-9 per HU group", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "abstract has no threshold; inferred from GEO supplementary DE_*vs0.csv files (all FDR step-up < 0.05, no FC cutoff)"}, "paper_method": "Partek Flow: STAR mm10, filter genes max count <= 50, median-ratio normalization, DESeq2 (GEO data_processing)", "paper_results": {"male_DEGs": {"24vs0": 3888, "48vs0": 4133, "72vs0": 1611, "168vs0": 3053}, "female_DEGs": {"24vs0": 3173, "48vs0": 4907, "72vs0": 3647, "168vs0": 1633}, "source": "GEO supplementary Total_Up_and_Down_DE_*.csv"}}

reasoning: Only the PubMed abstract and the GEO series description are available (no full text). Both describe hindlimb unloading (HU), a disuse/unloading model of muscle atrophy, compared against 0 h ambulatory controls in each sex. No exercise, training, or loading intervention is described.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE240814\\GSE240814_HU_female_total.csv", "owned": true, "checks": ["GEO Series_pubmed_id = 37746697", "Series title equals paper title", "metadata description 'HU female_total.xlsx' names this matrix"], "accession": "GSE240814", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE240814\\GSE240814_metadata.csv"}

reasoning: GSE240814 is the paper's own deposit; the per-sex matrix is listed in each sample's description field.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 39, "n_metadata": 80, "coverage": 0.4875, "unmatched_matrix_columns": ["Start", "Stop", "Length", "gene_version"], "unmatched_metadata_samples": ["GSM7709796", "GSM7709797", "GSM7709798", "GSM7709799", "GSM7709800", "GSM7709801", "GSM7709802", "GSM7709803", "GSM7709804", "GSM7709805", "GSM7709806", "GSM7709807", "GSM7709808", "GSM7709809", "GSM7709810", "GSM7709811", "GSM7709812", "GSM7709813", "GSM7709814", "GSM7709815", "GSM7709816", "GSM7709817", "GSM7709818", "GSM7709819", "GSM7709820", "GSM7709821", "GSM7709822", "GSM7709823", "GSM7709824", "GSM7709825", "GSM7709826", "GSM7709827", "GSM7709828", "GSM7709829", "GSM7709830", "GSM7709831", "GSM7709832", "GSM7709833", "GSM7709834", "GSM7709835", "GSM7709836"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37746697\\GSE240814_female\\aligned\\aligned_metadata.csv", "columns": {"trt": {"alias_of": "characteristics_ch1.2.treatment"}, "sex": {"alias_of": "characteristics_ch1.3.Sex"}, "time": {"source": "characteristics_ch1.4.time point", "regex": "^(\\d+)h$", "recode": {"0": "h0", "24": "h24", "48": "h48", "72": "h72", "168": "h168"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37746697\\GSE240814_female\\aligned\\design_metadata.csv", "sha256": "65898bc9986742403bbb6f57136367bdb86ba306e7674b26be4107209fb2d228", "levels": {"trt": {"Hindlimb Unloading": 31, "Control": 8}, "sex": {"Female": 3 ... [65 more characters]

reasoning: Matrix columns equal metadata 'title' exactly (inspect alignment_keys). Short formula-safe columns trt/sex/time derived for the record.

### matrix (valid, not_started)

final: {"matrix_type": "DESeq2 median-ratio normalized counts (linear, non-integer)", "recommended_method": "limma on log2(x+1) (raw counts not deposited)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37746697\\GSE240814_female\\aligned\\aligned_matrix.csv", "sha256": "c0e4252a2d9ccfa1f42d9844f9d76565be84203e6509ccf39de6ad47afb0892a", "n_features": 11068, "n_samples": 39, "annotation_columns_dropped": [], "duplicated_feature_ids": 11046, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1187630.0, "median": 304.3, "integer_fraction": 0.0061, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Integer fraction ~0.03; GEO data_processing: 'filtered counts were median ratio normalized and tested ... using DESeq2' (Partek Flow). Values are normalized counts, not raw counts. Not needed further because the case stops at design.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37746697\\GSE240814_female\\suitability\\suitability.md", "n_comparisons": 10, "n_analyzable": 10}}

reasoning: Treatment column has only 'Control' and 'Hindlimb Unloading'; time 0h=controls. Any contrast available here (HU vs control) estimates disuse, not exercise; relabelling it as exercise would misstate the estimand.

rejected alternatives: [{"value": "time_h24/h48/h72/h168_vs_h0 within sex (paper's own HU design)", "reason_rejected": "Estimates disuse/unloading, not exercise; outside the requested exercise estimand"}, {"value": "reverse direction (control vs HU) as a 'reloading/activity' proxy", "reason_rejected": "Ambulatory cage activity is not an exercise intervention; would be a manufactured contrast"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "group size",
    "paper": "n=8/group (abstract)",
    "data": "Female: controls 8, HU groups 7-9 samples",
    "disposition": "recorded_only"
  },
  {
    "item": "intervention",
    "paper": "hindlimb unloading (disuse)",
    "data": "GEO treatment: Control / Hindlimb Unloading",
    "disposition": "blocks_requested_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID37746697 / GSE240814

**Outcome: refused at the `design` gate (both cases). No DE model was run.**

## Paper evidence: abstract only
No full text was available. The comparison with the paper rests on the PubMed abstract only
(`PMID37746697_abstract.txt`, fetched with NCBI efetch), plus the GEO series summary and overall design
and the authors' GEO supplementary DE files.

## What ran
1. `python -m tools.case_runner inspect GSE240814 --data-root E:/agent/mwangLab_pdf/data` downloaded the series
   to `data/GSE240814/`. It holds two per-sex matrices (`GSE240814_HU_male_total.csv`, 41 samples;
   `GSE240814_HU_female_total.csv`, 39 samples) and the authors' per-time DE/pathway tables.
2. `case_spec.json` (made by `make_spec.py`) has two cases, `GSE240814_male` and `GSE240814_female`.
   - The gates `paper_reconstruction`, `ownership`, `alignment` (exact match on `title`, 100% of matrix columns) and `matrix` are all `valid`.
   - `design` is `refused`.
   - Run result: `execute` completed and the validator reported 10 records with 0 errors.
   - The suitability report said "analyzable" (10 HU-time comparisons per sex), but that is a check on the data structure, not on the estimand.

## Why refused
- The study is **hindlimb unloading (HU), a disuse/atrophy model**. It compares 24/48/72/168 h of HU with 0 h ambulatory controls, separately in each sex.
- GEO treatment levels are only `Control` and `Hindlimb Unloading`. There is no exercise, training or loading arm in the paper or the data.
- The requested estimand ("how exercise affects gene expression") therefore cannot be identified.
- Running HU vs control and calling it an exercise effect would misstate the estimand. Reversing it (control vs HU as an "activity" proxy) would be a manufactured contrast. Both alternatives are recorded as rejected candidates.

## DEG counts vs paper
None computed (refused). For the record:
- The abstract states no DEG counts or threshold.
- The authors' GEO files (`*_Total_Up_and_Down_DE_*.csv`) report the counts below. Their DE tables all have FDR step-up < 0.05 and no fold-change cutoff.
- So the paper's threshold, inferred from the deposit rather than from the paper, is **FDR < 0.05**.

| Sex | 24h vs 0h | 48h vs 0h | 72h vs 0h | 168h vs 0h |
|---|---|---|---|---|
| Male | 3888 | 4133 | 1611 | 3053 |
| Female | 3173 | 4907 | 3647 | 1633 |

## Deviations / notes
- **Matrix:** the deposited matrices are DESeq2 median-ratio normalized counts from Partek Flow (non ... [807 more characters]
