# Review packet B (the analysis' decisions): GSE123879

## Mechanical flags

- **possible_reversed_contrast**: {"contrast": "grp_MTG_vs_SED", "control": "SED", "treatment": "MTG", "note": "the control side reads as exercise or the test side as control"}
- **other_rule_matches_paper**: {"table": "joint/grp_EX_vs_SED", "paper": 1562, "applied": 900, "applied_rule": "padj < 0.05", "closest_rule": "padj<0.1", "closest_n": 1456, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "description", "pairs_or_sets": 5, "samples_linked": 15, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/grp_EX_vs_SED | 1562 | 900 | padj < 0.05 | 900 | 141 | 38 | 1456 | 2710 | 158 | 41 | 1355 | 0.064 | 0.217 |
| joint/grp_MTG_vs_SED | 5582 | 5878 | padj < 0.05 | 5878 | 1513 | 449 | 6816 | 6709 | 1520 | 449 | 5127 | 0.03 | 0.536 |

## Samples per design level

### `grp`
- **EX** (5): GSM3515066 / ExerciseQuad_RNAseq_rep1; GSM3515067 / ExerciseQuad_RNAseq_rep2; GSM3515068 / ExerciseQuad_RNAseq_rep3; GSM3515069 / ExerciseQuad_RNAseq_rep4; GSM3515070 / ExerciseQuad_RNAseq_rep5
- **MTG** (5): GSM3515071 / PGC1transgenic_RNAseq_rep1; GSM3515072 / PGC1transgenic_RNAseq_rep2; GSM3515073 / PGC1transgenic_RNAseq_rep3; GSM3515074 / PGC1transgenic_RNAseq_rep4; GSM3515075 / PGC1transgenic_RNAseq_rep5
- **SED** (5): GSM3515061 / ControlQuad_RNAseq_rep1; GSM3515062 / ControlQuad_RNAseq_rep2; GSM3515063 / ControlQuad_RNAseq_rep3; GSM3515064 / ControlQuad_RNAseq_rep4; GSM3515065 / ControlQuad_RNAseq_rep5

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE123879 (SuperSeries; RNA-seq SubSeries GSE123878)"], "assay": "bulk mRNA-seq (TruSeq stranded polyA, NextSeq 500 75bp SE) of quadriceps", "primary_estimand": "Effect of 4 weeks voluntary wheel running (Ex, harvested 4-6 h after last bout) vs sedentary wild-type controls (Con) on quadriceps gene expression in male C57BL/6J mice", "factors": {"grp": ["SED (sedentary WT control)", "EX (wheel-running WT)", "MTG (sedentary muscle-specific Pgc1a transgenic)"]}, "sample_inclusion": "n = 5 quadriceps per group (Fig 8A legend); all 15 deposited RNA-seq samples", "planned_contrasts": ["EX vs SED in quadriceps (S2.6.p1, Fig 8A left; paper: 779 up, 783 down = 1562 DEGs)", "MTG vs SED in quadriceps (S2.6.p1, Fig 8A right; paper: 2843 up, 2739 down = 5582 DEGs) - non-exercise comparison, secondary"], "repeated_measure_unit": "none; one quadriceps per independent mouse", "paper_method": "STAR (mm10) + DESeq2 via Illumina BaseSpace DESeq2 v1.1.0 app, direct pairwise comparisons Con vs Ex and Con vs mTg (S4.7.p1)", "normalization": "DESeq2 internal size factors on counts; FPKM used only for heatmaps/clustering (S4.7.p1)", "paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false, "source_locator": "S4.7.p1"}, "paper_results": {"EX_vs_SED": {"up": 779, "down": 783}, "MTG_vs_SED": {"up": 2843, "down": 2739}, "named_genes": "Acadl up and Myh4 down with exercise (S2.7.p1, Fig 9C)"}}

