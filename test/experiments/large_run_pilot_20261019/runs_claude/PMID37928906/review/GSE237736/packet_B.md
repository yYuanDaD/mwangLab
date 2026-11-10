# Review packet B (the analysis' decisions): GSE237736

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pairwise/grp_KOrun_vs_KOsed | 3272 | 2857 | pvalue < 0.05 | 0 | 0 | 0 | 159 | 2857 | 207 | 29 | 879 | 0.052 | 0.219 |
| pairwise/grp_KOsed_vs_WTsed | 1230 | 1725 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 1725 | 129 | 18 | 295 | 0.06 | 0.132 |
| pairwise/grp_WTrun_vs_WTsed | 762 | 744 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 744 | 47 | 8 | 194 | 0.099 | 0.057 |
| pairwise/grp_KOrun_vs_WTsed | 1475 | 1048 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 1048 | 80 | 12 | 273 | 0.094 | 0.08 |
| pairwise/grp_KOrun_vs_WTrun | 494 | 317 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 317 | 18 | 4 | 53 | 0.13 | 0.024 |
| interaction/geno_x_run | 866 | 619 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 619 | 56 | 13 | 112 | 0.084 | 0.048 |
| pairwise_nofilter/grp_KOrun_vs_KOsed | 3272 | 3669 | pvalue < 0.05 | 0 | 0 | 0 | 154 | 3669 | 192 | 29 | 1198 | 0.088 | 0.181 |
| pairwise_nofilter/grp_KOsed_vs_WTsed | 1230 | 2206 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 2206 | 114 | 14 | 427 | 0.091 | 0.109 |
| pairwise_nofilter/grp_WTrun_vs_WTsed | 762 | 1174 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 1174 | 47 | 8 | 310 | 0.122 | 0.058 |
| pairwise_nofilter/grp_KOrun_vs_WTsed | 1475 | 1528 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 1528 | 77 | 10 | 427 | 0.114 | 0.075 |
| pairwise_nofilter/grp_KOrun_vs_WTrun | 494 | 713 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 713 | 18 | 4 | 141 | 0.143 | 0.035 |

## Samples per design level

### `grp`
- **KOrun** (4): GSM7646320 / dentate gyrus, running 12 day, rep13 KO / 13KORun; GSM7646321 / dentate gyrus, running 12 day, rep14 KO / 14KORun; GSM7646322 / dentate gyrus, running 12 day, rep15 KO / 15KORun; GSM7646323 / dentate gyrus, running 12 day, rep16 KO / 16KORun
- **KOsed** (4): GSM7646312 / dentate gyrus, sedentary, rep5 KO / 5KOnoRun; GSM7646313 / dentate gyrus, sedentary, rep6 KO / 6KOnoRun; GSM7646314 / dentate gyrus, sedentary, rep7 KO / 7KOnoRun; GSM7646315 / dentate gyrus, sedentary, rep8 KO / 8KOnoRun
- **WTrun** (4): GSM7646316 / dentate gyrus, running 12 day, rep9 WT / 9WTRun; GSM7646317 / dentate gyrus, running 12 day, rep10 WT / 10WTRun; GSM7646318 / dentate gyrus, running 12 day, rep11 WT / 11WTRun; GSM7646319 / dentate gyrus, running 12 day, rep12 WT / 12WTRun
- **WTsed** (4): GSM7646308 / dentate gyrus, sedentary, rep1 WT / 1WTnoRun; GSM7646309 / dentate gyrus, sedentary, rep2 WT / 2WTnoRun; GSM7646310 / dentate gyrus, sedentary, rep3 WT / 3WTnoRun; GSM7646311 / dentate gyrus, sedentary, rep4 WT / 4WTnoRun

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE237736"], "assay": "bulk RNA-seq (Illumina NovaSeq 6000), bilateral dentate gyrus, 12-month-old male C57BL/6 p16Ink4a WT and KO mice", "factors": {"genotype": ["p16 WT", "p16 KO"], "treatment": ["CTL (sedentary)", "RUN (12 days voluntary wheel running)"]}, "design": "2x2 factorial, n = 4 independent mice per group (S2.10.p1), 16 samples", "sample_inclusion": "all 16 deposited samples; no exclusions stated", "primary_estimand": "effect of 12 days of voluntary running on dentate gyrus gene expression in aged p16 KO mice (Set A, KO RUN vs KO CTL) and how it differs from WT (genotype x running interaction, GLM/LRT); running in WT (Set C) is the WT exercise effect", "planned_contrasts": ["Set A: KO RUN vs KO CTL (S3.1.p4; paper: 3,272 genes p<0.05)", "Set B: KO CTL vs WT CTL (S3.1.p4; paper: 1,230 genes p<0.05) - genotype, not exercise", "Set C: WT RUN vs WT CTL (S3.1.p4; paper: 762 genes p<0.05)", "Set D: KO RUN vs WT CTL (S3.1.p4; paper: 1,475 genes p<0.05)", "Set E: KO RUN vs WT RUN (S3.1.p4; paper: 494 genes p<0.05)", "GLM LRT genotype x treatment interaction (S2.5.p5, S3.4.1.p1; paper: 866 genes p<0.05)"], "paper_method": "htseq-count reads -> DESeq2 Wald test per pairwise comparison; DESeq2 LRT full (genotype + treatment + interaction) vs reduced (no interaction) for the GLM set (S2.5.p4, S2.5.p5, S2.10.p1)", "repeated_measure_unit": "none (independent animals)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": null, "effect_cutoff ... [263 more characters]

