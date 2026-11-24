# Review packet B (the analysis' decisions): GSE156174

## Mechanical flags

- **unused_subject_like_column**: {"column": "dur", "n_values": 3, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "grp", "across": "source_name_ch1", "pairs_or_sets": 4, "samples_linked": 8, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"title": ["14wk hindlimb unloaded MSC", "14wk hindlimb unloaded SSC", "8wk hindlimb unloaded MSC", "8wk hindlimb unloaded SSC", "hindlimb unloaded+recovery"]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm, sample_size): No exercise contrast and no replication: (1) the intervention is hindlimb unloading/disuse and reloading, with no exercise or training arm; (2) every arm (cell type x treatment x duration) is ONE library of RNA pooled from 3-4 mice (S4.7.p1), so each comparison is n=1 vs n=1 with zero residual degrees of freedom. Between-sample variance cannot be estimated; the paper's 3991/1504 DEGs come from an edgeR exact test with an assumed dispersion of 0.2 (S4.8.p1), a fixed assumption rather than inference. No valid DE model exists for these data.

## Samples per design level

### `grp`
- **AMBR_w16** (1): GSM4726015 / recovery ambulatory
- **AMB_w14** (2): GSM4726010 / 14wk ambulatory MSC; GSM4726011 / 14wk ambulatory SSC
- **AMB_w8** (2): GSM4726006 / 8wk ambulatory MSC; GSM4726007 / 8wk ambulatory SSC
- **HUR_w16** (1): GSM4726014 / hindlimb unloaded+recovery
- **HU_w14** (2): GSM4726012 / 14wk hindlimb unloaded MSC; GSM4726013 / 14wk hindlimb unloaded SSC
- **HU_w8** (2): GSM4726008 / 8wk hindlimb unloaded MSC; GSM4726009 / 8wk hindlimb unloaded SSC

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE156174"], "assay": "bulk RNA-seq (NextSeq 500, HISAT2/featureCounts mm9), mouse bone-marrow Lin-LEPR+ SSCs (FACS) and immuno-depleted cultured MSCs", "primary_estimand": "Effect of hindlimb unloading (HU, mechanical disuse) vs ambulatory (AMB) controls on SSC and MSC transcriptomes at 8wk and 14wk; plus SSC transcriptome after 8wk HU + 8wk reloading (HUR) vs age-matched AMB", "factors": {"cell_type": ["SSC", "MSC"], "treatment": ["AMB", "HU", "HUR"], "duration": ["8wk", "14wk", "8wk+8wk reload"]}, "sample_inclusion": "One pooled RNA library per group: RNA pooled from 3-4 mice per group (S2.4.p1, S4.2.p1, S4.2.p2, S4.7.p1); 10 libraries total, no biological replicates", "planned_contrasts": ["8wk HU vs AMB in SSC (S2.4.p1; paper: 3991 DEGs)", "8wk HU vs AMB in MSC (S2.4.p1; paper: 1504 DEGs)", "14wk HU vs AMB in SSC and MSC (S2.5.p2; counts only in Supplementary Fig. 5d,e, 'fewer than 8wk')", "HUR vs AMB SSC pseudo-time K-means clustering (S2.6.p2-p3; no DEG count)"], "repeated_measure_unit": "none (pools of different mice per group)", "paper_method": "edgeR exact test with a FIXED dispersion of 0.2 (no replicates to estimate dispersion), TMM calcNormFactors, filter sum of counts > 2, protein-coding transcripts only (S4.8.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S4.9.p1 (general 'p <= 0.05'); DEG rule for RNA-seq not stated in S4.8.p1; Fig. 3c-e highlight Log2FC > 2", "sta ... [97 more characters]

reasoning: The intervention is hindlimb unloading (disuse, the opposite of mechanical loading/exercise) and reloading recovery; there is no exercise arm. Every group is a single library of RNA pooled from 3-4 mice (S4.7.p1). The paper fitted edgeR exactTest with a dispersion fixed at 0.2 because no replicate exists (S4.8.p1). The DEG threshold for RNA-seq is not stated.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34836964\\GSE156174\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["S8.p1 names GSE156174", "GEO samples = 10 libraries matching S2.4-S2.6 groups (8wk/14wk AMB/HU x SSC/MSC + HUR + recovery AMB SSC)", "data_processing: HISAT2 + featureCounts mm9, raw transcript counts = S4.8.p1"], "accession": "GSE156174", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE156174\\GSE156174_metadata.csv"}

reasoning: Paper's code-availability statement names GSE156174; sample groups and processing match.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 10, "n_metadata": 10, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34836964\\GSE156174\\aligned\\aligned_metadata.csv", "columns": {"cell": {"alias_of": "characteristics_ch1.2.cell type", "recode": {"flow sorted SSCs": "SSC", "depleted MSCs": "MSC"}}, "trt": {"alias_of": "characteristics_ch1.3.treatment", "recode": {"AMB": "AMB", "HU": "HU", "HU+recovery": "HUR", "recovery AMB": "AMBR"}}, "dur": {"alias_of": "characteristics_ch1.4.duration", "recode": {"8 weeks": "w8", "14 weeks": "w14", "8 weeks + reloaded": "w16", "Reloading control": "w16"}}, "grp": {"combine": ["trt", "dur"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34836964\\GSE156174\\aligned\\design_metadata.csv", "sha256": "4d1b97d3be3f5e76cf86ab43b5a8ce6160dbd176abe2b79ad371dc3f01ed71cb", "levels": {"cell": {"SSC": 6, "MSC": 4}, "trt": {"AMB": 4, "HU": 4, "HUR": 1, "AMBR": 1}, "dur": {"w8": 4, "w14": 4, "w16": 2}, "grp": {"AMB_w8": 2, "HU_w8": 2, "AMB_w14": 2, "HU_w14": 2, "HUR_w16": 1, "AMBR_w16": 1}}}}

reasoning: Tar-merged columns become GSM ids; exact match on metadata index (inspect: 10/10).

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34836964\\GSE156174\\aligned\\aligned_matrix.csv", "sha256": "28efd894eebec1fda0b7815377bade549018e5685b843d6776270760c4826eb0", "n_features": 95883, "n_samples": 10, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1801473.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Integer fraction 1.0, max 1.8e6; GEO data_processing 'featurecount ... raw transcript counts'; features are Ensembl transcript IDs (ENSMUST), matching the paper's transcript-level edgeR input (S4.8.p1).

### design (refused, not_started)

final: {"analysis_type": "two-group per cell type and duration (as paper)", "design_column": "grp", "contrasts": [{"name": "grp_HU_w8_vs_AMB_w8_cell-SSC", "control": "AMB_w8", "treatment": "HU_w8", "role": "primary"}, {"name": "grp_HU_w8_vs_AMB_w8_cell-MSC", "control": "AMB_w8", "treatment": "HU_w8", "role": "primary"}], "suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34836964\\GSE156174\\suitability\\suitability.md", "n_comparisons": 21, "n_analyzable": 0}}

