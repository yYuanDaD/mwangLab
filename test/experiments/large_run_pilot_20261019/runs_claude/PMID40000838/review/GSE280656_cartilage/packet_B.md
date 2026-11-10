# Review packet B (the analysis' decisions): GSE280656_cartilage

## Mechanical flags

- none

## Stop reasons

- design (manual_review; claim type: sample_size): Cartilage: control n=3 but every exercise arm (S1, S4, S24, R24) has n=2 pooled replicates, so no planned comparison has >= 3 per arm; the suitability report fails sample_size (not_analyzable), which the decision contract treats as a hard stop. The paper still ran iDEP DESeq2 at n=2. A third replicate per arm, or a contract rule allowing an exploratory n=2 vs n=3 contrast, would unblock it.

## Samples per design level

### `grp`
- **Control** (3): GSM8603244 / Cart_Control_rep1; GSM8603245 / Cart_Control_rep2; GSM8603246 / Cart_Control_rep3
- **R24** (2): GSM8603253 / Cart_Repeated_24hr_rep1; GSM8603254 / Cart_Repeated_24hr_rep2
- **S1** (2): GSM8603247 / Cart_Single_1hr_rep1; GSM8603248 / Cart_Single_1hr_rep2
- **S24** (2): GSM8603251 / Cart_Single_24hr_rep1; GSM8603252 / Cart_Single_24hr_rep2
- **S4** (2): GSM8603249 / Cart_Single_4hr_rep1; GSM8603250 / Cart_Single_4hr_rep2

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE280656"], "primary_estimand": "Effect of overloading exercise (treadmill + 20 g weight) on the cartilage transcriptome at 1, 4, 24 h after a single bout (S1, S4, S24) and 24 h after 4 daily bouts (R24), each versus non-running controls; plus adjacent time-point comparisons", "planned_contrasts": ["S1 vs control (Fig 3a/4a)", "S4 vs S1 (Fig 3b/4b)", "S24 vs S4 (Fig 3c/4c)", "S4 vs control (Fig 3d/4d)", "S24 vs control (Fig 3e/4e)", "R24 vs control (Fig 5)", "R24 vs S24 (Fig 8b)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "source_locator": "S4.4.p2"}, "factors": {"grp": ["Control", "S1", "S4", "S24", "R24"]}, "inclusion": "male C57BL/6J, 10-13 wk; each RNA-seq sample is a pool (synovium 6 knees, cartilage 9 knees); no exclusions (S4.1.p1, S4.4.p1)", "paper_method": "iDEP web app (default DESeq2 on RSEM counts across all groups), FDR < 0.1 and fold change > 2 (S4.4.p2)", "paper_results": "DEG counts per comparison only in Fig 2b (numbers not in text); overlaps: synovium S1&S4 vs control share 52 DEGs, S4&S24 share 9, common S1/S4/S24 = Clec4d, Calca, Ecel1, Saa3 (S2.3.p2); cartilage S1&S4 share 32, S4&S24 share 5, 11 common incl Wnt1, Tnf, Saa3 (S2.4.p2); R24 vs control >> S24 vs control DEGs (S2.5.p1)"}

reasoning: S2.1.p1 defines groups control/S1/S4/S24/R24; S2.2.p1 and Fig 2b compare time points pairwise; S4.4.p2 states iDEP defaults FDR < 0.1, FC > 2. Each tissue is a separate matrix and separate analysis in the paper (Fig 3 synovium, Fig 4 cartilage).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\prep\\GSE280656_cartilage_gene_count_noNaN.csv", "owned": true, "checks": ["S8.p1 names GSE280656", "metadata contact Yusuke Arino (first author Y.A.)", "matrix GSE280656_cartilage_gene_count.txt.gz columns equal the cartilage sample titles", "data_processing (fastp, STAR 2.7.8a, GRCm39/gencode vM33, RSEM 1.3.1) matches S4.4.p2"], "accession": "GSE280656", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE280656\\GSE280656_metadata.csv"}

