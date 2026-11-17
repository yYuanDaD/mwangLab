# HANDBACK — PMID 36481702 (EPS cellular exercise model; GSE176563 + GSE126001)

Route: case spec (`case_spec.json`) run with `python -m tools.case_runner execute`. Run status: completed. Contract validator: 22 records, 0 errors. Preflight skipped as instructed. No enrichment was run, because the paper's pathway work is IPA only and the request asks about gene expression.

## What ran

| Case | Contrast | Role | Method | Threshold (source) | Ours (up/down) | Paper |
|---|---|---|---|---|---|---|
| GSE176563 | EPS (n=4) vs CTRL (n=3), C2C12 myotubes | primary | limma on log2(CPM+1) | raw P < 0.01 and \|log2FC\| > 1 (paper, S2.1.p1/FIG1, applied on the deviation route) | **218** (143/75) | **774** (406/368) |
| GSE176563 | same, audit rule | audit | same | raw P < 0.001 and \|log2FC\| >= 1 (Methods S4.6.p1) | 79 | n/a |
| GSE176563 | same, CPM >= 1 in >= 3 samples (12,360 genes kept) | sensitivity | same | paper rule | 310 (216/94); audit 172 | 774 |
| GSE126001 | WT trained vs untrained (4 vs 4), gastrocnemius | primary | limma on log2(RPKM+1) | BH < 0.05 (workflow_default; the paper gives no DE rule for this public dataset) | 6 (6/0); 11 under the audit rule P < 0.01 and \|log2FC\| > 1 | none reported |
| GSE126001 | Il13-/- trained vs untrained (4 vs 4) | exploratory | same | workflow_default | 3 (2/1) | not used by the paper |

Paper genes in GSE176563: all 17 checked genes move in the paper's direction. Up: Prl2c2, Prl2c3, F13a1, Areg (log2FC 0.85, p 0.029), Cxcl1, Cxcl5, Il1b, Gdf15, Mt1 (+2.08), Mt2 (+2.63) and Atf3. Down: Myh4 (-2.48), Fam78a, Ppapdc3, Chrne, Kctd12 and Il12a. Several of these pass the paper rule, for example Mt1, Mt2, Myh4, Fam78a, Chrne, Kctd12, Il1b and F13a1, as long as their log2FC is above 1. Areg, Cxcl1 and Prl2c2 do not reach p < 0.01. Our log2FC values are much smaller than the paper's edgeR logFC for low-CPM genes: Prl2c2 is 1.34 here against 8.80 in the paper. The cause is the +1 offset on log2(CPM), which compresses low-expression fold changes.

Paper genes in GSE126001 (WT): Myh4 (log2FC -0.26, p 0.007), Il12a (-0.34, p 0.03), Fam78a, Ppapdc3 and Chrne go down, which agrees with the paper's direction. None are significant after BH. Mt1, Mt2 and Kctd12 do not go up as the signature expects: they are flat or slightly the other way. Atf3 is slightly up and not significant. Areg is zero in all 16 samples, so limma's zero-variance filter dropped it. This fits the paper's claim, which was about agreement across at least six datasets and not about GSE126001 alone (S2.2.p2, S3.p2: in long-term chronic exercise only Il12a was consistent).

## Decisions and deviations

1. **GSE176563 holds CPM only.** The per-sample `*_CPM.txt.gz` files are CPM; GEO says "CPM values of mRNA"; every column sums to exactly 1e6. The paper's edgeR negative-binomial test on counts (S4.6.p1) is therefore `blocked`. Counts cannot be recovered from CPM without library sizes, and rounding was not allowed. The declared deviation is limma on log2(CPM+1). The paper's quantile normalization was not applied. This deviation is the most likely main reason for 218 vs 774: limma's moderated variance with n = 3 vs 4 is more conservative than an edgeR exact test, and log2(x+1) shrinks fold changes for low-CPM genes below the |log2FC| > 1 cut.
2. **The paper gives two different thresholds.** Results and FIG1 say "P < 0.01, fold change > 2" (774 DEGs). Methods S4.6.p1 says "P < 0.001 and fold difference >= 2". The Results rule is the one tied to the reported count, so it is the applied paper rule. The Methods rule is the audit rule. Both use raw P, as the paper states, and FC 2 is \|log2FC\| 1.
3. **GSE126001 is a public dataset reused by the paper** (TAB1, S4.9.p1), not the authors' own deposit. The paper ran no DE on it; it used the dataset to test the DBN classifier and to check gene directions. TAB1 describes WT male mice only, so the primary contrast is WT trained vs untrained. Genotype (Il13-/-) is a stratum, and the KO training contrast is exploratory. Pooling the genotypes and fitting the genotype x training interaction were both rejected; the reasons are recorded in the spec. The matrix is CLC RPKM, so the route is log2(x+1) then limma. There is no paper threshold, so the applied rule is the workflow default BH < 0.05.
4. Alignment: GSE176563 matches exactly on GSM ids after the tar merge (7/7). GSE126001 matches exactly on the metadata `mouse id` after `matrix_column_pattern ^(W\d+)_` (16/16). No samples were excluded. Covariance is not required in either case: the samples are independent wells or mice, and no batch is recorded.

## Tool problems

- Minor: `inspect` returned an empty `alignment_keys` for GSE126001. `_contained_keys` (tools/case_runner.py:332-354) only finds metadata text that contains a matrix column name. It misses the reverse case, where a matrix column name such as `W100_S25_R1_001 trimmed (GE) - RPKM` contains a metadata value (`mouse id` = W100). I found the key by hand. A hint pointing to `matrix_column_pattern` would help.
- No executor failures. One expected behaviour to know about: limma drops all-zero genes, so `paper_gene_check` reports `null` for Areg in GSE126001. This is correct, but the null does not say why the gene is missing.

## Files

- Spec: `case_spec.json`. Log: `case_runner.log`. Summary: `summary.csv`.
- Results: `GSE176563/results/grp_EPS_vs_CTRL*/DEG_results_EPS_vs_CTRL.csv` and `GSE126001/results/train_TR_vs_UT_geno-*/DEG_results_TR_vs_UT.csv`.
- Suitability reports: `<GSE>/suitability/suitability.md`.
