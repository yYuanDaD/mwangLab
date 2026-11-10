# Review packet B (the analysis' decisions): GSE266883

## Mechanical flags

- **unused_subject_like_column**: {"column": "source_name_ch1", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "characteristics_ch1.0.tissue", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "characteristics_ch1.2.treatment", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "title without the source_name_ch1 level", "across": "source_name_ch1", "pairs_or_sets": 3, "samples_linked": 9, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Samples per design level

### `grp`
- **LSI** (3): GSM8255524 / Nucleus pulposus cells from LSI #1, RNA- / LSI_1,Sham_LSI_LSI_E_RPKM.txt; GSM8255525 / Nucleus pulposus cells from LSI #2, RNA- / LSI_2,Sham_LSI_LSI_E_RPKM.txt; GSM8255526 / Nucleus pulposus cells from LSI #3, RNA- / LSI_3,Sham_LSI_LSI_E_RPKM.txt
- **LSIE** (3): GSM8255527 / Nucleus pulposus cells from LSI-E #1, RN / LSI_E_1,Sham_LSI_LSI_E_RPKM.txt; GSM8255528 / Nucleus pulposus cells from LSI-E #2, RN / LSI_E_2,Sham_LSI_LSI_E_RPKM.txt; GSM8255529 / Nucleus pulposus cells from LSI-E #3, RN / LSI_E_3,Sham_LSI_LSI_E_RPKM.txt
- **Sham** (3): GSM8255521 / Nucleus pulposus cells from sham operati / Sham_1,Sham_LSI_LSI_E_RPKM.txt; GSM8255522 / Nucleus pulposus cells from sham operati / Sham_2,Sham_LSI_LSI_E_RPKM.txt; GSM8255523 / Nucleus pulposus cells from sham operati / Sham_3,Sham_LSI_LSI_E_RPKM.txt

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE266883"], "assay": "bulk RNA-seq of nucleus pulposus (NP) tissue/cells; rat L4-L5 IVDs (Sham, LSI, LSI-E; n=3 each) plus a separate human normal vs degenerated NP series (n=3 each) in the same GEO series", "organism": "Rattus norvegicus (male SD rats, S4.20.p1)", "factors": {"grp": ["Sham (sham operation)", "LSI (lumbar spinous process resection, no exercise)", "LSI-E (LSI + treadmill running, 8 weeks)"]}, "sample_inclusion": "rat samples only (9) for the exercise question; the 6 human IVDD/Normal samples address degeneration, not exercise, and are on a different matrix/organism", "primary_estimand": "effect of treadmill exercise on NP transcriptome in lumbar-instability rats: LSI-E vs LSI (Fig. 2G-J, S2.1.p2)", "planned_contrasts": ["LSI-E vs LSI (primary; S2.1.p2, Fig. 2G-J; paper reports GO/GSEA, no DEG count)", "LSI-E vs Sham (secondary; S2.1.p2, Supplementary Fig. 2A; no DEG count)"], "repeated_measure_unit": "none; one sample per rat", "normalization": "RPKM (GEO data_processing)", "paper_method": "not stated (DEG method unreported; GSEA 4.2.3 with NES |>1|, p<0.05, FDR q<0.25 - S4.3.p2, S4.21.p1)", "paper_threshold": {"metric": null, "cutoff": null, "effect_metric": null, "effect_cutoff": null, "stated": false, "source_locator": "not stated for DEGs; S4.3.p2 gives only GSEA cutoffs"}, "paper_results": "LSI-E vs LSI DEGs enriched for immune/inflammatory GO terms; GSEA: cytosolic DNA-sensing pathway, inflammatory response, NF-kB signaling up in LSI-E  ... [22 more characters]

reasoning: S2.1.p2: L4-L5 IVDs from sham, LSI and LSI-E rats were RNA-sequenced; DEGs LSI-E vs Sham and LSI-E vs LSI analysed by GO/KEGG/GSEA. Fig 2 legend: n=3 per group for RNA-seq. S4.20.2.p1 describes treadmill exercise. No DEG test or threshold is reported anywhere (S4.21.p1, S4.25.p1).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE266883\\GSE266883_Sham_LSI_LSI_E_RPKM.txt.gz", "owned": true, "checks": "S10.p1 names GSE266883; GEO samples GSM8255521-29 are Sham/LSI/LSI-E rat NP RNA-seq matching Fig 2A design (n=3 each); matrix GSE266883_Sham_LSI_LSI_E_RPKM.txt.gz columns Sham_1-3, LSI_1-3, LSI_E_1-3 match metadata description field", "accession": "GSE266883", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE266883\\GSE266883_metadata.csv"}

