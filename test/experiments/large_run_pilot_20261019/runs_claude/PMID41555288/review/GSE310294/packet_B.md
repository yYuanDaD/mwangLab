# Review packet B (the analysis' decisions): GSE310294

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.3.treatment", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_EX_vs_CTRL | 2076 | 4459 | pvalue <= 1 and |log2FoldChange| > 1 | 1 | 1 | 1 | 1 | 543 | 529 | 413 | 92 | 0.101 | 0.026 |

## Samples per design level

### `grp`
- **CTRL** (3): GSM9293443 / bone, control, rep1 / Library name: Sample 1; GSM9293444 / bone, control, rep2 / Library name: Sample 2; GSM9293445 / bone, control, rep3 / Library name: Sample 3
- **EX** (3): GSM9293446 / bone, exercised, rep1 / Library name: Sample 4; GSM9293447 / bone, exercised, rep2 / Library name: Sample 5; GSM9293448 / bone, exercised, rep3 / Library name: Sample 6

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE310294"], "assay": "bulk RNA-seq of left tibia (bone tissue), Novogene, Illumina", "organism": "Rat (male SD, 16 weeks old at start)", "factors": {"group": ["Ctrl", "Exercise"]}, "sample_inclusion": "RNA-seq n = 3 rats per group (Fig. 5 legend); left tibiae", "primary_estimand": "Effect of 6-week moderate-intensity treadmill exercise vs sedentary control on tibial bone gene expression in adult male rats", "planned_contrasts": ["Exercise vs Ctrl (S3.3.p1; paper: 2076 DEGs, 1552 up / 524 down)"], "repeated_measure_unit": "none (independent rats, one sample each)", "normalization": "not_reported (Novogene pipeline; GEO: StringTie FPKM)", "paper_method": "DEGseq R package (S2.6.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 1.0, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": false, "effect_cutoff_original": "Fold Change < -2 or > 2", "significance_criterion": "not_reported (paper states only the fold-change rule); encoded as no p-value filter", "source_locator": "S3.3.p1"}, "paper_results": "2076 DEGs (1552 up, 524 down); 39 bone-formation genes up incl. Igf1r, Bglap, Sp7, Smad6, Runx2, Ctnnb1, Col1a1, Pth1r (S3.3.p3); qPCR Runx2 up, Rankl/Trap down; GO/KEGG ORA (FDR < 0.05 for terms), GSEA ECM/osteoblast differentiation enriched in exercise"}

reasoning: S2.6.p1: left tibiae RNA-seq by Novogene, DE with DEGseq, GO/KEGG on DEGs with FDR < 0.05 for terms, GSEA v4.1.0. S3.3.p1: 'classic criteria (Fold Change < -2 or > 2)' gives 2076 DEGs (1552 up / 524 down); no p or q cutoff is stated for genes. Fig. 5 legend: n = 3 rats per group. ABS.p2: male SD rats, 6-week moderate treadmill. The gene threshold is encoded literally as FC-only (no p filter); a significance-filtered audit rule is reported separately.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\prep\\GSE310294_counts_renamed.csv", "owned": true, "checks": ["DA.p1 names GSE310294", "organism Rattus norvegicus, ENSRNOG gene IDs", "tissue bone; 3 'control' + 3 'exercised' samples matches Fig. 5 n = 3 per group", "only one expression file deposited (gene_expression_list.csv/.xlsx identical content)"], "accession": "GSE310294", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE310294\\GSE310294_metadata.csv"}

