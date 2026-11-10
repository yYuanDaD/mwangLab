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
- The tar merge replaces the per-sample value column header (`TPM`) with the sample name (tools/geo_tar.py:119-120). Neither the inspect JSON nor the log reports which column `choose_count_column` picked or why (tools/geo_tar.py:114-118). Inspect labelled the merged matrix "linear_normalized or estimated_counts". Identifying it as TPM, which contradicts the GEO "raw gene counts" note, meant opening the tar members by hand. Suggestion: record the chosen column name and reason in the inspect `notes`.
- No other problems: alignment, suitability and the validator ran cleanly.
