# Review packet B (the analysis' decisions): GSE242861

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.3.age of donor", "n_values": 5, "max_repeat": 6, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "donor", "n_values": 6, "max_repeat": 3, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "donor", "across": "characteristics_ch1.5.treatment", "pairs_or_sets": 6, "samples_linked": 18, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): GSE242861 contains only in-vitro primary myotubes transfected with miR-30a/miR-30c mimics or scramble (6 donors x 3 treatments). There is no exercise, sedentary/trained, or pre/post-exercise factor, so the requested exercise estimand cannot be identified. The paper's exercise analysis uses in-vivo TaqMan miRNA arrays (S5.8.p1, S5.9.3.p1) that are not deposited in this series.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE242861"], "study_parts": {"in_vivo_exercise_miRNA": "Gene SMART cohort, vastus lateralis biopsies at baseline and 3 h after one HIIE bout (S5.5.p1, S5.7.p1), 44 participants (24 M / 20 F), TaqMan human miRNA A+B arrays (S5.8.p1), 308 detected miRNAs; limma means model ~0 + Sex.Timepoint + BMI + Wpeak, duplicateCorrelation on participant ID (S5.9.3.p1). No GEO accession is named for these arrays (DA.p1 cites GSE242861 and Zenodo 10.5281/zenodo.8412095 only).", "in_vitro_miR30_overexpression": "Primary myotubes from 3 male + 3 female donors, transfected 24 h with miR-30a mimic, miR-30c mimic or scramble (S5.9.1.p1); total RNA-seq, kallisto transcript counts, DESeq2 ~ Sex * Condition, prefilter <10 RPM in <2 samples (S5.9.2.p1). This is the part deposited as GSE242861."}, "primary_estimand": "Paper-wide: sex differences in skeletal-muscle miRNA expression at baseline and in the miRNA response to acute HIIE (pre vs 3 h post, by sex, sex x time interaction). Exercise is an in-vivo factor of the miRNA array data only.", "planned_contrasts": ["miRNA arrays: male vs female at baseline (S2.1.p1; 148 miRNAs)", "miRNA arrays: post vs pre exercise in females (S2.2.p1; 4 up, 0 down)", "miRNA arrays: post vs pre exercise in males (S2.2.p1; 148 up, 2 down)", "miRNA arrays: sex x exercise interaction (S2.2.p1; 111 miRNAs)", "RNA-seq (GSE242861): male vs female donor cells, scramble (S2.7.p1; 26 genes)", "RNA-seq (GSE242861): miR-30a vs scramble in males (18 up/23 down) an ... [747 more characters]

reasoning: The exercise estimand of the paper lives entirely in the TaqMan miRNA array data from in-vivo biopsies (S5.8.p1, S5.9.3.p1). The only GEO series cited (DA.p1) is GSE242861, whose 18 samples are primary myotube cultures transfected with miR-30a/miR-30c mimics or scramble (S5.9.1.p1, S5.9.2.p1); there is no exercise, time or biopsy factor in it. FDR < 0.05 with no fold-change rule (S5.9.3.p3, FIG4, FIG5).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38012706\\GSE242861_transcript_counts_wide.csv", "owned": true, "checks": ["DA.p1 names GSE242861", "GEO series: 18 samples, Homo sapiens skeletal muscle primary cells, treatment 24h 20nM scramble / miR-30a / miR-30c, 9 MALE / 9 FEMALE, matching S5.9.1.p1 (3 male + 3 female donors x 3 treatments)", "data_processing (kallisto v0.46.1, GRCh38) matches S5.9.2.p1", "the in-vivo miRNA array data (pre/post HIIE) are not part of this series"], "accession": "GSE242861", "metadata_file": "data\\GSE242861\\GSE242861_metadata.csv"}

reasoning: GSE242861 belongs to this paper but only to its in-vitro miR-30 overexpression experiment. The single deposited file, GSE242861_3col.tsv.gz (long format sample/transcript/count), was pivoted to wide form with prep_pivot_3col.py; values unchanged. The wide GeneCounts_RAW DATA.csv mentioned in data_processing is not in the downloaded supplementary files.

### alignment (valid, not_started)

final: {"method": "exact:sample_key", "n_aligned": 18, "n_metadata": 18, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38012706\\GSE242861\\aligned\\aligned_metadata.csv", "columns": {"sex": {"alias_of": "characteristics_ch1.2.Sex", "recode": {"MALE": "M", "FEMALE": "F"}}, "donor": {"source": "title", "regex": "^Muscle, (SG191|SG193|FI6|FI7|SAAL|TRCO)"}, "tx": {"source": "title", "regex": "(SCRAM|30a|30c)$", "recode": {"SCRAM": "scr", "30a": "m30a", "30c": "m30c"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38012706\\GSE242861\\aligned\\design_metadata.csv", "sha256": "014a4ec7f7ded68aab88b95802bd77c6dc3f1945d5e6ba0feff8deea79639d07", "levels": {"sex": {"M": 9, "F": 9}, "donor": {"SG191": 3, "SG193": 3, "FI6": 3, "FI7": 3, "SAAL": 3, "TRCO": 3}, "tx": {"scr": 6, "m30a": 6, "m30c": 6}}}}

