# Review packet B (the analysis' decisions): GSE226005

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.4.treatment", "n_values": 3, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "grp", "n_values": 6, "max_repeat": 2, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): GSE226005 contains no exercise contrast: all 12 samples are human IMR90 fibroblasts (Senescent/Young, Hypoxia/Normoxia, 2-DG+Hypoxia/Hypoxia control). The paper's exercise estimand (running vs sedentary mouse gastrocnemius, snRNA-seq, S2.7.p1, S5.15.p1) is not in this series, so no exercise effect can be identified from these data. Analyzing a senescence or hypoxia contrast would not answer the exercise question.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE226008 (SuperSeries, DA.p1)", "GSE226005 (RNA-seq SubSeries of GSE226008; GEO Series_pubmed_id 40388671)"], "primary_estimand": "Exercise estimand of the paper: effect of 2-month treadmill running vs sedentary on gene expression in gastrocnemius muscle of 11-month-old (13-month at sacrifice) female C57BL/6 mice, measured by snRNA-seq (n = 2 mice per group), per cell type and globally (S2.7.p1, FIG7, S5.2.p1, S5.15.p1).", "planned_contrasts": ["Running vs Sedentary, mouse gastrocnemius snRNA-seq, per cell type (19 cell types) and global; Seurat FindMarkers Wilcoxon (S5.15.p1; DEG counts only in Figure S30B, not in text)", "Non-exercise bulk RNA-seq contrasts in IMR90 human fibroblasts (S2.1-S2.3, FIG2): Senescent vs Young, Hypoxia vs Normoxia, 2-DG+Hypoxia vs Hypoxia control (S5.12.p1)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.25, "inclusive": false, "source_locator": "S5.15.p1 (running vs sedentary per cell type: |log2FC| > 0.25 and adjusted P < 0.05; global: |log2FC| > 0.15 and adjusted P < 0.05)"}, "paper_method": "Exercise: Seurat 4.1.1 FindMarkers Wilcoxon rank-sum on snRNA-seq nuclei (S5.14.p1, S5.15.p1). Bulk IMR90 RNA-seq: featureCounts + DESeq2 1.34.0, |log2FC| > 1 or 0.58 and padj < 0.05 (S5.12.p1).", "sample_inclusion": "Exercise arm: sedentary vs running mice, n = 2 per group for snRNA-seq (FIG7 H). Not part of GSE226005.", "paper_results": "Adipocytes had the most running DEGs  ... [101 more characters]

reasoning: The paper's only exercise transcriptome is mouse gastrocnemius snRNA-seq of running vs sedentary mice (S2.7.p1, FIG7 H-N, S5.9.p1, S5.14.p1, S5.15.p1). The bulk RNA-seq (S5.12.p1) is human IMR90 fibroblasts for senescence/hypoxia/glycolysis-inhibition experiments (FIG2). DA.p1 names only the SuperSeries GSE226008; GSE226005 is its RNA-seq SubSeries (family.soft: 'SubSeries of: GSE226008'; overall design 'RNA-seq data for IMR90 cells during replicative senescence, upon hypoxia and 2-DG treatment').

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40388671\\GSE226005_merged_normalized.csv", "owned": true, "checks": ["GEO Series_pubmed_id = 40388671", "GSE226005 is a SubSeries of GSE226008, the accession named in DA.p1", "12 GSMs = IMR90 bulk RNA-seq (Senescent/Young, Hypoxia/Normoxia, 2-DG+Hypoxia/Hypoxia control), 2 replicates each, matching S5.12.p1 and FIG2", "No mouse, muscle, running or sedentary samples in this series (organism_ch1 = Homo sapiens for all 12; cell line IMR90)"], "accession": "GSE226005", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE226005\\GSE226005_metadata.csv"}

reasoning: The series belongs to the paper, but it holds only the cell-line bulk RNA-seq arm, not the exercise snRNA-seq samples.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40388671\\GSE226005\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^IMR90_([^_]+)_rep\\d\\(RNA-seq\\)$", "recode": {"Senescent": "SEN", "Young": "YNG", "Hypoxia": "HYP", "Normoxia": "NOR", "2-DG": "DG", "Control1": "CTL1"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40388671\\GSE226005\\aligned\\design_metadata.csv", "sha256": "fcf2a677560d08b479f1da5e13995e5f557dd685def5a8208e1cc1e835e19032", "levels": {"grp": {"SEN": 2, "YNG": 2, "HYP": 2, "NOR": 2, "DG": 2, "CTL1": 2}}}}

reasoning: The prep script names each tar member's column by its GSM id, which equals the metadata index (exact match, no position use). grp is parsed from the GEO title.

### matrix (valid, not_started)

