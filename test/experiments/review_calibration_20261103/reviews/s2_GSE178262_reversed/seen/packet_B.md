# Review packet B (the analysis' decisions): GSE178262_wheel

## Mechanical flags

- **possible_reversed_contrast**: {"contrast": "act_CTRL_vs_DA_zt-Z04", "control": "DA at ZT4", "treatment": "CTRL at ZT4", "note": "the control side reads as exercise or the test side as control"}
- **possible_reversed_contrast**: {"contrast": "act_CTRL_vs_DA_zt-Z16", "control": "DA at ZT16", "treatment": "CTRL at ZT16", "note": "the control side reads as exercise or the test side as control"}
- **pairing_key_candidate**: {"key": "characteristics_ch1.2.zeitgeber time (without act) + suffix of title", "across": "act", "pairs_or_sets": 8, "samples_linked": 22, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| wheel/act_CTRL_vs_DA_zt-Z04 | 2094 | 2257 | padj <= 0.05 | 2257 | 537 | 144 | 3015 | 4151 | 828 | 286 | 2430 | 0.109 | 0.212 |
| wheel/act_CTRL_vs_DA_zt-Z16 | 368 | 369 | padj <= 0.05 | 369 | 60 | 15 | 596 | 1944 | 281 | 110 | 861 | 0.121 | 0.099 |

## Samples per design level

### `act`
- **CTRL** (8): GSM5386039 / CTRL ZT4 1 / The L001 and L002 raw files were produce; GSM5386040 / CTRL ZT4 2 / The L001 and L002 raw files were produce; GSM5386041 / CTRL ZT4 3 / The L001 and L002 raw files were produce; GSM5386042 / CTRL ZT4 4 / The L001 and L002 raw files were produce; GSM5386047 / CTRL ZT16 1 / The L001 and L002 raw files were produce; GSM5386048 / CTRL ZT16 2 / The L001 and L002 raw files were produce; GSM5386049 / CTRL ZT16 3 / The L001 and L002 raw files were produce; GSM5386050 / CTRL ZT16 4 / The L001 and L002 raw files were produce
- **DA** (8): GSM5386043 / DA ZT4 1 / The L001 and L002 raw files were produce; GSM5386044 / DA ZT4 2 / The L001 and L002 raw files were produce; GSM5386045 / DA ZT4 3 / The L001 and L002 raw files were produce; GSM5386046 / DA ZT4 4 / The L001 and L002 raw files were produce; GSM5386051 / DA ZT16 1 / The L001 and L002 raw files were produce; GSM5386052 / DA ZT16 2 / The L001 and L002 raw files were produce; GSM5386053 / DA ZT16 3 / The L001 and L002 raw files were produce; GSM5386054 / DA ZT16 4 / The L001 and L002 raw files were produce

### `zt`
- **Z04** (8): GSM5386039 / CTRL ZT4 1 / The L001 and L002 raw files were produce; GSM5386040 / CTRL ZT4 2 / The L001 and L002 raw files were produce; GSM5386041 / CTRL ZT4 3 / The L001 and L002 raw files were produce; GSM5386042 / CTRL ZT4 4 / The L001 and L002 raw files were produce; GSM5386043 / DA ZT4 1 / The L001 and L002 raw files were produce; GSM5386044 / DA ZT4 2 / The L001 and L002 raw files were produce; GSM5386045 / DA ZT4 3 / The L001 and L002 raw files were produce; GSM5386046 / DA ZT4 4 / The L001 and L002 raw files were produce
- **Z16** (8): GSM5386047 / CTRL ZT16 1 / The L001 and L002 raw files were produce; GSM5386048 / CTRL ZT16 2 / The L001 and L002 raw files were produce; GSM5386049 / CTRL ZT16 3 / The L001 and L002 raw files were produce; GSM5386050 / CTRL ZT16 4 / The L001 and L002 raw files were produce; GSM5386051 / DA ZT16 1 / The L001 and L002 raw files were produce; GSM5386052 / DA ZT16 2 / The L001 and L002 raw files were produce; GSM5386053 / DA ZT16 3 / The L001 and L002 raw files were produce; GSM5386054 / DA ZT16 4 / The L001 and L002 raw files were produce

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE178262"], "assay": "bulk RNA-seq, kallisto + tximport lengthScaledTPM pseudo-counts (S2.8.p2)", "inclusion": "this case: the 16 scheduled-wheel samples (CTRL and DA at ZT4 and ZT16, n=4 each)", "factors": {"act": ["CTRL", "DA"], "zt": ["Z04", "Z16"]}, "primary_estimand": "effect of the timing of 3 weeks of voluntary wheel training (daytime wheel access with dark-phase food restriction, DA, vs ad-libitum night-time wheel access, CTRL) on gastrocnemius gene expression at ZT4 and at ZT16", "planned_contrasts": ["DA vs CTRL at ZT4 (S3.8.p1; Fig. 12A; paper: 2094 DEGs)", "DA vs CTRL at ZT16 (S3.8.p1; Fig. 12A; paper: 368 DEGs)"], "repeated_measure_unit": "none: one muscle per mouse", "paper_method": "DESeq2 1.26.0 on tximport pseudo-counts (S2.8.p2)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S3.3.p2"}, "paper_results": "2094 DEGs at ZT4, 368 at ZT16 (S3.8.p1); overlap includes Klf4, Klf5, Klf15, Maf factors, Nr4a3; Atf3, Per2, Ppargc1a and Ppara induced only by daytime training"}

reasoning: S2.3.p1 defines CTRL and DA; it states that only daytime vs night-time wheel-active animals are compared, not trained vs sedentary. S3.8.p1 reports 2094 DEGs at ZT4 and 368 at ZT16. The paper states FDR <= 0.05 for the RNA-seq DEGs (S3.3.p2) and gives no other rule for this experiment.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34142717\\GSE178262_lanes_merged_symbol.csv", "owned": true, "checks": ["S11.p1 names GSE178262", "GEO titles CTRL/DA ZT4/ZT16 with n=4 match S2.3/S3.8"], "accession": "GSE178262", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE178262\\GSE178262_metadata.csv"}

