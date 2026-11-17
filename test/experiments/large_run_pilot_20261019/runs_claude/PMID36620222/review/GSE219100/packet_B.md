# Review packet B (the analysis' decisions): GSE219100

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.2.treatment level", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 9, "samples_linked": 18, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"title": ["Cerebral palsy exercise 1", "Cerebral palsy exercise 2", "Cerebral palsy exercise 3", "Typically developed exercise 1", "Typically developed exercise 2"], "characteristics_ch1.1.group": ["CP EX", "TD EX"], "characteristics_ch1.2.treatment": ["aerobic exercise"], "treatment_protocol_ch1": ["Blood was collected before and 30 minutes after a bout of aerobic exercise"]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm): SuperSeries: its samples are the union of GSE218103 (human EV miRNA, exercise) and GSE219099 (mouse C2C12, no exercise). No single design spans two species and assays; the exercise contrast is identical to and analysed in case GSE218103, so re-running it here would duplicate it.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE219100 (SuperSeries of GSE218103 + GSE219099)"], "primary_estimand": "Exercise effect on EV miRNA cargo (analysed in case GSE218103) plus the non-exercise C2C12 miR-486 experiment (case GSE219099)", "planned_contrasts": ["see cases GSE218103 and GSE219099"], "paper_threshold": {"metric": "FDR", "adjustment": "BH", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "inclusive": false, "source_locator": "S2.9.p2"}}

reasoning: S2.6.p1, S2.8.p1 and DA.p1 cite GSE219100 for both experiments.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE219100\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["18 samples = the 12 GSE218103 EV samples (Homo sapiens) + the 6 GSE219099 C2C12 samples (Mus musculus); series_id lists each sub-series"], "accession": "GSE219100", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE219100\\GSE219100_metadata.csv"}

reasoning: The paper's own SuperSeries; every sample also belongs to one of the two sub-series.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 18, "n_metadata": 18, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE219100\\aligned\\aligned_metadata.csv", "columns": {}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE219100\\aligned\\design_metadata.csv", "sha256": "f5b22d994c5abdb535769aef942a407200f03262907569ad3dfe712ab980b992", "levels": {}}}

reasoning: Tar columns become GSM ids; exact match on the metadata index (18/18).

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE219100\\aligned\\aligned_matrix.csv", "sha256": "94442f967c50be3d6de16db5fafc192f72f14858eabd164db651ba6446e4a84c", "n_features": 54931, "n_samples": 18, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 234863.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Integer counts, but the merged tar matrix stacks human miRNA counts (12 EV samples) and mouse Ensembl gene counts (6 C2C12 samples) - two assays and species in one table, each valid only within its sub-series.

### design (refused, not_started)

final: {"suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE219100\\suitability\\suitability.md", "n_comparisons": 0, "n_analyzable": 0}}

reasoning: series_id, organism_ch1 and source_name_ch1 split the 18 samples exactly into the two sub-series.

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/0 comparisons have >= 3 per group |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
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
