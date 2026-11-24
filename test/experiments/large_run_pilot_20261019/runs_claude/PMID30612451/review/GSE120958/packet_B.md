# Review packet B (the analysis' decisions): GSE120958

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.2.diet", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: GSE120958 contains only normal- vs high-phosphate diet gastrocnemius samples (3 vs 3), all of unstated/non-exercised state. Exercise in the paper is a phenotypic outcome (treadmill capacity), not a factor of the sequenced design, so the data cannot identify an effect of exercise on gene expression.

## Samples per design level

### `grp`
- **HP** (3): GSM3422125 / HP_1; GSM3422126 / HP_2; GSM3422127 / HP_3
- **NP** (3): GSM3422122 / NP_1; GSM3422123 / NP_2; GSM3422124 / NP_3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE120958"], "assay": "bulk RNA-seq (Illumina HiSeq 2500), mouse gastrocnemius", "primary_estimand": "Effect of 12-week high-phosphate diet (2% Pi, HP) vs normal-phosphate diet (0.6% Pi, NP) on gastrocnemius gene expression (S4.4.p1, FIG5). Exercise is a phenotypic outcome (treadmill capacity, S4.2.p2), not a factor of the RNA-seq design.", "factors": {"diet": ["NP (control)", "HP"]}, "sample_inclusion": "n = 3 per diet group, male C57BL/6, 20-24 weeks old (FIG5, S2.2.p1); no exercise state is stated for the sequenced animals; related mitochondria assays are explicitly from non-exercised mice (FIG4 legend)", "planned_contrasts": ["HP vs NP diet (S4.4.p1, FIG5; paper: 'over 5,000' DEGs)"], "repeated_measure_unit": null, "paper_method": "DESeq2 (v1.6.3) ~ diet (FIG5; GEO data_processing)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "effect_inclusive": true, "source_locator": "FIG5"}, "paper_results": "over 5,000 DEGs HP vs NP (S4.4.p1); down: Fabp4, Fabp5, Lipe (Hsl), Fasn, Pparg, Adipoq, Pnpla3; up: Gck, Hk2, Pgk1, Irs2, Ldha, Slc2a4 (Glut4)", "exercise_contrast_in_rnaseq": false}

reasoning: S2.13.p1 deposits GSE120958 for muscle RNA-seq. S4.4.p1/FIG5 analyze HPD vs normal chow (n=3/group) with DESeq2, 'cutoff values of +/-1.5 fold change and P < 0.05' (raw P stated). Exercise appears only as treadmill phenotyping (S2.7, S4.2) and blood measures; no RNA-seq arm is exercised vs sedentary.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE120958\\GSE120958_countTable.txt.gz", "owned": true, "checks": ["S2.13.p1 names GSE120958", "GEO: gastrocnemius, C57BL/6, 12-week diet, 3 NP + 3 HP matches FIG5 n=3/group", "treatment_protocol_ch1 text matches S2.2.p1"], "accession": "GSE120958", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE120958\\GSE120958_metadata.csv"}

reasoning: Paper names the accession; tissue, strain, diet doses and group sizes agree.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30612451\\GSE120958\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(NP|HP)_\\d+$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30612451\\GSE120958\\aligned\\design_metadata.csv", "sha256": "dd4d53490a4503fd4e0a0ca4919164de7826ee07aaf43a36c4b9af093416601e", "levels": {"grp": {"NP": 3, "HP": 3}}}}

reasoning: Matrix columns NP_1..HP_3 equal metadata title exactly (6/6). grp derived from title; agrees with characteristics diet column.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30612451\\GSE120958\\aligned\\aligned_matrix.csv", "sha256": "cdbb63571d0da705e8a7eaaede27c230e2a07e57900aec0ba51f40d09595e42d", "n_features": 47967, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1542449.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: GSE120958_countTable.txt.gz is 100% integer, max 1.5e6; data_processing: featureCounts quantification, 'Tab-delimited text files include raw counts and FPKM values'. Paper input to DESeq2 is raw counts, consistent.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "grp", "exercise_contrast_available": false, "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30612451\\GSE120958\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Request asks how exercise affects gene expression. S4.4.p1/FIG5: the only RNA-seq comparison is HPD vs normal chow; GEO grouping column is diet only (normal phosphate 3, high phosphate 3); diet time 12 weeks constant. No exercise arm, no pre/post exercise timepoint.

rejected alternatives: [{"value": "grp_HP_vs_NP as an exercise contrast", "reason_rejected": "This is a dietary phosphate contrast, not exercise; neither arm is exercised or trained and no exercise-state variable exists in GEO or the paper's RNA-seq description. Relabelling diet as 'exercise intolerance' would misstate the estimand."}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "exercise factor",
    "paper": "Title/abstract emphasise exercise intolerance; RNA-seq contrast is diet only (S4.4.p1)",
    "data": "GEO has only diet factor (NP/HP)",
    "disposition": "blocks_requested_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID30612451 / GSE120958

**Status: refused at `design`** (decision_status `refused`, execution `not_run`). The contract validator ran on 5 records and reported 0 errors.

## What ran
- `case_runner inspect GSE120958`: downloaded the series to `data/GSE120958`. It has two matrices: raw counts (`GSE120958_countTable.txt.gz`, 100% integer) and FPKM. There are 6 samples, NP_1-3 and HP_1-3.
- `case_runner execute case_spec.json`: recorded these gates:
  - `paper_reconstruction`
  - `ownership`: owned.
  - `alignment`: exact match on `title`, 6/6 samples.
  - `matrix`: raw counts, so DESeq2 would be the method.
  - `design`: refused.
- The suitability report found the diet contrast HP vs NP analyzable. That contrast is not the requested estimand.

## Why it was refused
The request was how exercise affects gene expression. GSE120958 contains only a dietary phosphate contrast:
- 12 weeks of high-phosphate diet (2% Pi) vs normal-phosphate diet (0.6% Pi).
- Gastrocnemius muscle, n=3 per group (S4.4.p1, FIG5).

In the paper, exercise is a phenotypic outcome (treadmill VO2 and duration, S4.2.p2), not a factor of the sequenced design. No arm is exercised or trained, there is no pre/post-exercise sample, and GEO has no exercise variable. Running HP vs NP as an "exercise" comparison would misstate the estimand.

## DEG counts vs the paper
- Not run, so there are 0 contrasts to compare.
- The paper reports "over 5,000" DEGs for HP vs NP using DESeq2 with |FC| ≥ 1.5 and raw P < 0.05 (FIG5). That rule is recorded as `paper_threshold`: pvalue < 0.05 and |log2FC| ≥ 0.5849625.
- Genes the paper names:
  - Down: Fabp4, Fabp5, Lipe (Hsl), Fasn, Pparg, Adipoq, Pnpla3.
  - Up: Gck, Hk2, Pgk1, Irs2, Ldha, Slc2a4.

## Deviations
None. No analysis was run.

## Tool problems
None. Inspect, the runner and the validator all behaved as expected.

