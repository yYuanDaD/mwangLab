# GSE232510 / PMID39000297 — why HFS vs CS gave 2 DEGs, not 430

Date: 2026-10-29. This was read-only analysis: no tool, decision file or result in the run was changed. Supporting scripts and tables are in `investigation/` (the R scripts use DESeq2 1.51.7 under R 4.6.0; the Python scripts use `.venv-pdf`). The Rnor6 gene annotation came from the Ensembl 104 GTF (only the gene ID, name and chromosome lines were kept).

## Bottom line

**Two of the 10 deposited libraries are not in the paper's analysis, and one of them sits in the control group.** The paper's Table S1 gives a value for each animal for all 431 DEGs. Matching those values to the GEO counts identifies 8 of the 10 GEO samples exactly (log-ratio r = 0.97–1.00). The other two, **GSM7349355 "CS_Rep4"** and **GSM7349358 "HFS_Rep2"**, match none of the 14 paper animals. CS_Rep4 has a strong HFS-like profile, driven mostly by a ventral-dissection signature. Inside the CS group it inflates the CS variance and pulls the CS mean toward HFS. That cuts HFS vs CS from about 430 genes to 2.

The run's analysis was correct for the samples and labels as deposited. Reproduction failed because the deposit does not contain the paper's sample set. Neither the threshold nor DESeq2 settings explain it: our log2FC on the paper's 431 genes has r = 0.91 and 99.3% sign agreement with the authors' values, but about half the magnitude.

## 1. Our DEG tables under different rules

Counts are total (up/down), with the effect in the HFS direction (HFS/CS).

| fit | padj<0.1 & \|lfc\|>0.5 | padj<0.1 | p<0.05 | p<0.05 & \|lfc\|>0.5 | p<0.01 |
|---|---|---|---|---|---|
| run, pydeseq2 joint ~grp (10), HFS vs CS | 2 (2/0) | 2 (2/0) | 605 (306/299) | 465 (223/242) | 134 |
| run, pydeseq2 joint, HFR vs CS | 15 (5/10) | 15 (5/10) | 609 (277/332) | 445 (149/296) | 144 |
| R DESeq2 joint (10), HFS vs CS | 2 | 2 | 628 | 487 | 139 |
| R DESeq2 joint (10), HFR vs CS | 17 | 17 | 625 | 462 | 151 |

- The p<0.05 rules give roughly 450–630 DEGs. That number is close to 430, but only by coincidence: raw-p counts with ~19k tested genes carry about 970 expected false positives at p<0.05 and are not what the paper reports. The paper's own table has padj ≤ 0.1001 for all 431 rows.
- **The paper's real rule is FDR<0.1 alone.** In Table S1, 430 of 431 rows have padj<0.1, |log2FC| goes as low as 0.29, and only 352 rows have |lfc|>0.5. The "log2FC>0.5" in the Figure 2 legend and the "Fold>2" in the table header were not applied to the count. Our run used the legend rule, which made no difference here (2 vs 2) but should be FDR-only for this paper.

## 2. Two-group refits (HFS + CS only, and HFR + CS only)

| fit | padj<0.1 & \|lfc\|>0.5 | padj<0.1 | p<0.05 | p<0.05 & \|lfc\|>0.5 | p<0.01 |
|---|---|---|---|---|---|
| run audit, pydeseq2 HFS vs CS (3v3) | 17 (2/15) | 17 | 549 | 458 | 149 |
| R DESeq2 HFS vs CS (3v3) | 16 (2/14) | 16 | 562 | 471 | 150 |
| run audit, pydeseq2 HFR vs CS (3v4) | 15 (3/12) | 15 | 485 | 367 | 111 |
| R DESeq2 HFR vs CS (3v4) | 19 (4/15) | 19 | 503 | 384 | 113 |

The two-group fit changes little (2 → 16–17). Model choice is not the cause.

**Controls on the CS group (R DESeq2, HFS vs CS, padj<0.1):**

| change | DEGs |
|---|---|
| CS_Rep1 relabelled HFS (2v4) | 6 |
| **CS_Rep4 relabelled HFS (2v4)** | **427** (347 up / 80 down) |
| CS_Rep5 relabelled HFS (2v4) | 0 |
| drop CS_Rep1 (2v3) | 14 |
| **drop CS_Rep4 (2v3)** | **283** |
| drop CS_Rep5 (2v3) | 12 |
| **paper-matched animals only: CS1, CS12 vs HFS2, HFS9 (2v2)** | **171** |
| HFR vs CS without CS_Rep4 (2v4, the same set as paper-matched) | 27 |
| joint ~grp without CS_Rep4 (9 samples), HFR vs CS | 37 |
| joint, paper-matched 8 samples, HFR vs CS | 33 |

