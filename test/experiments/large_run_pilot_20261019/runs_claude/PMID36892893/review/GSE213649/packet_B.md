# Review packet B (the analysis' decisions): GSE213649

## Mechanical flags

- **other_rule_matches_paper**: {"table": "deseq2_PFC/grp_LPAEx_vs_CONSed_tissue-PFC", "paper": 170, "applied": 59, "applied_rule": "padj < 0.1 and |log2FoldChange| > 1", "closest_rule": "padj<0.05 & |lfc|>0.584963", "closest_n": 186, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deseq2_PFC/grp_LPAEx_vs_LPASed_tissue-PFC | 317 | 295 | padj < 0.1 and |log2FoldChange| > 1 | 1061 | 581 | 203 | 1874 | 3474 | 1572 | 664 | 1667 | 0.164 | 0.151 |
| deseq2_PFC/grp_LPAEx_vs_LPSed_tissue-PFC | 203 | 169 | padj < 0.1 and |log2FoldChange| > 1 | 642 | 336 | 95 | 1069 | 2850 | 1330 | 632 | 1246 | 0.163 | 0.124 |
| deseq2_PFC/grp_LPAEx_vs_CONSed_tissue-PFC | 170 | 59 | padj < 0.1 and |log2FoldChange| > 1 | 441 | 186 | 37 | 827 | 2752 | 1236 | 618 | 1140 | 0.174 | 0.12 |
| deseq2_PFC/grp_LPAEx_vs_LPEx_tissue-PFC | 14 | 8 | padj < 0.1 and |log2FoldChange| > 1 | 3 | 3 | 3 | 8 | 1298 | 794 | 493 | 373 | 0.172 | 0.057 |
| deseq2_PFC/grp_LPAEx_vs_CONEx_tissue-PFC | 4 | 2 | padj < 0.1 and |log2FoldChange| > 1 | 157 | 17 | 1 | 264 | 1726 | 715 | 378 | 643 | 0.158 | 0.075 |
| deseq2_LIV/grp_LPAEx_vs_CONEx_tissue-LIV | 258 | 287 | padj < 0.1 and |log2FoldChange| > 1 | 121 | 119 | 113 | 337 | 1713 | 1216 | 820 | 708 | 0.204 | 0.077 |
| deseq2_LIV/grp_LPAEx_vs_LPSed_tissue-LIV | 143 | 150 | padj < 0.1 and |log2FoldChange| > 1 | 49 | 49 | 47 | 169 | 1547 | 1105 | 760 | 605 | 0.195 | 0.07 |
| deseq2_LIV/grp_LPAEx_vs_LPASed_tissue-LIV | 112 | 97 | padj < 0.1 and |log2FoldChange| > 1 | 38 | 37 | 36 | 106 | 1505 | 1106 | 763 | 577 | 0.207 | 0.068 |
| deseq2_LIV/grp_LPAEx_vs_CONSed_tissue-LIV | 73 | 71 | padj < 0.1 and |log2FoldChange| > 1 | 52 | 47 | 38 | 93 | 1567 | 1016 | 682 | 545 | 0.197 | 0.071 |
| deseq2_LIV/grp_LPAEx_vs_LPEx_tissue-LIV | 19 | 15 | padj < 0.1 and |log2FoldChange| > 1 | 12 | 12 | 11 | 16 | 1117 | 694 | 464 | 313 | 0.208 | 0.05 |
| deseq2_MUS/grp_LPAEx_vs_CONEx_tissue-MUS | 15 | 22 | padj < 0.1 and |log2FoldChange| > 1 | 168 | 45 | 17 | 303 | 1777 | 590 | 327 | 666 | 0.202 | 0.084 |
| deseq2_HIP/grp_LPAEx_vs_CONSed_tissue-HIP | 19 | 8 | padj < 0.1 and |log2FoldChange| > 1 | 2 | 2 | 2 | 9 | 1855 | 805 | 409 | 514 | 0.179 | 0.079 |

## Samples per design level

### `grp`
- **CONEx** (30): GSM6591374 / PFC_CE5; GSM6591375 / PFC_CE7; GSM6591376 / PFC_CE9; GSM6591377 / PFC_CE10; GSM6591378 / PFC_CE11; GSM6591379 / PFC_CE12; GSM6591410 / HippoCE5; GSM6591411 / HippoCE7; GSM6591412 / HippoCE9; GSM6591413 / HippoCE10; GSM6591414 / HippoCE11; GSM6591415 / HippoCE12; GSM6591446 / L_CE5; GSM6591447 / L_CE7; GSM6591448 / L_CE9; GSM6591449 / L_CE10; GSM6591450 / L_CE11; GSM6591451 / L_CE12; GSM6591481 / C_CE5; GSM6591482 / C_CE7; GSM6591483 / C_CE9; GSM6591484 / C_CE10; GSM6591485 / C_CE11; GSM6591486 / C_CE12; GSM6591517 / M_CE5; GSM6591518 / M_CE7; GSM6591519 / M_CE9; GSM6591520 / M_CE10; GSM6591521 / M_CE11; GSM6591522 / M_CE12
- **CONSed** (30): GSM6591368 / PFC_CS3; GSM6591369 / PFC_CS4; GSM6591370 / PFC_CS6; GSM6591371 / PFC_CS7; GSM6591372 / PFC_CS8; GSM6591373 / PFC_CS10; GSM6591404 / HippoCS3; GSM6591405 / HippoCS4; GSM6591406 / HippoCS6; GSM6591407 / HippoCS7; GSM6591408 / HippoCS8; GSM6591409 / HippoCS10; GSM6591440 / L_CS3; GSM6591441 / L_CS4; GSM6591442 / L_CS6; GSM6591443 / L_CS7; GSM6591444 / L_CS8; GSM6591445 / L_CS10; GSM6591475 / C_CS3; GSM6591476 / C_CS4; GSM6591477 / C_CS6; GSM6591478 / C_CS7; GSM6591479 / C_CS8; GSM6591480 / C_CS10; GSM6591511 / M_CS3; GSM6591512 / M_CS4; GSM6591513 / M_CS6; GSM6591514 / M_CS7; GSM6591515 / M_CS8; GSM6591516 / M_CS10
- **LPAEx** (29): GSM6591398 / PFC_AE4; GSM6591399 / PFC_AE6; GSM6591400 / PFC_AE7; GSM6591401 / PFC_AE9; GSM6591402 / PFC_AE11; GSM6591403 / PFC_AE12; GSM6591434 / HippoAE4; GSM6591435 / HippoAE6; GSM6591436 / HippoAE7; GSM6591437 / HippoAE9; GSM6591438 / HippoAE11; GSM6591439 / HippoAE12; GSM6591469 / L_AE4; GSM6591470 / L_AE6; GSM6591472 / L_AE9; GSM6591473 / L_AE11; GSM6591474 / L_AE12; GSM6591505 / C_AE4; GSM6591506 / C_AE6; GSM6591507 / C_AE7; GSM6591508 / C_AE9; GSM6591509 / C_AE11; GSM6591510 / C_AE12; GSM6591541 / M_AE4; GSM6591542 / M_AE6; GSM6591543 / M_AE7; GSM6591544 / M_AE9; GSM6591545 / M_AE11; GSM6591546 / M_AE12
- **LPASed** (30): GSM6591392 / PFC_AS4; GSM6591393 / PFC_AS5; GSM6591394 / PFC_AS6; GSM6591395 / PFC_AS7; GSM6591396 / PFC_AS9; GSM6591397 / PFC_AS11; GSM6591428 / HippoAS4; GSM6591429 / HippoAS5; GSM6591430 / HippoAS6; GSM6591431 / HippoAS7; GSM6591432 / HippoAS9; GSM6591433 / HippoAS11; GSM6591463 / L_AS4; GSM6591464 / L_AS5; GSM6591465 / L_AS6; GSM6591466 / L_AS7; GSM6591467 / L_AS9; GSM6591468 / L_AS11; GSM6591499 / C_AS4; GSM6591500 / C_AS5; GSM6591501 / C_AS6; GSM6591502 / C_AS7; GSM6591503 / C_AS9; GSM6591504 / C_AS11; GSM6591535 / M_AS4; GSM6591536 / M_AS5; GSM6591537 / M_AS6; GSM6591538 / M_AS7; GSM6591539 / M_AS9; GSM6591540 / M_AS11
- **LPEx** (28): GSM6591386 / PFC_PE3; GSM6591387 / PFC_PE4; GSM6591388 / PFC_PE6; GSM6591389 / PFC_PE8; GSM6591390 / PFC_PE10; GSM6591391 / PFC_PE11; GSM6591422 / HippoPE3; GSM6591423 / HippoPE4; GSM6591424 / HippoPE6; GSM6591425 / HippoPE8; GSM6591426 / HippoPE10; GSM6591427 / HippoPE11; GSM6591459 / L_PE6; GSM6591460 / L_PE8; GSM6591461 / L_PE10; GSM6591462 / L_PE11; GSM6591493 / C_PE3; GSM6591494 / C_PE4; GSM6591495 / C_PE6; GSM6591496 / C_PE8; GSM6591497 / C_PE10; GSM6591498 / C_PE11; GSM6591529 / M_PE3; GSM6591530 / M_PE4; GSM6591531 / M_PE6; GSM6591532 / M_PE8; GSM6591533 / M_PE10; GSM6591534 / M_PE11
- **LPSed** (30): GSM6591380 / PFC_PS4; GSM6591381 / PFC_PS5; GSM6591382 / PFC_PS7; GSM6591383 / PFC_PS8; GSM6591384 / PFC_PS10; GSM6591385 / PFC_PS13; GSM6591416 / HippoPS4; GSM6591417 / HippoPS5; GSM6591418 / HippoPS7; GSM6591419 / HippoPS8; GSM6591420 / HippoPS10; GSM6591421 / HippoPS13; GSM6591452 / L_PS4; GSM6591453 / L_PS5; GSM6591454 / L_PS7; GSM6591455 / L_PS8; GSM6591456 / L_PS10; GSM6591457 / L_PS13; GSM6591487 / C_PS4; GSM6591488 / C_PS5; GSM6591489 / C_PS7; GSM6591490 / C_PS8; GSM6591491 / C_PS10; GSM6591492 / C_PS13; GSM6591523 / M_PS4; GSM6591524 / M_PS5; GSM6591525 / M_PS7; GSM6591526 / M_PS8; GSM6591527 / M_PS10; GSM6591528 / M_PS13

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE213649"], "primary_estimand": "Per tissue (PFC, hippocampus, colon, liver, TA muscle), expression differences of each of the five other groups vs LPAEx (Ang(1-7) probiotic + exercise) in a 3x2 probiotic x exercise design; the exercise effect the paper interprets is LPAEx vs LPASed (S4.p4), with LPAEx vs LPSed/CONSed as combined-intervention contrasts.", "factors": {"probiotic": ["Control", "LP", "LPA"], "activity": ["Sed", "Ex"]}, "inclusion": "Aged (24 mo) male F344BN rats, n=4-6/group/tissue (S2.4.3.p1, TAB1); deposited 179 samples: 6/group/tissue except liver LPEx n=5 (LPEx3 liver absent, as in TAB1).", "planned_contrasts": ["LPAEx vs LPASed in each tissue (S2.4.3.2.p1)", "LPAEx vs LPSed in each tissue (S2.4.3.2.p1)", "LPAEx vs CONSed in each tissue (S2.4.3.2.p1)", "LPAEx vs CONEx in each tissue (S2.4.3.2.p1)", "LPAEx vs LPEx in each tissue (S2.4.3.2.p1)"], "paper_method": "DESeq2 ~group (6-level single factor) per tissue, R 4.1.2 (S2.4.3.2.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "source_locator": "S2.4.3.2.p1"}, "paper_results": "PFC: vs LPASed 317 (262/55), vs LPSed 203 (163/40), vs CONSed 170 (140/30), vs LPEx 14, vs CONEx 4 (TAB2). Liver: vs CONEx 258 (252/6), vs LPSed 143, vs LPASed 112 (105/7), vs CONSed 73 (63/10), vs LPEx 19 (TAB3). Muscle vs CONEx 15 (9/6); hippocampus vs CONSed 19 (5/14); other muscle/hippocampus/colon comparisons 2-14 (S3.4.p1)."}

