# Review packet B (the analysis' decisions): GSE214542_pretreatment

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.3.treatment", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "grp", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.3.treatment", "pairs_or_sets": 3, "samples_linked": 9, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"data_processing": ["A cDNA library constructed by technology from the pooled RNA from midbrain samples of mouse was sequenced run with Illumina sequence platform. Prior to assembly, the low quality reads(1,reads containing sequencing adaptors; 2,reads containing sequencing primer;3, nucleotide with q quality score lower than 20) were removed.,We aligned reads of samples to the UCSC (http://genome.ucsc.edu/) C57BL_6NJ mouse reference genome using HISAT package.,Th ... [709 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: every sequenced sample is a sedentary mouse given vehicle, MPTP and/or injected recombinant irisin (GEO treatment field; S2.5.p1). Exercise exists only in the human serum cohort (S2.1.p1), which has no transcriptome. Irisin injection is not exercise; an irisin-vs-vehicle contrast would answer a different (pharmacological) estimand.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE214542"], "assay": "bulk RNA-seq of mouse nigral/midbrain tissue (S4.16.p1); GEO series holds two experiments: irisin pre-treatment (Control/MPTP/Irisin+MPTP, n=3 each) and irisin delayed treatment (Control/Irisin/MPTP/MPTP+Irisin, n=3 each)", "primary_estimand": "Effect of exogenous recombinant irisin (i.p. 200 ug/kg/d, 5 days) on the midbrain transcriptome of MPTP-treated mice (S2.5.p1, FIG4). Exercise appears only in the human cohort (S2.1.p1: 23 PD patients, 12-week exercise, serum irisin ELISA, no transcriptomics). No sequenced sample received exercise.", "factors": {"treatment": ["vehicle (ddH2O)", "MPTP", "irisin+MPTP (pre)", "irisin alone (delayed experiment)", "MPTP then irisin (delayed)"]}, "sample_inclusion": "male C57BL/6 mice, 6 weeks (GEO characteristics); n=3 per group", "planned_contrasts": ["Irisin+MPTP vs MPTP (pre-treatment), GSEA only (S2.5.p1, Supplementary Fig. 3a-b, Fig. 4a); paper reports no DEG count", "MPTP+Irisin vs MPTP (delayed treatment), GSEA only (S2.5.p1, Supplementary Fig. 3c-d, Fig. 4b); paper reports no DEG count"], "repeated_measure_unit": "none (independent animals)", "paper_method": "featureCounts read counts; downstream analysis in R (S4.16.p1), DE method not named; GEO data_processing: StringTie/edgeR expression, DE |log2FC| >= 1 and p < 0.05", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "effect_inclusive": true, "source_locator ... [223 more characters]

reasoning: The paper studies irisin as an exercise-induced myokine. Exercise is applied only to human PD patients (S2.1.p1, Table 1) whose readout is serum irisin and clinical scores. The RNA-seq (S2.5.p1, S4.16.p1, DA.p1 -> GSE214542) compares MPTP mice with and without injected recombinant irisin, so its estimand is a pharmacological irisin effect, not an exercise effect.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36720890\\prep\\GSE214542_1_counts.csv", "owned": true, "checks": ["DA.p1 names GSE214542", "GEO: midbrain, Mus musculus C57BL/6 male, NovaSeq 6000 matches S4.16.p1", "groups Control/MPTP/Irisin_MPTP match the FIG1/FIG4 pre-treatment design", "file 1 holds the 9 pre-treatment samples (titles *_M_rep*)"], "accession": "GSE214542", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE214542\\GSE214542_metadata.csv"}

reasoning: Accession named in the data-availability statement; tissue, platform and group structure agree with the paper.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 9, "n_metadata": 21, "coverage": 0.4286, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM6611235", "GSM6611236", "GSM6611237", "GSM6611238", "GSM6611239", "GSM6611240", "GSM6611241", "GSM6611242", "GSM6611243", "GSM6611244", "GSM6611245", "GSM6611246"], "excluded_samples": {"GSM6611235": "delayed-treatment experiment; not in file 1", "GSM6611236": "delayed-treatment experiment; not in file 1", "GSM6611237": "delayed-treatment experiment; not in file 1", "GSM6611238": "delayed-treatment experiment; not in file 1", "GSM6611239": "delayed-treatment experiment; not in file 1", "GSM6611240": "delayed-treatment experiment; not in file 1", "GSM6611241": "delayed-treatment experiment; not in file 1", "GSM6611242": "delayed-treatment experiment; not in file 1", "GSM6611243": "delayed-treatment experiment; not in file 1", "GSM6611244": "delayed-treatment experiment; not in file 1", "GSM6611245": "delayed-treatment experiment; not in file 1", "GSM6611246": "delayed-treatment experiment; not in file 1"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36720890\\GSE214542_pretreatment\\aligned\\aligned_metadata_kept.csv", "columns": {"grp": {"source": "title", "regex": "^(Control_M|Irisin_MPTP_M|MPTP_M)_rep\\d$", "recode": {"Control_M": "CTRL", "Irisin_MPTP_M": "IRISMPTP", "MPTP_M": "MPTP"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36720890\\GSE214542_pr ... [179 more characters]

reasoning: Count columns of file 1 renamed to GEO titles by prep/extract_counts.py (count.MPTP1_M -> MPTP_M_rep1, confirmed by best log-count/FPKM correlation with FPKM.MPTP_M_rep1). Exact match on title; group from the title prefix, consistent with the characteristics treatment field.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36720890\\GSE214542_pretreatment\\aligned\\aligned_matrix.csv", "sha256": "fa2fc33c7f2212396801c4a6ebf996c98eb4e4e950e60dfe62ea0fb6e6f2daba", "n_features": 33829, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2500054.0, "median": 55.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: The deposited file mixes FPKM.* and count.* columns; the count.* columns are 100% integer with library sizes 66-76M. Paper S4.16.p1 states featureCounts read counts as input; GEO data_processing says StringTie. Integer count columns used; FPKM columns not used.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36720890\\GSE214542_pretreatment\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: The request is the exercise effect as the paper intends; the paper never sequences exercised animals or people.

rejected alternatives: [{"value": "grp IRISMPTP vs MPTP as an exercise proxy", "reason_rejected": "irisin i.p. is a pharmacological intervention, not an exercise exposure; relabelling it would misstate the estimand"}, {"value": "grp MPTP vs CTRL", "reason_rejected": "neurotoxin model contrast, unrelated to exercise"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "expression quantification",
    "paper": "featureCounts read counts (S4.16.p1)",
    "data": "GEO data_processing: HISAT2/StringTie, mm9, FPKM + counts",
    "disposition": "recorded_only"
  },
  {
    "item": "exercise in RNA-seq",
    "paper": "exercise only in the human cohort (S2.1.p1)",
    "data": "no exercise arm among the 21 GEO samples",
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
