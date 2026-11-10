# Review packet B (the analysis' decisions): GSE289091

## Mechanical flags

- **other_rule_matches_paper**: {"table": "silmna_stretch_run2/silmna_stretch_run2", "paper": 634, "applied": 2119, "applied_rule": "padj < 0.05 and |log2FoldChange| > 0.5", "closest_rule": "pvalue<0.05 & |lfc|>1", "closest_n": 581, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **pairing_key_candidate**: {"key": "cond (without characteristics_ch1.2.genotype) + suffix of title", "across": "characteristics_ch1.2.genotype", "pairs_or_sets": 5, "samples_linked": 10, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ctl_stretch/ctl_stretch | 7 | 21 | padj < 0.05 and |log2FoldChange| > 0.5 | 23 | 13 | 3 | 26 | 544 | 120 | 18 | 178 | 0.125 | 0.038 |
| silmna_stretch_run2/silmna_stretch_run2 | 634 | 2119 | padj < 0.05 and |log2FoldChange| > 0.5 | 3985 | 1694 | 554 | 5168 | 5705 | 1917 | 581 | 3642 | 0.046 | 0.382 |

## Samples per design level

### `cond`
- **static** (10): GSM8783555 / myotubes, siControl, Hours72, static, re / Library name: ctrl2,run1; GSM8783556 / myotubes, siControl, Hours72, static, re / Library name: ctrl3,run1; GSM8783558 / myotubes, siLaminsA/C, Hours72, static,  / Library name: si-1,run1; GSM8783559 / myotubes, siLaminsA/C, Hours72, static,  / Library name: si-2,run1; GSM8783560 / myotubes, siLaminsA/C, Hours72, static,  / Library name: si-3,run1; GSM8783566 / myotubes, siLaminsA/C, Hours72, static,  / Library name: Nsi-0,run2; GSM8783567 / myotubes, siLaminsA/C, Hours72, static,r / Library name: Nsi-2,run2; GSM8783568 / myotubes, siLaminsA/C, Hours72, static,r / Library name: Nsi-3,run2; GSM8783569 / myotubes, siLaminsA/C, Hours72, static,r / Library name: Nsi-4,run2; GSM9181790 / human myotubes, siControl, Hours72, stat / Library name: ctrl1,run1
- **stretch** (7): GSM8783563 / myotubes, siControl, Hours72, stretch,re / Library name: Sctrl4,run1; GSM8783564 / myotubes, siControl, Hours72, stretch,re / Library name: Sctrl5,run1; GSM8783565 / myotubes, siControl, Hours72, stretch,re / Library name: Sctrl6,run1; GSM8783570 / myotubes, siLaminsA/C, Hours72, stretch, / Library name: Ssi_1_1,run2; GSM8783571 / myotubes, siLaminsA/C, Hours72, stretch, / Library name: Ssi_1_2,run2; GSM8783572 / myotubes, siLaminsA/C, Hours72, stretch, / Library name: Ssi_1_3,run2; GSM8783573 / myotubes, siLaminsA/C, Hours72, stretch, / Library name: Ssi_4_1,run2

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE289091 (RNA-seq)", "GSE288984 (ATAC-seq, not analysed here)"], "assay": "bulk RNA-seq of immortalized human myotubes (clone 8220), DRAGEN mapping to hg38 + GENCODE v37 quantification", "factors": {"genotype": ["siControl (Ctl)", "siLMNA (siLaminsA/C)"], "loading": ["static", "4 h equibiaxial cyclic stretch 10%, 0.5 Hz"]}, "primary_estimand": "effect of acute mechanical stretch (in vitro exercise mimic) on gene expression, within each genotype: S-Ctl vs Ctl and S-siLMNA vs siLMNA", "planned_contrasts": ["S-Ctl vs Ctl (Fig. 6d, S3.3.p3; paper: 7 DEGs)", "S-siLMNA vs siLMNA (Fig. 6e, S3.3.p3; paper: 634 DEGs = 485 up / 149 down)"], "non_exercise_contrasts_not_run": ["siLMNA vs Ctl static (Fig. 3a; 876 DEGs, 446 up / 430 down)", "S-siLMNA vs S-Ctl (Fig. 8; ATAC only)"], "sample_inclusion": "n = 4 to 9 samples/group (S2.6.p1); exact samples per comparison not stated", "repeated_measure_unit": "none; independent wells/siRNA transfections", "normalization": "edgeR CPM; keep genes with CPM > 1 in at least 2 samples (S2.6.p3)", "paper_method": "DESeq2 v1.34 GLM likelihood ratio test, BH FDR (S2.6.p3)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "source_locator": "FIG6 legend d,e (stretch DEGs); S2.6.p3 states |log2FC| > 1 globally"}, "paper_results": "Ctl stretch: 7 DEGs; siLMNA stretch: 485 up, 149 down; up genes in cytokine activity, ECM, adhesion; down in HDAC, DNA methylation, contractile fibre; ... [87 more characters]

reasoning: Abstract (ABS.p2) frames the stretch as 'mechanical stress mimicking acute muscle exercise'. The exercise-like estimand is stretch vs static within genotype (Fig. 6d,e; S3.3.p3). Methods S2.6.p3 give DESeq2 LRT with CPM>1-in-2 filter and |log2FC|>1 & FDR<0.05, but the Fig. 6 legend for the stretch DEG volcano plots states log2FC > 0.5 & FDR < 0.05; the figure-specific rule is taken as the paper threshold for these contrasts and the methods rule is kept as an audit threshold.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE289091\\GSE289091_numreads_merged.csv", "owned": true, "checks": ["S10.p1 names GSE289091 as the RNA-seq dataset", "18 GSM samples: myotubes, siControl/siLaminsA/C, static/stretch, Hours72", "DRAGEN/GENCODE v37 processing in data_processing matches S2.6.p3"], "accession": "GSE289091", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE289091\\GSE289091_metadata.csv"}

