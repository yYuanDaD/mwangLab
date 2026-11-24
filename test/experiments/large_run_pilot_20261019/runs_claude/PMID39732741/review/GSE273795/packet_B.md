# Review packet B (the analysis' decisions): GSE273795

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: all 6 samples are HFD-fed mice split only by drug (R159 vs vehicle). Wheel running is a behavioural outcome, not a group factor, so exercise effects on gene expression cannot be identified from GSE273795.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE273795"], "assay": "bulk polyA RNA-seq, mouse liver (S9.p1; Methods RNA-seq paragraph, line 111-115 of paper.md)", "primary_estimand": "Effect of the gp130 Y814 inhibitor R159 vs vehicle on liver gene expression in aged (16-month) male C57BL/6 mice on high-fat diet (Fig. 3e,f). Exercise is not an intervention in this paper: voluntary wheel running is measured only as a behavioural outcome (Fig. legend line 63).", "factors": {"treatment": ["HFD, Vehicle", "HFD, R159"]}, "sample_inclusion": "n = 3 livers per group (Fig. 3e,f legend)", "planned_contrasts": ["HFD-R159 vs HFD-Veh in liver (Fig. 3e,f; no DEG count reported, heat map of inflammation/fibrosis genes only)"], "exercise_contrast": "none: no exercise vs sedentary arm exists; wheel running is an outcome, not a factor", "paper_method": "DESeq2 on median-ratio-normalized EM-quantified counts", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "source_locator": "Methods RNA-seq paragraph: fold change > 1.5 and p-value < 0.05"}, "paper_results": "Veh up vs R159: Ccl2, Tlr5, Col1a1, Ctsk, Mmp2, Pdgfc, Apob, Lpl, Sele, Vcam1; no DEG total given"}

reasoning: The paper studies a drug (R159) in HFD-fed aged mice. The only RNA-seq experiment (GSE273795, S9.p1) is liver R159 vs vehicle, n = 3 per group (Fig. 3 legend). Voluntary wheel running (Fig. legend at paper.md line 63, Discussion line 81) is a measured activity outcome, not an exercise intervention, and no RNA-seq sample is defined by exercise.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE273795\\GSE273795_merged_from_tar.csv", "owned": true, "checks": ["S9.p1 names GSE273795", "GEO treatment_protocol: 1-year-old male C57BL/6 on HFD, R159 or Veh i.p. twice weekly for 12 weeks, matching paper", "6 liver samples = 3 + 3 as in Fig. 3e,f"], "accession": "GSE273795", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE273795\\GSE273795_metadata.csv"}

reasoning: Accession, tissue, treatment protocol and n match the paper.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39732741\\GSE273795\\aligned\\aligned_metadata.csv", "columns": {"treat": {"alias_of": "characteristics_ch1.2.treatment"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39732741\\GSE273795\\aligned\\design_metadata.csv", "sha256": "8fad157e94f851812b5c241d643b74994a400c882fee46e09e84ac7cbd06f1b1", "levels": {"treat": {"HFD, R159": 3, "HFD, Vehicle": 3}}}}

reasoning: Tar-merged columns carry the GSM id as prefix; inspect shows 6/6 exact matches on the metadata index. Treatment column copied to a formula-safe alias.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39732741\\GSE273795\\aligned\\aligned_matrix.csv", "sha256": "de3821d85be3df3657fa6430e534d7863e114b3547f614fe457ca87d640bda82", "n_features": 18705, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 4790000.0, "median": 326.766, "integer_fraction": 0.038, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Files are named *_normalized_counts; 3.8% integer values, max 4.79e6; GEO data_processing: STAR + EM quantification, 'Normalization was done using median ratio method'. These are DESeq2-style size-factor-normalized EM estimates, not raw counts. Not used further because the case stops at design.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_factor": null, "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39732741\\GSE273795\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Metadata has one grouping column (treatment: HFD, R159 = 3; HFD, Vehicle = 3). The paper's RNA-seq contrast is drug vs vehicle (Fig. 3e,f). Manufacturing an exercise contrast is not possible, and the drug contrast does not answer the exercise request.

rejected alternatives: [{"value": "treat: HFD, R159 vs HFD, Vehicle", "reason_rejected": "drug effect, not exercise; the request asks for the exercise effect"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix input",
    "paper": "DESeq2 on counts (Methods)",
    "data": "GEO deposits only median-ratio normalized counts per sample",
    "disposition": "not_evaluated_case_stopped"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID39732741 / GSE273795

**Status: refused at the `design` gate.** The data cannot answer the exercise question.

## What ran
- `python -m tools.case_runner inspect GSE273795`: downloaded the series to `data/GSE273795`. The tar merged into 18,705 genes × 6 samples (`*_normalized_counts`).
- `python -m tools.case_runner execute case_spec.json`: the runner recorded paper_reconstruction, ownership, alignment (6/6 exact matches on GSM), matrix, and design (refused). The validator reported 0 errors.
- It ran twice. The first attempt is kept in `_previous/20261124T044942Z`. Its stop_reason called the mice "sedentary-housed", which the paper does not support, since the paper measures voluntary wheel running. I removed that wording and ran it again.

## Why it was refused
- The paper is about a drug: R159, a gp130 Y814 inhibitor, compared with vehicle in aged male mice on a high-fat diet (HFD).
- The only RNA-seq experiment is liver, HFD-R159 vs HFD-Veh, n = 3 per group (Fig. 3e,f; S9.p1).
- Voluntary wheel running appears only as a behavioural outcome (activity and motivation, Fig. legend at paper.md line 63; Discussion line 81). No group is defined by exercise.
- The GEO metadata has a single factor, treatment (HFD, R159 = 3; HFD, Vehicle = 3). With no exercise vs sedentary arm, the exercise estimand cannot be identified. The drug contrast is analyzable, but it does not answer the exercise request, so I did not run it.

## DEG counts vs paper
- None computed, because the case stopped before execution.
- The paper gives no DEG total either. It shows enriched terms and a heat map (Ccl2, Tlr5, Col1a1, Ctsk, Mmp2, Pdgfc, Apob, Lpl, Sele, Vcam1).
- The paper's threshold is raw p < 0.05 and fold change > 1.5, i.e. |log2FC| > 0.5849625 (Methods, RNA-seq paragraph). It was recorded in paper_reconstruction.

## Deviations
- None. No analysis was executed.
- Recorded discrepancy (not evaluated because the case stopped): GEO deposits only median-ratio-normalized EM estimates, not raw counts. I recorded the matrix as `estimated counts` with medium confidence.

## Tool problems
- None blocking.
- Minor: the matrix policy has no type word for already size-factor-normalized counts (a DESeq2 median-ratio matrix), so I used `estimated counts`. See `.claude/skills/bioinformatics-workflow/references/matrix-method-policy.md`, which has no "normalized counts" entry.

