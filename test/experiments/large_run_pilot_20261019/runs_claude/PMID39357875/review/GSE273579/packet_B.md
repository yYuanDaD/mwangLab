# Review packet B (the analysis' decisions): GSE273579

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.4.treatment", "n_values": 5, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## Samples per design level

### `ex`
- **EX** (8): GSM8432626 / High fat diet fed mouse, Exercise, non-t; GSM8432627 / High fat diet fed mouse, Exercise, non-t; GSM8432628 / High fat diet fed mouse, Exercise, non-t; GSM8432629 / High fat diet fed mouse, Exercise, non-t; GSM8432630 / High fat diet fed mouse, Exercise, tumor; GSM8432631 / High fat diet fed mouse, Exercise, tumor; GSM8432632 / High fat diet fed mouse, Exercise, tumor; GSM8432633 / High fat diet fed mouse, Exercise, tumor
- **NE** (12): GSM8432614 / Normal diet fed mouse, Non exercise, mou; GSM8432615 / Normal diet fed mouse, Non exercise, mou; GSM8432616 / Normal diet fed mouse, Non exercise, mou; GSM8432617 / Normal diet fed mouse, Non exercise, mou; GSM8432618 / High fat diet fed mouse, Non exercise, n; GSM8432619 / High fat diet fed mouse, Non exercise, n; GSM8432620 / High fat diet fed mouse, Non exercise, n; GSM8432621 / High fat diet fed mouse, Non exercise, n; GSM8432622 / High fat diet fed mouse, Non exercise, t; GSM8432623 / High fat diet fed mouse, Non exercise, t; GSM8432624 / High fat diet fed mouse, Non exercise, t; GSM8432625 / High fat diet fed mouse, Non exercise, t

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE273579"], "assay": "bulk RNA-seq (TruSeq stranded mRNA, NextSeq 500 SE76), mouse liver", "model": "neonatal DMBA + high-fat diet steatosis-associated liver cancer, male C57BL/6 mice; treadmill 18 m/min, 20 min/day, 5 d/wk for last 10 of 35 weeks", "factors": {"exercise": ["non-exercise", "exercise"], "tissue": ["non-tumor", "tumor"], "diet": ["ND (non-exercise only)", "HFD"]}, "sample_inclusion": "HFD-fed DMBA mice, n=4 per exercise arm; non-tumor and tumor liver tissue from each mouse; ND non-exercise mice (n=4) are a diet reference with no exercise arm", "primary_estimand": "Effect of regular treadmill exercise vs non-exercise on liver gene expression in DMBA/HFD mice, within non-tumor and within tumor tissue", "planned_contrasts": ["HFD exercise vs HFD non-exercise, non-tumor liver (abstract: exercise vs non-exercise liver profiles; no DEG count in abstract)", "HFD exercise vs HFD non-exercise, tumor tissue (GEO summary: RNA from non-tumor and tumor tissues; no DEG count in abstract)"], "repeated_measure_unit": "mouse (tumor and non-tumor from the same liver); irrelevant within a tissue stratum", "paper_method": "not stated in abstract", "paper_threshold": {"metric": "not stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "abstract only; full text unavailable"}, "paper_results": "Per1 and Cry2 up in exercise; E2F1 and c-Myc target genes down; E2f1 and Myc mRNA unchanged"}

reasoning: No full text. Abstract (PubMed efetch) and GEO series summary/overall_design define the estimand: exercise vs non-exercise in HFD/DMBA livers; GEO says non-tumor and tumor tissue were both sequenced. Method and threshold are not stated.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["GEO Series_pubmed_id = 39357875", "series title equals paper title", "20 GSM per-sample featureCounts files in GSE273579_RAW.tar match the 20 metadata samples"], "accession": "GSE273579", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE273579\\GSE273579_metadata.csv"}

reasoning: GEO series links PMID 39357875 and shares the title.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 20, "n_metadata": 20, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\aligned\\aligned_metadata.csv", "columns": {"ex": {"source": "characteristics_ch1.4.treatment", "regex": "(Non exercise|Exercise)", "recode": {"Non exercise": "NE", "Exercise": "EX"}}, "tis": {"source": "characteristics_ch1.4.treatment", "regex": "(Normal diet|non-tumor|tumor tissue)", "recode": {"Normal diet": "ND", "non-tumor": "NT", "tumor tissue": "T"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\aligned\\design_metadata.csv", "sha256": "9c61c9f109beb5e71c6d1ebf33e19ec5cddf0a8f1c21c811ed0c5edf62a4ec8d", "levels": {"ex": {"NE": 12, "EX": 8}, "tis": {"NT": 8, "T": 8, "ND": 4}}}}

