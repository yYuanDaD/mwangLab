# HANDBACK: PMID41078024 / GSE302532

## What ran
- Case spec route (`tools.case_runner execute case_spec.json`); validator: 10 records, 0 errors; status completed.
- Data: `GSE302532_ExerciseExosomeTPMs.csv` (CLC Genomics Workbench v25 TPM, 29,541 features x 8 samples; every column sums to 1e6). Rat plasma exosome total RNA-seq, 4 Sedentary vs 4 Exercised (non-PD cohort 2, S2.1.p1, S2.5.p1).
- Prep: `prep_rename_columns.py` renames columns `Sedentary - 437P_S7 (GE) - TPM` to the GEO library name `437P` (values unchanged, Ensembl `Identifier` column dropped). Alignment exact on the key derived from `description` ("Library name: 437P"), 8/8.
- Design: two-group `~ grp`, EX vs SED, independent animals, no covariates. Suitability: analyzable.
- Method: limma (moderated t, eBayes) on log2(TPM+1); 17,901 features after the executor drops zero-variance rows. No enrichment (paper reports none).

## DEG counts vs paper
- Paper: 27 RNAs upregulated (Table 2, S3.4.p1); no downregulated list. The paper states no rule; Table 2 implies raw P <= 0.05 and FC >= 3 (FC 3.09 to 142.31).
- Applied (workflow_default, BH padj < 0.05, no FC cutoff): 0 DEGs (min padj 0.47).
- Audit (Table 2 implied rule, raw p <= 0.05 and |log2FC| >= log2(3) on log2(TPM+1)): 21 (17 up, 4 down: Alb, Tf, Hpx, LOC120101153). 11 of the 27 Table 2 RNAs pass (Npy, B2m, Mt-atp6, Anp32e, Pf4, Snora81_1, SNORA73, Snord89, Y_RNA_6, LOC120095472, LOC120102095). 14/27 have raw p < 0.05 and positive log2FC.
- Direction: 26/27 Table 2 RNAs positive here. Contradiction: LOC120098346 (paper up 3.25-fold, P 0.04) has log2FC -0.49, p 0.82 (recorded in study caveats). Rgs4 (paper FC 12.9) p = 0.078 here, driven by one exercise sample (452P).

## Deviations
- Paper DE test not named (GEO says CLC Genomics Workbench, which tests counts); only TPM deposited, so limma on log2(TPM+1) is a declared deviation (route `declared_deviation`).
- Threshold: paper states none, so workflow_default applied; Table 2 rule kept as a labelled audit. Paper's 27 rest on uncorrected P.
- log2(TPM+1) compresses fold changes for low-TPM RNAs relative to the paper's FC, so the audit FC filter is stricter than the paper's.
- Sample size discrepancy: S2.5.p1 and GEO give 4 per group; S4.4.p1 says 5 per group. Ran on the 4+4 deposited.

## Tool problems
- `tools/case_runner.py:504` (`native.align_to_metadata`) needs matrix column names to equal a metadata value exactly; when the key is embedded in the matrix column name (`Sedentary - 437P_S7 (GE) - TPM`) there is no spec option (key_patterns only rewrites metadata, line 501), so a prep script was needed to rename matrix columns.
- `inspect` reported `alignment_keys: []` with no hint that the library name sits inside the matrix column names (reverse containment not checked, `tools/case_runner.py` ~297-316).
- Otherwise none.
