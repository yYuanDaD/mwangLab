# Review packet B (the analysis' decisions): GSE205173

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.1.treatment", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "description", "n_values": 3, "max_repeat": 6, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## Samples per design level

### `grp`
- **Ctrl** (3): GSM6206813 / Ctrl1; GSM6206814 / Ctrl2; GSM6206815 / Ctrl3
- **CtrlSwim** (3): GSM6206816 / Ctrl_Swim2; GSM6206817 / Ctrl_Swim3; GSM6206818 / Ctrl_Swim4
- **Model** (3): GSM6206819 / Model1; GSM6206820 / Model2; GSM6206821 / Model3
- **ModelSwim** (3): GSM6206822 / Swim1; GSM6206823 / Swim2; GSM6206824 / Swim3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE205173"], "assay": "bulk RNA-seq (TruSeq stranded mRNA) of colorectal tissue, male C57BL/6 mice", "factors": {"disease": ["vehicle (water)", "AOM/DSS CAC model"], "swim": ["no swim (shallow-water sham)", "swimming pretreatment, 2 months before and throughout the experiment"]}, "groups": ["Ctrl", "Ctrl_Swim", "Model", "Model_Swim"], "sample_inclusion": "Animals: Ctrl n=5, Ctrl_Swim n=5, Model n=10, Model_Swim n=10 (S2.3.p1); GEO deposits 3 colons per group (12 samples). Paper does not state how the sequenced subset was chosen.", "primary_estimand": "Effect of swimming pretreatment on colonic gene expression in AOM/DSS-induced CAC mice (Model_Swim vs Model); secondary: swimming in healthy mice (Ctrl_Swim vs Ctrl) and disease effect (Model vs Ctrl), which together define the paper's swim-reversed STEM profiles (S3.2.p1).", "planned_contrasts": ["Model_Swim vs Model (S3.2.p1, S3.4.p2 pair list; paper gives no per-contrast count)", "Ctrl_Swim vs Ctrl (S3.4.p2 pair list; no per-contrast count)", "Model vs Ctrl (S3.2.p1; no per-contrast count)", "Model_Swim vs Ctrl_Swim (S3.4.p2 pair list; no per-contrast count)", "Union of pairwise DEGs = 1403 genes (S3.2.p1), 279 STEM-selected, 48 inflammation/immune genes (S3.2.p1, Fig 3K)"], "repeated_measure_unit": "none; one colon per independent animal", "normalization": "paper: HISAT2 + HTSeq-count read counts, Cufflinks FPKM (S2.7.p1)", "paper_method": "DESeq2 pairwise between groups (S2.7.p1)", "paper_threshold": {"metr ... [470 more characters]

reasoning: Four-group 2x2 design (S2.3.p1). Transcriptome DE by DESeq2 with q<0.05 and FC>2 or <0.5 (S2.7.p1). The paper reports only the union (1403) of pairwise DEG sets, not which pairs were included nor per-pair counts (S3.2.p1); the metabolomics section lists the four pairs Ctrl/Ctrl_Swim, Ctrl/Model, Ctrl_Swim/Model_Swim, Model_Swim/Model (S3.4.p2), which I take as the planned pairs. The exercise question is Model_Swim vs Model (title, S3.2.p1, Fig 3I differential genes caused by swimming in AOM/DSS-induced CAC mice).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE205173\\GSE205173_Raw_gene_counts_matrix.txt.gz", "owned": true, "checks": ["S2.7.p1 and S5.p1 name GSE205173", "GEO organism Mus musculus, colorectal tissue, matches S2.4.p1", "four treatment levels NC / swim only / AOM/DSS / AOM/DSS+swimming pretreatment match the paper's four groups", "contact institute Shanghai Tong Ren Hospital matches the authors"], "accession": "GSE205173", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE205173\\GSE205173_metadata.csv"}

reasoning: Paper deposits RNA-seq as GSE205173 (S2.7.p1, S5.p1); GEO sample annotation matches the four groups. Raw gene count matrix (integers) chosen over the FPKM/RPKM file because the paper's DESeq2 used read counts.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(Ctrl_Swim|Ctrl|Model|Swim)\\d+$", "recode": {"Ctrl": "Ctrl", "Ctrl_Swim": "CtrlSwim", "Model": "Model", "Swim": "ModelSwim"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\aligned\\design_metadata.csv", "sha256": "a3ebecae6dfb154dc5fc42bc0ba9cd8c0b745be14194f74fddc2d8b9af65e2a1", "levels": {"grp": {"Ctrl": 3, "CtrlSwim": 3, "Model": 3, "ModelSwim": 3}}}}

