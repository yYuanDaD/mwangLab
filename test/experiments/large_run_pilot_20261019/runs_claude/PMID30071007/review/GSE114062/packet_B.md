# Review packet B (the analysis' decisions): GSE114062

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the source_name_ch1 level", "across": "source_name_ch1", "pairs_or_sets": 7, "samples_linked": 14, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| edgeR_QL/line_region_Hi_St_vs_Co_Ce | 86 | 75 | padj < 0.05 | 75 | 54 | 34 | 169 | 1441 | 399 | 151 | 525 | 0.09 | 0.095 |

## Samples per design level

### `line`
- **Co** (8): GSM3131807 / cerebellum_Control_0; GSM3131808 / cerebellum_Control_1; GSM3131809 / cerebellum_Control_2; GSM3131810 / cerebellum_Control_3; GSM3131815 / striatum_Control_0; GSM3131816 / striatum_Control_1; GSM3131817 / striatum_Control_2; GSM3131818 / striatum_Control_3
- **Hi** (7): GSM3131811 / cerebellum_Selected_0; GSM3131812 / cerebellum_Selected_1; GSM3131813 / cerebellum_Selected_2; GSM3131814 / cerebellum_Selected_3; GSM3131819 / striatum_Selected_0; GSM3131820 / striatum_Selected_1; GSM3131821 / striatum_Selected_2

### `region`
- **Ce** (8): GSM3131807 / cerebellum_Control_0; GSM3131808 / cerebellum_Control_1; GSM3131809 / cerebellum_Control_2; GSM3131810 / cerebellum_Control_3; GSM3131811 / cerebellum_Selected_0; GSM3131812 / cerebellum_Selected_1; GSM3131813 / cerebellum_Selected_2; GSM3131814 / cerebellum_Selected_3
- **St** (7): GSM3131815 / striatum_Control_0; GSM3131816 / striatum_Control_1; GSM3131817 / striatum_Control_2; GSM3131818 / striatum_Control_3; GSM3131819 / striatum_Selected_0; GSM3131820 / striatum_Selected_1; GSM3131821 / striatum_Selected_2

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE114062"], "assay": "bulk RNA-seq (Illumina HiSeq 2000, 100 nt PE), cerebellum and striatum, male Hsd:ICR mice, generation 66 of a selection experiment", "primary_estimand": "Associational difference in brain gene expression between a line selectively bred for high voluntary wheel running (Hi, line 7) and a non-selected control line (Co, line 1), within cerebellum (CeHi-CeCo) and striatum (StHi-StCo), plus the line-by-region interaction. All mice had 6 days of wheel access before sampling, so the contrast is genetic line (dominated by 66 generations of selection) with the running amount co-varying; it is not a randomized exercise intervention (S2.1.p3, S4.p3).", "factors": {"line": ["Co (control line 1)", "Hi (high-runner line 7)"], "region": ["Ce (cerebellum)", "St (striatum)"]}, "sample_inclusion": "16 samples (4 per line-region cell); one StHi sample removed as PCA outlier (S2.2.p1) -> 15 analysed; GEO deposits exactly these 15.", "planned_contrasts": ["CeHi vs CeCo within cerebellum (S2.2.p2; Table 1/Table 3; reported as CeCo-CeHi)", "StHi vs StCo within striatum (S2.2.p2; Table 1/Table 4; reported as StCo-StHi)", "line-by-region interaction (S2.2.p2, S3.2.p1: 86 genes at FDR < 0.05; 334 at raw P < 0.005)", "StHi vs CeHi (third orthogonal contrast, S2.2.p2; no count reported)", "main effect of line Hi vs Co across regions (S2.2.p2, S3.6.p1; Table 5; 144 genes |log2FC|>1 in Table E, 122 genes after removing interaction genes; p rule not stated)", "main e ... [901 more characters]

