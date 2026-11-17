# Review packet B (the analysis' decisions): GSE150620

## Mechanical flags

- **pairing_key_candidate**: {"key": "characteristics_ch1.4.replicate", "across": "characteristics_ch1.5.reagent", "pairs_or_sets": 6, "samples_linked": 22, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Samples per design level

### `act_raw`
- **sed** (11): GSM4553924 / Control_1; GSM4553925 / Control_2; GSM4553926 / Control_3; GSM4553927 / Control_4; GSM4553928 / Control_5; GSM4553929 / Control_6; GSM4553936 / Clodronate_13; GSM4553937 / Clodronate_14; GSM4553938 / Clodronate_15; GSM4553939 / Clodronate_16; GSM4553940 / Clodronate_18
- **wheel** (11): GSM4553930 / Wheel_7; GSM4553931 / Wheel_8; GSM4553932 / Wheel_9; GSM4553933 / Wheel_10; GSM4553934 / Wheel_11; GSM4553935 / Wheel_12; GSM4553941 / WheelClodronate_19; GSM4553942 / WheelClodronate_20; GSM4553943 / WheelClodronate_21; GSM4553944 / WheelClodronate_22; GSM4553945 / WheelClodronate_24

### `lip_raw`
- **clo** (10): GSM4553936 / Clodronate_13; GSM4553937 / Clodronate_14; GSM4553938 / Clodronate_15; GSM4553939 / Clodronate_16; GSM4553940 / Clodronate_18; GSM4553941 / WheelClodronate_19; GSM4553942 / WheelClodronate_20; GSM4553943 / WheelClodronate_21; GSM4553944 / WheelClodronate_22; GSM4553945 / WheelClodronate_24
- **pbs** (12): GSM4553924 / Control_1; GSM4553925 / Control_2; GSM4553926 / Control_3; GSM4553927 / Control_4; GSM4553928 / Control_5; GSM4553929 / Control_6; GSM4553930 / Wheel_7; GSM4553931 / Wheel_8; GSM4553932 / Wheel_9; GSM4553933 / Wheel_10; GSM4553934 / Wheel_11; GSM4553935 / Wheel_12

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE150620"], "other_accessions_not_analyzed": {"GSE129508": "human window-of-opportunity RCT (Ligibel et al.), analyzed in S3.p5 / Fig 1A-B; not the requested series"}, "assay": "Lexogen QuantSeq 3' FWD RNA-seq of mouse left 4th mammary tissue with engrafted EO771 tumor cells; GEO deposits per-sample CPM", "primary_estimand": "Effect of 2 weeks of voluntary wheel running (before EO771 engraftment) vs sedentary housing on mammary-tissue gene expression, read out in the paper as a hypoxia signature score (lower in wheel runners)", "factors": {"activity": ["Control (hub shelter, sedentary)", "Wheel (Fast-Trac wheel)"], "liposome (GEO only, not mentioned in paper)": ["PBS liposomes", "Clodronate liposomes"]}, "sample_inclusion": "Paper says 'mice randomized to exercise vs. control in GSE150620' (FIG1 C) and 'compared to sedentary control mice that also received mammary cancer' (S3.p6); it does not state n, nor whether the 10 clodronate-liposome (macrophage-depleted) mice were included", "planned_contrasts": ["Wheel vs Control (sedentary) mammary tissue (S3.p6, FIG1 C; paper reports a hypoxia-signature TRA P = 0.003, no DEG count)"], "repeated_measure_unit": "none; one mammary sample per mouse", "paper_method": "Transcriptome representation analysis (TRA) of a Buffa et al. hypoxia gene set (Supplementary Data File 1) on log2 expression; group difference in mean gene expression scores (FIG1 C). No gene-level DE model described.", "normalization": "GEO data_processi ... [420 more characters]

reasoning: Perspective article; the only GSE150620 analysis is S3.p6 + FIG1 C: hypoxia-signature TRA, exercise vs control, P = 0.003, lower hypoxia with wheel running. No DEG list, no threshold, no sample counts. The GEO series is a 2x2 (activity x liposome) design from the same lab (contact D. Lamkin = first author); the paper does not mention the clodronate arm.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\input\\GSE150620_cpm_dedup.csv", "owned": true, "checks": ["S3.p6, FIG1 C and S5.p1 name GSE150620", "GEO contact Donald M. Lamkin (UCLA) = author DL; ethics statement S6.p1 names UCLA IACUC", "GEO tissue 'Mammary tissue with engrafted EO771 cells', wheel vs hub-shelter for two weeks before engraftment, matches S3.p6", "22 per-sample CPM files in GSE150620_RAW.tar, one per GSM in the metadata"], "accession": "GSE150620", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE150620\\GSE150620_metadata.csv"}

