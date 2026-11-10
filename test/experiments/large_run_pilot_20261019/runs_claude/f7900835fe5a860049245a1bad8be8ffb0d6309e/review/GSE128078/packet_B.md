# Review packet B (the analysis' decisions): GSE128078

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.4.individual identifier", "n_values": 25, "max_repeat": 4, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| day_CFS/day_d2_vs_d1_dzraw-CFS | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 340 | 5 | 3 | 35 | 0.13 | 0.016 |
| day_CFS/day_d3_vs_d1_dzraw-CFS | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 532 | 6 | 2 | 86 | 0.134 | 0.025 |
| day_CFS/day_d7_vs_d1_dzraw-CFS | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 373 | 12 | 4 | 47 | 0.133 | 0.017 |
| day_HC/day_d2_vs_d1_dzraw-HC | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 592 | 32 | 16 | 85 | 0.116 | 0.028 |
| day_HC/day_d3_vs_d1_dzraw-HC | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 495 | 26 | 12 | 82 | 0.141 | 0.023 |
| day_HC/day_d7_vs_d1_dzraw-HC | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 3103 | 531 | 33 | 636 | 0.072 | 0.146 |
| change_d2_CFS_vs_HC/CFS_vs_HC | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 310 | 9 | 5 | 24 | 0.159 | 0.014 |
| change_d3_CFS_vs_HC/CFS_vs_HC | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 303 | 17 | 2 | 34 | 0.122 | 0.014 |
| change_d7_CFS_vs_HC/CFS_vs_HC | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 1548 | 396 | 27 | 194 | 0.068 | 0.072 |
| dz_d1 | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 217 | 12 | 6 | 13 | 0.13 | 0.01 |
| dz_d2 | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 202 | 10 | 9 | 19 | 0.168 | 0.01 |
| dz_d3 | 0 | 0 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 0 | 411 | 38 | 6 | 40 | 0.11 | 0.019 |
| dz_d7 | 1 | 1 | padj < 0.1 and |log2FoldChange| > 0.584963 | 0 | 0 | 0 | 1 | 5030 | 1124 | 63 | 1418 | 0.044 | 0.238 |

## Samples per design level

### `day`
- **d1** (25): GSM3664555 / Sample_G1-1; GSM3664559 / Sample_G12-1; GSM3664562 / Sample_G13-1; GSM3664566 / Sample_G2-1; GSM3664570 / Sample_G4-1; GSM3664574 / Sample_G9-1; GSM3664578 / Sample_K1-1; GSM3664582 / Sample_K12-1; GSM3664586 / Sample_K2-1; GSM3664590 / Sample_K4-1; GSM3664594 / Sample_K7-1; GSM3664598 / Sample_P10-1; GSM3664602 / Sample_P11-1; GSM3664606 / Sample_P14-1; GSM3664610 / Sample_P3-1; GSM3664614 / Sample_P5-1; GSM3664618 / Sample_P6-1; GSM3664622 / Sample_P7-1; GSM3664626 / Sample_P8-1; GSM3664630 / Sample_T10-1; GSM3664634 / Sample_T11-1; GSM3664638 / Sample_T13-1; GSM3664642 / Sample_T14-1; GSM3664646 / Sample_T6-1; GSM3664650 / Sample_T9-1
- **d2** (25): GSM3664556 / Sample_G1-2; GSM3664560 / Sample_G12-2; GSM3664563 / Sample_G13-2; GSM3664567 / Sample_G2-2; GSM3664571 / Sample_G4-2; GSM3664575 / Sample_G9-2; GSM3664579 / Sample_K1-2; GSM3664583 / Sample_K12-2; GSM3664587 / Sample_K2-2; GSM3664591 / Sample_K4-2; GSM3664595 / Sample_K7-2; GSM3664599 / Sample_P10-2; GSM3664603 / Sample_P11-2; GSM3664607 / Sample_P14-2; GSM3664611 / Sample_P3-2; GSM3664615 / Sample_P5-2; GSM3664619 / Sample_P6-2; GSM3664623 / Sample_P7-2; GSM3664627 / Sample_P8-2; GSM3664631 / Sample_T10-2; GSM3664635 / Sample_T11-2; GSM3664639 / Sample_T13-2; GSM3664643 / Sample_T14-2; GSM3664647 / Sample_T6-2; GSM3664651 / Sample_T9-2
- **d3** (24): GSM3664557 / Sample_G1-3; GSM3664561 / Sample_G12-3; GSM3664564 / Sample_G13-3; GSM3664568 / Sample_G2-3; GSM3664572 / Sample_G4-3; GSM3664576 / Sample_G9-3; GSM3664580 / Sample_K1-3; GSM3664584 / Sample_K12-3; GSM3664588 / Sample_K2-3; GSM3664592 / Sample_K4-3; GSM3664596 / Sample_K7-3; GSM3664600 / Sample_P10-3; GSM3664604 / Sample_P11-3; GSM3664612 / Sample_P3-3; GSM3664616 / Sample_P5-3; GSM3664620 / Sample_P6-3; GSM3664624 / Sample_P7-3; GSM3664628 / Sample_P8-3; GSM3664632 / Sample_T10-3; GSM3664636 / Sample_T11-3; GSM3664640 / Sample_T13-3; GSM3664644 / Sample_T14-3; GSM3664648 / Sample_T6-3; GSM3664652 / Sample_T9-3
- **d7** (23): GSM3664558 / Sample_G1-7; GSM3664565 / Sample_G13-7; GSM3664569 / Sample_G2-7; GSM3664573 / Sample_G4-7; GSM3664577 / Sample_G9-7; GSM3664581 / Sample_K1-7; GSM3664585 / Sample_K12-7; GSM3664589 / Sample_K2-7; GSM3664593 / Sample_K4-7; GSM3664597 / Sample_K7-7; GSM3664601 / Sample_P10-7; GSM3664605 / Sample_P11-7; GSM3664613 / Sample_P3-7; GSM3664617 / Sample_P5-7; GSM3664621 / Sample_P6-7; GSM3664625 / Sample_P7-7; GSM3664629 / Sample_P8-7; GSM3664633 / Sample_T10-7; GSM3664637 / Sample_T11-7; GSM3664641 / Sample_T13-7; GSM3664645 / Sample_T14-7; GSM3664649 / Sample_T6-7; GSM3664653 / Sample_T9-7

