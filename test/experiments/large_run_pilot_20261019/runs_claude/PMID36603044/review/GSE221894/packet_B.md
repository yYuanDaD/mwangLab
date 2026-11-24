# Review packet B (the analysis' decisions): GSE221894

## Mechanical flags

- **other_rule_matches_paper**: {"table": "time_post_vs_pre", "paper": 35, "applied": 174, "applied_rule": "padj < 0.05", "closest_rule": "padj<0.05 & |lfc|>0.584963", "closest_n": 33, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| time_post_vs_pre | 35 | 174 | padj < 0.05 | 174 | 33 | 7 | 255 | 1403 | 300 | 125 | 544 | 0.199 | 0.07 |
| unpaired_all_time_post_vs_pre | 35 | 62 | padj < 0.05 | 62 | 14 | 5 | 158 | 1347 | 302 | 133 | 461 | 0.168 | 0.067 |

## Samples per design level

### `time`
- **post** (14): GSM6909063 / 14b; GSM6909065 / 16b; GSM6909067 / 19b; GSM6909069 / 1b; GSM6909071 / 20b; GSM6909074 / 28b; GSM6909076 / 32b; GSM6909078 / 33b; GSM6909080 / 34b; GSM6909082 / 3b; GSM6909083 / 4b; GSM6909085 / 6b; GSM6909087 / 7b; GSM6909088 / 8b
- **pre** (13): GSM6909062 / 14a; GSM6909064 / 16a; GSM6909066 / 19a; GSM6909068 / 1a; GSM6909070 / 20a; GSM6909072 / 27a; GSM6909073 / 28a; GSM6909075 / 32a; GSM6909077 / 33a; GSM6909079 / 34a; GSM6909081 / 3a; GSM6909084 / 6a; GSM6909086 / 7a

### `subject`
- **S1** (2): GSM6909068 / 1a; GSM6909069 / 1b
- **S14** (2): GSM6909062 / 14a; GSM6909063 / 14b
- **S16** (2): GSM6909064 / 16a; GSM6909065 / 16b
- **S19** (2): GSM6909066 / 19a; GSM6909067 / 19b
- **S20** (2): GSM6909070 / 20a; GSM6909071 / 20b
- **S27** (1): GSM6909072 / 27a
- **S28** (2): GSM6909073 / 28a; GSM6909074 / 28b
- **S3** (2): GSM6909081 / 3a; GSM6909082 / 3b
- **S32** (2): GSM6909075 / 32a; GSM6909076 / 32b
- **S33** (2): GSM6909077 / 33a; GSM6909078 / 33b
- **S34** (2): GSM6909079 / 34a; GSM6909080 / 34b
- **S4** (1): GSM6909083 / 4b
- **S6** (2): GSM6909084 / 6a; GSM6909085 / 6b
- **S7** (2): GSM6909086 / 7a; GSM6909087 / 7b
- **S8** (1): GSM6909088 / 8b

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE221894"], "source_text": "PubMed abstract only (no full text available) plus GEO series summary/overall design and the authors' deposited DESeq2 table GSE221894_PostLean-PreLean_rawDE-v2.xls.gz", "assay": "bulk RNA-seq, vastus lateralis biopsy, Illumina NextSeq 2000 100bp SE, salmon v1.4.0 (GEO data_processing)", "sample_inclusion": "15 sedentary normal-weight adults started, 14 completed 7 HIIT sessions over 14 days; biopsies before and 48 h after the last session (abstract)", "factors": {"time": ["pre (baseline)", "post (48 h after 2 wk HIIT)"]}, "primary_estimand": "within-person change in vastus lateralis gene expression from before to 48 h after 2 weeks (7 sessions) of HIIT", "repeated_measure_unit": "participant (pre and post biopsy from the same person)", "planned_contrasts": ["post-HIIT vs pre-HIIT (abstract: transcripts that increased/decreased with HIIT; GEO deposited table PostLean-PreLean)"], "paper_method": "DESeq2 v1.32.0 on salmon quantifications (GEO data_processing); exact design formula (paired or not) not stated in the abstract", "paper_threshold": {"metric": "not stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "abstract states no DEG threshold"}, "paper_results": "abstract: increased transcripts enriched for mitochondrial respiration gene sets (especially complex I); decreased transcripts enriched for DNA and chromatin remodelling pathways; no DEG count given. Deposited authors' table: 35 genes p ... [71 more characters]

reasoning: No full text; the abstract defines the estimand (pre vs 48 h post 2-wk HIIT in the same people) and the qualitative pathway result. GEO data_processing names salmon v1.4.0 + DESeq2 v1.32.0. The GEO supplementary DE table (Post-Pre) gives the authors' own gene-level result and is used as the count comparison.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE221894\\GSE221894_salmon_gene_numreads.csv", "owned": true, "checks": ["GEO Series_pubmed_id = 36603044", "series title equals the paper title", "27 GSM quant.sf files in GSE221894_RAW.tar, one per GSM of the series", "matrix built from that tar by prep_salmon_to_gene.py"], "accession": "GSE221894", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE221894\\GSE221894_metadata.csv"}

reasoning: GSE221894 is linked to PMID 36603044 in GEO and has the paper's title; the matrix is derived only from this series' per-sample salmon files.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 27, "n_metadata": 27, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\aligned\\aligned_metadata.csv", "columns": {"sex": {"alias_of": "characteristics_ch1.3.Sex"}, "status": {"alias_of": "characteristics_ch1.1.status"}, "subject": {"source": "title", "regex": "^(\\d+)[ab]$", "recode": {"1": "S1", "3": "S3", "4": "S4", "6": "S6", "7": "S7", "8": "S8", "14": "S14", "16": "S16", "19": "S19", "20": "S20", "27": "S27", "28": "S28", "32": "S32", "33": "S33", "34": "S34"}}, "time": {"source": "title", "regex": "^\\d+([ab])$", "recode": {"a": "pre", "b": "post"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\aligned\\design_metadata.csv", "sha256": "f724497e226e8fa54555cf1f047b17eceeb4c44ced8d249c50b273ce5eee0b70", "levels": {"sex": {"Female": 16, "Male": 11}, "status": {"baseline": 14, "48hr post training": 13}, "subject": {"S14": 2, "S16": 2, "S19": 2, "S1": 2, "S20": 2, "S28": 2, "S32": 2, "S33": 2, "S34": 2, "S3": 2, "S6": 2, "S7": 2, "S27": 1, "S4": 1, "S8": 1}, "time": {"post": 14, "pre": 13}}}}

