# Review packet B (the analysis' decisions): GSE132520

## Mechanical flags

- **unused_subject_like_column**: {"column": "source_name_ch1", "n_values": 4, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| main/grp_MMEX_vs_MMSED | 582 | 137 | padj < 0.05 | 137 | 100 | 43 | 211 | 1226 | 217 | 59 | 452 | 0.081 | 0.113 |
| main/grp_VVEX_vs_VVSED | 216 | 31 | padj < 0.05 | 31 | 28 | 17 | 53 | 1075 | 108 | 37 | 323 | 0.075 | 0.099 |

## Samples per design level

### `grp`
- **MMEX** (4): GSM3872552 / 2161-4_quad_ex_WT_of_MMVVg; GSM3872553 / 2161-9_quad_ex_WT_of_MMVVg; GSM3872554 / 2246-4_quad_ex_WT_of_MMVVg; GSM3872555 / 2297-3_quad_ex_WT_of_MMVVg
- **MMSED** (4): GSM3872548 / 2032-3_quad_sed_WT_of_MMVVg; GSM3872549 / 2074-1_quad_sed_WT_of_MMVVg; GSM3872550 / 2127-1_quad_sed_WT_of_MMVVg; GSM3872551 / 2127-3_quad_sed_WT_of_MMVVg
- **VVEX** (4): GSM3872560 / 2161-5_quad_ex_MMVVg; GSM3872561 / 2161-7_quad_ex_MMVVg; GSM3872562 / 2296-2_quad_ex_MMVVg; GSM3872563 / 2296-3_quad_ex_MMVVg
- **VVSED** (4): GSM3872556 / 2074-2_quad_sed_MMVVg; GSM3872557 / 2074-5_quad_sed_MMVVg; GSM3872558 / 2126-4_quad_sed_MMVVg; GSM3872559 / 2296-5_quad_sed_MMVVg

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE132520"], "assay": "bulk poly(A)+ RNA-seq, mouse quadriceps, NovaSeq 100 bp PE (S4.25.p1, S4.26.p1)", "sample_inclusion": "male mice 13-15 weeks; MM (WT littermate) and VV (CaMKIIgamma M281V/M282V knock-in); sedentary or single bout of submaximal treadmill exercise (350 m), muscle collected 3 h after exercise; mice not finishing the protocol excluded; n = 4 per group (S4.23.p1, FIG3 legend b)", "factors": {"genotype": ["MM (WT)", "VV"], "treatment": ["sedentary", "exercised"]}, "primary_estimand": "acute transcriptional response of quadriceps to one bout of submaximal exercise (exercised vs sedentary, 3 h post) within each genotype, MM (WT) and VV (S2.3.p1, FIG3 c)", "planned_contrasts": ["MM exercised vs MM sedentary (S2.3.p1; paper: 582 genes q < 0.05)", "VV exercised vs VV sedentary (S2.3.p1; paper: 216 genes q < 0.05, 180 shared with MM)", "MM exercised vs VV exercised (S2.3.p2, S4.26.p2; genes over 2 sigma fed to IPA, no q-value count reported)"], "repeated_measure_unit": "none; independent mice, one quadriceps each", "normalization": "Tophat -> Stringtie -> Cuffdiff v2.2.1 FPKM (GEO data_processing)", "paper_method": "Cuffdiff v2.2.1 per-genotype exercised vs sedentary (GEO data_processing; S4.26.p1 defers to Tables S2-4)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.3.p1; FIG3 legend c"}, "paper_results": {"MM_EX_vs_SED": 582, "VV_EX_vs_SED": 216, "overlap": 180}}

reasoning: S2.3.p1 states 582 genes (q < 0.05) changed by exercise in MM and 216 in VV; FIG3 legend c defines the FDR-adjusted q < 0.05 rule with no fold-change cutoff. S4.23.p1 gives the acute exercise protocol; S4.26.p1/S9.p1 name GSE132520. The method (Cuffdiff) comes from the GEO data_processing field because the paper defers to Tables S2-4. The 2-sigma rule (S4.26.p2) only selects genes for IPA and is not the DEG count rule.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE132520\\GSE132520_FPKM_Matrice_SkelMuscle.csv", "owned": true, "checks": ["S4.26.p1 and S9.p1 name GSE132520", "GEO: 16 male quadriceps samples, 4 WT/VV x sed/ex, matches FIG3 b n = 4 per group", "treatment_protocol matches S4.23.p1 (350 m submaximal run, 3 h rest)"], "accession": "GSE132520", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE132520\\GSE132520_metadata.csv"}

