# Stage H: one real study against Bo's gold results

Reference: Bo's frozen benchmark folder `RNAseqData4Testing/GSE195482` (R DESeq2, `~ Group`,
`rowSums >= 10` filter, DEGs at padj < 0.05 and |log2FC| > 0.5). Two pairwise contrasts:
`WMF_vs_WCF` (female WT, HFpEF diet vs chow) and `WMM_vs_WCM` (male).

The tested workspace (`output/stage_h/repo`) holds a clean repository snapshot plus
`cases/GSE195482/` with the two count matrices, their metadata, `paper.md` (text of the
published article), and `cases/manifest.json`. Bo's DEG, GSEA, and script files are withheld.

After the run, score each contrast:

    python compare_to_reference.py <skill DEG csv> <bo>/WMF_vs_WCF.allgene.DEseq2.txt --out wmf.json
    python compare_to_reference.py <skill DEG csv> <bo>/WMM_vs_WCM.allgene.DEseq2.txt --out wmm.json

Expected decisions: two separate pairwise contrasts per sex as in the paper (not pooled), raw
counts, DESeq2, no blocking (different animals), paper threshold. Differences from Bo's numbers
must be explained by a recorded decision (for example a different low-count filter or an
effect cutoff the paper does not state).