reasoning: Accession, processing pipeline and sample groups match the paper.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 11, "n_metadata": 26, "coverage": 0.4231, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM8603229", "GSM8603230", "GSM8603231", "GSM8603232", "GSM8603233", "GSM8603234", "GSM8603235", "GSM8603236", "GSM8603237", "GSM8603238", "GSM8603239", "GSM8603240", "GSM8603241", "GSM8603242", "GSM8603243"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_cartilage\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^Cart_(Control|Single_1hr|Single_4hr|Single_24hr|Repeated_24hr)_rep\\d+$", "recode": {"Control": "Control", "Single_1hr": "S1", "Single_4hr": "S4", "Single_24hr": "S24", "Repeated_24hr": "R24"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_cartilage\\aligned\\design_metadata.csv", "sha256": "e09abdc906eea9df0358c132a0b8837cd0e6c8550e0efe4b8a8bb3cf6dda451f", "levels": {"grp": {"Control": 3, "S1": 2, "S4": 2, "S24": 2, "R24": 2}}}}

reasoning: Matrix columns equal metadata title exactly (11/11); the other tissue's samples are in a separate matrix. grp parsed from the title.

### matrix (valid, not_started)

final: {"source": "GSE280656_cartilage_gene_count.txt.gz (57 all-NaN rows dropped by prep/drop_nan_rows.py)", "paper_input": "RSEM expression levels analysed in iDEP with DESeq2 normalization (S4.4.p2-p3)", "matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_cartilage\\aligned\\aligned_matrix.csv", "sha256": "d764e214a3c612eb7d3d1acacc1999564e7e02ff18599a5e49e71d08d0f0faed", "n_features": 56923, "n_samples": 11, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1160797.84, "median": 0.0, "integer_fraction": 0.9318, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: 93% integer values with fractional remainder, library sums ~18-26 M, data_processing says RSEM 'gene count': RSEM expected counts, so DESeq2 after rounding (same as the paper's DESeq2 in iDEP).

### design (manual_review, not_started)

final: {"analysis_type": "multi-group, one model with planned pairwise contrasts", "design_column": "grp", "contrasts": [{"name": "grp_S1_vs_Control", "control": "Control", "treatment": "S1", "role": "primary"}, {"name": "grp_S4_vs_Control", "control": "Control", "treatment": "S4", "role": "primary"}, {"name": "grp_S24_vs_Control", "control": "Control", "treatment": "S24", "role": "primary"}, {"name": "grp_R24_vs_Control", "control": "Control", "treatment": "R24", "role": "primary"}, {"name": "grp_S4_vs_S1", "control": "S1", "treatment": "S4", "role": "secondary"}, {"name": "grp_S24_vs_S4", "control": "S4", "treatment": "S24", "role": "secondary"}, {"name": "grp_R24_vs_S24", "control": "S24", "treatment": "R24", "role": "secondary"}], "suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_cartilage\\suitability\\suitability.md", "n_comparisons": 12, "n_analyzable": 0}}

reasoning: Five independent groups of pooled animals (no subject repeated across groups: separate mice per time point, S2.1.p1). One DESeq2 model on all samples of the tissue, as iDEP does, with the paper's pairwise comparisons. Rejected: pooling single-bout time points; tissue as a factor (paper analyzes tissues separately, separate matrices). Cartilage exercise arms have n=2 (control n=3), so all cartilage contrasts are exploratory. Stopped: the runner's suitability gate (tools/suitability.py:259-277, 502-505) makes sample_size a hard fail when no comparison has n>=3 per arm, and tools/decision_contract.py:172-173 rejects a valid design under that verdict, although the skill says small n alone is not ... [8 more characters]

rejected alternatives: [{"value": "pool S1/S4/S24 as 'single'", "reason_rejected": "paper treats time points as distinct levels"}, {"value": "tissue x grp joint model", "reason_rejected": "paper analyzes tissues separately; separate deposited matrices"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/12 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 11 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DE software",
    "paper": "iDEP web app (DESeq2 default)",
    "data": "pydeseq2 joint model",
    "disposition": "executable_without_change"
  },
  {
    "item": "input values",
    "paper": "RSEM expression levels",
    "data": "RSEM expected counts with decimals; 57 all-NaN rows",
    "disposition": "executable_without_change"
  },
  {
    "item": "replicates",
    "paper": "group sizes in figures",
    "data": "cartilage: control 3, exercise arms 2",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID40000838 / GSE280656

## What ran
- Route: case spec (`case_spec.json`, built by `prep/build_spec.py`; cartilage stop applied by `prep/stop_cartilage.py`). `python -m tools.case_runner execute` finished with status completed and 21 records, 0 validator errors.
- Prep: `prep/drop_nan_rows.py` removed 57 gene rows that are NaN in every sample, in both deposited RSEM matrices. No other values were changed.
- Two cases, one per tissue. The tissues come as separate matrices, and the paper analyses them separately (Fig 3 synovium, Fig 4 cartilage).
  - **GSE280656_synovium** (paper_aligned, completed). There are 15 samples, n=3 in each of Control, S1, S4, S24 and R24. Alignment is exact on `title`. Matrix: RSEM expected counts. The method is one joint pydeseq2 model, `~ grp`, on all 15 samples, which is how iDEP works. Counts were rounded, and the filter kept genes with CPM >= 0.5 in at least 1 sample (the assumed iDEP default). That filter kept 17,315 genes against the paper's 17,316 (S4.4.p3). All 7 planned pairwise contrasts ran. Enrichment: Enrichr ORA up and down plus Hallmark GSEA, for S1 vs control and R24 vs control.
  - **GSE280656_cartilage** (stopped at `design`, `manual_review`). Control has n=3, but each exercise arm has n=2. Because no planned comparison has n >= 3 per arm, the suitability report fails `sample_size` and returns `not_analyzable`, and the contract then refuses to record the design as valid. Nothing was run for cartilage.

## DEG counts (paper threshold: FDR < 0.1 and fold change > 2, i.e. padj < 0.1 and |log2FC| > 1; S4.4.p2, iDEP defaults)
Synovium, our results (up/down). The audit column is padj < 0.05 with no fold-change cutoff.

| Comparison | n (up/down) | audit n |
|---|---|---|
| S1 vs Control | 1104 (598/506) | 4896 |
| S4 vs Control | 412 (180/232) | 1776 |
| S24 vs Control | 171 (83/88) | 500 |
| R24 vs Control | 1844 (1008/836) | 6568 |
| S4 vs S1 | 1373 (626/747) | 5114 |
| S24 vs S4 | 639 (365/274) | 2510 |
| R24 vs S24 | 1377 (699/678) | 5261 |

- The paper gives its DEG counts only as a figure (Fig 2b), and the numbers are not in the text, so no exact count comparison was possible.
- The qualitative pattern matches the paper:
  - S24 vs control has the fewest DEGs in synovium (S2.2.p1).
  - R24 vs control has far more DEGs than S24 vs control (S2.5.p1).
- Named genes match in direction:
  - Nr4a3 is up at S1 (log2FC 4.8) and down from S4 to S24.
  - Inhba is up at S1, at R24 and in R24 vs S24.
  - Saa3, ... [2151 more characters]
