# Review packet B (the analysis' decisions): GSE250520

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.3.treatment", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: GSE250520 contains only vehicle vs IL-1beta cardiac organoids (no exercise, training, or NE/stress-test arm). The paper's 'simulated exercise' (NE stress test, S2.6.p2) is a functional beating-rate assay without RNA-seq, so the requested exercise estimand cannot be identified from these data. IL-1beta vs vehicle is not an exercise comparison and was not run as a substitute.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE250520"], "assay": "bulk RNA-seq of human cardiac organoids (hPSC-CM/hcFB/HUVEC/hADSC), n=3 vehicle vs n=3 IL-1beta, day 4 of treatment", "primary_estimand": "Transcriptomic effect of 4-day IL-1beta stimulation vs vehicle in human cardiac organoids (COVID-19 cytokine-storm model). No exercise estimand: the only 'simulated exercise' is a functional norepinephrine stress test (beating rate/FAC, S2.6.p2, FIG7d-g) that has no transcriptome.", "planned_contrasts": ["IL-1beta vs control hCOs (S2.1.p2, FIG2d volcano; paper DEG count not stated)"], "exercise_contrast_in_paper": "none for RNA-seq; NE 'stress test to simulate physiological exercise' is beating-rate only (S2.6.p2)", "factors": {"treatment": ["vehicle", "IL-1beta"]}, "sample_inclusion": "3 vs 3 organoid pools (FIG3b n=3)", "repeated_measure_unit": "none; single hiPSC-CM donor line", "paper_threshold": {"metric": null, "cutoff": null, "effect_metric": null, "effect_cutoff": null, "stated": false, "source_locator": "S5.p2 (only generic p<0.05 t-test rule for non-omics assays); FIG2d gives no DEG rule"}, "paper_method": "not stated for RNA-seq; Median-of-Ratios normalization (FIG3c) suggests DESeq2", "paper_results": "IL1R1 up in IL-1beta hCOs (S2.1.p2); ADRB2 up, ADRB1 unchanged (S2.6.p2)"}

reasoning: Abstract ABS.p1 mentions 'simulated exercise conditions'; the only such experiment is the NE stress test in S2.6.p2/FIG7, a functional readout. RNA-seq (S2.1.p2) compares IL-1beta vs vehicle only. Methods S5 give no RNA-seq pipeline or DEG threshold.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE250520\\GSE250520_il1b_rawcounts_041621.csv", "owned": true, "checks": ["GEO contact Dimitrios Arhontoulis, Mei lab, MUSC = first/senior authors (S6.p1)", "cardiac organoids, IL1B 4 days = paper's regimen (S5.p1)", "3 Vehicle + 3 IL1b samples = paper n=3 (FIG3b)", "DA.p1 promised GEO deposit; GSE250520 public Dec 2023"], "accession": "GSE250520", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE250520\\GSE250520_metadata.csv"}

reasoning: Series metadata and files match the paper's authors, model, treatment and sample count.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35689600\\GSE250520\\aligned\\aligned_metadata.csv", "columns": {"trt": {"alias_of": "characteristics_ch1.3.treatment", "recode": {"control": "VEH", "IL-1 cytokine": "IL1B"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35689600\\GSE250520\\aligned\\design_metadata.csv", "sha256": "d44ad5774f5e8d4c210de2350108d149d6a9579338fee083193e68a3a558dc5b", "levels": {"trt": {"VEH": 3, "IL1B": 3}}}}

reasoning: Matrix columns Vehicle.1..IL1bOrgs.3 sit inside the GEO title after 'cardiac organoids, '; exact match on the derived key. Treatment column recoded to formula-safe trt.

### matrix (valid, not_started)

final: {"source": "GSE250520_il1b_rawcounts_041621.csv", "paper_input": "not stated; FIG3c uses median-of-ratios values, consistent with DESeq2 on counts", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35689600\\GSE250520\\aligned\\aligned_matrix.csv", "sha256": "03b9c7a3d659f2e6a7e3eeafdf7cdfbaa8ed506abcf820c3e949a2d2d50ee4ee", "n_features": 60608, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 6, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 831330.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 831330; data_processing: STAR + htseq-count. The other file is DESeq2 median-of-ratios normalized (non-integer).

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": null, "contrasts": [], "exercise_factor_present": false, "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35689600\\GSE250520\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Only grouping column is treatment (control 3, IL-1 cytokine 3); all other fields constant. No time, NE, or exercise factor exists in metadata or matrix columns.

rejected alternatives: [{"value": "trt IL1B vs VEH", "reason_rejected": "cytokine-storm treatment, not exercise; answering it would substitute a different estimand"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "exercise",
    "paper": "abstract mentions reversibility 'at baseline and simulated exercise conditions' (ABS.p1); NE stress test D4/D14 (S2.6.p2)",
    "data": "GEO series has only D4 vehicle vs IL-1beta RNA-seq; no NE or D14 samples",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID35689600 / GSE250520

**Status: refused at `design`** (decision_status `refused`, route `stopped`). The validator reported 0 errors across 5 records.

## What ran
- `python -m tools.case_runner inspect GSE250520` used the cached data in `E:/agent/mwangLab_pdf/data/GSE250520`.
- I read the paper (PMC9350263.paper.md): ABS.p1, S2.1.p2, S2.6.p2, S5.p1–p2, DA.p1.
- `case_spec.json` recorded these gates: paper_reconstruction → ownership → alignment → matrix → design (refused). `execute` completed.
- Alignment was an exact match on a key taken from the GEO title (`^cardiac organoids, (.+)$`). All 6 samples matched (6/6): VEH 3, IL1B 3. Suitability: analyzable for IL1B vs VEH, but that is not an exercise contrast.
- No DE executions and no enrichment were run.

## Why refused
- The RNA-seq in GSE250520 covers only 3 vehicle and 3 IL-1β organoid pools, at day 4 of treatment (COVID-19 cytokine-storm model).
- The paper's "simulated exercise" is a norepinephrine stress test (S2.6.p2, FIG7d–g). It measures beating rate and FAC only, and there is no transcriptome for it. GEO has no NE, D14 or exercise samples.
- No exercise estimand can be identified from these data. I deliberately did not run IL-1β vs vehicle as a substitute.

## DEG counts vs paper
- None computed.
- The paper gives no DEG count and no RNA-seq DEG threshold. It shows only the volcano plot in FIG2d. S5.p2 gives a generic t-test rule of p<0.05 for the non-omics assays.
- I recorded the paper threshold as "not stated".

## Deviations
None. The case stopped before any method was chosen.

## Tool problems / observations
- `data/GSE250520/GSE250520_il1b_rawcounts_041621.csv`, line 2: the xlsx→csv conversion kept a second header row as a data row. It holds `EnsembleID` and fastq names. Inspect still reported `integer_fraction 1.0` but also `missing_values: 6`, and listed `EnsembleID` as a feature ID. The matrix profile does not flag a non-numeric data row. If this matrix is ever used, it needs a prep script that drops that row. This did not affect the refusal.
- Nothing else to report.