reasoning: Tar columns become GSM ids and equal the metadata index (20/20). ex = exercise arm, tis = ND liver / HFD non-tumor / HFD tumor, from the treatment characteristic.

### matrix (valid, not_started)

final: {"source": "GSE273579_RAW.tar per-sample featureCounts outputs (last column = read counts), merged", "paper_input": "not stated in abstract; GEO data_processing: STAR + featureCounts raw count matrices", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\aligned\\aligned_matrix.csv", "sha256": "bd43fd7d8f7e8c84c3591450e2cf5478300d0d6b029098e7655dcb79d7d5def0", "n_features": 55359, "n_samples": 20, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3150344.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Per-sample files are featureCounts outputs (header line '# Program:featureCounts v2.0.5'), integer fraction 1.0, library sizes 16-20 M. GEO data_processing says the supplementary files hold TPM, but the deposited files are raw featureCounts counts; recorded as a discrepancy.

### design (valid, not_started)

final: {"analysis_type": "two-group within tissue strata", "design_column": "ex", "control": "NE", "treatment": "EX", "contrasts": [{"name": "ex_EX_vs_NE_tis-NT", "control": "NE", "treatment": "EX", "role": "primary"}, {"name": "ex_EX_vs_NE_tis-T", "control": "NE", "treatment": "EX", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\suitability\\suitability.md", "n_comparisons": 2, "n_analyzable": 2}}

reasoning: Exercise is randomized among HFD/DMBA mice only, so each exercise contrast is within HFD and within one tissue (4 vs 4). The non-tumor liver is the primary analysis per the abstract's 'livers of the exercise and non-exercise groups'; tumor tissue is secondary. ND samples are not used in any contrast.

rejected alternatives: [{"value": "pool tumor and non-tumor tissue in one exercise contrast", "reason_rejected": "tissue type dominates expression; GEO describes them as separate tissues; comparisons stay within tissue"}, {"value": "HFD non-exercise vs ND non-exercise", "reason_rejected": "diet contrast, not exercise; ND has no exercise arm"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(ex)", "n_samples": 20, "n_columns": 2, "columns": ["Intercept", "ex_NE"], "rank": 2, "full_rank": true, "residual_df": 18, "levels": {"ex": {"NE": 12, "EX": 8}}, "cells": [{"cell": ["EX"], "n": 8}, {"cell": ["NE"], "n": 12}], "min_cell_size": 8, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 20, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 20, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.age", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.genotype", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.4.treatment", "n_levels": 5, "status": "nested_in_primary", "crosstab": {"EX": {"High fat d ... [2340 more characters]

reasoning: Within a tissue stratum each mouse contributes one sample, so no blocking is needed; no batch or sequencing-run variable is recorded; all mice male, same age, euthanized the same day.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ ex", "paper_route": {"method": "not stated in abstract", "status": "unknown", "reason": "full text unavailable"}, "deviations": ["paper's DE method unknown; workflow default DESeq2 on raw counts"]}

reasoning: Raw featureCounts counts support DESeq2; fitted separately in each tissue stratum.

### threshold (valid, not_started)

final: {"paper_threshold": null, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Abstract states no threshold; BH padj < 0.05 without fold-change cutoff is the workflow default. Raw p < 0.05 is reported only as a labelled audit rule."}

reasoning: No threshold in the abstract or GEO record.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "ex_EX_vs_NE_tis-NT", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\ex_EX_vs_NE_tis-NT\\input\\matrix.csv", "formula": "~ ex", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\ex_EX_vs_NE_tis-NT\\DEG_results_EX_vs_NE.csv"], "counts": {"ex_EX_vs_NE_tis-NT": {"applied": {"rule": "padj < 0.05", "n_tested": 13999, "n_significant": 189, "n_up": 144, "n_down": 45, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 26195, "n_significant": 1599, "n_up": 816, "n_down": 783, "deg_sanity": "ok"}}}}

reasoning: HFD exercise vs non-exercise, non-tumor liver, 4 vs 4

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "ex_EX_vs_NE_tis-T", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\ex_EX_vs_NE_tis-T\\input\\matrix.csv", "formula": "~ ex", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\ex_EX_vs_NE_tis-T\\DEG_results_EX_vs_NE.csv"], "counts": {"ex_EX_vs_NE_tis-T": {"applied": {"rule": "padj < 0.05", "n_tested": 14195, "n_significant": 68, "n_up": 51, "n_down": 17, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 26557, "n_significant": 978, "n_up": 512, "n_down": 466, "deg_sanity": "ok"}}}}

reasoning: HFD exercise vs non-exercise, tumor tissue, 4 vs 4

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ex_EX_vs_NE_tis-NT", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\enrichment_ex_EX_vs_NE_tis-NT\\ora\\DEG_results_EX_vs_NE_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\enrichment_ex_EX_vs_NE_tis-NT\\ora\\DEG_results_EX_vs_NE_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\enrichment_ex_EX_vs_NE_tis-NT\\ora\\DEG_results_EX_vs_NE_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\enrichment_ex_EX_vs_NE_tis-NT\\ora\\DEG_results_EX_vs_NE_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 189 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Entrainment Of Circadian Clock By Photoperiod (GO:0043153) | padj=4.90e-05 | overlap=6/23 | genes=PER2;PER1;PER3;ID2;USP2;CRY2 - Photoperiodism (GO:00096 ... [1186 more characters]

reasoning: abstract reports E2F/Myc target down-regulation (Hallmark E2F_TARGETS / MYC_TARGETS)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ex_EX_vs_NE_tis-NT", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\enrichment_ex_EX_vs_NE_tis-NT\\gsea\\DEG_results_EX_vs_NE_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25986 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 45 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_BILE_ACID_METABOLISM | NES=2.18 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=2.01 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.88 | NOM p=0.00e+00 | FDR q=2.68e-04 - HALLMARK_HEME_METABOLISM | NES=1.77 | NOM p=0.00e+00 | FDR q=2.21e-03 - HALLMARK_PROTEIN_SECRETION | NES=1.73 | NOM p=0.00e+00 | FDR q=1.93e-03 - HALLMARK_ANDROGEN_RESPONSE | NES=1.65 | NOM p=0.00e+00 | FDR q=4.29e-03 - HALLMARK_COAGULATION | NES=1.64 | NOM p=1.73e-03 | FDR q=4.25e-03 - HALLMARK_MYC_TARGETS_V1 | NES=1.64 | NOM p=0.00e+00 | FDR q=4.52e-03 - HALLMARK_MYC_TARGETS_V2 | NES=1.56 | NOM p=5.89e-03 | FDR q=9.91e-03 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.47 | NOM p=7.81e-03 | FDR q=2.27e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=-2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-2.27 | NOM p=0.00e+00 | FD ... [390 more characters]

reasoning: abstract reports E2F/Myc target down-regulation (Hallmark E2F_TARGETS / MYC_TARGETS)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ex_EX_vs_NE_tis-T", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\enrichment_ex_EX_vs_NE_tis-T\\ora\\DEG_results_EX_vs_NE_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\enrichment_ex_EX_vs_NE_tis-T\\ora\\DEG_results_EX_vs_NE_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\enrichment_ex_EX_vs_NE_tis-T\\ora\\DEG_results_EX_vs_NE_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\enrichment_ex_EX_vs_NE_tis-T\\ora\\DEG_results_EX_vs_NE_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 68 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Entrainment Of Circadian Clock By Photoperiod (GO:0043153) | padj=5.21e-06 | overlap=5/23 | genes=PER1;PER3;ID2;USP2;CRY2 - Photoperiodism (GO:0009648) | padj= ... [1181 more characters]

reasoning: same pathway check in tumor tissue

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ex_EX_vs_NE_tis-T", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39357875\\GSE273579\\results\\enrichment_ex_EX_vs_NE_tis-T\\gsea\\DEG_results_EX_vs_NE_GSEA_Hallmark.csv"], "summary": "GSEA complete on 26336 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 44 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.88 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.30 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.18 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_BILE_ACID_METABOLISM | NES=2.11 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.00 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=1.84 | NOM p=0.00e+00 | FDR q=7.55e-04 - HALLMARK_P53_PATHWAY | NES=1.57 | NOM p=0.00e+00 | FDR q=1.24e-02 - HALLMARK_HEME_METABOLISM | NES=1.57 | NOM p=1.99e-03 | FDR q=1.16e-02 - HALLMARK_PANCREAS_BETA_CELLS | NES=1.45 | NOM p=5.61e-02 | FDR q=3.57e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_G2M_CHECKPOINT | NES=-3.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=-2.85 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES= ... [388 more characters]

reasoning: same pathway check in tumor tissue

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Comparison with the paper rests on the abstract and GEO description only; no paper DEG counts available.", "Paper method and threshold unknown; workflow default used.", "Direction contradiction in non-tumor liver: Hallmark MYC_TARGETS_V1 (NES +1.64, FDR 0.0045) and MYC_TARGETS_V2 (NES +1.56, FDR 0.0099) are enriched UP with exercise and E2F_TARGETS is NES +1.31 (FDR 0.068), whereas the abstract reports E2F1/c-Myc targets downregulated. In tumor tissue the paper's direction holds: E2F_TARGETS NES -2.85 and G2M_CHECKPOINT NES -3.12 (FDR ~0); MYC_TARGETS_V1 NES -1.09 (n.s.).", "Myc mRNA log2FC +0.89 in non-tumor (raw p 0.036, padj 0.41): not significant, consistent with 'transcriptionally unchanged' under padj but trending up."], "results": {"ex_EX_vs_NE_tis-NT": {"n_deg": 189, "up": 144, "down": 45, "rule": "padj < 0.05", "audit_n": 1599}, "ex_EX_vs_NE_tis-T": {"n_deg": 68, "up": 51, "down": 17, "rule": "padj < 0.05", "audit_n": 978}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"ex_EX_vs_NE_tis-NT": {"Per1": {"baseMean": 442.3225, "log2FoldChange": 1.085, "padj": 0.00504, "pvalue": 2.09e-05}, "Cry2": {"baseMean": 508.4345, "log2FoldChange": 0.3173, "padj": 0.0388, "pvalue": 0.000457}, "E2f1": {"baseMean": 112.1004, "log2FoldChange": 0.2028, "padj": 0.72, "pvalue": 0.187}, "Myc": {"baseMean": 131.6153, "log2FoldChange": 0.8888, "padj": 0.41, "pvalue": 0.0361}}, "ex_EX_vs_NE_tis-T": {"Per1": {"baseMean": 467.0244, "log2 ... [333 more characters]

reasoning: Abstract: Per1, Cry2 up with exercise; E2f1 and Myc mRNA unchanged; E2F1/c-Myc targets down.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 20 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "supplementary file content",
    "paper": "GEO data_processing: supplementary files include TPM values",
    "data": "per-sample files are featureCounts raw integer counts",
    "disposition": "executable_without_change"
  },
  {
    "item": "annotation version",
    "paper": "GEO data_processing: Gencode GRCm39 Release M32",
    "data": "featureCounts header uses gencode.vM27 GTF",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID39357875 / GSE273579

**The comparison with the paper rests on the abstract only.** No full text was available. I used the PubMed abstract (NCBI efetch, saved as `abstract_PMID39357875.txt`) and the GEO series summary and overall design. The paper's DE method, threshold and DEG counts are unknown.

## What ran
- `case_runner inspect GSE273579`, then `case_runner execute case_spec.json`. It ran twice: the second run only added study caveats, and the first run is in `_previous/`. The final run's status is `completed`, and the validator found 15 records with 0 errors.
- **Matrix:** `GSE273579_RAW.tar` holds per-sample featureCounts outputs (raw integer counts; library sizes 16–20 M). They were merged into 55,359 genes × 20 samples, and every sample aligned exactly to its GSM ID (20/20).
- **Design:** there are 5 groups of 4 male mice: ND non-exercise; HFD non-exercise non-tumor (NT); HFD non-exercise tumor (T); HFD exercise NT; HFD exercise T. Exercise was compared with non-exercise only within HFD/DMBA mice and within one tissue at a time (4 vs 4). No blocking was needed, because each mouse gives one sample per tissue. The ND samples are not used in any contrast, since ND has no exercise arm.
- **Method:** DESeq2 (pydeseq2 Wald), `~ ex`, fitted separately for NT and for T.
- **Threshold:** `workflow_default`, BH padj < 0.05 with no fold-change cutoff, because the abstract states no threshold. Raw p < 0.05 is reported as a labelled audit rule.
- **Enrichment:** ORA (Enrichr GO/KEGG) and Hallmark GSEA ran on both contrasts and completed.

## DEG counts vs the paper
| Contrast | Role | padj<0.05 (up/down) | audit raw p<0.05 | Paper |
|---|---|---|---|---|
| EX vs NE, non-tumor liver | primary | 189 (144/45) | 1599 | not stated in abstract |
| EX vs NE, tumor tissue | secondary | 68 (51/17) | 978 | not stated in abstract |

Genes the abstract names:
- **Per1** goes up in both tissues, as the paper says: NT log2FC 1.09, padj 0.005; T log2FC 1.18, padj 0.013.
- **Cry2** goes up in both tissues, as the paper says: NT log2FC 0.32, padj 0.039; T log2FC 0.60, padj 0.009.
- **E2f1** is unchanged in both tissues, as the paper says: padj 0.72 (NT) and 0.999 (T).
- **Myc** is not significant in either tissue (padj 0.41 / 0.85), which matches "transcriptionally unchanged". Its raw log2FC is +0.89 in NT, though (p 0.036).

Paper's "E2F1/c-Myc targets down" claim:
- **Tumor tissue agrees.** Hallmark E2F_TARGETS has NES −2.85 and G2M_CHECKPOINT has NES −3.12, ... [1502 more characters]