reasoning: Matrix columns are GSM ids = metadata index (27/27 exact). Titles follow <participant><a|b>; a = baseline and b = 48 h post for 26/27 samples per the status field. Time is taken from the title: GSM6909087 '7b' is annotated 'baseline' but its title says b; with 7b as post there are exactly 14 post biopsies = the 14 completers in the abstract, and 13 complete pre samples + 1 non-completer. This is treated as a GEO labelling error and fixed (sensitivity run excludes participant 7). Unpaired samples: 27a (likely the non-completer), 4b and 8b (no baseline deposited).

rejected alternatives: [{"value": "time from characteristics status", "reason_rejected": "makes participant 7 have two baselines and only 13 post samples, inconsistent with the title convention and 14 completers"}]

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\aligned\\aligned_matrix.csv", "sha256": "cea44cc6fc0439621556d4a15b5f49d59401f20315713e59e94cad04e468be68", "n_features": 34402, "n_samples": 27, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1596970.0, "median": 0.0, "integer_fraction": 0.8696, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Salmon v1.4.0 NumReads (estimated counts, 87% integer-valued, max 1.6e6) summed per Ensembl gene (tximport-style, Ensembl 104 tx2gene; ~1.4% reads on transcripts absent from Ens104). The paper used DESeq2 on salmon output, so rounded estimated counts into DESeq2 matches the paper's input.

