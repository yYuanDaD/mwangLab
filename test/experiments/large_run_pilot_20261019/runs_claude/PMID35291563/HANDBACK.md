# HANDBACK — PMID 35291563 / GSE149405

**Status:** finished (case completed, route `declared_deviation`, validator 13 records, 0 errors)

## What ran
- `inspect GSE149405`: downloaded the series and merged `GSE149405_RAW.tar` into `GSE149405_merged_from_tar.csv` (30,630 ENSMUSG genes × 12 samples, gene-level StringTie FPKM).
- Case spec `case_spec.json` → `python -m tools.case_runner execute` (run twice; the first attempt is in `_previous/`, the only change was adding study caveats).
  - Alignment: GSM id taken from the matrix column names (`^(GSM\d+)_\d+$`), exact match to the metadata index, 12/12. `grp` = `characteristics_ch1.1.group` (control 6, swimming 6).
  - Matrix: FPKM (24% integer values, median 0.37, GEO `data_processing` says FPKM). Gene level, while the paper analysed transcripts.
  - Design: two groups, swimming vs control, `~ grp`; mice are independent, so no blocking. Suitability verdict: analyzable.
  - Method: limma-trend on log2(FPKM+1).
    - Primary run filters to FPKM ≥ 1 in ≥ 6 samples (12,737 genes kept).
    - Sensitivity run uses no filter (30,630 genes).
  - Enrichment on the primary table:
    - ORA (GO and KEGG 2019 Mouse) on the paper-threshold DEGs.
    - GSEA on MSigDB Hallmark, ranked by the moderated t.

## Threshold
- The paper's rule (S2.6.p1, FIG2) reads "cut-off > 2; P < 0.05". I took this as fold change > 2 (|log2FC| > 1) and raw P < 0.05, with no FDR.
- That rule was applied as given (`paper_on_deviation_route`).
- Audit rule: BH FDR < 0.05, with no fold-change cutoff.

## DEG counts vs the paper
| Contrast | Ours (paper rule) | Up / Down | Audit FDR<0.05 | Paper |
|---|---|---|---|---|
| swimming vs control (primary, filtered) | 20 | 13 / 7 | 0 | 1344 transcripts (715 up / 629 down) |
| swimming vs control (no filter, sensitivity) | 17 | 12 / 5 | 0 | — |

- At the gene level there is almost no signal. In the primary run, 714 of 12,737 genes have raw P < 0.05, against about 637 expected by chance.
- The paper's named genes do not replicate:
  - Vegfa (paper: significantly down): log2FC −0.09, P = 0.56.
  - Stat3, Pdgfa, Pld2 and Pik3r2 (paper: decreased): all have P > 0.05 and three of the four lean upward.
  - Hif1a and Kdr: unchanged, as the paper also reports.
- Enrichment, kept separate from the DE result:
  - Hallmark HYPOXIA is enriched upward with swimming (NES +1.72, FDR 0.006), the opposite of the paper's "reduced hypoxia" reading.
  - Hallmark ANGIOGENESIS is not enriched (FDR 1.0).
  - The top Hallmark sets are interferon-γ/α response and G2M/E2F, all upward.
  - KEGG ORA on the 20 DEGs is driven by four MHC-II genes (antigen processing and presentation). The paper's angiogenesis, hypoxia and VEGF pathways do not appear.
- These contradictions are recorded in the study gate's `caveats`.

## Deviations (declared)
1. **Feature level.** GEO has only gene-level FPKM; the paper's DETs are transcripts (ENSMUST IDs in Table 1). Transcript-level DE cannot be reproduced, so the counts cannot be compared directly.
2. **Transform and filter.** The paper states neither. I chose log2(FPKM+1) and FPKM ≥ 1 in ≥ 6 samples, and ran an unfiltered sensitivity analysis next to it.
3. **Reference genome.** The paper text says reads were mapped to hg38; GEO says GRCm38.92, and the matrix uses mouse Ensembl IDs. I treated hg38 as a typo.

## Tool problems
- No blocking problems.
- Minor: in the inspect output, `extract_protocol_ch1` shows mojibake ("1 渭g" instead of "1 µg"). The UTF-8 µ is being decoded as GBK somewhere when the metadata or soft file is read during inspect (`tools/case_runner.py` inspect path / GEO metadata writer). I could not find the exact file:line. It only affects display, not the analysis.
