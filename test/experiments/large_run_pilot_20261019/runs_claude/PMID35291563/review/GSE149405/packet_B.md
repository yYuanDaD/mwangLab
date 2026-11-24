# Review packet B (the analysis' decisions): GSE149405

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_swimming_vs_control | 1344 | 20 | pvalue < 0.05 and |log2FoldChange| > 1 | 0 | 0 | 0 | 0 | 714 | 86 | 20 | 116 | 0.092 | 0.056 |

## Samples per design level

### `grp`
- **control** (6): GSM4499029 / control1 [167]; GSM4499030 / control2 [176]; GSM4499031 / control3 [169]; GSM4499032 / control4 [170]; GSM4499033 / control5 [160]; GSM4499034 / control6 [177]
- **swimming** (6): GSM4499035 / swimming1 [172]; GSM4499036 / swimming2 [179]; GSM4499037 / swimming3 [166]; GSM4499038 / swimming4 [156]; GSM4499039 / swimming5 [159]; GSM4499040 / swimming6 [162]

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE149405"], "assay": "bulk RNA-seq (rRNA-depleted, NovaSeq 6000) of subcutaneous CT-26 tumor tissue", "sample_inclusion": "6 tumors per group randomly selected from 10 control and 10 swimming male BALB/c mice (S2.6.p1, S2.4.p1)", "factors": {"group": ["control", "swimming"]}, "primary_estimand": "Effect of 3 weeks of swimming (twice daily, 6 d/week, up to 30 min) on tumor-tissue gene expression in CT-26 tumor-bearing mice, swimming vs control (S2.5.p1, S3.2.p1)", "planned_contrasts": ["swimming vs control (S3.2.p1; paper: 715 up / 629 down transcripts = 1344 DETs)"], "repeated_measure_unit": "none; one tumor per independent mouse", "normalization": "StringTie FPKM (S2.6.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "S2.6.p1; FIG2"}, "paper_method": "limma on StringTie transcript-level expression (S2.6.p1); KEGG ORA on DETs (S3.3.p1)", "paper_results": "715 up / 629 down transcripts; Vegfa mRNA down; Stat3, Pdgfa, Pld2, Pik3r2 decreased; Hif1a and Kdr (VEGFR2) mRNA unchanged (S3.2.p1, S3.4.p1, S4.p4)"}

reasoning: Single two-arm exercise design. S2.6.p1 states limma with 'cut-off > 2; P < 0.05'; read as fold change > 2 (|log2FC| > 1) and raw P < 0.05 — no FDR is mentioned, and Table 1 lists raw P values only. Results are reported as transcripts (ENSMUST IDs in Table 1).

rejected alternatives: [{"value": "cut-off > 2 meaning |log2FC| > 2", "reason_rejected": "'cut-off' with value 2 conventionally refers to fold change; Table 1 top hits have |logFC| 5-9 so either reading is consistent there, FC>2 is the standard reading"}]

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE149405\\GSE149405_merged_from_tar.csv", "owned": true, "checks": ["S2.6.p1 and S2.9.p1 name GSE149405", "GEO contact institute (Fujian Univ. TCM) and author Jun Peng (S6.p1) match", "12 samples = 6 control + 6 swimming as in S2.6.p1", "tumor tissue, CT-26 cells, Mus musculus"], "accession": "GSE149405", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE149405\\GSE149405_metadata.csv"}

reasoning: Paper cites GSE149405 explicitly; sample counts and tissue match.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.1.group"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\aligned\\design_metadata.csv", "sha256": "bbc9b21e99b472970efc219721f78128e44c5eaaa89f00f01a238b1ac25af127", "levels": {"grp": {"control": 6, "swimming": 6}}}}

reasoning: Merged tar columns are GSM<id>_<tumor id>; regex extracts the GSM id, which equals the metadata index (12/12 per inspect). Group taken from characteristics 'group' (control/swimming), consistent with titles control1-6 / swimming1-6.

### matrix (valid, not_started)

