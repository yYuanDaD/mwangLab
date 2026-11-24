# Review packet B (the analysis' decisions): GSE137631

## Mechanical flags

- none

## Samples per design level

### `grp`
- **ETpost** (6): GSM4083523 / RYGB + exercise training_1 POST9; GSM4083525 / RYGB + exercise training_2 POST9; GSM4083527 / RYGB + exercise training_3 POST9; GSM4083529 / RYGB + exercise training_4 POST9; GSM4083531 / RYGB + exercise training_5 POST9; GSM4083533 / RYGB + exercise training_6 POST9
- **ETpre** (6): GSM4083522 / RYGB + exercise training_1 PRE; GSM4083524 / RYGB + exercise training_2 PRE; GSM4083526 / RYGB + exercise training_3 PRE; GSM4083528 / RYGB + exercise training_4 PRE; GSM4083530 / RYGB + exercise training_5 PRE; GSM4083532 / RYGB + exercise training_6 PRE
- **LEAN** (6): GSM4083516 / lean control_1; GSM4083517 / lean control_2; GSM4083518 / lean control_3; GSM4083519 / lean control_4; GSM4083520 / lean control_5; GSM4083521 / lean control_6
- **RYpost** (6): GSM4083535 / RYGB_1 POST9; GSM4083537 / RYGB_2 POST9; GSM4083539 / RYGB_3 POST9; GSM4083541 / RYGB_4 POST9; GSM4083543 / RYGB_5 POST9; GSM4083545 / RYGB_6 POST9
- **RYpre** (6): GSM4083534 / RYGB_1 PRE; GSM4083536 / RYGB_2 PRE; GSM4083538 / RYGB_3 PRE; GSM4083540 / RYGB_4 PRE; GSM4083542 / RYGB_5 PRE; GSM4083544 / RYGB_6 PRE

### `subject`
- **LEAN_1** (1): GSM4083516 / lean control_1
- **LEAN_2** (1): GSM4083517 / lean control_2
- **LEAN_3** (1): GSM4083518 / lean control_3
- **LEAN_4** (1): GSM4083519 / lean control_4
- **LEAN_5** (1): GSM4083520 / lean control_5
- **LEAN_6** (1): GSM4083521 / lean control_6
- **RYGBET_1** (2): GSM4083522 / RYGB + exercise training_1 PRE; GSM4083523 / RYGB + exercise training_1 POST9
- **RYGBET_2** (2): GSM4083524 / RYGB + exercise training_2 PRE; GSM4083525 / RYGB + exercise training_2 POST9
- **RYGBET_3** (2): GSM4083526 / RYGB + exercise training_3 PRE; GSM4083527 / RYGB + exercise training_3 POST9
- **RYGBET_4** (2): GSM4083528 / RYGB + exercise training_4 PRE; GSM4083529 / RYGB + exercise training_4 POST9
- **RYGBET_5** (2): GSM4083530 / RYGB + exercise training_5 PRE; GSM4083531 / RYGB + exercise training_5 POST9
- **RYGBET_6** (2): GSM4083532 / RYGB + exercise training_6 PRE; GSM4083533 / RYGB + exercise training_6 POST9
- **RYGB_1** (2): GSM4083534 / RYGB_1 PRE; GSM4083535 / RYGB_1 POST9
- **RYGB_2** (2): GSM4083536 / RYGB_2 PRE; GSM4083537 / RYGB_2 POST9
- **RYGB_3** (2): GSM4083538 / RYGB_3 PRE; GSM4083539 / RYGB_3 POST9
- **RYGB_4** (2): GSM4083540 / RYGB_4 PRE; GSM4083541 / RYGB_4 POST9
- **RYGB_5** (2): GSM4083542 / RYGB_5 PRE; GSM4083543 / RYGB_5 POST9
- **RYGB_6** (2): GSM4083544 / RYGB_6 PRE; GSM4083545 / RYGB_6 POST9

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE137631"], "assay": "Lexogen QuantSeq 3' mRNA-seq, vastus lateralis, women", "primary_estimand": "Change in skeletal-muscle gene expression from pre-surgery to 9 months after RYGB in women randomized to RYGB + combined aerobic/resistance exercise training (RYGB+ET), compared with RYGB alone (standard of care); lean women as a baseline reference", "factors": {"arm": ["RYGB", "RYGB+ET", "lean"], "time": ["PRE", "POST9 (9 months)"]}, "sample_inclusion": "GEO: 6 RYGB (pre/post9), 6 RYGB+ET (pre/post9), 6 lean controls (baseline only); 3-month biopsies mentioned in abstract are not in GEO", "repeated_measure_unit": "patient (pre and post9 biopsies from the same woman)", "planned_contrasts": ["RYGB+ET POST9 vs PRE, paired (abstract: 'candidates modulated by exercise training'; GEO summary: transcriptome changes explaining RYGB+ET improvement; DEG count not in abstract)", "RYGB POST9 vs PRE, paired (surgery alone)", "exercise-specific: change in RYGB+ET minus change in RYGB (randomized comparison; not stated as a DE contrast in the abstract)", "POST9 groups vs lean controls (GEO summary: 'restored to a lean phenotype')"], "paper_threshold": {"metric": "not_stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "abstract does not give a DEG threshold; full text unavailable"}, "paper_method": "DESeq2 V1.18.1 (GEO data_processing); JMP Genomics ANOVA also listed", "paper_results": "Abstract names TGF-beta1/SMAD2/3 pathway and follist ... [128 more characters]