reasoning: Paper cites GSE132520 directly; sample count, tissue, sex, genotypes and protocol match.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 16, "n_metadata": 16, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\aligned\\aligned_metadata.csv", "columns": {"geno": {"alias_of": "characteristics_ch1.1.genotype/variation", "recode": {"Wildtype": "MM", "CaMK2gVV/CaMK2gVV": "VV"}}, "trt": {"alias_of": "characteristics_ch1.3.treatment", "recode": {"sedentary": "SED", "exercised": "EX"}}, "litter": {"source": "title", "regex": "^(\\d+)-\\d+_", "recode": {"2032": "L2032", "2074": "L2074", "2126": "L2126", "2127": "L2127", "2161": "L2161", "2246": "L2246", "2296": "L2296", "2297": "L2297"}}, "grp": {"combine": ["geno", "trt"], "separator": "_", "of": "recoded values", "recode": {"MM_SED": "MMSED", "MM_EX": "MMEX", "VV_SED": "VVSED", "VV_EX": "VVEX"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\aligned\\design_metadata.csv", "sha256": "99a211f5e2bb9f9a03b3b4cdb9b87e9246bea2d1be397ffcb2d6781752090c9f", "levels": {"geno": {"MM": 8, "VV": 8}, "trt": {"SED": 8, "EX": 8}, "litter": {"L2161": 4, "L2074": 3, "L2296": 3, "L2127": 2, "L2032": 1, "L2246": 1, "L2297": 1, "L2126": 1}, "grp": {"MMSED": 4, "MMEX": 4, "VVSED": 4, "VVEX": 4}}}}

reasoning: Matrix column names equal the GEO title exactly (inspect alignment_keys: title 16/16). Genotype and treatment come from the characteristics fields; titles agree (WT_of_MMVVg = Wildtype, quad_ex = exercised). The numeric title prefix (e.g. 2161) looks like a litter/cage ID and is derived only for the confounding report.

### matrix (valid, not_started)

