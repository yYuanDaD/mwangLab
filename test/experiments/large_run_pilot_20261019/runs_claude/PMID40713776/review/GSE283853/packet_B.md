# Review packet B (the analysis' decisions): GSE283853

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the grp level", "across": "grp", "pairs_or_sets": 3, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: GSE283853 is an in-vitro gain-of-function experiment (adenoviral MAFA/MAFB/MAF overexpression vs mCherry in iPSC-derived myotubes). There is no exercise, training, or physical-activity arm, so the requested exercise estimand cannot be identified from this series. The paper's exercise-related data (endurance- vs power-trained biopsies) are in GSE200398/dbGaP, not GSE283853.

## Samples per design level

### `grp`
- **MAF** (3): GSM8673181 / pAV-MAF_1 / Library name: c1; GSM8673182 / pAV-MAF_2 / Library name: c2; GSM8673183 / pAV-MAF_3 / Library name: c3
- **MAFA** (3): GSM8673175 / pAV-MAFA_1 / Library name: a1; GSM8673176 / pAV-MAFA_2 / Library name: a2; GSM8673177 / pAV-MAFA_3 / Library name: a3
- **MAFB** (3): GSM8673178 / pAV-MAFB_1 / Library name: b1; GSM8673179 / pAV-MAFB_2 / Library name: b2; GSM8673180 / pAV-MAFB_3 / Library name: b3
- **mCherry** (3): GSM8673172 / pAV-mCherry_1 / Library name: m1; GSM8673173 / pAV-mCherry_2 / Library name: m2; GSM8673174 / pAV-mCherry_3 / Library name: m3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE283853"], "assay": "bulk total-RNA RNA-seq (rRNA-depleted, NextSeq500 2x36) of human iPSC-derived (414C2 iMuSC) myotubes, day 4 after adenoviral infection (S2.10.p1)", "samples": "12 cultures: pAV-mCherry (control), pAV-MAFA, pAV-MAFB, pAV-MAF, n=3 each (FIG4 C-H)", "factors": {"grp": ["mCherry", "MAFA", "MAFB", "MAF"]}, "primary_estimand": "Effect of adenoviral overexpression of each large MAF transcription factor (MAFA, MAFB, MAF) versus mCherry control on the myotube transcriptome; not an exercise estimand", "planned_contrasts": ["MAFA vs mCherry (FIG4.A; paper: 3,685 DEGs)", "MAFB vs mCherry (FIG4.A; paper: 2,289 DEGs)", "MAF vs mCherry (FIG4.A; paper: 4,446 DEGs)"], "paper_method": "CLC Main Workbench Empirical Analysis of DGE (edgeR exact test), genes with zero counts in any sample excluded (S2.10.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.10.p1"}, "exercise_component": "Exercise/training appears only in the human biopsy analyses (GSE200398 Russian endurance- vs power-trained, resting-state, cross-sectional; dbGaP phs001048 Finnish), which are separate accessions (S2.18.p1, S3.4.p3, DA.p1). GSE283853 contains no exercise, training, or physical-activity factor."}

reasoning: S2.10.p1 describes the GSE283853 experiment: myotubes overexpressing MAFA/MAFB/MAF or mCherry, edgeR test, FDR < 0.05. FIG4.A gives DEG counts per MAF vs control. DA.p1 maps GSE283853 to the myotube RNA-seq only; the training-background comparison (S3.4.p3) uses GSE200398, not this series.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40713776\\prep\\GSE283853_expression_values.csv", "owned": true, "checks": ["DA.p1 names GSE283853 for RNA-seq of human iMuSC-derived myotubes", "GEO cell type 'iPS cell-derived myotubes', cell line 414C2, 12 samples pAV-mCherry/MAFA/MAFB/MAF x3, NextSeq 500 match S2.10.p1"], "accession": "GSE283853", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE283853\\GSE283853_metadata.csv"}

reasoning: Metadata and the CLC export (sample groups pAV-mCherry, pAV-MAFA, pAV-MAFB, pAV-MAF; library names m/a/b/c 1-3) match the paper's myotube experiment.

### alignment (valid, not_started)

