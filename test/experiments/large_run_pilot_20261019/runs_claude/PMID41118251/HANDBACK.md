# HANDBACK: PMID41118251 / GSE289569

Paper: PMC12643488, "A role for the transcriptional coregulator RIP140 in the control of muscle endurance fitness."
Status: finished (valid decision; execution completed; route `declared_deviation`). The validator found 0 errors across 12 records.

## What ran
- `python -m tools.case_runner inspect GSE289569`: the data were not cached and were downloaded into `data/GSE289569`.
- `prep/prep_matrix.py` splits the single GEO supplementary table `GSE289569_fpkm_and_deseq2_results.tsv.gz` into two files:
  - the 12 FPKM sample columns, indexed by unique `gene_id` (Ensembl). The column names were decoded from the authors' labels, e.g. `WT_S_EDL_1` became `Ctrl_Sedentary_1`.
  - the authors' 8 DESeq2 result columns, saved as `prep/GSE289569_author_deseq2_results.csv` for reference.
  - No values were changed.
- `case_spec.json` was then run with `python -m tools.case_runner execute`:
  - **Alignment:** exact match on a key derived from the GEO title. 12/12 samples aligned; groups are geno WT/KO × train SED/TR, n=3 per cell.
  - **Matrix:** FPKM. The paper used DESeq2 on tximport counts, but no counts are deposited, so the paper route is blocked. The declared deviation is limma-trend on log2(FPKM+1).
  - **Model:** one joint limma cell-means model (`~ 0 + C(cell)`) on all 12 samples, with no blocking because the mice are independent.
  - **Contrasts:**
    - Train vs Sed within WT: primary exercise estimand.
    - Train vs Sed within KO: secondary.
    - KO vs WT within Sed and within Train: secondary; these are the paper's reported results.
    - geno×train interaction: exploratory.
- **Threshold:** the paper's rule, FDR ≤ 0.05 and |FC| ≥ 1.2, i.e. |log2FC| ≥ 0.2630344, inclusive (S4.13.p2). It was applied to limma BH-adjusted p and logFC (`paper_on_deviation_route`).
- **Enrichment:** run on the WT Train-vs-Sed table. GSEA Hallmark completed; ORA was not run because there were 0 DEGs.

## DEG counts vs paper (paper threshold)
| Contrast | Ours (up/down) | Paper / authors' deposited DESeq2 | Notes |
|---|---|---|---|
| Train vs Sed, WT (primary exercise) | 0 (0/0); min padj 0.104 | 51 (39/12), from the deposited table only | Paper text gives no count. Sign agrees on 100% of the reference DEGs. |
| Train vs Sed, KO | 0 (0/0); min padj 0.109 | 128 (73/55), from the deposited table only | logFC r=0.94 on the reference DEGs; sign agrees on 100%. |
| KO vs WT, Sed | 402 (225/177) | 709 (421/288), stated in S2.4.p1 | 370 of our 402 are reference DEGs; sign agrees on 100%. |
| KO vs WT, Train | 716 (380/336) | 1122 (616/506), stated in S2.4.p1 / FIG4B | 658 of our 716 are reference DEGs; logFC r=0.87 on the reference DEGs. |
| Interaction (exploratory) | 0 | not reported | |

- Recomputing the authors' deposited padj/log2FC at the paper threshold reproduces the text's 421/288 and 616/506 exactly. That is why the deposited Train-Sed counts are used as the paper reference for the exercise contrasts.
- Named NMJ genes reach significance in our KO-vs-WT results:
  - Musk, Chrna4 and Wnt16 are up in both Sed and Train.
  - Fgfbp1 is up in Sed.
  - Vegfa and Chrna2 do not reach padj ≤ 0.05.
- Exercise result: limma on FPKM finds no training DEGs at FDR 0.05 in either genotype with n=3, although 371 genes in WT and 556 in KO have raw p < 0.01. The authors' count-based DESeq2 gives a small set (51 and 128 genes). Our effect directions agree with theirs, but our test has less power.
- GSEA Hallmark on the WT training effect, kept separate from the DE result:
  - Enriched up: EMT, TGF-beta, myogenesis.
  - Enriched down: xenobiotic metabolism, ROS pathway, coagulation (FDR < 0.03).

## Deviations
- Method: limma-trend on log2(FPKM+1) instead of DESeq2 on tximport counts, because only FPKM was deposited. This is the main reason our counts are lower than the paper's.
- The exercise contrasts' reference counts come from the GEO-deposited author table, not the paper text. The paper only reports KO-vs-WT counts.
- No extra low-expression filter was applied. The deposited matrix already holds 17,752 genes, each expressed in at least one sample.
- A prep script decoded the matrix column names so they could be aligned exactly with the GEO titles. Alignment was by name, not by position.

## Tool problems
- `tools/case_runner.py:838-843` (`_finish`): for a joint execution, `n_deg` in `summary.csv` / `finish` comes from the first table whose name starts with the primary execution's name. That table is `geno_KO_vs_WT_train-SED` (402), a secondary contrast, not the primary exercise contrast `train_TR_vs_SED_geno-WT` (0). The contrast roles set in `design.final.contrasts` are ignored.
- `tools/case_runner.py:496-497`: `alignment.key_patterns` cannot recode. When the matrix labels use a different vocabulary from the metadata (WT/S/TR vs Ctrl/Sedentary/Trained), the key cannot be built in the spec, and a prep script had to rename the matrix columns.
- `inspect` treats the 8 deposited DESeq2 result columns (`KO-WT|Sed log2FoldChange`, ...) as samples. It reports n_samples=20, 15,187 missing values, negative minimum values, `candidates: []` and no `alignment_keys`, which hides the fact that the table is a clean 12-sample FPKM matrix.