final: {"source": "GSE132520_FPKM_Matrice_SkelMuscle.csv (converted from the deposited .xlsx)", "paper_input": "Cuffdiff on aligned reads (BAM), not deposited", "matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\aligned\\aligned_matrix.csv", "sha256": "107aafcf1ca1af9e13a8b612c0b1f617e718fbbbb24e0daa5a821a1070ce43de", "n_features": 18873, "n_samples": 16, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 32, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 28111.8, "median": 1.6400199999999998, "integer_fraction": 0.1773, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Values are non-integer (integer fraction 0.18 is zeros), range 0-28112, median 1.6; file name and data_processing (.xlsx file of FPKM values) say FPKM. No raw counts are deposited, so the Cuffdiff/count route is blocked.

### design (valid, not_started)

final: {"analysis_type": "multi-group (2x2 genotype x treatment as 4-level cell factor)", "design_column": "grp", "contrasts": [{"name": "grp_MMEX_vs_MMSED", "control": "MMSED", "treatment": "MMEX", "role": "primary"}, {"name": "grp_VVEX_vs_VVSED", "control": "VVSED", "treatment": "VVEX", "role": "primary"}, {"name": "grp_VVEX_vs_MMEX", "control": "MMEX", "treatment": "VVEX", "role": "exploratory"}, {"name": "grp_VVSED_vs_MMSED", "control": "MMSED", "treatment": "VVSED", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\suitability\\suitability.md", "n_comparisons": 7, "n_analyzable": 7}}

reasoning: The paper's estimand is the exercise response within each genotype (S2.3.p1, FIG3 c), so both within-genotype contrasts are planned and fitted from one 4-cell model on all 16 samples. The post-exercise genotype comparison (S2.3.p2) is run as exploratory because the paper only used a 2-sigma ranking for IPA and reports no count; the sedentary genotype comparison is exploratory (paper: PCA similar, FIG3 b).

rejected alternatives: [{"value": "pooled exercised vs sedentary across genotypes", "reason_rejected": "paper reports exercise effects separately per genotype; pooling mixes genotypes whose responses differ"}, {"value": "two separate per-genotype fits of 8 samples", "reason_rejected": "one joint model shares variance across 16 samples; differs only in variance pooling, recorded as a deviation from per-pair Cuffdiff runs"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "litter", "disposition": "rejected: not in the paper's design, spread unevenly across cells (many litters with 1-2 samples), would consume residual df"}], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 16, "n_columns": 4, "columns": ["Intercept", "grp_MMSED", "grp_VVEX", "grp_VVSED"], "rank": 4, "full_rank": true, "residual_df": 12, "levels": {"grp": {"MMSED": 4, "MMEX": 4, "VVSED": 4, "VVEX": 4}}, "cells": [{"cell": ["MMEX"], "n": 4}, {"cell": ["MMSED"], "n": 4}, {"cell": ["VVEX"], "n": 4}, {"cell": ["VVSED"], "n": 4}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "litter", "n_levels": 8, "status": "crossed", "crosstab": {"MMEX": {"L2032": 0, "L2074": 0, "L2126": 0, "L2127": 0, "L2161": 2, "L2246": 1, "L2296": 0, "L2297": 1}, "MMSED": {"L2032": 1, "L2074": 1, "L2126": 0, "L2127": 2, "L2161": 0, "L2246": 0, "L2296": 0, "L2297": 0}, "VVEX": {"L2032": 0, "L2074": 0, "L2126": 0, "L2127": 0, "L2161": 2, "L2246": 0, "L2296": 2, "L2297": 0}, "VVSED": {"L2032": 0, "L2074": 2, "L2126": 1, "L2127": 0, "L2161": 0, "L2246": 0, "L2296": 1, "L2297": 0}}}]}

reasoning: Independent mice, one muscle per mouse, no batch recorded in GEO or the paper. The title prefix may be a litter ID; it is reported in the confounding check but not modelled because the paper does not block on it.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (limma-trend on log2(FPKM+1))", "formula": "~ 0 + grp", "paper_route": {"method": "Cuffdiff v2.2.1 on aligned reads", "status": "blocked", "reason": "only FPKM deposited; no BAM or count matrix in GEO, and FPKM must not be rounded into counts"}, "deviations": ["limma on log2(FPKM+1) instead of Cuffdiff", "one joint 4-cell model instead of per-pair Cuffdiff runs", "low-expression filter FPKM >= 1 in >= 4 samples (stands in for Cuffdiff not testing low-expressed genes)"], "transform": "log2(x+1)"}

reasoning: Matrix policy: FPKM -> log2(x+1) -> limma. Cuffdiff cannot run without reads. A FPKM >= 1 in at least 4 samples (one group size) filter removes near-zero genes that Cuffdiff would not test; a no-filter sensitivity run is added.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Paper's FDR q < 0.05 (Cuffdiff q-value, BH) applied to limma BH-adjusted p."}

reasoning: S2.3.p1 and FIG3 legend c: FDR-adjusted q < 0.05, no fold-change cutoff.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "main", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\main\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\main\\DEG_results_grp_MMEX_vs_MMSED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\main\\DEG_results_grp_VVEX_vs_VVSED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\main\\DEG_results_grp_VVEX_vs_MMEX.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\main\\DEG_results_grp_VVSED_vs_MMSED.csv"], "counts": {"main/grp_MMEX_vs_MMSED": {"applied": {"rule": "padj < 0.05", "n_tested": 10879, "n_significant": 137, "n_up": 118, "n_down": 19, "deg_sanity": "ok"}}, "main/grp_VVEX_vs_VVSED": {"applied": {"rule": "padj < 0.05", "n_tested": 10879, "n_significant": 31, "n_up": 28, "n_down": 3, "deg_sanity": "ok"}}, "main/grp_VVEX_vs_MMEX": {"applied": {"rule": "padj < 0.05", "n_tested": 10879, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "main/grp_VVSED_vs_MMSED": {"applied": {"rule": "padj < 0.05", "n_tested": 10879, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: One limma model ~0+grp on all 16 samples; the two within-genotype exercise contrasts are the paper's planned estimands; the genotype contrasts are exploratory.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "nofilter", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\nofilter\\DEG_results_grp_MMEX_vs_MMSED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\nofilter\\DEG_results_grp_VVEX_vs_VVSED.csv"], "counts": {"nofilter/grp_MMEX_vs_MMSED": {"applied": {"rule": "padj < 0.05", "n_tested": 18460, "n_significant": 106, "n_up": 87, "n_down": 19, "deg_sanity": "ok"}}, "nofilter/grp_VVEX_vs_VVSED": {"applied": {"rule": "padj < 0.05", "n_tested": 18460, "n_significant": 16, "n_up": 14, "n_down": 2, "deg_sanity": "ok"}}}}

