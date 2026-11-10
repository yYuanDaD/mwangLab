# Review packet B (the analysis' decisions): GSE60833

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P2_trained_leg_T4_vs_T3 | 852 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 1472 | 101 | 31 | 409 | 0.072 | 0.112 |
| P2_untrained_leg_U4_vs_U3 | 928 | 6 | padj < 0.05 | 6 | 2 | 0 | 64 | 1808 | 98 | 14 | 646 | 0.066 | 0.138 |
| leg_T3_vs_U3 | 0 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 1784 | 71 | 28 | 531 | 0.071 | 0.137 |

## Samples per design level

### `grp`
- **T3** (13): GSM1489559 / 103; GSM1489564 / 159; GSM1489570 / 137; GSM1489574 / 193; GSM1489581 / 125; GSM1489585 / 154; GSM1489592 / 115; GSM1489597 / 120; GSM1489602 / 171; GSM1489609 / 156; GSM1489611 / 181; GSM1489616 / 142; GSM1489622 / 176
- **T4** (10): GSM1489560 / 119; GSM1489565 / 175; GSM1489571 / 153; GSM1489575 / 114; GSM1489586 / 170; GSM1489598 / 136; GSM1489603 / 187; GSM1489612 / 102; GSM1489617 / 158; GSM1489623 / 192
- **U2** (21): GSM1489558 / 221; GSM1489561 / 190; GSM1489566 / 151; GSM1489569 / 203; GSM1489572 / 129; GSM1489576 / 185; GSM1489579 / 204; GSM1489580 / 209; GSM1489582 / 117; GSM1489587 / 146; GSM1489590 / 215; GSM1489591 / 210; GSM1489593 / 107; GSM1489596 / 216; GSM1489599 / 112; GSM1489604 / 163; GSM1489607 / 222; GSM1489608 / 124; GSM1489613 / 173; GSM1489618 / 134; GSM1489621 / 188
- **U3** (12): GSM1489562 / 111; GSM1489567 / 167; GSM1489577 / 106; GSM1489583 / 133; GSM1489588 / 162; GSM1489594 / 123; GSM1489600 / 128; GSM1489605 / 179; GSM1489610 / 164; GSM1489614 / 189; GSM1489619 / 150; GSM1489624 / 184
- **U4** (12): GSM1489563 / 127; GSM1489568 / 183; GSM1489573 / 161; GSM1489578 / 122; GSM1489584 / 149; GSM1489589 / 178; GSM1489595 / 139; GSM1489601 / 144; GSM1489606 / 195; GSM1489615 / 110; GSM1489620 / 166; GSM1489625 / 105