### design (valid, not_started)

final: {"analysis_type": "paired two-group (repeated measures)", "design_column": "time", "control": "pre", "treatment": "post", "contrasts": [{"name": "time_post_vs_pre", "control": "pre", "treatment": "post", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Abstract: biopsies before and 48 h after HIIT in the same participants; the estimand is the within-person training effect. Single two-level time factor with participant as the blocking unit; samples without a partner do not inform a subject-blocked contrast and are dropped by complete_pairs. Both sexes are present; per-sex paired analyses are added as exploratory.

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "sex", "disposition": "absorbed by subject blocking (constant within participant); per-sex exploratory runs instead"}], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 27, "n_columns": 16, "columns": ["Intercept", "time_pre", "subject_S14", "subject_S16", "subject_S19", "subject_S20", "subject_S27", "subject_S28", "subject_S3", "subject_S32", "subject_S33", "subject_S34", "subject_S4", "subject_S6", "subject_S7", "subject_S8"], "rank": 16, "full_rank": true, "residual_df": 11, "levels": {"time": {"post": 14, "pre": 13}, "subject": {"S14": 2, "S16": 2, "S19": 2, "S1": 2, "S20": 2, "S28": 2, "S32": 2, "S33": 2, "S34": 2, "S3": 2, "S6": 2, "S7": 2, "S27": 1, "S4": 1, "S8": 1}}, "cells": [{"cell": ["post", "S1"], "n": 1}, {"cell": ["post", "S14"], "n": 1}, {"cell": ["post", "S16"], "n": 1}, {"cell": ["post", "S19"], "n": 1}, {"cell": ["post", "S20"], "n": 1}, {"cell": ["post", "S28"], "n": 1}, {"cell": ["post", "S3"], "n": 1}, {"cell": ["post", "S32"], "n": 1}, {"cell": ["post", "S33"], "n": 1}, {"cell": ["post", "S34"], "n": 1}, {"cell": ["post", "S4"], "n": 1}, {"cell": ["post", "S6"], "n": 1}, {"cell": ["post", "S7"], "n": 1}, {"cell": ["post", "S8"], "n": 1}, {"cell": ["pre", "S1"], "n": 1}, {"cell": ["pre", "S14"], "n": 1}, {"cell": ["pre", "S16"], "n": 1}, {"cell": ["pre", "S19"], "n": 1}, {"cell": ["pre", "S20"], "n": 1}, {"cell": ["pre", "S27"], "n": 1}, {"cell": [" ... [420 more characters]

reasoning: Repeated measures within participant -> subject is a blocking term (~ subject + time). Sex does not vary within a participant so it is aliased with subject and not added.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "DESeq2 (pydeseq2 Wald) ~ subject + time on rounded salmon gene-level estimated counts", "formula": "~ subject + time", "rounding_documented": true, "paper_route": {"method": "DESeq2 v1.32.0 (R)", "status": "reproduced_approximately", "reason": "same model family; abstract does not state whether the authors blocked on participant; pydeseq2 instead of R DESeq2; tximport length offsets not used"}, "deviations": ["participant blocking chosen from the study design (paper formula unknown)", "gene summarisation by summed NumReads without tximport average-length offsets", "pydeseq2 instead of R DESeq2"], "transform": "round"}

reasoning: DESeq2 on rounded estimated counts reproduces the paper's DESeq2-on-salmon route; subject blocking matches the paired design. An unpaired all-sample ~ time model is run as exploratory to compare with the authors' deposited table, which may have been unpaired.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "not stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Abstract gives no DEG threshold; BH padj < 0.05 without fold-change cutoff (workflow default). Raw p < 0.05 shown only as a labelled audit count (authors' table: 788 at p<0.05)."}

reasoning: No threshold in the available text.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "time_post_vs_pre", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 24, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\time_post_vs_pre\\input\\paired\\paired_matrix.csv", "transform": "round", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\time_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"time_post_vs_pre": {"applied": {"rule": "padj < 0.05", "n_tested": 7566, "n_significant": 174, "n_up": 93, "n_down": 81, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 19932, "n_significant": 1403, "n_up": 752, "n_down": 651, "deg_sanity": "ok"}}}}

reasoning: paired DESeq2 on the 12 complete participants (including 7 with 7b as post)

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "sens_no_subject7_time_post_vs_pre", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 22, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\sens_no_subject7_time_post_vs_pre\\input\\paired\\paired_matrix.csv", "transform": "round", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\sens_no_subject7_time_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"sens_no_subject7_time_post_vs_pre": {"applied": {"rule": "padj < 0.05", "n_tested": 10190, "n_significant": 104, "n_up": 55, "n_down": 49, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 19775, "n_significant": 1283, "n_up": 701, "n_down": 582, "deg_sanity": "ok"}}}}

reasoning: drops participant 7 whose post label was corrected

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "unpaired_all_time_post_vs_pre", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 27, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\transformed\\rounded_counts.csv", "transform": "round", "formula": "~ time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\unpaired_all_time_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"unpaired_all_time_post_vs_pre": {"applied": {"rule": "padj < 0.05", "n_tested": 6469, "n_significant": 62, "n_up": 32, "n_down": 30, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 20123, "n_significant": 1347, "n_up": 654, "n_down": 693, "deg_sanity": "ok"}}}}

