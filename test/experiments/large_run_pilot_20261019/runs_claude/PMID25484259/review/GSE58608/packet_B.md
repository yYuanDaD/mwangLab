# Review packet B (the analysis' decisions): GSE58608

## Mechanical flags

- **unused_subject_like_column**: {"column": "subject", "n_values": 12, "max_repeat": 2, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "subject", "across": "characteristics_ch1.3.biopsy location", "pairs_or_sets": 12, "samples_linked": 24, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"characteristics_ch1.2.exercise status": ["untrained"]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm): GSE58608 holds only pre-training biopsies (T1 and U1, all 'untrained'); no post-training sample exists in this series, so the paper's T2 vs T1 training estimand cannot be identified from it alone. U1 vs T1 is a baseline leg comparison, not an exercise contrast. Its 12 T1 samples are analyzed with the post-training samples in the GSE60591 SuperSeries case.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE58608", "GSE60590", "GSE60591"], "accession_roles": {"GSE58608": "RNA-seq, pre-training biopsies of both legs (T1 = leg to be trained, U1 = untrained leg) for 12 subjects; S5.4.p2 notes a baseline subset (n=12) analyzed earlier", "GSE60590": "RNA-seq, 22 post-training trained-leg biopsies (T2) plus 11 pre-training T1 biopsies of the other 11 subjects", "GSE60591": "GEO SuperSeries joining GSE58608 + GSE60590 (57 samples); not named in the paper but holds exactly the two cited series", "GSE60655": "DNA methylation 450K (S5.6.p1); not part of this gene-expression request"}, "assay": "bulk RNA-seq, Illumina HiSeq2000, 2x100 bp, vastus lateralis (S5.4.p1, S3.1.p1)", "primary_estimand": "Within-subject change in trained-leg skeletal-muscle gene expression after 3 months of supervised one-legged endurance knee-extension training: T2 (24 h after last session) vs T1 (pre-training), trained leg (S3.1.p1, S3.1.p2, S5.1.p1, S5.4.p2)", "planned_contrasts": ["T2 vs T1, trained leg, individual and library preparation as covariates (S5.4.p2; paper: 4076 DEGs, S3.1.p2)"], "factors": {"group": ["T1 pre-training trained leg", "T2 post-training trained leg"], "individual": "23 subjects (12 M, 11 F; TAB1)", "library_preparation": "covariate named in S5.4.p2; not annotated in GEO"}, "sample_inclusion": "23 sedentary young subjects; biopsies from both legs before and after training (S3.1.p1). RNA-seq DE is trained leg T2 vs T1 (S3.1.p2, S5.4.p2). The untrained leg is an intrain ... [1060 more characters]

reasoning: S5.4.p2 gives the RNA-seq DE: edgeR, group T2 vs T1 with library preparation and individual as covariates, FDR<0.05; S3.1.p2 reports 4076 DEGs. Design (one-legged training, biopsies pre/post) from S3.1.p1 and S5.1.p1. S5.6.p1 names GSE58608 and GSE60590 for expression.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE58608\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["S5.6.p1 cites GSE58608", "24 samples = 12 subjects x {T1, U1}, all exercise status 'untrained' (pre-training)", "series_id GSE58608,GSE60591"], "accession": "GSE58608", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE58608\\GSE58608_metadata.csv"}

reasoning: S5.6.p1 names GSE58608 and GSE60590 as the gene-expression series. GSE58608 metadata: Homo sapiens skeletal muscle, KTH/SciLifeLab, HiSeq2000 RNA-seq, original sample IDs <subject><T|U><1|2> matching the paper's T1/T2 and trained/untrained leg scheme.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 24, "n_metadata": 24, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE58608\\aligned\\aligned_metadata.csv", "columns": {"subject": {"source": "supplementary_file_1", "regex": "_(\\d+)[TU][12]\\.fpkm", "recode": {"4": "s04", "7": "s07", "9": "s09", "11": "s11", "12": "s12", "13": "s13", "15": "s15", "16": "s16", "18": "s18", "19": "s19", "20": "s20", "21": "s21"}}, "grp": {"source": "supplementary_file_1", "regex": "_\\d+([TU][12])\\.fpkm"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE58608\\aligned\\design_metadata.csv", "sha256": "e0e825a1fb72670f17555fc77450d12249323a227d2c7a42755a949c8c31b10b", "levels": {"subject": {"s11": 2, "s12": 2, "s13": 2, "s15": 2, "s16": 2, "s18": 2, "s19": 2, "s20": 2, "s21": 2, "s04": 2, "s07": 2, "s09": 2}, "grp": {"T1": 12, "U1": 12}}}}