reasoning: Matrix column names equal metadata title exactly (12/12). Group from title prefix; cross-checked against characteristics treatment: Ctrl=NC, Ctrl_Swim=swim only, Model=AOM/DSS treated, Swim=AOM/DSS treated+swimming pretreatment. Swim titles are the Model_Swim group, recoded ModelSwim.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\aligned\\aligned_matrix.csv", "sha256": "02f755fbcb69e9780afdd6345064aad0e84d9113fea94b55aaabcf67b19104e4", "n_features": 18514, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 392826.0, "median": 280.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Raw_gene_counts_matrix: integer fraction 1.0, max 392826, library sizes 17.3-19.5M per sample: unnormalized read counts. GEO data_processing says counts and RPKM came from CLC Genomics Workbench (the FPKM file is the RPKM output), while the paper says HISAT2/HTSeq-count; both are read counts, so the DESeq2 input is the same kind as the paper's. Gene IDs are symbols; 12 symbols are Excel-mangled (1-Mar..11-Mar, 15-Sep) but unique, kept as-is (none is a paper-named gene).

### design (valid, not_started)

final: {"analysis_type": "multi-group (2x2 factorial expressed as 4-level cell-means factor), pairwise planned contrasts", "design_column": "grp", "contrasts": [{"name": "grp_ModelSwim_vs_Model", "control": "Model", "treatment": "ModelSwim", "role": "primary"}, {"name": "grp_CtrlSwim_vs_Ctrl", "control": "Ctrl", "treatment": "CtrlSwim", "role": "secondary"}, {"name": "grp_Model_vs_Ctrl", "control": "Ctrl", "treatment": "Model", "role": "secondary"}, {"name": "grp_ModelSwim_vs_CtrlSwim", "control": "CtrlSwim", "treatment": "ModelSwim", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: Paper analyzes four groups pairwise (S3.2.p1, S3.4.p2). One DESeq2 model on all 12 samples with planned pairwise contrasts; the exercise estimand is ModelSwim vs Model (interventional, randomized assignment S2.3.p1), with CtrlSwim vs Ctrl as the swim effect without disease. Model vs Ctrl and ModelSwim vs CtrlSwim are disease contrasts kept because the paper's union includes them. n=3 per group. All male (S2.1.p1). The swim x disease interaction is not a paper contrast and is not run.

rejected alternatives: [{"value": "two factors disease + swim additive", "reason_rejected": "additive model would force the swim effect to be equal in healthy and CAC mice; paper compares groups pairwise"}, {"value": "pool Ctrl and Ctrl_Swim as one control", "reason_rejected": "pools levels of the factor of interest"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 12, "n_columns": 4, "columns": ["Intercept", "grp_CtrlSwim", "grp_Model", "grp_ModelSwim"], "rank": 4, "full_rank": true, "residual_df": 8, "levels": {"grp": {"Ctrl": 3, "CtrlSwim": 3, "Model": 3, "ModelSwim": 3}}, "cells": [{"cell": ["Ctrl"], "n": 3}, {"cell": ["CtrlSwim"], "n": 3}, {"cell": ["Model"], "n": 3}, {"cell": ["ModelSwim"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 12, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 12, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.treatment", "n_levels": 4, "status": "complete_confounding", "crosstab": {"Ctrl": {"AOM/DSS treated": 0, "AOM/DSS treated+swimming pretreatment": 0, "NC": 3, "swim only": 0}, "CtrlSwim": {" ... [2863 more characters]

reasoning: Independent animals, one colon each; no batch, lane, or sex variable (all male, single submission/platform). No covariate column in metadata.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "DESeq2", "status": "reproduced"}, "deviations": ["one model fitted on all 12 samples (shared dispersion) rather than per-pair fits; a per-pair two-arm fit for the primary contrast is run as sensitivity", "counts from CLC Genomics Workbench (GEO) rather than the paper's stated HISAT2/HTSeq-count"]}

reasoning: Raw counts support the paper's DESeq2 route (S2.7.p1).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: S2.7.p1: q value < 0.05 and fold change > 2 or < 0.5 = padj < 0.05 and |log2FC| > 1 (strict). Audit: padj < 0.05 without effect cutoff.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "de", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\de\\DEG_results_grp_ModelSwim_vs_Model.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\de\\DEG_results_grp_CtrlSwim_vs_Ctrl.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\de\\DEG_results_grp_Model_vs_Ctrl.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\de\\DEG_results_grp_ModelSwim_vs_CtrlSwim.csv"], "counts": {"de/grp_ModelSwim_vs_Model": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 15162, "n_significant": 111, "n_up": 42, "n_down": 69, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15162, "n_significant": 359, "n_up": 215, "n_down": 144, "deg_sanity": "ok"}}, "de/grp_CtrlSwim_vs_Ctrl": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 12678, "n_significant": 65, "n_up": 26, "n_down": 39, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 12678, "n_significant": 661, "n_up": 213, "n_down": 448, "deg_sanity": "ok"}}, "de/grp_Model_vs_Ctrl": {"applied": {"rule": "pad ... [562 more characters]

reasoning: One DESeq2 ~grp model on all 12 samples; four planned pairwise contrasts, primary ModelSwim vs Model.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pair_ModelSwim_vs_Model", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\pair_ModelSwim_vs_Model\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\pair_ModelSwim_vs_Model\\DEG_results_ModelSwim_vs_Model.csv"], "counts": {"pair_ModelSwim_vs_Model": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 15993, "n_significant": 130, "n_up": 35, "n_down": 95, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15993, "n_significant": 315, "n_up": 140, "n_down": 175, "deg_sanity": "ok"}}}}

reasoning: Per-pair two-arm DESeq2 fit (only the 6 samples of the pair), as a vendor pairwise pipeline would do.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "de/grp_ModelSwim_vs_Model", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\enrichment_de_grp_ModelSwim_vs_Model\\ora\\DEG_results_grp_ModelSwim_vs_Model_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\enrichment_de_grp_ModelSwim_vs_Model\\ora\\DEG_results_grp_ModelSwim_vs_Model_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\enrichment_de_grp_ModelSwim_vs_Model\\ora\\DEG_results_grp_ModelSwim_vs_Model_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\enrichment_de_grp_ModelSwim_vs_Model\\ora\\DEG_results_grp_ModelSwim_vs_Model_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 111 Mouse genes (direction=all, padj<0.05, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Proteolysis (GO:0006508) | padj=6.36e-03 | overlap=10/330 | gene ... [1275 more characters]

reasoning: Paper reports GO/KEGG enrichment of swimming-affected genes (S2.7.p1, Fig 3J).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "de/grp_ModelSwim_vs_Model", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35847876\\GSE205173\\results\\enrichment_de_grp_ModelSwim_vs_Model\\gsea\\DEG_results_grp_ModelSwim_vs_Model_GSEA_Hallmark.csv"], "summary": "GSEA complete on 18399 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 35 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.36 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.79 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.69 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=2.25 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_BILE_ACID_METABOLISM | NES=2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_PEROXISOME | NES=2.07 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HEME_METABOLISM | NES=1.94 | NOM p=0.00e+00 | FDR q=1.44e-04 - HALLMARK_PROTEIN_SECRETION | NES=1.89 | NOM p=0.00e+00 | FDR q=3.84e-04 - HALLMARK_ANDROGEN_RESPONSE | NES=1.87 | NOM p=0.00e+00 | FDR q=3.46e-04 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=-2.45 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=-2.29 | N ... [417 more characters]

reasoning: Paper reports GO/KEGG enrichment of swimming-affected genes (S2.7.p1, Fig 3J).

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper reports only the union of pairwise DEGs (1403) with no per-contrast counts, so per-table comparison is not possible; union across our four planned tables is reported in HANDBACK.md.", "n=3 per group; paper does not say how 3 of 5/10 animals per group were chosen for sequencing.", "Counts are CLC Genomics Workbench output (GEO) although the paper states HISAT2/HTSeq.", "Named genes, ModelSwim vs Model: Pla2g4f and Ptges lower with swimming and Fzd9, Cldn15, Tfrc higher (directions agree with the paper) but none passes padj < 0.05; Ptger2 is unchanged (log2FC +0.07), so the paper's swim-reduced Ptger2/EP2 is not reproduced at the gene level.", "Named genes, Model vs Ctrl: Pla2g4f and Ptges up, Fzd9, Cldn15, Tfrc down, all padj < 0.05 (agree with the paper); Ptger2 not significantly up (log2FC +0.32, padj 0.42), contrary to the paper's AOM/DSS-induced Ptger2 up-regulation.", "Top KEGG ORA term for ModelSwim vs Model is Pancreatic secretion (plus protein/fat/carbohydrate digestion and absorption), in line with the paper's digestion-and-absorption KEGG terms (S3.2.p1), but pancreatic-enzyme genes in colon tissue may reflect tissue composition rather than swimming biology."], "results": {"de/grp_ModelSwim_vs_Model": {"n_deg": 111, "up": 42, "down": 69, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 359}, "de/grp_CtrlSwim_vs_Ctrl": {"n_deg": 65, "up": 26, "down": 39, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n":  ... [1645 more characters]

reasoning: Paper-aligned DESeq2 with the paper threshold; named genes from S3.2.p1 (Ptger2/Pla2g4f/Ptges up in Model and reduced by swimming; Fzd9/Cldn15/Tfrc lowest in Model).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "alignment/quantification pipeline",
    "paper": "Trimmomatic, HISAT2, HTSeq-count, Cufflinks FPKM (S2.7.p1)",
    "data": "GEO data_processing: CLC Genomics Workbench 11 mapping, counts and RPKM",
    "disposition": "executable_without_change"
  },
  {
    "item": "sequenced sample size",
    "paper": "Ctrl 5, Ctrl_Swim 5, Model 10, Model_Swim 10 animals (S2.3.p1)",
    "data": "3 samples per group in GEO",
    "disposition": "executable_without_change"
  },
  {
    "item": "sequencer",
    "paper": "Illumina HiSeq X Ten (S2.7.p1)",
    "data": "GEO instrument Illumina NovaSeq 6000",
    "disposition": "executable_without_change"
  },
  {
    "item": "per-contrast DEG counts",
    "paper": "only union 1403 across pairwise comparisons, pairs not listed (S3.2.p1)",
    "data": "four planned pairwise tables",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 35847876 / GSE205173

## What ran
- Route: case spec (`tools.case_runner execute case_spec.json`). Status completed, decision contract validator reported 0 errors (13 records). The run was executed twice; the first attempt (same numbers, no gene-check caveats) is in `_previous/20261117T225315Z`.
- Data: `GSE205173_Raw_gene_counts_matrix.txt.gz`. Integer counts, 18,514 gene symbols, 12 samples (3 per group), 17.3-19.5M reads per sample. Aligned exactly on `title` (12/12). Group comes from the title prefix and agrees with the GEO treatment field: Ctrl, CtrlSwim, Model (AOM/DSS), ModelSwim (AOM/DSS plus swimming).
- Design: one DESeq2 (pydeseq2 Wald) `~ grp` model on all 12 samples with four planned pairwise contrasts. No blocking: the samples are independent animals, all male (the sex check passed, one sex only), with no batch recorded.
  - Primary: ModelSwim vs Model.
  - Secondary: CtrlSwim vs Ctrl, Model vs Ctrl, ModelSwim vs CtrlSwim.
- Sensitivity: a separate two-arm DESeq2 fit on only the 6 Model and ModelSwim samples.
- Enrichment on the primary table: ORA (GO BP/MF/CC, KEGG) on the paper-threshold DEGs, and GSEA (Hallmark) on the full ranking by stat. Both completed.

## Threshold
The paper's rule (S2.7.p1) is "q value < 0.05, fold change > 2, or fold change < 0.5". It was applied as padj < 0.05 and |log2FC| > 1, both strict (threshold_source = paper). The audit rule is padj < 0.05 with no fold-change cutoff.

## DEG counts vs the paper
The paper gives no per-contrast counts. It reports only the union of pairwise DEGs (1403), without saying which pairs went into it (S3.2.p1).

| Table | ours (paper rule) | up / down | audit (padj<0.05) | paper |
|---|---|---|---|---|
| de/grp_ModelSwim_vs_Model (primary) | 111 | 42 / 69 | 359 | not reported |
| de/grp_CtrlSwim_vs_Ctrl | 65 | 26 / 39 | 661 | not reported |
| de/grp_Model_vs_Ctrl | 1343 | 1139 / 204 | 5545 | not reported |
| de/grp_ModelSwim_vs_CtrlSwim | 270 | 239 / 31 | 1557 | not reported |
| pair_ModelSwim_vs_Model (sensitivity, per-pair fit) | 130 | 35 / 95 | 315 | - |
| Union of our 4 tables | 1442 | | | 1403 (union) |

- The joint and per-pair fits agree closely: log2FC r = 0.991, and 90 DEGs are shared.
- Genes reversed by swimming (comparable to the paper's STEM selection of 279):
  - 59 genes are up in Model vs Ctrl and down in ModelSwim vs Model.
  - 33 genes are down in Model vs Ctrl and up in ModelSwim vs Model.
- Named genes (S3.2.p1):
  - ModelSwim vs Model: Pla2g4f (-0. ... [2371 more characters]