reasoning: The paper's data availability statement (S10.p1) names GSE289091 for RNA-seq; sample titles carry the paper's genotype x stretch design.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 18, "n_metadata": 18, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM8783562": "labelled siControl stretch rep1 (library Sctrl3), but LMNA expression is at knockdown level (CPM 249 vs 801-874 in the other six siControl samples; 184-219 in run-1 siLMNA) and its expression profile correlates best with the run-1 siLMNA static samples (r 0.992-0.993 vs 0.978-0.981 with siControl); genotype label is not trustworthy"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\aligned\\aligned_metadata_kept.csv", "columns": {"geno": {"source": "title", "regex": "^.*?(siControl|siLaminsA/C),.*$", "recode": {"siControl": "Ctl", "siLaminsA/C": "siLMNA"}}, "cond": {"source": "title", "regex": "^.*?(static|stretch).*$", "recode": {"static": "static", "stretch": "stretch"}}, "run": {"source": "description", "regex": "^.*run(\\d)$", "recode": {"1": "r1", "2": "r2"}}, "grp": {"combine": ["geno", "cond"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\aligned\\design_metadata.csv", "sha256": "e959bad89138fd9c7179fbb305de8c54ac1c66446d5a7491277058a498741674", "levels": {"geno": {"siLMNA": 11, "Ctl": 6}, "cond": {"static": 10, "stretch": 7}, "run": {"r1": 9, "r2": 8}, "grp": {"siLMNA_static": 7, "siLMNA_stretch": 4, "Ctl_static": 3, "Ctl_stre ... [11 more characters]

reasoning: Matrix columns are GSM ids from the merged per-sample quant files, so the metadata index aligns exactly. Genotype and loading come from the title, sequencing run (run1 NovaSeq GPL24676 / run2 NextSeq GPL21697) from the description field. One sample excluded as a genotype labelling problem (LMNA knockdown check).

### matrix (valid, not_started)

final: {"source": "NumReads column of DRAGEN quant.genes.sf (Salmon-format) per sample, merged by prep_merge_quant.py", "paper_input": "DRAGEN gene quantification counts (S2.6.p3)", "matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\aligned\\aligned_matrix.csv", "sha256": "aaeb0d57965a7365d39bcc1d005cac6b88c3c74465c4977717facc30f3eddef3", "n_features": 60607, "n_samples": 17, "annotation_columns_dropped": ["GSM8783562"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2063253.27, "median": 0.0, "integer_fraction": 0.9331, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Non-negative values, 93% integer with fractional remainder typical of EM-estimated counts; library sizes 27-48 M, matching ~44 M reads/sample in S2.6.p3. Estimated counts are rounded for DESeq2, as DESeq2 users do with Salmon NumReads.

### design (valid, not_started)

final: {"analysis_type": "two-group within stratum (genotype)", "design_column": "cond", "contrasts": [{"name": "cond_stretch_vs_static_geno-Ctl", "control": "static", "treatment": "stretch", "stratum": {"geno": "Ctl"}, "role": "primary"}, {"name": "cond_stretch_vs_static_geno-siLMNA", "control": "static", "treatment": "stretch", "stratum": {"geno": "siLMNA"}, "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\suitability\\suitability.md", "n_comparisons": 2, "n_analyzable": 2}}

reasoning: Paper compares stretched to static myotubes separately within each genotype (Fig. 6d,e). Genotype is a stratum; loading is the factor. Run (sequencing batch) is a covariate candidate because siLMNA static samples span both runs.

rejected alternatives: [{"value": "genotype x stretch interaction", "reason_rejected": "not tested in the paper; the Ctl stretch contrast lies wholly in run 1 and the siLMNA stretch contrast wholly in run 2, so an interaction would also absorb any batch-by-stretch difference"}, {"value": "siLMNA vs Ctl static (Fig. 3)", "reason_rejected": "not an exercise/loading contrast"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": [], "covariates": [{"name": "run", "disposition": "handled by restricting the primary siLMNA contrast to run 2 (all four stretched siLMNA samples are run 2); sensitivity runs use all seven static siLMNA samples with and without a run term. Not needed for Ctl (all Ctl samples are run 1)."}], "design_check": {"formula_equivalent": "~ C(cond)", "n_samples": 17, "n_columns": 2, "columns": ["Intercept", "cond_stretch"], "rank": 2, "full_rank": true, "residual_df": 15, "levels": {"cond": {"static": 10, "stretch": 7}}, "cells": [{"cell": ["static"], "n": 10}, {"cell": ["stretch"], "n": 7}], "min_cell_size": 7, "missing_values": {}}, "confounding": [{"column": "run", "n_levels": 2, "status": "crossed", "crosstab": {"static": {"r1": 6, "r2": 4}, "stretch": {"r1": 3, "r2": 4}}}]}

reasoning: Sequencing run 1 (NovaSeq) vs run 2 (NextSeq) is a strong batch: run-1 and run-2 static siLMNA samples correlate at r ~0.97 vs ~0.996 within run 2. Stretched siLMNA samples are all run 2, so pooling all static siLMNA without adjustment would partly confound stretch with run. The paper does not mention batch handling.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "DESeq2 (R) LRT, full ~ cond vs reduced ~ 1, per genotype", "formula": "~ cond", "paper_route": {"method": "DESeq2 GLM likelihood ratio test after CPM>1-in-2 filter", "status": "reproduced"}, "deviations": ["sample-label exclusion of GSM8783562", "siLMNA primary restricted to run 2 for batch reasons (paper sample set unknown)", "filter rule implemented as CPM >= 1 (paper: > 1) in >= 2 samples of each comparison's samples"], "rounding_documented": true}

reasoning: Paper used DESeq2 LRT (S2.6.p3); R DESeq2 is available through tools.r_de_tools. Estimated counts are rounded (round_estimated_counts).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "deviation_note": "Fig. 6 legend (stretch DEGs) states log2FC > 0.5 & FDR < 0.05; Methods S2.6.p3 state |log2FC| > 1 & FDR < 0.05. Applied = figure rule; audit = methods rule."}

reasoning: Figure-specific rule for the stretch contrasts; methods rule reported alongside because the paper is internally inconsistent.

### execution (valid, completed)

final: {"method": "DESeq2 (R) LRT ~cond vs ~1", "subset": "ctl_stretch", "role": "primary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\ctl_stretch\\input\\matrix_filtered.csv", "formula": "~ cond", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\ctl_stretch\\DEG_results_ctl_stretch.csv"], "counts": {"ctl_stretch/ctl_stretch": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 14368, "n_significant": 21, "n_up": 20, "n_down": 1, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 14368, "n_significant": 3, "n_up": 3, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: S-Ctl vs Ctl (Fig. 6d); 3 static vs 3 stretch, all run 1.

### execution (valid, completed)

final: {"method": "DESeq2 (R) LRT ~cond vs ~1", "subset": "silmna_stretch_run2", "role": "primary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\silmna_stretch_run2\\input\\matrix_filtered.csv", "formula": "~ cond", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\silmna_stretch_run2\\DEG_results_silmna_stretch_run2.csv"], "counts": {"silmna_stretch_run2/silmna_stretch_run2": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 14938, "n_significant": 2119, "n_up": 1460, "n_down": 659, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 14938, "n_significant": 554, "n_up": 429, "n_down": 125, "deg_sanity": "ok"}}}}

reasoning: S-siLMNA vs siLMNA (Fig. 6e) within sequencing run 2: 4 static vs 4 stretch, free of the run batch.

### execution (valid, completed)

final: {"method": "DESeq2 (R) LRT ~run+cond vs ~run", "subset": "silmna_stretch_all_runadj", "role": "sensitivity", "tool": "tools.r_de_tools:run_r_de", "n_samples": 11, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\silmna_stretch_all_runadj\\input\\matrix_filtered.csv", "formula": "~ run + cond", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\silmna_stretch_all_runadj\\DEG_results_silmna_stretch_all_runadj.csv"], "counts": {"silmna_stretch_all_runadj/silmna_stretch_all_runadj": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 15264, "n_significant": 1963, "n_up": 1325, "n_down": 638, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 15264, "n_significant": 564, "n_up": 434, "n_down": 130, "deg_sanity": "ok"}}}}

reasoning: All 7 static vs 4 stretch siLMNA with a run term.

### execution (valid, completed)

final: {"method": "DESeq2 (R) LRT ~cond vs ~1", "subset": "silmna_stretch_all_naive", "role": "sensitivity", "tool": "tools.r_de_tools:run_r_de", "n_samples": 11, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\silmna_stretch_all_naive\\input\\matrix_filtered.csv", "formula": "~ cond", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\silmna_stretch_all_naive\\DEG_results_silmna_stretch_all_naive.csv"], "counts": {"silmna_stretch_all_naive/silmna_stretch_all_naive": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 15275, "n_significant": 1373, "n_up": 742, "n_down": 631, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 15275, "n_significant": 296, "n_up": 200, "n_down": 96, "deg_sanity": "ok"}}}}

reasoning: All siLMNA samples without batch adjustment, the likely paper sample set; partly confounded with run, reported only for comparison with the paper's count.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "silmna_stretch_run2/silmna_stretch_run2", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\enrichment_silmna_stretch_run2_silmna_stretch_run2\\ora_up\\DEG_results_silmna_stretch_run2_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\enrichment_silmna_stretch_run2_silmna_stretch_run2\\ora_up\\DEG_results_silmna_stretch_run2_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\enrichment_silmna_stretch_run2_silmna_stretch_run2\\ora_up\\DEG_results_silmna_stretch_run2_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\enrichment_silmna_stretch_run2_silmna_stretch_run2\\ora_up\\DEG_results_silmna_stretch_run2_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 1120 Human genes (direction=up, padj<0.05, |log2FC|>0.5). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted  ... [1345 more characters]

reasoning: Paper ORA (gProfiler) on up DEGs (Fig. 6f); GSEA skipped because the LRT statistic is unsigned.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "silmna_stretch_run2/silmna_stretch_run2", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\enrichment_silmna_stretch_run2_silmna_stretch_run2\\ora_down\\DEG_results_silmna_stretch_run2_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\enrichment_silmna_stretch_run2_silmna_stretch_run2\\ora_down\\DEG_results_silmna_stretch_run2_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\enrichment_silmna_stretch_run2_silmna_stretch_run2\\ora_down\\DEG_results_silmna_stretch_run2_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41126185\\GSE289091\\results\\enrichment_silmna_stretch_run2_silmna_stretch_run2\\ora_down\\DEG_results_silmna_stretch_run2_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 632 Human genes (direction=down, padj<0.05, |log2FC|>0.5). ### GO_Biological_Process_2023 — top 10 terms (sorted b ... [1355 more characters]

reasoning: Paper ORA on down DEGs (Fig. 6f).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["GSM8783562 excluded as a likely genotype mislabel (LMNA at knockdown level)", "Paper's exact sample sets and batch handling are not stated; the siLMNA primary uses run 2 only", "Paper threshold is internally inconsistent (Fig. 6: 0.5; Methods: 1)", "In vitro stretch of myotubes is an exercise mimic, not exercise in people"], "results": {"ctl_stretch/ctl_stretch": {"n_deg": 21, "up": 20, "down": 1, "rule": "padj < 0.05 and |log2FoldChange| > 0.5", "audit_n": 3}, "silmna_stretch_run2/silmna_stretch_run2": {"n_deg": 2119, "up": 1460, "down": 659, "rule": "padj < 0.05 and |log2FoldChange| > 0.5", "audit_n": 554}, "silmna_stretch_all_runadj/silmna_stretch_all_runadj": {"n_deg": 1963, "up": 1325, "down": 638, "rule": "padj < 0.05 and |log2FoldChange| > 0.5", "audit_n": 564}, "silmna_stretch_all_naive/silmna_stretch_all_naive": {"n_deg": 1373, "up": 742, "down": 631, "rule": "padj < 0.05 and |log2FoldChange| > 0.5", "audit_n": 296}}, "paper_counts": {"ctl_stretch/ctl_stretch": 7, "silmna_stretch_run2/silmna_stretch_run2": 634}, "comparison": {"ctl_stretch/ctl_stretch": {"ours": 21, "paper": 7}, "silmna_stretch_run2/silmna_stretch_run2": {"ours": 2119, "paper": 634}}, "paper_gene_check": {"silmna_stretch_run2/silmna_stretch_run2": {"HMGA2": {"baseMean": 106.2366, "log2FoldChange": 1.8032, "padj": 0.0, "pvalue": 0.0}, "TIMP3": {"baseMean": 1179.3979, "log2FoldChange": 1.0884, "padj": 0.0, "pvalue": 0.0}, "HAS1": {"baseMean": 56.3745, "log2F ... [414 more characters]

reasoning: Counts from S3.3.p3 and genes from S3.3.p4 (CKMT2 down, the others up).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 17 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DEG threshold",
    "paper": "Methods: |log2FC| > 1 & FDR < 0.05; Fig. 6 legend: log2FC > 0.5 & FDR < 0.05",
    "data": "n/a",
    "disposition": "executable_without_change"
  },
  {
    "item": "GSM8783562 genotype",
    "paper": "siControl stretch rep1 (GEO title)",
    "data": "LMNA expression at siLMNA level; profile clusters with run-1 siLMNA static",
    "disposition": "sample_excluded"
  },
  {
    "item": "batch",
    "paper": "not mentioned",
    "data": "two sequencing runs on different instruments; siLMNA stretch only in run 2",
    "disposition": "handled_by_subset_and_sensitivity"
  },
  {
    "item": "GSM9181790 (ctrl1)",
    "paper": "not described",
    "data": "added to GEO Aug 2025, molecule polyA RNA vs total RNA for others; profile concordant with other siControl (r 0.989-0.996)",
    "disposition": "kept"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID41126185 / GSE289091

Paper: Lamin A/C protects chromatin accessibility during mechanical loading in human skeletal muscle (PMC12542426).
The exercise mimic is 4 h of equibiaxial cyclic stretch (10%, 0.5 Hz) applied to immortalized human myotubes (S2.3.p1). Abstract ABS.p2 calls it "mechanical stress mimicking acute muscle exercise". This is an in vitro model, not exercise in people.

## What ran

- `prep_merge_quant.py` merged the `NumReads` column of the 18 DRAGEN `*.quant.genes.sf.gz` files (Salmon format) in `GSE289091_RAW.tar` into `data/GSE289091/GSE289091_numreads_merged.csv`. Gene versions were stripped and the 44 `_PAR_Y` rows were dropped. The result is 60,607 genes x 18 samples.
- `case_spec.json` went through `python -m tools.case_runner execute`. The validator found 15 records and 0 errors, and the run status is completed. The route is `declared_deviation`.
- Alignment matched exactly on GSM ids. Derived columns: `geno` (Ctl/siLMNA), `cond` (static/stretch), `run` (r1 NovaSeq / r2 NextSeq), `grp`.
- Method: R DESeq2 LRT (`tools.r_de_tools:run_r_de`, engine deseq2), comparing full `~ cond` with reduced `~ 1` within each genotype. This is the paper's route (S2.6.p3). Estimated counts were rounded. Genes were kept if CPM >= 1 in at least 2 of each comparison's samples.
- Threshold: the paper contradicts itself. The Fig. 6 legend for the stretch volcanoes says log2FC > 0.5 & FDR < 0.05. The Methods (S2.6.p3) say |log2FC| > 1 & FDR < 0.05. Applied rule = Fig. 6 rule (`threshold_source: paper`). Audit rule = Methods rule.
- ORA (Enrichr GO/KEGG) ran on the up and down lists of the siLMNA primary table. GSEA was not run because the LRT statistic is unsigned.

## DEG counts vs paper (FDR < 0.05)

| Table | Samples (static/stretch) | Applied: abs(LFC) > 0.5 | Audit: abs(LFC) > 1 | Paper |
|---|---|---|---|---|
| ctl_stretch (primary) | 3 / 3, run 1 | 21 (20 up / 1 down) | 3 (3 / 0) | 7 |
| silmna_stretch_run2 (primary) | 4 / 4, run 2 | 2119 (1460 / 659) | 554 (429 / 125) | 634 (485 / 149) |
| silmna_stretch_all_runadj (sensitivity, ~run+cond) | 7 / 4 | 1963 (1325 / 638) | 564 (434 / 130) | 634 |
| silmna_stretch_all_naive (sensitivity, no batch term) | 7 / 4 | 1373 (742 / 631) | 296 (200 / 96) | 634 |

The paper's 634 = 485 up / 149 down is much closer to our Methods-rule (|log2FC| > 1) counts: 554 = 429 / 125 within run 2, and 564 with a run term. This suggests the paper actually applied |log2FC| > 1, not the 0.5 in the Fig. 6 legend.
 ... [2878 more characters]
