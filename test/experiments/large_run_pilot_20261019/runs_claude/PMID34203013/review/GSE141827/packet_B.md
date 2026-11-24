# Review packet B (the analysis' decisions): GSE141827

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the tissue level", "across": "tissue", "pairs_or_sets": 21, "samples_linked": 42, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"source_name_ch1": ["hindlimb"], "characteristics_ch1.1.protocol": ["unloading 24 hours", "unloading 3 days", "unloading 7 days", "unloading 7 days; recovery 24 hours", "unloading 7 days; recovery 3 days"]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the study is hindlimb unloading (disuse) and reloading into normal cage activity versus active cage controls (S2.2.p1). No group performs exercise training or an exercise bout, so the requested estimand (effect of exercise on gene expression) is not identifiable. Reloading R1/R3/R7 vs D7 would be recovery from disuse, not exercise, and was not run as a substitute.

## Samples per design level

### `protocol`
- **CTRL** (6): GSM4213783 / U6_EDL; GSM4213784 / U6_Sol; GSM4213785 / U7_EDL; GSM4213786 / U7_Sol; GSM4213787 / U8_EDL; GSM4213788 / U8_Sol
- **D1** (6): GSM4213782 / U24_Sol; GSM4213790 / U25_EDL; GSM4213791 / U25_Sol; GSM4213792 / U26_EDL; GSM4213793 / U26_Sol; GSM4213821 / U24_EDL
- **D3** (6): GSM4213789 / U10_Sol; GSM4213794 / U9_EDL; GSM4213795 / U9_Sol; GSM4213796 / U11_EDL; GSM4213797 / U11_Sol; GSM4213817 / U10_EDL
- **D7** (6): GSM4213798 / U1_EDL; GSM4213799 / U1_Sol; GSM4213800 / U2_EDL; GSM4213801 / U2_Sol; GSM4213802 / U3_Sol; GSM4213822 / U3_EDL
- **R1** (6): GSM4213803 / U18_EDL; GSM4213804 / U18_Sol; GSM4213805 / U20_EDL; GSM4213806 / U20_Sol; GSM4213807 / U21_EDL; GSM4213808 / U21_Sol
- **R3** (6): GSM4213809 / U4_Sol; GSM4213813 / U16_EDL; GSM4213814 / U16_Sol; GSM4213815 / U5_EDL; GSM4213816 / U5_Sol; GSM4213823 / U4_EDL
- **R7** (6): GSM4213810 / U12_EDL; GSM4213811 / U12_Sol; GSM4213812 / U13_Sol; GSM4213818 / U13_EDL; GSM4213819 / U19_EDL; GSM4213820 / U19_Sol

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE141827"], "assay": "nAnT-iCAGE (CAGE-seq), rat soleus and EDL (S2.6.p1)", "primary_estimand": "Effect of hindlimb unloading (disuse; 1, 3, 7 days) and subsequent reloading/recovery (free cage activity 1, 3, 7 days after 7-day unloading) versus active cage controls on TSS-peak / gene expression, separately in soleus and EDL (S2.2.p1, S2.7.8.p1)", "factors": {"protocol": ["control", "D1", "D3", "D7", "R1", "R3", "R7"], "tissue": ["soleus", "EDL"]}, "sample_inclusion": "21 Wistar rats, 3 per group, both muscles per rat (S2.1.p1, S2.2.p1)", "planned_contrasts": ["each phase (D1, D3, D7, R1, R3, R7) vs control, per muscle (S2.7.8.p1, FIG3; counts only in Figure 3A / ST4, not in text)", "time-course comparisons between consecutive phases (S3.3.p1, ST4C,D)"], "repeated_measure_unit": "rat (soleus and EDL from the same animal); muscles analysed separately", "paper_method": "DESeq2 on CAGE TSS peaks, peak-level; gene DE if any peak in gene is DE (S2.7.8.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.25, "source_locator": "S2.7.8.p1"}, "paper_results": "DEG counts per phase only in Figure 3A (not stated numerically in text); R1 soleus has the most DEGs (S3.3.p2)", "exercise_arm": "none: no exercise training or acute exercise bout; 'recovery' is release from tail suspension into normal cage activity (S2.2.p1)"}

reasoning: S2.2.p1 defines the U-experiment: tail-suspension unloading followed by reloading in the home cage, compared with active controls. S2.7.8.p1 gives DESeq2 on peaks with padj < 0.05 and |LFC| > 1.25. The intervention is disuse (and recovery from disuse), not exercise.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34203013\\prep\\GSE141827_peak_raw_counts.csv", "owned": true, "checks": ["S11.p1 names GSE141827", "metadata: 42 GSMs, rat soleus/EDL, 7 protocol levels x 3 rats x 2 muscles = paper design", "Level2 OSC table holds 42 raw.* columns whose sample labels equal metadata titles"], "accession": "GSE141827", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE141827\\GSE141827_metadata.csv"}

