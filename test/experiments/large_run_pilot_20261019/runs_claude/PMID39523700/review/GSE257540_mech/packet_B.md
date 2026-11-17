# Review packet B (the analysis' decisions): GSE257540_mech

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_MS_vs_MC | 2 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 413 | 231 | 165 | 63 | 0.109 | 0.013 |

## Samples per design level

### `grp`
- **MC** (3): GSM8107904 / MC1; GSM8107905 / MC2; GSM8107907 / MC4
- **MS** (4): GSM8107900 / M1; GSM8107901 / M2; GSM8107902 / M3; GSM8107903 / M4

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE257540", "GSE281241"], "primary_estimand": "Transcriptomic effect on HB9::GFP mESC-derived motor neuron spheroids of (a) biochemical stimulation with conditioned medium from optogenetically exercised C2C12 muscle (1 Hz light, 30 min/day) or from spontaneously twitching (unstimulated) muscle, versus unconditioned control medium, and (b) mechanical stimulation by magnetic matrix actuation (MagMA) versus non-actuated MagMA controls (S2.4.p1-p4, FIG7, S4.6, S4.7).", "planned_contrasts": ["Exercise CM vs Control (FIG7c; S2.4.p3)", "Spontaneous-twitch CM vs Control (FIG7d)", "Exercise CM vs Spontaneous-twitch CM (FIG7e)", "Mechanical stimulation vs mechanical control (FIG7i; S2.4.p4: only 2 significant hits, both up)"], "paper_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": "not_reported", "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "FIG7 legend; S4.10.p1"}, "factors": {"biochemical": ["Control", "Spontaneous twitch CM (GEO: Low intensity biochem, NE1-6)", "Exercise CM (GEO: High intensity biochem, S1-6)"], "mechanical": ["Mechanical control (MC1-4)", "Mechanical stimulation (M1-4)"]}, "sample_inclusion": "QC exclusion of samples with <500K reads, rRNA >20% or exon/intron ratio <10 (n = 5, S4.10.p1); final n: control 5, spontaneous 4, exercise 4 (FIG7a); mechanical control 3, mechanical 4 (FIG7i)", "repeated_measure_unit": "not_reported (independent spheroid wells; no pairing described)", "normalization": "DESeq2 size ... [772 more characters]

reasoning: Built from S2.4.p1-p5, FIG7 legend, S4.6-S4.11 and DA.p1. Paper's DE threshold is BH-adjusted p with no stated numeric cutoff or fold-change rule (FIG7 legend: p-values used to determine DEGs were Benjamini-Hochberg adjusted).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE257540\\GSE257540_expression_data_counts.tsv.txt.gz", "owned": true, "checks": ["S4.8.p2 and DA.p1 cite GSE257540", "GEO Series_pubmed_id 39523700", "26 GSMs = HB9::GFP motor neuron spheroids with treatment labels matching the paper's 5 arms", "matrix columns C/L/H/M/MC map 1:1 to GSM titles C/LI/HI/M/MC"], "accession": "GSE257540", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE257540\\GSE257540_metadata.csv"}

reasoning: Paper names GSE257540 as its RNA-seq deposit; samples and arms match FIG7.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 26, "n_metadata": 26, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM8107906": "QC (S4.10.p1): 613K reads, 10x below other mechanical libraries, with 31.7K detected genes (highest of all samples), consistent with the low exon/intron coverage criterion; paper keeps 3 mechanical controls (FIG7i)", "GSM8107914": "biochemical-stimulation experiment with its own controls, analyzed in case GSE257540_biochem", "GSM8107915": "biochemical-stimulation experiment with its own controls, analyzed in case GSE257540_biochem", "GSM8107916": "biochemical-stimulation experiment with its own controls, analyzed in case GSE257540_biochem", "GSM8107917": "biochemical-stimulation experiment with its own controls, analyzed in case GSE257540_biochem", "GSM8107918": "biochemical-stimulation experiment with its own controls, analyzed in case GSE257540_biochem", "GSM8107919": "biochemical-stimulation experiment with its own controls, analyzed in case GSE257540_biochem", "GSM8107908": "biochemical-stimulation experiment with its own controls, analyzed in case GSE257540_biochem", "GSM8107909": "biochemical-stimulation experiment with its own controls, analyzed in case GSE257540_biochem", "GSM8107910": "biochemical-stimulation experiment with its own controls, analyzed in case GSE257540_biochem", "GSM8107911": "biochemical-stimulation experiment with its own controls, analyzed in case GSE257540_biochem", ... [1534 more characters]

