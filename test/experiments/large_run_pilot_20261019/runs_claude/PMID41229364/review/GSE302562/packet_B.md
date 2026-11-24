# Review packet B (the analysis' decisions): GSE302562

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.3.genotype level", "across": "characteristics_ch1.3.genotype", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: 7 sedentary young male mice differing only by Mybpc2 genotype. The exercise estimand is not identifiable.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE285405", "GSE302562", "GSE160827"], "assay": "bulk RNA-seq (BGISEQ), TA muscle, male FVB/N mice, 5-6 months", "factors": {"genotype": ["WT", "C2-/-"]}, "sample_inclusion": "young male WT vs C2-/- TA muscle (S3.7.p1); n not stated in text", "primary_estimand": "Effect of Mybpc2 knockout on TA gene expression in young (5-6 mo) male mice; used to find DEGs shared with the aged comparison", "planned_contrasts": ["C2-/-Young vs WT-Young TA (S3.7.p1; paper reports only the overlap with aged: 45 up / 14 down shared, Figure S8C)"], "exercise_component": "none (S2.11.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "source_locator": "S2.11.p1"}, "paper_method": "featureCounts -> edgeR TMM -> limma/voom (S2.11.p1)", "paper_results": {"n_deg": null, "shared_with_aged": {"up": 45, "down": 14}}}

reasoning: S3.7.p1 introduces GSE302562 as young TA RNA-seq compared against the aged KO DEGs. Genotype only; no exercise.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE302562\\GSE302562_log2_TMM.csv.gz", "owned": true, "checks": ["S3.7.p1 and S10.p1 name GSE302562", "metadata: male TA muscle, 5-6 months, FVBN WT (4) vs C2-/- (3)"], "accession": "GSE302562", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE302562\\GSE302562_metadata.csv"}

reasoning: Accession, tissue, age and genotypes match S3.7.p1.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 7, "n_metadata": 7, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE302562\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "description", "regex": "^Library name: (WT|KO)\\d$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE302562\\aligned\\design_metadata.csv", "sha256": "27166e8deed855b9124b51b303dc3b9f565b16d324ee4eabbfed9ecb7b296b98", "levels": {"grp": {"WT": 4, "KO": 3}}}}

reasoning: Matrix columns WT1_6603 / C2KO1_2880 reduce to WT1 / KO1, matching metadata 'Library name: WT1/KO1' exactly.

### matrix (valid, not_started)

final: {"source": "GSE302562_log2_TMM.csv.gz (GSE302562_DEG.csv.gz is the authors' limma result table, not a matrix)", "paper_input": "featureCounts counts, TMM, limma/voom (S2.11.p1)", "matrix_type": "log2 TMM-normalized expression (log2 CPM)", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE302562\\aligned\\aligned_matrix.csv", "sha256": "7f61854b5203116616bd3244acae14cd5acd03333ba730385587e54ae928dabf", "n_features": 12239, "n_samples": 7, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 4922, "negative_fraction": 0.057451, "min": -4.94126829200687, "max": 15.8987461047078, "median": 3.93653301758388, "integer_fraction": 0.0, "candidates": ["signed_log_scale (log ratios, M-values, or centered data)"]}}

reasoning: Non-integer values -4.9 to 15.9, file name log2_TMM, data_processing describes featureCounts + TMM normalization.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_factor": null, "available_factor": "genotype WT vs C2-/- only", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE302562\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Only grouping column is genotype; age, sex, tissue constant; S2.11.p1 describes no exercise.

rejected alternatives: [{"value": "grp_KO_vs_WT (genotype)", "reason_rejected": "knockout effect, not an exercise effect"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 7 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[]

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
