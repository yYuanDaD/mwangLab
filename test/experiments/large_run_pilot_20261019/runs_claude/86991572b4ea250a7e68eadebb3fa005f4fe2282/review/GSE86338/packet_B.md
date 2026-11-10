# Review packet B (the analysis' decisions): GSE86338

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.3.treatment", "n_values": 3, "max_repeat": 2, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "characteristics_ch1.3.treatment (without source_name_ch1) + suffix of title", "across": "source_name_ch1", "pairs_or_sets": 6, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: sample_size): Every iWAT arm has only 2 sequenced libraries (each a pool of 4 mice; S4.2.p1): SWIM n=2 vs CNT n=2. The suitability report is not_analyzable (sample_size: 0/6 comparisons have >= 3 per group), so no comparison, including the planned exercise contrast grp_SWIM_vs_CNT, meets the n >= 3 replicate rule and the contract rejects a valid design. Planned route if allowed: one limma model ~ grp on log2(FPKM+1) over the 8 iWAT samples, contrast SWIM vs CNT, paper threshold FDR<=0.05 & |log2FC|>=1 (paper: 673 up / 826 down).

## Samples per design level

### `grp`
- **CL** (2): GSM2300497 / iWAT_Cl316243_1 / S2BETA_1; GSM2300498 / iWAT_Cl316243_2 / S2BETA_2
- **CNT** (2): GSM2300495 / iWAT_Control_1 / S2CNT_1; GSM2300496 / iWAT_Control_2 / S2CNT_2
- **COLD** (2): GSM2300499 / iWAT_4oC7day_1 / S2COLD_1; GSM2300500 / iWAT_4oC7day_2 / S2COLD_2
- **SWIM** (2): GSM2300501 / iWAT_swimming_1 / S2SWIM_1; GSM2300502 / iWAT_swimming_2 / S2SWIM_2

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE86338"], "assay": "bulk polyA RNA-seq (Illumina HiSeq2000), mouse C57BL/6 male; each library = pooled RNA from 4 animals (S4.2.p1)", "primary_estimand": "Effect of a swimming exercise program (ramp 10->90 min twice daily, then 2 weeks) on the inguinal WAT (iWAT) transcriptome versus room-temperature control iWAT (S2.1.p1, S4.4.p1)", "sample_inclusion": "iWAT series S2: control (S2CNT_1/2) and swimming (S2SWIM_1/2); CL316243 and 7-day cold iWAT share the same control and are the paper's other browning arms. BAT series (S3, S5) are separate experiments (BAT whitening at 30C, BAT cold activation) with their own controls and are not part of the exercise estimand.", "factors": {"grp": ["CNT", "CL", "COLD", "SWIM"], "tissue": ["iWAT", "BAT (excluded)"]}, "planned_contrasts": ["iWAT swimming vs iWAT control (S2.2.p1; paper: 673 up + 826 down mRNAs)", "iWAT 4C 7d cold vs control (S2.2.p1; paper: 1062 up + 1201 down) - other browning arm, exploratory here", "iWAT CL316243 vs control (S2.2.p1; paper: 837 up + 681 down) - other browning arm, exploratory here"], "repeated_measure_unit": "none; each library is a pool of 4 independent mice (S4.2.p1); 2 pools per condition", "normalization": "Cufflinks FPKM, compatible-hits-norm for DE (S4.3.1.p1)", "paper_method": "Cuffdiff (Cufflinks 2.1.1) on TopHat alignments (S4.3.1.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": true, "source_locator": ... [319 more characters]

reasoning: S2.1.p1/S4.4.p1 describe the swimming protocol and the three iWAT browning arms sharing one control; S2.2.p1 gives the per-arm DEG counts with the threshold (|FC|>=2, FDR<=0.05); S4.3.1.p1 gives Cufflinks/Cuffdiff on FPKM; S4.2.p1 says each sequenced sample is a pool of 4 animals. GEO titles iWAT_Control_1/2 and iWAT_swimming_1/2 match.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE86338\\GSE86338_gene_fpkm.txt.gz", "owned": true, "checks": ["FN.p1 and S4.2.p1 name GSE86338 as the study's deposit", "18 GEO samples = 18 samples in the paper's PCA (S2.4.p1)", "GSE86338_gene_fpkm.txt.gz columns S2CNT_1..S5BAT_WT_COLD_3 equal the metadata description field 18/18", "data_processing: TopHat-2.0.9 + Cufflinks-2.1.1 FPKM, matching S4.3.1.p1"], "accession": "GSE86338", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE86338\\GSE86338_metadata.csv"}

