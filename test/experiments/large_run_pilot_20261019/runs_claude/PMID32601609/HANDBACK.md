# HANDBACK: PMID32601609 / GSE77178

STATUS: finished (route `declared_deviation`, decision `valid`, execution `completed`, validator 13 records / 0 errors)

## What ran
- Case spec route: `python -m tools.case_runner inspect GSE77178`, then `execute case_spec.json`. I ran it twice; the second run only added study caveats. The first attempt is in `_previous/20261117T162509Z`.
- Paper: PMC7323974. Exercise experiment: quiescent MuSCs from Y(-Ex)/Y(+Ex)/O(-Ex)/O(+Ex) mice (S0.p7, FIG11). Method in the paper: RUVs k=6 normalization, then edgeR NB GLM LRT on genes with normalized FPKM >= 6 in >= 3 samples, BH q-values (S1.19.p3). Threshold: 10% FDR with no fold-change cutoff (S0.p7).
- Ownership: the GEO file is the paper's processed table. It has exactly 11,337 genes, matching S1.19.p3, and comes from the Rando lab.
- Alignment: I derived a key from the GEO title (`O(-Ex) replicate 1` -> `O(-Ex)_1`), giving an exact match for 36/36 samples. I excluded the 15 samples from the Ccnd1 genotype series (2018 submission, a separate experiment in S0.p15). The kept samples form grp = OSed 7, OEx 5, YSed 6, YEx 3.
- Matrix: RUVs-normalized FPKM (GEO data_processing). No raw counts were deposited.
- Model: one limma cell-means model `~ 0 + grp` on log2(FPKM+1), fitted on 21 samples. Expression filter: FPKM >= 6 in >= 3 samples, which kept 6,481 of 11,332 genes. Hallmark preranked GSEA ranked by limma t for all three contrasts.

## DEG counts vs paper (paper threshold: BH FDR < 0.10, no FC cutoff)
| Contrast | Ours (padj<0.10) | up/down | audit padj<0.05 | Paper |
|---|---|---|---|---|
| O(+Ex) vs O(-Ex) (primary) | 1064 | 526/538 | 652 | 248 |
| Y(+Ex) vs Y(-Ex) | 442 | 146/296 | 146 | 35 |
| O(-Ex) vs Y(-Ex) (aging reference) | 3521 | 2021/1500 | 2997 | not reported (130 of the 248 called "rejuvenated") |

- Named gene: Ccnd1 is rank 1 in O(+Ex) vs O(-Ex) (log2FC +1.14, padj 3.4e-5), as in the paper (S0.p9, FIG11 c). It is lower in O(-Ex) than in Y(-Ex) (log2FC -0.49, padj 0.0016), matching "decreased during aging and restored by exercise".
- GSEA, where it agrees with the paper:
  - Exercise in old MuSCs lowers TNFA/NF-kB (NES -2.28), IL6, TGF-beta and IL2, and raises myogenesis and angiogenesis (the last two not significant).
  - Aging raises IFN alpha/gamma, inflammatory response and ROS, and lowers myogenesis (NES -2.20) and Notch.
- GSEA, where it contradicts the paper (recorded in study caveats):
  - Cell-cycle sets. In O(+Ex) vs O(-Ex), E2F has NES -0.96 (not significant) and G2M has NES -1.61 (q 0.04); the paper says exercise restores them. In O(-Ex) vs Y(-Ex), E2F has NES +1.28 (not significant); the paper says aging lowers them.
  - IFN gamma is borderline lower with exercise in old MuSCs (q 0.075), while the paper says it is not suppressed.

## Deviations
1. The paper's route (edgeR LRT on RUVs-normalized counts) is blocked because raw counts and the RUVs W factors are not deposited. I used limma on log2(normalized FPKM + 1) instead.
2. The RUVs factors are already removed from the deposited values, but their 6 degrees of freedom are not taken out of the residual df. This, together with limma-on-log-FPKM versus a count NB LRT, likely explains our 4-12x larger DEG counts. Do not read the counts as a reproduction; the ranking (Ccnd1 first) is the agreeing evidence.
3. I applied the expression filter (FPKM >= 6 in >= 3 samples) within the 21 exercise samples. The paper does not say which sample set it used.
4. Five gene symbols are duplicated (same Entrez ID, different Ensembl locus); I kept the first of each, giving 11,332 genes.
5. GSEA ranks by limma t (preranked). The paper used Signal2Noise with gene permutation. Hedgehog was not tested because it fell below the gene-set size limit after the filter.

## Tool problems
- None blocked the run.
- Cosmetic: after `add_reversed_planned` (tools/suitability.py:241-257) adds the planned reversed names, the suitability report (`GSE77178/suitability/suitability.md`) lists the same pair in both directions (`grp_YSed_vs_OSed` and `grp_OSed_vs_YSed`, `grp_YSed_vs_YEx` and `grp_YEx_vs_YSed`). The comparison count becomes 8 instead of 6 unique pairs.
- Missing capability: the runner cannot take out residual df for factors that were removed before deposit (RUV/SVA-normalized matrices). Small DEG counts like these cannot be calibrated against the paper.