reasoning: S4.7.p1, S2.4.p1 (pooled BM N=3 mice), S4.8.p1 (dispersion 0.2). GEO has exactly one sample per group.

rejected alternatives: [{"value": "HUR vs recovery AMB (reloading as a 'loading' contrast)", "reason_rejected": "n=1 vs n=1 pooled SSC library; reloading is recovery from disuse, not exercise"}, {"value": "pool durations (8wk+14wk) as replicates of HU vs AMB within cell type", "reason_rejected": "changes the estimand (duration and age differ; the paper treats them as separate cohorts; 14wk MSC libraries used total-RNA prep vs poly-A for all others, S4.7.p1) and still gives n=2 vs 2"}, {"value": "edgeR exactTest with f ... [233 more characters]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/21 comparisons have >= 3 per group |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "replication",
    "paper": "3991/1504 DEGs reported as differential expression",
    "data": "one pooled library per group; edgeR dispersion fixed at 0.2",
    "disposition": "blocks_estimand"
  },
  {
    "item": "exercise",
    "paper": "hindlimb unloading (disuse) and reloading",
    "data": "no exercise/training arm",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID34836964 / GSE156174

**Status: refused at `design`** (decision_status `refused`, execution `not_run`). Validator: 5 records, 0 errors.

## What ran
- `case_runner inspect GSE156174`: downloaded the series and merged `GSE156174_RAW.tar` into a 95,883 transcript (ENSMUST) × 10 sample integer matrix. GEO `data_processing` says featureCounts raw transcript counts.
- `case_runner execute case_spec.json`: recorded `paper_reconstruction` → `ownership` → `alignment` (exact match on metadata index, 10/10) → `matrix` (raw counts) → `design` (refused). The suitability report (`GSE156174/suitability/suitability.md`) gave the verdict `not_analyzable` because of `sample_size`: 0 of 21 comparisons can be analyzed.

## Why I refused
1. **No exercise arm.** The intervention is hindlimb unloading (HU, mechanical disuse) for 8 or 14 weeks, plus 8 weeks of reloading after 8 weeks of HU (HUR). Ambulatory (AMB) mice are the controls. There is no exercise or training arm.
2. **No replication.** Each group (cell type × treatment × duration) is a single library of RNA pooled from 3–4 mice (S4.7.p1, S2.4.p1). Every contrast is therefore 1 vs 1, with zero residual degrees of freedom. The paper ran an edgeR exact test with the dispersion **fixed at 0.2** (S4.8.p1). Its DEG counts come from that assumed constant, not from variance estimated in the data.

Alternatives I rejected (recorded in the design candidates):
- HUR vs recovery AMB: also 1 vs 1.
- Pooling 8wk and 14wk as replicates: this changes the estimand, because age and duration differ and the 14wk MSC libraries were total-RNA preps while the rest were poly-A. It would still give only 2 vs 2.
- Re-running the fixed-dispersion edgeR: no executor supports it, and the result would be an assumption rather than an estimate.

## DEG counts vs paper
| Contrast | Ours | Paper |
|---|---|---|
| 8wk HU vs AMB, SSC | not run (refused) | 3991 (S2.4.p1) |
| 8wk HU vs AMB, MSC | not run (refused) | 1504 (S2.4.p1) |
| 14wk HU vs AMB, SSC / MSC | not run | not given in the text; "fewer than 8wk" (Suppl. Fig. 5d,e) |

The paper gives no DEG threshold for the RNA-seq. S4.9.p1 sets a general p ≤ 0.05, and Fig. 3 highlights genes with log2FC > 2. I recorded `pvalue < 0.05` with `stated_explicitly: false`.

## Deviations
None executed. Paper's method (edgeR exactTest, dispersion = 0.2, TMM, sum of counts > 2, protein-coding transcripts) is recorded in `paper_reconstruction` but not reproduced.

## Tool problems
- The Bash heredo ... [665 more characters]
