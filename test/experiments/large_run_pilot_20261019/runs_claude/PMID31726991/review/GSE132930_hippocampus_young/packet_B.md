# Review packet B (the analysis' decisions): GSE132930_hippocampus_young

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H_young_Run_vs_Sed | 2026 | 1950 | padj < 0.05 | 1950 | 795 | 454 | 3052 | 4414 | 953 | 485 | 2310 | 0.047 | 0.292 |

## Samples per design level

### `grp`
- **Run** (5): GSM3896799 / 18289H; GSM3896800 / 18290H; GSM3896801 / 18526H; GSM3896802 / 18527H; GSM3896803 / 18528H
- **Sed** (4): GSM3896804 / 18605H; GSM3896806 / 18626H; GSM3896807 / 18627H; GSM3896808 / 18681H

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE132930"], "primary_estimand": "Effect of 12 weeks voluntary wheel running vs age-matched sedentary on brain gene expression, analysed separately per tissue (cortex, hippocampus) and per age cohort (young 1-2 mo start; midlife 12 mo start, runners split into high/low by >10,000 rotations/night)", "planned_contrasts": ["cortex young Run vs Sed (S2.2.p1: 1252 DE; 742 up, 510 down)", "cortex midlife RunHi vs Sed (S2.2.p1: 214; 70 up, 144 down)", "cortex midlife RunLow vs Sed (S2.2.p1: 67; 20 up, 47 down)", "hippocampus young Run vs Sed (S2.2.p1: 2026; 1498 up, 528 down)", "hippocampus midlife RunHi vs Sed (S2.2.p1: 271; 87 up, 184 down)", "hippocampus midlife RunLow vs Sed (S2.2.p1: 172; 80 up, 92 down)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false, "source_locator": "S5.6.p1"}, "paper_method": "RSEM counts; edgeR 3.20.9, filter CPM>=1 in >1 sample, TMM, quasi-likelihood F-test, per tissue (S5.6.p1)", "factors": {"activity": ["Sed", "Run (young)", "RunLow", "RunHi (midlife)"], "tissue": ["Cortex", "Hippocampus"], "age": ["Young", "Midlife"]}, "inclusion": "male C57BL/6J; young n=5 per activity for RNA-seq (S5.2.p1); midlife n=12 run (6 high, 6 low) + 12 sed (S2.1.p1, S5.2.p1); young and midlife not directly compared (run at separate times, S5.6.p1)", "paper_results": "DEG counts per contrast in S2.2.p1 / Fig 3b,g; named genes S2.3.p1, S2.4.p2"}

reasoning: Methods S5.6.p1 define edgeR QL per tissue and three comparisons per tissue; S2.2.p1 gives counts at FDR<0.05 with no fold-change cutoff. Young and midlife were sequenced at separate times and the authors state they cannot be compared directly, so each tissue x age is its own model.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE132930\\GSE132930_GeneCount_H_young.txt.gz", "owned": true, "checks": ["DA.p1 names GSE132930", "matrix GSE132930_GeneCount_H_young.txt.gz is deposited in GSE132930 supplementary files; restricted to Young hippocampus samples listed in GEO metadata", "deposited edgeR result tables in the same series reproduce the paper's DEG counts exactly at FDR<0.05 (1252/214/67/2026/271/172), confirming the sample sets"], "accession": "GSE132930", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE132930\\GSE132930_metadata.csv"}

