# HANDBACK: GSE217155 (PMC9807753, aerobic exercise in Ath-diet NASH mice)

Status: finished. Validator: 14 records, 0 errors. Route: paper_aligned.

## What ran
- `case_runner inspect GSE217155`. It downloaded the series and merged the RAW tar into 17846 genes x **8** samples. The metadata lists 9 samples.
- `prep/build_counts.py` rebuilds the matrix with all 9 samples:
  - It takes the `read_count_*` columns, which hold RSEM expected counts.
  - It checks that the 8 single-sample files are identical to the combined file (max abs diff 0).
  - It renames the columns to GSM ids using the metadata `title`.
  - It maps Entrez IDs to MGI symbols with MyGene: 17740 of 17846 mapped. Unmapped IDs keep their Entrez ID, and no symbols were duplicated.
  - Output: `prep/GSE217155_read_count_symbols.csv`.
- `case_runner execute case_spec.json`:
  - Matrix: estimated counts, rounded.
  - Model: one pydeseq2 model `~ grp` on all 9 samples (CON/NASH/EXE, 3 each), using `tools.joint_contrasts:run_joint_deseq2`.
  - Planned contrasts:
    - EXE vs NASH (primary: exercise effect within the Ath diet).
    - NASH vs CON (secondary: diet check).
  - Not run: EXE vs CON, because it confounds diet with exercise.
- Enrichment:
  - ORA (Enrichr GO and KEGG) on the up and down DEGs of EXE vs NASH.
  - Hallmark GSEA (ranked by stat) for both contrasts.

## DEG counts vs paper
Threshold is the paper's own (S2.6.p1): padj < 0.05 and |log2FC| > 1.

| Contrast | Ours (up/down) | Paper (up/down) | Audit padj<0.05 only |
|---|---|---|---|
| EXE vs NASH | 188 (68/120) | 204 (79/125), S3.2.p1 | 336 |
| NASH vs CON | 2577 (2099/478) | no count reported | 5146 |

Paper genes for EXE vs NASH:
- Dio1: log2FC +1.95, padj 2e-4. Up and significant, as the paper reports.
- Il1b (-0.28), Tnf (-0.75) and Adgre1/F4/80 (-0.36): all lower after exercise, matching the direction of the paper's qPCR, but none is significant here. The paper's qPCR used more mice.

Hallmark GSEA directions all match the paper (S3.2.p3):
- EXE vs NASH:
  - Negative: INFLAMMATORY (NES -2.28), IFNG (-2.14), IFNA (-1.96), IL6_JAK_STAT3 (-1.81), TNFA_NFKB (-1.78), TGF_BETA (-1.40, q=0.028).
  - Positive: OXPHOS (+3.03).
- NASH vs CON:
  - Positive: the inflammatory and IFN sets (NES +2.25 to +2.52).
  - Negative: OXPHOS (-3.38).

## Deviations
- Sample size: GEO has 3 mice per group, while the paper randomized 8 per group (S2.1.p1). The paper does not say how many mice were sequenced.
- RSEM expected counts were rounded to integers for DESeq2 (pydeseq2, not R DESeq2).
- The paper used DAVID for GO; we used Enrichr ORA.
- The paper's own T3-signature GSEA/GSVA and its T3 RRA meta-analysis of other GEO series (S2.7) were not reproduced.

## Tool problems
- `tools/geo_tar.py:111-114`: the tar member `GSM6705777_musNASH5.txt.gz` holds fpkm/tpm/read_count columns for **all nine** samples. `choose_count_column` cannot pick one column from it, so the member is skipped and sample NASH5 is dropped, leaving 8 of 9 samples. The `WARNING: skipped` line (`tools/geo_tar.py:124-127`) only goes to the log. The `inspect` JSON `notes` say only "merged ... 17846 genes x 8 samples" and do not say a sample was dropped. A multi-sample member should be either expanded or surfaced as a dropped sample in `inspect` (`tools/case_runner.py` inspect_series, near line 333). Worked around with a prep script.
- Feature IDs are Entrez gene IDs. Without mapping them to symbols, enrichment would have recorded `not_run`, because the runner accepts only symbols or Ensembl IDs. Symbol mapping was done in the prep script.
- Bash heredoc spec writing failed in this shell; I used the Write tool instead. This is an environment issue, not a repository bug.
