# HANDBACK: PMID 41673803 / GSE286570

The paper studies NAFLD mice on a high-fat diet (HFD) that did aerobic exercise (HAE) or resistance exercise (HRE). The data are liver RNA-seq: featureCounts raw counts, 12 samples, 3 per group (NC, HFD, HAE, HRE).

## What ran
- Case-spec route (`tools.case_runner execute case_spec.json`). Preflight was skipped as instructed. The run completed and the decision contract validated with 0 execution failures.
- **Gates.**
  - Ownership: DA.p1 names GSE286570. The GEO data_processing text matches S4.5.p1 word for word.
  - Alignment: the matrix columns matched the metadata `title` exactly after key normalization (`H-AE1` = `H-AE-1`), 12/12.
  - Groups: `grp` comes from the treatment characteristic, recoded to NC/HFD/HAE/HRE.
  - Matrix: raw counts, so DESeq2.
  - Covariance: not required, since every sample is an independent male mouse.
- **Primary execution.** One pydeseq2 model, `~ grp`, on all 12 samples, with HFD as the reference. It gave four contrasts:
  - HAE vs HFD and HRE vs HFD: primary, the exercise effect.
  - NC vs HFD: secondary, the diet check, which is the mirror of the paper's HFD vs NC.
  - HAE vs HRE: secondary, the comparison between exercise types.
- **Sensitivity.** Separate two-group DESeq2 fits for HAE vs HFD and HRE vs HFD, because the paper does not say whether it fitted each pair on its own.
- **Enrichment.** ORA on up-regulated genes (Enrichr GO and KEGG) and Hallmark GSEA, for both exercise contrasts.

## Threshold
The paper's threshold (S4.5.p1) is written as "log2FC < 1 and p-value < 1E-2". I read this as **raw p < 0.01 and |log2FC| > 1**. The literal wording cannot be right, because the paper reports both up- and down-regulated DEGs. This rule was applied as the paper's threshold. A second count at BH padj < 0.05 with no fold-change cutoff is kept as an audit.

## DEG counts vs the paper (paper's rule)
| Contrast | Ours (joint model) | Up/Down | Pairwise sensitivity | Paper | Audit (padj<0.05) |
|---|---|---|---|---|---|
| HAE vs HFD | 1488 | 420/1068 | 1551 | 1450 (Fig 6C) | 2082 |
| HRE vs HFD | 467 | 120/347 | 461 | 171 (Fig 6D) | 183 |
| HFD vs NC (run as NC vs HFD) | 2470 | 1556/914 as HFD vs NC | n/a | 2746 (Fig 6B) | 4163 |
| HAE vs HRE | 253 | 66/187 | n/a | 625 (Fig 6E) | 24 |

- **Closely reproduced:** HAE vs HFD and HFD vs NC.
- **Not reproduced:** we find about 2.7x the paper's DEGs for HRE vs HFD, and about 0.4x for HAE vs HRE.
- **Same ordering as the paper:** HAE changes liver expression more than HRE does, relative to HFD.
- **Named genes.** All of them move in the paper's direction in both exercise contrasts:
  - Up: Hsd3b5, Cyp4a12b, Slco1a1.
  - Down: Cd8b1, Cidea, Ccl7, Sprr1a, Sit1 (HAE) and Slc7a11 (HRE).
  - Most of them pass the paper's rule. Slco1a1 and Cyp4a12b pass in both contrasts. Ccl7 has p = 0.008 in HAE, and its padj is NA because DESeq2's independent filtering removed it.
- **Enrichment** is kept separate from the DE result. In KEGG ORA on HAE-up genes, Retinol metabolism and Arachidonic acid metabolism are significant. Bile secretion and Fatty acid degradation are nominally enriched; both are in the paper's Fig 6H. For HRE-up genes, PPAR signaling and Biosynthesis of unsaturated FA are nominal (p about 0.015, adjusted p 0.14), matching the paper's Fig 6I. In GSEA, the inflammatory Hallmark sets are negative in HRE vs HFD (TNFA/NFKB, IL6/JAK/STAT3, allograft rejection, IFN-gamma), which agrees with the paper's GO-down immune and inflammatory terms.

## Deviations
- pydeseq2 Wald was used instead of R DESeq2 1.40.1.
- The primary model is a joint 4-group fit with shared dispersion. The paper's design is not stated, so the pairwise fits are the sensitivity check, and they give similar counts.
- **Sample size.** GEO has 3 livers per group, while the paper's animal groups have n = 8 (NC n = 13). The RNA-seq n is not stated, so I assumed these 3 per group are what was sequenced. The deposited sample numbers are not consecutive (NC 2,4,5; RE 3,4,5), which suggests the authors picked a subset.
- The diet contrast was extracted as NC vs HFD because the model's reference is HFD. The counts are symmetric, so this does not change the result.
- With n = 3, counts at raw p < 0.01 are unstable. This is the most likely reason for the HRE and HAE-vs-HRE gaps, together with the joint model's dispersion.

## Tool problems
- No blocking problems.
- Minor: the metadata `data_processing` text contains mojibake. Smart quotes came through as "鈥", which looks like GBK decoding of the SOFT file when `GSE286570_metadata.csv` was written (tools/geo_tools.py:36, GEOparse parse path). This is cosmetic.
- Minor: `inspect`'s `feature_examples` (tools/case_runner.py:404) prints whole featureCounts rows, including very long `;`-joined Chr/Start/End fields. The output is bloated but correct.
- Minor: gseapy warned that about 15% of the preranked stat values are duplicated (case_runner.log:138,144).