reasoning: all 27 samples, ~ time, as the authors may have fitted; for comparison with the deposited table

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "female_time_post_vs_pre", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\female_time_post_vs_pre\\input\\paired\\paired_matrix.csv", "transform": "round", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\female_time_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"female_time_post_vs_pre": {"applied": {"rule": "padj < 0.05", "n_tested": 8310, "n_significant": 146, "n_up": 95, "n_down": 51, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 18984, "n_significant": 1414, "n_up": 733, "n_down": 681, "deg_sanity": "ok"}}}}

reasoning: per-sex split (7 female pairs)

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "male_time_post_vs_pre", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\male_time_post_vs_pre\\input\\paired\\paired_matrix.csv", "transform": "round", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\male_time_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"male_time_post_vs_pre": {"applied": {"rule": "padj < 0.05", "n_tested": 4896, "n_significant": 44, "n_up": 15, "n_down": 29, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 18597, "n_significant": 1027, "n_up": 488, "n_down": 539, "deg_sanity": "ok"}}}}

reasoning: per-sex split (5 male pairs)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\enrichment_time_post_vs_pre\\gsea\\DEG_results_post_vs_pre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 19036 Human genes ranked by 'stat'. 50 Hallmark sets tested, 32 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.86 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.04 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=1.91 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.89 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_GLYCOLYSIS | NES=1.83 | NOM p=0.00e+00 | FDR q=1.05e-03 - HALLMARK_ADIPOGENESIS | NES=1.80 | NOM p=0.00e+00 | FDR q=1.09e-03 - HALLMARK_MTORC1_SIGNALING | NES=1.67 | NOM p=0.00e+00 | FDR q=4.68e-03 - HALLMARK_COAGULATION | NES=1.57 | NOM p=1.85e-03 | FDR q=1.59e-02 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.51 | NOM p=0.00e+00 | FDR q=2.43e-02 - HALLMARK_KRAS_SIGNALING_UP | NES=1.49 | NOM p=0.00e+00 | FDR q=2.66e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_G2M_CHECKPOINT | NES=-1.47 | NOM p=0.00e+00 | FDR q=1.19e-01 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=-1.38 | NOM p=6.78e-02 | FDR q=1.34e-01 - H ... [389 more characters]