reasoning: Series and matrix belong to the paper; sample titles (mouse id + C/H) map to GSM records.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 10, "n_metadata": 65, "coverage": 0.1538, "unmatched_matrix_columns": ["17964H", "17966H", "17967H", "17969H", "17970H", "17971H", "17972H", "17973H", "17974H", "17976H", "17977H", "17978H", "17979H", "17980H", "17981H", "17982H", "17985H", "17986H", "17987H", "17989H", "17990H", "17991H", "17992H", "17993H", "17995H", "17996H", "17997H", "17999H", "18000H", "18532H", "18533H", "18534H", "18535H", "18536H", "18602H", "18603H", "18624H", "18625H", "18673H", "18674H", "18675H", "18676H", "18677H", "18678H", "18679H", "18680H"], "unmatched_metadata_samples": ["GSM3896744", "GSM3896745", "GSM3896746", "GSM3896747", "GSM3896748", "GSM3896749", "GSM3896750", "GSM3896751", "GSM3896752", "GSM3896753", "GSM3896754", "GSM3896755", "GSM3896756", "GSM3896757", "GSM3896758", "GSM3896759", "GSM3896760", "GSM3896761", "GSM3896762", "GSM3896763", "GSM3896764", "GSM3896765", "GSM3896766", "GSM3896767", "GSM3896768", "GSM3896769", "GSM3896770", "GSM3896771", "GSM3896772", "GSM3896773", "GSM3896774", "GSM3896775", "GSM3896776", "GSM3896777", "GSM3896778", "GSM3896779", "GSM3896780", "GSM3896781", "GSM3896782", "GSM3896783", "GSM3896784", "GSM3896785", "GSM3896786", "GSM3896787", "GSM3896788", "GSM3896789", "GSM3896790", "GSM3896791", "GSM3896792", "GSM3896793", "GSM3896794", "GSM3896795", "GSM3896796", "GSM3896797", "GSM3896798"], "excluded_samples": {"GSM3896805": "18606H excluded: the authors' deposited hippocampus result is named 'wo18606' and its CPM c ... [625 more characters]

reasoning: Matrix columns embed the GEO title (mouse id + C/H) followed by GT library id, barcode and lane; matrix_column_pattern extracts the title, exact match on metadata 'title'. grp from the activity characteristic.

### matrix (valid, not_started)

final: {"source": "GSE132930_GeneCount_H_young.txt.gz", "paper_input": "RSEM v1.2.12 gene counts (S5.6.p1)", "matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_hippocampus_young\\aligned\\aligned_matrix.csv", "sha256": "474802f47a879c91d985732b2bd0a3e2302bac5bc7ce0784ba731d1a24c94042", "n_features": 38924, "n_samples": 9, "annotation_columns_dropped": ["GSM3896805"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 896016.0, "median": 2.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, min 0, max ~1.3e6, file named GeneCount; paper quantified with RSEM (S5.6.p1) and analysed them with edgeR, so these are RSEM-derived integer gene counts, the paper's own input.

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "Sed", "treatment": "Run", "contrasts": [{"name": "grp_Run_vs_Sed", "control": "Sed", "treatment": "Run", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_hippocampus_young\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Young hippocampus: Run vs Sed (S5.6.p1 comparison i).

rejected alternatives: [{"value": "pool young with midlife sedentary/run in one model", "reason_rejected": "paper S5.6.p1: cohorts run at separate times, not directly comparable"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 9, "n_columns": 2, "columns": ["Intercept", "grp_Sed"], "rank": 2, "full_rank": true, "residual_df": 7, "levels": {"grp": {"Run": 5, "Sed": 4}}, "cells": [{"cell": ["Run"], "n": 5}, {"cell": ["Sed"], "n": 4}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 9, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 9, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.brain region", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.age", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.activity", "n_levels": 2, "status": "complete_confounding", "crosstab": {"Run": {"Run": 5, "Sed": 0}, "Sed": {"Run": 0, "Sed": 4}}}, {"column": "molecule_ch1", "n_l ... [1460 more characters]

reasoning: Independent animals, one sample per mouse per tissue; paper used ~group only (S5.6.p1). Young libraries spread over 8 lanes; no recorded batch to block on.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "edgeR (TMM + glmQLFit/glmQLFTest via inmoose)", "formula": "~ grp", "paper_route": {"method": "edgeR 3.20.9 QL F-test", "status": "reproduced"}, "deviations": ["inmoose edgepy port rather than R edgeR 3.20.9; TMM factors from repository implementation"]}

reasoning: Paper route (S5.6.p1): filter CPM>=1 in >=2 samples of each comparison, TMM, QL F-test, two-group fit per comparison (deposited tables contain only the two compared groups' samples).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}}

reasoning: S5.6.p1 / S2.2.p1: FDR < 0.05, no fold-change rule. Audit adds |FC|>1.5 for reference only.

### execution (valid, completed)

final: {"method": "run_edger_analysis", "subset": "H_young_Run_vs_Sed", "role": "primary", "tool": "tools.edger_tools:run_edger_analysis", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_hippocampus_young\\results\\H_young_Run_vs_Sed\\input\\matrix_filtered.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_hippocampus_young\\results\\H_young_Run_vs_Sed\\DEG_results_Run_vs_Sed.csv"], "counts": {"H_young_Run_vs_Sed": {"applied": {"rule": "padj < 0.05", "n_tested": 15096, "n_significant": 1950, "n_up": 1396, "n_down": 554, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 15096, "n_significant": 795, "n_up": 774, "n_down": 21, "deg_sanity": "ok"}}}}

reasoning: paper's edgeR QL two-group comparison

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "H_young_Run_vs_Sed", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_hippocampus_young\\results\\enrichment_H_young_Run_vs_Sed\\ora\\DEG_results_Run_vs_Sed_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_hippocampus_young\\results\\enrichment_H_young_Run_vs_Sed\\ora\\DEG_results_Run_vs_Sed_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_hippocampus_young\\results\\enrichment_H_young_Run_vs_Sed\\ora\\DEG_results_Run_vs_Sed_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_hippocampus_young\\results\\enrichment_H_young_Run_vs_Sed\\ora\\DEG_results_Run_vs_Sed_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 1934 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cilium Movement (GO:0003341) | padj=4.21e-11 | overlap=29/59 | genes=CLX ... [1266 more characters]

reasoning: paper reports KEGG/GO ECM, focal adhesion, angiogenesis enrichment for young runners (S2.3, Fig 3d,e,i,j)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "H_young_Run_vs_Sed", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_hippocampus_young\\results\\enrichment_H_young_Run_vs_Sed\\gsea\\DEG_results_Run_vs_Sed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 14773 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 25 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.90 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.86 | NOM p=0.00e+00 | FDR q=4.41e-04 - HALLMARK_BILE_ACID_METABOLISM | NES=1.78 | NOM p=0.00e+00 | FDR q=3.17e-03 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.69 | NOM p=0.00e+00 | FDR q=7.64e-03 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.65 | NOM p=1.13e-03 | FDR q=1.02e-02 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.65 | NOM p=2.67e-03 | FDR q=9.14e-03 - HALLMARK_APICAL_JUNCTION | NES=1.60 | NOM p=2.24e-03 | FDR q=1.50e-02 - HALLMARK_ADIPOGENESIS | NES=1.58 | NOM p=0.00e+00 | FDR q=1.63e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-2.30 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=-1.87  ... [410 more characters]

reasoning: paper reports KEGG/GO ECM, focal adhesion, angiogenesis enrichment for young runners (S2.3, Fig 3d,e,i,j)

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["young and midlife cohorts were sequenced separately; per paper S5.6.p1 they are not compared directly", "midlife high/low split is a post-hoc grouping by running distance (associational within runners)"], "results": {"H_young_Run_vs_Sed": {"n_deg": 1950, "up": 1396, "down": 554, "rule": "padj < 0.05", "audit_n": 795}}, "paper_counts": {"H_young_Run_vs_Sed": 2026}, "comparison": {"H_young_Run_vs_Sed": {"ours": 1950, "paper": 2026}}, "paper_gene_check": {}}

reasoning: Counts from S2.2.p1; genes from S2.3.p1/S2.4.p2.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "running duration",
    "paper": "12 weeks (S2.1.p1, S5.2.p1)",
    "data": "young deposited result file named 'Early_Diet ... 8wkrun ... CD.8weeks'",
    "disposition": "executable_without_change"
  },
  {
    "item": "young matrix scope",
    "paper": "n=5 per activity",
    "data": "young GeneCount matrices hold 56-57 libraries of a larger 'Early_Diet' experiment; only the 10 GEO-registered samples per tissue are used",
    "disposition": "executable_without_change"
  },
  {
    "item": "hippocampus young sample 18606H",
    "paper": "n=5 per activity, no exclusion stated (S5.2.p1)",
    "data": "deposited result file 'hippo_8wkrun_wo18606' omits 18606H (Sed)",
    "disposition": "executable_with_declared_exclusion"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID31726991 / GSE132930

Paper: Foley et al. 2019, BMC Genomics (PMC6854620): "Transcriptional profiling predicts running promotes cerebrovascular remodeling in young but not midlife mice". Run label PMID31726991.

## What ran
One spec (`case_spec.json`, built by a small generator script that lived only in the session scratchpad) ran through `python -m tools.case_runner execute`. The run completed and the validator passed on 60 records with 0 errors. It has five cases. Each tissue × age pair has its own matrix and model, because the paper says the young and midlife cohorts were sequenced at separate times (S5.6.p1).

| Case | Matrix | Samples | Executions |
|---|---|---|---|
| cortex_young | GeneCount_C_young | 5 Run, 5 Sed | edgeR QL Run vs Sed (primary) + ORA/GSEA |
| hippocampus_young | GeneCount_H_young | 5 Run, 4 Sed (18606H excluded) | edgeR QL Run vs Sed (primary) + ORA/GSEA |
| hippocampus_young_all10 | GeneCount_H_young | 5 Run, 5 Sed | edgeR QL (sensitivity, exploratory) |
| cortex_midlife | GeneCount_C_midlife | 6 RunHi, 6 RunLow, 10 Sed | edgeR QL RunHi vs Sed and RunLow vs Sed (primary, pairwise subsets); DESeq2 `~ pool + grp` (sensitivity) |
| hippocampus_midlife | GeneCount_H_midlife | 5 RunHi, 6 RunLow, 12 Sed | same as cortex_midlife |

- **Alignment:** matrix columns were matched exactly on the GEO `title` field (regex `^(?:16NGS-002-Howell_)?(\d+[CH])_`). The young matrices hold 56–57 libraries from a larger "Early_Diet" experiment. Only the 10 samples registered for this series were used in each tissue.
- **Matrix:** RSEM integer gene counts (integer fraction 1.0, as stated in S5.6.p1). These are the paper's own input.
- **Method:** the paper route as written in S5.6.p1. Genes were kept if CPM ≥ 1 in at least 2 samples of each comparison, then TMM normalisation and a quasi-likelihood F-test, using the inmoose edgeR port.
- **Threshold:** the paper's rule, FDR < 0.05 with no fold-change cutoff (S5.6.p1, S2.2.p1), source `paper`. The audit rule adds |log2FC| > 0.585 and is for reference only.

## DEG counts vs paper (FDR < 0.05, no FC cutoff)
| Contrast | Ours (up/down) | Paper (up/down) | Overlap with authors' deposited table |
|---|---|---|---|
| Cortex young Run vs Sed | 971 (542/429) | 1252 (742/510) | 920 of 1252 |
| Hippocampus young Run vs Sed | 1950 (1396/554) | 2026 (1498/528) | 1752 of 2026 |
| Cortex midlife RunHi vs Sed | 0 | 214 (70/144) | 0 |
| Cortex midlife RunLow vs Sed | 0 | 67 (20/47) | 0 |
| Hippocampus m ... [4266 more characters]