### `subject`
- **G1** (4): GSM3664555 / Sample_G1-1; GSM3664556 / Sample_G1-2; GSM3664557 / Sample_G1-3; GSM3664558 / Sample_G1-7
- **G12** (3): GSM3664559 / Sample_G12-1; GSM3664560 / Sample_G12-2; GSM3664561 / Sample_G12-3
- **G13** (4): GSM3664562 / Sample_G13-1; GSM3664563 / Sample_G13-2; GSM3664564 / Sample_G13-3; GSM3664565 / Sample_G13-7
- **G2** (4): GSM3664566 / Sample_G2-1; GSM3664567 / Sample_G2-2; GSM3664568 / Sample_G2-3; GSM3664569 / Sample_G2-7
- **G4** (4): GSM3664570 / Sample_G4-1; GSM3664571 / Sample_G4-2; GSM3664572 / Sample_G4-3; GSM3664573 / Sample_G4-7
- **G9** (4): GSM3664574 / Sample_G9-1; GSM3664575 / Sample_G9-2; GSM3664576 / Sample_G9-3; GSM3664577 / Sample_G9-7
- **K1** (4): GSM3664578 / Sample_K1-1; GSM3664579 / Sample_K1-2; GSM3664580 / Sample_K1-3; GSM3664581 / Sample_K1-7
- **K12** (4): GSM3664582 / Sample_K12-1; GSM3664583 / Sample_K12-2; GSM3664584 / Sample_K12-3; GSM3664585 / Sample_K12-7
- **K2** (4): GSM3664586 / Sample_K2-1; GSM3664587 / Sample_K2-2; GSM3664588 / Sample_K2-3; GSM3664589 / Sample_K2-7
- **K4** (4): GSM3664590 / Sample_K4-1; GSM3664591 / Sample_K4-2; GSM3664592 / Sample_K4-3; GSM3664593 / Sample_K4-7
- **K7** (4): GSM3664594 / Sample_K7-1; GSM3664595 / Sample_K7-2; GSM3664596 / Sample_K7-3; GSM3664597 / Sample_K7-7
- **P10** (4): GSM3664598 / Sample_P10-1; GSM3664599 / Sample_P10-2; GSM3664600 / Sample_P10-3; GSM3664601 / Sample_P10-7
- **P11** (4): GSM3664602 / Sample_P11-1; GSM3664603 / Sample_P11-2; GSM3664604 / Sample_P11-3; GSM3664605 / Sample_P11-7
- **P14** (2): GSM3664606 / Sample_P14-1; GSM3664607 / Sample_P14-2
- **P3** (4): GSM3664610 / Sample_P3-1; GSM3664611 / Sample_P3-2; GSM3664612 / Sample_P3-3; GSM3664613 / Sample_P3-7
- **P5** (4): GSM3664614 / Sample_P5-1; GSM3664615 / Sample_P5-2; GSM3664616 / Sample_P5-3; GSM3664617 / Sample_P5-7
- **P6** (4): GSM3664618 / Sample_P6-1; GSM3664619 / Sample_P6-2; GSM3664620 / Sample_P6-3; GSM3664621 / Sample_P6-7
- **P7** (4): GSM3664622 / Sample_P7-1; GSM3664623 / Sample_P7-2; GSM3664624 / Sample_P7-3; GSM3664625 / Sample_P7-7
- **P8** (4): GSM3664626 / Sample_P8-1; GSM3664627 / Sample_P8-2; GSM3664628 / Sample_P8-3; GSM3664629 / Sample_P8-7
- **T10** (4): GSM3664630 / Sample_T10-1; GSM3664631 / Sample_T10-2; GSM3664632 / Sample_T10-3; GSM3664633 / Sample_T10-7
- **T11** (4): GSM3664634 / Sample_T11-1; GSM3664635 / Sample_T11-2; GSM3664636 / Sample_T11-3; GSM3664637 / Sample_T11-7
- **T13** (4): GSM3664638 / Sample_T13-1; GSM3664639 / Sample_T13-2; GSM3664640 / Sample_T13-3; GSM3664641 / Sample_T13-7
- **T14** (4): GSM3664642 / Sample_T14-1; GSM3664643 / Sample_T14-2; GSM3664644 / Sample_T14-3; GSM3664645 / Sample_T14-7
- **T6** (4): GSM3664646 / Sample_T6-1; GSM3664647 / Sample_T6-2; GSM3664648 / Sample_T6-3; GSM3664649 / Sample_T6-7
- **T9** (4): GSM3664650 / Sample_T9-1; GSM3664651 / Sample_T9-2; GSM3664652 / Sample_T9-3; GSM3664653 / Sample_T9-7

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE128078"], "assay": "bulk RNA-seq of whole blood (PAXgene, Nugen Ovation rRNA/globin depletion), HiSeq 2500 PE100 (S2.5.p1)", "subjects": "14 female ME/CFS cases and 11 age/sex-matched sedentary controls (S2.2.p1, ABS.p1)", "factors": {"disease": ["ME/CFS", "Control"], "day": ["1 (pre-CPET 1)", "2 (pre-CPET 2, about 24 h after CPET 1)", "3 (home visit, about 24 h after CPET 2)", "7 (home visit)"]}, "repeated_measure_unit": "subject: 4 blood samples per subject (S2.5.p1)", "sample_inclusion": "two samples of one subject (day 3 and day 7) with <40% transcriptome coverage removed (S3.3.p1, S1 Fig A)", "primary_estimand": "Within-subject change in whole-blood gene expression after cardiopulmonary exercise testing (day 2, 3, 7 versus pre-exercise day 1), separately in ME/CFS patients and in controls (Table 3 lower block); secondary: ME/CFS-vs-control difference per day and difference in pre-to-post change (S3.3.p2).", "planned_contrasts": ["Day 2 vs Day 1 within ME/CFS (Table 3: 0 DEGs)", "Day 3 vs Day 1 within ME/CFS (Table 3: 0 DEGs)", "Day 7 vs Day 1 within ME/CFS (Table 3: 0 DEGs)", "Day 2 vs Day 1 within controls (Table 3: 0 DEGs)", "Day 3 vs Day 1 within controls (Table 3: 0 DEGs)", "Day 7 vs Day 1 within controls (Table 3: 0 DEGs)", "pre-to-post change ME/CFS vs controls, per time point and days 1,2 vs 3,7 (S3.3.p2: 0 DEGs)", "ME/CFS vs controls at day 1/2/3/7 (Table 3: 0/0/0/1 DEGs) and all days combined (6 DEGs) - disease comparison, associational", "lo ... [700 more characters]