reasoning: Paper, accession, lab and protocol agree.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 22, "n_metadata": 22, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\aligned\\aligned_metadata.csv", "columns": {"act_raw": {"alias_of": "characteristics_ch1.1.activity", "recode": {"Control": "sed", "Wheel": "wheel"}}, "lip_raw": {"alias_of": "characteristics_ch1.2.treatment", "recode": {"PBS liposomes": "pbs", "Clodronate liposomes": "clo"}}, "cell": {"combine": ["act_raw", "lip_raw"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\aligned\\design_metadata.csv", "sha256": "9f584567cead9540c7841490773648b7bb33b22a29396e074a4311a3917dac74", "levels": {"act_raw": {"sed": 11, "wheel": 11}, "lip_raw": {"pbs": 12, "clo": 10}, "cell": {"sed_pbs": 6, "wheel_pbs": 6, "sed_clo": 5, "wheel_clo": 5}}}}

reasoning: Prep script renamed matrix columns to GSM accessions, so exact match on the metadata index (inspect: 22/22 on index and geo_accession). act = activity (Control->sed, Wheel->wheel); lip = liposome (PBS->pbs, Clodronate->clo); cell = act_lip for the cell-means model. Titles agree with the characteristics (Control_1-6 = sed/pbs, Wheel_7-12 = wheel/pbs, Clodronate_13-18 = sed/clo, WheelClodronate_19-24 = wheel/clo).

### matrix (valid, not_started)