Only CS_Rep4 has this effect. The HFR vs CS number (paper: 39) falls in the 27–37 range once CS_Rep4 is removed, against 15–19 with it.

## 3. What the paper says (PMC11241292)

- **Software and counts:** STAR to Rnor6, samtools rmdup, then `htseq-count -s no --mode union`. The "read count matrix was assembled from all the tested RW groups" and analysed with pairwise DESeq2 (S5.6.3.p2). No DESeq2 version, formula, prefiltering or shrinkage is reported.
- **Threshold:** the text says FDR<0.1 (S2.2.p2); the Figure 2A legend says "FDR < 0.1; log2FC > 0.5". Table S1 shows the count used FDR<0.1 only (see §1).
- **Sample sizes:** n = 3 CS, 3 CR, 4 HFS, 4 HFR (S5.6.2.p1, Figure 2 legend). Table S1 columns: CS1, CS16, CS12 / CR1, CR4, CR5 / HFR4, HFR7, HFR11, HFR15 / HFS2, "HFS", HFS17, HFS9.
- **Two cohorts:** "The experiment was conducted twice" with n = 6 per group per experiment (S5.2.p1). Which cohort each sequenced animal came from is not reported anywhere, including GEO.
- **PCA (Figure S1):** PC1 is 43% of variance. All 3 CS sit at PC1 −10 to −0.5 and all 4 HFS at +3 to +10. One HFR is an outlier on PC2 and was kept. No CS animal sits on the HFS side.
- **Counts:** 430 in the methods; Table S1 has 431 rows; "432 DEGs" appears in S2.3.p2. The split "265 down / 165 up in CS vs HFS" is CS relative to HFS: Table S1's log2FoldChange is CS/HFS (sign agreement with mean(HFS)/mean(CS) per animal = 0%). In the HFS direction that is **265 up / 166 down**.
- **Named DE genes, our values (HFS/CS log2FC, padj):**

| gene | paper (Table S1) | run joint10 | R 3v3 | R CS_Rep4→HFS | R paper-matched 2v2 |
|---|---|---|---|---|---|
| Rtl5 (cl.1, down) | −1.42, 0.057 | −0.55, 0.99 | −0.55, 1.0 | −0.92, 0.50 | −1.40, 0.64 |
| Cck (cl.2, down) | −0.97, 0.021 | −1.10, 0.85 | −1.09, 0.35 | −1.25, 0.0017 | −1.18, 0.074 |
| Cxcl12 (cl.2, down) | −0.63, 0.057 | −0.43, 0.99 | −0.42, 1.0 | −0.35, 0.63 | −0.52, 0.87 |
| Btg2 (cl.3, up) | 1.04, 0.005 | 0.73, 0.99 | 0.73, 1.0 | 1.04, 0.022 | 1.13, 0.26 |
| Rras (cl.3, up) | 0.87, 0.003 | 0.36, 0.99 | 0.37, 1.0 | 0.79, 0.007 | 0.76, 0.28 |
| Cd44 (cl.4, up) | 1.38, 0.035 | 0.87, 0.99 | 0.87, 1.0 | 1.06, 0.22 | 1.29, 0.53 |
| Cd74 (cl.4, up) | 2.29, 0.037 | 0.92, 0.99 | 0.93, 1.0 | 2.13, 1.5e-18 | 2.15, 2.3e-09 |
| Mt2A (cl.4, up) | 1.71, 0.078 | 0.94, 0.99 | 0.94, 0.92 | 1.48, 4e-06 | 1.62, 6e-04 |
| Cxcl16 (cl.4, up) | 1.48, 0.061 | 0.63, 0.99 | 0.63, 1.0 | 1.12, 0.008 | 1.30, 0.046 |
| Hspb1 (cl.4, up) | 2.03, 3e-06 | 1.14, 0.99 | 1.14, 1.0 | 1.91, 0.064 | 2.22, 0.22 |
| Pomc (cl.4, up) | 2.08, 0.058 | 0.95, 0.99 | 0.95, 1.0 | 1.58, 0.012 | 1.71, 0.33 |
| Gad2 | −1.06, 6e-05 | −0.36, 0.99 | −0.35, 1.0 | −0.87, 0.014 | −0.81, 0.083 |
| Aldh1a1 | 1.31, 6e-05 | 0.69, 0.99 | 0.70, 1.0 | 1.00, 0.003 | 1.24, 0.002 |
| Hmox1 | 1.04, 0.035 | 0.45, 0.99 | 0.45, 1.0 | 0.55, 0.54 | 0.76, 0.77 |
| Timp1 | 1.47, 0.013 | 0.88, 0.99 | 0.88, 1.0 | 1.33, 8e-04 | 1.43, 0.041 |