reasoning: Data availability statement S10.p1 deposits GSE266883; contact institute Wuhan Union Hospital matches authors.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 9, "n_metadata": 15, "coverage": 0.6, "unmatched_matrix_columns": ["Chr", "Start", "End", "Length"], "unmatched_metadata_samples": ["GSM8255515", "GSM8255516", "GSM8255517", "GSM8255518", "GSM8255519", "GSM8255520"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "description", "regex": "^(Sham|LSI_E|LSI)_\\d+,", "recode": {"Sham": "Sham", "LSI": "LSI", "LSI_E": "LSIE"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\aligned\\design_metadata.csv", "sha256": "94ebc83545df0be27a711c9fb7bd641ed2df1b7552d54b5b2ab6656a6e3e222b", "levels": {"grp": {"Sham": 3, "LSI": 3, "LSIE": 3}}}}

reasoning: Matrix columns equal the token before the comma in metadata 'description' (e.g. 'LSI_E_1,Sham_LSI_LSI_E_RPKM.txt'); group derived from the same token and cross-checked with characteristics_ch1.2.treatment (Sham operation/LSI/LSI-E). Human samples excluded. The 6 human samples (GSM8255515-20) have no column in this rat matrix and drop out at alignment; not part of the exercise question.

### matrix (valid, not_started)

final: {"matrix_type": "RPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\aligned\\aligned_matrix.csv", "sha256": "01b48e550d4c6adccd2fc124eec8de1315e26781d234bc0471884e2c7a7a325a", "n_features": 23486, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 33346.03004, "median": 1.822891582, "integer_fraction": 0.1636, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name says RPKM; GEO data_processing: 'Read Per Kilobase of exon per Megabase of library size (RPKM) were calculated'; values are non-integer (integer fraction 0.16) with median 1.8. No raw counts deposited. Paper does not state its DE input.

### design (valid, not_started)

final: {"analysis_type": "multi-group (3 levels), one model, planned pairwise contrasts", "design_column": "grp", "contrasts": [{"name": "grp_LSIE_vs_LSI", "control": "LSI", "treatment": "LSIE", "role": "primary"}, {"name": "grp_LSIE_vs_Sham", "control": "Sham", "treatment": "LSIE", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: Primary estimand is exercise within LSI rats (LSI-E vs LSI, Fig 2G-J). Paper also compares LSI-E vs Sham (Supp Fig 2A), which confounds surgery and exercise and is secondary. LSI vs Sham (surgery effect) is not exercise and only exploratory. One limma model on all 9 rat samples. All three pairwise comparisons are fitted from the same model; grp_LSI_vs_Sham (surgery effect) is exploratory, not an exercise estimand.

rejected alternatives: [{"value": "pool LSI and Sham as non-exercise control", "reason_rejected": "pools distinct levels; Sham did not undergo surgery"}, {"value": "include human IVDD vs Normal", "reason_rejected": "degeneration, not exercise; different organism"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 9, "n_columns": 3, "columns": ["Intercept", "grp_LSIE", "grp_Sham"], "rank": 3, "full_rank": true, "residual_df": 6, "levels": {"grp": {"Sham": 3, "LSI": 3, "LSIE": 3}}, "cells": [{"cell": ["LSI"], "n": 3}, {"cell": ["LSIE"], "n": 3}, {"cell": ["Sham"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 9, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 9, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 3, "status": "complete_confounding", "crosstab": {"LSI": {"Nucleus pulposus tissue from LSI": 3, "Nucleus pulposus tissue from LSI-E": 0, "Nucleus pulposus tissue from sham operation": 0}, "LSIE": {"Nucleus pulposus tissue from LSI": 0, "Nucleus pulposus tissue from LSI-E": 3, "Nucleus pulposus tissue from sham operation": 0}, "Sham": {"Nucleus pulposus tissue from LSI": 0, "Nucleus pulposus tissue from LSI-E": 0, "Nucleus pulposus tissue from sham operation": 3}}}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"colum ... [2579 more characters]

reasoning: Independent male rats, one sample each; no batch, sex or lane annotation in GEO; all rat samples on one platform (GPL24688) and one matrix.

### method (valid, not_started)

final: {"matrix_type": "RPKM", "method": "limma (moderated t, empirical Bayes) on log2(RPKM+1)", "formula": "~ grp", "paper_route": {"method": "not stated", "status": "not_reported", "reason": "paper reports no DEG method; only RPKM deposited"}, "deviations": ["limma on log2(RPKM+1) chosen by policy because only RPKM is deposited and the paper names no DE method"], "transform": "log2(x+1)"}

reasoning: Matrix policy: linear normalized RPKM -> log2(x+1) then limma. Count methods would need raw counts, not deposited; RPKM is not rounded.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": null, "cutoff": null, "effect_metric": null, "effect_cutoff": null, "stated": false}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: Paper states no DEG threshold (only GSEA NES/p/FDR q cutoffs in S4.3.p2), so the workflow default BH-adjusted p < 0.05 with no fold-change rule is used and marked as fallback.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\joint\\DEG_results_grp_LSIE_vs_LSI.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\joint\\DEG_results_grp_LSI_vs_Sham.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\joint\\DEG_results_grp_LSIE_vs_Sham.csv"], "counts": {"joint/grp_LSIE_vs_LSI": {"applied": {"rule": "padj < 0.05", "n_tested": 23486, "n_significant": 9801, "n_up": 7373, "n_down": 2428, "deg_sanity": "ok"}}, "joint/grp_LSI_vs_Sham": {"applied": {"rule": "padj < 0.05", "n_tested": 23486, "n_significant": 10686, "n_up": 1979, "n_down": 8707, "deg_sanity": "ok"}}, "joint/grp_LSIE_vs_Sham": {"applied": {"rule": "padj < 0.05", "n_tested": 23486, "n_significant": 9438, "n_up": 4169, "n_down": 5269, "deg_sanity": "ok"}}}}

reasoning: one limma model (~ grp) on all 9 rat samples, log2(RPKM+1); grp_LSIE_vs_LSI is the exercise estimand, grp_LSIE_vs_Sham secondary per paper, grp_LSI_vs_Sham exploratory

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "joint_tpm_filt", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\joint_tpm_filt\\input\\matrix_filtered_normalized.csv", "transform": "log2(CPM+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\joint_tpm_filt\\DEG_results_grp_LSIE_vs_LSI.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\joint_tpm_filt\\DEG_results_grp_LSI_vs_Sham.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\joint_tpm_filt\\DEG_results_grp_LSIE_vs_Sham.csv"], "counts": {"joint_tpm_filt/grp_LSIE_vs_LSI": {"applied": {"rule": "padj < 0.05", "n_tested": 6292, "n_significant": 4735, "n_up": 3222, "n_down": 1513, "deg_sanity": "implausible_sig_fraction=75%(4735/6292)"}}, "joint_tpm_filt/grp_LSI_vs_Sham": {"applied": {"rule": "padj < 0.05", "n_tested": 6292, "n_significant": 4937, "n_up": 1233, "n_down": 3704, "deg_sanity": "implausible_sig_fraction=78%(4937/6292)"}}, "joint_tpm_filt/grp_LSIE_vs_Sham": {"applied": {"rule": "padj < 0.05", "n_tested": 6292, "n_significant": 4436, "n_up": 1984, "n_down": 2452, "deg_sanity": "implausible_sig_fraction=71%(4436/6292)"}}}}

reasoning: sensitivity: RPKM column sums differ by group (LSI carries a few genes up to 33k RPKM, shifting the median); rescaling each column to sum 1e6 (TPM-equivalent) before log2 and dropping genes with RPKM<1 in fewer than 3 samples tests whether the skewed up/down balance is a composition artefact

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "joint/grp_LSIE_vs_LSI", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\enrichment_joint_grp_LSIE_vs_LSI\\ora\\DEG_results_grp_LSIE_vs_LSI_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\enrichment_joint_grp_LSIE_vs_LSI\\ora\\DEG_results_grp_LSIE_vs_LSI_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\enrichment_joint_grp_LSIE_vs_LSI\\ora\\DEG_results_grp_LSIE_vs_LSI_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\enrichment_joint_grp_LSIE_vs_LSI\\ora\\DEG_results_grp_LSIE_vs_LSI_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 9801 Rat genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms  ... [1366 more characters]

reasoning: paper claims GO/KEGG/GSEA inflammatory, NF-kB and cytosolic DNA-sensing activation in LSI-E vs LSI (Fig 2G-I); rat symbols on mouse sets

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "joint/grp_LSIE_vs_LSI", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38982049\\GSE266883\\results\\enrichment_joint_grp_LSIE_vs_LSI\\gsea\\DEG_results_grp_LSIE_vs_LSI_GSEA_Hallmark.csv"], "summary": "GSEA complete on 23486 Rat genes ranked by 'stat'. 50 Hallmark sets tested, 38 significant at FDR q < 0.25. Rat genes matched to mouse Hallmark by symbol: 3975/4291 Hallmark genes present in the ranking. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_COAGULATION | NES=1.99 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.95 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HEME_METABOLISM | NES=1.89 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.87 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.85 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COMPLEMENT | NES=1.85 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.80 | NOM p=0.00e+00 | FDR q=2.74e-04 - HALLMARK_APOPTOSIS | NES=1.77 | NOM p=0.00e+00 | FDR q=3.59e-04 - HALLMARK_E2F_TARGETS | NES=1.75 | NOM p=0.00e+00 | FDR q=3.19e-04 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES= ... [542 more characters]

reasoning: paper claims GO/KEGG/GSEA inflammatory, NF-kB and cytosolic DNA-sensing activation in LSI-E vs LSI (Fig 2G-I); rat symbols on mouse sets

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper reports no DEG method, threshold or DEG counts; the DE route (limma on log2 RPKM) and threshold (workflow default) are not reproductions of a stated paper rule.", "n=3 rats per arm.", "About 10-20 gene IDs in the deposited matrix are Excel-date-mangled (e.g. 1-Mar, 15-Sep); left as deposited.", "Very large DEG sets (9801 LSIE vs LSI at BH<0.05, 4735 after TPM rescaling + RPKM>=1 filter): within-group Spearman r ~0.99 vs between-group ~0.93, and LSI columns have a different RPKM distribution (max ~33k vs ~14k); consistent with group-wise library processing that GEO does not record, so group may be partly aliased with an unrecorded batch.", "Pathway direction agrees with the paper: Hallmark INFLAMMATORY_RESPONSE, TNFA_SIGNALING_VIA_NFKB, IFN-gamma up in LSI-E vs LSI (GSEA FDR<0.001); KEGG ORA Osteoclast differentiation adj p 0.050 but Cytosolic DNA-sensing (0.70) and NF-kB (0.16) not significant by ORA on the all-direction DEG list."], "results": {"joint/grp_LSIE_vs_LSI": {"n_deg": 9801, "up": 7373, "down": 2428, "rule": "padj < 0.05"}, "joint/grp_LSI_vs_Sham": {"n_deg": 10686, "up": 1979, "down": 8707, "rule": "padj < 0.05"}, "joint/grp_LSIE_vs_Sham": {"n_deg": 9438, "up": 4169, "down": 5269, "rule": "padj < 0.05"}, "joint_tpm_filt/grp_LSIE_vs_LSI": {"n_deg": 4735, "up": 3222, "down": 1513, "rule": "padj < 0.05"}, "joint_tpm_filt/grp_LSI_vs_Sham": {"n_deg": 4937, "up": 1233, "down": 3704, "rule": "padj < 0.05"}, "joint_tpm_filt/grp ... [144 more characters]

reasoning: Contrast and sample set match the paper; comparison to the paper is at the pathway level (inflammatory response, NF-kB, cytosolic DNA sensing up in LSI-E).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DEG method and threshold",
    "paper": "not reported",
    "data": "RPKM only",
    "disposition": "executable_without_change"
  },
  {
    "item": "GEO series contains human IVDD/Normal samples",
    "paper": "human NP RNA-seq used for degeneration correlation (S2.1.p3), not exercise",
    "data": "separate human RPKM file, 6 samples",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID38982049 / GSE266883

## What ran
- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`). Validator: 13 records, 0 errors. Status: completed, route `paper_aligned`.
- Data: rat NP RNA-seq matrix `GSE266883_Sham_LSI_LSI_E_RPKM.txt.gz` (23,486 genes x 9 samples: Sham, LSI, LSI-E with n=3 each). The 6 human IVDD/Normal samples in the same series answer a degeneration question, not an exercise one. They have no columns in the rat matrix and drop out at alignment.
- Alignment: exact match on a key taken from metadata `description` (the token before the comma). Group comes from the same token and agrees with `characteristics_ch1.2.treatment`.
- Matrix: RPKM (file name, GEO data_processing, non-integer values). No raw counts were deposited.
- Design: `~ grp`, one limma model on all 9 samples. The primary exercise estimand is LSIE vs LSI (Fig. 2G-J, S2.1.p2). LSIE vs Sham is secondary (Supp. Fig. 2A). LSI vs Sham is the surgery effect and is exploratory. No covariates, because GEO records no batch.
- Method: limma on log2(RPKM+1) (primary). Sensitivity run: log2(CPM+1) on RPKM, which rescales each column to TPM-equivalent, plus a filter keeping genes with RPKM >= 1 in at least 3 samples (14,203 kept).
- Enrichment on joint/grp_LSIE_vs_LSI: ORA (GO/KEGG mouse) and Hallmark GSEA, using rat symbols on mouse gene sets.

## DEG counts vs paper
The paper reports no DEG method, no DEG threshold and no DEG counts. It gives GSEA cutoffs only (S4.3.p2). The applied rule is therefore `workflow_default`: BH padj < 0.05, no fold-change cutoff.

| Contrast | Primary (log2 RPKM+1) | Sensitivity (TPM-rescaled + filter) | Paper |
|---|---|---|---|
| LSIE vs LSI (primary) | 9801 (7373 up / 2428 down) | 4735 (3222 / 1513) | not reported |
| LSIE vs Sham (secondary) | 9438 (4169 / 5269) | 4436 (1984 / 2452) | not reported |
| LSI vs Sham (exploratory) | 10686 (1979 / 8707) | 4937 (1233 / 3704) | not reported |

Pathway level, LSIE vs LSI, agrees in direction with the paper:
- In Hallmark GSEA, INFLAMMATORY_RESPONSE (NES 1.67), TNFA_SIGNALING_VIA_NFKB (1.87), IFN-gamma, IL6/JAK/STAT3 and complement are all up, each at FDR < 0.001.
- In KEGG ORA, Osteoclast differentiation reaches adj p 0.050. NF-kB signaling (0.16) and Cytosolic DNA-sensing (0.70) are not significant by ORA on the all-direction DEG list.

## Deviations and caveats
- The DE method and threshold are not reproductions of a stated paper rule, because none is reported.
- The DEG sets ar ... [1153 more characters]