reasoning: Same model without the low-expression filter, to show how much the filter changes the counts.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "main/grp_MMEX_vs_MMSED", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\enrichment_main_grp_MMEX_vs_MMSED\\ora\\DEG_results_grp_MMEX_vs_MMSED_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\enrichment_main_grp_MMEX_vs_MMSED\\ora\\DEG_results_grp_MMEX_vs_MMSED_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\enrichment_main_grp_MMEX_vs_MMSED\\ora\\DEG_results_grp_MMEX_vs_MMSED_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\enrichment_main_grp_MMEX_vs_MMSED\\ora\\DEG_results_grp_MMEX_vs_MMSED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 137 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Response To Unfolded Protein (GO:0006986) | padj=6.28e-04 | overlap=6/44 | genes=ERN1;DNAJB4;HSPB7 ... [1241 more characters]

reasoning: paper reports pathway (IPA) results for the MM exercise response (FIG3 f)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "main/grp_MMEX_vs_MMSED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\enrichment_main_grp_MMEX_vs_MMSED\\gsea\\DEG_results_grp_MMEX_vs_MMSED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 10879 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 35 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.88 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.68 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.66 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=2.60 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.36 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL2_STAT5_SIGNALING | NES=2.32 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.32 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APOPTOSIS | NES=2.24 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_P53_PATHWAY | NES=2.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COMPLEMENT | NES=2.19 | NOM p=0.00e+00 | FDR q=0.00e+00 ### Top 8 DOWN (NES < 0, depleted in treatment): - HALLMARK_SPERMATOGENESIS | NES=-1.29 | NOM p=1.05e-01 | FDR q=6.32e-01 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-1.15 | NOM p=1.65e-01 | FDR q=8.29e ... [406 more characters]

reasoning: paper reports pathway (IPA) results for the MM exercise response (FIG3 f)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "main/grp_VVEX_vs_VVSED", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\enrichment_main_grp_VVEX_vs_VVSED\\ora\\DEG_results_grp_VVEX_vs_VVSED_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\enrichment_main_grp_VVEX_vs_VVSED\\ora\\DEG_results_grp_VVEX_vs_VVSED_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\enrichment_main_grp_VVEX_vs_VVSED\\ora\\DEG_results_grp_VVEX_vs_VVSED_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\enrichment_main_grp_VVEX_vs_VVSED\\ora\\DEG_results_grp_VVEX_vs_VVSED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 31 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cellular Response To Chemical Stress (GO:0062197) | padj=1.95e-03 | overlap=4/89 | genes=SRXN1;PPAR ... [1241 more characters]

reasoning: paper reports pathway (IPA) results for the VV exercise response (FIG3 g)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "main/grp_VVEX_vs_VVSED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34039988\\GSE132520\\results\\enrichment_main_grp_VVEX_vs_VVSED\\gsea\\DEG_results_grp_VVEX_vs_VVSED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 10879 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 23 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.90 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=2.50 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_P53_PATHWAY | NES=2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APOPTOSIS | NES=1.91 | NOM p=0.00e+00 | FDR q=5.48e-03 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.75 | NOM p=0.00e+00 | FDR q=2.05e-02 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.72 | NOM p=7.94e-03 | FDR q=2.07e-02 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.71 | NOM p=0.00e+00 | FDR q=1.77e-02 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.65 | NOM p=0.00e+00 | FDR q=2.83e-02 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.58 | NOM p=5.09e-02 | FDR q=3.73e-02 - HALLMARK_MYOGENESIS | NES=1.55 | NOM p=0.00e+00 | FDR q=3.94e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-1.42 | NOM p=7.22e-03 | FDR q=4.72e-01 - HALLMARK_PEROXISOME | NES=-1.37 | NOM p=4.18e-02 | FD ... [406 more characters]

