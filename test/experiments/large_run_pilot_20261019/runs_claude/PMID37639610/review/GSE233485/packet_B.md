# Review packet B (the analysis' decisions): GSE233485

## Mechanical flags

- none

## Stop reasons

- design (refused; claim type: exercise_arm): GSE233485 contains no exercised animals: all 35 samples are sedentary WT/PGC-1a mKO/mTG mice at 3 or 24 mo. The paper's exercise effects are proteomic (wheel running, ref 21; treadmill 25 mo, MassIVE MSV000092099; FIG4C/D, S1.4.p1). An mTG-vs-WT or age contrast is a genetic or aging estimand and must not be reported as an exercise effect.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE233485"], "assay": "bulk RNA-seq (TruSeq v2, HiSeq 2500 single-end, salmon v1.1.0, GRCm38) of gastrocnemius muscle (S3.6.p1, FIG1)", "samples": "WT, PGC-1a mKO and PGC-1a mTG male mice at 3 mo and 24 mo; n = 6 per group except mKO 3 mo n = 5 (FIG1 legend)", "factors": {"genotype": ["WT", "mKO", "mTG"], "age": ["3 mo", "24 mo"]}, "primary_estimand": "For GSE233485: age (24 vs 3 mo) and PGC-1a loss/gain-of-function effects on muscle transcription (S1.1.p1). The paper's exercise evidence is NOT in this series: exercise effects come from proteomics (wheel-running cohorts from ref 21, FIG4C; treadmill-trained vs sedentary 25 mo mice, TMT16plex, MassIVE MSV000092099, FIG4D, S3.15) and the RNA-seq is used only to show that mTG mimics the exercise pattern in the sedentary state (S1.4.p1, SI Fig S3H).", "planned_contrasts": ["WT 24 mo vs WT 3 mo (aging; S1.1.p1, FIG1E FDR<0.05 markers; no DEG count reported)", "mKO vs WT and mTG vs WT within age (PGC-1a dependence; S1.1.p1)", "No exercise contrast exists in GSE233485 (exercise = proteomics, FIG4C/D, S3.2, S3.15, DA.p1)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.01, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.7.p1"}, "paper_method": "edgeR on the count matrix, genes with >= 1 CPM in all 5-6 replicates (S3.7.p1; GEO data_processing); PCA/z-score clustering on log2 TPM (S3.8.p1)", "paper_results": "860 genes aligned with PC1/PC2; cluster 1 of mitochondrial genes; top GO terms include t ... [58 more characters]

reasoning: S0.p2 and S1.1.p1 describe the RNA-seq as young/old x WT/mKO/mTG. S1.4.p1 and the FIG4 legend: exercise results are proteomic (ref 21 data for wheel running; own TMT proteomics for treadmill in 25 mo mice, limma empirical Bayes). DA.p1 deposits RNA-seq in GSE233485 and proteomics in MassIVE MSV000092099. FDR < 0.01 (S3.7.p1) applies to the RNA-seq edgeR analysis; the FIG1 legend marks genes at FDR < 0.05.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE233485\\GSE233485_WT_mKO_mTG_3-24mo_Count_Matrix_TPM.tsv.gz", "owned": true, "checks": ["DA.p1 names GSE233485 as the paper's RNA-seq deposit", "GEO series: 35 gastrocnemius samples, WT/mKO/mTG x 3/24 mo, male, salmon GRCm38 release 100, matching S3.6.p1 and FIG1 (n=6, mKO 3 mo n=5)", "Matrix GSE233485_WT_mKO_mTG_3-24mo_Count_Matrix_TPM.tsv.gz: 35 columns whose group prefixes match the GEO group counts exactly", "The metadata input is a sample sheet derived from the matrix column names (prep_metadata.py) because the GEO records do not carry the animal IDs used as matrix column names"], "accession": "GSE233485", "metadata_file": "E:/agent/mwangLab_pdf/test/experiments/large_run_pilot_20261019/runs_claude/PMID37639610/sample_sheet_from_matrix_columns.csv"}

reasoning: Series, tissue, design and n match the paper; the only deposited matrix is the TPM file.

### alignment (valid, not_started)

final: {"mapping_level": "group (genotype x age) from matrix column prefixes; GSM-level mapping not determinable", "prefix_rules": {"WT_n": "WT 3 mo", "MCK_n": "mTG 3 mo", "MKO_n": "mKO 3 mo", "WSO_n": "WT 24 mo", "MCK_SO_n": "mTG 24 mo", "MKO_SO_n": "mKO 24 mo"}, "method": "exact:metadata_index", "n_aligned": 35, "n_metadata": 35, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37639610\\GSE233485\\aligned\\aligned_metadata.csv", "columns": {"geno": {"alias_of": "genotype"}, "agegrp": {"alias_of": "age", "recode": {"3mo": "Y", "24mo": "O"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37639610\\GSE233485\\aligned\\design_metadata.csv", "sha256": "b2220a7c933587390ce086f844bb064bc66f329d66d6cc0e82b28a98ba825c01", "levels": {"geno": {"WT": 12, "mTG": 12, "mKO": 11}, "agegrp": {"O": 18, "Y": 17}}}}

reasoning: The matrix columns encode genotype and age in their prefixes (MCK = muscle creatine kinase promoter PGC-1a transgene = mTG; MKO = muscle knockout; _SO / WSO = old). prep_metadata.py decodes them and verifies that the six group sizes equal the GEO counts (6/6/5/6/6/6; the unique n=5 group is mKO 3 mo, as in FIG1). Group labels are therefore reliable; individual GSM ids are not assigned.