reasoning: Study map from S2.1.p1-p4 (design, 2x2 factorial, line 7 vs line 1, wheel access for all), S2.2.p1 (samples, filter, outlier removal), S2.2.p2 (edgeR QL model and contrasts), S3.2.p1 (FDR < 0.05 significance rule, 86 interaction genes), S3.6.p1/Table 5 (line main effect), S3.7.p1 (region effect). The paper's tables report Co minus Hi (log2(Co/Hi)); this run reports Hi vs Co, so signs are flipped when comparing.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE114062\\GSE114062_Cere_Stri_FPKM.csv.gz", "owned": true, "checks": ["S2.1.p4 and S6.p1 name GSE114062", "GEO: Mus musculus Hsd:ICR, male, cerebellum and striatum, Control vs Selected, contact Rodriguez Zas (UIUC) = paper's group", "15 GSM samples = 16 minus the removed StHi outlier (S2.2.p1): striatum Selected has 3 samples", "matrix GSE114062_Cere_Stri_FPKM.csv.gz has exactly the 15 sample titles"], "accession": "GSE114062", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE114062\\GSE114062_metadata.csv"}

reasoning: Accession named in the paper; organism, strain, sex, tissues, conditions and sample count match the paper's design after the documented outlier removal.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 15, "n_metadata": 15, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\aligned\\aligned_metadata.csv", "columns": {"region": {"source": "title", "regex": "^(cerebellum|striatum)_", "recode": {"cerebellum": "Ce", "striatum": "St"}}, "line": {"source": "title", "regex": "_(Control|Selected)_\\d+$", "recode": {"Control": "Co", "Selected": "Hi"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\aligned\\design_metadata.csv", "sha256": "95871d966ceed328757ba129d703b6e72eac835d84b7e466285a82644f6b0d9e", "levels": {"region": {"Ce": 8, "St": 7}, "line": {"Co": 8, "Hi": 7}}}}

reasoning: Matrix column names equal the metadata title for all 15 samples (inspect alignment_keys: title 15/15). line and region are parsed from the title and agree with characteristics condition/tissue; recoded to the paper's labels Co/Hi and Ce/St.

### matrix (valid, not_started)

