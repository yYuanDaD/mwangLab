# HANDBACK: PMID 39523700 (PMC11874633)

Paper: *Actuating Extracellular Matrices Decouple the Mechanical and Biochemical Effects of Muscle Contraction on Motor Neurons.*
Decision maker: Claude Opus 5.5 (Claude Code session), bioinformatics-workflow skill, case-spec route. I skipped the preflight because the request said to.
Spec: `case_spec.json`. Runner output: `summary.csv`, `run_status.json`, per-case folders. Validator: 30 records, 0 errors.

## What ran

| Case | Outcome | Route |
|---|---|---|
| GSE257540_biochem | completed | paper_aligned. One DESeq2 model `~ grp` on Control (C, n=5), spontaneous-twitch CM (SP, n=5) and exercised-muscle CM (EX, n=4). Three planned contrasts (FIG7c-e). |
| GSE257540_mech | completed | paper_aligned. DESeq2 `~ grp` on MagMA-actuated (MS, n=4) vs non-actuated control (MC, n=3) (FIG7i). |
| GSE281241 | refused at `design` | Unstimulated ChR2::tdTomato C2C12 vs WT C2C12 myotubes. This is a genotype or cell-line characterization with no exercise or contraction arm. The paper does not cite this series: it cites only GSE257540 (S4.8.p2, DA.p1). The link comes only from GEO (Series_pubmed_id, SuperSeries GSE281242). |

How the decisions were made:
- **Group identity.** GEO's "Low intensity biochem" is the NE samples: medium from unstimulated, spontaneously twitching muscle. "High intensity biochem" is the S samples: medium from optically stimulated (exercised) muscle. Both come from the GSE257540 Series_overall_design.
- **Alignment.** Matrix columns L1 and H1 correspond to titles LI1 and HI1. I matched them by deriving a key with `key_patterns` and setting `normalize_keys`. The match is exact; nothing was aligned by position.
- **Matrix.** The counts are nf-core STAR/Salmon gene counts that the submitter deposited already rounded to integers. They went into DESeq2 unchanged, which is the paper's input. The TPM file was not used.
- **QC exclusions (S4.10.p1 criteria, computed from the deposited counts):**
  - C4: rRNA fraction 0.78.
  - LI6: 1,536 reads.
  - HI4: 243K reads.
  - HI5: 495K reads, just under the 500K cutoff.
  - MC3: 613K reads with the most detected genes of any sample, which fits the low exon/intron criterion.

  That makes 5 exclusions, matching the paper's "n = 5".
- **Threshold.** The paper says only that DEGs used BH-adjusted p-values and gives no cutoff and no fold-change rule. I applied `workflow_default` (padj < 0.05, no LFC rule) and labelled it as such. As an audit I also counted genes at nominal p < 0.05.

## DEG counts vs the paper (padj < 0.05, BH, no fold-change rule)

| Table | Ours (up/down) | Paper |
|---|---|---|
| EX vs C (exercise CM vs control) | 106 (70/36) | not reported per contrast |
| SP vs C (spontaneous CM vs control) | 128 (94/34) | not reported per contrast |
| EX vs SP | 14 (5/9) | not reported per contrast |
| **Union of the 3 biochemical contrasts** | **214** | **194** (FIG7b, S2.4.p3) |
| MS vs MC (mechanical) | **0** (nominal p < 0.05: 413) | **2**, both up, "RNA degradation markers", not named (S2.4.p4) |

Named genes:
- **EX vs C.** All 16 genes the paper names are significant and up in ours: Ntn1, Iqgap1, Wls, Lamb1, Itgb1, Sema3b, Sema3d, Cdh1, Lamc1, Serpinh1, Nid1, Nid2, Bgn, Col18a1, Aebp1, Loxl1. padj ranges from 0.0005 to 0.044 and LFC from +0.63 to +3.16.
- **SP vs C.** All 6 shared genes are significant and up: Ntn1, Iqgap1, Wls, Lamb1, Itgb1, Serpinh1.
- **Directions.** No gene contradicts the paper's direction.

Mechanical: our top nominal hits are Adnp and Jun (padj about 1). The paper's two hits are unnamed, so I can't check them.

Enrichment (GSEA, gseapy prerank, MSigDB Hallmark): this is not the paper's c2-c6 v7.0 collections, so it is not directly comparable to its figures.
- EX vs C: EMT, G2M, E2F and coagulation are enriched upward. This agrees with the paper's ECM/projection themes, but only loosely.
- MS vs MC: the Hallmark results include positive NES for hypoxia, hedgehog and TNFa, and negative NES for OXPHOS and MYC. The paper's neuron-projection and axon-development GO sets were not tested.
- EX vs C ORA (Enrichr GO and KEGG) also completed.

Enrichment results are kept separate from the DE results.

## Deviations

1. **No ashr or normal-prior LFC shrinkage, and pydeseq2 instead of R DESeq2 4.2.0.** Shrinkage changes LFC estimates only, not the Wald padj used for DEG calls. Implementation differences between pydeseq2 and R DESeq2 (dispersion fitting, independent filtering, Cooks outliers) may explain part of the 214 vs 194 and the 0 vs 2.
2. **Spontaneous arm has 5 samples where the paper has 4 (FIG7a).** The figure legends imply 6 exclusions (18→13 biochemical, 8→7 mechanical) but the methods say 5. Only 5 samples fail a criterion I can compute from the counts. Exon/intron ratios are not in GEO, so the second spontaneous exclusion cannot be identified. I recorded this as a discrepancy.
3. **The biochemical and mechanical experiments were fitted as separate models (two cases).** The paper analyzes them separately (separate PCA and controls) but does not state how it composed its models.
4. **The threshold cutoff of 0.05 is the workflow default**, because the paper gives no numeric cutoff.
5. **GSEA used the Hallmark collection, not MSigDB c2-c6 v7.0.**

## Tool problems

- **MyGene.info failed during enrichment.** It returned 502 Bad Gateway on one batch (batch 23) while mapping Ensembl IDs to symbols for GSEA. The batch failure is reported at `tools/enrichment_tools.py:150`. The tool carried on with partial mappings: 33,475 of 34,889 IDs mapped. The deposited matrix already has a `GeneSymbol` column, so the enrichment tools could have used it with no network call. I didn't use `inputs.feature_column: "GeneSymbol"` because it would have changed the DE feature IDs.
- **About 27% of ranked genes had tied stats in GSEA.** gseapy warned "Duplicated values found in preranked stats: 27.4%" because the full ranking (`tools/enrichment_tools.py:348`) keeps many near-zero, low-count genes. The results are valid, but ordering among the ties is arbitrary.
- **The mechanical case's run summary reports `n_aligned: 26`, though only 7 samples entered the model.** `exclude_samples` is applied after alignment (`tools/case_runner.py:588-595`). The per-case level counts (MS 4, MC 3) are correct.
- **pydeseq2 printed RuntimeWarnings** ("overflow encountered in exp", `pydeseq2/utils.py:1088`) during fitting. This is harmless here, since the runs completed and `deg_sanity` is ok.