rejected alternatives: [{"value": "align matrix columns to GSM ids via GEO description (WT_3mo_1 ...)", "reason_rejected": "matrix columns are animal IDs (MCK_3874, MKO_SO_23) absent from every GEO field; matching rep numbers would be position-based"}, {"value": "align by column order", "reason_rejected": "position-based alignment is forbidden"}]

### matrix (valid, not_started)

final: {"source": "GEO supplementary GSE233485_WT_mKO_mTG_3-24mo_Count_Matrix_TPM.tsv.gz", "paper_input": "edgeR on salmon counts (S3.7.p1); counts are not deposited, only TPM", "evidence": "every column sums to 1e6; non-zero values are non-integer (0.016% integers); 60.7% zeros explain the 0.607 integer fraction; file name and data_processing state TPM", "matrix_type": "TPM", "recommended_method": "limma (log2(TPM+1))", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37639610\\GSE233485\\aligned\\aligned_matrix.csv", "sha256": "28388321b046201f7919c42b6799774f90700410341ef5fe6849b7dbb28c1c1c", "n_features": 54416, "n_samples": 35, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 119431.0, "median": 0.0, "integer_fraction": 0.607, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Column sums are 1e6 and data_processing says the count matrix is comprised of TPM values. The paper's edgeR route would need counts, which are not deposited.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_contrast": "absent", "available_factors": "genotype (WT/mKO/mTG) x age (3/24 mo), all sedentary", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37639610\\GSE233485\\suitability\\suitability.md", "n_comparisons": 11, "n_analyzable": 11}}

reasoning: S0.p2, S1.1.p1 and FIG1: the RNA-seq design is age x genotype. S3.2 describes the exercise cohorts, which were profiled by proteomics (S3.15, FIG4C/D legend). The request asks for exercise effects on gene expression; this series cannot identify that estimand.

rejected alternatives: [{"value": "mTG vs WT as an exercise proxy (S1.4.p1, SI Fig S3H)", "reason_rejected": "PGC-1a overexpression is a genetic model, not exercise; the paper itself only uses it as a sedentary-state comparison"}, {"value": "24 mo vs 3 mo WT", "reason_rejected": "aging estimand, not exercise"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 35 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "exercise data modality",
    "paper": "exercise effects measured by proteomics (FIG4C/D; MassIVE MSV000092099; ref 21)",
    "data": "GSE233485 holds only sedentary genotype x age RNA-seq",
    "disposition": "blocks_estimand"
  },
  {
    "item": "matrix type",
    "paper": "edgeR on count matrix (S3.7.p1)",
    "data": "only TPM deposited",
    "disposition": "would_require_method_deviation"
  },
  {
    "item": "sample identifiers",
    "paper": "n per group (FIG1)",
    "data": "matrix uses animal IDs not present in GEO records; groups decodable from prefixes, GSM mapping not",
    "disposition": "group_level_only"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 37639610 / GSE233485

**Status: refused at `design`.** GSE233485 has no exercise contrast.

## What ran
1. `python -m tools.case_runner inspect GSE233485`: downloaded the series to `data/GSE233485`. It has one matrix, `GSE233485_WT_mKO_mTG_3-24mo_Count_Matrix_TPM.tsv.gz` (54,416 Ensembl genes x 35 samples).
2. `prep_metadata.py`: builds `sample_sheet_from_matrix_columns.csv`.
   - The matrix columns are animal IDs (`WT_1`, `MCK_3874`, `MKO_SO_23`, `WSO_13`, ...). None of them appear in any GEO sample field. The GEO descriptions are `WT_3mo_1`, `mTG_24mo_3`, and so on.
   - Genotype and age are encoded in the column prefixes: MCK = mTG, MKO = mKO, `_SO`/WSO = 24 mo.
   - The script decodes them and checks that the six group sizes equal the GEO counts (6/6/5/6/6/6). The unique n=5 group is mKO 3 mo, which matches the paper's FIG1 legend.
   - No GSM-level mapping is made, and nothing is matched by position.
3. `python -m tools.case_runner execute case_spec.json`: recorded these gates:
   - `paper_reconstruction`, `ownership`, `alignment` (35/35, exact on the sample sheet index) and `matrix` (TPM: column sums are 1e6 and `data_processing` says TPM) were all valid.
   - `design` was **refused**. The suitability report itself was `analyzable` for the genotype x age comparisons (11 comparisons).
   - The validator reported 0 errors on 5 records.

## Why refused
- All 35 samples are sedentary WT, PGC-1a mKO or PGC-1a mTG mouse gastrocnemius, at 3 or 24 months. The paper's RNA-seq estimand is aging x PGC-1a dosage (S1.1.p1, FIG1).
- The paper measures its exercise effects by **proteomics**, not in this series:
  - voluntary wheel endurance and resistance running, using previously published data (ref 21; FIG4C);
  - treadmill-trained vs sedentary 25 mo mice, TMT16plex with limma (FIG4D, S3.15), deposited in MassIVE MSV000092099 (DA.p1).
- mTG vs WT is a genetic model. The paper uses it only as a sedentary-state analogue (S1.4.p1, SI Fig S3H), so reporting it as an "exercise effect" would change the estimand. Both mTG vs WT and 24 vs 3 mo were rejected as candidates.

## DEG counts vs paper
- No contrasts were run, so there are no DEG counts.
- The paper's RNA-seq threshold is FDR < 0.01 with edgeR (S3.7.p1). It reports no DEG count for any contrast; it reports 860 PC-aligned genes.
- The paper has no RNA-seq exercise DEG count at all.

## Deviations
- The metadata input is a sample sheet derived from the matrix column names, not `GSE233485_metadata ... [1376 more characters]