final: {"source": "GSE114062_Cere_Stri_FPKM.csv.gz (only deposited matrix)", "paper_input": "Cuffnorm library-size-normalized gene counts, then TMM in edgeR (S2.2.p1)", "matrix_type": "size-factor-scaled fragment counts (Cuffnorm count table; the file name says otherwise, see reasoning)", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\aligned\\aligned_matrix.csv", "sha256": "a35165a2835f763d37cd170aa70f761270a3c2fff4b77f2313d9686dffa3043f", "n_features": 26628, "n_samples": 15, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 255767.0, "median": 82.49135, "integer_fraction": 0.284, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Despite the FPKM label, column sums are 38-44 million per sample (FPKM sums would not track fragment totals like this), and within each sample the non-zero values are integer multiples of one per-sample unit (e.g. 0.891534, 0.931986; 0.84-1.30, the mode value occurring ~900 times = one fragment): 81-96% of non-zero values are within 0.01 of an integer multiple, the rest are large values limited by 6-significant-digit printing. This is the Cuffnorm genes.count_table (counts scaled by geometric-mean size factors), which matches the paper's stated input (S2.2.p1 'Cuffnorm ... normalize the gene counts for library size'). Count-scale values on a near-unit scale are suitable for edgeR, which acce ... [43 more characters]

rejected alternatives: [{"value": "FPKM (linear normalized) -> log2(x+1) + limma", "reason_rejected": "values are quantized fragment counts with column sums ~ total fragments, not length-normalized FPKM; the paper analysed them with edgeR"}, {"value": "reconstruct raw integer counts by dividing by the per-sample unit", "reason_rejected": "possible but not the paper's input; size factors 0.84-1.30 change the NB scale little; noted as a possible sensitivity check"}]

### design (valid, not_started)

final: {"analysis_type": "factorial 2x2 (line x region), one model on all 15 samples", "estimand_type": "associational", "formula": "~ line * region", "contrasts": [{"name": "line_Hi_vs_Co_region-Ce", "expression": "lineHi", "role": "primary"}, {"name": "line_Hi_vs_Co_region-St", "expression": "lineHi + lineHi.regionSt", "role": "primary"}, {"name": "line_region_Hi_St_vs_Co_Ce", "expression": "lineHi.regionSt", "role": "primary"}, {"name": "line_Hi_vs_Co_avg", "expression": "lineHi + 0.5*lineHi.regionSt", "role": "secondary"}, {"name": "region_St_vs_Ce_HiLine", "expression": "regionSt + lineHi.regionSt", "role": "secondary"}, {"name": "region_St_vs_Ce_avg", "expression": "regionSt + 0.5*lineHi.regionSt", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: S2.1.p1 and S2.2.p1-p2 define a 2x2 factorial (activity line x brain region) fitted in one edgeR model with the interaction. The exercise-relevant estimand is Hi vs Co line within each region and the line-by-region interaction (S2.2.p2: 'patterns of particular interest'); the line main effect and the third orthogonal contrast StHi-CeHi plus the region main effect are secondary, as in the paper. The comparison is associational (selected line vs control line, both with wheel access; S2.1.p3, S4.p3), not a randomized exercise effect. Main effects are taken as averages over the other factor's levels because the model contains the interaction.

rejected alternatives: [{"value": "separate two-group fits per region", "reason_rejected": "the paper fits one model with interaction; the interaction needs both regions in one model"}, {"value": "pool regions and compare lines only (~ line)", "reason_rejected": "region is a dominant factor and the paper's primary interest is region-dependent line effects"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "animal (possible Ce/St from the same mouse)", "disposition": "not modelled: no animal ID in GEO; paper fits no animal term"}, {"name": "locomotor measures", "disposition": "excluded per paper (S2.2.p2): between-line variation dominates, no covariate"}], "design_check": {"formula_equivalent": "~ C(line) + C(region)", "n_samples": 15, "n_columns": 3, "columns": ["Intercept", "line_Hi", "region_St"], "rank": 3, "full_rank": true, "residual_df": 12, "levels": {"line": {"Co": 8, "Hi": 7}, "region": {"Ce": 8, "St": 7}}, "cells": [{"cell": ["Co", "Ce"], "n": 4}, {"cell": ["Co", "St"], "n": 4}, {"cell": ["Hi", "Ce"], "n": 4}, {"cell": ["Hi", "St"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "region", "n_levels": 2, "status": "crossed", "crosstab": {"Co": {"Ce": 4, "St": 4}, "Hi": {"Ce": 4, "St": 3}}}]}

reasoning: All mice are male, same age and generation; no batch or RIN column in GEO. S2.2.p2 states no covariate was included. Whether cerebellum and striatum came from the same 8 mice is not stated (S2.2.p1 '16 individual mouse samples'); GEO has no animal key, and the paper's model has none, so no blocking. Within-region line contrasts compare different animals either way; if regions were paired, region and interaction tests would be conservative-to-misestimated, which is recorded as a caveat.

### method (valid, not_started)

final: {"matrix_type": "size-factor-scaled fragment counts (Cuffnorm count table; the file name says otherwise, see reasoning)", "method": "edgeR QL F-test (R edgeR glmQLFit/glmQLFTest, robust), TMM", "formula": "~ line * region", "paper_route": {"method": "edgeR 3.14.0 QL F-test, robust tagwise dispersion, ~ line*region", "status": "reproduced", "reason": "same model and test; edgeR version 4.10.7 here vs 3.14.0 in the paper"}, "deviations": ["edgeR 4.10.7 (R 4.6) instead of 3.14.0 (R 3.3.1); glmQLFit defaults changed in edgeR 4 (legacy=FALSE)", "low-count filter (>= 1 CPM in >= 3 samples) applied on the deposited normalized counts"]}

reasoning: The paper's method (S2.2.p2) runs directly on the deposited count-scale matrix through tools.r_de_tools engine edger_ql (estimateDisp robust, glmQLFit robust, glmQLFTest per contrast, BH FDR). Contrasts are model-column vectors over ~ line * region with Co and Ce as references.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.005, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Audit rule raw P < 0.005 reproduces the paper's extended interaction list (Table A, 334 genes; S3.2.p1). Table 1 (FDR < 0.01, |log2FC| > 1.25), Table 5 (FDR < 0.01, |log2FC| > 4) and Table 6 are display filters, not DEG definitions."}

reasoning: S3.2.p1: significance is 'FDR-adjusted P-value < 0.05' (86 interaction genes); no fold-change rule in the DEG definition.

### execution (valid, completed)

final: {"method": "edgeR QL F-test (R), TMM, ~ line * region", "subset": "edgeR_QL", "role": "primary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 15, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\edgeR_QL\\input\\matrix_filtered.csv", "formula": "~ line * region", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\edgeR_QL\\DEG_results_line_Hi_vs_Co_region-Ce.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\edgeR_QL\\DEG_results_line_Hi_vs_Co_region-St.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\edgeR_QL\\DEG_results_line_region_Hi_St_vs_Co_Ce.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\edgeR_QL\\DEG_results_line_Hi_vs_Co_avg.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\edgeR_QL\\DEG_results_region_St_vs_Ce_HiLine.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\edgeR_QL\\DEG_results_region_St_vs_Ce_avg.csv"], "counts": {"edgeR_QL/line_Hi_vs_Co_region-Ce": {"applied": {"rule": "padj < 0.05", "n_tested": 15213, "n_significant": 964, "n_up": 452, "n_down": 512, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.005", "n_tested": 15213, "n_significant": 1149, "n_up": 539, "n_down": 610, "deg_sanity": "ok"}}, " ... [1605 more characters]

reasoning: Paper's edgeR QL model with interaction (S2.2.p2) and CPM filter (S2.2.p1); all six paper contrasts from one fit.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "edgeR_QL/line_Hi_vs_Co_region-Ce", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\enrichment_edgeR_QL_line_Hi_vs_Co_region-Ce\\gsea\\DEG_results_line_Hi_vs_Co_region-Ce_GSEA_Hallmark.csv"], "summary": "GSEA complete on 15213 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 21 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.23 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.94 | NOM p=0.00e+00 | FDR q=6.72e-03 - HALLMARK_ADIPOGENESIS | NES=1.93 | NOM p=0.00e+00 | FDR q=4.48e-03 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.88 | NOM p=2.17e-03 | FDR q=4.58e-03 - HALLMARK_MTORC1_SIGNALING | NES=1.65 | NOM p=0.00e+00 | FDR q=2.81e-02 - HALLMARK_PEROXISOME | NES=1.55 | NOM p=1.55e-02 | FDR q=5.34e-02 - HALLMARK_BILE_ACID_METABOLISM | NES=1.42 | NOM p=4.44e-02 | FDR q=1.21e-01 - HALLMARK_GLYCOLYSIS | NES=1.36 | NOM p=1.84e-02 | FDR q=1.72e-01 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.30 | NOM p=5.21e-02 | FDR q=2.39e-01 - HALLMARK_MYC_TARGETS_V1 | NES=1.28 | NOM p=4.92e-02 | FDR q=2.41e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-1.58 | NOM p=1.36e-02 | FDR q=1.40e-01 - HALLMARK_G2M_CHECKPOINT |  ... [432 more characters]

reasoning: S2.3.p1/Table 3: GSEA on the CeHi-CeCo ranking (paper used GO/KEGG; repository uses MSigDB Hallmark)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "edgeR_QL/line_Hi_vs_Co_region-St", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\enrichment_edgeR_QL_line_Hi_vs_Co_region-St\\gsea\\DEG_results_line_Hi_vs_Co_region-St_GSEA_Hallmark.csv"], "summary": "GSEA complete on 15213 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 13 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_ADIPOGENESIS | NES=1.89 | NOM p=0.00e+00 | FDR q=1.88e-02 - HALLMARK_BILE_ACID_METABOLISM | NES=1.78 | NOM p=1.96e-03 | FDR q=2.87e-02 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.76 | NOM p=0.00e+00 | FDR q=2.21e-02 - HALLMARK_P53_PATHWAY | NES=1.65 | NOM p=4.00e-03 | FDR q=3.70e-02 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.62 | NOM p=4.07e-03 | FDR q=3.95e-02 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.44 | NOM p=1.93e-02 | FDR q=1.33e-01 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.41 | NOM p=1.46e-02 | FDR q=1.45e-01 - HALLMARK_PEROXISOME | NES=1.37 | NOM p=5.09e-02 | FDR q=1.65e-01 - HALLMARK_COAGULATION | NES=1.36 | NOM p=5.39e-02 | FDR q=1.56e-01 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.29 | NOM p=1.06e-01 | FDR q=2.21e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_PANCREAS_BETA_CELLS | NES=-1.53 | NOM p=3.43e-02 | FDR q=2.40e-01 - HALLMARK_PROTEIN_SECRETION | NES=-1.49 | ... [432 more characters]

reasoning: S2.3.p1/Table 4: GSEA on the StHi-StCo ranking

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "edgeR_QL/line_region_Hi_St_vs_Co_Ce", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\enrichment_edgeR_QL_line_region_Hi_St_vs_Co_Ce\\ora\\DEG_results_line_region_Hi_St_vs_Co_Ce_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\enrichment_edgeR_QL_line_region_Hi_St_vs_Co_Ce\\ora\\DEG_results_line_region_Hi_St_vs_Co_Ce_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\enrichment_edgeR_QL_line_region_Hi_St_vs_Co_Ce\\ora\\DEG_results_line_region_Hi_St_vs_Co_Ce_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID30071007\\GSE114062\\results\\enrichment_edgeR_QL_line_region_Hi_St_vs_Co_Ce\\ora\\DEG_results_line_region_Hi_St_vs_Co_Ce_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 75 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p):  ... [1342 more characters]

reasoning: S2.3.p1/Table 2: functional enrichment (DAVID in the paper) of interaction genes; here Enrichr GO/KEGG ORA at the applied threshold

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Associational: selected high-runner line vs control line, both given 6 days of wheel access; differences reflect genetic selection plus differing running amounts and cannot be read as an effect of exercise per se (S4.p3).", "Direction conflict with the paper's text: our Hi-vs-Co log2FC within region equals the paper's Table 1 'CeCo-CeHi'/'StCo-StHi' values with the SAME sign (Npsr1 Ce -6.47, Vdr -3.37, Pcsk9 +3.21, Krt25 Ce -1.98 / St +3.02, Cd300lf St -4.23), so Table 1 columns are numerically Hi minus Co under the GEO Control/Selected labels. The paper's text reads them as Co minus Hi and therefore states the opposite direction: e.g. it says Npsr1, Vdr, Necab1 and Cd300lf are over-expressed in Hi and Npy/Pcsk9 under-expressed in Hi (S3.2.p3-p6), whereas the data show Npsr1/Vdr/Necab1/Cd300lf lower and Npy/Pcsk9 higher in Selected; Spp1 is higher (not lower) in St of Selected (S3.5.p2).", "Table 5 (log2(Co/Hi)) agrees in sign with the data (Ms4a2 Co/Hi +8.20 = our Hi-vs-Co -8.20; Cyp11a1 higher in Hi as the text says), so the GEO line labels appear correct and the Table 1 header/text sign is the paper's inconsistency.", "GSEA (Hallmark here, GO/KEGG in the paper): oxidative phosphorylation is enriched among genes HIGHER in the Selected line in both regions (NES +2.23 Ce, +1.76 St); the paper's text says oxidative phosphorylation is over-expressed in Co relative to Hi (S3.4.p3). Same sign problem as Table 1; recorded, not resolved.", "N ... [5766 more characters]

reasoning: Paper's model, test, filter and threshold reproduced on the deposited matrix; only the interaction has a paper count under the FDR < 0.05 rule. Within-region line counts are only in S1 Figure A (not available); line main-effect counts (144/122) use an unstated p rule with |log2FC| > 1.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix label",
    "paper": "Cuffnorm normalized gene counts analysed in edgeR",
    "data": "file named FPKM; values are size-factor-scaled fragment counts",
    "disposition": "executable_without_change"
  },
  {
    "item": "sample count",
    "paper": "16 samples, one StHi removed -> 15",
    "data": "15 samples deposited (St Selected n=3)",
    "disposition": "executable_without_change"
  },
  {
    "item": "gene count after filter",
    "paper": "15,213 genes (>= 1 CPM in >= 3 samples)",
    "data": "26,628 features deposited; same filter applied at execution",
    "disposition": "executable_without_change"
  },
  {
    "item": "sign convention",
    "paper": "log2(Co/Hi), CeCo-CeHi, StCo-StHi",
    "data": "results are Hi vs Co",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 30071007 / GSE114062

**Status: finished.** The run is paper-aligned and associational: it compares a high-runner selected line (Hi, line 7) with a control line (Co, line 1). Both lines had 6 days of wheel access, so this is not a randomized exercise effect.

## What ran
- Route: case spec (`case_spec.json`) through `python -m tools.case_runner execute`. Validator: 13 records, 0 errors. The last attempt is the one reported here; earlier attempts are in `_previous/`.
- Matrix: `GSE114062_Cere_Stri_FPKM.csv.gz` with 15 samples (the paper's 16 minus the StHi PCA outlier it removed).
  - The file is labelled FPKM, but it is the **Cuffnorm count table**: per-sample values are integer multiples of one size-factor unit (0.84-1.30), and the column sums are about 40M (roughly the fragment totals).
  - This matches the paper's stated edgeR input (S2.2.p1).
- Alignment: exact match on `title`, 15/15. `line` (Co/Hi) and `region` (Ce/St) were parsed from the title.
- Method: the paper's method, run with edgeR 4.10.7 through `tools.r_de_tools:run_r_de` (engine `edger_ql`).
  - TMM normalization, robust `estimateDisp`/`glmQLFit`, QL F-test, BH correction, model `~ line * region`.
  - Low-count filter: >= 1 CPM in >= 3 samples. This kept **15,213 genes, exactly the paper's number**.
- Contrasts, all from one fit:
  - CeHi-CeCo
  - StHi-StCo
  - line x region interaction
  - line main effect (averaged over regions)
  - StHi-CeHi
  - region main effect (averaged over lines)
- Enrichment:
  - Hallmark GSEA on both within-region line rankings.
  - Enrichr ORA on the interaction genes. No GO BP term passed adjusted p 0.19.

## DEG counts vs paper (paper threshold: FDR < 0.05, no fold-change cutoff; S3.2.p1)
| Contrast | Ours (FDR<0.05) | Paper |
|---|---|---|
| line x region interaction | **75** (39 up / 36 down) | **86** |
| interaction, raw P < 0.005 (audit; paper's Table A rule) | 349 | 334 |
| interaction genes also FDR<0.05 in a within-region line contrast | 73/75 | 76/86 |
| CeHi vs CeCo | 964 | not reported (S1 Fig A only) |
| StHi vs StCo | 448 | not reported |
| line main effect | 1327 | 144 at \|log2FC\|>1, p rule unstated (Table E); 122 excluding interaction genes |
| region main effect | 12205 | 243 at FDR<1e-15 excluding interaction genes (different rule) |

- Gene-level reproduction is close to exact. The within-region log2FCs match Table 1 to two decimals (Npsr1 -6.47, Vdr -3.37, Pcsk9 3.21, Krt25 -1.98/3.02, Cd300lf -4.23).
- The interaction p- ... [2078 more characters]