reasoning: Full text unavailable; reconstruction rests on the PubMed abstract (PMID 32409493) and GEO GSE137631 summary/overall design/data_processing. DESeq2 is named in data_processing.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631_raw_counts_gsm.csv", "owned": true, "checks": ["GEO series contact (Dantas WS, Pennington) = first author", "GEO overall design matches abstract (RYGB vs RYGB+ET randomized, women, pre and 9-month muscle biopsies)", "30 matrix columns map one-to-one by name to the 30 GSM titles"], "accession": "GSE137631", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE137631\\GSE137631_metadata.csv"}

reasoning: GSE137631 is the paper's RNA-seq deposit; raw_counts file used (DESeq2_normalized_counts rejected as normalized input).

rejected alternatives: [{"value": "GSE137631_DESeq2_normalized_counts.txt.gz", "reason_rejected": "DESeq2 size-factor-normalized, non-integer; has 33 columns incl. extra annotation; raw counts available"}]

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 30, "n_metadata": 30, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "characteristics_ch1.0.group", "regex": "^(.*)$", "recode": {"lean control": "LEAN", "RYGB + exercise training PRE SURGERY": "ETpre", "RYGB + exercise training POST SURGERY": "ETpost", "RYGB PRE SURGERY": "RYpre", "RYGB POST SURGERY": "RYpost"}}, "arm": {"source": "characteristics_ch1.0.group", "regex": "^(lean control|RYGB \\+ exercise training|RYGB)", "recode": {"lean control": "LEAN", "RYGB + exercise training": "RYGBET", "RYGB": "RYGB"}}, "tm": {"source": "characteristics_ch1.0.group", "regex": "(PRE|POST|control)", "recode": {"PRE": "pre", "POST": "post", "control": "none"}}, "num": {"source": "title", "regex": "_(\\d+)"}, "subject": {"combine": ["arm", "num"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\aligned\\design_metadata.csv", "sha256": "b5ec61e7ff32d6fe767291957b85bb148c855f4e0f1d3addc1007e774599de7b", "levels": {"grp": {"LEAN": 6, "ETpre": 6, "ETpost": 6, "RYpre": 6, "RYpost": 6}, "arm": {"RYGBET": 12, "RYGB": 12, "LEAN": 6}, "tm": {"pre": 12, "post": 12, "none": 6}, "num": {"1": 5, "2": 5, "3": 5, "4": 5, "5": 5, "6": 5}, ... [261 more characters]

reasoning: Matrix columns were renamed to GSM ids by prep_rename_columns.py using an explicit name rule (RYGB.k.PRE -> 'RYGB_k PRE', WD.RYGB.ET.k.T -> 'RYGB + exercise training_k T', WD.lean.control.k -> 'lean control_k'); exact index match. Subject = arm + patient number; ages agree within each PRE/POST9 pair, supporting the pairing.

### matrix (valid, not_started)

final: {"source": "GSE137631_raw_counts.txt.gz (Lexogen QuantSeq pipeline read count tables)", "paper_input": "DESeq2 on read counts (data_processing)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\aligned\\aligned_matrix.csv", "sha256": "8983ea1a739a521d0287586997aaf48273989c1f84f22f6c9052ba3601d53c70", "n_features": 15974, "n_samples": 30, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 690916.0, "median": 68.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 690916, file named raw_counts, data_processing: Lexogen QuantSeq pipeline read count tables then DESeq2.

### design (valid, not_started)

final: {"analysis_type": "paired within-arm pre/post plus between-arm change comparison", "design_column": "grp", "contrasts": [{"name": "ET_post9_vs_pre", "control": "ETpre", "treatment": "ETpost", "role": "primary"}, {"name": "RYGB_post9_vs_pre", "control": "RYpre", "treatment": "RYpost", "role": "secondary"}, {"name": "exercise_x_time_change", "control": "RYGB change", "treatment": "RYGBET change", "role": "secondary"}, {"name": "ETpost_vs_LEAN", "control": "LEAN", "treatment": "ETpost", "role": "exploratory"}, {"name": "RYpost_vs_LEAN", "control": "LEAN", "treatment": "RYpost", "role": "exploratory"}], "estimand_note": "Within-arm pre/post is a surgery(+training) effect over 9 months, not an exercise effect alone; the randomized exercise effect is the difference in change between arms. Lean comparisons are associational.", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\suitability\\suitability.md", "n_comparisons": 11, "n_analyzable": 11}}

reasoning: GEO overall design: randomized RYGB vs RYGB+ET, biopsies PRE and 9 months; lean controls baseline only. Paper used DESeq2 (within-group comparisons implied by abstract 'candidates modulated by exercise training'). The interaction (difference in change) is the only contrast isolating exercise; included as secondary. 3-month timepoint absent from GEO.

rejected alternatives: [{"value": "pooling RYGB and RYGB+ET post vs pre", "reason_rejected": "would mix the arms and lose the exercise contrast"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "age", "disposition": "not added: constant within subject, absorbed by subject blocking in paired contrasts"}, {"name": "bmi", "disposition": "not added: outcome of surgery, post-treatment variable"}], "design_check": {"formula_equivalent": "~ C(grp) + C(subject)", "n_samples": 30, "n_columns": 22, "columns": ["Intercept", "grp_ETpre", "grp_LEAN", "grp_RYpost", "grp_RYpre", "subject_LEAN_2", "subject_LEAN_3", "subject_LEAN_4", "subject_LEAN_5", "subject_LEAN_6", "subject_RYGBET_1", "subject_RYGBET_2", "subject_RYGBET_3", "subject_RYGBET_4", "subject_RYGBET_5", "subject_RYGBET_6", "subject_RYGB_1", "subject_RYGB_2", "subject_RYGB_3", "subject_RYGB_4", "subject_RYGB_5", "subject_RYGB_6"], "rank": 20, "full_rank": false, "residual_df": 10, "levels": {"grp": {"LEAN": 6, "ETpre": 6, "ETpost": 6, "RYpre": 6, "RYpost": 6}, "subject": {"RYGBET_1": 2, "RYGBET_2": 2, "RYGBET_3": 2, "RYGBET_4": 2, "RYGBET_5": 2, "RYGBET_6": 2, "RYGB_1": 2, "RYGB_2": 2, "RYGB_3": 2, "RYGB_4": 2, "RYGB_5": 2, "RYGB_6": 2, "LEAN_1": 1, "LEAN_2": 1, "LEAN_3": 1, "LEAN_4": 1, "LEAN_5": 1, "LEAN_6": 1}}, "cells": [{"cell": ["ETpost", "RYGBET_1"], "n": 1}, {"cell": ["ETpost", "RYGBET_2"], "n": 1}, {"cell": ["ETpost", "RYGBET_3"], "n": 1}, {"cell": ["ETpost", "RYGBET_4"], "n": 1}, {"cell": ["ETpost", "RYGBET_5"], "n": 1}, {"cell": ["ETpost", "RYGBET_6"], "n": 1}, {"cell": ["ETpre", "RYGBET_1"], "n": 1}, {"cell": ["ETpre", "RYGBET_2"], ... [1398 more characters]

reasoning: Same patient biopsied PRE and POST9 -> subject blocking. Matrix column prefix 'WD.' appears on lean and RYGB+ET columns but not on RYGB columns, which may indicate a separate processing batch per arm; any such batch is constant within subject, so within-arm paired contrasts and the difference-in-change are protected from additive batch, but lean-vs-POST comparisons crossing arms are not.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald) paired ~ subject + grp for within-arm contrasts; limma paired_change on log2(CPM+1) for difference-in-change", "formula": "~ subject + grp", "paper_route": {"method": "DESeq2", "status": "reproduced", "reason": "raw counts deposited; paper's exact DESeq2 design not stated in abstract (pairing assumed)"}, "deviations": ["difference-in-change uses limma paired_change on log2(CPM+1) (no DESeq2 interaction executor with nested subject); declared deviation", "lean comparisons use unpaired DESeq2 ~ grp"]}

reasoning: Raw counts support DESeq2 as named in GEO data_processing.

### threshold (valid, not_started)

final: {"paper_threshold": null, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Abstract states no DEG threshold and the full text is unavailable; workflow default BH padj < 0.05, no fold-change cutoff."}

reasoning: No threshold in abstract or GEO.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "ET_post9_vs_pre", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\ET_post9_vs_pre\\input\\matrix.csv", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\ET_post9_vs_pre\\DEG_results_ETpost_vs_ETpre.csv"], "counts": {"ET_post9_vs_pre": {"applied": {"rule": "padj < 0.05", "n_tested": 12877, "n_significant": 148, "n_up": 41, "n_down": 107, "deg_sanity": "ok"}}}}

reasoning: paired DESeq2 in RYGB+ET arm, 6 complete pairs

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "RYGB_post9_vs_pre", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\RYGB_post9_vs_pre\\input\\matrix.csv", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\RYGB_post9_vs_pre\\DEG_results_RYpost_vs_RYpre.csv"], "counts": {"RYGB_post9_vs_pre": {"applied": {"rule": "padj < 0.05", "n_tested": 12567, "n_significant": 160, "n_up": 68, "n_down": 92, "deg_sanity": "ok"}}}}

reasoning: paired DESeq2 in RYGB-alone arm

### execution (valid, completed)

final: {"method": "run_multigroup_analysis", "subset": "exercise_x_time", "role": "secondary", "tool": "tools.multigroup_tools:run_multigroup_analysis", "n_samples": 24, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\exercise_x_time\\input\\matrix_filtered_normalized.csv", "transform": "log2(CPM+1)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\exercise_x_time\\followup_post\\DEG_results_RYGBET_vs_RYGB.csv"], "counts": {"exercise_x_time/RYGBET_vs_RYGB": {"applied": {"rule": "padj < 0.05", "n_tested": 13384, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: randomized exercise effect: (POST9-PRE in RYGB+ET) minus (POST9-PRE in RYGB)

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "ETpost_vs_LEAN", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\ETpost_vs_LEAN\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\ETpost_vs_LEAN\\DEG_results_ETpost_vs_LEAN.csv"], "counts": {"ETpost_vs_LEAN": {"applied": {"rule": "padj < 0.05", "n_tested": 12854, "n_significant": 426, "n_up": 244, "n_down": 182, "deg_sanity": "ok"}}}}

reasoning: GEO summary: restoration toward lean phenotype; associational

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "RYpost_vs_LEAN", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\RYpost_vs_LEAN\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\RYpost_vs_LEAN\\DEG_results_RYpost_vs_LEAN.csv"], "counts": {"RYpost_vs_LEAN": {"applied": {"rule": "padj < 0.05", "n_tested": 13779, "n_significant": 1035, "n_up": 456, "n_down": 579, "deg_sanity": "ok"}}}}

reasoning: surgery-alone vs lean; associational

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "ET_post9_vs_pre", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\enrichment_ET_post9_vs_pre\\gsea\\DEG_results_ETpost_vs_ETpre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 14756 Human genes ranked by 'stat'. 50 Hallmark sets tested, 29 significant at FDR q < 0.25. ### Top 9 UP (NES > 0, enriched in treatment): - HALLMARK_MYC_TARGETS_V2 | NES=1.33 | NOM p=6.80e-02 | FDR q=4.06e-01 - HALLMARK_P53_PATHWAY | NES=1.31 | NOM p=2.78e-02 | FDR q=2.30e-01 - HALLMARK_PANCREAS_BETA_CELLS | NES=1.14 | NOM p=2.67e-01 | FDR q=5.76e-01 - HALLMARK_MYC_TARGETS_V1 | NES=1.10 | NOM p=2.06e-01 | FDR q=5.64e-01 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.03 | NOM p=3.75e-01 | FDR q=6.97e-01 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=0.99 | NOM p=5.07e-01 | FDR q=7.27e-01 - HALLMARK_E2F_TARGETS | NES=0.97 | NOM p=5.23e-01 | FDR q=6.62e-01 - HALLMARK_DNA_REPAIR | NES=0.95 | NOM p=6.11e-01 | FDR q=6.60e-01 - HALLMARK_G2M_CHECKPOINT | NES=0.78 | NOM p=9.71e-01 | FDR q=9.29e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.68 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-2.57 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=-2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK ... [391 more characters]

reasoning: paper reports pathway identification (TGF-beta/SMAD, ECM)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "exercise_x_time/RYGBET_vs_RYGB", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32409493\\GSE137631\\results\\enrichment_exercise_x_time_RYGBET_vs_RYGB\\gsea\\DEG_results_RYGBET_vs_RYGB_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12749 Human genes ranked by 'stat'. 50 Hallmark sets tested, 28 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.04 | NOM p=0.00e+00 | FDR q=2.25e-03 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.67 | NOM p=6.37e-03 | FDR q=1.61e-02 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.60 | NOM p=0.00e+00 | FDR q=2.35e-02 - HALLMARK_MYC_TARGETS_V2 | NES=1.54 | NOM p=1.68e-02 | FDR q=3.19e-02 - HALLMARK_MYC_TARGETS_V1 | NES=1.52 | NOM p=0.00e+00 | FDR q=3.21e-02 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.31 | NOM p=4.65e-02 | FDR q=1.57e-01 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.24 | NOM p=1.01e-01 | FDR q=2.42e-01 - HALLMARK_MTORC1_SIGNALING | NES=1.17 | NOM p=1.16e-01 | FDR q=3.54e-01 - HALLMARK_ADIPOGENESIS | NES=1.16 | NOM p=1.64e-01 | FDR q=3.39e-01 - HALLMARK_DNA_REPAIR | NES=1.14 | NOM p=1.74e-01 | FDR q=3.47e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_KRAS_SIGNALING_UP | NES=-1.85 | NOM p=0.00e+00 | FDR q=9.72e-03 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSI ... [420 more characters]

reasoning: exercise-specific pathway changes

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Comparison with the paper rests on the abstract only (no full text); abstract gives no DEG counts.", "Within-arm POST9 vs PRE confounds exercise with surgery and weight loss; exercise-specific effect = difference in change (limma, declared deviation).", "3-month biopsies are not in GEO.", "Possible per-arm processing batch ('WD.' column prefix) affects lean comparisons."], "results": {"ET_post9_vs_pre": {"n_deg": 148, "up": 41, "down": 107, "rule": "padj < 0.05"}, "RYGB_post9_vs_pre": {"n_deg": 160, "up": 68, "down": 92, "rule": "padj < 0.05"}, "exercise_x_time/RYGBET_vs_RYGB": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "ETpost_vs_LEAN": {"n_deg": 426, "up": 244, "down": 182, "rule": "padj < 0.05"}, "RYpost_vs_LEAN": {"n_deg": 1035, "up": 456, "down": 579, "rule": "padj < 0.05"}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"ET_post9_vs_pre": {"FST": {"baseMean": 42.6255, "log2FoldChange": 0.3468, "padj": 0.838, "pvalue": 0.322}, "TGFB1": {"baseMean": 7.7887, "log2FoldChange": -0.0381, "padj": null, "pvalue": 0.953}, "SMAD2": {"baseMean": 264.5908, "log2FoldChange": -0.1017, "padj": 0.9, "pvalue": 0.501}, "SMAD3": {"baseMean": 776.3287, "log2FoldChange": 0.0784, "padj": 0.938, "pvalue": 0.62}, "COL1A1": {"baseMean": 287.9596, "log2FoldChange": -0.619, "padj": 0.682, "pvalue": 0.126}, "COL1A2": {"baseMean": 599.5777, "log2FoldChange": -0.6598, "padj": 0.0879, "pvalue": 0.00131}}, "exercise_x_time/RYGBET_vs_RY ... [465 more characters]

reasoning: Abstract names FST and the TGF-beta1/SMAD2/3 pathway as exercise-modulated, and collagen I as reduced more with RYGB+ET.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "timepoints",
    "paper": "biopsies at baseline, 3 and 9 months",
    "data": "GEO has PRE and POST9 only",
    "disposition": "executable_without_change"
  },
  {
    "item": "DEG threshold",
    "paper": "not stated in abstract",
    "data": "n/a",
    "disposition": "workflow_default"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 32409493 / GSE137631

**The comparison with the paper rests on the abstract only.** No full text was available. The paper sources were the PubMed abstract (E-utilities efetch) and the GEO series title, summary, overall design and data_processing. Both are saved in `paper_abstract_and_geo.md`.

## What ran
- Design: women randomized to RYGB alone or RYGB plus combined aerobic and resistance exercise training (RYGB+ET). Vastus lateralis biopsies were taken before surgery (PRE) and 9 months after (POST9), from 6 patients per arm. 6 lean controls were sampled at baseline only. The 3-month biopsies mentioned in the abstract are not in GEO.
- Matrix: `GSE137631_raw_counts.txt.gz` (integer QuantSeq read counts). `prep_rename_columns.py` renamed its columns to GSM ids using an explicit name rule, never position; the map is in `GSE137631_raw_counts_gsm_column_map.csv`. All 30 samples aligned exactly. The DESeq2-normalized file was not used.
- Spec `case_spec.json` → `python -m tools.case_runner execute`. The run completed, suitability was analyzable (11/11 comparisons), and the validator reported 0 errors.
- Threshold: `workflow_default`, BH padj < 0.05 with no fold-change cutoff. The abstract states no DEG threshold.

| Table | Role | Method | DEGs (up/down) | Paper |
|---|---|---|---|---|
| ET_post9_vs_pre | primary (paper_aligned) | DESeq2 paired `~ subject + grp` | 148 (41/107) | count not in abstract |
| RYGB_post9_vs_pre | secondary | DESeq2 paired | 160 (68/92) | count not in abstract |
| exercise_x_time/RYGBET_vs_RYGB (difference in change) | secondary, declared deviation | limma paired_change, log2(CPM+1), CPM≥1 in ≥6 samples | 0 | — |
| ETpost_vs_LEAN | exploratory, associational | DESeq2 unpaired | 426 (244/182) | — |
| RYpost_vs_LEAN | exploratory, associational | DESeq2 unpaired | 1035 (456/579) | — |

The ordering of the lean comparisons (RYGB alone is further from lean than RYGB+ET) agrees with the GEO summary's claim that training restores a lean phenotype. Treat this as associational only; see the batch caveat below.

**Genes named in the abstract.** In the RYGB+ET arm, no named gene reached padj < 0.05:
- COL1A2: log2FC −0.66, padj 0.088
- COL1A1: −0.62, padj 0.68
- FST: +0.35, padj 0.84
- TGFB1: low expression, padj NA
- SMAD2 and SMAD3: unchanged

The directions for collagen I (down) and FST (up) match the abstract. None of these genes differ in the between-arm interaction (all padj > 0.9).

**Enrichment (GSEA, Hallmark, ranked ... [2432 more characters]