reasoning: The exercise question is answered in Table 3 lower block (Day 1 vs Day 2/3/7 within CFS and HC) and S3.3.p2 (pre vs post in CFS compared with controls). Day 1 and day 2 blood is drawn within 2 h before each CPET (S2.5.p1), so day 1 is the unexercised baseline and days 2, 3, 7 are about 24 h, 48 h and 6 days after the first test. The FDR text says '<0.1%' but every listed DEG in Table 4 has FDR 0.02-0.10, so the operative cutoff was FDR 0.1; treated as the paper threshold, with the literal 0.001 kept as audit.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\prep\\GSE128078_gene_FPKM.csv", "owned": true, "checks": ["GEO contact Chiu Lab UCSF matches the paper's sequencing site (S2.5.p1)", "99 whole-blood samples, 14 ME/CFS + 11 controls x 4 days (55 + 44; G12 day 7 absent) match ABS.p1 / S2.5.p1", "treatment field 'Cardiopulmonary exercise' and timepoints 1/2/3/7 match S2.5.p1"], "accession": "GSE128078", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE128078\\GSE128078_metadata.csv"}

reasoning: Series metadata (disease state, day, individual identifier, CPET) and sample structure match the paper's 25-subject x 4-day design. The deposited matrix is Cufflinks isoform FPKM (GEO data_processing: Tophat2/Bowtie2 on hg19), not the paper's Partek STAR/hg38 gene FPKM - recorded as a discrepancy, not an ownership failure.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 99, "n_metadata": 99, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM3664608": "P14 day 3: only 32% of transcripts detected (cohort median 69%); paper removed day 3 and day 7 of one subject for <40% coverage (S3.3.p1)", "GSM3664609": "P14 day 7: only 12.5% of transcripts detected; same paper exclusion (S3.3.p1)"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\aligned\\aligned_metadata_kept.csv", "columns": {"subject": {"alias_of": "characteristics_ch1.4.individual identifier"}, "dzraw": {"alias_of": "characteristics_ch1.1.disease state", "recode": {"ME/CFS": "CFS", "Control": "HC"}}, "day": {"alias_of": "characteristics_ch1.3.timepoint (day)", "recode": {"1": "d1", "2": "d2", "3": "d3", "7": "d7"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\aligned\\design_metadata.csv", "sha256": "1045b45c14537054014ddb4e338a211f83e5a89fff88a28613c709396e7cd273", "levels": {"subject": {"G1": 4, "G13": 4, "G2": 4, "G4": 4, "G9": 4, "K1": 4, "K12": 4, "K2": 4, "K4": 4, "K7": 4, "P10": 4, "P11": 4, "P3": 4, "P5": 4, "P6": 4, "P7": 4, "P8": 4, "T10": 4, "T11": 4, "T13": 4, "T14": 4, "T6": 4, "T9": 4, "G12": 3, "P14": 2}, "dzraw": {"CFS": 53, "HC": 44}, "day": {"d1": 25, "d2": 25, "d3": 24, "d7": 23}}}}

reasoning: Matrix columns equal the GEO title (99/99). Short columns: subject (individual identifier), dzraw (CFS/HC), day (d1..d7). Excluded the two low-coverage samples of subject P14 (day 3, day 7), which reproduces the paper's exclusion (S3.3.p1). G12 day 7 is not in GEO.

### matrix (valid, not_started)

final: {"paper_input": "gene FPKM from Partek/Cufflinks (S2.5.1.p1)", "source": "GSE128078_FES_isoforms_FPKM.txt.gz collapsed to gene symbols by prep/collapse_refseq_to_gene.py", "matrix_type": "FPKM (linear; gene-level sum of Cufflinks isoform FPKM)", "recommended_method": "limma on log2(FPKM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\aligned\\aligned_matrix.csv", "sha256": "c2cbfc1d72dcf6351bf300326b398faba24caa930a8d93e459ce247dbbfeab68", "n_features": 23293, "n_samples": 97, "annotation_columns_dropped": ["GSM3664608", "GSM3664609"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 496201.0, "median": 0.207493, "integer_fraction": 0.3233, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Deposited file is named isoforms_FPKM; GEO data_processing states FPKM from cufflinks 2; values are non-integer (39% integer only because of zeros), median about 0, max 4.96e5. Transcripts (NM_/NR_ RefSeq) were mapped to symbols with MyGene.info (40184/43497 mapped, 23293 genes) and summed per gene, as Cufflinks computes gene FPKM. No counts deposited, so count models are not possible.

### design (valid, not_started)

final: {"analysis_type": "repeated measures time series within disease group (paired by subject)", "formula": "~ 0 + day + subject (fitted separately within CFS and within HC)", "contrasts": [{"name": "day_d2_vs_d1_dzraw-CFS", "control": "d1", "treatment": "d2", "role": "primary"}, {"name": "day_d3_vs_d1_dzraw-CFS", "control": "d1", "treatment": "d3", "role": "primary"}, {"name": "day_d7_vs_d1_dzraw-CFS", "control": "d1", "treatment": "d7", "role": "primary"}, {"name": "day_d2_vs_d1_dzraw-HC", "control": "d1", "treatment": "d2", "role": "primary"}, {"name": "day_d3_vs_d1_dzraw-HC", "control": "d1", "treatment": "d3", "role": "primary"}, {"name": "day_d7_vs_d1_dzraw-HC", "control": "d1", "treatment": "d7", "role": "primary"}], "secondary": "change-from-day-1 difference CFS vs HC (paired change); CFS vs HC per day (associational); other day pairs exploratory", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\suitability\\suitability.md", "n_comparisons": 12, "n_analyzable": 12}}

reasoning: Table 3 lower block tests Day 1 vs Day 2/3/7 separately within CFS and HC, so disease is a stratum and day the factor with subject blocking (S2.5.p1: each subject gives 4 samples). Disease-group comparisons are cross-sectional (associational), run as secondary. The 'all days combined' CFS vs HC comparison needs a random subject effect that the runner cannot fit; not run. Low-VO2 / test-retest subsets cannot be built: per-subject classification is not deposited.

rejected alternatives: [{"value": "one joint model ~ 0 + dz:day + subject", "reason_rejected": "subject is nested in disease, so the disease main effect is aliased with subject; within-stratum fits equal the paper's per-group tests"}, {"value": "pooled pre (d1,d2) vs post (d3,d7)", "reason_rejected": "day 2 blood is after the first CPET; kept per-day contrasts as in Table 3"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "blocking (fixed effect within each disease stratum)"}, {"name": "library batch", "disposition": "not recorded in GEO; paper reports no batch structure by PCA (S3.3.p1)"}], "design_check": {"formula_equivalent": "~ C(day) + C(subject)", "n_samples": 97, "n_columns": 28, "columns": ["Intercept", "day_d2", "day_d3", "day_d7", "subject_G12", "subject_G13", "subject_G2", "subject_G4", "subject_G9", "subject_K1", "subject_K12", "subject_K2", "subject_K4", "subject_K7", "subject_P10", "subject_P11", "subject_P14", "subject_P3", "subject_P5", "subject_P6", "subject_P7", "subject_P8", "subject_T10", "subject_T11", "subject_T13", "subject_T14", "subject_T6", "subject_T9"], "rank": 28, "full_rank": true, "residual_df": 69, "levels": {"day": {"d1": 25, "d2": 25, "d3": 24, "d7": 23}, "subject": {"G1": 4, "G13": 4, "G2": 4, "G4": 4, "G9": 4, "K1": 4, "K12": 4, "K2": 4, "K4": 4, "K7": 4, "P10": 4, "P11": 4, "P3": 4, "P5": 4, "P6": 4, "P7": 4, "P8": 4, "T10": 4, "T11": 4, "T13": 4, "T14": 4, "T6": 4, "T9": 4, "G12": 3, "P14": 2}}, "cells": [{"cell": ["d1", "G1"], "n": 1}, {"cell": ["d1", "G12"], "n": 1}, {"cell": ["d1", "G13"], "n": 1}, {"cell": ["d1", "G2"], "n": 1}, {"cell": ["d1", "G4"], "n": 1}, {"cell": ["d1", "G9"], "n": 1}, {"cell": ["d1", "K1"], "n": 1}, {"cell": ["d1", "K12"], "n": 1}, {"cell": ["d1", "K2"], "n": 1}, {"cell": ["d1", "K4"], "n": 1}, {"cell": ["d1", "K7"], "n": 1}, ... [3893 more characters]

reasoning: Repeated samples from the same subject must be blocked (S2.5.p1). No batch, lane, or RIN column in GEO; paper saw no batch effect (S2.5.p1, S3.3.p1). All subjects are female (S2.2.p1), so no sex covariate.

### method (valid, not_started)

final: {"matrix_type": "FPKM (linear; gene-level sum of Cufflinks isoform FPKM)", "method": "limma (moderated t) on log2(FPKM+1)", "formula": "~ 0 + C(day) + C(subject)", "paper_route": {"method": "Partek Flow multimodel (AICc-selected normal/lognormal/NB/Poisson per gene)", "status": "blocked", "reason": "proprietary Partek GSA not available; deposited data are FPKM, not counts, so count models are not possible"}, "deviations": ["limma on log2(FPKM+1) instead of Partek multimodel", "gene FPKM summed from deposited hg19 Cufflinks isoform FPKM instead of the paper's hg38 STAR/Partek gene FPKM", "log2FC from limma on log scale instead of Partek linear fold change"], "transform": "log2(x+1)"}

reasoning: Policy: linear FPKM goes to log2(x+1) then limma. Subject blocking as fixed effect within strata.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.001, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "deviation_note": "Paper: |FC| > 1.5, p < 0.05, FDR < '0.1%'. Table 4 lists DEGs with FDR up to 0.10, so FDR < 0.1 is applied; the literal FDR < 0.001 is the audit rule. The extra p < 0.05 cannot be encoded alongside padj in one rule; with BH, padj < 0.1 and p >= 0.05 requires more than half of genes to be significant, so it is not binding here."}

reasoning: S2.5.1.p1 and TAB4. FC 1.5 converted exactly to log2(1.5) = 0.5849625.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "day_CFS", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 53, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_CFS\\input\\matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell) + C(cov0)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_CFS\\DEG_results_day_d2_vs_d1_dzraw-CFS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_CFS\\DEG_results_day_d3_vs_d1_dzraw-CFS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_CFS\\DEG_results_day_d7_vs_d1_dzraw-CFS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_CFS\\DEG_results_day_d3_vs_d2_dzraw-CFS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_CFS\\DEG_results_day_d7_vs_d2_dzraw-CFS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_CFS\\DEG_results_day_d7_vs_d3_dzraw-CFS.csv"], "counts": {"day_CFS/day_d2_vs_d1_dzraw-CFS": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| >  ... [1926 more characters]

reasoning: Table 3: day 2/3/7 vs day 1 within ME/CFS, subject-blocked; other day pairs exploratory; comparisons listed explicitly because 'all' also pulls the other stratum's comparisons into a subset fit

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "day_HC", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 44, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_HC\\input\\matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell) + C(cov0)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_HC\\DEG_results_day_d2_vs_d1_dzraw-HC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_HC\\DEG_results_day_d3_vs_d1_dzraw-HC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_HC\\DEG_results_day_d7_vs_d1_dzraw-HC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_HC\\DEG_results_day_d3_vs_d2_dzraw-HC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_HC\\DEG_results_day_d7_vs_d2_dzraw-HC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\day_HC\\DEG_results_day_d7_vs_d3_dzraw-HC.csv"], "counts": {"day_HC/day_d2_vs_d1_dzraw-HC": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "n_te ... [1900 more characters]

reasoning: Table 3: day 2/3/7 vs day 1 within controls, subject-blocked; comparisons listed explicitly because 'all' also pulls the other stratum's comparisons into a subset fit

### execution (valid, completed)

final: {"method": "run_multigroup_analysis", "subset": "change_d2_CFS_vs_HC", "role": "secondary", "tool": "tools.multigroup_tools:run_multigroup_analysis", "n_samples": 97, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\change_d2_CFS_vs_HC\\followup_d2\\DEG_results_CFS_vs_HC.csv"], "counts": {"change_d2_CFS_vs_HC/CFS_vs_HC": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "n_tested": 21507, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.001 and |log2FoldChange| > 0.584963", "n_tested": 21507, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: S3.3.p2: change from day 1 to d2 in ME/CFS compared with controls; one execution per follow-up because the runner keys multigroup tables by contrast name only

### execution (valid, completed)

final: {"method": "run_multigroup_analysis", "subset": "change_d3_CFS_vs_HC", "role": "secondary", "tool": "tools.multigroup_tools:run_multigroup_analysis", "n_samples": 97, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\change_d3_CFS_vs_HC\\followup_d3\\DEG_results_CFS_vs_HC.csv"], "counts": {"change_d3_CFS_vs_HC/CFS_vs_HC": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "n_tested": 21507, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.001 and |log2FoldChange| > 0.584963", "n_tested": 21507, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: S3.3.p2: change from day 1 to d3 in ME/CFS compared with controls; one execution per follow-up because the runner keys multigroup tables by contrast name only

### execution (valid, completed)

final: {"method": "run_multigroup_analysis", "subset": "change_d7_CFS_vs_HC", "role": "secondary", "tool": "tools.multigroup_tools:run_multigroup_analysis", "n_samples": 97, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\change_d7_CFS_vs_HC\\followup_d7\\DEG_results_CFS_vs_HC.csv"], "counts": {"change_d7_CFS_vs_HC/CFS_vs_HC": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "n_tested": 21507, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.001 and |log2FoldChange| > 0.584963", "n_tested": 21507, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: S3.3.p2: change from day 1 to d7 in ME/CFS compared with controls; one execution per follow-up because the runner keys multigroup tables by contrast name only

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "dz_d1", "role": "secondary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 25, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\dz_d1\\input\\matrix.csv", "transform": "log2(x+1)", "formula": "~ dzraw", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\dz_d1\\DEG_results_CFS_vs_HC.csv"], "counts": {"dz_d1": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "n_tested": 21014, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.001 and |log2FoldChange| > 0.584963", "n_tested": 21014, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Table 3 ME/CFS vs controls day 1 (associational)

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "dz_d2", "role": "secondary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 25, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\dz_d2\\input\\matrix.csv", "transform": "log2(x+1)", "formula": "~ dzraw", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\dz_d2\\DEG_results_CFS_vs_HC.csv"], "counts": {"dz_d2": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "n_tested": 21128, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.001 and |log2FoldChange| > 0.584963", "n_tested": 21128, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Table 3 ME/CFS vs controls day 2

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "dz_d3", "role": "secondary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 24, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\dz_d3\\input\\matrix.csv", "transform": "log2(x+1)", "formula": "~ dzraw", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\dz_d3\\DEG_results_CFS_vs_HC.csv"], "counts": {"dz_d3": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "n_tested": 21133, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.001 and |log2FoldChange| > 0.584963", "n_tested": 21133, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Table 3 ME/CFS vs controls day 3

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "dz_d7", "role": "secondary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 23, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\dz_d7\\input\\matrix.csv", "transform": "log2(x+1)", "formula": "~ dzraw", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f7900835fe5a860049245a1bad8be8ffb0d6309e\\GSE128078\\results\\dz_d7\\DEG_results_CFS_vs_HC.csv"], "counts": {"dz_d7": {"applied": {"rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "n_tested": 21106, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.001 and |log2FoldChange| > 0.584963", "n_tested": 21106, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Table 3 ME/CFS vs controls day 7 (paper 1 DEG, LINC01158)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Different upstream processing (hg19 Tophat2/Cufflinks isoforms deposited vs hg38 STAR/Partek gene-level in paper)", "Low-VO2 and test-retest subset comparisons not reproducible: subject classification not in GEO", "All-days CFS vs HC (paper 6 DEGs) not run: needs a random subject effect"], "results": {"day_CFS/day_d2_vs_d1_dzraw-CFS": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "audit_n": 0}, "day_CFS/day_d3_vs_d1_dzraw-CFS": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "audit_n": 0}, "day_CFS/day_d7_vs_d1_dzraw-CFS": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "audit_n": 0}, "day_CFS/day_d3_vs_d2_dzraw-CFS": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "audit_n": 0}, "day_CFS/day_d7_vs_d2_dzraw-CFS": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "audit_n": 0}, "day_CFS/day_d7_vs_d3_dzraw-CFS": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "audit_n": 0}, "day_HC/day_d2_vs_d1_dzraw-HC": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "audit_n": 0}, "day_HC/day_d3_vs_d1_dzraw-HC": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.1 and |log2FoldChange| > 0.584963", "audit_n": 0}, "day_HC/day_d7_vs_d1_dzraw-HC": {"n_deg": 0, "up": 0, "down": 0, "ru ... [2433 more characters]

reasoning: Method and preprocessing differ from the paper; the planned exercise contrasts and thresholds are kept.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 97 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "upstream processing",
    "paper": "STAR v2.4.1 + Cufflinks on hg38, Partek Flow, 25,278 RefSeq genes (S2.5.1.p1)",
    "data": "GEO data_processing: Tophat2/Bowtie2 on hg19, cufflinks 2 isoform FPKM, 43,497 RefSeq transcripts",
    "disposition": "executable_with_deviation"
  },
  {
    "item": "FDR cutoff",
    "paper": "text FDR < 0.1%",
    "data": "Table 4 DEGs have FDR 0.02-0.10",
    "disposition": "executable_without_change"
  },
  {
    "item": "sample count",
    "paper": "100 libraries, 2 removed (S2.5.p1, S3.3.p1)",
    "data": "99 samples in GEO (G12 day 7 absent); P14 day 3/7 low coverage removed here",
    "disposition": "executable_without_change"
  },
  {
    "item": "VO2 / test-retest subsets",
    "paper": "8 low-VO2 and test-retest subjects (S3.2.p3)",
    "data": "per-subject labels not deposited",
    "disposition": "not_executable"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE128078 / PMC6428308 (ME/CFS vs controls, CPET, whole blood RNA-seq)

## What ran

- Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Final status: completed, validator 18 records with 0 errors, 0 external LLM attempts. Route label: `declared_deviation`.
- Prep step (`prep/collapse_refseq_to_gene.py`): GEO only has Cufflinks **isoform** FPKM keyed by RefSeq NM_/NR_ accessions. I mapped them to gene symbols with MyGene.info (40,184 of 43,497 mapped) and summed them into 23,293 gene-level FPKM rows. The mapping is saved in `prep/refseq_to_symbol.csv`.
- Alignment: exact match on `title` (99/99). Derived columns: `subject`, `dzraw` (CFS/HC), `day` (d1/d2/d3/d7). I excluded P14 day 3 (GSM3664608, 32% of transcripts detected) and P14 day 7 (GSM3664609, 12.5%). This repeats the paper's removal of day 3 and day 7 from one subject with <40% coverage (S3.3.p1). 97 samples were analysed. G12 day 7 is not in GEO.
- Matrix and method: linear FPKM, transformed with log2(x+1), then limma. The paper's Partek multimodel route is blocked (proprietary software, and no counts were deposited).
- Design (the exercise question, Table 3 lower block): day was the factor and disease a stratum. One limma model `~ 0 + C(day) + C(subject)` was fitted within each group (14 CFS, 11 HC), with subject blocking. Primary contrasts: d2/d3/d7 vs d1. Other pairs of days were run as exploratory.
- Secondary analyses: change from day 1 (d2, d3, d7) compared between CFS and HC (paired_change). CFS vs HC on each day (two-arm limma, associational).
- Threshold: the paper's rule as I read it, padj < 0.1 and |log2FC| > log2(1.5) = 0.5849625 (`paper_on_deviation_route`). The text says "FDR < 0.1%", but every DEG in Table 4 has an FDR between 0.02 and 0.10. I used the literal FDR < 0.001 as the audit rule. The paper's extra p < 0.05 rule cannot be encoded next to padj, and it does not bind here.

## DEG counts vs the paper

| Comparison | Ours (padj<0.1, abs(log2FC)>0.585) | Paper (Table 3) |
|---|---|---|
| CFS d2 vs d1 / d3 vs d1 / d7 vs d1 | 0 / 0 / 0 | 0 / 0 / 0 |
| HC d2 vs d1 / d3 vs d1 / d7 vs d1 | 0 / 0 / 0 | 0 / 0 / 0 |
| Change from d1, CFS vs HC (d2/d3/d7) | 0 / 0 / 0 | 0 (S3.3.p2) |
| CFS vs HC d1 / d2 / d3 / d7 | 0 / 0 / 0 / 1 | 0 / 0 / 0 / 1 |

- Every exercise contrast matches the paper: no exercise-induced DEGs in either group. The smallest padj was 0.24 to 1.0.
- The single day-7 disease DEG is a different gene. Ours is HARS2 (log2FC 0.587, pad ... [1704 more characters]