reasoning: abstract reports gene sets up (mitochondrial respiration, complex I) and down (DNA/chromatin remodelling); Hallmark GSEA on the full ranking

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\enrichment_time_post_vs_pre\\ora_up\\DEG_results_post_vs_pre_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\enrichment_time_post_vs_pre\\ora_up\\DEG_results_post_vs_pre_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\enrichment_time_post_vs_pre\\ora_up\\DEG_results_post_vs_pre_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\enrichment_time_post_vs_pre\\ora_up\\DEG_results_post_vs_pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 93 Human genes (direction=up, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Aerobic Electron Transport Chain (GO:0019646) | padj=4.30e-07 | overlap=8/68 | genes=NDUFA8;NDUFB6;COX15;UQCRFS1;CYCS;COX7A2;COX5B;UQCRH - Mit ... [1199 more characters]

reasoning: GO/KEGG of increased transcripts (abstract: mitochondrial respiration)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\enrichment_time_post_vs_pre\\ora_down\\DEG_results_post_vs_pre_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\enrichment_time_post_vs_pre\\ora_down\\DEG_results_post_vs_pre_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\enrichment_time_post_vs_pre\\ora_down\\DEG_results_post_vs_pre_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36603044\\GSE221894\\results\\enrichment_time_post_vs_pre\\ora_down\\DEG_results_post_vs_pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 81 Human genes (direction=down, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Skeletal Muscle Tissue Development (GO:0007519) | padj=5.72e-04 | overlap=5/42 | genes=RYR1;MYLK2;SVIL;MYF6;DMD - Positive Regulat ... [1209 more characters]

reasoning: GO/KEGG of decreased transcripts (abstract: DNA and chromatin remodelling)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Comparison with the paper rests on the PubMed abstract and GEO-deposited files only (no full text).", "Participant 7's post sample (GSM6909087, title 7b) is annotated 'baseline' in GEO; relabelled as post from the title (sensitivity run excludes participant 7).", "Authors' deposited table lists only 5944 genes (baseMean>140); its 35 padj<0.05 genes are the count reference, but its gene filtering and design are unknown.", "Per-sex analyses are exploratory (5 male pairs)."], "results": {"time_post_vs_pre": {"n_deg": 174, "up": 93, "down": 81, "rule": "padj < 0.05", "audit_n": 1403}, "sens_no_subject7_time_post_vs_pre": {"n_deg": 104, "up": 55, "down": 49, "rule": "padj < 0.05", "audit_n": 1283}, "unpaired_all_time_post_vs_pre": {"n_deg": 62, "up": 32, "down": 30, "rule": "padj < 0.05", "audit_n": 1347}, "female_time_post_vs_pre": {"n_deg": 146, "up": 95, "down": 51, "rule": "padj < 0.05", "audit_n": 1414}, "male_time_post_vs_pre": {"n_deg": 44, "up": 15, "down": 29, "rule": "padj < 0.05", "audit_n": 1027}}, "paper_counts": {"time_post_vs_pre": 35, "unpaired_all_time_post_vs_pre": 35}, "comparison": {"time_post_vs_pre": {"ours": 174, "paper": 35}, "unpaired_all_time_post_vs_pre": {"ours": 62, "paper": 35}}, "paper_gene_check": {"time_post_vs_pre": {"COQ10A": {"baseMean": 2732.4117, "log2FoldChange": 0.5222, "padj": 1.41e-07, "pvalue": 1.86e-11}, "CIAO2A": {"baseMean": 1211.2953, "log2FoldChange": 0.5764, "padj": 4.62e-07, "pvalue": 2. ... [1594 more characters]

reasoning: Planned route is DESeq2 like the paper but with declared deviations (blocking chosen by us, gene summarisation). paper_counts are from the authors' GEO-deposited DESeq2 table at padj<0.05 (19 up incl. COQ10A, MDH1, ALAS1, BCKDK, CHCHD3; 16 down incl. MSTN, PFKFB3, USP6), not from the abstract.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); sex: omit (makes the design rank deficient) |
- | Sex | pass | Sex inference completed on 27 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "participant 7 post label",
    "paper": "14 completers with pre and post biopsies",
    "data": "GSM6909087 titled 7b but status 'baseline'; only 13 samples annotated post",
    "disposition": "fixed from title; sensitivity without participant 7"
  },
  {
    "item": "unpaired samples",
    "paper": "14 completers",
    "data": "27a has no post; 4b and 8b have no baseline",
    "disposition": "excluded from paired models by complete_pairs; included in exploratory unpaired model"
  },
  {
    "item": "design formula",
    "paper": "DESeq2 v1.32.0, formula not stated in abstract",
    "data": "paired structure available",
    "disposition": "paired ~ subject + time primary; unpaired ~ time exploratory"
  },
  {
    "item": "deposited DE gene set",
    "paper": "not stated",
    "data": "authors' table has 5944 genes, baseMean > 140",
    "disposition": "count comparison noted as approximate"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID36603044 / GSE221894

**The comparison with the paper rests on the abstract only.** No full text was available. The sources were the PubMed abstract (`PMID36603044_abstract.txt`, NCBI efetch), the GEO series description and data_processing (`GSE221894_family.soft`), and the authors' deposited DESeq2 table `GSE221894_PostLean-PreLean_rawDE-v2.xls.gz`. The abstract gives no DEG count and no threshold. The count comparison below uses the deposited table, not the paper text.

## What ran
- **Data.** 27 per-sample salmon v1.4.0 `quant.sf` files from `GSE221894_RAW.tar`, at transcript level (ENST.version).
  - `prep_salmon_to_gene.py` sums NumReads per Ensembl gene, using a transcript→gene map from the Ensembl 104 GTF (`data/_reference/`). This is tximport-style, without length offsets.
  - Result: 34,402 genes × 27 GSM. About 1.4% of reads fall on transcripts missing from Ens104 and are not counted (log: `prep_salmon_to_gene.log`).
- **Matrix type.** Estimated counts, rounded, run through DESeq2 (pydeseq2), matching the paper's salmon → DESeq2 route.
- **Design.** Within-person change, post (48 h after 7 HIIT sessions) vs pre. Primary model `~ subject + time` on complete pairs.
- **Labelling fix.** GSM6909087 (title `7b`) is annotated "baseline" in GEO. I relabelled it as post from the title convention: that gives 14 post biopsies, which matches the abstract's 14 completers.
  - Unpaired samples (27a, 4b, 8b) are dropped from the paired models.
- **Runs** (all executed; the contract validator reported 0 errors):

| table | role | samples | DEGs padj<0.05 (up/down) | raw p<0.05 (audit) |
|---|---|---|---|---|
| time_post_vs_pre | primary, paired | 12 pairs | 174 (93/81) | 1403 |
| sens_no_subject7_time_post_vs_pre | sensitivity | 11 pairs | 104 (55/49) | 1283 |
| unpaired_all_time_post_vs_pre | exploratory, `~ time` | 27 (14 post/13 pre) | 62 (32/30) | 1347 |
| female_time_post_vs_pre | exploratory | 7 pairs | 146 (95/51) | 1414 |
| male_time_post_vs_pre | exploratory | 5 pairs | 44 (15/29) | 1027 |

- **Threshold.** The abstract states none, so I used the workflow default: BH padj < 0.05 with no fold-change cutoff.

## DEG counts vs the paper
- **Authors' deposited table:** 35 DEGs at padj < 0.05 (19 up, 16 down). It lists only 5,944 genes, all with baseMean > 140.
- **Unpaired `~ time` (exploratory):** essentially the authors' model.
  - logFC r = 0.999 and sign agreement 99.8% on the 5,944 shared genes.
  - It recovers 34 of their 35 DEGs. We ... [2827 more characters]