reasoning: Same series and submitter as the treadmill case.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 40, "n_metadata": 40, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM5386015": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386016": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386017": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386018": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386019": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386020": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386021": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386022": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386023": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386024": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386025": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386026": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386027": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386028": "treadmill experiment (quadriceps); analysed in case GSE178262_treadmill", "GSM5386029": "treadmill experiment (quadriceps); analysed in case GSE178262_tre ... [1440 more characters]

reasoning: Lane-summed matrix with GSM columns (see treadmill case); exact alignment on the metadata index. act from the treatment-group field (Night activity = CTRL, Day activity = DA, matching GEO titles CTRL/DA); zt from the zeitgeber-time field.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts (tximport lengthScaledTPM gene-level pseudo-counts from kallisto)", "recommended_method": "DESeq2", "profile": {"path": "E:/agent/mwangLab_review/.review_queue/case_04/run/GSE178262_wheel\\aligned\\aligned_matrix.csv", "sha256": "0a39b7ce1c0223e151a192ec56340d426d1f949692b983301713ffa43c20aa5e", "n_features": 23621, "n_samples": 16, "annotation_columns_dropped": ["GSM5386015", "GSM5386016", "GSM5386017", "GSM5386018", "GSM5386019", "GSM5386020", "GSM5386021", "GSM5386022", "GSM5386023", "GSM5386024", "GSM5386025", "GSM5386026", "GSM5386027", "GSM5386028", "GSM5386029", "GSM5386030", "GSM5386031", "GSM5386032", "GSM5386033", "GSM5386034", "GSM5386035", "GSM5386036", "GSM5386037", "GSM5386038"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 4436020.59558839, "median": 56.36100033673981, "integer_fraction": 0.273, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Same matrix as the treadmill case: non-integer count-scale pseudo-counts; S2.8.p2 analyses them with DESeq2.