final: {"matrix_type": "linear normalized CPM (floored at 1)", "recommended_method": "limma on log2(x+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\aligned\\aligned_matrix.csv", "sha256": "27edef0ad0447b208c5bd4ddc6cd54bd34db53ebb2e571cec69f52fb4e5dc06a", "n_features": 52528, "n_samples": 22, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 1.0, "max": 199180.9739, "median": 1.0, "integer_fraction": 0.7453, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GEO data_processing: 'Tab-delimited text files include CPM values for each Sample'. Column sums ~1.037e6 (1e6 plus the floor), minimum exactly 1.0 in ~74% of entries, non-integer otherwise: linear CPM with values below 1 set to 1. No raw counts deposited, so count models (DESeq2/edgeR/voom) are not available. Paper analyzed log2 expression (FIG1 C 'on log2 scale').

### design (valid, not_started)

final: {"analysis_type": "factorial (2x2 activity x liposome) cell-means model, limma", "formula": "~ 0 + C(cell)", "contrasts": [{"name": "wheel_vs_sed_pbs", "role": "primary", "definition": "wheel_pbs - sed_pbs (exercise effect with intact macrophages, 6 vs 6)"}, {"name": "wheel_vs_sed_avg", "role": "secondary", "definition": "0.5*(wheel_pbs + wheel_clo) - 0.5*(sed_pbs + sed_clo) (exercise main effect averaged over liposome, all 22 mice)"}, {"name": "wheel_vs_sed_clo", "role": "exploratory", "definition": "wheel_clo - sed_clo (exercise effect after macrophage depletion, 5 vs 5)"}, {"name": "interaction_act_x_lip", "role": "exploratory", "definition": "(wheel_clo - sed_clo) - (wheel_pbs - sed_pbs)"}, {"name": "clo_vs_pbs_sed", "role": "exploratory", "definition": "sed_clo - sed_pbs (liposome effect, not exercise; listed by suitability)"}, {"name": "clo_vs_pbs_wheel", "role": "exploratory", "definition": "wheel_clo - wheel_pbs (liposome effect, not exercise; listed by suitability)"}, {"name": "pooled_wheel_vs_sed", "role": "sensitivity", "definition": "separate two-group limma ~ act_raw on all 22 mice, liposome ignored (one possible reading of the paper's 'exercise vs control')"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: Paper (S3.p6) asks wheel vs sedentary control; it does not mention clodronate, so which mice entered FIG1 C is unknown. Primary = wheel vs sed within PBS liposomes (the untouched-physiology exercise effect, the paper's stated question); secondary = activity main effect averaged over liposome (uses all randomized mice, closest to a pooled reading of the paper); clodronate-arm and interaction contrasts exploratory. One cell-means model on all 22 samples. Suitability names: primary = act_raw_wheel_vs_sed_lip_raw-pbs; clodronate arm = act_raw_wheel_vs_sed_lip_raw-clo; interaction = act_raw_lip_raw_wheel_clo_vs_sed_pbs; the two liposome-within-activity comparisons are also fitted as exploratory.

rejected alternatives: [{"value": "pool all 22 mice by activity, ignoring liposome (11 vs 11)", "reason_rejected": "clodronate is a randomized design factor with 10/22 mice; ignoring it would inflate residual variance and mix two conditions; the averaged-cell contrast keeps the all-mice estimand without that; run only as a labelled sensitivity fit (pooled_wheel_vs_sed) to test which reading matches the paper's hypoxia result"}, {"value": "PBS-only 6 vs 6 two-group fit", "reason_rejected": "same estimand as the primary ... [93 more characters]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "lip_raw", "disposition": "design factor, modeled in the cell-means formula (not a nuisance covariate)"}, {"name": "characteristics_ch1.4.replicate", "disposition": "excluded: within-group running index 1-6 (titles show distinct animals Control_1..WheelClodronate_24); not a pairing or batch key"}, {"name": "characteristics_ch1.3.experiment #", "disposition": "constant (1); no batch"}], "design_check": {"formula_equivalent": "~ C(act_raw) + C(lip_raw)", "n_samples": 22, "n_columns": 3, "columns": ["Intercept", "act_raw_wheel", "lip_raw_pbs"], "rank": 3, "full_rank": true, "residual_df": 19, "levels": {"act_raw": {"sed": 11, "wheel": 11}, "lip_raw": {"pbs": 12, "clo": 10}}, "cells": [{"cell": ["sed", "clo"], "n": 5}, {"cell": ["sed", "pbs"], "n": 6}, {"cell": ["wheel", "clo"], "n": 5}, {"cell": ["wheel", "pbs"], "n": 6}], "min_cell_size": 5, "missing_values": {}}, "confounding": [{"column": "characteristics_ch1.4.replicate", "n_levels": 6, "status": "crossed", "crosstab": {"sed": {"1": 2, "2": 2, "3": 2, "4": 2, "5": 2, "6": 1}, "wheel": {"1": 2, "2": 2, "3": 2, "4": 2, "5": 2, "6": 1}}}]}

reasoning: Independent mice, one sample each, one experiment; no subject or batch blocking.

### method (valid, not_started)

final: {"matrix_type": "linear normalized CPM (floored at 1)", "method": "limma (moderated t, empirical Bayes) on log2(CPM+1)", "formula": "~ 0 + C(cell)", "paper_route": {"method": "TRA of the Buffa hypoxia gene set (Supplementary Data File 1)", "status": "blocked", "reason": "gene set file (Table_1.XLS) not available locally and TRA is not an executor in this workflow; gene-level limma plus Hallmark-hypoxia GSEA used as the declared alternative"}, "deviations": ["gene-level limma DE instead of the paper's gene-set TRA", "hypoxia direction checked with MSigDB Hallmark HYPOXIA (GSEA) instead of the Buffa signature", "duplicated gene symbols collapsed by highest mean CPM; 4 duplicated Excel-date IDs dropped (prep_merge_cpm.py)"], "transform": "log2(x+1)"}

reasoning: Linear CPM -> log2(x+1) -> limma (matrix policy). A cell-means design keeps both randomized factors and gives all four contrasts from one fit.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "none", "cutoff": null, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Paper reports no gene-level DE rule; workflow default BH padj < 0.05, no fold-change cutoff. Raw p < 0.05 shown only as a labelled audit count."}

reasoning: S3.p6 / FIG1 C give only gene-set TRA P values.

### execution (valid, completed)

final: {"method": "run_multigroup_analysis", "subset": "analysis", "role": "primary", "tool": "tools.multigroup_tools:run_multigroup_analysis", "n_samples": 22, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\results\\analysis\\DEG_results_wheel_vs_sed_pbs.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\results\\analysis\\DEG_results_wheel_vs_sed_avg.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\results\\analysis\\DEG_results_wheel_vs_sed_clo.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\results\\analysis\\DEG_results_interaction_act_x_lip.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\results\\analysis\\DEG_results_clo_vs_pbs_sed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\results\\analysis\\DEG_results_clo_vs_pbs_wheel.csv"], "counts": {"analysis/wheel_vs_sed_pbs": {"applied": {"rule": "padj < 0.05", "n_tested": 19171, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 19171, "n_significant": 871, "n_up": 149, "n_down": 722, "deg_sanity": "ok"}}, "analysis/wheel_vs_sed_avg": {"applie ... [1350 more characters]

reasoning: One limma cell-means fit on all 22 mice; wheel_vs_sed_pbs is the primary contrast, wheel_vs_sed_avg secondary, the clodronate-arm and interaction contrasts exploratory.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "pooled_wheel_vs_sed", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 22, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ act_raw", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\results\\pooled_wheel_vs_sed\\DEG_results_wheel_vs_sed.csv"], "counts": {"pooled_wheel_vs_sed": {"applied": {"rule": "padj < 0.05", "n_tested": 19171, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 19171, "n_significant": 1018, "n_up": 371, "n_down": 647, "deg_sanity": "ok"}}}}

reasoning: Paper does not mention the liposome factor; this 11 vs 11 fit ignoring liposome tests the pooled reading of FIG1 C. Rejected as primary because it ignores a randomized design factor.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "analysis/wheel_vs_sed_pbs", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\results\\enrichment_analysis_wheel_vs_sed_pbs\\gsea\\DEG_results_wheel_vs_sed_pbs_GSEA_Hallmark.csv"], "summary": "GSEA complete on 19171 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 8 significant at FDR q < 0.25. ### Top 5 UP (NES > 0, enriched in treatment): - HALLMARK_BILE_ACID_METABOLISM | NES=1.08 | NOM p=2.72e-01 | FDR q=1.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=0.98 | NOM p=5.71e-01 | FDR q=1.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=0.87 | NOM p=8.54e-01 | FDR q=1.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=0.85 | NOM p=9.76e-01 | FDR q=1.00e+00 - HALLMARK_ADIPOGENESIS | NES=0.84 | NOM p=9.63e-01 | FDR q=8.49e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-2.41 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=-2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=-2.02 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=-1.87 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=-1.71 | NOM p=0.00e+00 | FDR q=3.30e-03 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=-1.60 | NOM p=2.16e-03 | FDR q=1.17e-02 - HALLMARK_MITOTIC_SPINDLE | NES=-1.51 | NOM p=3.12e-03 | FDR ... [420 more characters]

reasoning: Paper's readout is a hypoxia signature; Hallmark HYPOXIA NES sign is the comparable result

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "analysis/wheel_vs_sed_avg", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\results\\enrichment_analysis_wheel_vs_sed_avg\\gsea\\DEG_results_wheel_vs_sed_avg_GSEA_Hallmark.csv"], "summary": "GSEA complete on 19171 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 42 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=2.98 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.52 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.42 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.85 | NOM p=0.00e+00 | FDR q=1.24e-03 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.74 | NOM p=0.00e+00 | FDR q=3.47e-03 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.56 | NOM p=3.28e-03 | FDR q=1.15e-02 - HALLMARK_COMPLEMENT | NES=1.38 | NOM p=1.56e-02 | FDR q=4.97e-02 - HALLMARK_KRAS_SIGNALING_UP | NES=1.20 | NOM p=6.55e-02 | FDR q=1.76e-01 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.15 | NOM p=1.46e-01 | FDR q=2.20e-01 - HALLMARK_APOPTOSIS | NES=1.12 | NOM p=1.96e-01 | FDR q=2.36e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYOGENESIS | NES=-2.11 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=-2.09 | NOM p=0.00e+00 ... [411 more characters]

reasoning: same check on the all-mice reading

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "pooled_wheel_vs_sed", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33123481\\GSE150620\\results\\enrichment_pooled_wheel_vs_sed\\gsea\\DEG_results_wheel_vs_sed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 19171 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 38 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=2.92 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.45 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.77 | NOM p=0.00e+00 | FDR q=2.28e-03 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.74 | NOM p=0.00e+00 | FDR q=2.74e-03 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.65 | NOM p=0.00e+00 | FDR q=5.96e-03 - HALLMARK_COMPLEMENT | NES=1.28 | NOM p=5.13e-02 | FDR q=1.03e-01 - HALLMARK_KRAS_SIGNALING_UP | NES=1.19 | NOM p=7.82e-02 | FDR q=1.85e-01 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.06 | NOM p=2.86e-01 | FDR q=3.80e-01 - HALLMARK_APOPTOSIS | NES=1.01 | NOM p=4.16e-01 | FDR q=4.59e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYOGENESIS | NES=-2.15 | NOM p=0.00e+00 | FDR q=0.00e+0 ... [395 more characters]

reasoning: hypoxia direction under the pooled reading

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper reports no DEG counts; comparison with the paper is the direction of hypoxia gene expression (expected lower in wheel runners), checked by Hallmark HYPOXIA GSEA", "Paper does not say whether clodronate-liposome mice were in its exercise-vs-control comparison; both readings are run (PBS-only primary, liposome-averaged secondary)", "Hypoxia signature differs from the paper's (Hallmark vs Buffa et al.)", "Hallmark HYPOXIA GSEA: lower in wheel runners in all three readings, but significant only when all 22 mice are used (liposome-averaged NES -1.68, FDR 0.005; pooled 11 vs 11 NES -1.68, FDR 0.007); PBS-only primary NES -0.88, FDR 1.0. The paper's P = 0.003 most likely used all 22 mice; the hypoxia direction is not shown with intact macrophages alone at n = 6 vs 6.", "No gene passes BH padj < 0.05 in the primary contrast; the only gene in the averaged contrast is Gm7536 (predicted gene, up), which is driven by the clodronate arm (interaction padj < 0.05)."], "results": {"analysis/wheel_vs_sed_pbs": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 871}, "analysis/wheel_vs_sed_avg": {"n_deg": 1, "up": 1, "down": 0, "rule": "padj < 0.05", "audit_n": 1286}, "analysis/wheel_vs_sed_clo": {"n_deg": 3, "up": 3, "down": 0, "rule": "padj < 0.05", "audit_n": 1778}, "analysis/interaction_act_x_lip": {"n_deg": 1, "up": 1, "down": 0, "rule": "padj < 0.05", "audit_n": 1256}, "analysis/clo_vs_pbs_sed": {"n_deg": 0, "up": 0, "dow ... [2490 more characters]

reasoning: Paper genes listed are canonical hypoxia-signature genes (Buffa metagene members) used only to read direction; the paper itself names no genes for GSE150620.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 22 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "clodronate-liposome arm",
    "paper": "not mentioned; 'mice randomized to exercise vs. control'",
    "data": "2x2 design, 10/22 mice received clodronate liposomes",
    "disposition": "executable_with_declared_choice: PBS-only primary + liposome-averaged secondary from one model"
  },
  {
    "item": "analysis method",
    "paper": "TRA of a Buffa hypoxia gene set",
    "data": "CPM matrix; gene set file not available locally",
    "disposition": "declared deviation: limma DE + Hallmark hypoxia GSEA"
  },
  {
    "item": "duplicated gene symbols",
    "paper": "n/a",
    "data": "106 duplicated symbols in deposited files (incl. Excel-date IDs)",
    "disposition": "prep script: highest-mean row kept, duplicated date IDs dropped"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 33123481 / GSE150620

Status: **finished** (decision `valid`, execution `completed`, route `declared_deviation`; contract validator: 14 records, 0 errors).

## What the paper does with GSE150620
A perspective article. Its only analysis of GSE150620 is S3.p6 and FIG1 C. Mice ran on wheels for 2 weeks before EO771 engraftment, and their mammary tissue showed less expression of a Buffa et al. hypoxia gene set than sedentary controls (transcriptome representation analysis, P = 0.003). The paper reports **no gene-level DEG count, no DE threshold and no n**. It also never mentions that GEO holds a 2x2 design: activity (Control/Wheel) x liposome (PBS/Clodronate), with 6/6/5/5 mice.

## What ran
- Inspect, then `prep_merge_cpm.py`, which rebuilds the matrix from the 22 per-sample CPM files. Columns become GSM IDs. For duplicated symbols the row with the highest mean is kept, and 4 duplicated Excel-date IDs are dropped. Output: 52,528 genes x 22 samples.
- Matrix: linear CPM floored at 1. GEO data_processing says CPM; column sums are about 1.037e6. Transformed with log2(x+1). No raw counts were deposited, so count models do not apply.
- One limma cell-means model, `~ 0 + C(cell)`, fitted on all 22 mice. Contrasts:
  - primary: `wheel_vs_sed_pbs`
  - secondary: `wheel_vs_sed_avg` (activity effect averaged over liposome)
  - exploratory: `wheel_vs_sed_clo`, `interaction_act_x_lip`, `clo_vs_pbs_sed`, `clo_vs_pbs_wheel`
- Sensitivity: a separate two-group limma (`~ act_raw`, 11 vs 11) that ignores liposome. This is the pooled reading of the paper.
- No blocking. `replicate` is a within-group index, not a pairing key, and there is one experiment.
- Hallmark GSEA (prerank on the moderated t) for the primary, secondary and pooled tables.

## DEG counts vs paper (threshold: workflow_default, BH padj < 0.05, no FC cutoff; the paper has none)
| Table | n (up/down) | raw p < 0.05 audit | Paper |
|---|---|---|---|
| wheel_vs_sed_pbs (primary) | 0 | 871 | no DEG count reported |
| wheel_vs_sed_avg (secondary) | 1 (1/0), Gm7536 | 1286 | — |
| pooled_wheel_vs_sed (sensitivity) | 0 | 1018 | — |
| wheel_vs_sed_clo (exploratory) | 3 (3/0) | 1778 | — |
| interaction (exploratory) | 1 (1/0) | 1256 | — |
| clo_vs_pbs_sed / clo_vs_pbs_wheel (exploratory, not exercise) | 0 / 5 | 1216 / 1914 | — |

The comparable result is the paper's claim that hypoxia is lower in wheel runners:
- Hallmark HYPOXIA NES −1.68, FDR 0.005 (liposome-averaged)
- NES −1.68, FDR 0.007 (pooled 11 ... [1654 more characters]