### `subject`
- **S1** (4): GSM1489581 / 125; GSM1489582 / 117; GSM1489583 / 133; GSM1489584 / 149
- **S11** (1): GSM1489558 / 221
- **S12** (5): GSM1489559 / 103; GSM1489560 / 119; GSM1489561 / 190; GSM1489562 / 111; GSM1489563 / 127
- **S13** (5): GSM1489564 / 159; GSM1489565 / 175; GSM1489566 / 151; GSM1489567 / 167; GSM1489568 / 183
- **S14** (1): GSM1489569 / 203
- **S15** (4): GSM1489570 / 137; GSM1489571 / 153; GSM1489572 / 129; GSM1489573 / 161
- **S16** (5): GSM1489574 / 193; GSM1489575 / 114; GSM1489576 / 185; GSM1489577 / 106; GSM1489578 / 122
- **S18** (1): GSM1489579 / 204
- **S19** (1): GSM1489580 / 209
- **S2** (1): GSM1489608 / 124
- **S20** (5): GSM1489585 / 154; GSM1489586 / 170; GSM1489587 / 146; GSM1489588 / 162; GSM1489589 / 178
- **S21** (1): GSM1489590 / 215
- **S22** (1): GSM1489591 / 210
- **S23** (4): GSM1489592 / 115; GSM1489593 / 107; GSM1489594 / 123; GSM1489595 / 139
- **S24** (1): GSM1489596 / 216
- **S26** (5): GSM1489597 / 120; GSM1489598 / 136; GSM1489599 / 112; GSM1489600 / 128; GSM1489601 / 144
- **S27** (5): GSM1489602 / 171; GSM1489603 / 187; GSM1489604 / 163; GSM1489605 / 179; GSM1489606 / 195
- **S28** (1): GSM1489607 / 222
- **S3** (2): GSM1489609 / 156; GSM1489610 / 164
- **S4** (5): GSM1489611 / 181; GSM1489612 / 102; GSM1489613 / 173; GSM1489614 / 189; GSM1489615 / 110
- **S5** (5): GSM1489616 / 142; GSM1489617 / 158; GSM1489618 / 134; GSM1489619 / 150; GSM1489620 / 166
- **S7** (1): GSM1489621 / 188
- **S9** (4): GSM1489622 / 176; GSM1489623 / 192; GSM1489624 / 184; GSM1489625 / 105

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE58608", "GSE60590", "GSE60833"], "this_accession_holds": "U2 (untrained leg after Period 1, n=21), T3/U3 (both legs before Period 2, n=13/12), T4/U4 (both legs after Period 2, n=10/12); T1/T2 (Period 1 trained-leg pre/post) are deposited in GSE58608/GSE60590, not here", "assay": "bulk RNA-seq, human vastus lateralis, Illumina HiSeq 2000 paired-end; TopHat/Cufflinks FPKM and HTSeq gene counts (S4.5.p1)", "design": "one-legged endurance training: Period 1 trains one leg (T), other leg untrained (U); after 9-month break Period 2 trains both legs (S2.1.p1, S4.2.p1-p2, FIG1)", "factors": {"leg": ["T (trained in Period 1)", "U (untrained in Period 1)"], "time": ["1 pre-P1", "2 post-P1", "3 pre-P2", "4 post-P2"]}, "repeated_measure_unit": "subject (both legs and all time points from the same individual)", "primary_estimand": "within-subject effect of 3-month one-legged endurance training on skeletal muscle gene expression; in this accession: Period 2 training response in the previously trained leg (T4 vs T3) and in the previously untrained leg (U4 vs U3)", "planned_contrasts": ["T4 vs T3 (Period 2, previously trained leg; S2.4.p2: 852 genes, n=10 individuals FIG2c)", "U4 vs U3 (Period 2, previously untrained leg; S2.4.p2: 928 genes, n=11 individuals FIG2d)", "T3 vs U3 (memory, before Period 2; S2.4.p1: no specific genes differed)", "T4 vs U4 (after Period 2; S2.4.p2: OPLS no statistical difference)", "T2 vs T1 and U2 vs T1 (Period 1; need GSE58608/GSE60590, out o ... [938 more characters]

reasoning: Study map from S2.1, S2.4, S4.2, S4.5, S4.6. Gene-level DEG counts for Period 2 come from the OPLS loading/jack-knife rule (S2.2.p1 'From the loading values of the OPLS models, we identified significant differentially expressed isoforms and genes'; S2.4.p2 852/928). GSE60833 holds only U2/T3/T4/U3/U4, so the Period 1 primary contrast is outside this accession.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833_gene_fpkm_merged.csv", "owned": true, "checks": ["S4.10.p1 and S7.p1 list GSE60833", "metadata original sample ids encode subject+leg+timepoint (e.g. 12T3) matching the paper's T/U x 2/3/4 scheme", "Homo sapiens skeletal muscle, HiSeq 2000, TopHat 2.0.4 / Cufflinks, hg19 ENSEMBL v71 as in S4.5.p1", "68 samples = 21 U2 + 13 T3 + 10 T4 + 12 U3 + 12 U4"], "accession": "GSE60833", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE60833\\GSE60833_metadata.csv"}

reasoning: The paper names GSE60833 in its data-availability statements; the sample naming and processing match. Matrix = per-sample Cufflinks gene FPKM files from GSE60833_RAW.tar merged by prep_merge_fpkm.py (columns are GSM ids).

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 68, "n_metadata": 68, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\aligned\\aligned_metadata.csv", "columns": {"sex": {"alias_of": "characteristics_ch1.1.gender"}, "location": {"alias_of": "characteristics_ch1.2.biopsy location"}, "subject": {"source": "characteristics_ch1.5.original sample id", "regex": "^(\\d+)[TU]\\d$", "recode": {"1": "S1", "2": "S2", "3": "S3", "4": "S4", "5": "S5", "7": "S7", "9": "S9", "11": "S11", "12": "S12", "13": "S13", "14": "S14", "15": "S15", "16": "S16", "18": "S18", "19": "S19", "20": "S20", "21": "S21", "22": "S22", "23": "S23", "24": "S24", "26": "S26", "27": "S27", "28": "S28"}}, "grp": {"source": "characteristics_ch1.5.original sample id", "regex": "^\\d+([TU]\\d)$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\aligned\\design_metadata.csv", "sha256": "7196f4a70daab87898a701b09a58b086fdc31b4c5b49707d22bed71b185282b7", "levels": {"sex": {"male": 36, "female": 32}, "location": {"left leg": 39, "right leg": 29}, "subject": {"S12": 5, "S13": 5, "S16": 5, "S20": 5, "S26": 5, "S27": 5, "S4": 5, "S5": 5, "S15": 4, "S1": 4, "S23": 4, "S9": 4, "S3": 2, "S11": 1, "S14": 1, "S18": 1, "S19": 1, "S21": 1, "S22": 1, "S24": 1, "S28 ... [85 more characters]

reasoning: Matrix columns are GSM ids (prep script names them from the tar member names) and equal the metadata index exactly. subject and grp (leg+timepoint, T3/T4/U2/U3/U4) are parsed from 'original sample id' (e.g. 12T3); subject recoded to S<n> so it is a categorical factor. The metadata 'exercise status' column (trained/untrained) describes training state at the biopsy, not the leg, so it is not used; the leg is the T/U letter. Each subject-leg maps to one biopsy side and each subject to one sex (checked).

### matrix (valid, not_started)

final: {"matrix_type": "fpkm_or_tpm", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\aligned\\aligned_matrix.csv", "sha256": "be8c57b9b849d7f8cc7341f9540c43742a3b91bea801f33b237e5286668b911d", "n_features": 61779, "n_samples": 68, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 87763.4, "median": 0.0, "integer_fraction": 0.584, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Per-sample files are Cufflinks genes.fpkm_tracking (columns FPKM, FPKM_conf_lo/hi); data_processing names Cufflinks; non-integer values. The paper's gene-level DE input was batch-corrected FPKM (S4.5.p1), so FPKM is the paper's input type, but without ComBat correction (batch labels are not in GEO). HTSeq counts mentioned in S4.5.p1 are not deposited. 131 duplicated Cufflinks tracking_ids (genes split over loci) were summed per gene in prep.

### design (valid, not_started)

final: {"analysis_type": "paired two-group (within-subject pre vs post), one fit per leg", "design_column": "grp", "contrasts": [{"name": "grp_T4_vs_T3", "control": "T3", "treatment": "T4", "role": "primary"}, {"name": "grp_U4_vs_U3", "control": "U3", "treatment": "U4", "role": "primary"}, {"name": "grp_T3_vs_U3", "control": "U3", "treatment": "T3", "role": "exploratory"}, {"name": "grp_T4_vs_U4", "control": "U4", "treatment": "T4", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\suitability\\suitability.md", "n_comparisons": 10, "n_analyzable": 10}}

reasoning: S2.4.p2 compares pre vs post Period 2 within each leg (T3 vs T4, U3 vs U4) on paired individuals (FIG2c n=10, FIG2d n=11). These are the exercise contrasts this accession supports. T3 vs U3 and T4 vs U4 (S2.4.p1-p2) are leg comparisons (memory), kept exploratory and associational to prior training.

rejected alternatives: [{"value": "exercise status (trained vs untrained) as design column", "reason_rejected": "mixes U2/T3/U3 (all 'untrained') against T4/U4 and confounds time with training state; not a paper contrast"}, {"value": "U2 vs T1 / T2 vs T1 (Period 1)", "reason_rejected": "T1 and T2 are not in GSE60833"}, {"value": "U3 vs U2", "reason_rejected": "detraining time effect in an untrained leg, not an exercise contrast and not analysed in the paper"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "blocking (paired pre/post within subject)"}, {"name": "sex", "disposition": "not added: constant within subject, absorbed by subject blocking"}, {"name": "location", "disposition": "not added: left/right leg is constant within subject-leg, absorbed by subject in the per-leg fits"}, {"name": "sequencing batch", "disposition": "not available in GEO; paper used ComBat; recorded as caveat"}], "design_check": {"formula_equivalent": "~ C(grp) + C(subject)", "n_samples": 68, "n_columns": 27, "columns": ["Intercept", "grp_T4", "grp_U2", "grp_U3", "grp_U4", "subject_S11", "subject_S12", "subject_S13", "subject_S14", "subject_S15", "subject_S16", "subject_S18", "subject_S19", "subject_S2", "subject_S20", "subject_S21", "subject_S22", "subject_S23", "subject_S24", "subject_S26", "subject_S27", "subject_S28", "subject_S3", "subject_S4", "subject_S5", "subject_S7", "subject_S9"], "rank": 27, "full_rank": true, "residual_df": 41, "levels": {"grp": {"U2": 21, "T3": 13, "U3": 12, "U4": 12, "T4": 10}, "subject": {"S12": 5, "S13": 5, "S16": 5, "S20": 5, "S26": 5, "S27": 5, "S4": 5, "S5": 5, "S15": 4, "S1": 4, "S23": 4, "S9": 4, "S3": 2, "S11": 1, "S14": 1, "S18": 1, "S19": 1, "S21": 1, "S22": 1, "S24": 1, "S28": 1, "S2": 1, "S7": 1}}, "cells": [{"cell": ["T3", "S1"], "n": 1}, {"cell": ["T3", "S12"], "n": 1}, {"cell": ["T3", "S13"], "n": 1}, {"cell": ["T3", "S15"], "n": 1}, {"cell": ["T3", " ... [2635 more characters]

reasoning: Repeated biopsies from the same individuals (S2.1.p1); pre/post pairs blocked by subject. Sex and biopsy side do not vary within a subject-leg, so subject blocking removes them. Paper ComBat batch correction cannot be reproduced because batch labels are absent.

### method (valid, not_started)

final: {"matrix_type": "fpkm_or_tpm", "method": "limma (moderated t, ~ subject + grp) on log2(FPKM+1), genes with mean FPKM >= 1 in the fitted samples", "formula": "~ subject + grp", "paper_route": {"method": "OPLS (Simca) jack-knife loading significance on ComBat-corrected FPKM", "status": "blocked", "reason": "proprietary Simca OPLS with jack-knife loading CI has no executor in this repository, and ComBat batch labels are not deposited"}, "deviations": ["limma paired moderated t replaces OPLS loading significance", "no ComBat batch correction (batches unknown)", "gene filter mean FPKM >= 1 per fit instead of > 1 over the paper's sample set"], "transform": "log2(x+1)"}

reasoning: FPKM supports limma on log2(FPKM+1) (matrix-method policy). The paper's own univariate tool is limma (S4.5.p1, S4.8.p1); the gene-level OPLS route is blocked. Paired by subject as in the repeated-measures design.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "OPLS_jackknife_loading", "cutoff": 0.01, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "The paper's gene rule (|OPLS loading| - |jack-knife 99% CI| > 0, S4.6.p2) has no p-value equivalent; BH-adjusted p < 0.05 with no fold-change rule is the workflow default (and matches the paper's limma rule for novel transcripts, TAB3 adj p <= 0.05)."}

reasoning: S4.6.p2 defines significance by OPLS loadings; not convertible to padj, so workflow default is used and labelled.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "P2_trained_leg_T4_vs_T3", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_trained_leg_T4_vs_T3\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_trained_leg_T4_vs_T3\\DEG_results_T4_vs_T3.csv"], "counts": {"P2_trained_leg_T4_vs_T3": {"applied": {"rule": "padj < 0.05", "n_tested": 13133, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.01", "n_tested": 13133, "n_significant": 409, "n_up": 161, "n_down": 248, "deg_sanity": "ok"}}}}

reasoning: S2.4.p2 T3 vs T4, paired by subject (FIG2c n=10); mean FPKM >= 1 filter mirrors S4.6.p1.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "P2_untrained_leg_U4_vs_U3", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 22, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_untrained_leg_U4_vs_U3\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_untrained_leg_U4_vs_U3\\DEG_results_U4_vs_U3.csv"], "counts": {"P2_untrained_leg_U4_vs_U3": {"applied": {"rule": "padj < 0.05", "n_tested": 13144, "n_significant": 6, "n_up": 6, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.01", "n_tested": 13144, "n_significant": 646, "n_up": 489, "n_down": 157, "deg_sanity": "ok"}}}}

reasoning: S2.4.p2 U3 vs U4, paired by subject (FIG2d n=11).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "leg_T3_vs_U3", "role": "exploratory", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 24, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\leg_T3_vs_U3\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\leg_T3_vs_U3\\DEG_results_T3_vs_U3.csv"], "counts": {"leg_T3_vs_U3": {"applied": {"rule": "padj < 0.05", "n_tested": 13035, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.01", "n_tested": 13035, "n_significant": 531, "n_up": 393, "n_down": 138, "deg_sanity": "ok"}}}}

