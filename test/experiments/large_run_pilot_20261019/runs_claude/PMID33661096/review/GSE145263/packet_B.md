# Review packet B (the analysis' decisions): GSE145263

## Mechanical flags

- none

## Samples per design level

### `grp`
- **EXE** (3): GSM4310331 / EXE1; GSM4310332 / EXE2; GSM4310333 / EXE3
- **SED** (3): GSM4310328 / SED1; GSM4310329 / SED2; GSM4310330 / SED3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE145263"], "assay": "bulk RNA-seq (SMARTer Stranded Total RNA-Seq Pico v2) of FACS-sorted cardiac endothelial cells (CD31+CD140a-CD45-Ter119-DAPI-), NextSeq 550 single-end", "primary_estimand": "Effect of 6-week progressive treadmill exercise training vs sedentary on the cardiac endothelial-cell transcriptome in young adult (10-week-old at start) male C57BL/6J mice", "planned_contrasts": ["EXE vs SED (S2.1.p1, FIG2A; DEG count shown only in the MA-plot image, not in text)"], "other_experiments_in_series": "Aged vs Young, HFD vs Chow, TAC 2wk vs Sham, TAC 7wk vs Sham (each with its own control; not exercise; out of scope)", "sample_inclusion": "SED1-3 (n=3) and EXE1-3 (n=3) male mice; FIG2 legend N=3-4 male mice/group", "factors": {"group": ["SED (reference)", "EXE"]}, "repeated_measure_unit": "none (independent animals, one EC sample per mouse)", "normalization": "DESeq2 size factors on HTSeq raw counts (S4.15.p1)", "paper_method": "DESeq2 (Chipster v3.12.2) two-group, ~ group, Wald test, BH FDR (S4.15.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": true, "source_locator": "S4.15.p1; FIG2 legend"}, "paper_results": "Exercise affected fewer genes than the risk factors (S2.1.p2, S3.p2). Serpinh1, Vwa1, Mest and Fhl3 significantly DOWN-regulated by exercise (S2.3.p1, FIG4A-C). PANTHER ORA of up/down genes (S2.2.p1, S4.16.p1)."}

reasoning: S2.1.p1 defines exercise training (6 wk treadmill) vs sedentary as one of five experiments; S4.2.p1: 10-wk-old male mice used for RNA-seq; S4.15.p1: HTSeq counts -> DESeq2 Wald + BH, FDR <= 0.05; FIG2 legend: FDR (BH) threshold 0.05, n=3-4/group. No fold-change cutoff is stated. The exercise DEG count appears only inside the FIG2A image, which is not in the text, so no numeric paper count is available.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["S4.15.p1 and S11.p1 name GSE145263", "GEO titles SED1-3/EXE1-3 with treatment Sedentary/Exercise training match the paper's groups", "data_processing: HISAT2 GRCm38.90 + HTSeq-count, as in S4.15.p1", "metadata gender Male matches S4.1.p1"], "accession": "GSE145263", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE145263\\GSE145263_metadata.csv"}

reasoning: Series is the paper's own deposit (S11.p1, S11.p3; same authors Kivela and Hemanthakumar). Per-sample HTSeq count files in GSE145263_RAW.tar are the only matrix.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 31, "n_metadata": 31, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM4310334": "separate experiment (YOUNG: Young (2 months old)); the paper analyses each model only against its own control (S2.1.p1, FIG2 A-E); not part of the exercise-vs-sedentary estimand", "GSM4310335": "separate experiment (YOUNG: Young (2 months old)); the paper analyses each model only against its own control (S2.1.p1, FIG2 A-E); not part of the exercise-vs-sedentary estimand", "GSM4310336": "separate experiment (YOUNG: Young (2 months old)); the paper analyses each model only against its own control (S2.1.p1, FIG2 A-E); not part of the exercise-vs-sedentary estimand", "GSM4310337": "separate experiment (AGED: Aged (18 months old)); the paper analyses each model only against its own control (S2.1.p1, FIG2 A-E); not part of the exercise-vs-sedentary estimand", "GSM4310338": "separate experiment (AGED: Aged (18 months old)); the paper analyses each model only against its own control (S2.1.p1, FIG2 A-E); not part of the exercise-vs-sedentary estimand", "GSM4310339": "separate experiment (AGED: Aged (18 months old)); the paper analyses each model only against its own control (S2.1.p1, FIG2 A-E); not part of the exercise-vs-sedentary estimand", "GSM4310340": "separate experiment (CHOW: Standard chow diet); the paper analyses each model only against its own control (S2.1.p1, FIG2 A-E); not part of the  ... [4495 more characters]

reasoning: Tar-merged columns are GSM ids that equal the metadata index exactly (31/31). Group column 'grp' is derived by recoding the GEO treatment characteristic. The 25 samples of the aging/HFD/TAC experiments are excluded because the paper compares each intervention only with its own control; using them would change the estimand.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\aligned\\aligned_matrix.csv", "sha256": "ca60cc93c8af4fd2d8551cbeac05ecb5aab76139c31238080beae204db9b9c6a", "n_features": 52636, "n_samples": 6, "annotation_columns_dropped": ["GSM4310334", "GSM4310335", "GSM4310336", "GSM4310337", "GSM4310338", "GSM4310339", "GSM4310340", "GSM4310341", "GSM4310342", "GSM4310343", "GSM4310344", "GSM4310345", "GSM4310346", "GSM4310347", "GSM4310348", "GSM4310349", "GSM4310350", "GSM4310351", "GSM4310352", "GSM4310353", "GSM4310354", "GSM4767053", "GSM4767056", "GSM4767058", "GSM4767061"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 5418076.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values are integers (integer_fraction 1.0, max 5.4M, many zeros); GEO data_processing and S4.15.p1 state HTSeq-count read counts per gene; paper used these raw counts as DESeq2 input. No HTSeq '__' summary rows remain in the merged matrix.

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "SED", "treatment": "EXE", "contrasts": [{"name": "grp_EXE_vs_SED", "control": "SED", "treatment": "EXE", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Independent-group comparison of trained vs sedentary male mice, n=3 vs 3, exactly as FIG2A. Causal estimand (randomised intervention vs sedentary control).

rejected alternatives: [{"value": "one model over all 31 samples with every group as a level", "reason_rejected": "paper fits each experiment separately against its own control (S2.1.p1, FIG2A-E); pooling unrelated experiments changes the dispersion estimates and the estimand"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 6, "n_columns": 2, "columns": ["Intercept", "grp_SED"], "rank": 2, "full_rank": true, "residual_df": 4, "levels": {"grp": {"SED": 3, "EXE": 3}}, "cells": [{"cell": ["EXE"], "n": 3}, {"cell": ["SED"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "submission_date", "n_levels": 1, "status": "constant"}]}

reasoning: One sample per animal, no pairing or batch variable recorded for the SED/EXE samples (all submitted Feb 13 2020; the Sep 2020 additions belong to other experiments and are excluded). All male. No covariate is added.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald, BH)", "formula": "~ grp", "paper_route": {"method": "DESeq2 ~ group (Chipster v3.12.2, R DESeq2)", "status": "reproduced"}, "deviations": ["pydeseq2 implementation instead of R DESeq2 in Chipster; same model (NB GLM, empirical-Bayes dispersion shrinkage, Wald test, BH). Small numerical differences expected, especially from independent filtering and outlier handling."]}

reasoning: Raw counts support DESeq2, the paper's method (S4.15.p1).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": true, "source_locator": "S4.15.p1; FIG2 legend"}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": true}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}}

reasoning: S4.15.p1: FDR (p adj.) <= 0.05; FIG2 legend: BH-adjusted p threshold 0.05; no fold-change rule. Audit adds |log2FC| > 1 for reference only.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_EXE_vs_SED", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\aligned\\aligned_matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\results\\grp_EXE_vs_SED\\DEG_results_EXE_vs_SED.csv"], "counts": {"grp_EXE_vs_SED": {"applied": {"rule": "padj <= 0.05", "n_tested": 13154, "n_significant": 139, "n_up": 48, "n_down": 91, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 13154, "n_significant": 28, "n_up": 4, "n_down": 24, "deg_sanity": "ok"}}}}

reasoning: paper's two-group DESeq2 Wald test, EXE vs SED (S4.15.p1, FIG2A)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_EXE_vs_SED", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": true}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\results\\enrichment_grp_EXE_vs_SED\\ora_up\\DEG_results_EXE_vs_SED_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\results\\enrichment_grp_EXE_vs_SED\\ora_up\\DEG_results_EXE_vs_SED_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\results\\enrichment_grp_EXE_vs_SED\\ora_up\\DEG_results_EXE_vs_SED_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\results\\enrichment_grp_EXE_vs_SED\\ora_up\\DEG_results_EXE_vs_SED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 48 Mouse genes (direction=up, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - RNA Splicing, Via Transesterification Reactions With Bulged Adenosine As Nucleophile (GO:0000377) | padj=1.27e-01 | overlap=4/180 | genes=SNRNP70;TRA2A;PRPF4 ... [1184 more characters]

reasoning: paper runs over-representation analysis on up-regulated DEGs (S2.2.p1, S4.16.p1; PANTHER, here Enrichr GO/KEGG)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_EXE_vs_SED", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": true}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\results\\enrichment_grp_EXE_vs_SED\\ora_down\\DEG_results_EXE_vs_SED_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\results\\enrichment_grp_EXE_vs_SED\\ora_down\\DEG_results_EXE_vs_SED_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\results\\enrichment_grp_EXE_vs_SED\\ora_down\\DEG_results_EXE_vs_SED_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\results\\enrichment_grp_EXE_vs_SED\\ora_down\\DEG_results_EXE_vs_SED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 84 Mouse genes (direction=down, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Extracellular Structure Organization (GO:0043062) | padj=2.21e-02 | overlap=5/109 | genes=ADAMTS4;COL15A1;COL4A2;COL4A1;PXDN - Extracellular Matr ... [1194 more characters]

reasoning: paper runs over-representation analysis on down-regulated DEGs (S2.2.p1, S4.16.p1)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_EXE_vs_SED", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33661096\\GSE145263\\results\\enrichment_grp_EXE_vs_SED\\gsea\\DEG_results_EXE_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 27719 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 44 significant at FDR q < 0.25. ### Top 5 UP (NES > 0, enriched in treatment): - HALLMARK_UV_RESPONSE_DN | NES=1.40 | NOM p=1.68e-02 | FDR q=1.18e-01 - HALLMARK_PROTEIN_SECRETION | NES=1.19 | NOM p=1.47e-01 | FDR q=3.22e-01 - HALLMARK_ANGIOGENESIS | NES=1.12 | NOM p=2.69e-01 | FDR q=3.61e-01 - HALLMARK_APICAL_SURFACE | NES=0.98 | NOM p=4.90e-01 | FDR q=6.42e-01 - HALLMARK_PANCREAS_BETA_CELLS | NES=0.81 | NOM p=7.79e-01 | FDR q=8.94e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-2.52 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.37 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=-2.37 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=-2.27 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-2.27 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=-2.15 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=-2.11 | NOM p=0.00e+00 | FDR ... [393 more characters]

reasoning: exploratory Hallmark GSEA on the full Wald-stat ranking (paper discusses TGF-beta/IFN/TNF pathways)

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper's exercise DEG count is only in the FIG2A image and could not be read; no numeric count comparison.", "n=3 per group; results are sensitive to single animals."], "results": {"grp_EXE_vs_SED": {"n_deg": 139, "up": 48, "down": 91, "rule": "padj <= 0.05", "audit_n": 28}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"grp_EXE_vs_SED": {"Serpinh1": {"baseMean": 12605.181, "log2FoldChange": -0.5003, "padj": 0.0416, "pvalue": 0.000381}, "Vwa1": {"baseMean": 4105.5847, "log2FoldChange": -0.595, "padj": 0.00448, "pvalue": 1.36e-05}, "Mest": {"baseMean": 1192.2842, "log2FoldChange": -0.4293, "padj": 0.0405, "pvalue": 0.000362}, "Fhl3": {"baseMean": 178.7594, "log2FoldChange": -1.0092, "padj": 0.00988, "pvalue": 3.38e-05}}}}

reasoning: Paper-aligned two-group DESeq2; named genes from S2.3.p1/FIG4 (all down in EXE) are checked.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "series content",
    "paper": "five experiments, exercise is one",
    "data": "31 samples across 9 groups",
    "disposition": "executable_without_change (other experiments excluded)"
  },
  {
    "item": "paper DEG count",
    "paper": "shown in FIG2A MA-plot image only",
    "data": "not available in text",
    "disposition": "not_comparable"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 33661096 / GSE145263

**Status: finished** (case-spec route, `python -m tools.case_runner execute case_spec.json`; validator: 13 records, 0 errors).

## What ran
- Paper (PMC8043751): five separate mouse cardiac-EC RNA-seq experiments, each compared with its own control. The exercise experiment is 6-week progressive treadmill training (EXE) vs sedentary (SED) in male C57BL/6J mice, n=3 vs 3 (S2.1.p1, S4.2.p1, FIG2A). Method: HTSeq counts with a two-group DESeq2 Wald test and BH correction (Chipster v3.12.2), FDR <= 0.05 and no fold-change cutoff (S4.15.p1, FIG2 legend).
- Data: `GSE145263_RAW.tar` was merged into 52,636 Ensembl genes x 31 samples of integer HTSeq counts. Samples aligned exactly on GSM id (31/31). `grp` was recoded from `characteristics_ch1.2.treatment`. The 25 samples from the aging, HFD and TAC experiments were excluded because the paper analyses each experiment only against its own control.
- Suitability: analyzable. The sex check passed (all male, as in the metadata).
- Model: DESeq2 (pydeseq2) `~ grp`, EXE vs SED, alpha 0.05, no covariates. Animals are independent and no batch is recorded.
- Enrichment: Enrichr ORA (GO BP/MF/CC + KEGG) on the up-regulated and down-regulated DEG sets, standing in for the paper's PANTHER, plus exploratory Hallmark GSEA ranked by the Wald stat.

## DEG counts vs paper (paper threshold: BH FDR <= 0.05, no |log2FC| cutoff)
| Contrast | Ours | Paper |
|---|---|---|
| EXE vs SED | 139 (48 up / 91 down) | not readable: the count is only inside the FIG2A MA-plot image, not in the text |

- Audit rule (padj < 0.05 and |log2FC| > 1): 28 DEGs.
- Named genes (S2.3.p1, FIG4A-C: all down with exercise) are all reproduced as significantly down:

| Gene | log2FC | padj |
|---|---|---|
| Serpinh1 | -0.50 | 0.042 |
| Vwa1 | -0.60 | 0.0045 |
| Mest | -0.43 | 0.041 |
| Fhl3 | -1.01 | 0.0099 |

- Consistent with the paper's statement that exercise affected fewer genes than the risk factors (S2.1.p2, S3.p2).
- ORA:
  - Down-regulated genes: 6 GO BP terms at adj p < 0.05, including extracellular matrix/structure organization. This partly matches the paper's report that exercise down-regulates collagen- and ECM-related pathways.
  - Up-regulated genes: no GO BP term at adj p < 0.05.
- GSEA: no Hallmark set at FDR < 0.05. TGF-beta signaling has the lowest negative NES (-1.25, FDR 0.09), the same direction as the paper's reduced TGF-beta after exercise. This is exploratory.

## Deviations
- pydeseq2 was used ins ... [900 more characters]
