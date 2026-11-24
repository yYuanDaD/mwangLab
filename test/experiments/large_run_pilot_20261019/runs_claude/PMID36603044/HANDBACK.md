# HANDBACK — PMID36603044 / GSE221894

**The comparison with the paper rests on the abstract only.** No full text was available. The sources were the PubMed abstract (`PMID36603044_abstract.txt`, NCBI efetch), the GEO series description and data_processing (`GSE221894_family.soft`), and the authors' deposited DESeq2 table `GSE221894_PostLean-PreLean_rawDE-v2.xls.gz`. The abstract gives no DEG count and no threshold. The count comparison below uses the deposited table, not the paper text.

## What ran
- **Data.** 27 per-sample salmon v1.4.0 `quant.sf` files from `GSE221894_RAW.tar`, at transcript level (ENST.version).
  - `prep_salmon_to_gene.py` sums NumReads per Ensembl gene, using a transcript→gene map from the Ensembl 104 GTF (`data/_reference/`). This is tximport-style, without length offsets.
  - Result: 34,402 genes × 27 GSM. About 1.4% of reads fall on transcripts missing from Ens104 and are not counted (log: `prep_salmon_to_gene.log`).
- **Matrix type.** Estimated counts, rounded, run through DESeq2 (pydeseq2), matching the paper's salmon → DESeq2 route.
- **Design.** Within-person change, post (48 h after 7 HIIT sessions) vs pre. Primary model `~ subject + time` on complete pairs.
- **Labelling fix.** GSM6909087 (title `7b`) is annotated "baseline" in GEO. I relabelled it as post from the title convention: that gives 14 post biopsies, which matches the abstract's 14 completers.
  - Unpaired samples (27a, 4b, 8b) are dropped from the paired models.
- **Runs** (all executed; the contract validator reported 0 errors):

| table | role | samples | DEGs padj<0.05 (up/down) | raw p<0.05 (audit) |
|---|---|---|---|---|
| time_post_vs_pre | primary, paired | 12 pairs | 174 (93/81) | 1403 |
| sens_no_subject7_time_post_vs_pre | sensitivity | 11 pairs | 104 (55/49) | 1283 |
| unpaired_all_time_post_vs_pre | exploratory, `~ time` | 27 (14 post/13 pre) | 62 (32/30) | 1347 |
| female_time_post_vs_pre | exploratory | 7 pairs | 146 (95/51) | 1414 |
| male_time_post_vs_pre | exploratory | 5 pairs | 44 (15/29) | 1027 |

- **Threshold.** The abstract states none, so I used the workflow default: BH padj < 0.05 with no fold-change cutoff.

## DEG counts vs the paper
- **Authors' deposited table:** 35 DEGs at padj < 0.05 (19 up, 16 down). It lists only 5,944 genes, all with baseMean > 140.
- **Unpaired `~ time` (exploratory):** essentially the authors' model.
  - logFC r = 0.999 and sign agreement 99.8% on the 5,944 shared genes.
  - It recovers 34 of their 35 DEGs. We call 62 in total; the extra genes probably come from different filtering or independent filtering.
  - Conclusion: the authors did not block on participant.
- **Paired primary:** 174 DEGs.
  - logFC r = 0.83 vs the authors' table; it recovers 31 of their 35 DEGs.
  - Named genes keep their direction: COQ10A, MDH1, ALAS1, BCKDK, CHCHD3 and GYS1 up; MSTN, USP6 and TRIM32 down. PFKFB3 is down but padj = 0.054.
- **Pathways (abstract):** "increased transcripts → mitochondrial respiration, esp. complex I" is reproduced.
  - Hallmark OXPHOS is the top GSEA set (NES 2.86, FDR ≈ 0).
  - Top ORA-up terms are aerobic ETC and respiration; the genes include complex I subunits NDUFA8 and NDUFB6.
- **Pathways (abstract):** "decreased transcripts → DNA/chromatin remodelling" is only weakly seen.
  - ORA-down is led by muscle development and fibre organisation terms; chromatin and DNA terms have FDR > 0.09.
  - GSEA G2M checkpoint and mitotic spindle are negative at FDR ≈ 0.1.
  - Nothing contradicts the paper's direction.

## Deviations
- **Participant blocking.** I added it from the study design. The authors evidently fitted an unpaired model, which is run here as exploratory.
- **Gene summarisation.** Summed NumReads without tximport length offsets, Ensembl 104 map, pydeseq2 instead of R DESeq2 1.32.
- **7b relabelled to post**, with a sensitivity run that drops subject 7 (104 DEGs).

## Tool and environment problems
1. **GEO download failed through the tool.** The NCBI GEO FTP and HTTPS mirror returned 403 for every `/geo/` path for about 10 minutes, then worked again.
   - `download_geo_data` (`tools/geo_tools.py:30`, `GEOparse.get_GEO`) failed with a missing temp-file error rather than surfacing the 403.
   - I fetched the SOFT file through acc.cgi, built the metadata with `GEOparse.get_GEO(filepath=…)`, and downloaded the supplementary files with curl once the 403s stopped.
2. **Inspect cannot read this `.xls.gz`.** `tools/case_runner.py:54` assumes GEO `.xls.gz` files are TSV. This one is real BIFF Excel, so inspect raised a UnicodeDecodeError. `xlrd` is also missing from `.venv-pdf`; I installed it to the scratchpad only.
3. **No salmon `quant.sf` support.** The runner and `merge_raw_tar` have no transcript→gene route for salmon files, so a hand prep script plus a downloaded GTF was needed. Ensembl BioMart returned an empty response, and the US mirror failed on TLS.
4. **Sex check is unreliable on this matrix.**
   - XIST is absent from the matrix (the salmon index appears to have no lncRNAs), so all females come out "ambiguous".
   - 20b is called male (low) on Y-gene counts of about 10–16 against 300–1,000 in males (`tools/stats_tools.py:379`, an absolute margin on log signal). That is a false MISMATCH.
   - Reported sexes agree with the Y-gene signal, so no samples were changed.