reasoning: S2.4.p1 memory test: previously trained vs untrained leg before Period 2, paired by subject; paper found no specific genes.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "leg_T4_vs_U4", "role": "exploratory", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\leg_T4_vs_U4\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\leg_T4_vs_U4\\DEG_results_T4_vs_U4.csv"], "counts": {"leg_T4_vs_U4": {"applied": {"rule": "padj < 0.05", "n_tested": 13124, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.01", "n_tested": 13124, "n_significant": 36, "n_up": 8, "n_down": 28, "deg_sanity": "ok"}}}}

reasoning: S2.4.p2: legs after Period 2; paper OPLS found no difference.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "P2_trained_leg_T4_vs_T3_female", "role": "exploratory", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_trained_leg_T4_vs_T3_female\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_trained_leg_T4_vs_T3_female\\DEG_results_T4_vs_T3.csv"], "counts": {"P2_trained_leg_T4_vs_T3_female": {"applied": {"rule": "padj < 0.05", "n_tested": 13217, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.01", "n_tested": 13217, "n_significant": 233, "n_up": 74, "n_down": 159, "deg_sanity": "ok"}}}}

reasoning: Per-sex split (suitability split_plan); paper pooled sexes and found no sex-specific training response (S2.1.p4).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "P2_trained_leg_T4_vs_T3_male", "role": "exploratory", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_trained_leg_T4_vs_T3_male\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_trained_leg_T4_vs_T3_male\\DEG_results_T4_vs_T3.csv"], "counts": {"P2_trained_leg_T4_vs_T3_male": {"applied": {"rule": "padj < 0.05", "n_tested": 12964, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.01", "n_tested": 12964, "n_significant": 60, "n_up": 33, "n_down": 27, "deg_sanity": "ok"}}}}

