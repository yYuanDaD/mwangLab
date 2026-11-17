# HANDBACK: PMID 33661096 / GSE145263

**Status: finished** (case-spec route, `python -m tools.case_runner execute case_spec.json`; validator: 13 records, 0 errors).

## What ran
- Paper (PMC8043751): five separate mouse cardiac-EC RNA-seq experiments, each compared with its own control. The exercise experiment is 6-week progressive treadmill training (EXE) vs sedentary (SED) in male C57BL/6J mice, n=3 vs 3 (S2.1.p1, S4.2.p1, FIG2A). Method: HTSeq counts with a two-group DESeq2 Wald test and BH correction (Chipster v3.12.2), FDR <= 0.05 and no fold-change cutoff (S4.15.p1, FIG2 legend).
- Data: `GSE145263_RAW.tar` was merged into 52,636 Ensembl genes x 31 samples of integer HTSeq counts. Samples aligned exactly on GSM id (31/31). `grp` was recoded from `characteristics_ch1.2.treatment`. The 25 samples from the aging, HFD and TAC experiments were excluded because the paper analyses each experiment only against its own control.
- Suitability: analyzable. The sex check passed (all male, as in the metadata).
- Model: DESeq2 (pydeseq2) `~ grp`, EXE vs SED, alpha 0.05, no covariates. Animals are independent and no batch is recorded.
- Enrichment: Enrichr ORA (GO BP/MF/CC + KEGG) on the up-regulated and down-regulated DEG sets, standing in for the paper's PANTHER, plus exploratory Hallmark GSEA ranked by the Wald stat.

## DEG counts vs paper (paper threshold: BH FDR <= 0.05, no |log2FC| cutoff)
| Contrast | Ours | Paper |
|---|---|---|
| EXE vs SED | 139 (48 up / 91 down) | not readable: the count is only inside the FIG2A MA-plot image, not in the text |

- Audit rule (padj < 0.05 and |log2FC| > 1): 28 DEGs.
- Named genes (S2.3.p1, FIG4A-C: all down with exercise) are all reproduced as significantly down:

| Gene | log2FC | padj |
|---|---|---|
| Serpinh1 | -0.50 | 0.042 |
| Vwa1 | -0.60 | 0.0045 |
| Mest | -0.43 | 0.041 |
| Fhl3 | -1.01 | 0.0099 |

- Consistent with the paper's statement that exercise affected fewer genes than the risk factors (S2.1.p2, S3.p2).
- ORA:
  - Down-regulated genes: 6 GO BP terms at adj p < 0.05, including extracellular matrix/structure organization. This partly matches the paper's report that exercise down-regulates collagen- and ECM-related pathways.
  - Up-regulated genes: no GO BP term at adj p < 0.05.
- GSEA: no Hallmark set at FDR < 0.05. TGF-beta signaling has the lowest negative NES (-1.25, FDR 0.09), the same direction as the paper's reduced TGF-beta after exercise. This is exploratory.

## Deviations
- pydeseq2 was used instead of R DESeq2 in Chipster. The model is the same, but independent filtering and outlier handling differ slightly.
- Enrichr GO/KEGG ORA was used instead of PANTHER (v14.1, raw p < 0.05). Enrichment is reported separately from the DE result.
- The paper's own count could not be compared numerically (image only). The supplementary Fig. 2 source data (xlsx) were not downloaded.

## Tool problems
- Minor: Hallmark GSEA ranks every gene the DESeq2 output keeps, including about 7,200 genes with baseMean < 1. These give tied Wald stats, and gseapy warns that 25% of the ranked stats are duplicates (`case_runner.log:81`). The ranking is built in `tools/enrichment_tools.py:348-397`, which drops NaN but applies no low-count filter. The tied genes make the GSEA gene order partly arbitrary.
- No other problems: alignment, suitability, execution, ORA and the validator all completed without errors.
