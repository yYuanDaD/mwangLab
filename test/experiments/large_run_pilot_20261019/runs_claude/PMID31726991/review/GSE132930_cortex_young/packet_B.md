# Review packet B (the analysis' decisions): GSE132930_cortex_young

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C_young_Run_vs_Sed | 1252 | 971 | padj < 0.05 | 971 | 159 | 25 | 2293 | 4160 | 330 | 47 | 1802 | 0.053 | 0.279 |

## Samples per design level

### `grp`
- **Run** (5): GSM3896789 / 18289C; GSM3896790 / 18290C; GSM3896791 / 18526C; GSM3896792 / 18527C; GSM3896793 / 18528C
- **Sed** (5): GSM3896794 / 18605C; GSM3896795 / 18606C; GSM3896796 / 18626C; GSM3896797 / 18627C; GSM3896798 / 18681C

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE132930"], "primary_estimand": "Effect of 12 weeks voluntary wheel running vs age-matched sedentary on brain gene expression, analysed separately per tissue (cortex, hippocampus) and per age cohort (young 1-2 mo start; midlife 12 mo start, runners split into high/low by >10,000 rotations/night)", "planned_contrasts": ["cortex young Run vs Sed (S2.2.p1: 1252 DE; 742 up, 510 down)", "cortex midlife RunHi vs Sed (S2.2.p1: 214; 70 up, 144 down)", "cortex midlife RunLow vs Sed (S2.2.p1: 67; 20 up, 47 down)", "hippocampus young Run vs Sed (S2.2.p1: 2026; 1498 up, 528 down)", "hippocampus midlife RunHi vs Sed (S2.2.p1: 271; 87 up, 184 down)", "hippocampus midlife RunLow vs Sed (S2.2.p1: 172; 80 up, 92 down)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false, "source_locator": "S5.6.p1"}, "paper_method": "RSEM counts; edgeR 3.20.9, filter CPM>=1 in >1 sample, TMM, quasi-likelihood F-test, per tissue (S5.6.p1)", "factors": {"activity": ["Sed", "Run (young)", "RunLow", "RunHi (midlife)"], "tissue": ["Cortex", "Hippocampus"], "age": ["Young", "Midlife"]}, "inclusion": "male C57BL/6J; young n=5 per activity for RNA-seq (S5.2.p1); midlife n=12 run (6 high, 6 low) + 12 sed (S2.1.p1, S5.2.p1); young and midlife not directly compared (run at separate times, S5.6.p1)", "paper_results": "DEG counts per contrast in S2.2.p1 / Fig 3b,g; named genes S2.3.p1, S2.4.p2"}

reasoning: Methods S5.6.p1 define edgeR QL per tissue and three comparisons per tissue; S2.2.p1 gives counts at FDR<0.05 with no fold-change cutoff. Young and midlife were sequenced at separate times and the authors state they cannot be compared directly, so each tissue x age is its own model.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE132930\\GSE132930_GeneCount_C_young.txt.gz", "owned": true, "checks": ["DA.p1 names GSE132930", "matrix GSE132930_GeneCount_C_young.txt.gz is deposited in GSE132930 supplementary files; restricted to Young cortex samples listed in GEO metadata", "deposited edgeR result tables in the same series reproduce the paper's DEG counts exactly at FDR<0.05 (1252/214/67/2026/271/172), confirming the sample sets"], "accession": "GSE132930", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE132930\\GSE132930_metadata.csv"}