reasoning: S3.1.p3 states DE genes from DESeq2 Wald with significance threshold raw p-value < 0.05 (padj computed in S2.10.p1 but the counts in S3.1.p4 are at p<0.05). S3.1.p4 defines Sets A-E with counts. S2.5.p5/S3.4.1.p1 define the LRT interaction (866 genes). S2.10.p1 gives n = 4 per group.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\prep\\GSE237736_StringTie_FPKM_merged.csv", "owned": true, "checks": ["S2.5.p6 names GSE237736", "16 GSMs = 4 groups x 4 (S2.10.p1)", "GEO characteristics: dentate gyrus, one-year-old male, p16Ink4a +/+ and -/-, sedentary vs running 12 days, matching S2 and FIG1"], "accession": "GSE237736", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE237736\\GSE237736_metadata.csv"}

reasoning: The paper deposits exactly this series; sample annotations match the design. Matrix is the merge of the 16 per-sample StringTie gene_abundance files in GSE237736_RAW.tar (prep/merge_stringtie_fpkm.py).

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 16, "n_metadata": 16, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\aligned\\aligned_metadata.csv", "columns": {"geno": {"alias_of": "characteristics_ch1.4.genotype", "recode": {"p16Ink4a +/+": "WT", "p16Ink4a -/-": "KO"}}, "trt": {"alias_of": "characteristics_ch1.5.treatment", "recode": {"sedentary": "sed", "running 12 days": "run"}}, "grp": {"combine": ["geno", "trt"], "separator": "_", "of": "recoded values", "recode": {"WT_sed": "WTsed", "WT_run": "WTrun", "KO_sed": "KOsed", "KO_run": "KOrun"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\aligned\\design_metadata.csv", "sha256": "285383b8875d9312a783d5f1980050a1c45de05cf1368647a764dde62a6d03c8", "levels": {"geno": {"WT": 8, "KO": 8}, "trt": {"sed": 8, "run": 8}, "grp": {"WTsed": 4, "KOsed": 4, "WTrun": 4, "KOrun": 4}}}}

reasoning: Matrix columns are GSM ids taken from the tar member names; they equal the metadata index. Genotype and treatment come from the GEO characteristics; description (e.g. 1WTnoRun) agrees.

### matrix (valid, not_started)

