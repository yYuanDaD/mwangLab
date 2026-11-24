# Review packet B (the analysis' decisions): GSE269698_young_vehicle

## Mechanical flags

- none

## Samples per design level

### `stim`
- **N** (6): GSM8324931 / Non-Stim TA, Young Vehicle, 1 / YVN1; GSM8324932 / Non-Stim TA, Young Vehicle, 2 / YVN2; GSM8324933 / Non-Stim TA, Young Vehicle, 3 / YVN3; GSM8324934 / Non-Stim TA, Young Vehicle, 4 / YVN4; GSM8324935 / Non-Stim TA, Young Vehicle, 5 / YVN5; GSM8324936 / Non-Stim TA, Young Vehicle, 6 / YVN6
- **S** (6): GSM8324937 / Stim TA, Young Vehicle, 1 / YVS1; GSM8324938 / Stim TA, Young Vehicle, 2 / YVS2; GSM8324939 / Stim TA, Young Vehicle, 3 / YVS3; GSM8324940 / Stim TA, Young Vehicle, 4 / YVS4; GSM8324941 / Stim TA, Young Vehicle, 5 / YVS5; GSM8324942 / Stim TA, Young Vehicle, 6 / YVS6

### `subject`
- **m1** (2): GSM8324931 / Non-Stim TA, Young Vehicle, 1 / YVN1; GSM8324937 / Stim TA, Young Vehicle, 1 / YVS1
- **m2** (2): GSM8324932 / Non-Stim TA, Young Vehicle, 2 / YVN2; GSM8324938 / Stim TA, Young Vehicle, 2 / YVS2
- **m3** (2): GSM8324933 / Non-Stim TA, Young Vehicle, 3 / YVN3; GSM8324939 / Stim TA, Young Vehicle, 3 / YVS3
- **m4** (2): GSM8324934 / Non-Stim TA, Young Vehicle, 4 / YVN4; GSM8324940 / Stim TA, Young Vehicle, 4 / YVS4
- **m5** (2): GSM8324935 / Non-Stim TA, Young Vehicle, 5 / YVN5; GSM8324941 / Stim TA, Young Vehicle, 5 / YVS5
- **m6** (2): GSM8324936 / Non-Stim TA, Young Vehicle, 6 / YVN6; GSM8324942 / Stim TA, Young Vehicle, 6 / YVS6

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE248869", "GSE269698"], "assay": "bulk RNA-seq of mouse tibialis anterior, STAR + DESeq2 per GEO data_processing", "primary_estimand": "Acute effect of unilateral high-force eccentric contractions (electrically stimulated sciatic nerve, harvested 4 h later) vs the contralateral non-stimulated TA, within mouse, in young (4 mo) vehicle-treated males.", "planned_contrasts": ["Stim vs Non-Stim TA, young vehicle, paired by mouse (abstract: increased load lowered Arrdc2, not Arrdc3; no DEG count in abstract)"], "factors": {"stim": ["NS", "S"], "age": ["Young", "Aged"], "treatment": ["Vehicle", "Dexamethasone"]}, "repeated_measure_unit": "mouse (Stim and Non-Stim leg of the same animal)", "sample_inclusion": "Vehicle arm only for this paper; DEX arms belong to the glucocorticoid question of the later papers that the series also cites (PMIDs 39495237, 40880111).", "paper_threshold": {"metric": "FDR", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "not stated in abstract; GEO data_processing: DESeq2 default, BH FDR"}, "paper_method": "DESeq2 1.30.1 default; deposited sheet names 'Paired_YVNvsYVS' imply a paired design"}