reasoning: Per-sex split (suitability split_plan); S2.1.p4.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "P2_untrained_leg_U4_vs_U3_female", "role": "exploratory", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_untrained_leg_U4_vs_U3_female\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_untrained_leg_U4_vs_U3_female\\DEG_results_U4_vs_U3.csv"], "counts": {"P2_untrained_leg_U4_vs_U3_female": {"applied": {"rule": "padj < 0.05", "n_tested": 13136, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.01", "n_tested": 13136, "n_significant": 163, "n_up": 120, "n_down": 43, "deg_sanity": "ok"}}}}

reasoning: Per-sex split (suitability split_plan); S2.1.p4.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "P2_untrained_leg_U4_vs_U3_male", "role": "exploratory", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_untrained_leg_U4_vs_U3_male\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\P2_untrained_leg_U4_vs_U3_male\\DEG_results_U4_vs_U3.csv"], "counts": {"P2_untrained_leg_U4_vs_U3_male": {"applied": {"rule": "padj < 0.05", "n_tested": 13030, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.01", "n_tested": 13030, "n_significant": 250, "n_up": 176, "n_down": 74, "deg_sanity": "ok"}}}}

reasoning: Per-sex split (suitability split_plan); S2.1.p4.

### enrichment (valid, not_run)

final: {"organism": "Human", "subset": "P2_trained_leg_T4_vs_T3", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "reason_not_run": "no gene passes the ORA input threshold"}