final: {"matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\aligned\\aligned_matrix.csv", "sha256": "f239196d52479ed5754e1132b95ab9571a8c7eaeb80c908a500c8564e629b4bc", "n_features": 24421, "n_samples": 16, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2469.810791, "median": 1.3069410000000001, "integer_fraction": 0.2737, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Deposited files are StringTie gene_abundance tables with Coverage/FPKM/TPM columns only; GEO data_processing: 'tab-delimited text files include FPKM values for each Sample'. No htseq counts were deposited although the paper's DESeq2 used htseq-count reads (S2.5.p4). Using FPKM column, gene IDs summed over duplicate loci.

### design (valid, not_started)

final: {"analysis_type": "multilevel", "design_column": "grp", "formula": "~ 0 + C(grp)", "contrasts": [{"name": "grp_KOrun_vs_KOsed", "control": "KOsed", "treatment": "KOrun", "role": "primary", "paper_set": "A"}, {"name": "grp_WTrun_vs_WTsed", "control": "WTsed", "treatment": "WTrun", "role": "primary", "paper_set": "C"}, {"name": "grp_KOsed_vs_WTsed", "control": "WTsed", "treatment": "KOsed", "role": "secondary", "paper_set": "B (genotype, not exercise)"}, {"name": "grp_KOrun_vs_WTsed", "control": "WTsed", "treatment": "KOrun", "role": "secondary", "paper_set": "D (genotype and running combined)"}, {"name": "grp_KOrun_vs_WTrun", "control": "WTrun", "treatment": "KOrun", "role": "secondary", "paper_set": "E (genotype within runners)"}, {"name": "interaction_geno_x_run", "role": "secondary", "paper_set": "GLM LRT interaction"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\suitability\\suitability.md", "n_comparisons": 8, "n_analyzable": 8}}

reasoning: 2x2 factorial with n=4 independent mice per cell. The four cells are coded as one factor grp so all five pairwise Sets of S3.1.p4 come from one model; the exercise effects are Set A (running within KO) and Set C (running within WT). Sets B/D/E are genotype or mixed contrasts and are reproduced only for comparison with the paper. The interaction (S2.5.p5) is the 1-df contrast (KOrun-KOsed)-(WTrun-WTsed), equivalent in a 2x2 to the paper's LRT of full vs reduced model.

rejected alternatives: [{"value": "pool genotypes for RUN vs CTL", "reason_rejected": "paper never pools; genotype modifies the running effect (the study's central question)"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 16, "n_columns": 4, "columns": ["Intercept", "grp_KOsed", "grp_WTrun", "grp_WTsed"], "rank": 4, "full_rank": true, "residual_df": 12, "levels": {"grp": {"WTsed": 4, "KOsed": 4, "WTrun": 4, "KOrun": 4}}, "cells": [{"cell": ["KOrun"], "n": 4}, {"cell": ["KOsed"], "n": 4}, {"cell": ["WTrun"], "n": 4}, {"cell": ["WTsed"], "n": 4}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 16, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 16, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.age", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.Sex", "n_levels": 1, "status": "constant"}, {"co ... [2486 more characters]

reasoning: Independent animals, one sample each; all male, same age and tissue; no batch or lane recorded in GEO. No blocking unit.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (log2(FPKM+1), moderated t, one model ~ 0 + C(grp))", "formula": "~ 0 + C(grp)", "paper_route": {"method": "DESeq2 Wald / LRT on htseq-count reads", "status": "blocked", "reason": "only StringTie FPKM/TPM/Coverage tables deposited in GEO; no read counts; FPKM must not be rounded into counts"}, "deviations": ["limma on log2(FPKM+1) instead of DESeq2 on counts", "genes kept with FPKM >= 1 in >= 4 samples (one group) before fitting; the paper's DESeq2 used its own independent filtering", "interaction tested as 1-df limma contrast instead of DESeq2 LRT", "sensitivity run without the FPKM filter (pairwise_nofilter) for low-expressed paper genes"], "transform": "log2(x+1)"}

reasoning: Matrix-method policy: FPKM -> log2(x+1) -> limma. Paper route blocked (no counts).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "paper's raw p < 0.05 rule applied to limma p-values; BH padj < 0.05 reported as audit"}

reasoning: S3.1.p3: 'significance threshold ... set to p-value <0.05'; Set counts in S3.1.p4 and the 866 GLM genes (S3.4.1.p1) use p < 0.05. No fold-change cutoff.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "pairwise", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise\\DEG_results_grp_KOrun_vs_KOsed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise\\DEG_results_grp_KOsed_vs_WTsed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise\\DEG_results_grp_WTrun_vs_WTsed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise\\DEG_results_grp_KOrun_vs_WTsed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise\\DEG_results_grp_KOrun_vs_WTrun.csv"], "counts": {"pairwise/grp_KOrun_vs_KOsed": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13019, "n_significant": 2857, "n_up": 1500, "n_down": 1357, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13019, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "pairwise/grp_KOsed_vs_WTsed": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13019, "n_significant": 1725, "n_up": 740, "n_down": 985, "deg_sanity": "ok"}, "audit" ... [943 more characters]

reasoning: Sets A-E from one limma model on all 16 samples (exercise effects: A and C).

### execution (valid, completed)

final: {"method": "run_multigroup_analysis", "subset": "interaction", "role": "secondary", "tool": "tools.multigroup_tools:run_multigroup_analysis", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\interaction\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(grp)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\interaction\\DEG_results_geno_x_run.csv"], "counts": {"interaction/geno_x_run": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13019, "n_significant": 619, "n_up": 273, "n_down": 346, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13019, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Genotype x running interaction, analogue of the paper's GLM LRT (866 genes).

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "pairwise_nofilter", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise_nofilter\\DEG_results_grp_KOrun_vs_KOsed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise_nofilter\\DEG_results_grp_WTrun_vs_WTsed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise_nofilter\\DEG_results_grp_KOrun_vs_WTrun.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise_nofilter\\DEG_results_grp_KOsed_vs_WTsed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\pairwise_nofilter\\DEG_results_grp_KOrun_vs_WTsed.csv"], "counts": {"pairwise_nofilter/grp_KOrun_vs_KOsed": {"applied": {"rule": "pvalue < 0.05", "n_tested": 20287, "n_significant": 3669, "n_up": 2023, "n_down": 1646, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 20287, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "pairwise_nofilter/grp_WTrun_vs_WTsed": {"applied": {"rule": "pvalue < 0.05", "n_tested": 20287, "n_significant": ... [1035 more characters]

reasoning: Same model without the FPKM>=1 filter: the paper-validated genes (Tfap2c, Lepr, Top2a, Chrm5, Ccr1) have FPKM < 1 in this dentate gyrus and are removed by the primary filter; DESeq2 on counts would have tested them.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "pairwise/grp_KOrun_vs_KOsed", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\enrichment_pairwise_grp_KOrun_vs_KOsed\\ora\\DEG_results_grp_KOrun_vs_KOsed_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\enrichment_pairwise_grp_KOrun_vs_KOsed\\ora\\DEG_results_grp_KOrun_vs_KOsed_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\enrichment_pairwise_grp_KOrun_vs_KOsed\\ora\\DEG_results_grp_KOrun_vs_KOsed_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\enrichment_pairwise_grp_KOrun_vs_KOsed\\ora\\DEG_results_grp_KOrun_vs_KOsed_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 2857 Mouse genes (direction=all, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cytoplasmic Translation (GO:0002181) | padj=4.00e-43 | overlap=7 ... [1272 more characters]

reasoning: paper reports GO enrichment for running-regulated genes in KO (S3.6, Table 3)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "pairwise/grp_KOrun_vs_KOsed", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\enrichment_pairwise_grp_KOrun_vs_KOsed\\gsea\\DEG_results_grp_KOrun_vs_KOsed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13019 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 16 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_MITOTIC_SPINDLE | NES=1.72 | NOM p=0.00e+00 | FDR q=2.41e-02 - HALLMARK_G2M_CHECKPOINT | NES=1.36 | NOM p=2.18e-02 | FDR q=3.83e-01 - HALLMARK_MYOGENESIS | NES=1.36 | NOM p=2.90e-02 | FDR q=2.58e-01 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.32 | NOM p=4.39e-02 | FDR q=2.53e-01 - HALLMARK_APICAL_JUNCTION | NES=1.31 | NOM p=4.33e-02 | FDR q=2.21e-01 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.27 | NOM p=1.30e-01 | FDR q=2.41e-01 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.27 | NOM p=6.72e-02 | FDR q=2.11e-01 - HALLMARK_TGF_BETA_SIGNALING | NES=1.14 | NOM p=2.51e-01 | FDR q=4.72e-01 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.13 | NOM p=2.21e-01 | FDR q=4.25e-01 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=1.09 | NOM p=3.11e-01 | FDR q=4.80e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-3.07 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOL ... [417 more characters]

reasoning: paper reports GO enrichment for running-regulated genes in KO (S3.6, Table 3)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "pairwise/grp_WTrun_vs_WTsed", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37928906\\GSE237736\\results\\enrichment_pairwise_grp_WTrun_vs_WTsed\\gsea\\DEG_results_grp_WTrun_vs_WTsed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13019 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 21 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_TGF_BETA_SIGNALING | NES=1.80 | NOM p=0.00e+00 | FDR q=1.82e-02 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.72 | NOM p=0.00e+00 | FDR q=1.58e-02 - HALLMARK_MITOTIC_SPINDLE | NES=1.70 | NOM p=0.00e+00 | FDR q=1.33e-02 - HALLMARK_MYOGENESIS | NES=1.46 | NOM p=2.07e-03 | FDR q=1.43e-01 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.45 | NOM p=1.28e-02 | FDR q=1.19e-01 - HALLMARK_APICAL_JUNCTION | NES=1.44 | NOM p=1.72e-02 | FDR q=1.10e-01 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.42 | NOM p=7.04e-02 | FDR q=1.15e-01 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.38 | NOM p=2.22e-02 | FDR q=1.32e-01 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.36 | NOM p=2.50e-02 | FDR q=1.47e-01 - HALLMARK_KRAS_SIGNALING_UP | NES=1.32 | NOM p=5.23e-02 | FDR q=1.73e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_DNA_REPAIR | NES=-1.72 | NOM p=0.00e+00 | FDR q=2.66e-02 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-1.64 ... [417 more characters]

reasoning: exercise effect in WT; GSEA only (exploratory)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["paper's DESeq2-on-counts route is blocked: only FPKM deposited; limma on log2(FPKM+1) is a declared deviation", "raw p < 0.05 without multiplicity correction is the paper's rule; padj audit counts reported alongside", "n = 4 per group", "Sets B, D, E are genotype or mixed contrasts, not exercise effects"], "results": {"pairwise/grp_KOrun_vs_KOsed": {"n_deg": 2857, "up": 1500, "down": 1357, "rule": "pvalue < 0.05", "audit_n": 0}, "pairwise/grp_KOsed_vs_WTsed": {"n_deg": 1725, "up": 740, "down": 985, "rule": "pvalue < 0.05", "audit_n": 0}, "pairwise/grp_WTrun_vs_WTsed": {"n_deg": 744, "up": 399, "down": 345, "rule": "pvalue < 0.05", "audit_n": 0}, "pairwise/grp_KOrun_vs_WTsed": {"n_deg": 1048, "up": 539, "down": 509, "rule": "pvalue < 0.05", "audit_n": 0}, "pairwise/grp_KOrun_vs_WTrun": {"n_deg": 317, "up": 146, "down": 171, "rule": "pvalue < 0.05", "audit_n": 0}, "interaction/geno_x_run": {"n_deg": 619, "up": 273, "down": 346, "rule": "pvalue < 0.05", "audit_n": 0}, "pairwise_nofilter/grp_KOrun_vs_KOsed": {"n_deg": 3669, "up": 2023, "down": 1646, "rule": "pvalue < 0.05", "audit_n": 0}, "pairwise_nofilter/grp_WTrun_vs_WTsed": {"n_deg": 1174, "up": 639, "down": 535, "rule": "pvalue < 0.05", "audit_n": 0}, "pairwise_nofilter/grp_KOrun_vs_WTrun": {"n_deg": 713, "up": 389, "down": 324, "rule": "pvalue < 0.05", "audit_n": 0}, "pairwise_nofilter/grp_KOsed_vs_WTsed": {"n_deg": 2206, "up": 952, "down": 1254, "rule": "pvalue < 0.05", "audit_n ... [4809 more characters]

reasoning: Running effects (Set A, Set C) are the exercise estimands; paper-validated genes (S3.5.p2-p3; S3.5.p1) are looked up.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "input matrix",
    "paper": "htseq-count read counts into DESeq2 (S2.5.p4)",
    "data": "GEO has only StringTie gene_abundance FPKM/TPM tables",
    "disposition": "declared_deviation"
  },
  {
    "item": "interaction test",
    "paper": "DESeq2 LRT full vs reduced (S2.5.p5)",
    "data": "limma 1-df interaction contrast on log2 FPKM",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID37928906 / GSE237736

## What ran
- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`). Run status completed; decision-contract validator 15 records, 0 errors.
- Design: 2x2 factorial (p16 WT/KO x sedentary/12-day running), dentate gyrus, 12-month-old males, n = 4 per cell, 16 samples, aligned exactly on GSM ids (16/16).
- Matrix: GEO has only StringTie `gene_abundance` tables (FPKM/TPM/Coverage) in `_RAW.tar`; no htseq counts. `prep/merge_stringtie_fpkm.py` merged the FPKM column into `prep/GSE237736_StringTie_FPKM_merged.csv` (24,421 genes; 152 duplicate-locus gene IDs summed per gene).
- Method: limma on log2(FPKM+1), one model `~ 0 + C(grp)` on all 16 samples (`run_joint_limma`) for Sets A-E; genotype x running interaction as a 1-df limma contrast (`run_multigroup_analysis`) in place of the paper's DESeq2 LRT. Primary filter FPKM >= 1 in >= 4 samples (13,019 genes kept); a no-filter sensitivity run (`pairwise_nofilter`) as well.
- Exercise estimands: Set A (KO RUN vs KO CTL) and Set C (WT RUN vs WT CTL). Sets B, D and E are genotype or mixed contrasts, reproduced only for comparison.
- Enrichment: ORA plus GSEA Hallmark on Set A; GSEA on Set C.

## Threshold
The paper's rule is raw DESeq2 Wald p < 0.05 with no fold-change cutoff (S3.1.p3, S3.1.p4). It is applied to limma p-values (`paper_on_deviation_route`). The audit rule is BH padj < 0.05.

## DEG counts vs paper (p < 0.05)
| Set | paper | ours (filtered) | ours (no filter) | audit padj<0.05 |
|---|---|---|---|---|
| A KO RUN vs KO CTL | 3272 | 2857 | 3669 | 0 |
| B KO CTL vs WT CTL | 1230 | 1725 | 2206 | 0 |
| C WT RUN vs WT CTL | 762 | 744 | 1174 | 0 |
| D KO RUN vs WT CTL | 1475 | 1048 | 1528 | 0 |
| E KO RUN vs WT RUN | 494 | 317 | 713 | 0 |
| GLM interaction | 866 | 619 | n/a | 0 |

No gene passes BH 0.05 in any contrast. The smallest padj is 0.066, in Set A. Only the paper's uncorrected rule produces DEG lists, so these lists are mostly nominal.

Paper genes:
- The qPCR-validated Set A genes all have the paper's direction in the no-filter run, each at p < 0.05: Tfap2c, Lepr, Top2a, Slc18a2 and Lpin2 up; Rgs14, Ramp3 and Chrm5 down.
- Rgs14 log2FC is -0.375, against the paper's -0.38 (S3.9.2.p1).
- Tfap2c, Lepr, Top2a, Chrm5 and Ccr1 have FPKM < 1, so the primary filter removed them.
- The Set B genes Eif2ak2, Magt1, Ntsr2 and Slc16a1 are up at p < 0.005. Ccr1 is up at p = 0.07.

GSEA Hallmark: MITOTIC_SPINDLE is enriched in Set A (NES 1.72, FDR 0.024). Th ... [838 more characters]