reasoning: Series and matrix belong to the paper; sample titles (mouse id + C/H) map to GSM records.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 10, "n_metadata": 65, "coverage": 0.1538, "unmatched_matrix_columns": ["17963C", "17964C", "17966C", "17967C", "17969C", "17970C", "17971C", "17972C", "17973C", "17974C", "17976C", "17977C", "17978C", "17979C", "17980C", "17981C", "17982C", "17985C", "17986C", "17987C", "17989C", "17990C", "17991C", "17992C", "17993C", "17995C", "17996C", "17997C", "17999C", "18000C", "18532C", "18533C", "18534C", "18535C", "18536C", "18602C", "18603C", "18624C", "18625C", "18673C", "18674C", "18675C", "18676C", "18677C", "18678C", "18679C", "18680C"], "unmatched_metadata_samples": ["GSM3896744", "GSM3896745", "GSM3896746", "GSM3896747", "GSM3896748", "GSM3896749", "GSM3896750", "GSM3896751", "GSM3896752", "GSM3896753", "GSM3896754", "GSM3896755", "GSM3896756", "GSM3896757", "GSM3896758", "GSM3896759", "GSM3896760", "GSM3896761", "GSM3896762", "GSM3896763", "GSM3896764", "GSM3896765", "GSM3896766", "GSM3896767", "GSM3896768", "GSM3896769", "GSM3896770", "GSM3896771", "GSM3896772", "GSM3896773", "GSM3896774", "GSM3896775", "GSM3896776", "GSM3896777", "GSM3896778", "GSM3896779", "GSM3896780", "GSM3896781", "GSM3896782", "GSM3896783", "GSM3896784", "GSM3896785", "GSM3896786", "GSM3896787", "GSM3896788", "GSM3896799", "GSM3896800", "GSM3896801", "GSM3896802", "GSM3896803", "GSM3896804", "GSM3896805", "GSM3896806", "GSM3896807", "GSM3896808"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID ... [426 more characters]

reasoning: Matrix columns embed the GEO title (mouse id + C/H) followed by GT library id, barcode and lane; matrix_column_pattern extracts the title, exact match on metadata 'title'. grp from the activity characteristic.

### matrix (valid, not_started)

final: {"source": "GSE132930_GeneCount_C_young.txt.gz", "paper_input": "RSEM v1.2.12 gene counts (S5.6.p1)", "matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_young\\aligned\\aligned_matrix.csv", "sha256": "51ed66b65c107a754a3621d6e3f18f235d84c1f471528cd95a9e5603b5b3ce8c", "n_features": 38924, "n_samples": 10, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1227221.0, "median": 2.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, min 0, max ~1.3e6, file named GeneCount; paper quantified with RSEM (S5.6.p1) and analysed them with edgeR, so these are RSEM-derived integer gene counts, the paper's own input.

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "Sed", "treatment": "Run", "contrasts": [{"name": "grp_Run_vs_Sed", "control": "Sed", "treatment": "Run", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_young\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Young cortex: Run vs Sed (S5.6.p1 comparison i).

rejected alternatives: [{"value": "pool young with midlife sedentary/run in one model", "reason_rejected": "paper S5.6.p1: cohorts run at separate times, not directly comparable"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 10, "n_columns": 2, "columns": ["Intercept", "grp_Sed"], "rank": 2, "full_rank": true, "residual_df": 8, "levels": {"grp": {"Run": 5, "Sed": 5}}, "cells": [{"cell": ["Run"], "n": 5}, {"cell": ["Sed"], "n": 5}], "min_cell_size": 5, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 10, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 10, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.brain region", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.age", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.activity", "n_levels": 2, "status": "complete_confounding", "crosstab": {"Run": {"Run": 5, "Sed": 0}, "Sed": {"Run": 0, "Sed": 5}}}, {"column": "molecule_ch1", " ... [1464 more characters]

reasoning: Independent animals, one sample per mouse per tissue; paper used ~group only (S5.6.p1). Young libraries spread over 8 lanes; no recorded batch to block on.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "edgeR (TMM + glmQLFit/glmQLFTest via inmoose)", "formula": "~ grp", "paper_route": {"method": "edgeR 3.20.9 QL F-test", "status": "reproduced"}, "deviations": ["inmoose edgepy port rather than R edgeR 3.20.9; TMM factors from repository implementation"]}

reasoning: Paper route (S5.6.p1): filter CPM>=1 in >=2 samples of each comparison, TMM, QL F-test, two-group fit per comparison (deposited tables contain only the two compared groups' samples).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}}

reasoning: S5.6.p1 / S2.2.p1: FDR < 0.05, no fold-change rule. Audit adds |FC|>1.5 for reference only.

### execution (valid, completed)

final: {"method": "run_edger_analysis", "subset": "C_young_Run_vs_Sed", "role": "primary", "tool": "tools.edger_tools:run_edger_analysis", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_young\\results\\C_young_Run_vs_Sed\\input\\matrix_filtered.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_young\\results\\C_young_Run_vs_Sed\\DEG_results_Run_vs_Sed.csv"], "counts": {"C_young_Run_vs_Sed": {"applied": {"rule": "padj < 0.05", "n_tested": 14936, "n_significant": 971, "n_up": 542, "n_down": 429, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14936, "n_significant": 159, "n_up": 136, "n_down": 23, "deg_sanity": "ok"}}}}

reasoning: paper's edgeR QL two-group comparison

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "C_young_Run_vs_Sed", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_young\\results\\enrichment_C_young_Run_vs_Sed\\ora\\DEG_results_Run_vs_Sed_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_young\\results\\enrichment_C_young_Run_vs_Sed\\ora\\DEG_results_Run_vs_Sed_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_young\\results\\enrichment_C_young_Run_vs_Sed\\ora\\DEG_results_Run_vs_Sed_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_young\\results\\enrichment_C_young_Run_vs_Sed\\ora\\DEG_results_Run_vs_Sed_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 949 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Extracellular Matrix Organization (GO:0030198) | padj=3.11e-03 | overlap=25/176 | genes=COL15 ... [1246 more characters]

reasoning: paper reports KEGG/GO ECM, focal adhesion, angiogenesis enrichment for young runners (S2.3, Fig 3d,e,i,j)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "C_young_Run_vs_Sed", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_young\\results\\enrichment_C_young_Run_vs_Sed\\gsea\\DEG_results_Run_vs_Sed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 14596 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 37 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.94 | NOM p=0.00e+00 | FDR q=1.72e-03 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.76 | NOM p=0.00e+00 | FDR q=8.86e-03 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.71 | NOM p=0.00e+00 | FDR q=9.86e-03 - HALLMARK_MITOTIC_SPINDLE | NES=1.62 | NOM p=0.00e+00 | FDR q=1.73e-02 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.58 | NOM p=3.95e-03 | FDR q=1.94e-02 - HALLMARK_NOTCH_SIGNALING | NES=1.48 | NOM p=2.97e-02 | FDR q=4.85e-02 - HALLMARK_KRAS_SIGNALING_DN | NES=1.44 | NOM p=2.36e-02 | FDR q=5.72e-02 - HALLMARK_ANGIOGENESIS | NES=1.41 | NOM p=7.66e-02 | FDR q=6.57e-02 - HALLMARK_COAGULATION | NES=1.33 | NOM p=7.13e-02 | FDR q=1.18e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-3.25 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=-3.16 | ... [405 more characters]

reasoning: paper reports KEGG/GO ECM, focal adhesion, angiogenesis enrichment for young runners (S2.3, Fig 3d,e,i,j)

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["young and midlife cohorts were sequenced separately; per paper S5.6.p1 they are not compared directly", "midlife high/low split is a post-hoc grouping by running distance (associational within runners)"], "results": {"C_young_Run_vs_Sed": {"n_deg": 971, "up": 542, "down": 429, "rule": "padj < 0.05", "audit_n": 159}}, "paper_counts": {"C_young_Run_vs_Sed": 1252}, "comparison": {"C_young_Run_vs_Sed": {"ours": 971, "paper": 1252}}, "paper_gene_check": {"C_young_Run_vs_Sed": {"Mmp14": {"log2FoldChange": 0.8094, "padj": 0.00187, "pvalue": 1.05e-06}, "Vegfa": {"log2FoldChange": 0.2727, "padj": 0.0746, "pvalue": 0.0081}, "Kdr": {"log2FoldChange": 0.5027, "padj": 0.0281, "pvalue": 0.000712}, "Flt1": {"log2FoldChange": 0.275, "padj": 0.0709, "pvalue": 0.00714}, "Dll4": {"log2FoldChange": 0.6763, "padj": 0.0771, "pvalue": 0.00871}, "Notch1": {"log2FoldChange": 0.373, "padj": 0.0271, "pvalue": 0.000629}}}}

reasoning: Counts from S2.2.p1; genes from S2.3.p1/S2.4.p2.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 10 samples.; per-sex analysis: no (one sex only) |
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
