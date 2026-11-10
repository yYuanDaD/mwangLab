# HANDBACK: PMID34039988 / GSE132520

## What ran
- Case spec route (`case_spec.json`), executed twice. The first attempt's primary execution failed on comparison names and was moved to `_previous/`. The second run completed, and the contract validator reported 15 records with 0 errors.
- Data: `GSE132520_FPKM_Matrice_SkelMuscle.csv`, 18,873 genes x 16 samples. Samples were aligned exactly on the GEO `title` (16/16).
- Design: 2x2 genotype (MM = WT, VV = CaMKIIgamma M281V/M282V) x treatment (sedentary, one bout of submaximal treadmill exercise with collection 3 h later), n = 4 per cell. The four cells form one factor, `grp`.
- Method: limma-trend on log2(FPKM+1), one model `~ 0 + grp` on all 16 samples. Genes were kept if FPKM >= 1 in >= 4 samples (10,879 kept). A sensitivity run with no filter was also done.
- Enrichment: ORA (GO/KEGG) and GSEA (Hallmark) on both exercise contrasts; all completed.

## DEG counts vs paper (paper threshold: FDR q < 0.05, no fold-change cutoff; S2.3.p1, FIG3c)

| Contrast | Ours (filtered) up/down | Ours (no filter) | Paper |
|---|---|---|---|
| MM exercised vs sedentary (planned) | 137 (118/19) | 106 | 582 |
| VV exercised vs sedentary (planned) | 31 (28/3) | 16 | 216 |
| Shared between MM and VV | 29 of 31 VV DEGs (94%) | | 180 of 216 (83%) |
| VV vs MM, exercised (exploratory) | 0 | | not counted (the paper used a 2-sigma list for IPA) |
| VV vs MM, sedentary (exploratory) | 0 | | not counted (the paper reports similar PCA) |

Qualitatively the paper's main finding is reproduced:
- The exercise response is much larger in MM than in VV.
- Nearly all VV DEGs are also MM DEGs.
- The top MM genes are classic acute-exercise genes: Atf3, Nr4a3, Xirp1, Srxn1, Csrp3.
- Hallmark GSEA top terms are inflammatory in both genotypes (TNFA_SIGNALING_VIA_NFKB, IL6_JAK_STAT3, hypoxia), matching the inflammation emphasis of the paper's IPA (FIG3f).

Absolute counts are about 4x (MM) and 7x (VV) lower than the paper's.

## Deviations
- **Paper route blocked.** The paper used Cuffdiff v2.2.1 on reads (from the GEO data_processing field), but only FPKM was deposited. limma-trend on log2(FPKM+1) ran instead as a declared deviation, with threshold source `paper_on_deviation_route`. Cuffdiff is typically more liberal than limma at n = 4, which likely explains much of the count gap.
- **One joint model.** We fit one 4-cell model; Cuffdiff ran a separate comparison per genotype.
- **Low-expression filter.** The FPKM >= 1 in >= 4 samples rule is our choice; the paper states no filter. It stands in for Cuffdiff not testing low-expression genes. Without it the counts are 106 and 16.
- **Exploratory genotype contrasts.** These are named VV-vs-MM, so their sign is the reverse of the paper's "MM vs VV".
- **Not reproduced.** The IPA analysis and its 2-sigma gene lists were not reproduced.
- **Litter not modelled.** The title prefix, which may be a litter ID, appears only in the confounding report: the paper does not block on it and it is spread unevenly across cells.

## Tool problems
- `tools/case_runner.py:823`: joint-limma `comparisons` accept only the orientation enumerated by suitability (level order). `grp_MMEX_vs_VVEX` was rejected even though the reverse exists. `tools/suitability.py:244` already maps reversed names for `planned`, but the execution `comparisons` check does not use that mapping.
- In the failed first attempt the case finish still read `status: completed` / `execution_status: completed` while the primary execution held a NativeToolError and its counts were null. The run-level status overstates success when the primary execution fails.
- Minor: the FPKM matrix has 32 NaN cells in 8 rows, including a row literally named `gene` that looks like a stray header. The runner handled it, but the spec gives no explicit record of how it was handled.