reasoning: Matrix columns are GSM ids (raw_tar). subject and grp (T1/U1) parsed from the per-sample file name in supplementary_file_1 (<subject><T|U><1|2>.fpkm), which equals 'original sample id'. Subject 7: biopsy location (7T1 right leg) disagrees with publication id 8L and with GSE60590 7T2 left leg; the T/U code is used as the arm label.

### matrix (valid, not_started)

final: {"source": "GEO per-sample Cufflinks genes.fpkm_tracking files in the _RAW.tar, merged on gene_id (FPKM column)", "paper_input": "gene read counts for edgeR (S5.4.p2); not deposited", "matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE58608\\aligned\\aligned_matrix.csv", "sha256": "52e50109082f8c16077499c5813f3d63b8fe1c5fd1d3f9a29bf5f08022cdcf9a", "n_features": 61779, "n_samples": 24, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 79750.4, "median": 0.0, "integer_fraction": 0.5798, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Per-sample files are Cufflinks genes.fpkm_tracking (FPKM, FPKM_conf_lo/hi, FPKM_status); data_processing: TopHat 2.0.4 + Cufflinks 2.0.2. Values are non-integer (integer fraction about 0.58, almost all zeros), max about 85,700: linear FPKM. No read counts deposited, so edgeR on counts cannot be reproduced; FPKM must not be rounded into counts. Route: log2(FPKM+1), then limma.

### design (refused, not_started)

final: {"analysis_type": "none", "suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE58608\\suitability\\suitability.md", "n_comparisons": 0, "n_analyzable": 0}}

reasoning: Metadata exercise status 'untrained' for all 24 samples; ids are T1/U1 only (S3.1.p1: T2 is the post-training biopsy).

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/0 comparisons have >= 3 per group |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "series content",
    "paper": "T2 vs T1 DE (S5.4.p2)",
    "data": "baseline-only T1/U1 biopsies",
    "disposition": "refused standalone; samples analyzed in GSE60591"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 25484259 (Lindholm et al. 2014, Epigenetics; PMC4622000)

Run directory: `test/experiments/large_run_pilot_20261019/runs_claude/PMID25484259` (run label PMID25484259)
Spec: `case_spec.json` (built from a scratch script, not a driver). Runner: `python -m tools.case_runner execute`.
Validator: 28 records, 0 errors. Evaluator `audit_run.py --no-write`: verdict pass, score 100, coverage 90.2, no blocking findings.

## Paper (what it intends)
- Design: 23 sedentary young adults (12 M, 11 F) did 3 months of supervised one-legged knee-extension endurance training. Vastus lateralis biopsies were taken from both legs before (T1/U1) and 24 h after the last session (T2) (S3.1.p1, S5.1.p1).
- RNA-seq DE (S5.4.p2): edgeR on gene counts, with group (T2 vs T1, trained leg), library preparation and individual as covariates. Threshold **FDR < 0.05, no fold-change cutoff**. Result: **4076 DEGs** (S3.1.p2, S4.p2).
- Data (S5.6.p1): GSE58608 and GSE60590 are the expression series; GSE60655 is methylation and was not requested. GSE60591 is the GEO SuperSeries of the two expression series.

## Data facts
- All three series deposit only Cufflinks `genes.fpkm_tracking` files per sample (TopHat 2.0.4 + Cufflinks 2.0.2). There are **no read counts**, and there is no library-preparation annotation.
- GSE58608 (24 samples): 12 subjects x {T1, U1}, all taken before training.
- GSE60590 (33 samples): 22 T2 samples, plus 11 T1 samples from the 11 other subjects.
- GSE60591 (57 samples) = GSE58608 + GSE60590. It has T1 for 23 subjects and T2 for 22; subject 13 has no T2.
- Subject, arm (T1/T2/U1) and series batch were parsed from the per-sample file name in `supplementary_file_1` (`<subject><T|U><1|2>.fpkm`). This file name equals `original sample id`.

## What ran

| Case | Gate outcome | Model | Samples | DEGs at the paper's rule (padj<0.05) | Up / down | Paper |
|---|---|---|---|---|---|---|
| GSE58608 | **refused at design**: baseline only (T1/U1), no post-training sample | - | - | - | - | - |
| GSE60591 (primary) | declared deviation | limma on log2(FPKM+1), `~ Treatment + C(subject) + C(batch)` | 23 T1 + 22 T2 | **1608** | 1069 / 539 | 4076 |
| GSE60591 (sensitivity, no batch term) | declared deviation | limma, `~ Treatment + C(subject)` | 23 T1 + 22 T2 | **2576** | 1583 / 993 | 4076 |
| GSE60590 (sensitivity, pairs within the series) | declared deviation | limma, `~ Treatment + C(subject)`, complete pairs | 11 pairs | **1428** | 899 / 529 | 4076 |

- Gene filter:  ... [3623 more characters]
