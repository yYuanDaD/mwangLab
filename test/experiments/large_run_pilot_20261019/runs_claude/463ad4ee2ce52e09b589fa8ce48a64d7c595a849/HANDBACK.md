# HANDBACK: GSE207992 / PMC9971895 (paper_id 463ad4ee2ce52e09b589fa8ce48a64d7c595a849)

Paper: Timed exercise stabilizes behavioral rhythms but not molecular programs in the brain's suprachiasmatic clock (iScience 2023, PMID 36866044).
Status: finished. Route: paper_aligned (case spec route, `tools.case_runner execute`, validator 0 errors).

## What ran
- Data: GEO deposits only `GSE207992_DESeq2_normcounts.csv` (DESeq2-normalized counts, 55401 genes x 14 SCN samples). Exact integer raw counts were recovered by dividing each sample by its smallest non-zero value (all entries integer within 1e-8; size factors 0.65-1.45): `prep_recover_raw_counts.py` -> `GSE207992_raw_counts_recovered.csv` (Ensembl IDs without version) + `GSE207992_gene_symbols.csv`.
- Alignment: matrix columns renamed to AH labels = GEO `description`; exact match 14/14. grp = genotype (WT / KO = Vipr2-/-) x exercise (nSVE / SVE): WT_nSVE 4, WT_SVE 4, KO_nSVE 3, KO_SVE 3 (= paper S4.4.2.p1).
- Suitability: analyzable; all male (sex check passed); no batch/subject covariates.
- Primary route: one DESeq2 (pydeseq2 Wald) model `~ grp` on all 14 samples, the paper's 4 planned contrasts (`joint`), plus WT SVE vs KO SVE (`joint_extra`, exploratory, no paper count).
- Sensitivity: separate two-group DESeq2 fit per pair (`pairwise_*`) - my first attempt; it reproduced the paper worse, so the joint model became primary (skill rule: one model for one multi-level design).
- Enrichment: KEGG/GO ORA (up, down) and Hallmark GSEA on KO SVE vs KO nSVE; Hallmark GSEA on WT SVE vs WT nSVE. All completed.

## DEG counts vs paper (paper threshold: FDR (BH) < 0.05, no fold-change rule; S2.2.p2, S4.4.2.p2)
| Contrast | Role | Joint model (primary) up/down | Pairwise fit (sensitivity) | Paper up/down |
|---|---|---|---|---|
| KO SVE vs KO nSVE (exercise, both CT14) | primary | 329 (190/139) | 33 | 223 (105/118) |
| WT SVE vs WT nSVE (exercise + 8h phase shift) | secondary | 772 (542/230) | 2047 | 795 (556/239) |
| KO nSVE vs WT nSVE (genotype) | secondary | 457 (187/270) | 326 | 307 (158/149) |
| KO SVE vs WT nSVE | secondary | 557 (242/315) | 594 | 557 (246/311) |
| WT SVE vs KO SVE | exploratory | 532 (285/247) | - | not reported |

Gene-level agreement (joint model): KO exercise - Kdr, Banp, Syk, Naif1, Kctd18, Gm1848, Ncor1 up; Cox16, Ndufa4 down; Per2/Arntl/Nr1d1/Cry1 not DE - all as in the paper (S2.5.p1, S2.7.p2). WT exercise - Nr1d1, Rgs16, Miat, Serpine1, Syngap1 up; Cry1, Per2, Slc2a13 down - as in S2.4.p1. Genotype contrasts reproduce Gpc3/Penk/Tmem254b,c up and Kdr/Ncor1/C1ql3/Vip/Avp/Creb3l1/Kcnc2/Mobp down (S2.3.p1), and the S2.6.p1 genes for KO SVE vs WT nSVE.

## Deviations and caveats
- Counts recovered from the deposited normalized matrix (exact), not re-quantified; GEO says GRCm39/vM27, paper says GRCm38.
- pydeseq2 instead of R DESeq2 (Bioconductor 3.14).
- The paper does not say whether its pairwise comparisons came from one model or per-pair fits. The joint model matches 2/4 counts closely (557 = 557; 772 vs 795), but the two contrasts involving KO nSVE are ~1.5x the paper's (329 vs 223; 457 vs 307). Per-pair fits are far off for the exercise contrasts (33, 2047). The gap is not resolved.
- WT SVE vs WT nSVE is confounded by design with circadian time (ZT14/CT22 vs CT14; paper S2.4.p1): not a pure exercise effect. Only the KO comparison is an exercise estimand matched for circadian time.
- Pathway direction conflict (recorded in study caveats): for KO exercise our KEGG ORA puts Parkinson/Huntington disease/OXPHOS in the down genes and GSEA gives OXPHOS NES -2.4, while paper S2.5.p1 says Parkinson disease is up and mTOR is down. Paper S1.p4 says neurodegeneration pathways are *down* with exercise in the KO SCN, and its named down genes (Cox16, Ndufa4) are OXPHOS genes, so the paper contradicts itself; our result agrees with S1.p4.
- Paper gives the WT SVE sampling phase as CT22 (S2.2.p1, S4.4.p4) and as CT24 (S4.4.2.p1).

## Tool problems
- `tools/case_runner.py:429-443` (`_gene_lookup`): an Ensembl-indexed table is mapped to symbols through MyGene current symbols only, so renamed or retired symbols (Arntl -> Bmal1, Ndufa4, Tmem254b, Tmem254c) come back null even though the deposited GENCODE annotation has them. I checked them by hand from `GSE207992_gene_symbols.csv`: Ndufa4 log2FC -0.93 padj < 1e-4 in KO exercise; Arntl n.s. in every contrast; Tmem254b/c +2.3 padj < 1e-4 in KO vs WT nSVE. A spec-level symbol map (or keeping the matrix's own symbol column) would fix this.
- `inspect` classifies the DESeq2-normalized file only as "linear_normalized or estimated_counts"; it does not detect that integer counts can be recovered exactly by per-sample rescaling (a cheap check: values / min non-zero all integer). I did this in a prep script.
- Prok2 padj is NA in several joint contrasts (Cook's outlier filtering); this matches the paper's note that Prok2 was highly variable (S2.8.p1). Not a bug.
- Each `execute` takes ~6-7 min; runs moved to the background past 180 s (no failures).
