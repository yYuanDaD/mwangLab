# HANDBACK — PMID39747484 / GSE280845

**The comparison with the paper rests on the abstract only.** No full text was available. I used the PubMed abstract (efetch, saved as `abstract_PMID39747484.txt`) and the GEO series text (summary, overall_design, data_processing). The paper's DEG counts are not known, so no count comparison was possible.

## What ran
- Data: `GSE280845_RAWCountMatrix.csv.gz`. These are StringTie gene raw counts from 12 gastrocnemius samples of male mice, in a 2×2 design: fl/fl WT vs cFeimin MKO, crossed with Sedentary vs 90-min running. There are n=3 per cell, and every value is an integer.
- Prep: `prep/fix_column_typo.py` renames one matrix column, `Exe_KO_reap4`, to `Exe_KO_rep4` to match the GEO title of GSM8606529. No values were changed. After the rename, all 12 samples align exactly on `title`.
- Model: one pydeseq2 Wald model fitted on all 12 samples (`tools.joint_contrasts:run_joint_deseq2`, cell model `~ ex + geno + ex:geno`). The suitability verdict was analyzable for all 5 comparisons, and the sex check found only one sex (consistent with "male" in GEO).
- Primary contrast: Exe vs Sed in WT (`ex_EXE_vs_SED_geno-WT`). The other comparisons are exploratory.
- Threshold: the authors' rule as stated in GEO data_processing, raw p < 0.05 and |log2FC| ≥ 1 (source `paper`). The audit rule is BH padj < 0.05 with no fold-change cutoff.
- Enrichment (primary contrast only): ORA (GO BP/MF/CC, KEGG) and Hallmark GSEA both completed. Top GSEA sets were TNFα/NF-κB up (NES 2.63), mTORC1 up, TGF-β up, EMT down and IFN-α down, all with FDR < 0.001. This is a typical acute-exercise immediate-early and stress response.

## DEG counts (paper rule: p<0.05 & |log2FC|≥1; audit: padj<0.05)
| Comparison | Role | DEGs (up/down) | audit padj<0.05 | Paper |
|---|---|---|---|---|
| Exe vs Sed, WT | primary | 840 (470/370) | 1116 | not available (abstract only) |
| Exe vs Sed, MKO | exploratory | 545 (328/217) | 625 | n/a |
| MKO vs WT, Exe | exploratory | 291 (188/103) | 126 | n/a |
| MKO vs WT, Sed | exploratory | 116 (94/22) | 1 | n/a |
| interaction ex×geno | exploratory | 128 (48/80) | 2 | n/a |

Gene named in the abstract: **Sln**. Its direction agrees with the abstract. Sln is higher in MKO than WT after exercise (log2FC +3.75) and slightly lower after exercise in WT (log2FC −0.87). However, its p-value is NaN: DESeq2's Cook's-distance filter flagged the outlier sample Exe_KO_rep4, which has 568 counts against 44–58 in the other two Exe_KO samples. With n=3 there is no outlier replacement, and R DESeq2 would also set this p-value to NaN. So the data support the abstract's Sln claim in direction only, not with a test. Foxc2 is barely expressed (baseMean 3.7, p=0.37).

## Deviations
- I used pydeseq2 instead of R DESeq2 1.40.2.
- The paper's exact contrasts are unknown. I took Exe-vs-Sed within WT as primary because the request is about the exercise effect.
- GEO extract_protocol mentions 18 libraries, but only 12 are deposited, and all 12 were used.
- The threshold is the authors' own rule but uses raw p, so with n=3 it is permissive. The padj audit counts are reported next to it.

## Tool problems
- None blocked the run.
- Minor: `inspect` showed the title key matching 11/12 samples but did not point out the near-miss column `Exe_KO_reap4`. I found it by hand and fixed it in a prep script.
- Minor: the runner's `paper_gene_check` reports `pvalue: null` for Sln without saying the Cook's filter caused it.
- Environment: a long bash heredoc containing apostrophes failed to parse (`unexpected EOF`), so the spec was written with the file tool instead.