final: {"method": "exact:lib", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40713776\\GSE283853\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^pAV-(mCherry|MAFA|MAFB|MAF)_\\d$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40713776\\GSE283853\\aligned\\design_metadata.csv", "sha256": "392077be92cb352c62d36cdb711a14d0983a16faf7cb69ba1c74a12041416b07", "levels": {"grp": {"mCherry": 3, "MAFA": 3, "MAFB": 3, "MAF": 3}}}}

reasoning: The deposited CLC export has per-sample columns '<lib> - Expression values'; the prep script keeps those 12 columns and renames them to the library name, which equals the metadata 'description' field ('Library name: m1'). Group taken from title.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "source": "CLC 'Expression values' columns (total read counts per gene) from GSE283853_ProcessedData_quantile_totalcount_normalized_ANOVA.csv", "paper_input": "CLC total read counts analyzed with the edgeR test (S2.10.p1)", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40713776\\GSE283853\\aligned\\aligned_matrix.csv", "sha256": "9260e3467aeeb9ca1c0d904d3236a7b4fe6487523d755d334d5c19a7d36f5a20", "n_features": 57773, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 188793.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: The 12 extracted 'Expression values' columns are all integers (file name 'totalcount'); the 'Normalized expression values' (quantile) and 'Transformed values' columns plus group means were dropped. S2.10.p1 runs edgeR on these counts.

rejected alternatives: [{"value": "Normalized expression values (quantile)", "reason_rejected": "quantile-normalized, not counts; not the paper's edgeR input"}]

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "grp", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40713776\\GSE283853\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: The only factor is the overexpressed transgene (title pAV-*; S2.10.p1; FIG4). A MAF-vs-mCherry contrast is valid for the paper's own question but does not answer how exercise affects gene expression; manufacturing an exercise interpretation would be invalid. Refused at design.

rejected alternatives: [{"value": "grp MAFA/MAFB/MAF vs mCherry (paper's planned contrasts)", "reason_rejected": "transgene overexpression in culture, not an exercise intervention; outside the requested estimand"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference completed on 12 samples.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "requested estimand",
    "paper": "GSE283853 = MAF overexpression in myotubes (S2.10.p1, DA.p1); training comparison uses GSE200398 (S3.4.p3)",
    "data": "12 myotube cultures, groups pAV-mCherry/MAFA/MAFB/MAF",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID40713776 / GSE283853

## Outcome: refused at the `design` gate

GSE283853 is the paper's in-vitro experiment. Human iPSC-derived (414C2) myotubes were given adenoviral pAV-mCherry (control), pAV-MAFA, pAV-MAFB or pAV-MAF, with n=3 per group and 12 samples in total (S2.10.p1, FIG4, DA.p1). The series has no exercise, training or physical-activity factor, so the requested exercise estimand cannot be identified from it. The paper's only training-related analysis compares endurance-trained with power-trained resting biopsies. That analysis is cross-sectional and uses GSE200398 (Russian cohort) and dbGaP phs001048 (Finnish cohort), not this series (S2.18.p1, S3.4.p3).

## What ran

- `tools.case_runner inspect GSE283853`: the data were already cached in E:/agent/mwangLab_pdf/data.
- `prep/extract_counts.py`: the deposited CLC export (`GSE283853_ProcessedData_quantile_totalcount_normalized_ANOVA.csv`) has 48 columns. Each of the 12 samples has three: Expression values, Normalized expression values and Transformed values. There are also 12 group-mean columns. The script keeps the 12 integer "<lib> - Expression values" columns, which are the total read counts, and renames them to the library names m1..c3. Output: `prep/GSE283853_expression_values.csv`.
- `tools.case_runner execute case_spec.json`: 5 records were written (paper_reconstruction, ownership, alignment, matrix, design). Alignment matched all 12 of 12 samples exactly, using `lib` taken from `description` ("Library name: m1"). The matrix type is raw counts (CLC total counts). The design was refused, and the validator reported 0 errors.

## DEG counts vs the paper

None were computed (refused). For reference, the paper reports these counts for the non-exercise contrasts (FIG4.A), using an edgeR exact test in CLC with FDR < 0.05 and no fold-change cutoff (S2.10.p1):

| Contrast | Paper DEGs |
|---|---|
| MAFA vs mCherry | 3,685 |
| MAFB vs mCherry | 2,289 |
| MAF vs mCherry | 4,446 |

The suitability report rates all 6 MAF/mCherry comparisons as analyzable. They fall outside the exercise request, so they were not run.

## Deviations

- The matrix was repaired with a prep script, which selects the count columns and renames them. The script is listed in `prep_scripts`.

## Tool problems

- Minor: `inspect` profiles every column of a CLC Workbench export as a sample (`tools/case_runner.py:361`). It reports 48 "samples", an integer fraction of 0.78 and a "linear_normalized or estimated_counts" c ... [335 more characters]
