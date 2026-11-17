# Review packet B (the analysis' decisions): GSE219099

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.2.treatment level", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the only factor is miR-486 mimic vs scramble miRNA transfection in C2C12 myoblasts (S2.8.p1). It tests a miRNA's effect in vitro, not exercise, so it cannot answer how exercise affects gene expression.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE219100 (SuperSeries)", "GSE219099 (C2C12 miR-486 mimic vs scramble)"], "assay": "poly-A RNA-seq of C2C12 mouse myoblasts (STAR mm10, raw counts)", "primary_estimand": "miR-486 mimic vs scramble miRNA transfection in C2C12 myoblasts (S2.8.p1, S3.3.p2) - a mechanistic follow-up, not an exercise contrast", "planned_contrasts": ["miR-486 mimic vs scramble (S3.3.p2, FIG3; DEG count only in Supp Table S2)"], "paper_threshold": {"metric": "not_reported", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.3.p2"}, "paper_method": "not_reported for the C2C12 data (S2.9.p2 describes the miRNA analysis only)"}

reasoning: S2.8.p1 and S3.3.p2: C2C12 cells transfected with a miR-486 mimic or scramble control; no exercise factor. The request is the exercise effect.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE219099\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["series_id = GSE219099,GSE219100 (sub-series of the SuperSeries named in S2.8.p1/DA.p1)", "6 samples: 3 scramble control, 3 miR-486 mimic; C2C12; HiSeq, matching S2.8.p1"], "accession": "GSE219099", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE219099\\GSE219099_metadata.csv"}

reasoning: Sub-series of GSE219100 holding the C2C12 experiment described in S2.8.p1.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE219099\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.2.treatment", "recode": {"Control scramble miRNA": "scr", "miR-486": "mir486"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE219099\\aligned\\design_metadata.csv", "sha256": "a3aff7c7b700545b0d6d3f9e2c3ba1087215237fb09ad0c7c8b19e65e6f30730", "levels": {"grp": {"scr": 3, "mir486": 3}}}}

reasoning: Tar columns become GSM ids; exact match on the metadata index (6/6).

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE219099\\aligned\\aligned_matrix.csv", "sha256": "90fdc63c2f0b290d28aafd3800a6701080e628aad9f7f61abf3ec1aa2ac23553", "n_features": 54532, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 234863.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Integer values, Ensembl mouse gene ids; data_processing: STAR mm10 alignment, raw counts.

### design (refused, not_started)

final: {"suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE219099\\suitability\\suitability.md", "n_comparisons": 0, "n_analyzable": 0}}

reasoning: S2.8.p1, S3.3.p2; metadata treatment = 'Control scramble miRNA' / 'miR-486' only.

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/0 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[]

## HANDBACK.md (start)

# HANDBACK: PMID 36620222 (PMC9811128)

**Run label:** PMID36620222  
**Decision maker:** Claude Code session (claude-opus-5-5) using the bioinformatics-workflow skill, case-spec route.  
**Spec:** `case_spec.json`. **Runner output:** `_execute_out.json`, `case_runner.log`, `summary.csv`. The decision contract validator passed: 20 records, 0 errors. The first attempt is kept in `_previous/`.

## What ran

| Case | Outcome | Why |
|---|---|---|
| GSE218103: plasma-EV small RNA-seq, human, 12 pooled samples | **completed**, paper_aligned | This is the only accession that contains an exercise contrast. |
| GSE219099: C2C12 cells, miR-486 mimic vs scramble, mouse, 6 samples | **refused at design** | No exercise factor. It is an in-vitro test of what one miRNA does. |
| GSE219100: SuperSeries of the two above, 18 samples | **refused at design** | Its samples are the union of GSE218103 (human miRNA) and GSE219099 (mouse mRNA). No single design spans the two species and assays, and its exercise contrast is the same as GSE218103's. |

### GSE218103: decisions
- **Sample groups.** In GEO, "CON" (treatment: control) means the **pre-exercise sample**, not the paper's separate TD CON no-exercise group. Evidence: only TD EX and CP EX were sequenced, as 3 pools per timepoint (S2.6.p1); the study has no "CP CON" group (S2.1.p1); and treatment_protocol reads "before and 30 minutes after a bout". So CON is pre and EX is post.
- **Model.** One DESeq2 model (pydeseq2) over the 4 genotype x time cells, 3 pools per cell. This matches the paper's genotype + activity model (S2.9.p2).
  - Planned: post vs pre within TD; post vs pre within CP.
  - Associational: CP vs TD at pre; CP vs TD at post.
  - Exploratory: the genotype x time interaction.
- **Low-count filter.** "MicroRNAs with less than 10 counts were removed" was read as a row total of at least 10 across the 12 samples. It was encoded as `min_mean_count` 0.8333 and keeps 298 of 399 miRNAs.
- **Covariance.** No pool blocking. The pre and post pools come from the same participants, but GEO does not say which pre pool matches which post pool. The pre/post correlations do not peak on matching indices, and the paper's model has no pool term. Ignoring this positive pairing makes the exercise tests conservative. It is recorded as a caveat and was not guessed.
- **Threshold.** The paper's own rule (S2.9.p2): BH-adjusted p < 0.05, no fold-change cutoff. Raw p < 0.05 is reported only as a labelled audit count.
- **Enrichment.** Not ... [2552 more characters]
