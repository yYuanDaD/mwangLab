# Review packet B (the analysis' decisions): GSE124819

## Mechanical flags

- none

## Samples per design level

### `arm`
- **CL** (5): GSM3554477 / SCI+In-Cage Acitivity Group, Contusion S; GSM3554479 / SCI+In-Cage Acitivity Group, Contusion S; GSM3554482 / SCI+In-Cage Acitivity Group, Contusion S; GSM3554485 / SCI+In-Cage Acitivity Group, Contusion S; GSM3554487 / SCI+In-Cage Acitivity Group, Contusion S
- **CT** (9): GSM3554469 / SCI+Exercise Group, Contusion SCI + Tiny; GSM3554471 / SCI+Exercise Group, Contusion SCI + Tiny; GSM3554473 / SCI+Exercise Group, Contusion SCI + Tiny; GSM3554475 / SCI+Exercise Group, Contusion SCI + Tiny; GSM3554489 / SCI+In-Cage Activity Group, Contusion SC; GSM3554493 / SCI+In-Cage Activity Group, Contusion SC; GSM3554495 / SCI+In-Cage Activity Group, Contusion SC; GSM3554497 / SCI+In-Cage Activity Group, Contusion SC; GSM3554499 / SCI+In-Cage Activity Group, Contusion SC
- **NSstd** (5): GSM3554501 / SCI+In-Cage Activity Group, No SCI + Sta; GSM3554503 / SCI+In-Cage Activity Group, No SCI + Sta; GSM3554505 / SCI+In-Cage Activity Group, No SCI + Sta; GSM3554507 / SCI+In-Cage Activity Group, No SCI + Sta; GSM3554509 / SCI+In-Cage Activity Group, No SCI + Sta
- **NStiny** (4): GSM3554461 / SCI+Exercise Group, No SCI + Tiny Cage, ; GSM3554463 / SCI+Exercise Group, No SCI + Tiny Cage, ; GSM3554465 / SCI+Exercise Group, No SCI + Tiny Cage, ; GSM3554467 / SCI+Exercise Group, No SCI + Tiny Cage, 
- **SWIM** (5): GSM3554441 / SCI+Exercise Group, Contusion SCI + Swim; GSM3554442 / SCI+Exercise Group, Contusion SCI + Swim; GSM3554443 / SCI+Exercise Group, Contusion SCI + Swim; GSM3554444 / SCI+Exercise Group, Contusion SCI + Swim; GSM3554445 / SCI+Exercise Group, Contusion SCI + Swim
- **SWW** (5): GSM3554446 / SCI+Exercise Group, Contusion SCI + SWW ; GSM3554447 / SCI+Exercise Group, Contusion SCI + SWW ; GSM3554448 / SCI+Exercise Group, Contusion SCI + SWW ; GSM3554449 / SCI+Exercise Group, Contusion SCI + SWW ; GSM3554451 / SCI+Exercise Group, Contusion SCI + SWW 
- **TX** (4): GSM3554453 / SCI+Exercise Group, Complete Transection; GSM3554454 / SCI+Exercise Group, Complete Transection; GSM3554457 / SCI+Exercise Group, Complete Transection; GSM3554459 / SCI+Exercise Group, Complete Transection

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE124819"], "study_type": "Scientific Data data descriptor: liver RNA-seq resource; no differential-expression analysis, DEG counts, or threshold reported (S2.5, S4.3).", "primary_estimand": "Within chronic T2 contusion SCI rats, effect of exercise on the liver transcriptome: SWIM vs sedentary CONT (tiny cage) and SWW vs CONT (tiny cage) in the SCI + Exercise set (S1.p2, S1.p3, S2.2.p1, S2.2.p4); and effect of enhanced in-cage activity: CONT + Large cage vs CONT + Tiny cage in the SCI + In-Cage Activity set (S1.p3, S2.2.p1, S2.2.p3).", "sample_sets": {"SCI + Exercise (22 rats)": "No SCI 4, TX 4, CONT 4, CONT+SWIM 5, CONT+SWW 5; all tiny cages from 3 d post-injury (S2.2.p1, S2.2.p4)", "SCI + In-Cage Activity (15 rats)": "No SCI + Standard 5, CONT + Tiny 5, CONT + Large 5 (S2.2.p1, S2.2.p3)"}, "factors": {"sample_set": ["SCI + Exercise", "SCI + In-Cage Activity"], "arm": ["No SCI", "TX", "CONT", "CONT+SWIM", "CONT+SWW", "CONT+Large", "No SCI+Standard"]}, "inclusion": "All 37 samples deposited; paper suggests removing overlapping samples in PCA for future comparisons (S4.3) but specifies no exclusion rule.", "planned_contrasts": ["CONT+SWIM vs CONT (SCI + Exercise set; S1.p3, S4.3.p2; paper reports no DEG count)", "CONT+SWW vs CONT (SCI + Exercise set; S1.p3, S4.3.p2; paper reports no DEG count)", "CONT+Large vs CONT+Tiny (SCI + In-Cage Activity set; S1.p3, S4.3.p1; paper reports no DEG count)"], "repeated_measure_unit": "none; one liver per rat; rats doubly ho ... [505 more characters]