reasoning: paper reports GO/KEGG/IPA for Period 2 (S2.5.p1, oxidative phosphorylation)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "P2_trained_leg_T4_vs_T3", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\enrichment_P2_trained_leg_T4_vs_T3\\gsea\\DEG_results_T4_vs_T3_GSEA_Hallmark.csv"], "summary": "GSEA complete on 11922 Human genes ranked by 'stat'. 50 Hallmark sets tested, 25 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.69 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.48 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.01 | NOM p=0.00e+00 | FDR q=1.97e-03 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.85 | NOM p=0.00e+00 | FDR q=8.37e-03 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.83 | NOM p=2.71e-03 | FDR q=7.49e-03 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.74 | NOM p=0.00e+00 | FDR q=7.88e-03 - HALLMARK_ANGIOGENESIS | NES=1.69 | NOM p=1.47e-02 | FDR q=1.18e-02 - HALLMARK_MYC_TARGETS_V2 | NES=1.69 | NOM p=0.00e+00 | FDR q=1.08e-02 - HALLMARK_GLYCOLYSIS | NES=1.68 | NOM p=0.00e+00 | FDR q=1.01e-02 - HALLMARK_PEROXISOME | NES=1.51 | NOM p=5.95e-03 | FDR q=3.90e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_G2M_CHECKPOINT | NES=-1.64 | NOM p=0.00e+00 | FDR q=6.47e-02 - HALLMARK_UV_RESPONSE_DN | NES=-1.5 ... [427 more characters]

