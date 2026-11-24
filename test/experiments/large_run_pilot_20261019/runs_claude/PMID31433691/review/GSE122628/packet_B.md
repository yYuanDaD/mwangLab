# Review packet B (the analysis' decisions): GSE122628

## Mechanical flags

- none

## Samples per design level

### `grp`
- **SHAM** (3): GSM3476633 / Unstim 1 [U1] / U1_TCCGGAGA-ATAGAGGC_L002,WT, not exerci; GSM3476634 / Unstim 2 [U2] / U2_CGCTCATT-ATAGAGGC_L002,WT, not exerci; GSM3476635 / Unstim 3 [U3] / U3_GAGATTCC-ATAGAGGC_L002,WT, not exerci
- **STIM** (3): GSM3476630 / Stim 1 [S1] / S1_ATTCAGAA-ATAGAGGC_L002,WT, exercised,; GSM3476631 / Stim 2 [S2] / S2_GAATTCGT-ATAGAGGC_L002,WT, exercised,; GSM3476632 / Stim 3 [S3] / S3_CTGAAGCT-ATAGAGGC_L002,WT, exercised,

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE122628"], "assay": "bulk RNA-seq (SMARTer Stranded Total RNA-seq Pico v2, HiSeq 4000 SE101) of FACS-sorted CD146+CD45-CD31- pericytes from gastrocnemius-soleus", "sample_inclusion": "6 male C57BL/6J WT mice, 14 wk; 3 e-stim, 3 sham (GEO overall_design)", "factors": {"treatment": ["sham (U)", "acute e-stim (S)"]}, "primary_estimand": "Effect of a single 10-min bout of electrically stimulated (eccentric) muscle contraction vs sham on the transcriptome of CD146+Lin- pericytes, 3 h post-contraction", "planned_contrasts": ["e-stim vs sham, CD146+Lin- pericytes, 3 h (abstract; GEO overall_design); paper DEG count not available from abstract"], "repeated_measure_unit": "none (one sample per mouse, independent groups)", "normalization": "Salmon -> tximport lengthScaledTPM gene counts (GEO data_processing)", "paper_method": "edgeR quasi-likelihood (GEO data_processing: counts analyzed directly using the edgeR-quasi method)", "paper_threshold": {"metric": "FDR", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "not stated in abstract or GEO; full text unavailable"}, "paper_results": "Abstract: upregulation of genes related to immunomodulation and extracellular matrix remodeling in CD146+Lin- pericytes after contraction; no counts or gene names given"}

reasoning: Only the PubMed abstract (PMID 31433691) and the GEO series/sample records are available; no full text. The abstract states RNA-seq of CD146+Lin- pericytes 3 h after a single e-stim session vs sham; GEO overall_design confirms n=3/group male mice, and data_processing names the edgeR-quasi method. No threshold or DEG count is recoverable.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\input\\matrix_feature_ids.csv", "owned": true, "checks": ["GEO Series_pubmed_id = 31433691", "6 GSMs (GSM3476630-35) match 6 matrix columns S1-S3, U1-U3", "cell type CD146+CD45-CD31- pericytes matches abstract"], "accession": "GSE122628", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE122628\\GSE122628_metadata.csv"}

