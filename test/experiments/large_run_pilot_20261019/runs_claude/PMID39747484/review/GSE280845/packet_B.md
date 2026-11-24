# Review packet B (the analysis' decisions): GSE280845

## Mechanical flags

- **pairing_key_candidate**: {"key": "characteristics_ch1.1.genotype (without characteristics_ch1.2.treatment) + suffix of title", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 4, "samples_linked": 8, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Samples per design level

### `ex`
- **EXE** (6): GSM8606524 / Exe_WT_rep3; GSM8606525 / Exe_WT_rep4; GSM8606526 / Exe_WT_rep5; GSM8606527 / Exe_KO_rep1; GSM8606528 / Exe_KO_rep2; GSM8606529 / Exe_KO_rep4
- **SED** (6): GSM8606518 / Sed_WT_rep1; GSM8606519 / Sed_WT_rep3; GSM8606520 / Sed_WT_rep4; GSM8606521 / Sed_KO_rep1; GSM8606522 / Sed_KO_rep2; GSM8606523 / Sed_KO_rep3

### `geno`
- **KO** (6): GSM8606521 / Sed_KO_rep1; GSM8606522 / Sed_KO_rep2; GSM8606523 / Sed_KO_rep3; GSM8606527 / Exe_KO_rep1; GSM8606528 / Exe_KO_rep2; GSM8606529 / Exe_KO_rep4
- **WT** (6): GSM8606518 / Sed_WT_rep1; GSM8606519 / Sed_WT_rep3; GSM8606520 / Sed_WT_rep4; GSM8606524 / Exe_WT_rep3; GSM8606525 / Exe_WT_rep4; GSM8606526 / Exe_WT_rep5

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE280845"], "assay": "bulk RNA-seq (DNBSEQ/BGISEQ-500, 50-bp SE), gastrocnemius, male mice", "factors": {"genotype": ["WT (fl/fl)", "cFeimin MKO"], "treatment": ["Sedentary", "90-min running at 60% max speed"]}, "sample_inclusion": "all 12 deposited samples (3 per genotype x exercise cell)", "primary_estimand": "acute-exercise (90-min run) effect on gastrocnemius gene expression in WT (fl/fl) mice; the paper's mechanistic question is how cFeimin MKO changes that response (Sln de-repression during exercise)", "planned_contrasts": ["Exe vs Sed within WT (exercise effect; GEO overall_design)", "Exe vs Sed within MKO (exercise effect in knockout)", "MKO vs WT within Exe and within Sed (genotype effect; abstract: Sln up in MKO during exercise)", "genotype x exercise interaction"], "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "GEO GSE280845 data_processing (authors' text): cutoff of log2 fold change (logFC) of +- 1 and a p-value < 0.05"}, "paper_method": "DESeq2 (v1.40.2) Wald test with contrast tests on StringTie gene counts (GEO data_processing)", "paper_results": "No full text: DEG counts not available. Abstract: cFeimin suppresses Sln expression during exercise via FOXC2; so Sln expected higher in MKO than WT after exercise."}

reasoning: No full text was available. Study map built from the PubMed abstract (efetch PMID 39747484) and the GEO series (summary, overall_design, per-sample characteristics, data_processing). GEO overall_design: gastrocnemius of Sed and 90-min Exe fl/fl (WT) and cFeimin MKO male mice. data_processing states DESeq2 Wald contrasts and |log2FC| 1 with raw p<0.05.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\prep\\GSE280845_RAWCountMatrix_fixed.csv.gz", "owned": true, "checks": ["GEO series title equals the paper title", "GEO summary equals the abstract", "contact Yiguo Wang, Tsinghua = corresponding author", "12 matrix columns = 12 GSM titles (one typo fixed)"], "accession": "GSE280845", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE280845\\GSE280845_metadata.csv"}

