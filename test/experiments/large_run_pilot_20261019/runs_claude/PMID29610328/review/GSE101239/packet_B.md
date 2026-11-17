# Review packet B (the analysis' decisions): GSE101239

## Mechanical flags

- none

## Samples per design level

### `grp`
- **Ctrl** (3): GSM2700541 / Control 12w rep1; GSM2700542 / Control 12w rep2; GSM2700543 / Control 12w rep3
- **VPA** (3): GSM2700544 / VPA 12w rep1; GSM2700545 / VPA 12w rep2; GSM2700546 / VPA 12w rep3
- **VPARun** (3): GSM2700547 / VPA+Run 12w rep1; GSM2700548 / VPA+Run 12w rep2; GSM2700549 / VPA+Run 12w rep3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE101239"], "assay": "bulk RNA-seq (50-bp SE, HiSeq 2500) of FACS-sorted Nestin-EGFP+ NS/PCs; forebrain at E15, dentate gyrus at P5 and 12w", "primary_estimand": "Effect of 8 wk voluntary wheel running on the adult (12w) dentate-gyrus NS/PC transcriptome of prenatally VPA-exposed mice: VPA+RW vs VPA (S1.4.p2, Fig. 5). Exercise was only given to VPA mice; there is no Ctrl+RW arm, so the exercise effect is identifiable only within VPA-exposed animals.", "planned_contrasts": ["VPA+RW vs VPA at 12w (S1.4.p2, Fig. 5B-E; exercise estimand; paper reports no DEG count, only that running mostly amended VPA-distorted genes incl. Cxcr4)", "VPA vs Ctrl at 12w (S1.2.p1, Fig. 2B/3; defines the VPA-DEG set that running normalizes; 12w count not stated in text, hundreds per S2.p2)", "VPA+RW vs Ctrl at 12w (implicit normalization check in Fig. 5B box plots)"], "factors": {"treatment": ["Ctrl (methylcellulose)", "VPA (300 mg/kg/day E12-14)", "VPA+RW (8 wk wheel)"], "stage": ["E15", "P5", "12w"]}, "inclusion": "Exercise estimand uses the 9 12w DG samples (3 Ctrl, 3 VPA, 3 VPA+Run); E15 and P5 samples are VPA-only developmental comparisons without exercise and were analysed per stage in the paper (S1.2.p1).", "repeated_measure_unit": "none; independent animals", "normalization": "Cufflinks FPKM", "paper_method": "Cuffdiff (Cufflinks) per developmental stage (GEO data_processing)", "paper_threshold": {"metric": "q-value", "cutoff": 0.05, "effect_metric": "fold change", "effect_c ... [225 more characters]

reasoning: Paper S1.4.p1-p2 and Fig. 5 define the exercise question: VPA mice with vs without 8 wk running at 12w. Threshold q<0.05 and FC>=1.5 at S1.2.p1; Cuffdiff in GEO data_processing. GSE101239 cited in the JATS data-availability statement.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["paper JATS names GSE101239", "21 samples: Ctrl/VPA at E15, P5, 12w plus VPA+Run 12w match Fig. 2A and Fig. 5A", "treatment_protocol matches VPA 300 mg/kg E12-14; Nestin-EGFP genotype matches S1.2.p1"], "accession": "GSE101239", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE101239\\GSE101239_metadata.csv"}

