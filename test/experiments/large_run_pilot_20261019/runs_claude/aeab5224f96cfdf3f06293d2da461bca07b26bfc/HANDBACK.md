# HANDBACK: GSE129962 / PMC7177479 (Cheedipudi et al., Cardiovasc Res 2020)

Paper: "Exercise restores dysregulated gene expression in a mouse model of arrhythmogenic cardiomyopathy". The data are bulk RNA-seq of isolated cardiac myocytes from Myh6-Cre:Dsp W/F (DH) and wild-type (WT) mice, N=5 per group:
- 3M WT and DH;
- 6M WT and DH after regular activity (RA);
- 6M WT and DH after 3 months of treadmill exercise (EX).

The paper used edgeR with q < 0.05 and no fold-change cutoff (S5.7.p2).

Run status: completed, route `declared_deviation`. The contract validator found 0 errors in 18 records.

## What ran

- **Spec:** `case_spec.json` on the case-spec route. `prep/prep_counts.py` removes the 23 ERCC rows (they contain NaN) and the 2 annotation columns. Gene counts are unchanged.
- **Alignment:** exact match of the title prefix to the matrix columns, 30/30. Derived columns: `geno` (WT/DH), `act` (RA/EX), `age` (M3/M6), and `batch` (inferred: b3M, b6RA, b6EX).
- **Key decision at the design gate: the paper's within-genotype exercise contrasts were not run.** These are WT EX vs RA (2529 DEGs in the paper) and DH EX vs RA (2391).
  - Exercise is completely aliased with a processing batch in the deposited data.
  - The 6M-EX samples come from a separate count table: they have no ERCC rows at all, while the 3M and 6M-RA tables each have a different ERCC subset.
  - Technical read composition does not overlap: misc_RNA fraction is 0.35-0.66% in EX vs 0.93-1.31% in 6M-RA and 1.5-2.5% in 3M. Mt_tRNA is non-zero only in 3M.
  - The paper says Tophat2 but GEO says HISAT2, which also points to mixed processing.
  - No batch annotation exists to separate exercise from batch.
- **What answers the exercise question instead.** Each batch holds 5 WT and 5 DH, so two estimands cancel an additive batch shift:
  - the genotype x exercise interaction at 6M, which is the paper's own rescue test (S6.4.p11, 65 genes). This is the **primary** contrast;
  - the DH vs WT contrast within each batch.
- **Executions:**
  - `joint_all`: DESeq2 joint cell model on all 30 samples. It gives the interaction (primary) and DH vs WT within 6M-RA, 6M-EX and 3M.
  - `edger_geno_6M_RA`, `edger_geno_6M_EX`, `edger_geno_3M`: the paper-method edgeR QL, two arms per batch.
  - `joint_6M_noDH4`: sensitivity run without 6M-EX-DH4. This is the mouse that stopped exercising with heart failure; its Nppa and Myh7 are about 10x the others. The paper included it.
- **Enrichment:**
  - GSEA Hallmark on the interaction and on both 6M genotype contrasts;
  - ORA on the interaction.

## DEG counts vs paper (rule: padj < 0.05, no FC cutoff, the paper's q < 0.05)

| Contrast | Ours | Paper |
|---|---|---|
| Interaction geno x act, 6M (primary, DESeq2 joint, n=30) | 8 (3 up / 5 down) | 65 (19/46) |
| Interaction, sensitivity without DH4 | 52 (28/24) | 65 |
| DH vs WT, 6M RA, edgeR (paper method) | 337 (213/124) | 781 (614/167) |
| DH vs WT, 6M RA, DESeq2 joint | 64 (23/41) | 781 |
| DH vs WT, 6M EX, edgeR | 56 (25/31) | not given; 492/781 "rescued" |
| DH vs WT, 6M EX, DESeq2 joint (without DH4: 145) | 203 (118/85) | not given |
| DH vs WT, 3M, edgeR | 46 (39/7) | 56 (21/35); 57 in the abstract |
| DH vs WT, 3M, DESeq2 joint | 146 (107/39) | 56 |
| WT EX vs RA, DH EX vs RA | not run (aliased with batch) | 2529 / 2391 |

What the counts show:
- edgeR within a batch gives 337 DH vs WT DEGs at 6M RA but only 56 among exercised mice. This is consistent with the paper's rescue claim.
- The joint DESeq2 model shares dispersion across all three batches and the DH4 outlier, which deflates the 6M counts. Without DH4 the interaction gives 52 genes, close to the paper's 65.
- Gene checks:
  - Serinc2 at 3M is reproduced: log2FC 4.5, padj 0.014.
  - The WNT inhibitors (Sfrp1, Frzb, Apoe, Lrp1) are up in DH at 6M RA but not significant in the joint model.

## Enrichment (separate from DE)

- **DH vs WT, 6M RA:** inflammation, interferon, EMT, IL6/STAT3 and complement are up; OXPHOS, fatty-acid metabolism and adipogenesis are down. This matches S6.1.p5 and FIG1F.
- **Interaction:** IFN-gamma/alpha, inflammatory response, IL6/STAT3, EMT, angiogenesis and coagulation are negative (FDR < 0.05). Exercise removes the genotype-induced inflammatory and EMT signature, which matches the paper's rescue (FIG3E).
- **DH vs WT among exercised mice:** EMT is still up (rescue is partial, as the paper says for EMT). OXPHOS and fatty-acid metabolism are still down, so OXPHOS is not rescued here, while the paper's discussion claims that it is.

## Deviations

1. The simple exercise contrasts were refused at the design gate (batch aliasing), as described above. This is the main departure from the paper.
2. The interaction and joint contrasts used DESeq2 Wald instead of edgeR, because the runner's edgeR executor fits two arms only. The paper's q < 0.05 was applied unchanged (`paper_on_deviation_route`).
3. The gene universe differs from the paper's (~11.1-11.6k genes analysed). The edgeR runs test all non-zero genes (29,868); DESeq2 uses independent filtering.
4. No RUVr, because no comparison crosses time points.
5. Sex was not modelled (neither in GEO nor in the paper). It was inferred from Xist and Ddx3y and is balanced across genotype within each batch. Per-sex analyses are impossible: 1 female per EX arm.

## Tool problems

- **`tools/edger_tools.py:107`:** keeps every gene with any non-zero count and has no `filterByExpr`. The BH universe is about 30k genes instead of the paper's ~11k, which costs power against the paper's counts. It is also slow: about 5 min per 10-sample contrast, with tagwise dispersion at `:123`.
- **`tools/edger_tools.py:116`:** two-arm `~ Treatment` only. There is no edgeR route for interaction or multi-cell contrasts (also see the case-spec table, `references/case-spec.md:66`), so the paper's edgeR interaction could not be reproduced.
- **NaN rows:** inspect reports `missing_values` (487 NaN in the ERCC rows), but the runner has no option to drop them. A prep script was needed.
- **Suitability sex check:** `suitability.md` says "per-sex analysis: yes", but female cells have n=1 in the EX arms. The report did not write a `split_plan` into `suitability.json`.
