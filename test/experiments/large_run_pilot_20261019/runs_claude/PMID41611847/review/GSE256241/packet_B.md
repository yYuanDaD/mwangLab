# Review packet B (the analysis' decisions): GSE256241

## Mechanical flags

- none

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast exists. The only factor is diet treatment (rosiglitazone 6 vs control 6, characteristics_ch1.1.treatment; S4.6.p1). Every mouse was sedentary apart from treadmill/rotarod/grip phenotyping tests given to both groups (S4.7-S4.9), so exercise is neither a factor nor separable from anything. The requested estimand (effect of exercise on gene expression) is not identifiable; the paper's own rosiglitazone-vs-control contrast does not answer the request and is not run as a substitute.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE256241"], "assay": "bulk RNA-seq (polyA, Illumina NovaSeq 6000 PE150) of gastrocnemius from aged male C57BL/6JRj mice (S2.8.p1, S4.11.p1)", "sample_inclusion": "12 mice randomized at 17 months to rosiglitazone diet (0.6 mg/kg/d in AIN-93M, n=6) or plain AIN-93M control diet (n=6) (S4.6.p1; FIG5 C n=6 per group). WGCNA used 5 rosiglitazone + 6 control (FIG5 D, Fig. S3).", "factors": {"treatment": ["control", "rosiglitazone"]}, "primary_estimand": "Effect of dietary rosiglitazone vs control diet on gastrocnemius gene expression in aged mice. No exercise intervention exists: treadmill (S4.7.p1), rotarod (S4.8.p1) and grip tests (S4.9.p1) are phenotyping assays applied to both groups, not a training arm.", "planned_contrasts": ["rosiglitazone vs control (S2.8.p1; paper: 383 up + 100 down = 483 DEGs)"], "repeated_measure_unit": "none (one gastrocnemius per independent mouse)", "normalization": "DESeq2 size factors; pre-filter genes with >1 count per sample and total >12 (S4.13.p1)", "paper_method": "DESeq2 1.34.0 ~ treatment, BH adjustment (S4.13.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": true, "inclusive": false, "source_locator": "FIG5 C caption; S4.13.p1 item (3)"}, "paper_results": "383 up / 100 down DEGs; Igf1 up; Foxo4, Fbxo32, Trim63 down; fgsea PI3K-Akt up NES 1.68 (S2.8.p1)"}

reasoning: The paper is a drug-repositioning study. Its only transcriptomic experiment (S2.8.p1, S4.11-S4.13) compares rosiglitazone-fed with control-fed aged mice. Exercise appears only as an outcome measure (treadmill exhaustion test, S4.7.p1) and as background in the introduction (S1.p4).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE256241\\GSE256241_raw_count.txt.gz", "owned": true, "checks": ["S9.p1 names GSE256241 as the mouse skeletal muscle RNA-seq", "12 GSM samples, skeletal muscle, Mus musculus, treatment rosiglitazone 6 / control 6 matches S4.6.p1", "data_processing fastp/HISAT2/StringTie matches S4.12.p1"], "accession": "GSE256241", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE256241\\GSE256241_metadata.csv"}