All 15 named genes go in the paper's direction in every fit. In the run, their effect sizes are about half the paper's and none passes FDR. With the paper-matched animals, the effect sizes match the paper (for example Cd74 2.15 vs 2.29, Rtl5 −1.40 vs −1.42).

## 4. Data sanity

- **Counts:** all values are non-negative integers (max 178,106), with 32,883 Rnor6 Ensembl genes after removing the 5 HTSeq `__` rows. These are raw htseq counts.
- **Library sizes (assigned reads):**

| sample | assigned reads |
|---|---|
| CS_Rep1 | 5.15M |
| CS_Rep4 | 5.63M |
| CS_Rep5 | 4.68M |
| HFS_Rep1 | 5.77M |
| HFS_Rep2 | 6.37M |
| HFS_Rep4 | 6.32M |
| HFR_Rep1 | 5.03M |
| HFR_Rep2 | 5.37M |
| HFR_Rep3 | 4.75M |
| HFR_Rep4 | 7.49M |

  Assigned fraction is 51–58%, multimapped about 17–21%, MT 0.9–8.2%. No sample is a QC failure.
- **PCA** (vst, top 500 genes): PC1 is 40.5% of variance. Samples split into cluster B = {CS_Rep4, HFS_Rep1, HFS_Rep2, HFS_Rep4, HFR_Rep4} (PC1 +5.7 to +10.4) and cluster A = {CS_Rep1, CS_Rep5, HFR_Rep1, HFR_Rep2, HFR_Rep3} (−4.8 to −11.2). HFR_Rep3 is the PC2 outlier, which is the paper's outlying HFR (= HFR11). CS_Rep4's nearest neighbour is HFS_Rep1 (r = 0.970); its correlation with the other two CS samples is 0.915 and 0.869. PC1 correlates with library size at r = 0.70.
- **What PC1 is:** the genes that load positively are pars tuberalis/pituitary (Cga, Tshb, Pitx1), leptomeninges/fibroblasts (Ptgds, Col1a1, Col3a1, Mgp, Igfbp2, Slc22a6, Aldh1a2), choroid plexus (Ttr), and MHC-II (Cd74, RT1-Ba). The genes that load negatively are dorsal/lateral hypothalamic neurons (Hcrt, Hdc, Sst, Gad2, Cck, Pvalb). So PC1 mainly tracks how much ventral surface tissue (median eminence/pars tuberalis/meninges) each punch contained.

| normalized counts | CS_Rep1 | CS_Rep4 | CS_Rep5 | HFS 1/2/4 | HFR 1/2/3/4 |
|---|---|---|---|---|---|
| Cga | 1688 | **6859** | 64 | 3827/5173/5349 | 34/30/500/2084 |
| Tshb | 254 | **553** | 4 | 482/1047/643 | 1/2/9/284 |
| Ptgds | 11k | **95k** | 17k | 59k/55k/68k | 6k/11k/5k/65k |

  The 427 DEGs from "CS_Rep4 as HFS" agree in sign with cluster B minus cluster A for 99.8% of genes. **Caveat:** the paper's HFS signature itself is therefore heavily mixed up with dissection depth. All 4 of the paper's HFS animals are on the B side of its PCA, and none of its CS animals is.
- **Sex:** all Rnor6 chrY protein-coding genes (Sry, Kdm5d, Eif2s3y, Ddx3-Y, Usp9y, Uba1y, …) have 0 counts in all 10 samples. That fits all-female animals, but it is weak evidence: Rnor6 has no Xist annotation, and multi-mapped X/Y reads are dropped by htseq. GEO labels all samples female.
- **GEO labels vs paper:** the file names CS_Rep1/4/5 and HFS_Rep1/2/4 do not match the GEO titles ("rep 1–3"). GEO has CS 3, HFS 3, HFR 4, CR 0. The paper has CS 3, CR 3, HFS 4, HFR 4.