reasoning: Series is cited by the paper, sample count and processing match, matrix columns match metadata description exactly.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 18, "n_metadata": 18, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM2300503": "BAT experiment (S3CNT_1), separate tissue/control; not part of the iWAT exercise estimand", "GSM2300504": "BAT experiment (S3CNT_2), separate tissue/control", "GSM2300505": "BAT 30C whitening (S330oC_1), separate tissue", "GSM2300506": "BAT 30C whitening (S330oC_2), separate tissue", "GSM2300507": "BAT control for cold (S5BAT_WT_1), separate experiment", "GSM2300508": "BAT control for cold (S5BAT_WT_2), separate experiment", "GSM2300509": "BAT control for cold (S5BAT_WT_3), separate experiment", "GSM2300510": "BAT cold (S5BAT_WT_COLD_1), separate experiment", "GSM2300511": "BAT cold (S5BAT_WT_COLD_2), separate experiment", "GSM2300512": "BAT cold (S5BAT_WT_COLD_3), separate experiment"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\86991572b4ea250a7e68eadebb3fa005f4fe2282\\GSE86338\\aligned\\aligned_metadata_kept.csv", "columns": {"grp": {"source": "title", "regex": "^iWAT_(Control|Cl316243|4oC7day|swimming)_\\d$", "recode": {"Control": "CNT", "Cl316243": "CL", "4oC7day": "COLD", "swimming": "SWIM"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\86991572b4ea250a7e68eadebb3fa005f4fe2282\\GSE86338\\aligned\\design_metadata.csv", "sha256": "2deae133a44c12246729f7f838fb0e13ec58a604a5f8345ec88908aac8df5d60", "levels": {"grp": {"CN ... [40 more characters]

reasoning: Matrix columns equal metadata 'description' 18/18 (inspect alignment_keys). Group derived from GEO title. BAT samples belong to different experiments with their own controls (S2.3.p1) and are excluded; comparisons never cross tissue.

### matrix (valid, not_started)

final: {"matrix_type": "FPKM (linear, Cufflinks)", "recommended_method": "limma on log2(FPKM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\86991572b4ea250a7e68eadebb3fa005f4fe2282\\GSE86338\\aligned\\aligned_matrix.csv", "sha256": "c07a44a1cf15a0383173d7e1a318f953e817314e65452ddadf5b3758fbbe402c", "n_features": 38553, "n_samples": 8, "annotation_columns_dropped": ["GSM2300503", "GSM2300504", "GSM2300505", "GSM2300506", "GSM2300507", "GSM2300508", "GSM2300509", "GSM2300510", "GSM2300511", "GSM2300512"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 4508350.0, "median": 0.0025673049999999998, "integer_fraction": 0.4999, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name gene_fpkm, data_processing states Cufflinks FPKM, values are non-integer (integer fraction 0.52 driven by zeros), median 0. Paper input for Cuffdiff was the read alignments; counts were not deposited. Linear normalized expression -> log2(x+1) then limma per policy.

### design (refused, not_started)

final: {"analysis_type": "multi-level one control (iWAT browning arms vs shared control)", "design_column": "grp", "formula": "~ grp", "contrasts": [{"name": "grp_SWIM_vs_CNT", "control": "CNT", "treatment": "SWIM", "role": "primary"}, {"name": "grp_COLD_vs_CNT", "control": "CNT", "treatment": "COLD", "role": "exploratory"}, {"name": "grp_CL_vs_CNT", "control": "CNT", "treatment": "CL", "role": "exploratory"}], "suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\86991572b4ea250a7e68eadebb3fa005f4fe2282\\GSE86338\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 0}}

reasoning: One control (CNT) with three iWAT treatments sharing it (S2.1.p1): one model, planned contrasts, no pooling of arms. Exercise contrast is primary; cold and CL arms are exploratory context for the paper's counts. Each arm has n=2 pooled libraries -> exploratory label per contract. Suitability report (GSE86338/suitability/suitability.md) failed sample_size for every comparison; the design is refused at this gate.

rejected alternatives: [{"value": "two-group SWIM vs CNT fit on 4 samples only", "reason_rejected": "residual df = 2; kept only as a sensitivity run. The paper's Cuffdiff run models all iWAT conditions together, so a one-model fit over the 4 iWAT groups (df = 4) is closer."}, {"value": "include BAT samples in one model", "reason_rejected": "different tissue and experiments with their own controls; comparisons must not cross tissue"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/6 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 8 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "library_strategy of CL316243 iWAT samples",
    "paper": "polyA RNA-seq for all browning arms (S4.2.p1)",
    "data": "GEO lists GSM2300497/8 as RIP-Seq / library_selection other",
    "disposition": "executable_without_change"
  },
  {
    "item": "age of swimming mice",
    "paper": "swimming started at 8 weeks, ~3-4 weeks of protocol (S4.4.p1); browning cohort 12 weeks old",
    "data": "all iWAT samples annotated 16 weeks old",
    "disposition": "executable_without_change"
  },
  {
    "item": "DE method and input",
    "paper": "Cuffdiff on alignments (S4.3.1.p1)",
    "data": "only Cufflinks FPKM deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "replicates per arm",
    "paper": "2 pooled libraries per condition, Cuffdiff run with n=2 (S4.2.p1, S2.4.p1: 18 samples)",
    "data": "2 libraries per iWAT arm; suitability requires >= 3",
    "disposition": "stop"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE86338 (PMC5538645, lncBATE10 / adipose browning)

## Outcome: refused at `design`

Validator: 5 records, 0 errors. Case status `stopped:design`, decision `refused`, execution `not_run`.

## What ran

1. `case_runner inspect GSE86338`: downloaded the series. Files: `GSE86338_gene_fpkm.txt.gz` (38,553 Ensembl genes x 18), `GSE86338_lncRNA_fpkm.txt.gz` (1,535 x 18), metadata.
2. Paper reconstruction from PMC5538645.paper.md:
   - Exercise arm: iWAT after a swimming program (S2.1.p1, S4.4.p1), compared with the room-temperature control iWAT. The cold (4C, 7 d) and CL316243 arms share that control.
   - Method: Cufflinks FPKM with compatible-hits-norm, then Cuffdiff (S4.3.1.p1).
   - Threshold: FDR <= 0.05 and |FC| >= 2 (S2.2.p1).
   - Paper's exercise result: 673 up and 826 down mRNAs (1,499).
3. Ownership confirmed: GSE86338 is cited in FN.p1 and S4.2.p1. GEO has 18 samples, as in the paper's PCA (S2.4.p1).
4. Alignment: matrix columns match the metadata `description` field exactly, 18 of 18. Group comes from the title (CNT/CL/COLD/SWIM). The 10 BAT samples (S3, S5) belong to separate experiments with their own controls, so they were excluded.
5. Matrix: Cufflinks FPKM, so the route would be log2(x+1) then limma. The Cuffdiff route is blocked because no alignments or counts were deposited.
6. Design: the suitability report is `not_analyzable` (sample_size: 0 of 6 comparisons have >= 3 per group).
   - Every iWAT arm has 2 libraries, and each library is a pool of 4 mice (S4.2.p1).
   - The planned exercise contrast, SWIM n=2 vs CNT n=2, cannot be recorded as valid, so the case is refused at this gate.
   - The planned route is written in the stop_reason: one limma model ~ grp over the 8 iWAT samples (residual df 4), contrast SWIM vs CNT, using the paper's threshold.

## DEG counts vs paper

- No DE was run, so there are no counts. The paper reports 673 up and 826 down mRNAs for exercise (FDR <= 0.05, |FC| >= 2).
- For context only, from the same paper: cold 1,062 / 1,201 and CL316243 837 / 681.

## Deviations / discrepancies recorded

- Paper method (Cuffdiff on alignments) is blocked because only FPKM was deposited.
- GEO labels the CL316243 iWAT samples (GSM2300497/8) as RIP-Seq / library_selection "other". The paper describes polyA RNA-seq, so this is most likely a GEO labelling error.
- GEO lists all iWAT samples as 16 weeks old. The paper says the browning cohort was 12 weeks old, and the swim protocol started at 8 weeks and ran about 3–4 w ... [1077 more characters]