reasoning: S4.2.p1: male C57BL/6J mice, voluntary wheel running for 4 weeks from 8 weeks of age vs individually caged without wheels; Ex harvested 4-6 h after last bout; mTg vs WT littermates. S2.6.p1 + Fig 8A: quadriceps mRNA-seq, n=5/group, Ex and mTg each compared with sedentary wild-type controls. S4.7.p1: DESeq2, FDR-adjusted p < 0.05. S2.6.p1 writes p-value < 0.05 for the 779/783 counts, but the deposited GSE123878_ExerciseQuad_DifferentialGenes list (1562 genes = 779+783) has max padj 0.04998 and max raw p 0.0062, so the counts were made with padj < 0.05 as the Methods state. S4.11.p1 / S8.p1 name SuperSeries GSE123879.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\prep\\GSE123878_FpkmValues_clean.csv", "owned": true, "checks": ["S4.11.p1 deposits all RNA-seq/ChIP-seq/ATAC-seq in SuperSeries GSE123879", "GSE123879 is SuperSeries of GSE123878 (RNA-Seq, 15 samples: ControlQuad/ExerciseQuad/PGC1transgenic rep1-5)", "GSE123878 supplementary FpkmValues_AllSamples has 15 columns Control_1-5, Exercise_1-5, PGC1transgenic_1-5 matching the 15 GSMs", "GSE123878 data_processing restates STAR + DESeq2 FDR<0.05 as in S4.7.p1", "deposited ExerciseQuad / mTgQuad DifferentialGenes lists reproduce the paper counts 779/783 and 2843/2739"], "accession": "GSE123879", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE123878\\GSE123878_metadata.csv"}

reasoning: The RNA-seq samples of SuperSeries GSE123879 are exactly the 15 samples of SubSeries GSE123878; the metadata of that SubSeries (subset of the SuperSeries metadata) and its series-level FPKM matrix are used. ChIP-seq and ATAC-seq samples in the SuperSeries are not expression data and are out of scope. GSE123878_RAW.tar holds per-sample bedGraph coverage tracks only (no gene counts), so the only gene-level matrix is FPKM.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 15, "n_metadata": 15, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(Control|Exercise|PGC1transgenic)", "recode": {"Control": "SED", "Exercise": "EX", "PGC1transgenic": "MTG"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\aligned\\design_metadata.csv", "sha256": "d4df1d17fae0bf32dcaf3de118d88294e838d3aa6b84123751771d5b950eb1ac", "levels": {"grp": {"SED": 5, "EX": 5, "MTG": 5}}}}

reasoning: Matrix columns are Control_N / Exercise_N / PGC1transgenic_N; metadata titles are ControlQuad_RNAseq_repN / ExerciseQuad_RNAseq_repN / PGC1transgenic_RNAseq_repN. key is derived from title as <group>_<rep> and matched exactly. grp recoded from the title prefix, which agrees with characteristics genotype (wild type / PGC1a Tg(+)) and treatment (sedentary / exercise).

### matrix (valid, not_started)