**Sample identity**, from correlating each GEO sample with the per-animal values in Table S1. Two tests: centred-log correlation, and a log-ratio test anchored on the matched pairs CS_Rep1 = CS1 and HFR_Rep2 = HFR7. Values are centred / log-ratio r.

| GEO | paper animal | r |
|---|---|---|
| CS_Rep1 GSM7349354 | CS1 | 0.96 / 1.00 |
| CS_Rep5 GSM7349356 | CS12 | 0.89 / 1.00 |
| HFS_Rep1 GSM7349357 | HFS2 | 0.98 / 1.00 |
| HFS_Rep4 GSM7349359 | HFS9 | 0.97 / 1.00 |
| HFR_Rep1–4 | HFR4, HFR7, HFR11, HFR15 | 0.90–0.95 / 0.97–1.00 |
| **CS_Rep4 GSM7349355** | **none**; best are HFS17/HFS2 (HFS-like, not identical); with CS16 r = −0.56 / −0.33 | 0.72 / 0.91 |
| **HFS_Rep2 GSM7349358** | **none** | 0.40 / 0.84 |

These paper animals have no GEO library: CS16, HFS17, "HFS", CR1, CR4, CR5.

## 5. Author DE table

- **GEO** has only `GSE232510_RAW.tar` (per-sample htseq counts). There is no processed DE table.
- **Paper supplement** (`ijms-25-07188-s001.zip`, from Europe PMC): Table S1 is the authors' DESeq2 output for HFS vs CS. It has 431 genes with baseMean, log2FoldChange (CS/HFS), lfcSE, stat, p, padj, and per-animal values. Table S3 is the miR-211 DE table; there is no HFR vs CS or CR vs CS table. Figure S1 is the PCA. A parsed copy is in `investigation/paperS1_table.csv`, and the Figure S1 image is `investigation/figS1.png`.
- **log2FC agreement on the paper's 431 genes** (our HFS/CS against −paper):

| fit | Pearson r | sign agreement | median \|lfc\| (paper 0.82) | paper genes recovered at our padj<0.1 |
|---|---|---|---|---|
| run, pydeseq2 joint10 | 0.907 | 99.3% | 0.41 | 2 |
| R 3v3 (GEO labels) | 0.907 | 99.1% | 0.42 | 2 |
| R without CS_Rep4 (2v3) | 0.966 | 100% | 0.71 | 115 |
| R CS_Rep4 → HFS (2v4) | 0.966 | 100% | 0.73 | 171 |
| **R paper-matched animals (2v2)** | **0.975** | **100%** | **0.81** | 78 |

The direction is reproduced everywhere. In the run, the magnitude is halved. Using only the paper's own animals restores the magnitude. At 2v2 there is not enough power to recover all 430 genes, since the paper had 3v4.

## Still unknown

1. **What CS_Rep4 really is.** It could be an HFS animal deposited under the wrong label (it is HFS-like, but it is not HFS17 or "HFS"), or a genuine CS animal with a deep ventral punch that the authors left out of their analysis. Either way the paper did not analyse it, and the paper's CS16 was not deposited.
2. **What HFS_Rep2 is.** It matches no paper animal and has a weaker HFS signature (score 0.54 against 0.59–0.91 for the other HFS).
3. **Whether the paper's 430 genes are diet biology or dissection.** The paper's HFS-vs-CS genes overlap strongly with the ventral-dissection axis (Cga, Tshb, Ptgds, Cd74 …). In our data that axis is present to some degree in all 4 HFS-like libraries, in HFR15 and in CS_Rep4, so diet and dissection cannot be separated with these samples.
4. **The two-cohort structure and the paper's model.** The paper's exact model (joint 14-sample vs pairwise) is unknown and cannot be rebuilt without CR, CS16, HFS17 and "HFS". The SRA run-info lookup for sequencing pools also returned nothing.

**Recommendation for the run record:** add a `paper_data_discrepancies` item saying that GSM7349355 (CS_Rep4) and GSM7349358 (HFS_Rep2) are not among the paper's analysed animals, as shown by the Table S1 match. Exclude them for the paper-route reproduction, using CS_Rep1/CS_Rep5 vs HFS_Rep1/HFS_Rep4, and HFR_Rep1–4 vs CS_Rep1/CS_Rep5. Also set the threshold to FDR<0.1 only.
