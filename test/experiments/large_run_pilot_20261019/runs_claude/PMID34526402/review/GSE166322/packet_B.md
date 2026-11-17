# Review packet B (the analysis' decisions): GSE166322

## Mechanical flags

- **possible_reversed_contrast**: {"contrast": "grp_Ctrl_vs_MDZ", "control": "MDZ", "treatment": "Ctrl", "note": "the control side reads as exercise or the test side as control"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_joint/grp_Ctrl_vs_MDZ | 1477 | 1972 | padj < 0.05 and |log2FoldChange| > 0.584963 | 1972 | 1972 | 1847 | 3009 | 4183 | 4064 | 3246 | 2305 | 0.052 | 0.283 |

## Samples per design level

### `grp`
- **Ctrl** (3): GSM5068526 / Control_8w_RNAseq_rep1; GSM5068527 / Control_8w_RNAseq_rep2; GSM5068528 / Control_8w_RNAseq_rep3
- **MDZ** (3): GSM5068529 / MDZ_8w_RNAseq_rep1; GSM5068530 / MDZ_8w_RNAseq_rep2; GSM5068531 / MDZ_8w_RNAseq_rep3
- **RunMDZ** (3): GSM5068542 / RUN_MDZ_8w_RNAseq_rep1; GSM5068543 / RUN_MDZ_8w_RNAseq_rep2; GSM5068544 / RUN_MDZ_8w_RNAseq_rep3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE166322"], "assay": "bulk RNA-seq (50-bp SE, HiSeq 2500) of FACS-sorted Nestin-EGFP+ dentate gyrus NSCs and progeny; ATAC-seq and Egr1 ChIP-seq in the same series are not expression data", "primary_estimand": "Effect of voluntary wheel running (from weaning, P28, to 8w) on the NSC transcriptome of mice exposed to midazolam (MDZ) early in life: MDZ+RW vs MDZ at 8w (Fig. 7A-B, S7.p1)", "factors": {"group_8w": ["Ctrl (dH2O)", "MDZ", "MDZ+RW"], "note": "Ctrl+RW exists only for histology/behaviour (Fig. 7D-O); no Ctrl+RW RNA-seq deposited"}, "sample_inclusion": "8w RNA-seq: Control_8w (n=3), MDZ_8w (n=3), RUN_MDZ_8w (n=3); each library pools 30,000 cells from 3-5 mice (S9.10.p1). P10 RNA-seq and in vitro Egr1/Ctrl NSC RNA-seq address other questions", "planned_contrasts": ["MDZ+RW vs MDZ at 8w (Fig. 7B; paper reports only overlaps: 42 MDZ-up genes reversed down, 76 MDZ-down genes reversed up; no total DEG count)", "MDZ vs Ctrl at 8w (Fig. 3E, S3.p1; 604 up, 873 down; needed for the Fig. 7B overlap)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "source_locator": "FIG7 legend (B): fold change > 1.5, q < 0.05; S3.p1: q < 0.05, fold change >= 1.5"}, "paper_method": "featureCounts raw counts -> DESeq2 (S9.11.p1); TPM for display", "paper_results": {"MDZ_vs_Ctrl_8w": {"up": 604, "down": 873}, "RW_reversal_overlap": {"MDZ_up_and_RW_down": 42, "MDZ_down_and_RW_up": 76}, "named_genes": ["Notch2 (MDZ ... [29 more characters]

reasoning: Abstract and S7.p1/Fig. 7 state the exercise question: voluntary running normalizes the MDZ-perturbed transcriptome. Fig. 7B defines the comparison MDZ+RW vs MDZ with fold change > 1.5 and q < 0.05, overlapped with MDZ vs Ctrl at 8w (Fig. 3E). Methods S9.11.p1: DESeq2 on featureCounts counts. S9.15.p1: four groups randomized at weaning, but RNA-seq only for Ctrl, MDZ, MDZ+RW.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE166322\\GSE166322_merged_from_tar.csv", "owned": true, "checks": ["S13.p1 names GSE166322 for the RNA-seq, ATAC-seq and ChIP-seq of this study", "sample titles Control_8w/MDZ_8w/RUN_MDZ_8w RNAseq rep1-3 match the paper's n = 3 per group at 8w", "contact at NAIST, matching the authors' institute"], "accession": "GSE166322", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE166322\\GSE166322_metadata.csv"}

reasoning: GSE166322 is the paper's own deposit; the 21 per-sample RNA-seq TPM files in GSE166322_RAW.tar are the expression data. Merged matrix built by inspect from the tar.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 21, "n_metadata": 31, "coverage": 0.6774, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM5068532", "GSM5068533", "GSM5068534", "GSM5068535", "GSM5068536", "GSM5068537", "GSM5068538", "GSM5068539", "GSM5068540", "GSM5068541"], "excluded_samples": {"GSM5068520": "P10 RNA-seq (Control); not part of the 8w exercise experiment", "GSM5068521": "P10 RNA-seq (Control); not part of the 8w exercise experiment", "GSM5068522": "P10 RNA-seq (Control); not part of the 8w exercise experiment", "GSM5068523": "P10 RNA-seq (MDZ); not part of the 8w exercise experiment", "GSM5068524": "P10 RNA-seq (MDZ); not part of the 8w exercise experiment", "GSM5068525": "P10 RNA-seq (MDZ); not part of the 8w exercise experiment", "GSM5068545": "in vitro cultured NSC (lentiviral Ctrl) RNA-seq; separate experiment (Fig. 5)", "GSM5068546": "in vitro cultured NSC (lentiviral Ctrl) RNA-seq; separate experiment (Fig. 5)", "GSM5068547": "in vitro cultured NSC (lentiviral Ctrl) RNA-seq; separate experiment (Fig. 5)", "GSM5068548": "in vitro Egr1-transduced NSC RNA-seq; separate experiment (Fig. 5)", "GSM5068549": "in vitro Egr1-transduced NSC RNA-seq; separate experiment (Fig. 5)", "GSM5068550": "in vitro Egr1-transduced NSC RNA-seq; separate experiment (Fig. 5)"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34526402\\GSE166322\\aligned\\aligned_metadata_kept.csv", "columns": {"grp": {"source": "tit ... [384 more characters]

reasoning: Matrix columns are GSM<id>_<title>; the GSM prefix equals the metadata index (inspect: 21/21 match). Group is parsed from the title. P10 and in vitro samples are excluded because the exercise question concerns only the 8w libraries (Fig. 7A).

### matrix (valid, not_started)

final: {"matrix_type": "TPM", "recommended_method": "limma on log2(TPM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34526402\\GSE166322\\aligned\\aligned_matrix.csv", "sha256": "d20eb471b223ccd7583f386f455b26378b526f77c450b2ba4c2c98c40093f64a", "n_features": 24657, "n_samples": 9, "annotation_columns_dropped": ["GSM5068520", "GSM5068521", "GSM5068522", "GSM5068523", "GSM5068524", "GSM5068525", "GSM5068545", "GSM5068546", "GSM5068547", "GSM5068548", "GSM5068549", "GSM5068550"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 7350.75, "median": 3.72736, "integer_fraction": 0.4206, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GEO data_processing: TXT files indicating TPM values of each sample. Values are non-integer (integer fraction 0.36, driven by zeros), median 1.74, max 55,925; per-sample files have one value column (e.g. Mrpl15 27.7). The paper ran DESeq2 on featureCounts raw counts, which were not deposited.

rejected alternatives: [{"value": "estimated counts", "reason_rejected": "data_processing explicitly says TPM and values are fractional at low magnitude"}]

### design (valid, not_started)

final: {"analysis_type": "multilevel", "design_column": "grp", "contrasts": [{"name": "grp_RunMDZ_vs_MDZ", "control": "MDZ", "treatment": "RunMDZ", "role": "primary"}, {"name": "grp_Ctrl_vs_MDZ", "control": "MDZ", "treatment": "Ctrl", "role": "secondary", "note": "sign reversed relative to the paper's MDZ vs Ctrl; up here = down in MDZ"}, {"name": "grp_RunMDZ_vs_Ctrl", "control": "Ctrl", "treatment": "RunMDZ", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34526402\\GSE166322\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: One control-level factor with three levels at 8w; one model with planned contrasts (no pooling). Primary exercise estimand is MDZ+RW vs MDZ (Fig. 7B). MDZ vs Ctrl (Fig. 3E) is the paper's comparison that Fig. 7B overlaps with. RunMDZ vs Ctrl is exploratory (does running bring MDZ mice back to control levels). No Ctrl+RW RNA-seq, so the running main effect in unexposed mice and the MDZ x running interaction cannot be estimated; the exercise effect is conditional on MDZ exposure.

rejected alternatives: [{"value": "2x2 MDZ x running factorial", "reason_rejected": "Ctrl+RW RNA-seq not performed/deposited"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 9, "n_columns": 3, "columns": ["Intercept", "grp_MDZ", "grp_RunMDZ"], "rank": 3, "full_rank": true, "residual_df": 6, "levels": {"grp": {"Ctrl": 3, "MDZ": 3, "RunMDZ": 3}}, "cells": [{"cell": ["Ctrl"], "n": 3}, {"cell": ["MDZ"], "n": 3}, {"cell": ["RunMDZ"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 9, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 9, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.age", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.genotype", "n_levels": 1, "status": "constant"}, {"column": "treatment_protocol_ch1", "n_levels": 1, "status":  ... [1460 more characters]

reasoning: Each library is an independent pool of 3-5 mice; no pairing or subject repeated across groups. No batch, sex or lane column in metadata. RUN_MDZ libraries have later GSM numbers (deposited after the ChIP samples), which hints at a separate sequencing batch, but no batch variable is recorded, so it cannot be modelled; recorded as a caveat.

### method (valid, not_started)

final: {"matrix_type": "TPM", "method": "limma (empirical Bayes) on log2(TPM+1)", "formula": "~ 0 + grp", "paper_route": {"method": "DESeq2 on featureCounts raw counts", "status": "blocked", "reason": "only per-sample TPM files were deposited in GEO; raw counts unavailable; TPM must not be rounded into counts"}, "deviations": ["limma on log2(TPM+1) instead of DESeq2 on counts", "low-expression filter TPM >= 1 in >= 3 of the 9 samples (paper states no filter; stands in for DESeq2 independent filtering)"], "transform": "log2(x+1)"}

reasoning: Matrix policy: TPM -> log2(x+1) -> limma. Run as a declared deviation from the paper's DESeq2 route.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper threshold (q < 0.05, FC > 1.5) applied to limma BH-adjusted p and log2FC on log2(TPM+1)"}

reasoning: FIG7 legend (B): fold change > 1.5, q < 0.05 for both MDZ vs Ctrl and MDZ+RW vs MDZ. log2(1.5) = 0.5849625. Audit rule: padj < 0.05 without fold-change cutoff.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "grp_joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34526402\\GSE166322\\results\\grp_joint\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34526402\\GSE166322\\results\\grp_joint\\DEG_results_grp_RunMDZ_vs_MDZ.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34526402\\GSE166322\\results\\grp_joint\\DEG_results_grp_Ctrl_vs_MDZ.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34526402\\GSE166322\\results\\grp_joint\\DEG_results_grp_RunMDZ_vs_Ctrl.csv"], "counts": {"grp_joint/grp_RunMDZ_vs_MDZ": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14759, "n_significant": 328, "n_up": 237, "n_down": 91, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14759, "n_significant": 328, "n_up": 237, "n_down": 91, "deg_sanity": "ok"}}, "grp_joint/grp_Ctrl_vs_MDZ": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14759, "n_significant": 1972, "n_up": 301, "n_down": 1671, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14759, "n_significant": 1972, "n_up": 301, "n_down": 1671, "deg_sanity": "ok"}}, "grp_joint/grp_RunMDZ_vs_Ctrl": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", " ... [217 more characters]

reasoning: One limma model on all 9 8w samples; primary contrast RunMDZ vs MDZ, MDZ-vs-Ctrl for the paper's overlap, RunMDZ vs Ctrl exploratory.

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper's DESeq2-on-counts route blocked (TPM only); limma on log2(TPM+1) used", "No Ctrl+RW RNA-seq: the exercise effect is estimable only in MDZ-exposed mice; no interaction", "RUN_MDZ libraries were likely sequenced separately from Ctrl/MDZ 8w (later GSM ids); running may be confounded with an unrecorded batch", "n = 3 pooled libraries per group", "Paper reports no total DEG count for MDZ+RW vs MDZ, only overlaps with MDZ vs Ctrl (42 and 76)", "Direction balance contradicts the paper for MDZ vs Ctrl 8w: ours 1671 up / 301 down in MDZ vs paper 604 up / 873 down", "Fig. 7B reversal overlaps differ: ours 80 MDZ-up genes reversed down by running (paper 42) and 16 MDZ-down genes reversed up (paper 76); both overlaps significant (hypergeometric P 5e-64, 3e-5)", "Notch2 moves in the paper's direction (up in MDZ, down with running) but is not significant here (padj 0.069 and 0.48)"], "results": {"grp_joint/grp_RunMDZ_vs_MDZ": {"n_deg": 328, "up": 237, "down": 91, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 328}, "grp_joint/grp_Ctrl_vs_MDZ": {"n_deg": 1972, "up": 301, "down": 1671, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 1972}, "grp_joint/grp_RunMDZ_vs_Ctrl": {"n_deg": 2753, "up": 2258, "down": 495, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 2753}}, "paper_counts": {"grp_joint/grp_Ctrl_vs_MDZ": 1477}, "comparison": {"grp_joint/grp_Ctrl_vs_MDZ": {"ours": 1972, "paper": 1 ... [447 more characters]

reasoning: Paper: 604 up + 873 down = 1477 for MDZ vs Ctrl at 8w (sign reversed here). Notch2 is the named running-reversed gene (S7.p1).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "input matrix",
    "paper": "featureCounts raw counts analysed with DESeq2",
    "data": "only per-sample TPM deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "Ctrl+RW group",
    "paper": "four groups incl. Ctrl+RW for histology/behaviour",
    "data": "no Ctrl+RW RNA-seq",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID34526402 / GSE166322

## What ran
- Case-spec route (`case_spec.json`), `tools.case_runner execute`. Status completed. The validator passed with 10 records and 0 errors.
- Input: `GSE166322_merged_from_tar.csv`, merged from the 21 per-sample RNA-seq files in `_RAW.tar`. GEO `data_processing` says these files hold TPM.
- Samples: the 9 libraries at 8 weeks (8w), n = 3 each:
  - Control_8w (Ctrl)
  - MDZ_8w (MDZ, early-life midazolam)
  - RUN_MDZ_8w (RunMDZ, MDZ mice given a running wheel)
- Excluded, with reasons recorded: 6 P10 RNA-seq libraries and 6 in vitro Egr1/Ctrl NSC libraries. The ATAC-seq and ChIP-seq samples are not in the matrix.
- Model: one limma model, `~ 0 + grp`, on log2(TPM+1), after a filter keeping TPM >= 1 in >= 3 samples (14,759 of 24,657 genes kept). It gives three contrasts:
  - primary: RunMDZ vs MDZ (paper Fig. 7B)
  - secondary: Ctrl vs MDZ (sign reversed relative to the paper's Fig. 3E)
  - exploratory: RunMDZ vs Ctrl
- Enrichment: not run, because the paper reports no pathway result for the running contrast.

## DEGs vs paper
Threshold is the paper's rule (Fig. 7B legend): q < 0.05 and FC > 1.5, i.e. padj < 0.05 and |log2FC| > 0.5849625. It is applied on the deviation route.

| Contrast | Ours | Paper |
|---|---|---|
| MDZ+RW vs MDZ (primary, exercise) | 328 (237 up, 91 down) | no total reported |
| MDZ vs Ctrl, 8w | 1972 (1671 up, 301 down in MDZ) | 1477 (604 up, 873 down) |
| Fig. 7B overlap: MDZ-up and reversed down by running | 80 | 42 |
| Fig. 7B overlap: MDZ-down and reversed up by running | 16 | 76 |
| RunMDZ vs Ctrl (exploratory) | 2753 | not reported |

- Both overlaps are significant, as in the paper (hypergeometric P = 5e-64 and 3e-5).
- The up/down balance is inverted relative to the paper. This is recorded in the study caveats.
- Notch2 moves in the paper's direction (up in MDZ, down with running) but is not significant here: padj 0.069 for MDZ vs Ctrl and 0.48 for RunMDZ vs MDZ.
- The audit rule (padj < 0.05, no FC cutoff) gives the same counts. With n = 3, every gene at padj < 0.05 already has |log2FC| > 0.585.

## Deviations
- The paper used DESeq2 on featureCounts raw counts, but GEO has only TPM. The paper route is blocked, and limma on log2(TPM+1) ran as a declared deviation.
- I added a low-expression filter (TPM >= 1 in >= 3 samples). The paper states no filter.
- No Ctrl+RW RNA-seq exists, so the running effect can only be estimated in MDZ-exposed mice. No interaction term is possible.
- The ... [556 more characters]
