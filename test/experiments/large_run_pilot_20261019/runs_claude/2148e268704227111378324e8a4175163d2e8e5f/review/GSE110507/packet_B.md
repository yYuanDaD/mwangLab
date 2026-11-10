# Review packet B (the analysis' decisions): GSE110507

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.0.animal identifier", "n_values": 14, "max_repeat": 2, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "subject", "n_values": 14, "max_repeat": 2, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "characteristics_ch1.0.animal identifier", "across": "characteristics_ch1.1.vdr status", "pairs_or_sets": 14, "samples_linked": 28, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"treatment_protocol_ch1": ["In vivo electroporation was used to knock out (ko) or knock in (ki) the vitmain D receptor in the tibialis anterior muscle of one hindlimb in rats. VDR-KD groups received VDR shRNA (Table S1) in right leg TAM and scramble shRNA in left leg TAM. VDR-OE groups received pCAGGS-mVDR in right leg TAM, and empty pCAGGS controls in left leg TAM. Immediately following, one HV (900 V/cm, 100 碌-sec pulse), and four LV (90 V/cm, 100 m-sec) pulses  ... [433 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: GSE110507 contains only VDR overexpression / knock-down vs contralateral control limbs in sedentary rats. The paper's exercise component (human 20-wk RET, pre vs post) is in GSE47881, not this series, so the requested exercise estimand cannot be identified from these data.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE110507 (not named in the paper; rat VDR-OE RNA-seq, S2.7.p1)", "GSE47881 (human 20-wk RET microarray, S2.8.p1; separate series, not this case)"], "assay": "rat tibialis anterior RNA-seq (Illumina HiSeq 4000, 75 bp PE), Rsubread featureCounts", "primary_estimand": "Effect of in vivo electrotransfer VDR overexpression (pCAGGS-mVDR, right TA) vs contralateral empty-vector control (left TA) on rat TA gene expression, paired within animal, n = 7 (S2.7.p1, FIG1, FIG5). No exercise intervention in the rat experiment.", "planned_contrasts": ["VDR-OE vs contralateral empty-vector control, paired by animal (S3.2.p1; paper: 3,330 genes at P < 0.05)"], "exercise_component": "Human 20-week resistance exercise training (pre vs post) is analysed only as VDR mRNA correlations with lean-mass/1-RM change, using GSE47881 (S2.8.p1, S3.4.p1, FIG7); not in GSE110507.", "factors": {"vdr_arm": ["VDR-OE (IVE, right)", "empty pCAGGS control (sham, left)"]}, "repeated_measure_unit": "animal (contralateral limbs)", "paper_method": "edgeR: CPM filter at a count of 10, TMM, glmFit with design accounting for animal pairing (S2.7.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.2.p1"}, "paper_results": "3,330 genes P < 0.05; 310 gene-sets FDR < 5%, ECM up, tRNA aminoacylation/mTOR down (S3.2.p1)"}

reasoning: The paper's RNA-seq (S2.7.p1, S3.2.p1) compares VDR-OE TA with the contralateral empty-vector TA in 7 rats; it is a genetic gain-of-function experiment with no exercise. The only exercise data are the human RET microarrays from GSE47881 (S2.8.p1), used for VDR correlation (S3.4.p1). The paper does not cite GSE110507.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\2148e268704227111378324e8a4175163d2e8e5f\\GSE110507\\input\\merged_from_tar_gsm.csv", "owned": true, "owned_subset": "14 VDR knock-in samples (animals 416-422); the 14 VDR knock-out (shRNA) samples (animals 423-429) are not part of this paper", "checks": ["rat TA, IVE, pCAGGS-mVDR right vs empty pCAGGS left (treatment_protocol_ch1) matches S2.2/S3.1", "HiSeq 4000, TruSeq, 7 animals per arm match S2.7.p1 and FIG1 n = 7", "GEO contact Iain Gallagher = IJG, who did the bioinformatics (S5.p1)"], "accession": "GSE110507", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE110507\\GSE110507_metadata.csv"}

reasoning: The paper names no accession for the rat RNA-seq, but GSE110507's protocol, platform, tissue, group size and contact author all match; the series also deposits a VDR knock-down arm not reported here.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 28, "n_metadata": 28, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\2148e268704227111378324e8a4175163d2e8e5f\\GSE110507\\aligned\\aligned_metadata.csv", "columns": {"subject": {"alias_of": "characteristics_ch1.0.animal identifier"}, "vdr": {"alias_of": "characteristics_ch1.1.vdr status", "recode": {"Sham VDR knock-in": "OEctrl", "IVE VDR knock-in": "OE", "Sham VDR knock-out": "KDctrl", "IVE VDR knock-out": "KD"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\2148e268704227111378324e8a4175163d2e8e5f\\GSE110507\\aligned\\design_metadata.csv", "sha256": "2aa62b3b7a0cea0ce7fe146a0c245de7e2c2a3e976d4e80aa10c8d41f9893914", "levels": {"subject": {"416": 2, "417": 2, "418": 2, "419": 2, "420": 2, "421": 2, "422": 2, "423": 2, "424": 2, "425": 2, "426": 2, "427": 2, "428": 2, "429": 2}, "vdr": {"OEctrl": 7, "OE": 7, "KDctrl": 7, "KD": 7}}}}

reasoning: raw_tar merge names columns by GSM id; exact match to the metadata index (inspect: 28/28). Animal id gives the pairing key; vdr status gives arm and limb.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\2148e268704227111378324e8a4175163d2e8e5f\\GSE110507\\aligned\\aligned_matrix.csv", "sha256": "ddc6d4fec33ae435576dcc87be9efd213317a575c6de84e07125d0d58d03b79c", "n_features": 32883, "n_samples": 28, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3174316.0, "median": 2.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (fraction 1.0), max 3.17e6; GEO description: raw RNA-seq derived counts per gene (Ensembl 89); paper used Rsubread feature counts into edgeR (S2.7.p1).

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_contrast": null, "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\2148e268704227111378324e8a4175163d2e8e5f\\GSE110507\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: The request is how exercise affects gene expression; every sample in GSE110507 is from non-exercised rats differing only by electrotransferred construct. A VDR-OE contrast would answer a different question, so the case is refused at design rather than manufacturing an exercise contrast.

rejected alternatives: [{"value": "vdr OE vs OEctrl paired by subject (paper's RNA-seq contrast)", "reason_rejected": "genetic VDR gain-of-function, not exercise; outside the requested exercise estimand"}, {"value": "vdr KD vs KDctrl", "reason_rejected": "VDR knock-down arm not reported in this paper and not exercise"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 28 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "accession",
    "paper": "names only GSE47881 (human RET) for transcriptomics",
    "data": "GSE110507 is the rat VDR-OE/KD RNA-seq, unnamed in the paper",
    "disposition": "recorded; ownership matched on protocol and contact"
  },
  {
    "item": "exercise arm",
    "paper": "exercise only in human RET cohort (GSE47881)",
    "data": "no exercise samples in GSE110507",
    "disposition": "blocks the exercise estimand; refused at design"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE110507 / PMC7475200 (VDR overexpression induces skeletal muscle hypertrophy)

## What ran
- `tools.case_runner inspect GSE110507`: downloaded the series and merged `GSE110507_RAW.tar` into 32,883 Ensembl rat genes x 28 samples, all integer raw counts.
- `tools.case_runner execute case_spec.json`: recorded paper_reconstruction, ownership, alignment (exact on GSM index, 28/28), matrix (raw counts) and design. The case was **refused at design**. The validator found 5 records and 0 errors.
- No differential expression or enrichment was run.

## Why refused
- The request asks how exercise affects gene expression. GSE110507 contains only sedentary male Wistar rats in which the tibialis anterior was electroporated:
  - VDR-OE (pCAGGS-mVDR, right leg) vs empty pCAGGS (left leg), 7 animals;
  - VDR shRNA knock-down vs scramble, 7 animals. The paper does not report this arm.
- There is no exercise arm.
- The paper's exercise component is the human 20-week resistance exercise training cohort. It is a separate series, GSE47881 (S2.8.p1), and the paper uses it only to correlate VDR mRNA with gains in lean mass and 1-RM (S3.4.p1, FIG7).
- The rat RNA-seq contrast (VDR-OE vs contralateral control, paired) is a genetic gain-of-function estimand, so I did not run it as a stand-in for exercise.

## DEG counts vs paper
- Paper (S3.2.p1): 3,330 genes at P < 0.05 (raw p, no fold-change rule) for VDR-OE vs control. Method: edgeR with CPM filter at a count of 10, TMM, and glmFit paired by animal (S2.7.p1). Also 310 gene sets at FDR < 5%.
- Ours: none. The case stopped at design and no exercise contrast exists in the data.

## Deviations / notes
- Ownership: the paper names no accession for its rat RNA-seq. I matched GSE110507 on several points:
  - protocol: IVE with pCAGGS-mVDR vs empty vector in the TA;
  - HiSeq 4000 with TruSeq libraries;
  - n = 7;
  - the GEO contact is I. Gallagher, who is IJG, the bioinformatician in S5.p1.
- Of the 28 samples, only the 14 knock-in samples (animals 416-422) belong to this paper.

## Tool problems
- None in repository tools.
- My first spec had a JSON escape error: the shell heredoc collapsed `\d` to `\d`. I removed the unneeded `matrix_column_pattern`, because a raw_tar merge already names columns by GSM.

