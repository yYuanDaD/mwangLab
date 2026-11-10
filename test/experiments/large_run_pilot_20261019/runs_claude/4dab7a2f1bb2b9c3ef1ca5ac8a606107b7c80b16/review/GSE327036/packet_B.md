# Review packet B (the analysis' decisions): GSE327036

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.1.genotype level", "across": "characteristics_ch1.1.genotype", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: GSE327036 contains only WT vs STARD7 muscle-KO soleus (3 vs 3) at baseline; exercise (treadmill) was a phenotyping test on other animals, so the data cannot identify an effect of exercise on gene expression.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE327036"], "assay": "bulk RNA-seq (poly(A) mRNA, Illumina), mouse soleus muscle", "sample_inclusion": "soleus from Stard7 flox/flox control (Cont) and Myf5-Cre; Stard7 flox/flox muscle-specific KO (mKO) mice, n = 3 biological replicates per group (S2.5.p1, FLT.p3)", "factors": {"genotype": ["Cont (Stard7 flox/flox)", "mKO (Myf5-Cre; Stard7 flox/flox)"]}, "exercise_in_rnaseq": "none: treadmill running (S2.3.p1) and lactate tests (S2.4.p1) are phenotyping assays; the RNA-seq samples (S2.5.p1, S3.3.p1) are not described as exercised or as harvested after a bout, and no exercise arm exists in the transcriptome design", "primary_estimand": "genotype effect (STARD7 mKO vs control) on soleus gene expression at baseline; not an exercise effect", "planned_contrasts": ["mKO vs Cont in soleus (FLT.p3 Fig. 3B/3C; paper DEG count not stated in text; named down genes Mybpc2, Actn3, Pvalb, Mct4 (Slc16a3), Myh4; Myh7 unchanged)"], "repeated_measure_unit": "none (independent animals)", "normalization": "CLC Genomics Workbench counts -> TPM, log2(TPM+1) for PCA/heatmap (S2.5.p1); edgeR with filterByExpr for DE (FLT.p3)", "paper_method": "edgeR (filterByExpr) mKO vs Cont, analysed in OlvTools", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "FLT.p3"}, "paper_results": "Fast-twitch genes Mybpc2, Actn3, Pvalb, Mct4, Myh4 down in mKO; Myh7 unchanged; GO 'muscle system process' top term (S3.3.p1)"}

reasoning: The only transcriptomic experiment is soleus RNA-seq of control vs muscle-specific STARD7 KO mice (S2.5.p1, S3.3.p1, FLT.p3). Exercise appears only as an outcome/phenotyping assay (treadmill endurance S2.3.p1, lactate before/after a bout S2.4.p1) on separate cohorts (male n=6, female n=9, FLT.p2); the RNA-seq animals have no exercise vs sedentary contrast.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE327036\\GSE327036_merged_from_tar.csv", "owned": true, "checks": ["GEO contact Yasuhiro Horibata, Dokkyo Medical University = corresponding author/affiliation", "6 soleus samples, WT x3 and mKO x3 = paper S2.5.p1 'three biological replicates per group'", "sample file names Horibata_Control_1-3 / Horibata_KO_1-3", "DA.p1 says RNA-seq will be deposited in GEO (accession not named in the preprint)"], "accession": "GSE327036", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE327036\\GSE327036_metadata.csv"}

reasoning: Submitter, tissue, genotype groups and replicate numbers match the paper; the paper does not cite the accession (DA.p1, deposited on acceptance), so ownership rests on these matching facts.

### alignment (valid, not_started)

