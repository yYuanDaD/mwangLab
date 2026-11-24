# Review packet B (the analysis' decisions): GSE160827

## Mechanical flags

- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"description": ["run0092_lane9_indexN721-S507=50~mouse10_align", "run0092_lane9_indexN722-S508=61~mouse10_align", "run0092_lane9_indexN723-S510=62~mouse10_align", "run0092_lane9_indexN724-S511=63~mouse10_align", "run0092_lane9_indexN726-S502=83~mouse10_align"]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: single EDL fibres from sedentary WT and C2KO mice; only genotype varies. The exercise estimand is not identifiable. (Fibres would also need the donor mouse as blocking unit, 3 WT and 2 KO mice per extract_protocol.)
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE285405", "GSE302562", "GSE160827"], "assay": "single EDL fibre RNA-seq (Illumina HiSeq 4000), male FVB/N mice, 2-3 months; reanalysed from an earlier study", "factors": {"genotype": ["WT", "C2KO"]}, "sample_inclusion": "n = 10 fibres per group (S3.5.p1)", "primary_estimand": "Effect of Mybpc2 knockout on single EDL fibre gene expression in young male mice", "planned_contrasts": ["C2-/- vs WT single EDL fibres (S3.5.p1; paper: 956 DEGs, 621 up / 335 down)"], "exercise_component": "none (S2.5.p1, S3.5.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "source_locator": "S2.11.p1"}, "paper_method": "featureCounts -> edgeR TMM -> limma/voom (S2.11.p1)", "paper_results": {"n_deg": 956, "up": 621, "down": 335, "genes": ["Actc1", "Phlda3", "Atp13a2", "Apcdd1"]}}

reasoning: S3.5.p1 reanalyses GSE160827 (single EDL fibres) for KO vs WT. Genotype only.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE160827\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["S3.5.p1 and S10.p1 name GSE160827", "metadata: EDL single fibres, FVB/N, WT (27) vs C2KO (20); same lab"], "accession": "GSE160827", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE160827\\GSE160827_metadata.csv"}

reasoning: Accession, tissue and genotypes match; sample count differs from the paper (27/20 deposited vs n=10/10 analysed) and the paper does not say which 20 fibres it used.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 47, "n_metadata": 47, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE160827\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "characteristics_ch1.1.genotype/variation", "regex": "^(WT|C2KO)$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE160827\\aligned\\design_metadata.csv", "sha256": "fead85bb3ddde0586bf05199acd1c85db286795a432912de1b13d4be5d054421", "levels": {"grp": {"WT": 27, "C2KO": 20}}}}

reasoning: Tar-merged columns become GSM ids, exact match on the metadata index (47/47).

### matrix (valid, not_started)

final: {"source": "GSE160827_RAW.tar per-sample featureCounts .count files merged", "paper_input": "featureCounts raw counts (S2.11.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE160827\\aligned\\aligned_matrix.csv", "sha256": "48b61132f520dfe60900a3975686c2bc5288811b05ab6eaa67265958ef5b1708", "n_features": 24421, "n_samples": 47, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1269842.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: 100% integer, 0 to 1.27e6; data_processing: featureCounts, 'Supplementary_files_format_and_content: Read counts'.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_factor": null, "available_factor": "genotype WT vs C2KO only", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE160827\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Grouping columns are genotype only; S2.5.p1 describes fibre isolation from untreated mice.

rejected alternatives: [{"value": "grp_C2KO_vs_WT (genotype)", "reason_rejected": "knockout effect, not an exercise effect"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 47 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample count",
    "paper": "n = 10 fibres per group (S3.5.p1)",
    "data": "27 WT and 20 C2KO fibres deposited; selection of the 20 not stated",
    "disposition": "recorded_not_needed_case_refused"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID41229364 (PMC12612635)

Paper: *Fast Myosin Binding Protein-C Is a Vital Regulator in Young and Aged Fast Skeletal Muscle Homeostasis* (J Cachexia Sarcopenia Muscle 2025).

## Outcome: refused (all 3 cases), at the `design` gate

The request asked for the effect of exercise on gene expression. All three RNA-seq series in this paper compare Mybpc2-knockout (C2-/-) mice with wild-type (WT) mice. None of the series has a training, running or acute-exercise arm (S2.11.p1, S3.5.p1, S3.7.p1). The only contraction intervention in the paper, eccentric-contraction injury (S2.3.p1), was measured by Western blot and ELISA in C57BL/6 mice and was never sequenced. So none of the data can answer an exercise question. I did not run the knockout comparison in its place, and I ran no DE model.

## What ran

- `python -m tools.case_runner inspect` for each series (`inspect_<GSE>.json`).
- `python -m tools.case_runner execute case_spec.json` recorded the gates paper_reconstruction → ownership → alignment → matrix → design (refused). The validator passed: 15 records, 0 errors.

| Case | Samples / alignment | Matrix decision | Paper's contrast (not run) |
|---|---|---|---|
| GSE285405 (aged TA, 22 mo) | 8/8 exact on `Library name` key (WT 4, KO 4) | `read_count_*` columns = estimated counts (94% integer, fractional values present) | C2-/-Old vs WT-Old: 310 DEGs (226 up / 84 down) |
| GSE302562 (young TA, 5–6 mo) | 7/7 exact (WT 4, KO 3) | `log2_TMM.csv.gz` = log2 TMM-CPM → limma | C2-/-Young vs WT-Young: only the overlap with aged is reported (45 up / 14 down shared) |
| GSE160827 (young single EDL fibres) | 47/47 exact on GSM (WT 27, C2KO 20) | Merged featureCounts counts from the tar = raw counts | C2-/- vs WT: 956 DEGs (621 up / 335 down), n=10/group |

The paper's threshold (S2.11.p1) is |fold change| > 1.5 (|log2FC| > 0.5849625) with adjusted p < 0.05, using limma/voom after edgeR TMM normalisation. The FIG8 legend instead says "log-transformed fold change cut off of 0.5". I applied no threshold because nothing was executed.

## DEG counts vs paper

None of ours to compare: 0 contrasts ran. The paper's knockout DEG counts are listed above for reference only.

## Deviations and discrepancies (recorded in the spec)

- GSE285405: GEO data_processing says Bowtie2 + DESeq2, and the table carries BGI DESeq2 columns. The paper says featureCounts + limma/voom. The growth protocol says "grown upto 2 months", but the age field says 22 months.
- GSE160827: GEO has 2 ... [1062 more characters]
