# HANDBACK: GSE293221 (PMC13076624, exercise / Phellodendron amurense in TRAMP prostate tumors)

## What ran
- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`); validator: 14 records, 0 errors; status completed, route `declared_deviation`.
- Input: per-sample HTSeq-count files from `GSE293221_RAW.tar` (merged), columns renamed to GSM ids and rows put in a fixed shuffled order by `prep_matrix.py` (values unchanged; see tool problem 1). Raw integer counts, 22,609 gene symbols x 9 samples; exact alignment on the GSM index, 9/9.
- Design: `grp` from title: CON / EX (voluntary wheel running) / PHAM (Nexrutine diet), 3 each, independent animals. No blocking. Housing (EX single-housed, others group-housed) is part of the intervention and fully aliased with it.
- Executions:
  - `joint` (primary): one pydeseq2 model `~ grp` on all 9 samples, contrasts EX vs CON (primary), PHAM vs CON (secondary), PHAM vs EX (exploratory).
  - `joint_cpmfilter` (sensitivity): same model after a CPM >= 1 in >= 3 samples filter (14,722 genes kept), standing in for the paper's RPKM > 1 filter.
  - `twoarm_EX_vs_CON` (sensitivity): DESeq2 on the 6 CON+EX samples only.
- Enrichment: ORA (Enrichr GO/KEGG) + Hallmark GSEA on joint EX vs CON; ORA on the two-arm table.

## Threshold
Paper rule (S4.7.p1): FDR < 0.05 and fold change > 1.5 either way, i.e. padj < 0.05 and |log2FC| > 0.5849625, applied as `paper_on_deviation_route`. The paper's third criterion (average RPKM > 1 in at least one group) could not be applied because the deposit has no gene lengths.

## DEG counts vs paper (paper rule)
| Contrast | Ours | Paper |
|---|---|---|
| EX vs CON, joint (primary) | 32 (27 up / 5 down) | 32 |
| EX vs CON, joint + CPM filter | 28 (23 / 5) | 32 |
| EX vs CON, two-arm | 385 (222 / 163) | 32 |
| PHAM vs CON, joint | 3694 (2644 / 1050) | 176 (76 up / 100 down) |
| PHAM vs CON, joint + CPM filter | 3399 | 176 |

The count match on the primary table is a coincidence, not a reproduction. Paper-named exercise genes:
- Joint fit: Lipe, Plin1 and Slc7a10 go in the paper's direction (down, log2FC -1.5 to -2.4), but their padj is NA (Cook's outlier flag driven by the PHAM arm). Gpr83 is down and Dgat2l6 up (log2FC 5.8), both non-significant.
- Two-arm fit: all five are significant in the paper's direction: Lipe, Plin1, Slc7a10 and Gpr83 down, Dgat2l6 up.

The joint EX DEGs are mostly up. They include seminal-vesicle secretory genes (Svs1-6, Sva, Spinkl), which suggests the excised tumors carried different amounts of seminal-vesicle tissue.

Enrichment:
- Joint EX ORA gives immune/neutrophil terms, not the paper's triglyceride/lipase terms.
- Two-arm ORA has Lipid Droplet (CC, padj 0.0017) and Acylglycerol O-acyltransferase (MF, padj 0.039). Triglyceride catabolic process (padj 0.07) and triglyceride lipase activity (padj 0.11) are near the cutoff.

## Deviations and caveats
- Method: DESeq2 (pydeseq2 Wald) instead of the original DESeq. There is no executor for the original DESeq here; its default "maximum" dispersion sharing and exact test are more conservative.
- The RPKM > 1 prefilter was not applied; the CPM filter run is a sensitivity analysis.
- **Direction contradiction**: the paper says BB123696 and Lman1l rise with both interventions (S2.2.p3). Here both are lower in EX (n.s.) and significantly lower in PHAM (log2FC -4.3, -5.3). This is recorded in the study caveats.
- Two of the three PHAM tumors (GSM8878842, GSM8878843) are outliers against every other sample (Spearman about 0.6-0.7, against 0.93 or more elsewhere). They have high Dcx/Sncb and lose Spink3/Plin1, which looks like a different tumor phenotype. This drives the inflated PHAM DEG count and the Cook's NA in the joint EX contrast. The paper-named PHAM genes all match its direction (Spink3/5, Slc26a4, Apof, Pls1, Mmp7, Dclk3, Gstt3, Atp2c2 down; Dcx, Sncb up).
- The tumors were "representative" (S2.2.p1), n = 3 per arm.
- GEO says stranded mRNA polyA; the paper says KAPA RiboErase. Recorded as a discrepancy that does not block execution.

## Tool problems
1. `tools/native.py:620` (`feature_id_report`) classifies only the first 2000 IDs, and the gene_symbol regex at `tools/native.py:601` rejects digit-leading mouse symbols (0610005C13Rik, 1110...). In an alphabetically sorted mouse table those IDs fill the head, so only 54.6% count as symbols. The type is then called "other", and `tools/case_runner.py:815-821` skips enrichment, although 93.5% of all IDs are symbols. Workaround: the row shuffle in `prep_matrix.py`.
2. `tools/joint_contrasts.py:115` and `tools/deseq2_tools.py:163` hard-code Cook's handling (`refit_cooks=True`, with no option to turn off Cook's p-value filtering). With 3 replicates per group, the paper's key genes get padj NA in the joint fit.
3. There is no executor for the original Bioconductor DESeq (method blocked, declared as a deviation).
