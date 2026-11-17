# Review packet B (the analysis' decisions): GSE281241

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of key", "across": "characteristics_ch1.3.genotype", "pairs_or_sets": 6, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: all 12 samples are unstimulated C2C12 myotubes after 6 days of differentiation; the only factor is genotype (ChR2::tdTomato optogenetic line vs wild-type), a cell-line characterization (Series_summary). There is no light-stimulation or contraction arm, and the paper reports no analysis of this series.

## Samples per design level

### `grp`
- **ChR2** (6): GSM8615539 / O1; GSM8615540 / O2; GSM8615541 / O3; GSM8615542 / O4; GSM8615543 / O5; GSM8615544 / O6
- **WT** (6): GSM8615545 / WT1; GSM8615546 / WT2; GSM8615547 / WT3; GSM8615548 / WT4; GSM8615549 / WT5; GSM8615550 / WT6

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE257540", "GSE281241"], "primary_estimand": "Transcriptomic effect on HB9::GFP mESC-derived motor neuron spheroids of (a) biochemical stimulation with conditioned medium from optogenetically exercised C2C12 muscle (1 Hz light, 30 min/day) or from spontaneously twitching (unstimulated) muscle, versus unconditioned control medium, and (b) mechanical stimulation by magnetic matrix actuation (MagMA) versus non-actuated MagMA controls (S2.4.p1-p4, FIG7, S4.6, S4.7).", "planned_contrasts": ["Exercise CM vs Control (FIG7c; S2.4.p3)", "Spontaneous-twitch CM vs Control (FIG7d)", "Exercise CM vs Spontaneous-twitch CM (FIG7e)", "Mechanical stimulation vs mechanical control (FIG7i; S2.4.p4: only 2 significant hits, both up)"], "paper_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": "not_reported", "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "FIG7 legend; S4.10.p1"}, "factors": {"biochemical": ["Control", "Spontaneous twitch CM (GEO: Low intensity biochem, NE1-6)", "Exercise CM (GEO: High intensity biochem, S1-6)"], "mechanical": ["Mechanical control (MC1-4)", "Mechanical stimulation (M1-4)"]}, "sample_inclusion": "QC exclusion of samples with <500K reads, rRNA >20% or exon/intron ratio <10 (n = 5, S4.10.p1); final n: control 5, spontaneous 4, exercise 4 (FIG7a); mechanical control 3, mechanical 4 (FIG7i)", "repeated_measure_unit": "not_reported (independent spheroid wells; no pairing described)", "normalization": "DESeq2 size ... [772 more characters]

reasoning: Built from S2.4.p1-p5, FIG7 legend, S4.6-S4.11 and DA.p1. Paper's DE threshold is BH-adjusted p with no stated numeric cutoff or fold-change rule (FIG7 legend: p-values used to determine DEGs were Benjamini-Hochberg adjusted).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE281241\\GSE281241_salmon.merged.gene_counts.tsv.gz", "owned": true, "checks": ["GEO Series_pubmed_id 39523700; SuperSeries GSE281242 shared with GSE257540", "same submitter/core", "paper text does not cite or analyze GSE281241"], "accession": "GSE281241", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE281241\\GSE281241_metadata.csv"}

reasoning: Linked to the paper by GEO, but the article reports no analysis of it (only GSE257540 is cited, S4.8.p2, DA.p1).

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE281241\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "characteristics_ch1.3.genotype", "regex": "^(.+)$", "recode": {"ChR2::tdTomato": "ChR2", "Wild-Type": "WT"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE281241\\aligned\\design_metadata.csv", "sha256": "60dbf0adff36413ae77c63623871a8141decb640ed3c98ebd1fc127ca061886e", "levels": {"grp": {"ChR2": 6, "WT": 6}}}}

reasoning: Matrix W1-6 = titles WT1-6, O1-6 = O1-6; exact match after stripping T and normalizing.

### matrix (valid, not_started)

final: {"source": "GSE281241_salmon.merged.gene_counts.tsv.gz", "paper_input": "not_reported (dataset not analyzed in the paper)", "matrix_type": "estimated counts (nf-core Salmon gene_counts, non-integer)", "recommended_method": "DESeq2 after documented rounding", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE281241\\aligned\\aligned_matrix.csv", "sha256": "45c61f9d03c1f537a9c1ef92de737a5525110b056ce4f1fb9a59fcdcb67d378f", "n_features": 56941, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 278368.0, "median": 0.0, "integer_fraction": 0.9181, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: 92% integers with a non-integer remainder: Salmon estimated counts (GEO data_processing).

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "grp", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE281241\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Series_overall_design: transcriptomic comparison of wild-type C2C12 and ChR2-optogenetic C2C12 under the same culture conditions. Genotype is not exercise; manufacturing a contrast would not answer how exercise affects expression.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "dataset use",
    "paper": "not cited",
    "data": "GEO links it to PMID 39523700",
    "disposition": "refused_at_design"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 39523700 (PMC11874633)

Paper: *Actuating Extracellular Matrices Decouple the Mechanical and Biochemical Effects of Muscle Contraction on Motor Neurons.*
Decision maker: Claude Opus 5.5 (Claude Code session), bioinformatics-workflow skill, case-spec route. I skipped the preflight because the request said to.
Spec: `case_spec.json`. Runner output: `summary.csv`, `run_status.json`, per-case folders. Validator: 30 records, 0 errors.

## What ran

| Case | Outcome | Route |
|---|---|---|
| GSE257540_biochem | completed | paper_aligned. One DESeq2 model `~ grp` on Control (C, n=5), spontaneous-twitch CM (SP, n=5) and exercised-muscle CM (EX, n=4). Three planned contrasts (FIG7c-e). |
| GSE257540_mech | completed | paper_aligned. DESeq2 `~ grp` on MagMA-actuated (MS, n=4) vs non-actuated control (MC, n=3) (FIG7i). |
| GSE281241 | refused at `design` | Unstimulated ChR2::tdTomato C2C12 vs WT C2C12 myotubes. This is a genotype or cell-line characterization with no exercise or contraction arm. The paper does not cite this series: it cites only GSE257540 (S4.8.p2, DA.p1). The link comes only from GEO (Series_pubmed_id, SuperSeries GSE281242). |

How the decisions were made:
- **Group identity.** GEO's "Low intensity biochem" is the NE samples: medium from unstimulated, spontaneously twitching muscle. "High intensity biochem" is the S samples: medium from optically stimulated (exercised) muscle. Both come from the GSE257540 Series_overall_design.
- **Alignment.** Matrix columns L1 and H1 correspond to titles LI1 and HI1. I matched them by deriving a key with `key_patterns` and setting `normalize_keys`. The match is exact; nothing was aligned by position.
- **Matrix.** The counts are nf-core STAR/Salmon gene counts that the submitter deposited already rounded to integers. They went into DESeq2 unchanged, which is the paper's input. The TPM file was not used.
- **QC exclusions (S4.10.p1 criteria, computed from the deposited counts):**
  - C4: rRNA fraction 0.78.
  - LI6: 1,536 reads.
  - HI4: 243K reads.
  - HI5: 495K reads, just under the 500K cutoff.
  - MC3: 613K reads with the most detected genes of any sample, which fits the low exon/intron criterion.

  That makes 5 exclusions, matching the paper's "n = 5".
- **Threshold.** The paper says only that DEGs used BH-adjusted p-values and gives no cutoff and no fold-change rule. I applied `workflow_default` (padj < 0.05, no LFC rule) and labelled it as such. As an audit I also counted genes at nominal  ... [3990 more characters]