reasoning: Accession cited by the paper; sample structure and protocol match the paper.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 21, "n_metadata": 21, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM2700529": "E15 forebrain; no exercise arm at this stage; paper analyses each stage separately (S1.2.p1)", "GSM2700530": "E15 forebrain; no exercise arm", "GSM2700531": "E15 forebrain; no exercise arm", "GSM2700532": "E15 forebrain; no exercise arm", "GSM2700533": "E15 forebrain; no exercise arm", "GSM2700534": "E15 forebrain; no exercise arm", "GSM2700535": "P5 DG; no exercise arm at this stage", "GSM2700536": "P5 DG; no exercise arm", "GSM2700537": "P5 DG; no exercise arm", "GSM2700538": "P5 DG; no exercise arm", "GSM2700539": "P5 DG; no exercise arm", "GSM2700540": "P5 DG; no exercise arm"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\aligned\\aligned_metadata_kept.csv", "columns": {"grp": {"source": "title", "regex": "^(Control|VPA\\+Run|VPA) 12w rep\\d$", "recode": {"Control": "Ctrl", "VPA": "VPA", "VPA+Run": "VPARun"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\aligned\\design_metadata.csv", "sha256": "5f820b1cfad66d57df08702d8305108f50620878140757fc1799395aadfded22", "levels": {"grp": {"Ctrl": 3, "VPA": 3, "VPARun": 3}}}}

reasoning: Tar per-sample files are named by GSM; exact match to the metadata index (21/21). Group derived from title (Control/VPA/VPA+Run at 12w). Per-sample file headers (Ctrl_12w_n_FPKM, VPA_12w_n_FPKM, VPA_12w_RUNn_FPKM) agree with the GSM titles.

### matrix (valid, not_started)

final: {"source": "GSE101239_RAW.tar per-sample Cufflinks gene FPKM (12w headers end in _FPKM)", "paper_input": "Cuffdiff on aligned reads; not deposited", "matrix_type": "FPKM", "recommended_method": "limma on log2(FPKM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\aligned\\aligned_matrix.csv", "sha256": "35fca8314a3b255ccd1a1e737d774f24453aba35083a24b020354e41dfbc9366", "n_features": 24322, "n_samples": 9, "annotation_columns_dropped": ["GSM2700529", "GSM2700530", "GSM2700531", "GSM2700532", "GSM2700533", "GSM2700534", "GSM2700535", "GSM2700536", "GSM2700537", "GSM2700538", "GSM2700539", "GSM2700540"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 41092.7, "median": 2.08375, "integer_fraction": 0.4298, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Per-sample file headers end in _FPKM (12w) and data_processing names Cufflinks/Cuffdiff; integer fraction 0.36 with decimals, per-sample totals ~4.8e5 (not counts). Counts are not deposited.

### design (valid, not_started)

final: {"analysis_type": "multi-group", "design_column": "grp", "contrasts": [{"name": "grp_VPARun_vs_VPA", "control": "VPA", "treatment": "VPARun", "role": "primary"}, {"name": "grp_VPA_vs_Ctrl", "control": "Ctrl", "treatment": "VPA", "role": "secondary"}, {"name": "grp_VPARun_vs_Ctrl", "control": "Ctrl", "treatment": "VPARun", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: One-way three-level model on the 12w samples; primary exercise contrast VPA+Run vs VPA (Fig. 5). VPA vs Ctrl is the paper's 12w DEG set that running normalizes; VPA+Run vs Ctrl is the normalization check (exploratory).

rejected alternatives: [{"value": "pool Ctrl and VPA as sedentary vs VPA+Run", "reason_rejected": "pools levels with different prenatal exposure; confounds exercise with VPA"}, {"value": "include E15/P5 samples in one model with stage", "reason_rejected": "different tissue/stage, no exercise arm; paper analysed within stage"}, {"value": "VPA x exercise factorial", "reason_rejected": "no Ctrl+RW arm; interaction not identifiable"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 9, "n_columns": 3, "columns": ["Intercept", "grp_VPA", "grp_VPARun"], "rank": 3, "full_rank": true, "residual_df": 6, "levels": {"grp": {"Ctrl": 3, "VPA": 3, "VPARun": 3}}, "cells": [{"cell": ["Ctrl"], "n": 3}, {"cell": ["VPA"], "n": 3}, {"cell": ["VPARun"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 9, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 9, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.cell type", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.age", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.4.genotype", "n_levels": 1, " ... [1472 more characters]

reasoning: Independent animals per group; no batch, sex or pairing recorded in GEO or paper.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (log2(FPKM+1), one-way model)", "formula": "~ grp", "paper_route": {"method": "Cuffdiff on aligned reads", "status": "blocked", "reason": "Cuffdiff needs read-level input; GEO deposits only per-sample FPKM"}, "deviations": ["limma on log2(FPKM+1) replaces Cuffdiff", "BH-adjusted limma p instead of Cuffdiff q", "three 12w groups fitted in one model (shared variance) instead of pairwise Cuffdiff"], "transform": "log2(x+1)"}

reasoning: Matrix policy: FPKM -> log2(x+1) -> limma. Never round FPKM for a count model.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "effect_inclusive": true}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "effect_inclusive": true}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "deviation_note": "q<0.05 and FC>=1.5 (S1.2.p1) converted exactly to padj<0.05 and |log2FC|>=log2(1.5)=0.5849625, applied on the limma route. Paper defined DEGs for VPA vs Ctrl; it never counted VPA+RW vs VPA DEGs."}

reasoning: S1.2.p1: q-value < 0.05, fold change >= 1.5.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "limma_12w", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\results\\limma_12w\\DEG_results_grp_VPARun_vs_VPA.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\results\\limma_12w\\DEG_results_grp_VPA_vs_Ctrl.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\results\\limma_12w\\DEG_results_grp_VPARun_vs_Ctrl.csv"], "counts": {"limma_12w/grp_VPARun_vs_VPA": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "n_tested": 19868, "n_significant": 4, "n_up": 1, "n_down": 3, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 19868, "n_significant": 4, "n_up": 1, "n_down": 3, "deg_sanity": "ok"}}, "limma_12w/grp_VPA_vs_Ctrl": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "n_tested": 19868, "n_significant": 3, "n_up": 2, "n_down": 1, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 19868, "n_significant": 3, "n_up": 2, "n_down": 1, "deg_sanity": "ok"}}, "limma_12w/grp_VPARun_vs_Ctrl": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "n_tested": 19868, "n_significant": 1, ... [164 more characters]

reasoning: One limma model on log2(FPKM+1) of the 9 12w samples; primary exercise contrast VPA+Run vs VPA, VPA vs Ctrl secondary, VPA+Run vs Ctrl exploratory.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "limma_12w_expfilter", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\results\\limma_12w_expfilter\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\results\\limma_12w_expfilter\\DEG_results_grp_VPARun_vs_VPA.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\results\\limma_12w_expfilter\\DEG_results_grp_VPA_vs_Ctrl.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\results\\limma_12w_expfilter\\DEG_results_grp_VPARun_vs_Ctrl.csv"], "counts": {"limma_12w_expfilter/grp_VPARun_vs_VPA": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "n_tested": 13847, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13847, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "limma_12w_expfilter/grp_VPA_vs_Ctrl": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "n_tested": 13847, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13847, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "limma_12w_expfilter/grp_VPARun_vs_Ctrl": {"applied ... [262 more characters]

reasoning: Same model after keeping genes with FPKM >= 1 in at least 3 of the 9 samples; Cuffdiff only tests genes with enough reads, so the unfiltered BH burden is heavier than the paper's. Sensitivity only; not in the paper.

### enrichment (valid, failed)

final: {"organism": "Mouse", "subset": "limma_12w/grp_VPARun_vs_VPA", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "effect_inclusive": true}, "direction": "all", "input_threshold_source": "applied", "execution_error": "Only 4 valid genes after filtering / ID conversion. Enrichment requires at least ~5 genes for meaningful results."}

reasoning: Paper interprets running via cell-migration GO terms (Fig. 5C-D); GSEA uses the full ranking.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_12w/grp_VPARun_vs_VPA", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29610328\\GSE101239\\results\\enrichment_limma_12w_grp_VPARun_vs_VPA\\gsea\\DEG_results_grp_VPARun_vs_VPA_GSEA_Hallmark.csv"], "summary": "GSEA complete on 19868 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 14 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_E2F_TARGETS | NES=2.30 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=2.03 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=1.56 | NOM p=0.00e+00 | FDR q=2.51e-02 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.55 | NOM p=9.06e-03 | FDR q=2.14e-02 - HALLMARK_MYC_TARGETS_V2 | NES=1.45 | NOM p=8.22e-03 | FDR q=4.05e-02 - HALLMARK_MITOTIC_SPINDLE | NES=1.42 | NOM p=0.00e+00 | FDR q=4.70e-02 - HALLMARK_PANCREAS_BETA_CELLS | NES=1.34 | NOM p=8.80e-02 | FDR q=9.34e-02 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.25 | NOM p=3.47e-02 | FDR q=1.89e-01 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.22 | NOM p=6.72e-02 | FDR q=2.08e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-1.54 | NOM p=0.00e+00 | FDR q=1.03e-01 - HALLMARK_COAGULATION | NES=-1.50 | NOM p=1.17 ... [416 more characters]

reasoning: Paper interprets running via cell-migration GO terms (Fig. 5C-D); GSEA uses the full ranking.

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Exercise effect is identifiable only in VPA-exposed mice (no Ctrl+RW arm).", "n = 3 per group; limma on FPKM replaces Cuffdiff.", "Paper gives no DEG count for VPA+RW vs VPA or for 12w VPA vs Ctrl in the text."], "results": {"limma_12w/grp_VPARun_vs_VPA": {"n_deg": 4, "up": 1, "down": 3, "rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "audit_n": 4}, "limma_12w/grp_VPA_vs_Ctrl": {"n_deg": 3, "up": 2, "down": 1, "rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "audit_n": 3}, "limma_12w/grp_VPARun_vs_Ctrl": {"n_deg": 1, "up": 0, "down": 1, "rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "audit_n": 1}, "limma_12w_expfilter/grp_VPARun_vs_VPA": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "audit_n": 0}, "limma_12w_expfilter/grp_VPA_vs_Ctrl": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "audit_n": 0}, "limma_12w_expfilter/grp_VPARun_vs_Ctrl": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05 and |log2FoldChange| >= 0.584963", "audit_n": 0}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"limma_12w/grp_VPARun_vs_VPA": {"Cxcr4": {"AveExpr": 5.3424, "log2FoldChange": 1.2729, "padj": 0.346, "pvalue": 0.00862}, "Cntn2": {"AveExpr": 3.912, "log2FoldChange": 1.1357, "padj": 0.234, "pvalue": 0.0016}}, "limma_12w/grp_VPA_vs_Ctrl": {"Cxcr4": {"AveExpr": 5.3424, "log2FoldChange": -0.9609, "padj": 0.816, "pvalue": 0.0285}, " ... [89 more characters]

reasoning: Paper: Cxcr4 and Cntn2 down in VPA vs Ctrl at 12w (Fig. 3D-E); running restores Cxcr4 (Fig. 5E), so expected up in VPA+RW vs VPA.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "Cuffdiff on reads",
    "data": "only per-sample FPKM deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "P5 file names",
    "paper": "Control",
    "data": "tar file names say Contol (typo); stage excluded anyway",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID29610328 / GSE101239

Run folder: `test/experiments/large_run_pilot_20261019/runs_claude/PMID29610328`. Spec: `case_spec.json`. The runner finished with status `completed`. The contract validator checked 13 records and found 0 errors. No external LLM calls were made.

## What ran
- **Paper.** Fig. 5 / S1.4.p2 sets the exercise question: 8 weeks of voluntary wheel running in prenatally VPA-exposed mice. The tissue is 12-week dentate-gyrus Nestin-EGFP+ NS/PCs, and the contrast is VPA+RW vs VPA. There is no Ctrl+RW arm. The exercise effect can therefore only be estimated within VPA mice, and a VPA x exercise interaction cannot be estimated.
- **Data.** GSE101239_RAW.tar holds per-sample Cufflinks FPKM files (the 12w file headers end in `_FPKM`). No counts were deposited. Samples were aligned exactly on the GSM index (21/21). The 12 E15 and P5 samples were excluded: those stages have no exercise arm, and the paper analysed each stage separately (S1.2.p1). Analysed: 9 samples at 12w, Ctrl 3 / VPA 3 / VPA+Run 3. Sex was inferred as all female; one sample (GSM2700549) had low confidence.
- **Method.** One limma model, `~ grp`, on log2(FPKM+1) (`run_joint_limma`). It produced three contrasts:
  - VPARun_vs_VPA (primary, exercise)
  - VPA_vs_Ctrl (secondary; the paper's 12w VPA-DEG set)
  - VPARun_vs_Ctrl (exploratory; checks normalisation back to Ctrl)
- **Sensitivity run.** The same model was refitted after keeping only genes with FPKM >= 1 in at least 3 samples.
- **Enrichment.** GSEA (Hallmark) completed on the primary contrast. ORA was attempted but did not run (only 4 DEGs).

## DEG counts vs paper
Paper threshold (S1.2.p1): q < 0.05 and FC >= 1.5. Applied exactly as padj < 0.05 and |log2FC| >= 0.5849625 (`paper_on_deviation_route`).

| Contrast | Ours (up/down) | Sensitivity, FPKM>=1 filter | Paper |
|---|---|---|---|
| VPA+RW vs VPA (exercise) | 4 (1/3): Gjc3, Gm14379, Arhgef4 down; Wipf3 up | 0 | no count reported; "mostly amended" VPA-distorted genes (Fig. 5B) |
| VPA vs Ctrl, 12w | 3 (2/1) | 0 | no 12w count in the text ("hundreds" per stage, S2.p2) |
| VPA+RW vs Ctrl | 1 | 0 | not reported |

Named genes:
- **Cxcr4.** Down in VPA vs Ctrl (log2FC -0.96, p = 0.029, padj 0.82). Up in RW vs VPA (+1.27, p = 0.0086, padj 0.35). The direction matches the paper; the change is significant only at nominal p, not after FDR correction.
- **Cntn2.** Down in VPA vs Ctrl (-0.73, p = 0.014). Up in RW vs VPA (+1.14, p = 0.0016, padj 0.23). The direction  ... [1737 more characters]
