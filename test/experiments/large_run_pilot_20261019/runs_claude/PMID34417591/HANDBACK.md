# HANDBACK — PMID 34417591 (Islam et al. 2021, irisin / FNDC5, PMC10317538)

Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`; validator 22 records, 0 errors. Final attempt is the third; earlier ones are in `_previous/`.

## What ran

| Case | Outcome | Why |
|---|---|---|
| GSE174211: newborn-neuron nuclei, WT/F5KO × Sed/Run (4/4/4/5 males) | **completed**, route `exploratory` | This is the only one of the three series with an exercise arm |
| GSE174210: APP/PS1 hippocampus, AAV8-irisin vs AAV8-GFP (5/5) | **refused at design** | There is no exercise arm. Irisin overexpression mimics exercise but is not exercise. The deposited matrix is DESeq2-normalized non-integer counts, and some gene IDs were converted to dates by Excel (`1-Mar` and similar) |
| GSE179078: dentate gyrus, F5KO vs WT (5/5) | **refused at design** | There is no exercise arm. The comparison is genotype only |

GSE174211 model and matrix:

- **Matrix:** raw STAR gene counts. The file is named "normalized", but every value is an integer and the library sizes range from 1.08M to 8.52M.
- **Model:** pydeseq2.
  - A joint `~ grp` model (grp = genotype_exercise, 4 cells) on all 17 samples.
  - Exercise main effect with `~ geno + ex`.
  - The paper's pooled genotype contrast with `~ geno`.
- **Sex check:** passed; all samples are male.
- **Enrichment:** not run. The paper's GSEA is for KO vs WT, not exercise.

## Threshold

The paper's rule (S2.5.p2) is "log2FC > |1.5|, p-value < 0.05": raw p < 0.05 and |log2FC| > 1.5. I applied it exactly. As an audit I also counted genes with BH padj < 0.05.

## DEG counts vs the paper

| Table | Ours (paper rule) | up / down | Audit padj<0.05 | Paper |
|---|---|---|---|---|
| joint/grp_WT_Run_vs_WT_Sed (exercise in WT, primary for the request) | 37 | 8 / 29 | 0 | not reported ("underpowered", S2.5.p2) |
| joint/grp_KO_Run_vs_KO_Sed (exercise in KO) | 26 | 14 / 12 | 0 | not reported |
| ex_Run_vs_Sed_adj_geno (~geno+ex) | 20 | 5 / 15 | 0 | not reported |
| geno_KO_vs_WT (pooled; the paper's contrast, secondary) | 784 | 436 / 348 | 5488 | 459 |
| joint KO_Sed vs WT_Sed, WT_Run vs KO_Run, and the cross-cell contrasts | 422 / 524 / 361 / 587 | — | — | — |

Conclusion on exercise: in this dataset, voluntary running has no FDR-significant effect on newborn-neuron nuclear transcripts in WT or KO mice. This agrees with the paper's statement that the dataset was underpowered for an exercise effect. The 20–37 genes that pass the raw-p rule are about what chance would produce among roughly 25k genes.

## Deviations

- Exercise contrasts are exploratory: the paper did not analyse them.
- pydeseq2 was used instead of R DESeq2 v1.10.1. The paper's gene-filtering rule is in a supplement that was not available, so no prefilter was applied. This probably explains why we find more KO-vs-WT DEGs than the paper (784 vs 459).
- I could not tell whether the paper's KO vs WT model included exercise. I used the pooled `~ geno` model.
- **FNDC5 is slightly higher in KO** in pooled KO vs WT (log2FC +0.36, padj 1.5e-4), which is unexpected for a knockout. The likely cause is a partial-exon deletion combined with nuclear/intronic reads. This is recorded in the study caveats; the genotype labels were not independently verified.

## Tool problems

- `tools/suitability.py:201-203`: when neither level is the reference, the pairwise comparisons get their direction from level order. With `comparisons: "all"`, the within-KO exercise contrast therefore came out as `grp_KO_Sed_vs_KO_Run`, with its sign inverted relative to the exercise direction. The workaround was to add `grp_KO_Run_vs_KO_Sed` to `planned`, which triggers `add_reversed_planned` at line 240.
- pydeseq2/joblib: there were overflow RuntimeWarnings in `pydeseq2/utils.py:1088`, and a loky worker raised `OSError: [WinError 6]` at shutdown on Windows. The run was not affected.
- `inspect`: the GSE174211 matrix is labelled "raw_counts (confirm...)". Correct, but the "normalized" file name and the FPKM line in data_processing make the matrix type ambiguous. I resolved it by hand from the column sums.