reasoning: paper reports pathway (IPA) results for the VV exercise response (FIG3 g)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Cuffdiff route blocked (FPKM only); limma-trend counts are not expected to equal Cuffdiff counts", "IPA 2-sigma gene lists and IPA pathway results are not reproduced", "n = 4 per group"], "results": {"main/grp_MMEX_vs_MMSED": {"n_deg": 137, "up": 118, "down": 19, "rule": "padj < 0.05"}, "main/grp_VVEX_vs_VVSED": {"n_deg": 31, "up": 28, "down": 3, "rule": "padj < 0.05"}, "main/grp_VVEX_vs_MMEX": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "main/grp_VVSED_vs_MMSED": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "nofilter/grp_MMEX_vs_MMSED": {"n_deg": 106, "up": 87, "down": 19, "rule": "padj < 0.05"}, "nofilter/grp_VVEX_vs_VVSED": {"n_deg": 16, "up": 14, "down": 2, "rule": "padj < 0.05"}}, "paper_counts": {"main/grp_MMEX_vs_MMSED": 582, "main/grp_VVEX_vs_VVSED": 216}, "comparison": {"main/grp_MMEX_vs_MMSED": {"ours": 137, "paper": 582}, "main/grp_VVEX_vs_VVSED": {"ours": 31, "paper": 216}}, "paper_gene_check": {}}

reasoning: Paper counts from S2.3.p1; the paper names no individual DEGs in the text.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "Cuffdiff v2.2.1 on reads (GEO data_processing)",
    "data": "only FPKM matrix deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "missing values",
    "paper": "not discussed",
    "data": "32 NaN cells in 8 rows of the FPKM matrix (one row named gene)",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID34039988 / GSE132520

## What ran
- Case spec route (`case_spec.json`), executed twice. The first attempt's primary execution failed on comparison names and was moved to `_previous/`. The second run completed, and the contract validator reported 15 records with 0 errors.
- Data: `GSE132520_FPKM_Matrice_SkelMuscle.csv`, 18,873 genes x 16 samples. Samples were aligned exactly on the GEO `title` (16/16).
- Design: 2x2 genotype (MM = WT, VV = CaMKIIgamma M281V/M282V) x treatment (sedentary, one bout of submaximal treadmill exercise with collection 3 h later), n = 4 per cell. The four cells form one factor, `grp`.
- Method: limma-trend on log2(FPKM+1), one model `~ 0 + grp` on all 16 samples. Genes were kept if FPKM >= 1 in >= 4 samples (10,879 kept). A sensitivity run with no filter was also done.
- Enrichment: ORA (GO/KEGG) and GSEA (Hallmark) on both exercise contrasts; all completed.

## DEG counts vs paper (paper threshold: FDR q < 0.05, no fold-change cutoff; S2.3.p1, FIG3c)

| Contrast | Ours (filtered) up/down | Ours (no filter) | Paper |
|---|---|---|---|
| MM exercised vs sedentary (planned) | 137 (118/19) | 106 | 582 |
| VV exercised vs sedentary (planned) | 31 (28/3) | 16 | 216 |
| Shared between MM and VV | 29 of 31 VV DEGs (94%) | | 180 of 216 (83%) |
| VV vs MM, exercised (exploratory) | 0 | | not counted (the paper used a 2-sigma list for IPA) |
| VV vs MM, sedentary (exploratory) | 0 | | not counted (the paper reports similar PCA) |

Qualitatively the paper's main finding is reproduced:
- The exercise response is much larger in MM than in VV.
- Nearly all VV DEGs are also MM DEGs.
- The top MM genes are classic acute-exercise genes: Atf3, Nr4a3, Xirp1, Srxn1, Csrp3.
- Hallmark GSEA top terms are inflammatory in both genotypes (TNFA_SIGNALING_VIA_NFKB, IL6_JAK_STAT3, hypoxia), matching the inflammation emphasis of the paper's IPA (FIG3f).

Absolute counts are about 4x (MM) and 7x (VV) lower than the paper's.

## Deviations
- **Paper route blocked.** The paper used Cuffdiff v2.2.1 on reads (from the GEO data_processing field), but only FPKM was deposited. limma-trend on log2(FPKM+1) ran instead as a declared deviation, with threshold source `paper_on_deviation_route`. Cuffdiff is typically more liberal than limma at n = 4, which likely explains much of the count gap.
- **One joint model.** We fit one 4-cell model; Cuffdiff ran a separate comparison per genotype.
- **Low-expression filter.** The FPKM >= 1 in >= 4 samples rule is ou ... [1335 more characters]