reasoning: Data descriptor (Sci Data). The stated objective (S1.p2) is how the chronic SCI liver profile is modified by in-cage activity and exercise; the two sample sets (S1.p3, S2.2.p1) define the exercise contrasts against sedentary CONT within each set. No DE test, DEG count, or threshold is reported, so the workflow default threshold applies and results are exploratory reproductions of the intended comparisons.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE124819\\GSE124819_GeneMatrix_RawCounts_ALL_UpdatedSampleNames_UpdatedCounts.txt.gz", "owned": true, "checks": ["S3.p1 names GSE124819", "37 samples = 37 in paper Table 1", "GEO tissue liver, female Sprague-Dawley, T2 SCI", "HTSeq Rn6 v93, 24,613 genes in both paper (S2.5.p1) and matrix"], "accession": "GSE124819", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE124819\\GSE124819_metadata.csv"}

reasoning: Paper S3.p1 deposits GSE124819; matrix has 24,613 gene rows and 37 samples matching Table 1 groups and replicate counts.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 37, "n_metadata": 37, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\d446594d1ade71b3541cb0f6a971599e29ccdf5a\\GSE124819\\aligned\\aligned_metadata.csv", "columns": {"set": {"source": "title", "regex": "^SCI\\+(Exercise|In-Cage) ", "recode": {"Exercise": "Ex", "In-Cage": "Ac"}}, "arm": {"source": "source_name_ch1", "regex": "^(.+)$", "recode": {"Contusion SCI + Tiny Cage": "CT", "Contusion SCI + Swim + Tiny Cage": "SWIM", "Contusion SCI + Sww + Tiny Cage": "SWW", "Contusion SCI + Large Cage": "CL", "No Injury + Standard Cage": "NSstd", "Complete transection SCI + Tiny Cage": "TX", "No Injury + Tiny Cage": "NStiny"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\d446594d1ade71b3541cb0f6a971599e29ccdf5a\\GSE124819\\aligned\\design_metadata.csv", "sha256": "a5a86a63d09c21ddc404338f30f7284edfe5c645e99625f64d8422e0c4fc9996", "levels": {"set": {"Ex": 22, "Ac": 15}, "arm": {"CT": 9, "SWIM": 5, "SWW": 5, "CL": 5, "NSstd": 5, "TX": 4, "NStiny": 4}}}}

reasoning: Matrix column names equal metadata title exactly (37/37). set from the title prefix (SCI+Exercise vs SCI+In-Cage Activity/Acitivity typo); arm from source_name_ch1. CONT + Tiny Cage occurs in both sets (4 + 5) and is kept separate by set.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\d446594d1ade71b3541cb0f6a971599e29ccdf5a\\GSE124819\\aligned\\aligned_matrix.csv", "sha256": "ca599d7b1f91eb1711b85b05fcfd865aedbdcd7520492490af389d0b7f874127", "n_features": 24613, "n_samples": 37, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 4118307.0, "median": 9.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer, max 4.1e6, median 9; GEO data_processing and paper S2.5.p1/S8.p7 state HTSeq-count read counts; file named GeneMatrix_RawCounts. Paper input to DESeq2 is the raw counts (S8.p9).

### design (valid, not_started)

