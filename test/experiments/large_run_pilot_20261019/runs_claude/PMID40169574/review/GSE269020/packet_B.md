# Review packet B (the analysis' decisions): GSE269020

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.2.genotype", "pairs_or_sets": 4, "samples_linked": 8, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast in the sequenced samples: GSE269020 contains only sedentary HFD-fed WT and KLF10^AKO iWAT (4 vs 4). The exercise (Ex vs Sed) groups of the paper were assayed by qPCR/western blot only.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE269020"], "assay": "bulk RNA-seq (Illumina NovaSeq 6000, PE150, Hisat2 -> featureCounts; Novogene)", "tissue": "inguinal white adipose tissue (iWAT)", "sample_inclusion": "HFD-fed male WT (KLF10 flox/flox control) and KLF10 adipocyte-specific knockout (KLF10^AKO) mice, sedentary (no exercise); n = 4 per group", "factors": {"genotype": ["WT", "KLF10AKO"]}, "primary_estimand": "Effect of adipocyte KLF10 knockout on the iWAT transcriptome of HFD-fed sedentary male mice (genetic estimand, not an exercise effect)", "planned_contrasts": ["KLF10AKO vs WT in HFD-fed mice without exercise (Fig. 5a legend; paper: 2907 up, 1639 down = 4546 DEGs)"], "exercise_contrast_in_rnaseq": "none: exercise (treadmill Ex vs Sed) appears only in physiology, RT-qPCR and western blot experiments (Fig. 4, Fig. 5d-g), not in the sequenced samples", "paper_method": "edgeR, Benjamini-Hochberg (S4.18.p1); Fig. 5 legend says two-sided Wald tests plus BH", "paper_threshold": {"metric": "padj", "cutoff": 0.05, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": true, "source_locator": "S4.18.p1 (Fig. 5a legend states only Padj < 0.05)"}, "paper_results": {"KLF10AKO_vs_WT": {"up": 2907, "down": 1639, "locator": "FIG5 a"}}}

reasoning: S4.18.p1: total RNA from iWAT of WT control and KLF10^AKO mice fed HFD; edgeR, BH, padj <= 0.05 and |log2FC| >= 1. FIG5 legend (a): 2907 up / 1639 down KLF10^AKO vs WT in iWAT of HFD-fed mice without exercise, n = 4 per group. DA.p1: GSE269020 holds the RNA-seq of Fig. 5a-c and Supplementary Fig. 5a,b. The exercise arms (Ex/Sed, Fig. 4) were never sequenced.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE269020\\GSE269020_gene_fpkm.txt.gz", "owned": true, "checks": ["DA.p1 names GSE269020 for Fig. 5a-c RNA-seq", "GEO: iWAT, male, HFD-fed, genotype Wildtype/KLF10AKO, 4+4 samples, matches n = 4 per group in FIG5", "contact institute Shanghai University of Sport, author Zhu J. as in DA.p1"], "accession": "GSE269020", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE269020\\GSE269020_metadata.csv"}

reasoning: Accession, tissue, sex, diet, genotype levels and n per group all match the paper's RNA-seq description.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 8, "n_metadata": 8, "coverage": 1.0, "unmatched_matrix_columns": ["gene_chr", "gene_start", "gene_end", "gene_length"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40169574\\GSE269020\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(WT|KO)-\\d+$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40169574\\GSE269020\\aligned\\design_metadata.csv", "sha256": "acc3e084d34c3817c6c180da873406ddf2c898496ea1e1a1b2c74ab9658b3851", "levels": {"grp": {"WT": 4, "KO": 4}}}}

reasoning: Matrix columns WT_1..KO_4; metadata titles WT-1..KO-4. key derived from title (groups joined with _) gives an exact match. grp from title; agrees with characteristics genotype (Wildtype/KLF10AKO).

### matrix (valid, not_started)