reasoning: GSE280845 title/summary are the paper's; single supplementary count matrix with columns named by sample title.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\aligned\\aligned_metadata.csv", "columns": {"ex": {"source": "title", "regex": "^(Sed|Exe)_(?:WT|KO)_rep\\d$", "recode": {"Sed": "SED", "Exe": "EXE"}}, "geno": {"source": "title", "regex": "^(?:Sed|Exe)_(WT|KO)_rep\\d$", "recode": {"WT": "WT", "KO": "KO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\aligned\\design_metadata.csv", "sha256": "46f1c0680b7ce750cd62da518cb5259ab0088013309e2c63b8c1ca331b492804", "levels": {"ex": {"SED": 6, "EXE": 6}, "geno": {"WT": 6, "KO": 6}}}}

reasoning: Exact match of matrix column names to GEO title. The deposited column Exe_KO_reap4 is a typo of title Exe_KO_rep4 (GSM8606529, the only unmatched title and the only unmatched column; both KO + 90-min running); renamed in prep/fix_column_typo.py without touching values. Title-derived ex/geno agree with the characteristics treatment/genotype columns (6/6 each).

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\aligned\\aligned_matrix.csv", "sha256": "031426b51cb4733a55bd452cb52c94981dc03376a92c26286e9781e2cd231334", "n_features": 43432, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 838179.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: 100% integers, max 838179, median 0; data_processing: tab-delimited text file including raw counts for each sample, StringTie gene read counting, then DESeq2: the same input the paper used.

### design (valid, not_started)

