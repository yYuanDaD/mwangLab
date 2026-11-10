# HANDBACK: GSE97718 / PMC5647435 (exercise x high-fat diet, mouse quadriceps)

## What ran
- Case spec route (`case_spec.json`), `python -m tools.case_runner execute`. Run status completed. The validator returned 24 records and 0 errors.
- Design: 2x2 (CON/HFD diet x pre/post acute maximal exercise, 3 h). n = 4 independent mice per group, 16 samples, all aligned by name (`CONpre_1 (FPKM)` <-> title `CON-pre 1`, key `CON_pre_1`).
- Matrix: Cufflinks FPKM (`GSE97718_FPKM_cufflinks_all_samples.txt.gz`). The prep script `prep/fix_matrix.py` restored 25 gene names that Excel had turned into date serials (36951 -> Marchf1, ..., Septin1-14, 42248 -> Selenof/Sep15). It also summed the 262 gene names that appear on several Cufflinks loci, leaving 23,995 genes.
- Method: limma on log2(FPKM+1). One model `~ 0 + grp` on all 16 samples, 4 planned contrasts. Cuffdiff (the paper's method) is blocked because only FPKM was deposited, so this is a declared deviation.
- Threshold: the paper states none (S4.6.p1 only says "cufflinks"). Applied the workflow default, BH FDR < 0.05 with no fold-change cutoff; this matches Cuffdiff's default q < 0.05. Audit rule: raw p < 0.01.
- Sensitivity case `GSE97718_expressed`: the same model restricted to 10,356 genes with FPKM >= 1 in >= 4 samples (`prep/filter_expressed.py`). The filter was my choice, to approximate Cuffdiff testing only loci with enough reads.
- Enrichment (case GSE97718, both exercise contrasts): Enrichr ORA and Hallmark GSEA completed.

## DEG counts vs paper (BH FDR < 0.05; paper = Cuffdiff, rule not stated)
| Contrast | Paper | Ours (all genes) | Ours (expressed filter) | Audit p<0.01 (all) |
|---|---|---|---|---|
| CON-post vs CON-pre (primary) | 401 (292 up / 109 down) | 122 (102 / 20) | 132 (113 / 19) | 628 |
| HFD-post vs HFD-pre (primary) | 323 (208 / 115) | 36 (34 / 2) | 59 (52 / 7) | 548 |
| HFD-pre vs CON-pre (secondary) | 212 (119 / 93) | 33 (21 / 12) | 32 (22 / 10) | 420 |
| HFD-post vs CON-post (secondary) | 234 | 9 (9 / 0) | 17 (13 / 4) | 310 |

Direction agrees with the paper. Exercise gives more DEGs in CON than in HFD (blunted response under HFD), mostly up-regulated. Our FDR counts are 3-25x lower than Cuffdiff's. Expected reasons: limma on log FPKM with n = 4 is more conservative than Cuffdiff, and Cuffdiff's lenient per-locus calls are known to be liberal.

Named genes (CON exercise, all-genes case): Nr4a3 (log2FC 2.70, padj 3e-4), Ppargc1a (1.91, 5e-4), Klf5 (0.92, 0.012), Cited2 (1.00, 0.016) and Dusp10 (0.84, 0.020) are significant and up. Egr1 is up 1.30 but padj 0.098 (0.037 with the filter). Trp63 is up 0.58, padj 0.36. In HFD, Klf5 is not induced (0.25, padj 0.66) and Egr1 is weaker (padj 0.27). This matches the paper: Klf5/Egr1 induced "mainly in CON", Cited2/Dusp10 induced in CON. Nr4a3 and Ppargc1a are induced in both diets (consistent with S2.2.p3). HFD-pre: Pfkfb3 is down (-0.77) and Tbc1d1 up (0.39), the paper's directions, but neither reaches FDR significance.

Enrichment (separate from DE): CON exercise GO BP top terms are regulation of fatty acid oxidation and negative regulation of transcription by Pol II (the paper reports transcription and muscle differentiation). Hallmark GSEA top sets: TNFa/NF-kB, hypoxia, fatty acid metabolism up. HFD exercise has weaker ORA (fatty acid oxidation, glucose transport; the paper reports insulin response).

## Deviations
1. Cuffdiff -> limma on log2(FPKM+1) (paper route blocked: no reads or counts deposited).
2. Pairwise Cuffdiff runs -> one joint limma model on all 16 samples.
3. Gene-level matrix: multi-locus names summed; Excel-mangled names repaired.
4. Threshold is the workflow default because the paper states none.
5. The expressed-gene filter is a sensitivity analysis only, not from the paper.

## Tool problems
- `tools/case_runner.py` inspect (matrix profile around line 366) reports `duplicated_feature_ids: 492` but does not flag that feature IDs are Excel date serials (`feature_examples` shows `36951`, `37135`). I had to spot the mangling by hand. A numeric-ID or date-serial warning would help.
- `filter_low_counts` is raw-counts-only, so an FPKM expression filter needed a separate prep matrix and a second case (`case_spec.md` section 3).
- Cosmetic: inspect output shows the GEO `contact_name` mojibake (`Joaqu铆n`), which suggests a metadata CSV was decoded with GBK somewhere upstream.
