# HANDBACK — PMID39357875 / GSE273579

**The comparison with the paper rests on the abstract only.** No full text was available. I used the PubMed abstract (NCBI efetch, saved as `abstract_PMID39357875.txt`) and the GEO series summary and overall design. The paper's DE method, threshold and DEG counts are unknown.

## What ran
- `case_runner inspect GSE273579`, then `case_runner execute case_spec.json`. It ran twice: the second run only added study caveats, and the first run is in `_previous/`. The final run's status is `completed`, and the validator found 15 records with 0 errors.
- **Matrix:** `GSE273579_RAW.tar` holds per-sample featureCounts outputs (raw integer counts; library sizes 16–20 M). They were merged into 55,359 genes × 20 samples, and every sample aligned exactly to its GSM ID (20/20).
- **Design:** there are 5 groups of 4 male mice: ND non-exercise; HFD non-exercise non-tumor (NT); HFD non-exercise tumor (T); HFD exercise NT; HFD exercise T. Exercise was compared with non-exercise only within HFD/DMBA mice and within one tissue at a time (4 vs 4). No blocking was needed, because each mouse gives one sample per tissue. The ND samples are not used in any contrast, since ND has no exercise arm.
- **Method:** DESeq2 (pydeseq2 Wald), `~ ex`, fitted separately for NT and for T.
- **Threshold:** `workflow_default`, BH padj < 0.05 with no fold-change cutoff, because the abstract states no threshold. Raw p < 0.05 is reported as a labelled audit rule.
- **Enrichment:** ORA (Enrichr GO/KEGG) and Hallmark GSEA ran on both contrasts and completed.

## DEG counts vs the paper
| Contrast | Role | padj<0.05 (up/down) | audit raw p<0.05 | Paper |
|---|---|---|---|---|
| EX vs NE, non-tumor liver | primary | 189 (144/45) | 1599 | not stated in abstract |
| EX vs NE, tumor tissue | secondary | 68 (51/17) | 978 | not stated in abstract |

Genes the abstract names:
- **Per1** goes up in both tissues, as the paper says: NT log2FC 1.09, padj 0.005; T log2FC 1.18, padj 0.013.
- **Cry2** goes up in both tissues, as the paper says: NT log2FC 0.32, padj 0.039; T log2FC 0.60, padj 0.009.
- **E2f1** is unchanged in both tissues, as the paper says: padj 0.72 (NT) and 0.999 (T).
- **Myc** is not significant in either tissue (padj 0.41 / 0.85), which matches "transcriptionally unchanged". Its raw log2FC is +0.89 in NT, though (p 0.036).

Paper's "E2F1/c-Myc targets down" claim:
- **Tumor tissue agrees.** Hallmark E2F_TARGETS has NES −2.85 and G2M_CHECKPOINT has NES −3.12, both FDR ≈ 0. MYC_TARGETS_V1 is down but not significant (NES −1.09).
- **Non-tumor liver contradicts it.** MYC_TARGETS_V1 has NES +1.64 (FDR 0.0045), MYC_TARGETS_V2 has NES +1.56 (FDR 0.0099), and E2F_TARGETS has NES +1.31 (FDR 0.068). This is recorded in the study `caveats`. We cannot tell which tissue the paper's claim refers to.

## Deviations
- The route is `declared_deviation`. The paper's DE method and threshold are unknown, so I used DESeq2 with the workflow-default threshold.
- Analysing the two tissues separately was my decision. GEO lists them as separate tissues, and the abstract does not say how the paper split them.
- **Discrepancy:** GEO `data_processing` says the supplementary files contain TPM, but the deposited files are raw featureCounts counts (the header line reads `# Program:featureCounts v2.0.5`).
- **Discrepancy:** GEO says the annotation is Gencode M32, but the featureCounts command used `gencode.vM27.annotation.gtf`. Neither discrepancy blocks the analysis.

## Tool problems
- The cached GEO metadata has broken characters: in `data/GSE273579/GSE273579_metadata.csv`, `’` appears as `鈥檚` and `μ` as `渭`. The UTF-8 text was decoded as GBK at download time, somewhere in `tools/geo_tools.py`. I did not pin the line. It does not affect the analysis.
- pydeseq2 printed `RuntimeWarning: overflow encountered in exp` (`pydeseq2/utils.py:1088`) during fitting. This is harmless, and the results look sane.
- Nothing else; the runner and validator raised no errors.