final: {"analysis_type": "multi-group, stratified by sample set", "design_column": "arm", "contrasts": [{"name": "arm_SWIM_vs_CT_set-Ex", "control": "CT", "treatment": "SWIM", "role": "primary"}, {"name": "arm_SWW_vs_CT_set-Ex", "control": "CT", "treatment": "SWW", "role": "primary"}, {"name": "arm_CL_vs_CT_set-Ac", "control": "CT", "treatment": "CL", "role": "primary"}], "estimand_type": "causal (randomized arms within set)", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\d446594d1ade71b3541cb0f6a971599e29ccdf5a\\GSE124819\\suitability\\suitability.md", "n_comparisons": 13, "n_analyzable": 13}}

reasoning: Paper randomized animals to arms within each set (S2.2.p1). Exercise effect = exercised CONT vs sedentary CONT within the Exercise set; activity effect = Large vs Tiny cage CONT within the Activity set. Set is a stratum because the sets are separate experiments.

rejected alternatives: [{"value": "pool CONT+Tiny across both sets", "reason_rejected": "the two sets are separate experiments with different sequencing depth (~30M vs ~42M reads, Table 1) and different control housing; comparisons stay within set"}, {"value": "SWIM and SWW pooled as 'exercise'", "reason_rejected": "paper defines them as two distinct exercise paradigms (S1.p3); one model, separate contrasts"}, {"value": "injury contrasts (CT vs No SCI, TX vs CT)", "reason_rejected": "not exercise estimands; not run"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "cage (double housing with same-group partner, S2.2.p1)", "disposition": "not available in GEO; cannot be modelled; noted as caveat"}, {"name": "weeks post injury", "disposition": "GEO records 11.5 wk for all CONT arms in both sets; paper says exercised animals collected at 13.5 wk (S2.3.p1, S4.4.p1) - if so, time is part of the exercise arm by design and is not separable; caveat"}], "design_check": {"formula_equivalent": "~ C(arm)", "n_samples": 37, "n_columns": 7, "columns": ["Intercept", "arm_CT", "arm_NSstd", "arm_NStiny", "arm_SWIM", "arm_SWW", "arm_TX"], "rank": 7, "full_rank": true, "residual_df": 30, "levels": {"arm": {"CT": 9, "SWIM": 5, "SWW": 5, "CL": 5, "NSstd": 5, "TX": 4, "NStiny": 4}}, "cells": [{"cell": ["CL"], "n": 5}, {"cell": ["CT"], "n": 9}, {"cell": ["NSstd"], "n": 5}, {"cell": ["NStiny"], "n": 4}, {"cell": ["SWIM"], "n": 5}, {"cell": ["SWW"], "n": 5}, {"cell": ["TX"], "n": 4}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 37, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 37, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "cons ... [5300 more characters]

reasoning: Independent animals, one sample each; no batch or subject key within set. Separate sets handled as strata.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald), one cell-means model per sample set", "formula": "~ arm (within set)", "paper_route": {"method": "DESeq2 RLE normalization only", "status": "not_reported", "reason": "paper ran no DE test"}, "deviations": ["DE test is our addition; paper only normalized with DESeq2 RLE"]}

reasoning: Raw HTSeq counts; DESeq2 is consistent with the paper's DESeq2 RLE normalization (S8.p9). One model fitted on all samples of a set (including No SCI and TX in the Exercise set) for shared dispersion; planned contrasts extracted from it.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": null, "cutoff": null, "effect_metric": null, "effect_cutoff": null, "stated": false, "note": "data descriptor; no DE threshold"}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Data descriptor states no DE threshold; workflow default BH padj < 0.05, no fold-change cutoff."}

reasoning: No threshold in the paper (data descriptor).

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "exercise_set", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 22, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\d446594d1ade71b3541cb0f6a971599e29ccdf5a\\GSE124819\\results\\exercise_set\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\d446594d1ade71b3541cb0f6a971599e29ccdf5a\\GSE124819\\results\\exercise_set\\DEG_results_arm_SWIM_vs_CT_set-Ex.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\d446594d1ade71b3541cb0f6a971599e29ccdf5a\\GSE124819\\results\\exercise_set\\DEG_results_arm_SWW_vs_CT_set-Ex.csv"], "counts": {"exercise_set/arm_SWIM_vs_CT_set-Ex": {"applied": {"rule": "padj < 0.05", "n_tested": 13800, "n_significant": 121, "n_up": 62, "n_down": 59, "deg_sanity": "ok"}}, "exercise_set/arm_SWW_vs_CT_set-Ex": {"applied": {"rule": "padj < 0.05", "n_tested": 13800, "n_significant": 184, "n_up": 85, "n_down": 99, "deg_sanity": "ok"}}}}

reasoning: One DESeq2 cell-means model on all 22 SCI + Exercise samples; SWIM vs CONT and SWW vs CONT.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "activity_set", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 15, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\d446594d1ade71b3541cb0f6a971599e29ccdf5a\\GSE124819\\results\\activity_set\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\d446594d1ade71b3541cb0f6a971599e29ccdf5a\\GSE124819\\results\\activity_set\\DEG_results_arm_CL_vs_CT_set-Ac.csv"], "counts": {"activity_set/arm_CL_vs_CT_set-Ac": {"applied": {"rule": "padj < 0.05", "n_tested": 17544, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: One DESeq2 cell-means model on all 15 SCI + In-Cage Activity samples; Large vs Tiny cage CONT.

### study (valid, completed)

final: {"route": "exploratory", "caveats": ["Paper is a data descriptor with no DE results; DEG counts cannot be compared with the paper.", "Paper says exercised animals were collected 13.5 wk post-injury vs other CONT animals at 8.5/11.5 wk (S2.3.p1, S4.4.p1) while GEO lists 11.5 wk for all CONT arms; if the paper is right, exercise is inseparable from 2 extra weeks post-injury.", "Rats were doubly housed with same-group partners (S2.2.p1); cage effects cannot be modelled (no cage IDs), so arms may be pseudo-replicated by cage.", "Paper notes large within-group variability in the In-Cage Activity set and overlapping CONT+Tiny/CONT+Large samples (S4.3.p1)."], "results": {"exercise_set/arm_SWIM_vs_CT_set-Ex": {"n_deg": 121, "up": 62, "down": 59, "rule": "padj < 0.05"}, "exercise_set/arm_SWW_vs_CT_set-Ex": {"n_deg": 184, "up": 85, "down": 99, "rule": "padj < 0.05"}, "activity_set/arm_CL_vs_CT_set-Ac": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {}}

reasoning: Exploratory: intended contrasts reconstructed from a descriptor that did not test them.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference completed on 37 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "time of sacrifice for exercised animals",
    "paper": "8.5, 11.5 or 13.5 wk post-SCI depending on condition; exercised animals 13.5 wk (S2.3.p1, S4.4.p1)",
    "data": "GEO characteristics: 11.5 weeks post injury for all contusion arms incl. SWIM/SWW; TX 8.5 wk",
    "disposition": "executable_without_change"
  },
  {
    "item": "anesthesia in protocol",
    "paper": "ketamine/xylazine/acepromazine (S2.2.p2)",
    "data": "GEO treatment_protocol: pentobarbital",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE124819 (PMC6565704, PMID 31197156)

## What ran
- Case spec route (`case_spec.json`, `python -m tools.case_runner execute`); validator 11 records, 0 errors.
- Paper is a Scientific Data **data descriptor**: it deposits liver RNA-seq for two sample sets and only normalizes with DESeq2 RLE; it reports no DE test, DEG counts or threshold. The intended exercise comparisons (S1.p2, S1.p3, S2.2.p1) were reconstructed and run as **exploratory**.
- Matrix: HTSeq raw counts (`GSE124819_GeneMatrix_RawCounts_ALL_UpdatedSampleNames_UpdatedCounts.txt.gz`), 24,613 genes x 37 samples, exact alignment on `title` (37/37).
- Design: `arm` factor (reference CONT + tiny cage), stratified by sample `set` (SCI + Exercise vs SCI + In-Cage Activity; separate experiments with different depth). One DESeq2 (pydeseq2 Wald) cell-means model per set on all of that set's samples.
- Threshold: `workflow_default` BH padj < 0.05, no fold-change cutoff (paper states none).
- No enrichment (not requested by the paper).

## DEG counts (padj < 0.05)
| Contrast | Ours (up/down) | Paper |
|---|---|---|
| CONT+SWIM vs CONT (Exercise set) | 121 (62/59) | not reported |
| CONT+SWW vs CONT (Exercise set) | 184 (85/99) | not reported |
| CONT+Large vs CONT+Tiny cage (Activity set) | 0 | not reported |

## Deviations and caveats
- The DE test itself is our addition; the paper has no DE route to reproduce.
- Paper says exercised animals were collected at 13.5 wk post-SCI (S2.3.p1, S4.4.p1); GEO says 11.5 wk for all contusion arms. If the paper is right, exercise is inseparable from 2 extra weeks post-injury.
- Rats were doubly housed with same-group partners (S2.2.p1); no cage IDs, so cage effects cannot be modelled.
- GEO protocol names pentobarbital, paper ketamine/xylazine/acepromazine (recorded discrepancy, no effect on design).
- Paper notes large within-group variability and overlap of Large/Tiny samples in the Activity set (S4.3.p1), consistent with 0 DEGs there.

## Tool problems
- `tools/decision_contract.py:160` (and :191): `paper_threshold: null` is rejected ("must be an object") even with `threshold_source: workflow_default`; the case-spec docs do not say how to encode "paper states no threshold". Worked around with an object of nulls plus `"stated": false`.
- `tools/case_runner.py:873-875`: `finish.n_deg` / summary.csv `n_deg` holds only the first planned table (121) for a multi-contrast case; the other tables' counts appear only in the per-execution output.