### design (valid, not_started)

final: {"analysis_type": "factorial 2x2 (act x zt), cell-means model, simple effects of act within zt", "formula": "~ cell (4 cells of n=4)", "contrasts": [{"name": "act_CTRL_vs_DA_zt-Z04", "control": "DA at ZT4", "treatment": "CTRL at ZT4", "role": "primary"}, {"name": "act_CTRL_vs_DA_zt-Z16", "control": "DA at ZT16", "treatment": "CTRL at ZT16", "role": "primary"}], "exploratory": "ZT16 vs ZT4 within each group and the act x zt interaction", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "E:/agent/mwangLab_review/.review_queue/case_04/run/GSE178262_wheel\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: Two training-timing groups within each sampling time; DA is the reference arm.

rejected alternatives: [{"value": "pool ZT4 and ZT16", "reason_rejected": "the paper reports each ZT separately; time of day changes expression strongly"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(act) + C(zt)", "n_samples": 16, "n_columns": 3, "columns": ["Intercept", "act_DA", "zt_Z16"], "rank": 3, "full_rank": true, "residual_df": 13, "levels": {"act": {"CTRL": 8, "DA": 8}, "zt": {"Z04": 8, "Z16": 8}}, "cells": [{"cell": ["CTRL", "Z04"], "n": 4}, {"cell": ["CTRL", "Z16"], "n": 4}, {"cell": ["DA", "Z04"], "n": 4}, {"cell": ["DA", "Z16"], "n": 4}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 16, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 16, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.zeitgeber time", "n_levels": 2, "status": "crossed", "crosstab": {"CTRL": {"ZT16": 4, "ZT4": 4}, "DA": {"ZT16": 4, "Z ... [1935 more characters]

reasoning: Independent single-housed mice, one sample each; same sequencing run; all male.

### method (valid, not_started)

final: {"matrix_type": "estimated counts (tximport lengthScaledTPM gene-level pseudo-counts from kallisto)", "method": "DESeq2 (pydeseq2 Wald, joint cell-means model on the 16 wheel samples)", "formula": "~ cell", "rounding_documented": true, "paper_route": {"method": "DESeq2 1.26.0 (R), lfcShrink fold changes", "status": "reproduced_with_deviation", "reason": "same method on the same pseudo-counts via pydeseq2; model scope not stated"}, "deviations": ["pydeseq2 instead of R DESeq2 1.26.0", "pseudo-counts rounded to integers", "two lanes summed per library", "one fit on all 16 wheel samples; unshrunk log2FC", "Entrez IDs mapped to symbols"]}

reasoning: S2.8.p2.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625}}

reasoning: S3.3.p2 defines RNA-seq DEGs as FDR <= 0.05; no fold-change rule is stated for the wheel experiment either.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "wheel", "role": "secondary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 16, "matrix": "E:/agent/mwangLab_review/.review_queue/case_04/run/GSE178262_wheel\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_04/run/GSE178262_wheel\\results\\wheel\\DEG_results_act_CTRL_vs_DA_zt-Z04.csv", "E:/agent/mwangLab_review/.review_queue/case_04/run/GSE178262_wheel\\results\\wheel\\DEG_results_act_CTRL_vs_DA_zt-Z16.csv", "E:/agent/mwangLab_review/.review_queue/case_04/run/GSE178262_wheel\\results\\wheel\\DEG_results_zt_Z16_vs_Z04_act-CTRL.csv", "E:/agent/mwangLab_review/.review_queue/case_04/run/GSE178262_wheel\\results\\wheel\\DEG_results_zt_Z16_vs_Z04_act-DA.csv", "E:/agent/mwangLab_review/.review_queue/case_04/run/GSE178262_wheel\\results\\wheel\\DEG_results_act_zt_CTRL_Z16_vs_DA_Z04.csv"], "counts": {"wheel/act_CTRL_vs_DA_zt-Z04": {"applied": {"rule": "padj <= 0.05", "n_tested": 14650, "n_significant": 2257, "n_up": 1121, "n_down": 1136, "deg_sanity": "ok"}, "audit": {"rule": "padj <= 0.05 and |log2FoldChange| >= 0.584963", "n_tested": 14650, "n_significant": 537, "n_up": 289, "n_down": 248, "deg_sanity": "ok"}}, "wheel/act_CTRL_vs_DA_zt-Z16": {"applied": {"rule": "padj <= 0.05", "n_tested": 12754, "n_significant": 369, "n_up": 200, "n_down": 169, "deg_sanity": "ok"}, "audit": {"rule": "padj <= 0.05 and |log2FoldChange| >= 0.584963", "n_tested": 12754, "n_significant": ... [1012 more characters]

reasoning: One DESeq2 model on the 16 wheel samples; the two DA vs CTRL contrasts are the paper route, the rest exploratory.

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["both arms exercise: the estimand is the timing of training (plus the DA feeding restriction), not exercise vs sedentary", "feeding schedule differs between arms by design"], "results": {"wheel/act_CTRL_vs_DA_zt-Z04": {"n_deg": 2257, "up": 1121, "down": 1136, "rule": "padj <= 0.05", "audit_n": 537}, "wheel/act_CTRL_vs_DA_zt-Z16": {"n_deg": 369, "up": 200, "down": 169, "rule": "padj <= 0.05", "audit_n": 60}, "wheel/zt_Z16_vs_Z04_act-CTRL": {"n_deg": 2915, "up": 1421, "down": 1494, "rule": "padj <= 0.05", "audit_n": 777}, "wheel/zt_Z16_vs_Z04_act-DA": {"n_deg": 2402, "up": 1174, "down": 1228, "rule": "padj <= 0.05", "audit_n": 558}, "wheel/act_zt_CTRL_Z16_vs_DA_Z04": {"n_deg": 1658, "up": 860, "down": 798, "rule": "padj <= 0.05", "audit_n": 769}}, "paper_counts": {"wheel/act_CTRL_vs_DA_zt-Z04": 2094, "wheel/act_CTRL_vs_DA_zt-Z16": 368}, "comparison": {"wheel/act_CTRL_vs_DA_zt-Z04": {"ours": 2257, "paper": 2094}, "wheel/act_CTRL_vs_DA_zt-Z16": {"ours": 369, "paper": 368}}, "paper_gene_check": {"wheel/act_CTRL_vs_DA_zt-Z04": {"Klf4": {"baseMean": 805.3142, "log2FoldChange": -1.0409, "padj": 0.0001, "pvalue": 0.0}, "Klf5": {"baseMean": 84.399, "log2FoldChange": 0.3805, "padj": 0.1028, "pvalue": 0.0215}, "Klf15": {"baseMean": 2378.9523, "log2FoldChange": -0.8702, "padj": 0.0, "pvalue": 0.0}, "Maff": {"baseMean": 141.9274, "log2FoldChange": -0.9313, "padj": 0.0, "pvalue": 0.0}, "Nr4a3": {"baseMean": 328.3151, "log2FoldChange": -3.8845, "pa ... [865 more characters]

reasoning: Paper contrasts and threshold; S3.8.p1 counts and named genes.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sequencing lanes",
    "paper": "not described",
    "data": "one column per lane",
    "disposition": "executable_without_change: lanes summed per library"
  },
  {
    "item": "comparison type",
    "paper": "daytime vs night-time trained animals only (S2.3.p1)",
    "data": "no sedentary arm in the wheel experiment",
    "disposition": "executable_without_change: estimand recorded as training timing"
  }
]