reasoning: Abstract: 'mechanical load was increased by ... inducing high-force contractions' in young and aged mice and 'Increasing mechanical load beyond normal ambulatory levels lowered Arrdc2 mRNA, but not Arrdc3 mRNA, in young and aged muscle'. The abstract does not say whether this came from RNA-seq or qPCR; GSE269698 cites PMID 38314723 and holds exactly that design (young/aged, Stim/Non-Stim) plus a DEX factor from the later papers. Only the abstract is available, so the comparison rests on it.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE269698\\GSE269698_rlog_Gordon__rlog_Paired_YVNvsYVS.csv", "owned": true, "checks": ["GEO Series_pubmed_id lists 38314723 (with 39495237 and 40880111)", "vehicle Stim/Non-Stim arms in young and aged males match the abstract's contraction experiment", "matrix columns YVN1-6/YVS1-6 match metadata description field exactly"], "accession": "GSE269698", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE269698\\GSE269698_metadata.csv"}

reasoning: Shared series; this paper owns the vehicle contraction arms. Confidence medium because the abstract does not say the contraction data were sequenced rather than measured by qPCR.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 12, "n_metadata": 48, "coverage": 0.25, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM8324943", "GSM8324944", "GSM8324945", "GSM8324946", "GSM8324947", "GSM8324948", "GSM8324949", "GSM8324950", "GSM8324951", "GSM8324952", "GSM8324953", "GSM8324954", "GSM8324955", "GSM8324956", "GSM8324957", "GSM8324958", "GSM8324959", "GSM8324960", "GSM8324961", "GSM8324962", "GSM8324963", "GSM8324964", "GSM8324965", "GSM8324966", "GSM8324967", "GSM8324968", "GSM8324969", "GSM8324970", "GSM8324971", "GSM8324972", "GSM8324973", "GSM8324974", "GSM8324975", "GSM8324976", "GSM8324977", "GSM8324978"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38314723\\GSE269698_young_vehicle\\aligned\\aligned_metadata.csv", "columns": {"subject": {"source": "description", "regex": "^[YO][VD][NS](\\d)$", "recode": {"1": "m1", "2": "m2", "3": "m3", "4": "m4", "5": "m5", "6": "m6"}}, "stim": {"source": "description", "regex": "^[YO][VD]([NS])\\d$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38314723\\GSE269698_young_vehicle\\aligned\\design_metadata.csv", "sha256": "33907452e16b92706983eeb3d462a82583c2520698959d3d822bcb971d5c3299", "levels": {"subject": {"m1": 2, "m2": 2, "m3": 2, "m4": 2, "m5": 2, "m6": 2}, "stim": {"N": 6, "S": 6}}}}

reasoning: Exact match of matrix columns to metadata 'description' (12/12). Stim from the N/S letter (same as 'contractions protocol' column). Subject = replicate number within age x treatment: the series is a unilateral design (both TAs from each mouse) and the deposited sheet is named 'Paired_YVNvsYVS', so YVN k and YVS k are taken as the same mouse. This pairing is inferred from naming, not stated per sample.

### matrix (valid, not_started)