reasoning: paper reports GO/KEGG/IPA for Period 2 (S2.5.p1, oxidative phosphorylation)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "P2_untrained_leg_U4_vs_U3", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\enrichment_P2_untrained_leg_U4_vs_U3\\ora\\DEG_results_U4_vs_U3_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\enrichment_P2_untrained_leg_U4_vs_U3\\ora\\DEG_results_U4_vs_U3_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\enrichment_P2_untrained_leg_U4_vs_U3\\ora\\DEG_results_U4_vs_U3_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\enrichment_P2_untrained_leg_U4_vs_U3\\ora\\DEG_results_U4_vs_U3_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 6 Human genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Skin Morphog ... [1329 more characters]

reasoning: paper reports enrichment for both Period 2 legs (S2.5.p1)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "P2_untrained_leg_U4_vs_U3", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\ef574c2d9b2d7f168faeb39ddc5cb09258575c41\\GSE60833\\results\\enrichment_P2_untrained_leg_U4_vs_U3\\gsea\\DEG_results_U4_vs_U3_GSEA_Hallmark.csv"], "summary": "GSEA complete on 11945 Human genes ranked by 'stat'. 50 Hallmark sets tested, 25 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.64 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.37 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.87 | NOM p=0.00e+00 | FDR q=1.52e-03 - HALLMARK_PEROXISOME | NES=1.82 | NOM p=0.00e+00 | FDR q=1.83e-03 - HALLMARK_BILE_ACID_METABOLISM | NES=1.81 | NOM p=0.00e+00 | FDR q=1.52e-03 - HALLMARK_ANGIOGENESIS | NES=1.81 | NOM p=1.37e-03 | FDR q=1.45e-03 - HALLMARK_ANDROGEN_RESPONSE | NES=1.68 | NOM p=2.38e-03 | FDR q=9.76e-03 - HALLMARK_PROTEIN_SECRETION | NES=1.65 | NOM p=3.56e-03 | FDR q=1.13e-02 - HALLMARK_KRAS_SIGNALING_UP | NES=1.52 | NOM p=1.40e-02 | FDR q=4.52e-02 ### Top 7 DOWN (NES < 0, depleted in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-1.83 | NOM p=0.00e+00 | FDR q=7.38e-03 - HALLMARK_MYOGENESIS | NES=-1.38 | NOM  ... [432 more characters]

reasoning: paper reports enrichment for both Period 2 legs (S2.5.p1)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Period 1 (T1/T2, paper 2,394 genes) is not in GSE60833 and was not analysed", "paper counts come from OPLS on ComBat-corrected FPKM; ours are limma padj < 0.05 on uncorrected FPKM, so counts are not directly comparable", "T3 vs U3 and T4 vs U4 are leg comparisons (associational to prior training), exploratory; T3 vs U3 shows 0 padj<0.05 genes (agrees with paper) but an excess of nominal p<0.05 genes (1784/13035), consistent with unmodelled sequencing batch rather than memory", "direction agrees with the paper: the named OXPHOS/collagen genes have positive log2FC in both Period 2 legs, and GSEA Hallmark oxidative phosphorylation is the top up-regulated set in both legs, but under BH 0.05 the trained leg has 0 DEGs and the untrained leg 6 vs the paper's 852/928", "per-sex analyses are exploratory with 4-6 pairs per sex"], "results": {"P2_trained_leg_T4_vs_T3": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 409}, "P2_untrained_leg_U4_vs_U3": {"n_deg": 6, "up": 6, "down": 0, "rule": "padj < 0.05", "audit_n": 646}, "leg_T3_vs_U3": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 531}, "leg_T4_vs_U4": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 36}, "P2_trained_leg_T4_vs_T3_female": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 233}, "P2_trained_leg_T4_vs_T3_male": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 60}, "P2_untrained_leg_U4_ ... [2334 more characters]