final: {"source": "GSE123878_FpkmValues_AllSamples.xlsx (series supplementary; converted to csv; 21 Excel date-mangled gene IDs dropped by prep_fpkm.py)", "paper_input": "read counts from STAR into DESeq2 (S4.7.p1); counts not deposited", "matrix_type": "FPKM", "recommended_method": "limma on log2(FPKM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\aligned\\aligned_matrix.csv", "sha256": "5c1540f8f49c4eafa1d6348eb8897caac1bd3dc377d463d5b06094f2a37f1ff6", "n_features": 12508, "n_samples": 15, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 26391.6316283242, "median": 5.384084841716195, "integer_fraction": 0.0, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name says Fpkm; integer fraction 0.0, range 0-26392, non-integer values: linear FPKM. The paper's DESeq2 input (gene counts) is not deposited; RAW.tar contains only bedGraph tag tracks.

### design (valid, not_started)

final: {"analysis_type": "multi-group, one control", "design_column": "grp", "contrasts": [{"name": "grp_EX_vs_SED", "control": "SED", "treatment": "EX", "role": "primary"}, {"name": "grp_MTG_vs_SED", "control": "SED", "treatment": "MTG", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: Three groups of 5 sharing one sedentary WT control set. EX vs SED is the exercise estimand (primary); MTG vs SED is the paper's second planned comparison (genetic, not exercise) kept as secondary. All male (S4.2.p1).

rejected alternatives: [{"value": "grp_EX_vs_MTG", "reason_rejected": "not a paper comparison; the paper compares each model with sedentary controls only (S4.7.p1)"}, {"value": "two separate two-arm fits", "reason_rejected": "one control shared by two arms: one model with planned contrasts; difference from the paper's separate pairwise DESeq2 fits recorded as a deviation"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 15, "n_columns": 3, "columns": ["Intercept", "grp_MTG", "grp_SED"], "rank": 3, "full_rank": true, "residual_df": 12, "levels": {"grp": {"SED": 5, "EX": 5, "MTG": 5}}, "cells": [{"cell": ["EX"], "n": 5}, {"cell": ["MTG"], "n": 5}, {"cell": ["SED"], "n": 5}], "min_cell_size": 5, "missing_values": {}}, "confounding": []}

reasoning: Independent mice, one quadriceps each, randomly assigned to wheel/no wheel (S4.2.p1). No batch, lane or sex variation recorded in GEO metadata (all submitted Dec 14 2018, single platform). No covariates added.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (moderated t, empirical Bayes) on log2(FPKM+1)", "formula": "~ 0 + grp", "paper_route": {"method": "DESeq2 on STAR gene counts (BaseSpace DESeq2 v1.1.0)", "status": "blocked", "reason": "gene-level read counts not deposited in GEO; only FPKM matrix and bedGraph tracks; FPKM must not be rounded into counts"}, "deviations": ["limma on log2(FPKM+1) instead of DESeq2 on counts", "one joint 3-group model instead of separate pairwise fits", "21 date-mangled gene IDs dropped", "deposited FPKM matrix already restricted to 12,529 genes by the authors"], "transform": "log2(x+1)"}

reasoning: Matrix-method policy: FPKM -> log2(x+1) then limma. Paper route DESeq2 blocked by missing counts; run limma as a declared deviation.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "deviation_note": "Paper rule BH padj < 0.05 (S4.7.p1; confirmed by the deposited DE list) applied to limma results. Audit rule adds |FC| > 1.5 (Fig 8A red points: absolute FC > 1.5 and adjusted p < 0.05)."}

reasoning: S4.7.p1 FDR-adjusted p < 0.05, no fold-change cutoff; S2.6.p1 wording p-value < 0.05 is contradicted by the deposited list (max padj 0.04998). Fig 8A FC > 1.5 used only as a labelled audit rule.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 15, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\results\\joint\\DEG_results_grp_EX_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\results\\joint\\DEG_results_grp_MTG_vs_SED.csv"], "counts": {"joint/grp_EX_vs_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 12508, "n_significant": 900, "n_up": 520, "n_down": 380, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 12508, "n_significant": 141, "n_up": 110, "n_down": 31, "deg_sanity": "ok"}}, "joint/grp_MTG_vs_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 12508, "n_significant": 5878, "n_up": 2883, "n_down": 2995, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 12508, "n_significant": 1513, "n_up": 954, "n_down": 559, "deg_sanity": "ok"}}}}

reasoning: One limma model on log2(FPKM+1) with the three groups; planned contrasts EX vs SED (primary, exercise) and MTG vs SED (secondary).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_EX_vs_SED", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\results\\enrichment_joint_grp_EX_vs_SED\\ora\\DEG_results_grp_EX_vs_SED_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\results\\enrichment_joint_grp_EX_vs_SED\\ora\\DEG_results_grp_EX_vs_SED_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\results\\enrichment_joint_grp_EX_vs_SED\\ora\\DEG_results_grp_EX_vs_SED_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\results\\enrichment_joint_grp_EX_vs_SED\\ora\\DEG_results_grp_EX_vs_SED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 900 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Myofibril Assembly (GO:0030239) | padj=2.31e-06 | overlap=15/46 | genes=WDR1;ADPRHL1;ACTN2;TMOD4;TPM1;LMOD3;KLHL41;CSRP3;MYH3;MYL ... [1210 more characters]

reasoning: Paper runs GO/KEGG/Reactome enrichment (Metascape) on exercise DEGs (S4.7.p1, Fig 8E).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_EX_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31589602\\GSE123879\\results\\enrichment_joint_grp_EX_vs_SED\\gsea\\DEG_results_grp_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12508 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 20 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.95 | NOM p=0.00e+00 | FDR q=6.06e-03 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.79 | NOM p=0.00e+00 | FDR q=7.58e-03 - HALLMARK_ANGIOGENESIS | NES=1.79 | NOM p=5.52e-03 | FDR q=5.05e-03 - HALLMARK_MYOGENESIS | NES=1.72 | NOM p=0.00e+00 | FDR q=6.82e-03 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.68 | NOM p=0.00e+00 | FDR q=1.11e-02 - HALLMARK_ADIPOGENESIS | NES=1.61 | NOM p=3.13e-03 | FDR q=2.36e-02 - HALLMARK_APICAL_JUNCTION | NES=1.52 | NOM p=3.17e-03 | FDR q=4.37e-02 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.48 | NOM p=9.57e-03 | FDR q=6.07e-02 - HALLMARK_PEROXISOME | NES=1.46 | NOM p=2.20e-02 | FDR q=6.04e-02 - HALLMARK_APICAL_SURFACE | NES=1.46 | NOM p=4.44e-02 | FDR q=5.60e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=-1.68 | NOM p=2.64e-03 | FDR q=3.64e-02 - HALLMARK_MYC_TARGETS_V1 | NES=-1.60 | NOM p=0.00e+00 | FDR q=4.28e-02 - HA ... [396 more characters]

reasoning: Paper runs GO/KEGG/Reactome enrichment (Metascape) on exercise DEGs (S4.7.p1, Fig 8E).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["limma on log2(FPKM+1) replaces the paper's DESeq2 on counts; DEG counts are not expected to match exactly", "MTG vs SED is a genetic (Pgc1a transgene) comparison, not an exercise effect", "deposited FPKM matrix covers only 12,529 genes (pre-filtered by the authors); 21 Sept/March genes lost to Excel date conversion"], "results": {"joint/grp_EX_vs_SED": {"n_deg": 900, "up": 520, "down": 380, "rule": "padj < 0.05", "audit_n": 141}, "joint/grp_MTG_vs_SED": {"n_deg": 5878, "up": 2883, "down": 2995, "rule": "padj < 0.05", "audit_n": 1513}}, "paper_counts": {"joint/grp_EX_vs_SED": 1562, "joint/grp_MTG_vs_SED": 5582}, "comparison": {"joint/grp_EX_vs_SED": {"ours": 900, "paper": 1562}, "joint/grp_MTG_vs_SED": {"ours": 5878, "paper": 5582}}, "paper_gene_check": {"joint/grp_EX_vs_SED": {"Acadl": {"AveExpr": 7.9751, "log2FoldChange": 0.3473, "padj": 0.00443, "pvalue": 8.14e-05}, "Myh4": {"AveExpr": 12.8796, "log2FoldChange": -0.4332, "padj": 0.0199, "pvalue": 0.000845}, "Myh2": {"AveExpr": 8.8106, "log2FoldChange": 1.8669, "padj": 5.76e-06, "pvalue": 5.07e-09}}, "joint/grp_MTG_vs_SED": {"Ppargc1a": {"AveExpr": 3.8862, "log2FoldChange": 2.7519, "padj": 6.54e-10, "pvalue": 7.16e-12}}}}

