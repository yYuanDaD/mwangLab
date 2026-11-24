# HANDBACK: PMID28066330 / GSE87748

**Status: finished** (decision `valid`, execution `completed`, route `declared_deviation`, validator: 12 records, 0 errors)

## What ran
- Paper (PMC5179501): 10 sedentary young men. Vastus lateralis biopsies were taken at rest and 4 h after a 15-min cycling bout at 80% VO2max (S2.1.p1). Total RNA-seq, featureCounts, genes with > 2.5 RPKM in ≥ 5 samples, edgeR glmQLFit/glmQLFTest (S2.3.p1). Result: 165 DEGs (72 up, 93 down) out of 6,242 genes; NR4A3 was the top up gene at 26-fold (S3.1.p1, Table 1). The paper cites the SuperSeries GSE87749. GSE87748 is its RNA-seq SubSeries.
- Matrix: `GSE87748_RNAseq_Readcoverage_v3.txt.gz`, integer featureCounts counts, 57,820 genes × 20 samples. Matched to metadata by exact `title`, 20/20. `subject` and `time` (Pre/Post) were parsed from the title.
- Gene universe: the RPKM filter needs exon lengths, which were not deposited. I restricted the matrix to the authors' own 6,242 tested genes from `GSE87748_RNAseq_stats.txt.gz` (script: `prep/restrict_to_paper_universe.py`). Counts are unchanged.
- Primary: R edgeR QL F-test with TMM, `~ subject + time`, coefficient `timePost` (`tools.r_de_tools:run_r_de`, engine `edger_ql`).
- Sensitivity runs: edgeR QL unpaired (`~ time`) and pydeseq2 paired (`~ subject + time`).
- Enrichment: not run. The paper reports no pathway analysis.

## Threshold
The paper's text never states the DEG cutoff. In the authors' deposited table, FDR < 0.1 gives exactly **165 (72 up / 93 down)**, which matches S3.1.p1. FDR < 0.05 gives 141. Table 1 also includes METTL7B at FDR 0.080. I therefore applied **FDR (BH) < 0.1 with no fold-change cutoff** as the paper's rule. This is inferred, not stated. FDR < 0.05 is kept as the audit rule.

## DEG counts vs paper (FDR < 0.1)
| Table | Ours (up/down) | Audit FDR<0.05 | Paper | Overlap with authors' 165 | logFC r vs authors |
|---|---|---|---|---|---|
| edgeR paired (primary) | 418 (205/213) | 277 | 165 (72/93) | 162/165 | 0.992 |
| edgeR unpaired | 257 (118/139) | 181 | — | 151/165 | 0.981 |
| DESeq2 paired | 559 (279/280) | 431 | — | 165/165 | 0.985 |

- All 10 genes in Table 1 go up in our primary table. NR4A3: log2FC 5.01 (≈ 32-fold vs the paper's 26), FDR 0.0024. PRKAG2: 2.60 (authors' 2.605). The other 7 found genes all have FDR < 0.001. METTL7B (ENSG00000170439) is also up: log2FC 1.52, FDR 0.049. It shows as `null` in the runner's gene check only because of the lookup problem described under Tool problems.
- Effect sizes match the authors' closely, and nearly all of their 165 genes are recovered. Our p-values are more significant across the board: the median log10 p ratio is about 1.8, which is why we get 418 genes instead of 165. The paired fit matches the authors' logFC best. Their exact model is not known; the likely causes of the gap are edgeR 3.12.1 vs 4.x QL dispersion and prior-df handling, and possibly an unstated difference in the design.

## Deviations
1. Gene filter: the authors' 6,242 tested genes were used instead of recomputing > 2.5 RPKM in ≥ 5 samples, because no exon lengths were deposited.
2. Pairing by subject is assumed. The paper does not state it; the unpaired fit is reported as a sensitivity run.
3. The FDR < 0.1 threshold was inferred from the authors' deposited table.
4. Software: edgeR 4.x under R 4.6, vs the paper's v3.12.1.

## Tool problems
- `tools/case_runner.py:483` (`_gene_lookup`): Ensembl-indexed tables are mapped through MyGene's *current* symbols. A gene renamed since the paper (METTL7B → TMT1B) therefore comes back `null` even though it is in the table. It should fall back to alias/previous symbols, or to a gene-name column in the deposited files.
- The `Bash` heredoc for writing the spec JSON failed with an "unexpected EOF" quote error, probably because of the apostrophes in the text. This was an environment issue, not a repository tool problem; I used the file writer instead.
- The runner itself had no problems: no `spec_error` and no case errors.