final: {"analysis_type": "factorial 2x2 (exercise x genotype), one model on all 12 samples", "formula": "~ ex + geno + ex:geno (cell-means)", "contrasts": [{"name": "ex_EXE_vs_SED_geno-WT", "control": "SED", "treatment": "EXE", "role": "primary"}, {"name": "ex_EXE_vs_SED_geno-KO", "control": "SED", "treatment": "EXE", "role": "exploratory"}, {"name": "geno_KO_vs_WT_ex-EXE", "control": "WT", "treatment": "KO", "role": "exploratory"}, {"name": "geno_KO_vs_WT_ex-SED", "control": "WT", "treatment": "KO", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: Request is the exercise effect; GEO overall_design defines Sed vs 90-min Exe in fl/fl WT and MKO. Primary = exercise within WT; the other cells' comparisons and the interaction are exploratory, fitted in one model. All male (GEO design), so no sex split.

rejected alternatives: [{"value": "pool genotypes for Exe vs Sed", "reason_rejected": "genotype is a manipulated factor the paper expects to change the exercise response; pooling would mix estimands"}, {"value": "refuse (no clean exercise contrast)", "reason_rejected": "WT Sed vs WT Exe is a clean acute-exercise contrast with n=3 per arm"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(ex) + C(geno)", "n_samples": 12, "n_columns": 3, "columns": ["Intercept", "ex_SED", "geno_WT"], "rank": 3, "full_rank": true, "residual_df": 9, "levels": {"ex": {"SED": 6, "EXE": 6}, "geno": {"WT": 6, "KO": 6}}, "cells": [{"cell": ["EXE", "KO"], "n": 3}, {"cell": ["EXE", "WT"], "n": 3}, {"cell": ["SED", "KO"], "n": 3}, {"cell": ["SED", "WT"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 12, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 12, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.genotype", "n_levels": 2, "status": "crossed", "crosstab": {"EXE": {"WT": 3, "cFeimin MKO": 3}, "SED": {"WT": 3, "cFeimin MKO": 3}}}, {"column": "characteristics_ch1.2.treatment", "n_levels": 2, "status ... [1569 more characters]

reasoning: Independent animals, one sample each; no batch, lane or date recorded in GEO; all male.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ ex + geno + ex:geno (joint cell model)", "paper_route": {"method": "DESeq2 Wald contrasts", "status": "reproduced"}, "deviations": ["pydeseq2 instead of R DESeq2 1.40.2"]}

reasoning: Paper used DESeq2 Wald contrast tests on raw counts; same route.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "effect_inclusive": true}, "threshold_source": "paper", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "effect_inclusive": true}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: Authors' GEO data_processing: |log2FC| >= 1 (stated as +- 1) and raw p < 0.05. Kept as raw p exactly; BH padj < 0.05 reported as a labelled audit rule.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\results\\joint\\DEG_results_ex_EXE_vs_SED_geno-KO.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\results\\joint\\DEG_results_ex_EXE_vs_SED_geno-WT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\results\\joint\\DEG_results_geno_KO_vs_WT_ex-EXE.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\results\\joint\\DEG_results_geno_KO_vs_WT_ex-SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\results\\joint\\DEG_results_ex_geno_EXE_KO_vs_SED_WT.csv"], "counts": {"joint/ex_EXE_vs_SED_geno-KO": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| >= 1", "n_tested": 24022, "n_significant": 545, "n_up": 328, "n_down": 217, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14707, "n_significant": 625, "n_up": 384, "n_down": 241, "deg_sanity": "ok"}}, "joint/ex_EXE_vs_SED_geno-WT": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| >= 1", "n_tested": 24022, "n_significant": 840, "n_up": 470, "n_down": 370, "deg_sanity": "ok"},  ... [1035 more characters]

reasoning: One DESeq2 model on all 12 samples; planned exercise-in-WT contrast plus every analyzable comparison (exploratory).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/ex_EXE_vs_SED_geno-WT", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "effect_inclusive": true}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\results\\enrichment_joint_ex_EXE_vs_SED_geno-WT\\ora\\DEG_results_ex_EXE_vs_SED_geno-WT_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\results\\enrichment_joint_ex_EXE_vs_SED_geno-WT\\ora\\DEG_results_ex_EXE_vs_SED_geno-WT_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\results\\enrichment_joint_ex_EXE_vs_SED_geno-WT\\ora\\DEG_results_ex_EXE_vs_SED_geno-WT_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\results\\enrichment_joint_ex_EXE_vs_SED_geno-WT\\ora\\DEG_results_ex_EXE_vs_SED_geno-WT_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 823 Mouse genes (direction=all, pvalue<0.05, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Negative Regulation Of Cell ... [1310 more characters]

reasoning: pathway view of the primary exercise response

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/ex_EXE_vs_SED_geno-WT", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39747484\\GSE280845\\results\\enrichment_joint_ex_EXE_vs_SED_geno-WT\\gsea\\DEG_results_ex_EXE_vs_SED_geno-WT_GSEA_Hallmark.csv"], "summary": "GSEA complete on 22632 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 42 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.63 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=2.24 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TGF_BETA_SIGNALING | NES=2.23 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=1.84 | NOM p=0.00e+00 | FDR q=1.89e-03 - HALLMARK_HYPOXIA | NES=1.80 | NOM p=0.00e+00 | FDR q=3.02e-03 - HALLMARK_MYC_TARGETS_V1 | NES=1.73 | NOM p=0.00e+00 | FDR q=5.04e-03 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.70 | NOM p=1.70e-03 | FDR q=5.86e-03 - HALLMARK_ANDROGEN_RESPONSE | NES=1.70 | NOM p=0.00e+00 | FDR q=5.26e-03 - HALLMARK_UV_RESPONSE_UP | NES=1.66 | NOM p=1.55e-03 | FDR q=7.20e-03 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.66 | NOM p=1.62e-03 | FDR q=6.70e-03 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NE ... [421 more characters]

reasoning: pathway view of the primary exercise response

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Comparison with the paper rests on the abstract and GEO text only; no DEG counts available from the paper.", "n=3 per cell; raw-p threshold is permissive."], "results": {"joint/ex_EXE_vs_SED_geno-KO": {"n_deg": 545, "up": 328, "down": 217, "rule": "pvalue < 0.05 and |log2FoldChange| >= 1", "audit_n": 625}, "joint/ex_EXE_vs_SED_geno-WT": {"n_deg": 840, "up": 470, "down": 370, "rule": "pvalue < 0.05 and |log2FoldChange| >= 1", "audit_n": 1116}, "joint/geno_KO_vs_WT_ex-EXE": {"n_deg": 291, "up": 188, "down": 103, "rule": "pvalue < 0.05 and |log2FoldChange| >= 1", "audit_n": 126}, "joint/geno_KO_vs_WT_ex-SED": {"n_deg": 116, "up": 94, "down": 22, "rule": "pvalue < 0.05 and |log2FoldChange| >= 1", "audit_n": 1}, "joint/ex_geno_EXE_KO_vs_SED_WT": {"n_deg": 128, "up": 48, "down": 80, "rule": "pvalue < 0.05 and |log2FoldChange| >= 1", "audit_n": 2}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"joint/geno_KO_vs_WT_ex-EXE": {"Sln": {"baseMean": 87.5709, "log2FoldChange": 3.7507, "padj": null, "pvalue": null}, "Foxc2": {"baseMean": 3.7407, "log2FoldChange": -0.8022, "padj": null, "pvalue": 0.372}}, "joint/ex_EXE_vs_SED_geno-WT": {"Sln": {"baseMean": 87.5709, "log2FoldChange": -0.8661, "padj": null, "pvalue": null}}}}

reasoning: Abstract names Sln (suppressed by cFeimin during exercise, i.e. expected up in MKO vs WT after exercise) and FOXC2 (binding partner).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix column name",
    "paper": "GEO title Exe_KO_rep4",
    "data": "matrix column Exe_KO_reap4",
    "disposition": "executable_without_change"
  },
  {
    "item": "library count",
    "paper": "extract_protocol says 18 libraries prepared",
    "data": "12 samples deposited",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID39747484 / GSE280845

**The comparison with the paper rests on the abstract only.** No full text was available. I used the PubMed abstract (efetch, saved as `abstract_PMID39747484.txt`) and the GEO series text (summary, overall_design, data_processing). The paper's DEG counts are not known, so no count comparison was possible.

## What ran
- Data: `GSE280845_RAWCountMatrix.csv.gz`. These are StringTie gene raw counts from 12 gastrocnemius samples of male mice, in a 2×2 design: fl/fl WT vs cFeimin MKO, crossed with Sedentary vs 90-min running. There are n=3 per cell, and every value is an integer.
- Prep: `prep/fix_column_typo.py` renames one matrix column, `Exe_KO_reap4`, to `Exe_KO_rep4` to match the GEO title of GSM8606529. No values were changed. After the rename, all 12 samples align exactly on `title`.
- Model: one pydeseq2 Wald model fitted on all 12 samples (`tools.joint_contrasts:run_joint_deseq2`, cell model `~ ex + geno + ex:geno`). The suitability verdict was analyzable for all 5 comparisons, and the sex check found only one sex (consistent with "male" in GEO).
- Primary contrast: Exe vs Sed in WT (`ex_EXE_vs_SED_geno-WT`). The other comparisons are exploratory.
- Threshold: the authors' rule as stated in GEO data_processing, raw p < 0.05 and |log2FC| ≥ 1 (source `paper`). The audit rule is BH padj < 0.05 with no fold-change cutoff.
- Enrichment (primary contrast only): ORA (GO BP/MF/CC, KEGG) and Hallmark GSEA both completed. Top GSEA sets were TNFα/NF-κB up (NES 2.63), mTORC1 up, TGF-β up, EMT down and IFN-α down, all with FDR < 0.001. This is a typical acute-exercise immediate-early and stress response.

## DEG counts (paper rule: p<0.05 & |log2FC|≥1; audit: padj<0.05)
| Comparison | Role | DEGs (up/down) | audit padj<0.05 | Paper |
|---|---|---|---|---|
| Exe vs Sed, WT | primary | 840 (470/370) | 1116 | not available (abstract only) |
| Exe vs Sed, MKO | exploratory | 545 (328/217) | 625 | n/a |
| MKO vs WT, Exe | exploratory | 291 (188/103) | 126 | n/a |
| MKO vs WT, Sed | exploratory | 116 (94/22) | 1 | n/a |
| interaction ex×geno | exploratory | 128 (48/80) | 2 | n/a |

Gene named in the abstract: **Sln**. Its direction agrees with the abstract. Sln is higher in MKO than WT after exercise (log2FC +3.75) and slightly lower after exercise in WT (log2FC −0.87). However, its p-value is NaN: DESeq2's Cook's-distance filter flagged the outlier sample Exe_KO_rep4, which has 568 counts against 44–58 in the other two Exe_KO sampl ... [1124 more characters]