reasoning: Paper counts from S2.6.p1 (779+783; 2843+2739). Acadl up and Myh4 down with exercise (S2.7.p1, Fig 9C); Myh2 (type IIa fibers increased by exercise, S2.6.p2) is up in the deposited Ex list; Ppargc1a is the transgene.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "threshold wording",
    "paper": "S2.6.p1: significantly induced ... (p-value < 0.05); S4.7.p1: FDR-adjusted p < 0.05",
    "data": "deposited ExerciseQuad DE list: 1562 genes, max padj 0.04998, max raw p 0.0062",
    "disposition": "executable_without_change"
  },
  {
    "item": "DE input",
    "paper": "DESeq2 on STAR counts",
    "data": "only FPKM (12,529 genes) and bedGraph tracks deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "gene IDs",
    "paper": "gene symbols",
    "data": "21 symbols converted to dates by Excel (2018-03-02 twice)",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 31589602 / GSE123879

The paper is "Dynamic enhancers control skeletal muscle identity and reprogramming" (PLoS Biol 2019, PMC6799888).

**Status: finished (declared deviation).** The case spec is `case_spec.json`. The runner log is `case_runner.log`. The validator passed: 12 records, 0 errors.

## What ran
- **Data.** GSE123879 is a SuperSeries (RNA-seq, ChIP-seq and ATAC-seq). Its RNA-seq part is SubSeries **GSE123878**: 15 quadriceps samples, 5 sedentary WT (Control), 5 wheel-running WT (Exercise) and 5 sedentary Pgc1a muscle transgenic (mTg).
  - The only gene-level matrix deposited is `GSE123878_FpkmValues_AllSamples.xlsx`: FPKM, 12,529 genes, already pre-filtered by the authors.
  - `_RAW.tar` holds bedGraph tracks only, with no counts.
- **Prep.** `prep/prep_fpkm.py` dropped 21 gene IDs that Excel had turned into dates (Sept*/March* genes). `2018-03-02` occurs twice, so the original symbols cannot be recovered. 12,508 genes remain.
- **Alignment.** The key was taken from the metadata title (`<group>_<rep>`) and matched exactly: 15/15 samples. Groups are SED, EX and MTG, n = 5 each.
- **Model.** One limma model (`~0 + grp`) on log2(FPKM+1), with planned contrasts:
  - EX vs SED (primary, the exercise effect)
  - MTG vs SED (secondary, genetic and not exercise)
- **Covariance.** None needed: independent mice, randomly assigned.
- **Enrichment for EX vs SED.**
  - ORA (Enrichr GO and KEGG) completed.
  - GSEA Hallmark completed. Top sets are OXPHOS, angiogenesis, myogenesis, IFN-gamma/alpha and adipogenesis (all up); UPR and MYC targets are down (FDR < 0.05).

## DEG counts vs the paper
Paper threshold: DESeq2 BH padj < 0.05, no fold-change rule (S4.7.p1). We applied the same rule to the limma results (`paper_on_deviation_route`).

| Contrast | Ours (up/down) | Paper (up/down) | Audit: padj<0.05 & \|FC\|>1.5 |
|---|---|---|---|
| EX vs SED | 900 (520/380) | 1562 (779/783) | 141 (deposited DESeq2 list: 182) |
| MTG vs SED | 5878 (2883/2995) | 5582 (2843/2739) | 1513 (deposited: 2334) |

Comparison with the authors' deposited DESeq2 lists (`*_DifferentialGenes`):
- **EX vs SED:** 868 of our 900 DEGs are in the paper's list. On shared genes, log2FC r = 0.961 and sign agreement is 100%.
- **MTG vs SED:** 5362 of our 5878 DEGs are in the paper's list. r = 0.956, sign agreement 100%.
- **Named genes, all in the paper's direction:**
  - Acadl up (log2FC 0.35, padj 0.004)
  - Myh4 down (log2FC -0.43, padj 0.020)
  - Myh2 up (log2FC 1.87)
  - P ... [1661 more characters]