final: {"matrix_type": "DESeq2 size-factor-normalized counts (non-integer), normalized separately per experiment batch", "recommended_method": "limma on log2(x+1) (raw counts not deposited); not run because the case stops at design", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40388671\\GSE226005\\aligned\\aligned_matrix.csv", "sha256": "896e55e597687a982c597c1232f8a22089037bb843626a7fe984f2aa9cbdb3e1", "n_features": 17453, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 25788, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1281228.05434238, "median": 363.962982736632, "integer_fraction": 0.0058, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Values are non-integer (e.g. A1BG 17.449); data_processing: 'featureCounts ... normalized with DESeq2 (version 1.34.0) ... tab-delimited text files include normalized values for each sample'. Gene sets differ across sample groups (25,788 missing cells in the merged 17,453 x 12 matrix), consistent with per-experiment filtering and normalization.

### design (refused, not_started)

final: {"suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40388671\\GSE226005\\suitability\\suitability.md", "n_comparisons": 15, "n_analyzable": 0}}

reasoning: The request is the exercise effect as the paper intends. The paper measures it only in mouse muscle snRNA-seq (FIG7 H-N), deposited outside GSE226005 (presumably another SubSeries of GSE226008). No metadata column or title in GSE226005 records running, training, sedentary, mouse or muscle.

rejected alternatives: [{"value": "grp_SEN_vs_YNG (replicative senescence)", "reason_rejected": "aging/senescence of a cell line, not exercise"}, {"value": "grp_HYP_vs_NOR (hypoxia)", "reason_rejected": "hypoxic culture is not an exercise intervention; the paper does not treat it as an exercise proxy"}, {"value": "grp_DG_vs_CTL1 (2-DG glycolysis inhibition)", "reason_rejected": "pharmacological glycolysis inhibition, not exercise"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/15 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "Exercise data location",
    "paper": "Running vs sedentary snRNA-seq of mouse gastrocnemius (S2.7.p1, S5.15.p1); DA.p1 points to SuperSeries GSE226008",
    "data": "GSE226005 is the human IMR90 bulk RNA-seq SubSeries only (senescence, hypoxia, 2-DG)",
    "disposition": "blocks_estimand"
  },
  {
    "item": "Deposited matrix scale",
    "paper": "DESeq2 on featureCounts counts (S5.12.p1)",
    "data": "per-sample DESeq2-normalized values only; no raw counts",
    "disposition": "not_evaluated_case_refused"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 40388671 / GSE226005

**Status: refused at the `design` gate. GSE226005 has no exercise contrast.**

## What ran
1. `python -m tools.case_runner inspect GSE226005`: cached metadata, family.soft and `_RAW.tar` (12 per-sample `*_normalized.txt.gz`). Inspect found no candidate matrix, because the tar merge skipped all 12 members (see Tool problems).
2. `prep_merge_tar.py` (listed in `prep_scripts`) merged the 12 tar members, reading them as tab-delimited with the title line skipped. The result is `GSE226005_merged_normalized.csv`: 17,453 genes x 12 GSMs, with 25,788 missing cells because each experiment pair was filtered and normalized on its own.
3. `python -m tools.case_runner execute case_spec.json`:
   - Gates recorded: `paper_reconstruction`, `ownership`, `alignment` (exact on the metadata index, 12/12), `matrix`, then `design` = `refused`.
   - Validator: 5 records, 0 errors.
   - Route `stopped`. Records are in `GSE226005/`, and `summary.csv` is written.

## Why refused
- **Paper's exercise estimand:** 2-month treadmill running vs sedentary in 11-month-old female C57BL/6 mice (S5.2.p1). It was measured by snRNA-seq of gastrocnemius muscle, n = 2 per group (S2.7.p1, FIG7 H-N).
- **Paper's DE route for it:** Seurat FindMarkers Wilcoxon per cell type at |log2FC| > 0.25 and padj < 0.05, and globally at |log2FC| > 0.15 and padj < 0.05 (S5.15.p1).
- **What GSE226005 holds instead:** it is the human IMR90 fibroblast bulk RNA-seq SubSeries of SuperSeries GSE226008 (DA.p1). Its 12 samples, 2 per group, are:
  - Senescent and Young
  - Hypoxia and Normoxia
  - 2-DG+Hypoxia and Hypoxia "Control1"
- No sample in this series is mouse, muscle, running or sedentary. The senescence, hypoxia and 2-DG contrasts are not exercise, and the paper does not use them as an exercise proxy. They were recorded as rejected candidates.
- The exercise snRNA-seq is presumably in another SubSeries of GSE226008. It was not examined, because it is outside this task.

## DEG counts vs paper
- **Ours:** none computed (refused before execution).
- **Paper:** gives running DEG counts only in Figure S30B (adipocytes had the most), not in the text.
- **Paper threshold:** padj < 0.05 and |log2FC| > 0.25 per cell type; 0.15 for global DEGs (S5.15.p1).
- The bulk IMR90 threshold, |log2FC| > 1 or 0.58 with padj < 0.05 (S5.12.p1), does not apply to exercise.

## Deviations
- The matrix was built by a prep script, not by the runner's tar merge.
- The matrix gate recorded DESeq2-nor ... [925 more characters]