reasoning: Data availability statement (DA.p1) names GSE310294; the series has 6 rat bone samples, 3 control and 3 exercised, matching the RNA-seq design in Fig. 5. The csv and xlsx contain the same 32883 x 6 table; the csv is used.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "characteristics_ch1.3.treatment", "regex": "^(no|exercise)$", "recode": {"no": "CTRL", "exercise": "EX"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\aligned\\design_metadata.csv", "sha256": "fa064c4ba1d8b005fa6e53b1534056049ed5e34f013bbbb4e8d4cca7bb25b032", "levels": {"grp": {"CTRL": 3, "EX": 3}}}}

reasoning: Matrix columns sample1..6_FPKM were renamed to Sample_1..6 by prep_rename_columns.py (values untouched); metadata 'description' holds 'Library name: Sample N', from which key_patterns derives 'Sample_N' for an exact match. Group from characteristics 'treatment' (no -> CTRL, exercise -> EX), consistent with titles 'bone, control/exercised, repN'. No position-based mapping.

### matrix (valid, not_started)

final: {"source": "GSE310294_gene_expression_list.csv (supplementary, columns renamed only)", "paper_input": "not_reported explicitly; DEGseq takes read counts", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\aligned\\aligned_matrix.csv", "sha256": "ca38fdc7605beab0787b5e8facaa9748d14f9f552f8aee6fbeb4a4bf6c6cba13", "n_features": 32883, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1197892.0, "median": 2.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Column names say '_FPKM' but every value is an integer (integer fraction 1.0), median 2, max 1.2e6, and column sums are 14.1-18.1 million, i.e. library sizes; FPKM columns would not be integers and would not sum to read depths. GEO data_processing says 'Supplementary files ... include raw fragment counts for each Sample'. Decision: raw fragment counts mislabelled as FPKM. (data_processing also mentions hg38/mm10, which is boilerplate: IDs are rat ENSRNOG.)

rejected alternatives: [{"value": "FPKM", "reason_rejected": "all-integer values with column sums equal to read depths (14-18 M); GEO processing note says raw fragment counts"}]

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "CTRL", "treatment": "EX", "estimand_type": "causal (randomized intervention per paper)", "contrasts": [{"name": "grp_EX_vs_CTRL", "control": "CTRL", "treatment": "EX", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: One exercise arm and one control arm of independent rats (S3.3.p1, Fig. 5); the paper's only RNA-seq contrast is Exercise vs Ctrl. 3 vs 3.

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 6, "n_columns": 2, "columns": ["Intercept", "grp_EX"], "rank": 2, "full_rank": true, "residual_df": 4, "levels": {"grp": {"CTRL": 3, "EX": 3}}, "cells": [{"cell": ["CTRL"], "n": 3}, {"cell": ["EX"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 6, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 6, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.cell type", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.genotype", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.treatment", "n_levels": 2, "status": "complete_confounding", "crosstab": {"CTRL": {"exercise": 0, "no": 3}, "EX": {"exercise": 3, "no": 0}}}, {"column": "molecule_ ... [1346 more characters]

reasoning: Independent animals, one tibia sample each; no batch, sex (all male) or other covariate in the metadata or paper.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "DEGseq (R)", "status": "blocked", "reason": "no DEGseq executor in the workflow; DEGseq's MA-plot test is designed for unreplicated data and is not a validated route here"}, "deviations": ["DESeq2 Wald on raw counts instead of DEGseq; edgeR (TMM) run as sensitivity because GEO data_processing names edgeR"]}

reasoning: Raw integer counts support DESeq2. The paper's DEGseq (S2.6.p1) has no executor, so DESeq2 runs as a declared deviation with the paper's threshold; edgeR sensitivity mirrors the GEO processing note.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 1.0, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 1.0, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "deviation_note": "Paper rule (FC > 2 or < -2, no stated p/q cutoff) applied to DESeq2 log2FC; audit adds BH padj < 0.05."}

reasoning: S3.3.p1 states only 'Fold Change < -2 or > 2' -> |log2FC| > 1 (exact, strict); no gene-level significance cutoff is given, so the paper rule is FC-only. Audit rule padj < 0.05 & |log2FC| > 1 shows how many of those also pass significance.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_EX_vs_CTRL", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\aligned\\aligned_matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\results\\grp_EX_vs_CTRL\\DEG_results_EX_vs_CTRL.csv"], "counts": {"grp_EX_vs_CTRL": {"applied": {"rule": "pvalue <= 1 and |log2FoldChange| > 1", "n_tested": 20681, "n_significant": 4459, "n_up": 2808, "n_down": 1651, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 20681, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: two-group count model for the paper's Exercise vs Ctrl contrast (deviation from DEGseq)

### execution (valid, completed)

final: {"method": "run_edger_analysis", "subset": "edgeR_EX_vs_CTRL", "role": "sensitivity", "tool": "tools.edger_tools:run_edger_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\aligned\\aligned_matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\results\\edgeR_EX_vs_CTRL\\DEG_results_EX_vs_CTRL.csv"], "counts": {"edgeR_EX_vs_CTRL": {"applied": {"rule": "pvalue <= 1 and |log2FoldChange| > 1", "n_tested": 20727, "n_significant": 5321, "n_up": 3266, "n_down": 2055, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 20727, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: GEO data_processing names edgeR; checks method sensitivity

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "grp_EX_vs_CTRL", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 1.0, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\results\\enrichment_grp_EX_vs_CTRL\\ora\\DEG_results_EX_vs_CTRL_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\results\\enrichment_grp_EX_vs_CTRL\\ora\\DEG_results_EX_vs_CTRL_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\results\\enrichment_grp_EX_vs_CTRL\\ora\\DEG_results_EX_vs_CTRL_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\results\\enrichment_grp_EX_vs_CTRL\\ora\\DEG_results_EX_vs_CTRL_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 3040 Rat genes (direction=all, pvalue<1.0, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - R ... [1338 more characters]

reasoning: paper reports GO/KEGG ORA on DEGs and GSEA (S2.6.p1, S3.3.p2-p3)

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "grp_EX_vs_CTRL", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41555288\\GSE310294\\results\\enrichment_grp_EX_vs_CTRL\\gsea\\DEG_results_EX_vs_CTRL_GSEA_Hallmark.csv"], "summary": "GSEA complete on 15975 Rat genes ranked by 'stat'. 50 Hallmark sets tested, 40 significant at FDR q < 0.25. Rat genes matched to mouse Hallmark by symbol: 3825/4291 Hallmark genes present in the ranking. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_E2F_TARGETS | NES=3.25 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=2.81 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HEME_METABOLISM | NES=2.64 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.48 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.38 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.15 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_DNA_REPAIR | NES=2.06 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=1.98 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.97 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COMPLEMENT | NES=1.62 | NOM p=0.00e+00 | FDR q=7 ... [522 more characters]

reasoning: paper reports GO/KEGG ORA on DEGs and GSEA (S2.6.p1, S3.3.p2-p3)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper used DEGseq; DESeq2 runs instead (paper route blocked).", "Paper threshold is fold-change only; FC-only counts on DESeq2 MLE log2FC include low-count genes, so the padj audit count is the more reliable number.", "Matrix columns are labelled FPKM but hold raw integer counts (decided from values and GEO processing note)."], "results": {"grp_EX_vs_CTRL": {"n_deg": 4459, "up": 2808, "down": 1651, "rule": "pvalue <= 1 and |log2FoldChange| > 1", "audit_n": 1}, "edgeR_EX_vs_CTRL": {"n_deg": 5321, "up": 3266, "down": 2055, "rule": "pvalue <= 1 and |log2FoldChange| > 1", "audit_n": 0}}, "paper_counts": {"grp_EX_vs_CTRL": 2076}, "comparison": {"grp_EX_vs_CTRL": {"ours": 4459, "paper": 2076}}, "paper_gene_check": {"grp_EX_vs_CTRL": {"Igf1r": {"baseMean": 113.0595, "log2FoldChange": -0.0781, "padj": 0.9977, "pvalue": 0.8782}, "Bglap": {"baseMean": 419.7422, "log2FoldChange": -0.5244, "padj": 0.9951, "pvalue": 0.8067}, "Sp7": {"baseMean": 19.9991, "log2FoldChange": -1.012, "padj": null, "pvalue": null}, "Smad6": {"baseMean": 120.6181, "log2FoldChange": -0.137, "padj": 0.9951, "pvalue": 0.7937}, "Runx2": {"baseMean": 192.9606, "log2FoldChange": 0.2788, "padj": 0.9951, "pvalue": 0.7973}, "Ctnnb1": {"baseMean": 3136.8011, "log2FoldChange": -0.1798, "padj": 0.9951, "pvalue": 0.4179}, "Col1a1": {"baseMean": 18661.6725, "log2FoldChange": -1.205, "padj": 0.9951, "pvalue": 0.277}, "Pth1r": {"baseMean": 158.734, "log2FoldChange": -0.6406, "padj":  ... [319 more characters]

reasoning: Paper reports 2076 DEGs (1552 up / 524 down) and names bone-formation genes as up in exercise (S3.3.p3); qPCR Rankl (Tnfsf11) and Trap (Acp5) down; p53/Caspase-3 protein down (S3.5.p1).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix scale label",
    "paper": "not stated",
    "data": "columns named *_FPKM but integer raw fragment counts (sums 14-18 M; GEO: raw fragment counts)",
    "disposition": "executable_without_change"
  },
  {
    "item": "DE method",
    "paper": "DEGseq (S2.6.p1)",
    "data": "GEO data_processing says edgeR; workflow has neither DEGseq executor",
    "disposition": "requires_explicit_deviation"
  },
  {
    "item": "gene threshold",
    "paper": "Fold Change < -2 or > 2, no p/q stated (S3.3.p1)",
    "data": "applied literally (FC-only) plus padj audit",
    "disposition": "executable_without_change"
  },
  {
    "item": "reference genome note",
    "paper": "not stated",
    "data": "GEO says hg38 / mm10 but IDs are rat ENSRNOG",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID41555288 / GSE310294

Run: `python -m tools.case_runner execute test/experiments/large_run_pilot_20261019/runs_claude/PMID41555288/case_spec.json`. Status `completed`, 13 records, 0 contract validator errors.

## What ran

- **Paper (PMC12896231):** 6-week moderate treadmill exercise vs sedentary control in adult male SD rats. RNA-seq on the left tibia, n = 3 per group (Fig. 5). Novogene used the DEGseq R package for DE (S2.6.p1). The DEG rule is only "Fold Change < -2 or > 2" (S3.3.p1); no p or q cutoff is stated. Paper result: 2076 DEGs (1552 up, 524 down).
- **Ownership:** DA.p1 names GSE310294. The series has 6 rat bone samples (3 control, 3 exercised) with ENSRNOG IDs.
- **Alignment:** a prep script, `prep_rename_columns.py`, renamed the matrix columns from `sampleN_FPKM` to `Sample_N`; the values are unchanged. `key_patterns` builds the same `Sample_N` key from the metadata field `description` ("Library name: Sample N"). Match is exact, 6/6. Groups come from the `treatment` field (no -> CTRL, exercise -> EX).
- **Matrix:** raw counts. The columns are named `_FPKM`, but every value is an integer and the column sums are 14.1-18.1 M, which are library sizes. GEO data_processing also says "raw fragment counts".
- **Design:** two groups, `~ grp`, EX vs CTRL, 3 vs 3. The suitability check returned "analyzable". No blocking or covariates.
- **Method:** DESeq2 (pydeseq2 Wald) as the primary analysis. This is a declared deviation: the paper's DEGseq route is blocked because the workflow has no DEGseq executor. edgeR (TMM) ran as a sensitivity analysis, because GEO data_processing names edgeR.
- **Threshold:** the paper's rule was applied exactly, on the deviation route: |log2FC| > 1 with no p-value filter. A separate audit rule adds BH padj < 0.05.
- **Enrichment** on the primary table:
  - ORA (Enrichr GO BP/MF/CC and KEGG_2019_Mouse, using rat gene symbols), on the FC-only list. Top KEGG terms include cytokine-receptor interaction, hematopoietic cell lineage and ECM-receptor interaction.
  - GSEA Hallmark, mouse sets. Enriched in exercise: E2F targets, G2M checkpoint, heme metabolism, allograft rejection and interferon responses, all at FDR about 0. This agrees in direction with the paper's GO findings: "chromosome, centromeric region" up and leukocyte immunity up.

## DEG counts vs paper (paper rule: |FC| > 2, no p filter)

| Table | Paper rule (FC-only) | Audit (padj < 0.05 and abs log2FC > 1) | Paper |
|---|---|---|---|
| DESeq2 EX vs CTR ... [1913 more characters]