reasoning: Genes named in S2.2.p3 as changed in Period 1 and both legs in Period 2 (isoform level): COL4A1, COL4A2, HADHB, PDHA1, COX4I1, COX5A, NDUFB5, SDHB, UQCRC2 (Ensembl IDs; NDUFA3 omitted because Cufflinks reports several Ensembl IDs for it).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); location: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); sex: omit (makes the design rank deficient); location: omit (makes the design rank deficient) |
- | Sex | pass | Sex inference completed on 68 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "Period 1 samples",
    "paper": "T1/T2 central to the paper (2,394 genes)",
    "data": "GSE60833 holds U2, T3, T4, U3, U4 only",
    "disposition": "out_of_scope_for_this_accession"
  },
  {
    "item": "DE method",
    "paper": "OPLS jack-knife loadings on ComBat-corrected FPKM",
    "data": "per-sample uncorrected Cufflinks FPKM, no batch labels",
    "disposition": "declared_deviation"
  },
  {
    "item": "Sample sizes",
    "paper": "T3vsT4 n=10 individuals, U3vsU4 n=11",
    "data": "complete pairs T3/T4 = 10, U3/U4 = 11",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE60833 / PMC5033478 (endurance training, skeletal muscle memory)

## What ran
- Inspect: `inspect_GSE60833.json`. GSE60833 has 68 samples: U2 (untrained leg after Period 1, 21), T3 (13) and U3 (12), both legs before Period 2, and T4 (10) and U4 (12), both legs after Period 2. T1 and T2 (Period 1, trained leg before and after) are deposited in GSE58608/GSE60590, not in this series.
- Matrix: the per-sample Cufflinks `genes.fpkm_tracking` files in `GSE60833_RAW.tar`, merged by `prep_merge_fpkm.py` into `GSE60833_gene_fpkm_merged.csv` (61,779 Ensembl genes x 68 GSM). 131 duplicated tracking_ids (genes Cufflinks split over several loci) were summed per gene.
- Spec: `case_spec.json`, run with `python -m tools.case_runner execute`. Status completed; validator: 21 records, 0 errors.
- Alignment: exact match on the GSM index. `subject` and `grp` (T3/T4/U2/U3/U4) were parsed from `original sample id`, for example 12T3. Each subject-leg has one biopsy side and each subject one sex. Suitability verdict: analyzable, and the sex check passed.
- Method (declared deviation): limma `~ subject + grp` on log2(FPKM+1), paired with complete pairs per comparison, keeping genes with mean FPKM >= 1 in the fitted samples (about 13.1k genes, close to the paper's 12,848).
  - The paper's route was blocked: OPLS (Simca) with jack-knife loading significance on ComBat-corrected FPKM. There is no executor for it, and the batch labels are not deposited.
- Threshold: `workflow_default`, BH padj < 0.05 with no fold-change rule.
  - The paper's gene rule is |OPLS loading| - |jack-knife 99% CI| > 0 (S4.6.p2), which cannot be converted to a p-value rule.
  - Audit rule: nominal p < 0.01.
- Enrichment: GSEA Hallmark and ORA on the two primary contrasts. ORA was not run for T4 vs T3 because it had 0 DEGs.

## DEG counts vs paper (ours at padj < 0.05; audit count at p < 0.01 in brackets)
| Contrast | n pairs | Ours | Paper (OPLS) |
|---|---|---|---|
| T4 vs T3, Period 2 previously trained leg (primary) | 10 | 0 [409] | 852 |
| U4 vs U3, Period 2 previously untrained leg (primary) | 11 | 6, all up [646] | 928 |
| T3 vs U3, memory before Period 2 (exploratory) | 12 | 0 [531] | 0 (no specific genes) |
| T4 vs U4, after Period 2 (exploratory) | 10 | 0 [36] | no OPLS difference |
| Per-sex splits of both primary contrasts (exploratory) | 5-6 | 0 each | paper: no sex-specific response |

- Direction agrees with the paper:
  - COL4A1, COL4A2, HADHB, PDHA1, COX4I1, COX5A, NDUFB5, SDHB an ... [1696 more characters]