final: {"method": "exact:geo_accession", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\4dab7a2f1bb2b9c3ef1ca5ac8a606107b7c80b16\\GSE327036\\aligned\\aligned_metadata.csv", "columns": {"genotype": {"alias_of": "characteristics_ch1.1.genotype", "recode": {"WT": "WT", "mKO": "mKO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\4dab7a2f1bb2b9c3ef1ca5ac8a606107b7c80b16\\GSE327036\\aligned\\design_metadata.csv", "sha256": "fee08ff86d68e7b80e14d0a037f1eb77aad7a5f4911e8a61b92ce9e1c08f03e3", "levels": {"genotype": {"WT": 3, "mKO": 3}}}}

reasoning: Matrix columns are GSM ids with the library file stem appended; the regex keeps the GSM id and matches geo_accession exactly (6/6). The genotype column is aliased to a formula-safe name.

### matrix (valid, not_started)

final: {"source": "GSE327036_RAW.tar: per-sample CLC files GSM*_Horibata_*_GE_.txt.gz with columns 'Name','TPM'; merged by the runner into GSE327036_merged_from_tar.csv", "paper_input": "edgeR with filterByExpr on CLC read counts (FLT.p3); TPM/log2(TPM+1) for PCA/heatmap (S2.5.p1)", "matrix_type": "TPM", "recommended_method": "limma (log2(TPM+1)); edgeR on counts not possible from deposited files", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\4dab7a2f1bb2b9c3ef1ca5ac8a606107b7c80b16\\GSE327036\\aligned\\aligned_matrix.csv", "sha256": "82e25175f779bd44e18c8c13cef3af686185cdb5678f567cb2997316c9466eb3", "n_features": 43074, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 90451.6620634077, "median": 0.0, "integer_fraction": 0.5371, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Each per-sample file has header 'Name\tTPM' and the values of a sample sum to 1e6; integer fraction 0.54 with fractional values. GEO data_processing says 'raw gene counts', which contradicts the file contents; the file header and per-sample sums decide: TPM. Counts for the paper's edgeR route are not deposited.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_factor": null, "available_contrast": "genotype mKO vs WT (not an exercise contrast)", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\4dab7a2f1bb2b9c3ef1ca5ac8a606107b7c80b16\\GSE327036\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: The request is the effect of exercise on gene expression as the paper intends. The paper's RNA-seq estimand is a genotype effect (S3.3.p1, FLT.p3); the only grouping column is genotype (WT 3 / mKO 3) and tissue is constant (soleus). No exercise, training, time-after-bout or sedentary label exists in metadata or paper for these samples. Refused at design.

rejected alternatives: [{"value": "genotype_mKO_vs_WT as an exercise contrast", "reason_rejected": "genotype (STARD7 KO) is not an exercise intervention; none of the 6 RNA-seq animals was assigned to exercise vs sedentary, so the exercise estimand the request asks for is not identified"}, {"value": "treat reduced endurance of mKO as an exercise proxy", "reason_rejected": "endurance capacity is a phenotypic outcome measured on separate cohorts (FLT.p2); it is not a manipulated exercise exposure of the sequenced samples ... [3 more characters]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix content",
    "paper": "edgeR on read counts after filterByExpr (FLT.p3)",
    "data": "GEO data_processing claims raw gene counts, but every per-sample file holds a single TPM column (header 'TPM', sums 1e6)",
    "disposition": "recorded; would block the paper's edgeR route (case stopped before method)"
  },
  {
    "item": "reference genome and software",
    "paper": "GRCm38 release-94, CLC Genomics Workbench v22.0.1 (S2.5.p1)",
    "data": "GRCm39, CLC Genomics Workbench v23.0.2 (GEO data_processing)",
    "disposition": "recorded; does not affect the refusal"
  },
  {
    "item": "sequencer",
    "paper": "Illumina NextSeq500, 75-bp paired-end (S2.5.p1)",
    "data": "Illumina NovaSeq 6000 (GEO instrument_model)",
    "disposition": "recorded; does not affect the refusal"
  },
  {
    "item": "exercise estimand",
    "paper": "RNA-seq compares mKO vs control soleus; exercise only as phenotyping on separate cohorts",
    "data": "only genotype WT/mKO, no exercise arm",
    "disposition": "blocks the requested exercise estimand; refused at design"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE327036 (STARD7 muscle KO, soleus)

## Outcome
STATUS: refused at the `design` gate. No DE was run.

## What ran
1. `python -m tools.case_runner inspect GSE327036`: downloaded the series and merged `GSE327036_RAW.tar` (6 per-sample CLC files) into `data/GSE327036/GSE327036_merged_from_tar.csv`, 43,074 genes x 6 samples.
2. `python -m tools.case_runner execute case_spec.json`: these gates were recorded: paper_reconstruction, ownership, alignment (exact on geo_accession, 6/6), matrix (TPM) and design (refused). The validator returned 0 errors on 5 records. Case status is `stopped:design`.

## Why refused
The request asks how exercise affects gene expression. The paper's only transcriptome experiment is soleus RNA-seq comparing Stard7 flox/flox controls with Myf5-Cre STARD7 muscle-KO mice, 3 vs 3 (S2.5.p1, S3.3.p1, FLT.p3). Exercise appears only in phenotyping tests on separate cohorts: treadmill endurance (S2.3.p1) and lactate around a running bout (S2.4.p1; males n=6, females n=9 per FLT.p2). GEO has a single grouping column, genotype (WT 3 / mKO 3), and tissue is soleus for every sample. No exercise or sedentary arm exists, so the exercise estimand cannot be identified. I rejected two alternatives: treating genotype as the contrast, and treating the KO's low endurance as an exercise proxy.

## DEG counts vs paper
- Not run, so there are no counts. Paper threshold: FDR < 0.05 and |logFC| > 1, edgeR after filterByExpr (FLT.p3).
- The paper's text gives no DEG total. The genes it names as down in mKO are Mybpc2, Actn3, Pvalb, Mct4 and Myh4; Myh7 is unchanged.

## Deviations and paper-vs-data discrepancies (recorded in paper_data_discrepancies.json)
- **Matrix type.** GEO `data_processing` says "raw gene counts". Each per-sample file actually holds one `TPM` column, and each sample sums to 1e6. Read counts for the paper's edgeR route are not deposited, so a genotype reproduction would itself be a declared deviation (limma on log2(TPM+1)).
- **Genome and software.** The paper says GRCm38 rel-94 with CLC v22.0.1. GEO says GRCm39 with CLC v23.0.2.
- **Sequencer.** The paper says NextSeq500, 75-bp paired-end. GEO says NovaSeq 6000.
- **Ownership.** The preprint does not cite the accession (DA.p1: "will be deposited"). Ownership is confirmed (medium confidence) from the matching submitter, tissue, groups, n, and sample names `Horibata_Control_*` / `Horibata_KO_*`.

## Tool problems
- The tar merge replaces the per-sample value column header (`TPM`) wi ... [509 more characters]
