# HANDBACK — PMID36120562 / GSE208354

## What ran
- `inspect GSE208354` (downloaded to `data/GSE208354`), then the case spec route: `python -m tools.case_runner execute case_spec.json` (run twice; the first attempt is in `_previous/`). The validator passed: 14 records, 0 errors.
- Study: HFpEF mice (HFD + L-NAME) with 8 weeks of treadmill exercise (HFpEF+EXT) vs sedentary HFpEF. Heart input RNA-seq, 3 vs 3 (S2.8.p1, S3.4.p1). The paper's "control" is sedentary HFpEF, which GEO labels `control`.
- Matrix: `GSE208354_All_comparison_mRNA.csv`, which holds **FPKM** values (fractional; column sums 0.9–1.3e6; Fig 3A shows FPKM). No raw counts were deposited.
- Alignment: exact match on GEO `title`, 6/6 input samples. I excluded the 6 m6A IP (RIP-Seq) GSMs. Matrix column `HF40-input` has no GSM record, and the paper says n = 3, so it was dropped.
- Primary (`grp_HFEXT_vs_HF`): limma-trend on log2(FPKM+1), `~ grp`. I kept genes with FPKM >= 1 in at least 3 samples (12,057 of 53,465).
- Sensitivity (`grp_HFEXT_vs_HF_nofilter`): the same model with no expression filter.
- Enrichment: Enrichr ORA (GO/KEGG) for up and down DEGs separately, plus Hallmark GSEA on the limma t ranking. All three completed.
- Out of scope: the m6A peak and differential-methylation analysis (MeRIP), because it measures a different assay.

## DEG counts vs paper
Paper threshold (S3.4.p1, Fig 3B): FC > 2 and raw p < 0.05, applied here as |log2FC| > 1, p < 0.05.

| Table | Ours (up/down) | Paper (up/down) |
|---|---|---|
| grp_HFEXT_vs_HF (primary, filtered) | 97 (47/50) | 690 (267/423) |
| grp_HFEXT_vs_HF_nofilter (sensitivity) | 108 (49/59) | — |
| audit, BH FDR < 0.05 | 0 | — |

The 10 Table 3 genes all have the same sign as in the paper:
- Down: Casp12, Capn2, Fas, Casp7, Jun, Pdia3.
- Up: Tnnt2, Mef2a, Adrb1, Agtr1a.

Our fold changes are slightly smaller, for example Jun −0.87 vs −0.99 and Tnnt2 +0.65 vs +0.73. Seven of the 10 have p < 0.05; Casp12, Casp7 and Agtr1a do not. No gene passes FDR < 0.05, so with n = 3 the result rests on raw p, as the paper's does.

Pathways are supporting only:
- Down-DEG KEGG: fatty acid elongation, unsaturated fatty acid biosynthesis, Apelin, PPAR.
- Up-DEG KEGG: glycolysis/gluconeogenesis.
- GSEA: OXPHOS is up in EXT (FDR 0.04); myogenesis is up (FDR 0.07).

These broadly fit the paper's "myocardial energy metabolism" theme. Apoptosis is not among our top KEGG terms.

## Deviations
1. **Method.** I used limma on log2(FPKM+1) instead of DESeq2 on featureCounts counts, because counts were not deposited. The paper's threshold is applied unchanged (`paper_on_deviation_route`).
2. **Low-expression filter.** The FPKM >= 1 in ≥3 samples filter is my choice; the paper states none. The unfiltered sensitivity run gives almost the same count (108 vs 97), so the filter does not explain the gap to the paper's 690.
3. **Likely cause of the 7× gap.** log2(FPKM+1) shrinks fold changes of low-expressed genes. DESeq2 at raw p < 0.05 with no fold-change shrinkage calls many low-count genes with large fold changes. This cannot be checked without counts.
4. **HF40-input dropped.** It is a 4th HFpEF column in the deposited matrix with no GSM; the paper says n = 3.

## Tool problems
- No blocking problems; every gate and executor ran.
- Minor: the `data_processing` and `extract_protocol` text in `data/GSE208354/GSE208354_metadata.csv` is mojibake ("3鈥 adaptor", "NEBNext庐"). The UTF-8 text was decoded as GBK somewhere when the GEO metadata was written in `tools/geo_tools.py`; I did not find the exact line.
- Minor: `inspect` profiles `GSE208354_Differentially_methylated_sites.mRNA.txt.gz` as a candidate expression matrix. It treats BED coordinate columns (`chromStart`, `score`, ...) as samples; it was harmless here.