reasoning: Matrix columns (e.g. FI630a, SG191SCRAM) equal the metadata title after the 'Muscle, ' prefix; exact match on the derived key. Donor and treatment parsed from the same title; sex from characteristics.

### matrix (valid, not_started)

final: {"source": "GSE242861_3col.tsv.gz pivoted to transcript x sample (207,877 Ensembl transcripts x 18)", "paper_input": "kallisto transcript counts analysed with DESeq2 (S5.9.2.p1)", "matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38012706\\GSE242861\\aligned\\aligned_matrix.csv", "sha256": "3aa390293eeaab3e8e83182b3f0947296048a48af67184cf30ba3d6d02359d2e", "n_features": 207877, "n_samples": 18, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1780280.0, "median": 0.0, "integer_fraction": 0.6358, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: data_processing: kallisto v0.46.1 'aligned raw gene counts'; values are non-negative with ~36% non-integer entries, ENST transcript IDs: kallisto estimated counts at transcript level. Compatible with the paper's DESeq2 route after rounding / gene summarisation, but no exercise factor exists to analyse.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": null, "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38012706\\GSE242861\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: Exercise is not a factor of any sample in GSE242861. Per the paper the miR-30 family was chosen because it showed a sex-specific exercise response in the arrays (S2.6.p1), but the RNA-seq tests overexpression, not exercise.

rejected alternatives: [{"value": "tx: miR-30a or miR-30c vs scramble (by sex, donor blocked)", "reason_rejected": "Valid paper contrast (S2.7.p2, S2.8.p1) but it is a miRNA overexpression effect in cultured cells, not an effect of exercise; analysing it would manufacture an exercise answer."}, {"value": "sex: male vs female donor cells", "reason_rejected": "Baseline sex difference in cultured cells; not an exercise contrast."}, {"value": "exercise pre vs post 3 h HIIE", "reason_rejected": "Not present in GSE242861; t ... [59 more characters]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "Data for the exercise estimand",
    "paper": "Exercise response measured with TaqMan miRNA arrays on pre/post-HIIE biopsies (S5.8.p1, S5.9.3.p1)",
    "data": "GSE242861 holds only the miR-30 overexpression RNA-seq of primary myotubes",
    "disposition": "blocks_estimand"
  },
  {
    "item": "Deposited files",
    "paper": "DA.p1",
    "data": "data_processing lists 3col.tsv and GeneCounts_ RAW DATA.csv; only GSE242861_3col.tsv.gz was downloaded, so it was pivoted",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID38012706 / GSE242861

**Status: refused at `design`.** GSE242861 has no exercise comparison.

## What ran
- `case_runner inspect GSE242861` downloaded the series. It contains 18 samples and one supplementary file, `GSE242861_3col.tsv.gz`, in long format (sample, transcript, kallisto estimated count) with no header.
- `prep_pivot_3col.py` reshaped that file into a wide table of 207,877 ENST transcripts x 18 samples, `GSE242861_transcript_counts_wide.csv`. The values were not changed and there were no duplicate rows or missing values.
- `case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership, alignment (exact match on the title key, 18/18 samples), matrix (kallisto estimated counts at transcript level), and design. Design was **refused**. The contract validator reported 0 errors.

## Why refused
- The paper studies exercise in vivo. It measured miRNAs with TaqMan arrays on vastus lateralis biopsies taken before and 3 h after one HIIE bout (S5.8.p1, S5.9.3.p1). The paper does not name a GEO accession for those arrays. DA.p1 cites only GSE242861 and Zenodo.
- GSE242861 holds only the in-vitro experiment: primary myotubes from 3 male and 3 female donors, each transfected with a miR-30a mimic, a miR-30c mimic, or scramble, then total RNA-seq (S5.9.1.p1, S5.9.2.p1).
- There is no exercise, time, or trained/untrained factor. The miR-30 vs scramble contrasts are valid paper contrasts, and the suitability report rates them analyzable. They measure miRNA overexpression, though, not exercise, so they were rejected as candidates instead of being turned into an exercise answer.

## DEG counts vs paper
No differential analysis was run.
- The paper's exercise results come from the miRNA arrays, with FDR < 0.05 and no fold-change rule (S5.9.3.p3): 148 miRNAs differ by sex at baseline; after exercise females have 4 up / 0 down and males 148 up / 2 down; 111 miRNAs show a sex x exercise interaction.
- None of these can be reproduced from GSE242861.
- For reference, the paper's results for the RNA-seq that GSE242861 does contain:
  - male vs female donor cells: 26 genes
  - miR-30a vs scramble: male 18 up / 23 down, female 16 up / 23 down
  - miR-30c vs scramble: male 13 up / 12 down, female 10 up / 11 down

## Deviations
- The deposited long-format file had to be pivoted with a prep script, which is listed in `prep_scripts`. data_processing also mentions a wide-format file, "GeneCounts_ RAW DATA.csv", but it was not among th ... [472 more characters]
