# HANDBACK: PMID33598660 / GSE117161

## What ran
- Paper: STAR Protocols method paper (PMC7868630). It names GSE117161 as the transcriptome data of the companion study Ezagouri et al. 2019 (TAB1, S7.3.p2). It reports **no DE method, no threshold, and no DEG counts or genes**.
- Data: one raw-count matrix (STAR gene counts, 14,038 genes x 18 samples), gastrocnemius, male C57BL/6. Six cells (Basal/Moderate/High running x ZT14/ZT22), n=3 each. Samples aligned exactly on `title`, 18/18.
- Prep: `prep/fix_excel_genes.py` fixed Excel-mangled symbols (19 `Mar-0N`/`Sep-0N` renamed to `MarchfN`/`SeptinN`). It dropped 4 ambiguous duplicated rows, `Mar-01` x2 and `Mar-02` x2: each pair is March1/2 vs Marc1/2, and the file cannot tell which is which.
- Route: case spec. One DESeq2 (pydeseq2 Wald) cell-means model on all 18 samples, run through `tools.joint_contrasts:run_joint_deseq2`. No blocking: animals are independent and no batch is recorded. Sex check passed (all male).
- Planned (paper_aligned): Moderate run vs Basal (sedentary) within ZT14 and within ZT22. This is the protocol's running-vs-sedentary dissection (S3.3.p2) at the two ZTs it compares (S4.p1).
- Exploratory: all 11 analyzable comparisons. These cover High vs Basal, Moderate vs High, and time of day (ZT22 vs ZT14) within each protocol.
- Enrichment: not run, because the paper reports no pathway results.
- Contract validator: 11 records, 0 errors.

## DEG counts (threshold: workflow_default, BH padj < 0.05, no FC rule. The paper states no threshold.)
| Contrast | DEGs (up/down) | audit padj<0.05 and abs(log2FC)>1 | Paper |
|---|---|---|---|
| Moderate vs Basal, ZT14 | 734 (425/309) | 93 | not reported |
| Moderate vs Basal, ZT22 | 533 (337/196) | 92 | not reported |

Exploratory: High vs Basal gave 86 DEGs at ZT14 and 183 at ZT22. ZT22 vs ZT14 gave 705 in Basal, 433 in Moderate and 612 in High.

Sanity check: exercise-response genes go up with the moderate run at both ZTs. Nr4a3 log2FC is 3.4 at ZT14 and 3.0 at ZT22; Hspa1a is 2.7 and 3.0; Atf3 is 1.6 and 1.4. Ppargc1a is up only at ZT14 (0.61, padj 3e-5); at ZT22 it is 0.12 and not significant. Per1 rises strongly at ZT22 only. There are no paper results, so nothing contradicts the paper.

## Deviations and caveats
- The paper has no DE results, so there is no quantitative comparison with the paper. Because no method was stated, the method used (DESeq2) is the workflow's standard raw-count route.
- **Duration mismatch.** GEO says the moderate arm ran for 1 h at a final speed of 20 cm/s. The protocol describes 22-25 cm/s until fatigue, which takes several hours. The data show a 1 h bout, not run-to-fatigue.
- **Control timing unknown.** GEO does not record when the Basal controls were sacrificed relative to the run, and S3.3.p2 allows either option. Elapsed-time effects therefore cannot be separated from the exercise effect.
- n = 3 per cell.
- The High arm is outside this protocol's moderate-intensity scope, so it is exploratory only.

## Tool problems
- None blocking.
- Minor: `inspect` flags `excel_date_ids` and duplicated IDs but leaves the repair to a manual prep script. The ambiguous Mar-01/Mar-02 rows could not be resolved.
- Minor: `comparisons: "all"` recomputes and re-writes the planned contrasts under `exploratory/` (identical counts), which duplicates tables.
- Session-level: a Git Bash heredoc that held the spec JSON failed with "unexpected EOF". This is a harness issue, not a repo issue. I wrote the spec with the file tool instead.