reasoning: Data availability (S9.p1) names GSE256241; sample count, tissue, organism, groups and processing all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": ["length"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41611847\\GSE256241\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.1.treatment", "recode": {"control": "CTRL", "rosiglitazone": "ROSI"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41611847\\GSE256241\\aligned\\design_metadata.csv", "sha256": "7bac245551e7743e97f96bcd4da14f679423849e1fef454878dbc793eee673f7", "levels": {"grp": {"ROSI": 6, "CTRL": 6}}}}

reasoning: Matrix columns (C3..C15, A6..A25) equal the GEO title field exactly for 12/12 samples (inspect alignment_keys). Treatment comes from characteristics_ch1.1.treatment; the A/C prefixes agree with it.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts", "recommended_method": "DESeq2 after documented rounding", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41611847\\GSE256241\\aligned\\aligned_matrix.csv", "sha256": "e3bdcfc2361ad587655d3c6d31f01ad44449560d0c224df50def0023db6f5158", "n_features": 55716, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1748215.3, "median": 0.0, "integer_fraction": 0.894, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GSE256241_raw_count.txt.gz: values 0 to 1.75e6, 89.4% integer overall; about 21% of expressed entries are fractional (e.g. 13985.99, 43.85), the signature of StringTie/RSEM-style estimated counts rather than featureCounts integers. data_processing says HISAT2 + StringTie and the file is described as raw counts; the paper used it in DESeq2 (S4.13.p1). Annotation columns gene_name/description/length and empty Unnamed columns are not samples.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41611847\\GSE256241\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Request is exercise effect; paper and GEO metadata contain only a drug-vs-control arm. Rejected alternative: running rosiglitazone vs control as an 'exercise-capacity' proxy - rejected because improved treadmill performance is a drug outcome, not an exercise exposure.

rejected alternatives: [{"value": "grp_ROSI_vs_CTRL", "reason_rejected": "drug intervention, not exercise; does not answer the requested estimand"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "requested estimand",
    "paper": "rosiglitazone vs control diet in aged mice; exercise only as treadmill phenotyping",
    "data": "treatment: rosiglitazone 6 / control 6; no exercise field",
    "disposition": "blocks_estimand"
  },
  {
    "item": "WGCNA sample set",
    "paper": "5 rosiglitazone + 6 control for WGCNA (FIG5 D); 6+6 for DESeq2",
    "data": "12 samples deposited",
    "disposition": "not_relevant_after_stop"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID41611847 / GSE256241

**Status: refused at the `design` gate.** The data contain no exercise contrast.

## What ran
1. `python -m tools.case_runner inspect GSE256241` downloaded the series to `data/GSE256241`. It found one matrix, `GSE256241_raw_count.txt.gz` (55,716 Ensembl genes x 12 samples, plus annotation columns `gene_name`, `description` and `length` and empty `Unnamed:*` columns). Its columns match the GEO `title` field for 12 of 12 samples.
2. I read the paper (PMC13022187.paper.md), mainly S2.7, S2.8, FIG5, S4.6–S4.13 and S9.
3. I wrote `case_spec.json` and ran `python -m tools.case_runner execute`. It recorded these gates:
   - paper_reconstruction: valid
   - ownership: valid
   - alignment: valid (exact match on `title`, 12/12 samples)
   - matrix: valid (estimated counts)
   - design: **refused**

   The contract validator ran on 5 records and found 0 errors. The case route is `stopped`.

## Why it was refused
- The paper is a drug-repositioning study. Its only transcriptome experiment compares gastrocnemius from aged male mice fed rosiglitazone (n=6) with mice fed the control diet (n=6) (S4.6.p1, S2.8.p1).
- GEO has one grouping factor, `characteristics_ch1.1.treatment`, with rosiglitazone/control at 6/6.
- In this paper, exercise is only an outcome measure. The treadmill exhaustion, rotarod and grip-strength tests (S4.7–S4.9) were given to both groups.
- No group was trained or sedentary, so the effect of exercise on gene expression cannot be estimated.
- I did not run the rosiglitazone-vs-control contrast as a substitute. It is recorded as a rejected candidate.

## DEG counts vs paper
- **Paper:** rosiglitazone vs control gave 383 up and 100 down (483 DEGs).
  - Threshold: BH-adjusted P < 0.05 and |log2FC| >= 1 (FIG5 C caption; S4.13.p1 item 3).
  - Method: DESeq2 1.34.0, keeping genes with more than 1 count in every sample and a total above 12.
- **Ours:** none. No exercise contrast exists, so nothing was run (0 contrasts).

## Deviations
None. The case was stopped before any model was fitted.

Notes for anyone who later reproduces the drug contrast:
- The matrix holds StringTie estimated counts (about 21% of expressed entries are fractional), so DESeq2 would need documented rounding.
- WGCNA used 5 rosiglitazone + 6 control samples (FIG5 D). That is not relevant here.

## Tool problems
None blocking.
- Minor: the `inspect` matrix `candidates` for this file was "linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_coun ... [266 more characters]
