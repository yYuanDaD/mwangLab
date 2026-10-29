# HANDBACK: PMID38697122 / GSE242354 (MoTrPAC PASS1B rat endurance training, 8 tissues)

## What ran
- Route: case spec (`case_spec.json`, written by `prep/make_spec.py`), with `python -m tools.case_runner execute`. Run status completed. Validator: 102 records, 0 errors.
- Cases: 8, one for each tissue the paper analyses. These are SKM-GN (gastrocnemius), heart, kidney, liver, lung, hippocampus, BAT and WAT-SC. GEO has 19 tissues; the other 11 are not in the paper and were not run.
- Samples: 50 animals per tissue (5 groups x 5 M + 5 F), aligned exactly on the vial label (`_vial_<id>` in the GEO title, which matches the matrix column). Excluded:
  - MoTrPAC reference-RNA vials ("Reference"), which are not study animals.
  - The female control BAT sample GSM7760555 (vial 90266016902). The paper (S2.1.p1) excludes one female BAT sample that clustered with WAT-SC. Our correlation check (`prep/`) singles out this sample, with r_BAT 0.763 vs r_WAT 0.765; every other BAT sample is at least 0.07 closer to BAT.
- Matrix: RSEM expected counts, rounded before DESeq2. Low-count filter: CPM >= 0.5 in >= 2 samples of the execution (paper S5.4.3.p1).
- Executions per tissue:
  - `pooled`: joint DESeq2 `~ sex + grp`. The primary result is W8 vs SED. W1, W2 and W4 vs SED come from the same fit and are exploratory.
  - `male` and `female`: per-sex joint DESeq2 `~ grp`, all 5 groups, as secondary analyses.
- ORA (Enrichr GO/KEGG) on up and down DEGs from pooled W8 vs SED, for BAT, lung and SKM-GN.

## DEG counts vs paper
Paper threshold (S5.4.3.p2): 5% IHW-FDR on Fisher-combined per-sex DESeq2 LRT p-values (all training groups vs control, with technical covariates). Genes must also have the same week-8 log2FC sign in males and females. There is no fold-change cutoff. The paper reports 3,477 ERGs in total. The text gives only BAT 1,237 and hippocampus 124; the other tissues are only in Fig 6A.

Applied threshold: BH padj < 0.05, no fold-change rule, on pooled Wald W8 vs SED (`paper_on_deviation_route`). The sex-concordant column applies the paper's sign rule afterwards to our pooled DEGs (`prep/sex_sign_agreement.py`, written to `prep/sex_sign_agreement.csv`).

| Tissue | pooled W8 vs SED (up/down) | sex-concordant | paper ERGs |
|---|---|---|---|
| BAT | 2200 (1098/1102) | 2161 | 1237 |
| SKM-GN | 838 (427/411) | 838 | Fig 6A only |
| heart | 968 (541/427) | 967 | Fig 6A only |
| liver | 298 (148/150) | 297 | Fig 6A only |
| kidney | 138 (81/57) | 138 | Fig 6A only |
| lung | 133 (65/68) | 133 | Fig 6A only (~2x more down than up) |
| hippocampus | 29 (2/27) | 21 | 124 |
| WAT-SC | 8 (7/1) | 8 | Fig 6A only |
| total | 4612 | 4563 | 3477 |

- BAT is still the largest tissue and hippocampus among the smallest, as in the paper.
- Our lung result does not reproduce the down-excess the paper reports at week 8: lung W1/W2 vs SED do show it, W8 does not.
- WAT-SC W8 gives very few DEGs. Its W1 contrast has 1,771 DEGs, 2,184 of them in males alone. This looks like a batch or technical effect, which the paper's technical covariates would absorb; those covariates are omitted here.
- Named genes:
  - Gpr37l1 in hippocampus is up as in the paper (log2FC +0.15, p = 1e-4), but padj is 0.059.
  - In heart, Adra1d (-0.70, padj < 1e-4) and Adra1b (-0.14, padj 0.017) are down as in the paper. Adrb1 is down but not significant, and Adra2b is unchanged.
  - In WAT-SC, all four adrenergic receptor genes are down but not significant.
- ORA agrees with the paper (S2.7.p2) for:
  - BAT up: cytokine and TNF/IL-6 production (immune).
  - BAT down: respiration and electron transport chain.
  - SKM-GN up: mitochondrial respiration.
- ORA does not agree for lung down, which shows unfolded-protein response and ECM, not leukocyte migration.

## Deviations (declared in the method gate)
- The paper's DESeq2 LRT per sex, followed by Fisher combination and IHW, was replaced by a Wald W8 vs SED test from one all-group model per tissue, with BH correction. No such executor exists.
- The pooled-sex model uses sex as a covariate. Per-sex models were run as secondary analyses.
- Technical covariates (RIN, UMI duplication and others) were not included. The paper does not list them; it cites MoTrPAC ref 2.
- RSEM counts were rounded to integers. The low-count filter uses `>=` on 2 samples instead of the paper's "<= 0.5 CPM in all but one".
- Damaged matrix rows were dropped (see below): heart lost 125 genes, kidney 31, WAT-SC 23, liver 6 and lung 5, out of 32,883.

## Tool and data problems
- **Data (GEO):** the GSE242354 RSEM files for heart, kidney, liver, lung and WAT-SC contain blocks of NUL bytes. These truncate rows and merge them with the next one. A fresh download from the GEO FTP server has the same size and the same corruption, so the cached copies are faithful copies of the server files.
  - `prep/repair_matrix.py` keeps only intact rows and logs what it dropped in `prep/*_repair_log.json`.
  - Other files on GEO (cortex, adrenal, colon, testes, ovaries, blood, small intestine) also fail to parse or have missing values; they were not used.
- **inspect** (`tools/case_runner.py:358-367`): it reports damaged files only as a pandas `ParserError`, with no diagnosis of the NUL bytes. Lung and small intestine parse "successfully" with silent NaNs (lung: 38 missing values, 4 rows lost).
- **`native.feature_id_report`** (`tools/native.py:609`) reads with `pd.read_csv(..., usecols=[0])` and no separator sniffing. On tab-separated matrices the whole row becomes the "feature ID", so the `feature_examples` that inspect shows are full rows and the ID type is misclassified.
- **`case_runner` `exclude_samples`** (`tools/case_runner.py:505-509`) needs metadata-index IDs (GSM) even when the alignment `key_column` is a derived key such as `vial`. The error does not say so.
- **Missing executor:** there is no DESeq2 LRT, Fisher meta-analysis or IHW executor, so the paper's ERG route is blocked.
