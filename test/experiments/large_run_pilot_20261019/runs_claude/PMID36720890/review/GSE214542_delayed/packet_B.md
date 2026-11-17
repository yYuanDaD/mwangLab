# Review packet B (the analysis' decisions): GSE214542_delayed

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.3.treatment", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "grp", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.3.treatment", "pairs_or_sets": 3, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"data_processing": ["A cDNA library constructed by technology from the pooled RNA from midbrain samples of mouse was sequenced run with Illumina sequence platform. Prior to assembly, the low quality reads(1,reads containing sequencing adaptors; 2,reads containing sequencing primer;3, nucleotide with q quality score lower than 20) were removed.,We aligned reads of samples to the UCSC (http://genome.ucsc.edu/) C57BL_6NJ mouse reference genome using HISAT package.,Th ... [709 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: groups are vehicle, irisin injection, MPTP, and MPTP followed by irisin injection (GEO treatment field). No sample was exercised; exercise appears only in the human serum cohort (S2.1.p1) without transcriptomics.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE214542"], "assay": "bulk RNA-seq of mouse midbrain, irisin delayed-treatment experiment (Control/Irisin/MPTP/MPTP+Irisin, n=3 each)", "primary_estimand": "Effect of delayed exogenous irisin on the midbrain transcriptome of MPTP-treated mice (S2.5.p1, FIG4b). No exercise arm.", "planned_contrasts": ["MPTP+Irisin vs MPTP (delayed treatment), GSEA only (S2.5.p1, Supplementary Fig. 3c-d, Fig. 4b); no DEG count reported"], "paper_method": "featureCounts counts; R, method not named (S4.16.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "effect_inclusive": true, "source_locator": "GEO data_processing only"}, "paper_results": "GSEA only; no DEG counts"}

reasoning: Same paper; second experiment of the series. Exercise appears only in the human cohort (S2.1.p1).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36720890\\prep\\GSE214542_2_counts.csv", "owned": true, "checks": ["DA.p1 names GSE214542", "file 2 holds the 12 delayed-treatment samples (titles CONTROL/IRISIN/MPTP/MPTP_IRISIN_rep*)"], "accession": "GSE214542", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE214542\\GSE214542_metadata.csv"}

reasoning: Same accession; group structure matches the delayed-treatment design (FIG1, FIG4b).

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 12, "n_metadata": 21, "coverage": 0.5714, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM6611226", "GSM6611227", "GSM6611228", "GSM6611229", "GSM6611230", "GSM6611231", "GSM6611232", "GSM6611233", "GSM6611234"], "excluded_samples": {"GSM6611226": "pre-treatment experiment; not in file 2", "GSM6611227": "pre-treatment experiment; not in file 2", "GSM6611228": "pre-treatment experiment; not in file 2", "GSM6611229": "pre-treatment experiment; not in file 2", "GSM6611230": "pre-treatment experiment; not in file 2", "GSM6611231": "pre-treatment experiment; not in file 2", "GSM6611232": "pre-treatment experiment; not in file 2", "GSM6611233": "pre-treatment experiment; not in file 2", "GSM6611234": "pre-treatment experiment; not in file 2"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36720890\\GSE214542_delayed\\aligned\\aligned_metadata_kept.csv", "columns": {"grp": {"source": "title", "regex": "^(CONTROL|IRISIN|MPTP|MPTP_IRISIN)_rep\\d$", "recode": {"CONTROL": "CTRL", "IRISIN": "IRIS", "MPTP": "MPTP", "MPTP_IRISIN": "MPTPIRIS"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36720890\\GSE214542_delayed\\aligned\\design_metadata.csv", "sha256": "1fdedf41113fdf958c9c6275049bc6c9f011524a515f88b3a440e1230c2613ba", "levels": {"grp": {"CTRL": 3, "IRIS": 3, "MPTP": 3, "MPTPIRIS": 3}}}}

reasoning: Count columns renamed to GEO titles (prep/extract_counts.py); exact match on title.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36720890\\GSE214542_delayed\\aligned\\aligned_matrix.csv", "sha256": "469dd71d345a0dd24ae89691b9c4883027017b5116af814b6f08a2d146ad1138", "n_features": 55385, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1983051.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: count.* columns of file 2 are integer read counts (FPKM.* columns ignored); paper S4.16.p1 states featureCounts counts.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36720890\\GSE214542_delayed\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: The request asks for the exercise effect; the data hold none.

rejected alternatives: [{"value": "grp IRIS vs CTRL or MPTPIRIS vs MPTP as an exercise proxy", "reason_rejected": "injected recombinant irisin is not exercise; it would answer a pharmacological estimand"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "exercise in RNA-seq",
    "paper": "exercise only in the human cohort (S2.1.p1)",
    "data": "no exercise arm among the 12 delayed-experiment samples",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 36720890 / GSE214542

**Status: refused at `design` (both cases).** There is no exercise contrast in the sequenced samples.

## What ran
- `case_runner inspect GSE214542`: downloaded the series to `E:/agent/mwangLab_pdf/data/GSE214542`. It holds two deposited files and 21 GSMs (male C57BL/6 midbrain, NovaSeq 6000).
  - File 1 (`GSE214542_1_genes_fpkm_expression.txt.gz`) is the irisin pre-treatment experiment: Control_M / MPTP_M / Irisin_MPTP_M, n=3 each.
  - File 2 (`GSE214542_2_genes_fpkm_expression.txt.gz`) is the delayed-treatment experiment: CONTROL / IRISIN / MPTP / MPTP_IRISIN, n=3 each.
- `prep/extract_counts.py` keeps only the integer `count.*` columns of each file and renames them to the GEO titles. One count column was mislabelled `count.MPTP1_M`. Its log-count profile correlates best with `FPKM.MPTP_M_rep1`, so it was renamed `MPTP_M_rep1`.
- `case_runner execute case_spec.json` ran two cases, `GSE214542_pretreatment` and `GSE214542_delayed`.
  - Gates recorded: paper_reconstruction, ownership, alignment (exact on `title`, 9/9 and 12/12 samples), matrix (raw counts) and design. Design is refused in both cases.
  - The contract validator reported 10 records and 0 errors.
  - Suitability called both designs analyzable. It covered only the irisin/MPTP group comparisons; none of them is about exercise.

## Why it was refused
- Exercise appears only in the human cohort (S2.1.p1, Table 1): 23 PD patients did 12 weeks of exercise. Their readouts are serum irisin by ELISA, UPDRSIII and BBS. That cohort has no transcriptome.
- Every RNA-seq sample is a sedentary mouse given vehicle, MPTP and/or recombinant irisin by i.p. injection (GEO treatment field; S2.5.p1, S4.16.p1).
- Using irisin injection as a stand-in for exercise would answer a different, pharmacological question. That alternative is recorded as a rejected candidate.

## DEG counts vs paper
- None computed (refused).
- The article reports only GSEA (Supplementary Fig. 3, Fig. 4a-b). It gives no DEG counts or DEG gene lists for the two irisin-vs-MPTP contrasts, so there is nothing to compare.
- The paper's threshold appears only in GEO data_processing, not in the article: |log2FC| >= 1 and p < 0.05 (raw p). It is recorded in paper_reconstruction.

## Deviations
- Input: I used the deposited integer `count.*` columns and ignored the FPKM columns. The paper (S4.16.p1) says featureCounts; GEO data_processing says HISAT/StringTie on mm9. This is recorded as a discrepancy (`recorded_ ... [1234 more characters]