reasoning: S2.4.3.2.p1: DESeq2 ~group, DEGs for all groups compared with LPAEx in each tissue, FDR<0.10 (BH) and |LFC|>1.0. FIG5 volcano/text report 'upregulated' as higher in LPAEx.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE213649\\GSE213649_ang1_7_all_tissues_read_counts__1_.csv", "owned": true, "checks": ["S5.p1 names GSE213649", "male F344BN rat, five tissues as in S2.3.p1", "animal IDs in titles (CS3, CE5, ..., AE12) match the transcriptomic rows of TAB1", "processing (Trim Galore, STAR, Rnor_5.0) matches S2.4.3.2.p1"], "accession": "GSE213649", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE213649\\GSE213649_metadata.csv"}

reasoning: Series, organism, tissues, animal IDs and processing all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 179, "n_metadata": 179, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM6591471": "L_AE7: labelled liver but expression is colon (Spearman r 0.94 to colon median vs 0.72 to liver; best Pearson match C_AE12 0.967)", "GSM6591458": "L_PE4: labelled liver but expression is skeletal muscle (Spearman r 0.96 to muscle median vs 0.68 to liver)"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\aligned\\aligned_metadata_kept.csv", "columns": {"tissue": {"source": "title", "regex": "^(PFC|Hippo|L|C|M)_?[CPA][SE]\\d+$", "recode": {"PFC": "PFC", "Hippo": "HIP", "L": "LIV", "C": "COL", "M": "MUS"}}, "grp": {"source": "title", "regex": "^(?:PFC_|Hippo|L_|C_|M_)([CPA][SE])\\d+$", "recode": {"CS": "CONSed", "CE": "CONEx", "PS": "LPSed", "PE": "LPEx", "AS": "LPASed", "AE": "LPAEx"}}, "qc": {"source": "title", "regex": "^(.+)$", "recode": {"PFC_CS3": "pass", "PFC_CS4": "pass", "PFC_CS6": "pass", "PFC_CS7": "pass", "PFC_CS8": "pass", "PFC_CS10": "pass", "PFC_CE5": "pass", "PFC_CE7": "pass", "PFC_CE9": "pass", "PFC_CE10": "pass", "PFC_CE11": "pass", "PFC_CE12": "pass", "PFC_PS4": "pass", "PFC_PS5": "pass", "PFC_PS7": "pass", "PFC_PS8": "pass", "PFC_PS10": "pass", "PFC_PS13": "pass", "PFC_PE3": "pass", "PFC_PE4": "pass", "PFC_PE6": "pass", "PFC_PE8": "pass", "PFC_PE10": "pass", "PFC_PE11": "pass", "PFC_AS4": "pass", "PFC_AS5": "pass", ... [3198 more characters]

reasoning: Matrix columns equal GEO titles (179/179). Title code = tissue prefix + C/P/A (Control/LP/LPA) + S/E (Sed/Ex) + animal number; codes agree with the treatment and activity characteristics. Tissue-identity check (Spearman correlation of each sample to per-tissue median log2CPM): L_AE7 is colon and L_PE4 is muscle although labelled liver; both are excluded as mislabelled before any model (paper reports n=4-6/group, consistent with exclusions). L_AE11 is liver with a colon component (r 0.94 to liver, 0.75 to colon); kept in the paper-aligned run and dropped in a sensitivity run (qc column).

### matrix (valid, not_started)

final: {"source": "GEO supplementary read_counts (data_processing: STAR gene counts)", "paper_input": "STAR gene counts into DESeq2", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\aligned\\aligned_matrix.csv", "sha256": "13430aeb03f92434e71a15300fdaae8a34df3bd3a92c9e1ac9e79278d68b0a06", "n_features": 32545, "n_samples": 177, "annotation_columns_dropped": ["GSM6591458", "GSM6591471"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3254167.0, "median": 1.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: 100% integers, max 3.25e6, median 1; data_processing: STAR gene counts, file contains read_counts.

### design (valid, not_started)

final: {"analysis_type": "multi-group, one model per tissue", "design_column": "grp", "formula": "~ grp", "contrasts": [{"name": "grp_LPAEx_vs_LPASed_tissue-PFC", "control": "LPASed", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_LPSed_tissue-PFC", "control": "LPSed", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_CONSed_tissue-PFC", "control": "CONSed", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_CONEx_tissue-PFC", "control": "CONEx", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_LPEx_tissue-PFC", "control": "LPEx", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_LPASed_tissue-HIP", "control": "LPASed", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_LPSed_tissue-HIP", "control": "LPSed", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_CONSed_tissue-HIP", "control": "CONSed", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_CONEx_tissue-HIP", "control": "CONEx", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_LPEx_tissue-HIP", "control": "LPEx", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_LPASed_tissue-LIV", "control": "LPASed", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_LPSed_tissue-LIV", "control": "LPSed", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_CONSed_tissue-LIV", "control": "CONSed", "treatment": "LPAEx", "role": "primary"}, {"name": "grp_LPAEx_vs_CONE ... [1460 more characters]

reasoning: Paper design ~group per tissue with LPAEx as comparator. Exercise-only simple effects within CON and LP (CONEx vs CONSed, LPEx vs LPSed) are not reported by the paper and run as exploratory from the same fit.

rejected alternatives: [{"value": "factorial ~probiotic*activity", "reason_rejected": "paper explicitly chose the ~group single factor (S2.4.3.2.p1); exercise main effect not reported"}, {"value": "one model across all tissues", "reason_rejected": "paper analyzes each tissue separately"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 177, "n_columns": 6, "columns": ["Intercept", "grp_CONSed", "grp_LPAEx", "grp_LPASed", "grp_LPEx", "grp_LPSed"], "rank": 6, "full_rank": true, "residual_df": 171, "levels": {"grp": {"CONSed": 30, "CONEx": 30, "LPSed": 30, "LPASed": 30, "LPAEx": 29, "LPEx": 28}}, "cells": [{"cell": ["CONEx"], "n": 30}, {"cell": ["CONSed"], "n": 30}, {"cell": ["LPAEx"], "n": 29}, {"cell": ["LPASed"], "n": 30}, {"cell": ["LPEx"], "n": 28}, {"cell": ["LPSed"], "n": 30}], "min_cell_size": 28, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 177, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 177, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 5, "status": "crossed", "crosstab": {"CONEx": {"Colon": 6, "Hippocampus": 6, "Liver": 6, "Prefrontal Cortex": 6, "Skeletal Muscle": 6}, "CONSed": {"Colon": 6, "Hippocampus": 6, "Liver": 6, "Prefrontal Cortex": 6, "Skeletal Muscle": 6}, "LPAEx": {"Colon": 6, "Hippocampus": 6, "Liver": 5, "Prefrontal Cortex": 6, "Skeletal Muscle": 6}, "LPASed": {" ... [4373 more characters]

reasoning: Each tissue is fitted separately with one sample per animal, so no repeated measures within a model. No batch/lane variable recorded; paper adjusts for none.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "DESeq2 ~group (R)", "status": "reproduced"}, "deviations": ["pydeseq2 rather than R DESeq2; pre-filtering not stated by paper, none applied"]}

reasoning: Raw counts support DESeq2 as the paper used.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "source_locator": "S2.4.3.2.p1"}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: S2.4.3.2.p1: FDR<0.10 (BH) and |LFC|>1.0.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2_PFC", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 36, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_PFC\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_PFC\\DEG_results_grp_LPAEx_vs_LPASed_tissue-PFC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_PFC\\DEG_results_grp_LPAEx_vs_LPSed_tissue-PFC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_PFC\\DEG_results_grp_LPAEx_vs_CONSed_tissue-PFC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_PFC\\DEG_results_grp_LPAEx_vs_CONEx_tissue-PFC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_PFC\\DEG_results_grp_LPAEx_vs_LPEx_tissue-PFC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_PFC\\DEG_results_grp_CONEx_vs_CONSed_tissue-PFC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_PFC\\DEG_results_grp_LPEx_vs_LPSed_tissue-PFC.csv"], "counts": {"deseq2_PFC/grp_LPAEx_vs_LPASed_tissue-PFC": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 1", "n ... [2069 more characters]

reasoning: S2.4.3.2.p1: DESeq2 ~group fitted per tissue, all groups vs LPAEx; PFC samples only. Exercise-only contrasts CONEx vs CONSed and LPEx vs LPSed come from the same fit as exploratory.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2_HIP", "role": "secondary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 36, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_HIP\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_HIP\\DEG_results_grp_LPAEx_vs_LPASed_tissue-HIP.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_HIP\\DEG_results_grp_LPAEx_vs_LPSed_tissue-HIP.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_HIP\\DEG_results_grp_LPAEx_vs_CONSed_tissue-HIP.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_HIP\\DEG_results_grp_LPAEx_vs_CONEx_tissue-HIP.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_HIP\\DEG_results_grp_LPAEx_vs_LPEx_tissue-HIP.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_HIP\\DEG_results_grp_CONEx_vs_CONSed_tissue-HIP.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_HIP\\DEG_results_grp_LPEx_vs_LPSed_tissue-HIP.csv"], "counts": {"deseq2_HIP/grp_LPAEx_vs_LPASed_tissue-HIP": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 1",  ... [2042 more characters]

reasoning: S2.4.3.2.p1: DESeq2 ~group fitted per tissue, all groups vs LPAEx; HIP samples only. Exercise-only contrasts CONEx vs CONSed and LPEx vs LPSed come from the same fit as exploratory.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2_LIV", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 33, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV\\DEG_results_grp_LPAEx_vs_LPASed_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV\\DEG_results_grp_LPAEx_vs_LPSed_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV\\DEG_results_grp_LPAEx_vs_CONSed_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV\\DEG_results_grp_LPAEx_vs_CONEx_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV\\DEG_results_grp_LPAEx_vs_LPEx_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV\\DEG_results_grp_CONEx_vs_CONSed_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV\\DEG_results_grp_LPEx_vs_LPSed_tissue-LIV.csv"], "counts": {"deseq2_LIV/grp_LPAEx_vs_LPASed_tissue-LIV": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 1", "n ... [2062 more characters]

reasoning: S2.4.3.2.p1: DESeq2 ~group fitted per tissue, all groups vs LPAEx; LIV samples only. Exercise-only contrasts CONEx vs CONSed and LPEx vs LPSed come from the same fit as exploratory.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2_COL", "role": "secondary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 36, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_COL\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_COL\\DEG_results_grp_LPAEx_vs_LPASed_tissue-COL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_COL\\DEG_results_grp_LPAEx_vs_LPSed_tissue-COL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_COL\\DEG_results_grp_LPAEx_vs_CONSed_tissue-COL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_COL\\DEG_results_grp_LPAEx_vs_CONEx_tissue-COL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_COL\\DEG_results_grp_LPAEx_vs_LPEx_tissue-COL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_COL\\DEG_results_grp_CONEx_vs_CONSed_tissue-COL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_COL\\DEG_results_grp_LPEx_vs_LPSed_tissue-COL.csv"], "counts": {"deseq2_COL/grp_LPAEx_vs_LPASed_tissue-COL": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 1",  ... [2042 more characters]

reasoning: S2.4.3.2.p1: DESeq2 ~group fitted per tissue, all groups vs LPAEx; COL samples only. Exercise-only contrasts CONEx vs CONSed and LPEx vs LPSed come from the same fit as exploratory.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2_MUS", "role": "secondary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 36, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_MUS\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_MUS\\DEG_results_grp_LPAEx_vs_LPASed_tissue-MUS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_MUS\\DEG_results_grp_LPAEx_vs_LPSed_tissue-MUS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_MUS\\DEG_results_grp_LPAEx_vs_CONSed_tissue-MUS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_MUS\\DEG_results_grp_LPAEx_vs_CONEx_tissue-MUS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_MUS\\DEG_results_grp_LPAEx_vs_LPEx_tissue-MUS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_MUS\\DEG_results_grp_CONEx_vs_CONSed_tissue-MUS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_MUS\\DEG_results_grp_LPEx_vs_LPSed_tissue-MUS.csv"], "counts": {"deseq2_MUS/grp_LPAEx_vs_LPASed_tissue-MUS": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 1",  ... [2046 more characters]

reasoning: S2.4.3.2.p1: DESeq2 ~group fitted per tissue, all groups vs LPAEx; MUS samples only. Exercise-only contrasts CONEx vs CONSed and LPEx vs LPSed come from the same fit as exploratory.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2_LIV_noAE11", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 32, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV_noAE11\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV_noAE11\\DEG_results_grp_LPAEx_vs_LPASed_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV_noAE11\\DEG_results_grp_LPAEx_vs_LPSed_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV_noAE11\\DEG_results_grp_LPAEx_vs_CONSed_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV_noAE11\\DEG_results_grp_LPAEx_vs_CONEx_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV_noAE11\\DEG_results_grp_LPAEx_vs_LPEx_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV_noAE11\\DEG_results_grp_CONEx_vs_CONSed_tissue-LIV.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\deseq2_LIV_noAE11\\DEG_results_grp_LPEx_vs_LPSed_tissue-LIV.csv"], "counts": {"deseq2_LIV_noAE11/grp_LPAEx_vs_LPASed_t ... [2156 more characters]

reasoning: Liver refit without the colon-contaminated L_AE11 (LPAEx n=4) to test whether the inflated LPAEx-up signal is contamination.

### enrichment (valid, failed)

final: {"organism": "Rat", "subset": "deseq2_PFC/grp_LPAEx_vs_LPASed_tissue-PFC", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "execution_error": "Enrichment analysis failed. Error: TypeError: 'float' object is not subscriptable"}

reasoning: paper reports pathways of upregulated DEGs for this exercise comparison (FIG5E); BioPlanet not available, GO/KEGG/Hallmark used

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "deseq2_PFC/grp_LPAEx_vs_LPASed_tissue-PFC", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\enrichment_deseq2_PFC_grp_LPAEx_vs_LPASed_tissue-PFC\\gsea\\DEG_results_grp_LPAEx_vs_LPASed_tissue-PFC_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17117 Rat genes ranked by 'stat'. 50 Hallmark sets tested, 26 significant at FDR q < 0.25. Rat genes matched to mouse Hallmark by symbol: 3874/4291 Hallmark genes present in the ranking. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_ANGIOGENESIS | NES=1.86 | NOM p=0.00e+00 | FDR q=2.74e-03 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.81 | NOM p=0.00e+00 | FDR q=2.28e-03 - HALLMARK_MITOTIC_SPINDLE | NES=1.79 | NOM p=0.00e+00 | FDR q=2.13e-03 - HALLMARK_UV_RESPONSE_DN | NES=1.72 | NOM p=0.00e+00 | FDR q=5.25e-03 - HALLMARK_G2M_CHECKPOINT | NES=1.67 | NOM p=0.00e+00 | FDR q=7.66e-03 - HALLMARK_PROTEIN_SECRETION | NES=1.64 | NOM p=1.71e-03 | FDR q=9.58e-03 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.56 | NOM p=1.91e-02 | FDR q=1.34e-02 - HALLMARK_E2F_TARGETS | NES=1.47 | NOM p=4.94e-03 | FDR q=3.46e-02 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.30 | NOM p=4.41e-02 | ... [596 more characters]

reasoning: paper reports pathways of upregulated DEGs for this exercise comparison (FIG5E); BioPlanet not available, GO/KEGG/Hallmark used

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "deseq2_LIV/grp_LPAEx_vs_LPASed_tissue-LIV", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\enrichment_deseq2_LIV_grp_LPAEx_vs_LPASed_tissue-LIV\\ora_up\\DEG_results_grp_LPAEx_vs_LPASed_tissue-LIV_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\enrichment_deseq2_LIV_grp_LPAEx_vs_LPASed_tissue-LIV\\ora_up\\DEG_results_grp_LPAEx_vs_LPASed_tissue-LIV_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\enrichment_deseq2_LIV_grp_LPAEx_vs_LPASed_tissue-LIV\\ora_up\\DEG_results_grp_LPAEx_vs_LPASed_tissue-LIV_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\enrichment_deseq2_LIV_grp_LPAEx_vs_LPASed_tissue-LIV\\ora_up\\DEG_results_grp_LPAEx_vs_LPASed_tissue-LIV_K ... [1536 more characters]

reasoning: paper reports pathways for this liver comparison (FIG6G)

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "deseq2_LIV/grp_LPAEx_vs_LPASed_tissue-LIV", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36892893\\GSE213649\\results\\enrichment_deseq2_LIV_grp_LPAEx_vs_LPASed_tissue-LIV\\gsea\\DEG_results_grp_LPAEx_vs_LPASed_tissue-LIV_GSEA_Hallmark.csv"], "summary": "GSEA complete on 16853 Rat genes ranked by 'stat'. 50 Hallmark sets tested, 37 significant at FDR q < 0.25. Rat genes matched to mouse Hallmark by symbol: 3893/4291 Hallmark genes present in the ranking. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.12 | NOM p=0.00e+00 | FDR q=9.35e-04 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.11 | NOM p=0.00e+00 | FDR q=4.67e-04 - HALLMARK_E2F_TARGETS | NES=2.11 | NOM p=0.00e+00 | FDR q=3.12e-04 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.05 | NOM p=0.00e+00 | FDR q=2.34e-04 - HALLMARK_G2M_CHECKPOINT | NES=2.04 | NOM p=0.00e+00 | FDR q=1.87e-04 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.03 | NOM p=0.00e+00 | FDR q=1.56e-04 - HALLMARK_COMPLEMENT | NES=1.86 | NOM p=0.00e+00 | FDR q=2.67e-04 - HALLMARK_ANGIOGENESIS | NES=1.76 | NOM p=0.00e+00 | FDR q=4.67e-04 - HALLMARK_HEME_METABOLISM | NES=1.76 | NOM p=0.00e+00 | FDR q=5. ... [596 more characters]

reasoning: paper reports pathways for this liver comparison (FIG6G)

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper reports n=4-6/group; deposited data have 6/group per tissue (liver LPEx 5).", "Only LPAEx vs LPASed isolates exercise among the paper's contrasts; LPAEx vs CONSed/LPSed mixes probiotic and exercise.", "Paper counts for most hippocampus/colon/muscle comparisons are only in supplementary tables (stated as 2-14).", "PFC_AE9, PFC_CS7 and HippoPS7 correlate slightly better with the other brain region; PFC and hippocampus are similar, so not treated as mislabelled.", "Deposited liver columns L_AE7/GSM6591471 (colon) and L_PE4/GSM6591458 (muscle) are mislabelled and excluded; with them excluded the liver counts match the paper (paper probably excluded them too: n=4-6).", "Liver LPAEx contrasts depend on L_AE11 (GSM6591473), which carries colon contamination: without it LPAEx vs LPASed drops from 97 to 6 DEGs and the other LPAEx contrasts to 2-13. The paper's liver 'inflammation' signature of LPAEx is therefore not robust to this sample.", "Gene-level checks by symbol are not possible: the matrix has Ensembl IDs only, and the paper's named genes are symbols."], "results": {"deseq2_PFC/grp_LPAEx_vs_LPASed_tissue-PFC": {"n_deg": 295, "up": 246, "down": 49, "rule": "padj < 0.1 and |log2FoldChange| > 1", "audit_n": 1061}, "deseq2_PFC/grp_LPAEx_vs_LPSed_tissue-PFC": {"n_deg": 169, "up": 138, "down": 31, "rule": "padj < 0.1 and |log2FoldChange| > 1", "audit_n": 642}, "deseq2_PFC/grp_LPAEx_vs_CONSed_tissue-PFC": {"n_deg": 59, "up": 50, "down": 9 ... [9140 more characters]

reasoning: Paper's contrasts reproduced with its method and threshold.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 177 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "liver LPAEx vs LPSed split",
    "paper": "text 137 up/10 down; TAB3 143 = 137/6",
    "data": "n/a",
    "disposition": "executable_without_change"
  },
  {
    "item": "liver LPAEx vs LPEx count",
    "paper": "TAB3 19 (11/8); text 22 (11/11)",
    "data": "n/a",
    "disposition": "executable_without_change"
  },
  {
    "item": "group sizes",
    "paper": "n=4-6 per group (S2.4.3.p1)",
    "data": "6/group per tissue, liver LPEx 5",
    "disposition": "executable_without_change"
  },
  {
    "item": "liver sample identity",
    "paper": "all liver samples treated as liver (TAB1 marks L for AE7 and PE4)",
    "data": "L_AE7 expression is colon, L_PE4 is muscle, L_AE11 partly colon",
    "disposition": "excluded_samples"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID36892893 / GSE213649

## What ran
- `case_runner inspect` then `case_runner execute case_spec.json` (final attempt; earlier attempts are in `_previous/`). Validator: 19 records, 0 errors. Status: completed, route `paper_aligned`.
- Data: `GSE213649_ang1_7_all_tissues_read_counts__1_.csv`: STAR raw integer counts, 32,545 Ensembl rat genes × 179 samples (5 tissues × 6 groups). Samples were aligned exactly on `title` (179/179).
- Design, following the paper (S2.4.3.2.p1): DESeq2 (pydeseq2 Wald) with `~ grp` (6 levels: CONSed, CONEx, LPSed, LPEx, LPASed, LPAEx), fitted separately for each tissue. The paper's planned contrasts are LPAEx vs each of the other 5 groups in each tissue (25 contrasts).
- LPAEx vs LPASed is the contrast that isolates exercise. Two exercise contrasts the paper does not report ran as exploratory analyses from the same fits: CONEx vs CONSed and LPEx vs LPSed.
- Sensitivity run `deseq2_LIV_noAE11`: liver refitted without L_AE11.
- Threshold (paper, S2.4.3.2.p1): BH FDR < 0.10 and |log2FC| > 1.0. The audit rule is padj < 0.05 with no fold-change cutoff.
- Enrichment: ORA on up-regulated genes (Enrichr GO and KEGG) and Hallmark GSEA, for PFC and liver LPAEx vs LPASed. The paper used Enrichr BioPlanet 2019, which is not available here.

## Sample QC decision (labelling fix before modelling)
A check of each sample against the per-tissue median profile (Spearman correlation) found that two columns labelled liver are other tissues:
- L_AE7 / GSM6591471 is colon (r = 0.94 to colon vs 0.72 to liver).
- L_PE4 / GSM6591458 is skeletal muscle (r = 0.96 to muscle vs 0.68 to liver).
- Neither is a byte-copy of another column.

Both are excluded. L_AE11 / GSM6591473 is liver with a colon component (r = 0.94 to liver vs about 0.98 for the other liver samples, and 0.75 to colon). It was kept in the primary run and dropped in the sensitivity run.

With all liver samples included, the liver LPAEx contrasts gave about 1,000–1,300 DEGs, nearly all higher in LPAEx. After the two exclusions the liver counts match the paper, so the authors probably dropped these samples too (they report n = 4–6 per group).

PFC_AE9, PFC_CS7 and HippoPS7 correlate slightly better with the other brain region. They were kept, because PFC and hippocampus have similar profiles.

## DEGs vs paper (FDR<0.10 & |LFC|>1; ours / paper)
| Tissue | vs LPASed (exercise) | vs LPSed | vs CONSed | vs CONEx | vs LPEx |
|---|---|---|---|---|---|
| PFC | 295 (246↑/49↓) / 317 (262/ ... [3138 more characters]