reasoning: Same key derivation as the biochemical case. Keeps the mechanical experiment only (M1-4, MC1/2/4). MC3 excluded by the S4.10.p1 QC criteria (paper keeps 3 controls, FIG7i).

### matrix (valid, not_started)

final: {"source": "GSE257540_expression_data_counts.tsv.txt.gz (GEO supplementary)", "paper_input": "Gene-level expression tables from STAR/Salmon (S4.10.p1), tested with DESeq2", "rounding_documented": true, "matrix_type": "estimated counts (nf-core STAR/Salmon gene-level counts, deposited as integers)", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_mech\\aligned\\aligned_matrix.csv", "sha256": "ed2ca93c0e2aedc66c8c69a31f080045707553734f2bfd6bf83539b80cb07aac", "n_features": 56941, "n_samples": 7, "annotation_columns_dropped": ["GSM8107906", "GSM8107908", "GSM8107909", "GSM8107910", "GSM8107911", "GSM8107912", "GSM8107913", "GSM8107914", "GSM8107915", "GSM8107916", "GSM8107917", "GSM8107918", "GSM8107919", "GSM8107920", "GSM8107921", "GSM8107922", "GSM8107923", "GSM8107924", "GSM8107925"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 619602.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values are non-negative integers (integer fraction 1.0), max 1.1M, Ensembl gene rows with GeneSymbol/Biotype annotation. GEO data_processing: nf-core/rnaseq 3.11.1, gene-level raw counts and TPM generated by Salmon. Salmon gene counts are estimated counts; the submitter deposited them already rounded to integers, which is the count input the paper gave DESeq2 (S4.10.p1). The deposited integers are used unchanged (no further rounding). The companion _tpms file is TPM and is not used for DE.

rejected alternatives: [{"value": "GSE257540_expression_data_tpms.tsv.txt.gz", "reason_rejected": "TPM, used by the paper for visualization only; DESeq2 needs counts"}]

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "MC", "treatment": "MS", "contrasts": [{"name": "grp_MS_vs_MC", "control": "MC", "treatment": "MS", "role": "primary"}], "estimand_type": "causal (randomized in vitro treatment)", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_mech\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: FIG7i: mechanically actuated MagMA spheroids vs non-actuated MagMA controls on the same hydrogel type (S2.3, FIG5d). n = 4 vs 3.

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 7, "n_columns": 2, "columns": ["Intercept", "grp_MS"], "rank": 2, "full_rank": true, "residual_df": 5, "levels": {"grp": {"MS": 4, "MC": 3}}, "cells": [{"cell": ["MC"], "n": 3}, {"cell": ["MS"], "n": 4}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 7, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 7, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.cell line", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.cell type", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.genotype", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.4.treatment", "n_levels": 2, "status": "complete_confounding", "crosstab": {"MC": {"M ... [1967 more characters]

reasoning: Independent spheroid wells per arm; no donor/subject, pairing, batch or lane variable in GEO metadata or paper. Nothing to block on.

### method (valid, not_started)

final: {"matrix_type": "estimated counts (nf-core STAR/Salmon gene-level counts, deposited as integers)", "method": "DESeq2 (pydeseq2 Wald, ~ grp)", "formula": "~ grp", "rounding_documented": true, "paper_route": {"method": "DESeq2 Wald with normal-prior/ashr LFC shrinkage (R 4.2.0)", "status": "reproduced_without_shrinkage", "reason": "pydeseq2 has no ashr; shrinkage changes LFC only"}, "deviations": ["no ashr/normal-prior LFC shrinkage", "pydeseq2 instead of R DESeq2"]}

reasoning: Paper's method (S4.10.p1) on the deposited counts.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": "not_reported", "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "FIG7 legend; S4.10.p1"}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Paper defines DEGs by BH-adjusted p without stating the cutoff; the workflow default BH padj < 0.05 with no fold-change rule is applied (same metric and adjustment). Nominal p < 0.05 is reported as an audit count because the paper used nominal p for its FIG7j mechanical heatmap."}

reasoning: FIG7 legend and S4.10.p1 name BH-adjusted p-values but no numeric cutoff; no effect-size rule stated.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_MS_vs_MC", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 7, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_mech\\aligned\\aligned_matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_mech\\results\\grp_MS_vs_MC\\DEG_results_MS_vs_MC.csv"], "counts": {"grp_MS_vs_MC": {"applied": {"rule": "padj < 0.05", "n_tested": 30598, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 30598, "n_significant": 413, "n_up": 221, "n_down": 192, "deg_sanity": "ok"}}}}

reasoning: Paper's two-group DESeq2 for the mechanical experiment.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_MS_vs_MC", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_mech\\results\\enrichment_grp_MS_vs_MC\\gsea\\DEG_results_MS_vs_MC_GSEA_Hallmark.csv"], "summary": "GSEA complete on 29629 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 40 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HEDGEHOG_SIGNALING | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.01 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.88 | NOM p=0.00e+00 | FDR q=5.99e-04 - HALLMARK_HEME_METABOLISM | NES=1.82 | NOM p=0.00e+00 | FDR q=1.25e-03 - HALLMARK_UV_RESPONSE_DN | NES=1.71 | NOM p=0.00e+00 | FDR q=4.07e-03 - HALLMARK_ANDROGEN_RESPONSE | NES=1.67 | NOM p=2.12e-03 | FDR q=5.06e-03 - HALLMARK_KRAS_SIGNALING_UP | NES=1.66 | NOM p=0.00e+00 | FDR q=4.66e-03 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.58 | NOM p=2.17e-03 | FDR q=1.36e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-2.47 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLM ... [383 more characters]

reasoning: Paper's key mechanical claim is GSEA (FIG7k); ORA skipped (2 DEGs in paper).

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Small arms (4 vs 3)."], "results": {"grp_MS_vs_MC": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 413}}, "paper_counts": {"grp_MS_vs_MC": 2}, "comparison": {"grp_MS_vs_MC": {"ours": 0, "paper": 2}}, "paper_gene_check": {}}

reasoning: S2.4.p4: two significant hits, both up (RNA-degradation markers, unnamed).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 7 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "QC exclusions",
    "paper": "mechanical control n = 3 (FIG7i)",
    "data": "MC3 is the only mechanical library failing the depth/coverage pattern",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 39523700 (PMC11874633)

Paper: *Actuating Extracellular Matrices Decouple the Mechanical and Biochemical Effects of Muscle Contraction on Motor Neurons.*
Decision maker: Claude Opus 5.5 (Claude Code session), bioinformatics-workflow skill, case-spec route. I skipped the preflight because the request said to.
Spec: `case_spec.json`. Runner output: `summary.csv`, `run_status.json`, per-case folders. Validator: 30 records, 0 errors.

## What ran

| Case | Outcome | Route |
|---|---|---|
| GSE257540_biochem | completed | paper_aligned. One DESeq2 model `~ grp` on Control (C, n=5), spontaneous-twitch CM (SP, n=5) and exercised-muscle CM (EX, n=4). Three planned contrasts (FIG7c-e). |
| GSE257540_mech | completed | paper_aligned. DESeq2 `~ grp` on MagMA-actuated (MS, n=4) vs non-actuated control (MC, n=3) (FIG7i). |
| GSE281241 | refused at `design` | Unstimulated ChR2::tdTomato C2C12 vs WT C2C12 myotubes. This is a genotype or cell-line characterization with no exercise or contraction arm. The paper does not cite this series: it cites only GSE257540 (S4.8.p2, DA.p1). The link comes only from GEO (Series_pubmed_id, SuperSeries GSE281242). |

How the decisions were made:
- **Group identity.** GEO's "Low intensity biochem" is the NE samples: medium from unstimulated, spontaneously twitching muscle. "High intensity biochem" is the S samples: medium from optically stimulated (exercised) muscle. Both come from the GSE257540 Series_overall_design.
- **Alignment.** Matrix columns L1 and H1 correspond to titles LI1 and HI1. I matched them by deriving a key with `key_patterns` and setting `normalize_keys`. The match is exact; nothing was aligned by position.
- **Matrix.** The counts are nf-core STAR/Salmon gene counts that the submitter deposited already rounded to integers. They went into DESeq2 unchanged, which is the paper's input. The TPM file was not used.
- **QC exclusions (S4.10.p1 criteria, computed from the deposited counts):**
  - C4: rRNA fraction 0.78.
  - LI6: 1,536 reads.
  - HI4: 243K reads.
  - HI5: 495K reads, just under the 500K cutoff.
  - MC3: 613K reads with the most detected genes of any sample, which fits the low exon/intron criterion.

  That makes 5 exclusions, matching the paper's "n = 5".
- **Threshold.** The paper says only that DEGs used BH-adjusted p-values and gives no cutoff and no fold-change rule. I applied `workflow_default` (padj < 0.05, no LFC rule) and labelled it as such. As an audit I also counted genes at nominal  ... [3990 more characters]
