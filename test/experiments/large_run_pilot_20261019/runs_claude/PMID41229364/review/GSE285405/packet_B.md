# Review packet B (the analysis' decisions): GSE285405

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.2.genotype", "pairs_or_sets": 4, "samples_linked": 8, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: all 8 samples are sedentary aged male mice differing only by Mybpc2 genotype (WT vs C2-/-). The request's estimand (effect of exercise on gene expression) is not identifiable; the paper's own contrast is a knockout effect, not exercise.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE285405", "GSE302562", "GSE160827"], "assay": "bulk RNA-seq (BGISEQ), TA muscle, male FVB/N mice, 21-22 months", "factors": {"genotype": ["WT", "C2-/- (Mybpc2 KO)"]}, "sample_inclusion": "aged male WT vs C2-/- TA muscle, n = 4 per group (FIG8)", "primary_estimand": "Effect of Mybpc2 (fMyBP-C) knockout on TA muscle gene expression in aged (21-22 mo) male mice; genotype, not exercise", "planned_contrasts": ["C2-/-Old vs WT-Old (S3.7.p1, FIG8; paper: 310 DEGs, 226 up / 84 down)"], "exercise_component": "none: no training, running, or acute exercise arm in any RNA-seq dataset (S2.11.p1). The only contraction intervention in the paper (ECC injury, S2.3.p1) was analysed by Western blot/ELISA in C57BL/6 mice, not sequenced.", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "source_locator": "S2.11.p1"}, "paper_method": "featureCounts -> edgeR TMM -> limma/voom (S2.11.p1)", "paper_results": {"n_deg": 310, "up": 226, "down": 84, "genes": ["Actc1", "Myh13", "Fam174b", "Apold1"]}}

reasoning: S2.11.p1 defines the RNA-seq as genotype comparisons (WT vs C2-/-) at young and old ages; S3.7.p1/FIG8 reports the aged TA comparison on GSE285405. Threshold S2.11.p1: |fold| > 1.5x and adjusted p < 0.05 (FIG8 legend says 'log-transformed fold change cut off of 0.5', which is consistent with log2(1.5)=0.585 rounded). No exercise factor exists.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE285405\\GSE285405_core_table_gene_C2KO_Aging.txt.gz", "owned": true, "checks": ["S3.7.p1 and S10.p1 name GSE285405", "metadata: male TA muscle, 22 months, FVBN WT vs C2-/-, n=4/4, matches FIG8"], "accession": "GSE285405", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE285405\\GSE285405_metadata.csv"}

reasoning: Accession, tissue, age, sex, genotype and n match the paper's aged dataset.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 8, "n_metadata": 8, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE285405\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "description", "regex": "^Library name: (WT|KO)\\d$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE285405\\aligned\\design_metadata.csv", "sha256": "7d3f21baffbf5dffc21042add8ff347d5cbf3a526781ad3fdf0ff630e98df96e", "levels": {"grp": {"WT": 4, "KO": 4}}}}

reasoning: Matrix columns read_count_WT1..KO4 hold the library names given in metadata description ('Library name: WT1'); exact match on the derived key. grp = genotype (WT/KO).

### matrix (valid, not_started)

final: {"source": "GSE285405_core_table_gene_C2KO_Aging.txt.gz read_count_* columns (BGI core table; also holds fpkm/tpm and BGI DESeq2 diffexp columns)", "paper_input": "featureCounts raw counts (S2.11.p1)", "matrix_type": "estimated counts", "recommended_method": "DESeq2 (rounded) or limma-voom", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE285405\\aligned\\aligned_matrix.csv", "sha256": "6f2f5c98fa9beb5fadc1cb4e319975b6871588911aec41a97ffd03c1e3c99763", "n_features": 16687, "n_samples": 8, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 8, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1894356.0, "median": 152.0, "integer_fraction": 0.9402, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: read_count columns are 94% integer with fractional values (e.g. 1544165.29), i.e. estimated counts; GEO data_processing says Bowtie2 + DESeq2, the paper says featureCounts + limma/voom. Type is not decisive for the stop because the case stops at design.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_factor": null, "available_factor": "genotype WT vs C2-/- only", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41229364\\GSE285405\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: S2.11.p1 and FIG8: genotype-only design; metadata grouping column is characteristics genotype only, age/sex/tissue constant. Running a KO vs WT model would not answer the exercise question, so no contrast is manufactured.

rejected alternatives: [{"value": "grp_KO_vs_WT (genotype)", "reason_rejected": "knockout effect, not an exercise effect"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "edgeR TMM + limma/voom (S2.11.p1)",
    "data": "GEO data_processing: Bowtie2 + DESeq2; table carries BGI DESeq2 columns",
    "disposition": "recorded_not_needed_case_refused"
  },
  {
    "item": "growth protocol age",
    "paper": "21-22 months (FIG8)",
    "data": "growth_protocol says 'grown upto 2 months' while age field says 22 Months",
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