final: {"matrix_type": "rlog (DESeq2 regularized log2 counts)", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38314723\\GSE269698_young_vehicle\\aligned\\aligned_matrix.csv", "sha256": "04a63c3697109493a91203b42959bb3cddea662ed079d688b812614ba720d7cd", "n_features": 57010, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 178167, "negative_fraction": 0.260432, "min": -2.211678421, "max": 20.74020202, "median": 0.0, "integer_fraction": 0.3912, "candidates": ["signed_log_scale (log ratios, M-values, or centered data)"]}}

reasoning: File name 'rlog', values -2.2 to 20.7, non-integer, zeros for unexpressed genes; GEO data_processing says counts were analysed with DESeq2 but no count table was deposited (supplementary only rlog xlsx). rlog is a log2-scale, variance-stabilised matrix, so a log-scale linear model (limma) is the supported route; DESeq2 cannot run on it.

### design (valid, not_started)

final: {"analysis_type": "paired two-group", "design_column": "stim", "control": "N", "treatment": "S", "contrasts": [{"name": "stim_S_vs_N", "control": "N", "treatment": "S", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38314723\\GSE269698_young_vehicle\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Within-mouse contraction effect, young vehicle, n=6 pairs.

rejected alternatives: [{"value": "pool young and aged", "reason_rejected": "the abstract reports young and aged separately and the deposited rlog matrices are per age"}, {"value": "include DEX arms", "reason_rejected": "DEX is the later papers' factor, not part of this paper's question"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "blocking factor (mouse) in the model"}], "design_check": {"formula_equivalent": "~ C(stim) + C(subject)", "n_samples": 12, "n_columns": 7, "columns": ["Intercept", "stim_S", "subject_m2", "subject_m3", "subject_m4", "subject_m5", "subject_m6"], "rank": 7, "full_rank": true, "residual_df": 5, "levels": {"stim": {"N": 6, "S": 6}, "subject": {"m1": 2, "m2": 2, "m3": 2, "m4": 2, "m5": 2, "m6": 2}}, "cells": [{"cell": ["N", "m1"], "n": 1}, {"cell": ["N", "m2"], "n": 1}, {"cell": ["N", "m3"], "n": 1}, {"cell": ["N", "m4"], "n": 1}, {"cell": ["N", "m5"], "n": 1}, {"cell": ["N", "m6"], "n": 1}, {"cell": ["S", "m1"], "n": 1}, {"cell": ["S", "m2"], "n": 1}, {"cell": ["S", "m3"], "n": 1}, {"cell": ["S", "m4"], "n": 1}, {"cell": ["S", "m5"], "n": 1}, {"cell": ["S", "m6"], "n": 1}], "min_cell_size": 1, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 12, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 12, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1 ... [2466 more characters]

reasoning: Stim and Non-Stim legs come from the same mouse; mouse is a blocking factor.

### method (valid, not_started)

final: {"matrix_type": "rlog (DESeq2 regularized log2 counts)", "method": "limma (moderated t, eBayes) on deposited rlog values", "formula": "~ subject + stim", "paper_route": {"method": "DESeq2 paired (~ mouse + stim) on counts", "status": "blocked", "reason": "no count table deposited; only rlog values"}, "deviations": ["limma on rlog instead of DESeq2 on counts", "low-expression filter: rlog >= 1 in >= 3 of the 12 samples (removes all-zero rows)"]}

reasoning: Validated log-scale route on the deposited matrix with mouse blocking.

### threshold (valid, not_started)

final: {"paper_threshold": null, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Abstract states no DEG threshold; GEO says DESeq2 BH FDR without a cutoff. Workflow default BH padj < 0.05, no fold-change rule."}

reasoning: No paper threshold available (abstract only).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "stim_S_vs_N", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38314723\\GSE269698_young_vehicle\\results\\stim_S_vs_N\\input\\matrix_filtered.csv", "formula": "~ subject + stim", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38314723\\GSE269698_young_vehicle\\results\\stim_S_vs_N\\DEG_results_S_vs_N.csv"], "counts": {"stim_S_vs_N": {"applied": {"rule": "padj < 0.05", "n_tested": 17492, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Paired limma: contraction effect within mouse, young vehicle.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "stim_S_vs_N_unpaired", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38314723\\GSE269698_young_vehicle\\results\\stim_S_vs_N_unpaired\\input\\matrix_filtered.csv", "formula": "~ stim", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38314723\\GSE269698_young_vehicle\\results\\stim_S_vs_N_unpaired\\DEG_results_S_vs_N.csv"], "counts": {"stim_S_vs_N_unpaired": {"applied": {"rule": "padj < 0.05", "n_tested": 17492, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Unpaired limma (~ stim) to check how much the inferred mouse pairing changes the result.

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Comparison with the paper rests on the abstract only; the abstract gives no DEG count, only that contractions lowered Arrdc2 but not Arrdc3.", "Pairing of Stim/Non-Stim legs inferred from replicate numbers and sheet name.", "limma on rlog values, not DESeq2 on counts.", "Sensitivity: unpaired limma also gives 0 DEGs; young non-stimulated legs already show high immediate-early gene levels (Atf3, Fos, Egr1), so the stim contrast is weak in these data.", "Arrdc2 does not decrease with contractions in young vehicle (log2FC ~ -0.04), contrary to the abstract's statement for young muscle."], "results": {"stim_S_vs_N": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "stim_S_vs_N_unpaired": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"stim_S_vs_N": {"Arrdc2": {"AveExpr": 11.7308, "log2FoldChange": -0.0373, "padj": 0.972, "pvalue": 0.746}, "Arrdc3": {"AveExpr": 10.0447, "log2FoldChange": 0.1277, "padj": 0.745, "pvalue": 0.00213}}, "stim_S_vs_N_unpaired": {"Arrdc2": {"AveExpr": 11.7308, "log2FoldChange": -0.0373, "padj": 1.0, "pvalue": 0.893}, "Arrdc3": {"AveExpr": 10.0447, "log2FoldChange": 0.1277, "padj": 1.0, "pvalue": 0.448}}}}

reasoning: Paper's expected direction: Arrdc2 down with contractions, Arrdc3 unchanged.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "input matrix",
    "paper": "DESeq2 on count tables",
    "data": "only rlog matrices deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "pairing",
    "paper": "unilateral contractions; 'Paired' sheet names",
    "data": "no per-sample mouse ID; replicate number used",
    "disposition": "executable_with_assumption"
  },
  {
    "item": "aged vehicle n",
    "paper": "GEO overall_design says Aged-Vehicle n=4 mice",
    "data": "6 OVN + 6 OVS samples deposited",
    "disposition": "recorded"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 38314723 (Arrdc2, mechanical load, aging)

**The paper comparison rests on the abstract only.** No full text was available. I used the PubMed abstract (fetched with E-utilities efetch) and the GEO series descriptions, saved under `paper/`. The abstract gives no DEG counts and no DEG threshold.

## What ran
Route: case spec (`case_spec.json`) run with `python -m tools.case_runner execute`. Validator: 25 records, 0 errors. Run status: completed.

| Case | Outcome |
|---|---|
| GSE248869: C2C12 myotubes, Arrdc2 vs GFP adenovirus, 5 vs 5 | **Refused at `alignment`.** The series has no exercise contrast (it is a cell-culture overexpression experiment). Also, the matrix columns (GFP3–7, Arrdc2-6/7/9/10/11) cannot be matched by name to the GSM titles (control 1–5, treatment 1–5). Only a positional mapping would work, and that is not allowed. |
| GSE269698_young_vehicle: young vehicle TA, contraction-stimulated vs contralateral non-stimulated leg, 6 vs 6 | Ran. limma on the deposited rlog values, `~ subject + stim`, plus an unpaired sensitivity run (`~ stim`). |
| GSE269698_aged_vehicle: aged vehicle TA, stimulated vs non-stimulated, 6 vs 6 | Ran. Same model as the young case. |

The exercise-like estimand is the acute response to high-force eccentric contractions, 4 h after electrical stimulation, compared within mouse. The DEX arms of GSE269698 belong to the later papers that the series also cites (PMIDs 39495237 and 40880111), so I left them out.

## DEG counts vs the paper
Threshold: `workflow_default`, BH padj < 0.05 with no fold-change rule. The abstract states no threshold; GEO only says "DESeq2 default, BH FDR".

| Contrast | Ours (paired, primary) | Ours (unpaired, sensitivity) | Paper |
|---|---|---|---|
| Young vehicle Stim vs Non-Stim | 0 | 0 | not given in abstract |
| Aged vehicle Stim vs Non-Stim | 1 (1 up) | 104 (95 up, 9 down) | not given in abstract |

The abstract's only gene-level claim is that increased load lowered Arrdc2 mRNA, but not Arrdc3, in young and aged muscle.
- **Young:** Arrdc2 log2FC −0.04 (p = 0.75). This does not reproduce the abstract's decrease. The young claim may come from qPCR or another cohort.
- **Aged:** Arrdc2 log2FC −0.45 (p = 0.024, padj = 0.20). The direction agrees but it is not significant after FDR.
- **Arrdc3:** not significant in either age (young +0.13, aged +0.21), consistent with "not Arrdc3".

## Deviations
- **Matrix:** only DESeq2 rlog matrices were deposited, with no count table. So I ra ... [1802 more characters]