reasoning: Data availability statement S11.p1 links GSE141827; sample count and design match S2.2.p1.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 42, "n_metadata": 42, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34203013\\GSE141827\\aligned\\aligned_metadata.csv", "columns": {"tissue": {"alias_of": "characteristics_ch1.0.tissue", "recode": {"soleus muscle": "Sol", "EDL muscle": "EDL"}}, "protocol": {"alias_of": "characteristics_ch1.1.protocol", "recode": {"control": "CTRL", "unloading 24 hours": "D1", "unloading 3 days": "D3", "unloading 7 days": "D7", "unloading 7 days; recovery 24 hours": "R1", "unloading 7 days; recovery 3 days": "R3", "unloading 7 days; recovery 7 days": "R7"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34203013\\GSE141827\\aligned\\design_metadata.csv", "sha256": "4734cb743f3553d3ed858af0356c5a787119fc84d83d0b384f25d8b0968d00cf", "levels": {"tissue": {"Sol": 21, "EDL": 21}, "protocol": {"D1": 6, "CTRL": 6, "D3": 6, "D7": 6, "R1": 6, "R3": 6, "R7": 6}}}}

reasoning: Matrix columns raw.LaneN.<title>.<barcode> carry the GEO title (e.g. U24_Sol); the pattern strips lane and barcode and aligns exactly on title. Normalized (norm.*) columns were dropped by the prep script.

### matrix (valid, not_started)

final: {"source": "GSE141827_Level2_table.osc.txt.gz, raw.* columns (CAGE tag counts per DPI TSS peak; '##' OSC header lines stripped by prep_osc.py)", "paper_input": "CTSS peak counts into DESeq2 (S2.7.p1, S2.7.8.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34203013\\GSE141827\\aligned\\aligned_matrix.csv", "sha256": "f54c1e91decb724ddb5c3d2c5a5ea71e6c5ff2b7465d69ee787d4b9f6d66e016", "n_features": 9971, "n_samples": 42, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1809936.0, "median": 84.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: raw.* columns are integer CAGE tag counts per TSS peak (values like 63.0, 155.0); the file also has norm.* (TPM-like) columns, excluded. Features are peaks (L2__chr_strand_pos) without gene annotation, not genes. Matches the paper's peak-level DESeq2 input.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "protocol", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34203013\\GSE141827\\suitability\\suitability.md", "n_comparisons": 12, "n_analyzable": 12}}

reasoning: Paper-first: the paper's estimand is disuse-induced atrophy and recovery (title, S1.p2, S2.2.p1). The design is analyzable for that estimand (3 rats per phase per muscle) but contains no exercise arm, so the request's exercise estimand cannot be identified. Refused at design.

rejected alternatives: [{"value": "protocol R1/R3/R7 vs CTRL (paper's recovery phases)", "reason_rejected": "recovery from 7-day unloading versus active controls; estimand is residual disuse/reloading effect, not exercise"}, {"value": "protocol R1 vs D7 (reloading vs unloaded)", "reason_rejected": "return to normal ambulation after disuse; not an exercise intervention and not a paper-planned phase-vs-control comparison"}, {"value": "protocol D1/D3/D7 vs CTRL", "reason_rejected": "disuse (inactivity) effect; opposite o ... [44 more characters]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Rat') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "requested estimand",
    "paper": "disuse (hindlimb unloading) and recovery versus active control",
    "data": "same: 7 protocol levels (control, unloading 1/3/7 d, recovery 1/3/7 d) x soleus/EDL, no exercise group",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID34203013 / GSE141827

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
1. `python -m tools.case_runner inspect GSE141827 --data-root E:/agent/mwangLab_pdf/data` (data were already cached) → `inspect_GSE141827.json`.
2. `prep/prep_osc.py` (listed in `prep_scripts`): stripped the 139 `##` OSC header lines from `GSE141827_Level2_table.osc.txt.gz` and kept the 42 `raw.*` CAGE tag-count columns (dropped the `norm.*` columns and coordinates) → `prep/GSE141827_peak_raw_counts.csv` (9,971 TSS peaks × 42 samples).
3. `python -m tools.case_runner execute case_spec.json` → records for `paper_reconstruction`, `ownership`, `alignment` (exact on `title`, 42/42), `matrix` (raw counts, peak level), and `design` (refused). The validator reported 0 errors. The case route is `stopped`.

## Why it was refused
The paper (S2.2.p1) uses tail-suspension hindlimb **unloading** (disuse, 1/3/7 days) followed by **reloading**: the rats are released into their home cage after 7 days of unloading (recovery 1/3/7 days). These groups are compared with active cage controls, with soleus and EDL analysed separately. No group does exercise training or an acute exercise bout. The paper's estimand is disuse atrophy and recovery from it, so an exercise effect cannot be identified from these data. I considered recovery vs control, R1 vs D7 (reloading) and unloading vs control as alternatives and rejected all three (see `design.candidates`). The design itself is analyzable for the paper's own estimand: the suitability report lists 12 analyzable comparisons, 6 phases × 2 muscles, with n = 3 per group.

## DEG counts vs the paper
- None were computed, because the case was refused.
- Paper threshold (S2.7.8.p1): DESeq2 on TSS peaks, BH padj < 0.05 and |LFC| > 1.25. A gene counts as DE if any of its peaks is DE.
- The paper gives its per-phase DEG counts only graphically (Figure 3A, Supplementary ST4). The text states no number; it says only that soleus R1 has the most DEGs.

## Deviations
- The matrix was repaired by a prep script (header stripped, `raw.*` columns selected). Nothing else deviates, since no model was fitted.
- The deposited Level2 table is peak-level with no gene annotation. Even for the paper's own estimand, the paper's peak-to-gene DEG rule would need an annotation step (Ensembl v93 gene regions ±200 nt) that the runner does not have.

## Tool problems
- `case_runner inspect` profiled the `.osc.txt.gz` file wrongly:
  - Its `feature_exa ... [762 more characters]