reasoning: Series links PMID 31433691; supplementary gene-count file belongs to this series and its columns map one-to-one to the series samples.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "source_name_ch1", "regex": "\\((S|U)\\)$", "recode": {"S": "STIM", "U": "SHAM"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\aligned\\design_metadata.csv", "sha256": "dbcc72ba84b2a17d357ae6e8f0e7ba13af8e8b72bbe863cabcf6347e34ab0206", "levels": {"grp": {"STIM": 3, "SHAM": 3}}}}

reasoning: Matrix columns S1..U3 are the bracketed codes in GEO titles (Stim 1 [S1]); group from source_name_ch1 (S)/(U), consistent with treatment Exercised/Not Exercised.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\aligned\\aligned_matrix.csv", "sha256": "94378637a7815209ef348e37115f1b0fb6d350abbcb2bfb4c541e72b182df42e", "n_features": 53595, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1907473.20868477, "median": 8.717253000598106, "integer_fraction": 0.2532, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Only 25% of values are integers, max 1.9e6, median 8.7; GEO data_processing: Salmon quasi-mapping + tximport lengthScaledTPM summed to gene level -> estimated (length-scaled) counts on the count scale, not TPM. Paper input is the same file, analyzed with edgeR-quasi.

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "SHAM", "treatment": "STIM", "contrasts": [{"name": "grp_STIM_vs_SHAM", "control": "SHAM", "treatment": "STIM", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Single factor, two independent arms (3 vs 3); e-stim induced contraction is the paper's exercise model. Treatment column (Exercised/Not Exercised) is identical to source_name grouping.

rejected alternatives: [{"value": "characteristics_ch1.4.treatment", "reason_rejected": "identical partition to source_name_ch1; used one column"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 6, "n_columns": 2, "columns": ["Intercept", "grp_STIM"], "rank": 2, "full_rank": true, "residual_df": 4, "levels": {"grp": {"STIM": 3, "SHAM": 3}}, "cells": [{"cell": ["SHAM"], "n": 3}, {"cell": ["STIM"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 6, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 6, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 2, "status": "complete_confounding", "crosstab": {"SHAM": {"acute electrical stimulation (S)": 0, "unstimulated sham control (U)": 3}, "STIM": {"acute electrical stimulation (S)": 3, "unstimulated sham control (U)": 0}}}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain background", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.genotype/variation", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.age", "n_levels": 1, "st ... [2277 more characters]

reasoning: Independent mice, all male, same age/strain, one sequencing lane (L002 for all in description); no batch or pairing recorded.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "edgeR (quasi-likelihood F-test, TMM) on rounded tximport lengthScaledTPM counts", "formula": "~ grp", "rounding_documented": true, "paper_route": {"method": "edgeR-quasi on non-integer lengthScaledTPM counts", "status": "approximated", "reason": "repository edgeR executor (inmoose) enforces integer input; counts are rounded to nearest integer, which edgeR in R would accept unrounded; effect is negligible except for very low counts"}, "deviations": ["counts rounded to integers before edgeR", "paper's low-expression filter unknown (abstract only); executor defaults used"], "transform": "round"}

reasoning: Reproduce the paper's stated edgeR-quasi route. Rounding of tximport lengthScaledTPM counts is the standard documented recipe for count-based tools on tximport output.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": null, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Paper threshold not recoverable from the abstract; workflow default BH-FDR < 0.05, no fold-change cutoff. Raw p < 0.05 recorded as an audit count only."}

reasoning: No full text; abstract and GEO give no cutoff.

### execution (valid, completed)

final: {"method": "run_edger_analysis", "subset": "grp_STIM_vs_SHAM", "role": "primary", "tool": "tools.edger_tools:run_edger_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\transformed\\rounded_counts.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\results\\grp_STIM_vs_SHAM\\DEG_results_STIM_vs_SHAM.csv"], "counts": {"grp_STIM_vs_SHAM": {"applied": {"rule": "padj < 0.05", "n_tested": 48759, "n_significant": 122, "n_up": 53, "n_down": 69, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 48759, "n_significant": 2996, "n_up": 1340, "n_down": 1656, "deg_sanity": "ok"}}}}

reasoning: paper's edgeR-quasi two-group test

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_STIM_vs_SHAM_deseq2", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\transformed\\rounded_counts.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\results\\grp_STIM_vs_SHAM_deseq2\\DEG_results_STIM_vs_SHAM.csv"], "counts": {"grp_STIM_vs_SHAM_deseq2": {"applied": {"rule": "padj < 0.05", "n_tested": 20359, "n_significant": 206, "n_up": 67, "n_down": 139, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 48707, "n_significant": 2118, "n_up": 836, "n_down": 1282, "deg_sanity": "ok"}}}}

reasoning: second NB method on the same rounded counts to gauge method sensitivity at n=3

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_STIM_vs_SHAM", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\results\\enrichment_grp_STIM_vs_SHAM\\ora\\DEG_results_STIM_vs_SHAM_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\results\\enrichment_grp_STIM_vs_SHAM\\ora\\DEG_results_STIM_vs_SHAM_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\results\\enrichment_grp_STIM_vs_SHAM\\ora\\DEG_results_STIM_vs_SHAM_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\results\\enrichment_grp_STIM_vs_SHAM\\ora\\DEG_results_STIM_vs_SHAM_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 122 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Leukocyte Aggregation (GO:0070486) | padj=4.03e-03 | overlap=3/7 | genes=IL1B;S100A9;S100A8 - Regulation Of Lipid Catabolic Process (GO:0050994) | p ... [1191 more characters]

reasoning: abstract reports immunomodulation and ECM remodelling gene programs

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_STIM_vs_SHAM", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31433691\\GSE122628\\results\\enrichment_grp_STIM_vs_SHAM\\gsea\\DEG_results_STIM_vs_SHAM_GSEA_Hallmark.csv"], "summary": "GSEA complete on 48759 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 44 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=2.45 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=2.38 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.08 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=2.03 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=1.99 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.97 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=1.89 | NOM p=0.00e+00 | FDR q=1.06e-04 - HALLMARK_MTORC1_SIGNALING | NES=1.63 | NOM p=0.00e+00 | FDR q=4.53e-03 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.56 | NOM p=2.47e-03 | FDR q=7.98e-03 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.55 | NOM p=2.43e-03 | FDR q=8.00e-03 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_UV_RESPONSE_DN | NES=-2.30 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=-2.22 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELI ... [389 more characters]

reasoning: abstract reports immunomodulation and ECM remodelling gene programs

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Comparison with the paper rests on the abstract only (no DEG count or gene list available)", "n=3 per group", "counts rounded for the integer-only edgeR executor", "threshold is the workflow default, not the paper's", "Immunomodulation direction agrees with the abstract (GSEA Hallmark inflammatory response, IL6-JAK-STAT3, TNFa-NFkB, allograft rejection positive; S100a8/S100a9, Il1rn, Cxcl3, Ptx3 up), but Hallmark EPITHELIAL_MESENCHYMAL_TRANSITION (ECM-rich set, NES -2.18) and ANGIOGENESIS (NES -2.15) are NEGATIVELY enriched, which does not support the abstract's ECM-remodelling up-regulation at the Hallmark level; the paper's specific ECM genes are unknown (abstract only)"], "results": {"grp_STIM_vs_SHAM": {"n_deg": 122, "up": 53, "down": 69, "rule": "padj < 0.05", "audit_n": 2996}, "grp_STIM_vs_SHAM_deseq2": {"n_deg": 206, "up": 67, "down": 139, "rule": "padj < 0.05", "audit_n": 2118}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {}}

reasoning: Paper's stated method on the paper's deposited input; the abstract reports only a direction (up-regulation of immunomodulatory and ECM-remodelling genes).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "edgeR input",
    "paper": "non-integer lengthScaledTPM counts into edgeR-quasi",
    "data": "executor requires integers",
    "disposition": "executable_with_declared_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID31433691 / GSE122628

**The comparison with the paper rests on the abstract only.** No full text was available. The sources were the PubMed abstract (efetch, saved as `abstract_PMID31433691.txt`) and the GEO series and sample records. The abstract gives no DEG count, no named genes and no threshold.

## What ran
- Study: CD146+CD45-CD31- pericytes FACS-sorted from mouse gastrocnemius-soleus, 3 h after one 10-min bout of electrically stimulated contraction (STIM, n=3) vs sham (SHAM, n=3). All mice were male C57BL/6J, 14 wk old.
- Route: case spec (`case_spec.json`) run by `tools.case_runner execute`. The validator reported 13 records and 0 errors.
- Matrix: `GSE122628_Boppart_GeneCounts_GEO.txt.gz`. These are Salmon + tximport lengthScaledTPM gene counts, so they are estimated counts: only 25% of values are integers. Features were collapsed to `external_gene_name`, summing 120 repeated symbols, which left 53,595 genes.
- Primary analysis: edgeR quasi-likelihood F-test with TMM, `~ grp`, on rounded counts. This is the method GEO `data_processing` names ("edgeR-quasi").
- Sensitivity analysis: DESeq2 Wald test on the same rounded counts.
- Enrichment: ORA (GO BP/MF/CC, KEGG) and Hallmark GSEA on the primary table. Both completed.

## DEG counts vs paper
Threshold: workflow default of BH-FDR < 0.05 with no fold-change cutoff. The paper's threshold is not recoverable from the abstract.

| Table | DEGs (up/down) | raw p<0.05 (audit only) | Paper |
|---|---|---|---|
| edgeR QL (primary) | 122 (53/69) | 2996 | not reported in abstract |
| DESeq2 (sensitivity) | 206 (67/139) | 2118 | – |

Direction compared with the abstract:
- **Immunomodulation agrees with the abstract.** Up genes include S100a8, S100a9, Il1rn, Cxcl3, Ptx3, Clec4d, Serpinb2 and Mt2. GSEA is positive for inflammatory response, IL6-JAK-STAT3, TNFa-NFkB and allograft rejection.
- **ECM remodelling is not supported at the Hallmark level.** EMT (NES -2.18), angiogenesis (NES -2.15) and coagulation are negatively enriched. This is recorded in the study caveats. The paper's specific ECM genes are unknown.

## Deviations
1. **Rounded counts.** The counts were rounded to integers because the repository's edgeR executor needs integer input. The paper fed non-integer lengthScaledTPM counts to edgeR in R. This is declared in the method gate (`paper_route.status: approximated`).
2. **No low-expression filter.** The paper's filter (probably `filterByExpr`) is unknown, so none was applied; the  ... [1549 more characters]