final: {"source": "GSE269020_gene_fpkm.txt.gz (only supplementary matrix)", "paper_input": "read counts into edgeR (S4.18.p1); raw counts not deposited", "matrix_type": "FPKM", "recommended_method": "limma on log2(FPKM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40169574\\GSE269020\\aligned\\aligned_matrix.csv", "sha256": "23bd9300a643ee26f1cbee576aa98cff0cb4cd8e0655a9d711f868e05eeb1153", "n_features": 54532, "n_samples": 8, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 76877.1678875718, "median": 0.0, "integer_fraction": 0.5698, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name says FPKM; data_processing: featureCounts counts then FPKM calculated; 57% of values are integers only because many are 0; max 76877 non-integer. Not counts, so edgeR on counts cannot be reproduced. Recorded for completeness; the case stops at design.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_contrast": "absent", "available_contrast": "grp KO vs WT (genetic, sedentary HFD only)", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40169574\\GSE269020\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: The request is how exercise affects gene expression. All 8 sequenced samples are sedentary HFD-fed mice differing only in genotype (GEO characteristics: treatment HFD-fed constant; genotype Wildtype/KLF10AKO; FIG5 legend: 'without exercise'). There is no exercise or training arm, so no exercise estimand can be identified. Running KO vs WT would answer a genetic question, not the requested exercise question; it is not manufactured as a substitute.

rejected alternatives: [{"value": "grp KO vs WT as exercise proxy", "reason_rejected": "genotype contrast in sedentary mice; not an exercise effect"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 8 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix type",
    "paper": "edgeR on read counts",
    "data": "only FPKM deposited",
    "disposition": "would block paper route; moot because case is refused at design"
  },
  {
    "item": "threshold",
    "paper": "S4.18.p1: padj <= 0.05 and |log2FC| >= 1",
    "data": "FIG5 legend states Padj < 0.05 only for the 2907/1639 counts",
    "disposition": "recorded; moot"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID40169574 / GSE269020

**Status: refused at `design`.** The sequenced samples contain no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE269020`: the series was downloaded into `E:/agent/mwangLab_pdf/data/GSE269020`. It has one matrix, `GSE269020_gene_fpkm.txt.gz`: 54,532 Ensembl genes by 8 samples.
- The case spec (`case_spec.json`) recorded these gates, and `execute` passed with 5 records and 0 validator errors:
  - `paper_reconstruction`
  - `ownership`
  - `alignment` (exact match on a key built from `title`, 8 of 8 samples)
  - `matrix` (FPKM)
  - `design` (refused)
- No DE executor or enrichment ran.

## Why refused
- The paper's RNA-seq covers iWAT from HFD-fed **sedentary** WT and KLF10^AKO male mice, n = 4 per group. Sources: S4.18.p1, the Fig. 5a legend ("without exercise") and DA.p1.
- In GEO, `treatment` is constant (HFD-fed) and `genotype` is Wildtype or KLF10AKO.
- The treadmill Ex vs Sed groups (Fig. 4, Fig. 5d-g) were measured only by physiology, RT-qPCR and western blot. They were never sequenced.
- The only estimable contrast is genetic (KO vs WT). It does not answer the exercise question, so it was not run as a substitute.

## DEG counts vs paper
- Paper, KLF10AKO vs WT: 2907 up and 1639 down (Fig. 5a, Padj < 0.05).
- The methods section (S4.18.p1) gives a different rule: padj <= 0.05 and |log2FC| >= 1 (edgeR, BH).
- Ours: not run, because there is no exercise contrast.

## Deviations
- None were executed.
- The paper's route could not have been reproduced anyway. It used edgeR on read counts, but only FPKM was deposited, so limma on log2(FPKM+1) would have been a declared deviation.
- The paper is inconsistent on the threshold: the Fig. 5a legend says Padj only, while S4.18.p1 adds |log2FC| >= 1.

## Tool problems
- None blocking.
- Minor: the metadata title (`WT-1`) and the matrix column (`WT_1`) differ only in separator. `inspect` reported `alignment_keys: []` rather than suggesting a `key_patterns` derivation. The fix was `key_patterns {"key": ["title", "^(WT|KO)-(\\d+)$"]}`.