final: {"matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\aligned\\aligned_matrix.csv", "sha256": "a8daad6fb25646aeccee4f38bac3cd068f4a4f18ca9d75ca2cf37fb792856014", "n_features": 30630, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 7145.1529, "median": 0.36717, "integer_fraction": 0.2426, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Per-sample files hold one decimal column; only 24% integer values, max 7145, median 0.37; data_processing: 'Supplementary files ... include FPKM values for each Sample' (StringTie). Gene-level (ENSMUSG) whereas the paper analyzed transcripts (ENSMUST). Paper input was StringTie expression, analyzed by limma.

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "control", "treatment": "swimming", "contrasts": [{"name": "grp_swimming_vs_control", "control": "control", "treatment": "swimming", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Randomized two-arm intervention (S2.4.p1); swimming vs control is the paper's contrast (S3.2.p1). Causal estimand. All male (S2.3.p1).

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 12, "n_columns": 2, "columns": ["Intercept", "grp_swimming"], "rank": 2, "full_rank": true, "residual_df": 10, "levels": {"grp": {"control": 6, "swimming": 6}}, "cells": [{"cell": ["control"], "n": 6}, {"cell": ["swimming"], "n": 6}], "min_cell_size": 6, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 12, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 12, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.group", "n_levels": 2, "status": "complete_confounding", "crosstab": {"control": {"control": 6, "swimming": 0}, "swimming": {"control": 0, "swimming": 6}}}, {"column": "characteristics_ch1.2.cell type", "n_levels": 1, "status": "constant"}, {"column": "molecule_ch1", "n_levels": 1, "status": "constant ... [1382 more characters]

reasoning: Independent mice, one tumor each; no batch, lane or pairing recorded in GEO or the paper.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (limma-trend on log2(FPKM+1))", "formula": "~ grp", "paper_route": {"method": "limma on StringTie transcript-level expression", "status": "blocked", "reason": "Only gene-level FPKM is deposited; transcript-level quantification is not available, so the paper's per-transcript DET table cannot be reproduced."}, "deviations": ["gene-level instead of transcript-level features", "log2(FPKM+1) transform and expression filter (FPKM >= 1 in >= 6 samples) chosen here; paper does not state its transform or filtering"], "transform": "log2(x+1)"}

reasoning: FPKM is linear-normalized, not counts, so DESeq2/edgeR do not apply; limma on log2(FPKM+1) matches the paper's limma route on the available gene-level matrix.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "deviation_note": "Paper rule applied to gene-level features; paper counts are transcripts, so counts are not directly comparable."}

reasoning: S2.6.p1 / FIG2: 'cut-off > 2, P < 0.05' -> FC > 2 and raw P < 0.05. Audit: BH FDR < 0.05, no FC rule.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_swimming_vs_control", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\results\\grp_swimming_vs_control\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\results\\grp_swimming_vs_control\\DEG_results_swimming_vs_control.csv"], "counts": {"grp_swimming_vs_control": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 12737, "n_significant": 20, "n_up": 13, "n_down": 7, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 12737, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Paper's limma two-group contrast on gene-level log2(FPKM+1), filtered to expressed genes.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_swimming_vs_control_nofilter", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\results\\grp_swimming_vs_control_nofilter\\DEG_results_swimming_vs_control.csv"], "counts": {"grp_swimming_vs_control_nofilter": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 30630, "n_significant": 17, "n_up": 12, "n_down": 5, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 30630, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Same model without the expression filter, since the paper states none.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_swimming_vs_control", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\results\\enrichment_grp_swimming_vs_control\\ora\\DEG_results_swimming_vs_control_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\results\\enrichment_grp_swimming_vs_control\\ora\\DEG_results_swimming_vs_control_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\results\\enrichment_grp_swimming_vs_control\\ora\\DEG_results_swimming_vs_control_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\results\\enrichment_grp_swimming_vs_control\\ora\\DEG_results_swimming_vs_control_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 20 Mouse genes (direction=all, pvalue<0.05, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Response To Type II Interferon (GO:0034341) | padj=9.00e-02 | overlap=2/80 | genes ... [1256 more characters]

reasoning: Paper reports KEGG pathways (angiogenesis, hypoxia, VEGF) from DETs (S3.3.p1).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_swimming_vs_control", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35291563\\GSE149405\\results\\enrichment_grp_swimming_vs_control\\gsea\\DEG_results_swimming_vs_control_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12613 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 17 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=3.19 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=3.07 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=2.59 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=2.58 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.53 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=2.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.81 | NOM p=0.00e+00 | FDR q=2.11e-03 - HALLMARK_HYPOXIA | NES=1.72 | NOM p=0.00e+00 | FDR q=5.55e-03 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.71 | NOM p=0.00e+00 | FDR q=5.08e-03 - HALLMARK_KRAS_SIGNALING_DN | NES=1.38 | NOM p=7.05e-02 | FDR q=1.26e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V2 | NES=-2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=-1.88 | NOM p=0.00e+0 ... [411 more characters]

reasoning: Paper reports KEGG pathways (angiogenesis, hypoxia, VEGF) from DETs (S3.3.p1).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper DETs are transcripts (ENSMUST); our features are genes (ENSMUSG); counts are not directly comparable.", "Paper threshold uses raw P with no multiple-testing correction; audit FDR count reported separately.", "Paper text says reads mapped to hg38 while GEO says GRCm38.92; the matrix uses mouse Ensembl IDs, so hg38 is treated as a typo.", "Direction contradiction: paper reports Vegfa mRNA significantly down with swimming; here Vegfa log2FC -0.09, P = 0.56 (not changed). Stat3, Pdgfa, Pld2, Pik3r2 (paper: decreased) are unchanged or slightly up (all P > 0.05).", "Direction contradiction: paper argues swimming reduces tumor hypoxia; Hallmark HYPOXIA GSEA is positively enriched in swimming (NES +1.72, FDR 0.006). Hallmark ANGIOGENESIS is not enriched (FDR 1.0).", "Gene-level signal is near null: 714/12737 genes at raw P < 0.05 vs ~637 expected by chance; 0 genes at FDR < 0.05. The paper's 1344 transcript DETs under raw P < 0.05 with FC > 2 likely include many low-expression isoform-level chance hits."], "results": {"grp_swimming_vs_control": {"n_deg": 20, "up": 13, "down": 7, "rule": "pvalue < 0.05 and |log2FoldChange| > 1", "audit_n": 0}, "grp_swimming_vs_control_nofilter": {"n_deg": 17, "up": 12, "down": 5, "rule": "pvalue < 0.05 and |log2FoldChange| > 1", "audit_n": 0}}, "paper_counts": {"grp_swimming_vs_control": 1344}, "comparison": {"grp_swimming_vs_control": {"ours": 20, "paper": 1344}}, "paper_gene_check": {"grp_swimming_v ... [893 more characters]

reasoning: Paper reports 715 up + 629 down = 1344 transcripts; named genes: Vegfa, Stat3, Pdgfa, Pld2, Pik3r2 down; Hif1a, Kdr unchanged; Table 1 examples Nupr1 (down), Fgfr1, Clta (up).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "feature level",
    "paper": "transcript-level DETs (ENSMUST, S3.2.p1, Table 1)",
    "data": "gene-level FPKM (ENSMUSG)",
    "disposition": "declared_deviation"
  },
  {
    "item": "reference genome",
    "paper": "hg38 (S2.6.p1)",
    "data": "GRCm38.92 per GEO data_processing; mouse Ensembl IDs",
    "disposition": "executable_without_change"
  },
  {
    "item": "group size",
    "paper": "10 per group in the tumor study, 6 per group sequenced (S2.6.p1)",
    "data": "6 + 6 samples",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 35291563 / GSE149405

**Status:** finished (case completed, route `declared_deviation`, validator 13 records, 0 errors)

## What ran
- `inspect GSE149405`: downloaded the series and merged `GSE149405_RAW.tar` into `GSE149405_merged_from_tar.csv` (30,630 ENSMUSG genes × 12 samples, gene-level StringTie FPKM).
- Case spec `case_spec.json` → `python -m tools.case_runner execute` (run twice; the first attempt is in `_previous/`, the only change was adding study caveats).
  - Alignment: GSM id taken from the matrix column names (`^(GSM\d+)_\d+$`), exact match to the metadata index, 12/12. `grp` = `characteristics_ch1.1.group` (control 6, swimming 6).
  - Matrix: FPKM (24% integer values, median 0.37, GEO `data_processing` says FPKM). Gene level, while the paper analysed transcripts.
  - Design: two groups, swimming vs control, `~ grp`; mice are independent, so no blocking. Suitability verdict: analyzable.
  - Method: limma-trend on log2(FPKM+1).
    - Primary run filters to FPKM ≥ 1 in ≥ 6 samples (12,737 genes kept).
    - Sensitivity run uses no filter (30,630 genes).
  - Enrichment on the primary table:
    - ORA (GO and KEGG 2019 Mouse) on the paper-threshold DEGs.
    - GSEA on MSigDB Hallmark, ranked by the moderated t.

## Threshold
- The paper's rule (S2.6.p1, FIG2) reads "cut-off > 2; P < 0.05". I took this as fold change > 2 (|log2FC| > 1) and raw P < 0.05, with no FDR.
- That rule was applied as given (`paper_on_deviation_route`).
- Audit rule: BH FDR < 0.05, with no fold-change cutoff.

## DEG counts vs the paper
| Contrast | Ours (paper rule) | Up / Down | Audit FDR<0.05 | Paper |
|---|---|---|---|---|
| swimming vs control (primary, filtered) | 20 | 13 / 7 | 0 | 1344 transcripts (715 up / 629 down) |
| swimming vs control (no filter, sensitivity) | 17 | 12 / 5 | 0 | — |

- At the gene level there is almost no signal. In the primary run, 714 of 12,737 genes have raw P < 0.05, against about 637 expected by chance.
- The paper's named genes do not replicate:
  - Vegfa (paper: significantly down): log2FC −0.09, P = 0.56.
  - Stat3, Pdgfa, Pld2 and Pik3r2 (paper: decreased): all have P > 0.05 and three of the four lean upward.
  - Hif1a and Kdr: unchanged, as the paper also reports.
- Enrichment, kept separate from the DE result:
  - Hallmark HYPOXIA is enriched upward with swimming (NES +1.72, FDR 0.006), the opposite of the paper's "reduced hypoxia" reading.
  - Hallmark ANGIOGENESIS is not enriched (FDR 1.0).
  - The top Hallmark s ... [1210 more characters]
