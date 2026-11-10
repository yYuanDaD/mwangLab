# HANDBACK: PMID38766755 / GSE263838

Status: finished (case route `paper_aligned`, validator 13 records, 0 errors).

## What ran
- Case-spec route (`python -m tools.case_runner execute case_spec.json`), preflight skipped as instructed.
- Matrix: `GSE263838_GeneCounts_RAW_DATA.csv.gz` (Kallisto gene counts deposited as integers, 40,514 genes x 38 samples), filtered with `prep/filter_mean10.py` to genes with mean count >= 10. This keeps **15,543 genes, the exact number in the paper** (S2.8.p1).
- Alignment: exact match on GEO `title` (38/38). The participant key is the 4-letter title prefix (10 women; SASY has only SR-D3 and NS-D9). `cond` (NS/SR) and `day` (D3/D9) come from the characteristics columns. `grp` = cond_day.
- Design: 2x2 cross-over with repeated measures. All pre-exercise biopsies go into one model. The exercise estimand is pre-exercise day 9 vs pre-exercise day 3 within each sleep condition. This is a training/time effect of three REx sessions measured 48 h after the last one, not an acute response.
- Primary: joint DESeq2 (pydeseq2) `~ subject + grp`, with 4 planned simple effects plus the exploratory cond x day interaction.
- Sensitivity: joint DESeq2 `~ grp` (unblocked). The paper does not state its formula.
- GSEA (Hallmark, ranked by log2FC as in the paper) on both exercise contrasts of the blocked fit.

## DEG counts vs paper
Paper threshold (Methods S2.8.p1) = padj < 0.05 and |log2FC| > 1; audit = padj < 0.05 only.

| Contrast | Paper | Blocked, paper rule | Blocked, FDR only | Unblocked, paper rule | Unblocked, FDR only |
|---|---|---|---|---|---|
| NS D9 vs D3 (exercise) | 2962 (128 "up" / 2834 "down") | 1061 | 4003 | 1136 | **2965** |
| SR D9 vs D3 (exercise) | 2219 (102 / 2117) | 777 | 2943 | 807 | **2224** |
| SR vs NS, day 3 | 1 (GGNBP2) | 1 (GGNBP2) | 1 | 1 | 1 |
| SR vs NS, day 9 | 0 | 0 | 0 | 0 | 0 |
| cond x day interaction (exploratory) | not tested | 0 | 0 | - | - |

- The paper's totals are reproduced almost exactly by the **unblocked, FDR-only** fit. The paper therefore counted at FDR < 0.05 only, as its Results say, not with its Methods |log2FC| > 1 rule, and it did not block on participant. Our primary (blocked, paper rule) gives fewer DEGs.
- The paper's up/down split is not a sign split. Its "up" (128 / 102) matches our padj < 0.05 with log2FC(D9/D3) < -1 (130 / 102). Its "down" matches the remaining FDR genes (2835 / 2122). Our real FDR-only sign split for D9 vs D3 is 1964 up / 1001 down (NS) and 1346 / 878 (SR).
- **Direction contradicts the paper's text** (recorded in the study caveats):
  - The paper says oxidative metabolism goes up with training and the cell cycle goes down. Our D9 vs D3 results have HALLMARK_OXIDATIVE_PHOSPHORYLATION NES -2.57 (NS) / -2.58 (SR), and E2F/G2M NES +2.1 to +2.3.
  - The paper calls GGNBP2 upregulated by SR. Our log2FC(SR/NS) is -2.27.
  - Both fit the paper writing its contrasts as reference over test (NS3_vs_NS9, NS3_vs_SR3), so its stated directions look sign-reversed.

## Deviations
- Participant blocking was added in the primary fit, because the paper's formula is unstated; the unblocked fit runs as a sensitivity analysis.
- pydeseq2 was used instead of R DESeq2.
- GSEA uses MSigDB Hallmark instead of Reactome through fgsea.
- The paper's mean-count filter was applied by a prep script, not by the runner.
- The counts are rounded Kallisto estimates as deposited; `rounding_documented`, no further rounding.

## Tool problems
- The runner's `filter_low_counts` (tools/case_runner.py:668) only supports "CPM >= x in >= n samples". It cannot express the paper's "mean count >= 10" filter, so a prep script was needed.
- The paper-vs-ours comparison (tools/case_runner.py:846) uses only the applied-threshold count of the named table. The audit count and the sensitivity tables are not compared, and in this case those were what matched the paper.
- inspect reports the long-format `GSE263838_3col.tsv.gz` as a matrix error (tools/analysis_policy.py:46) instead of identifying it as a long-format copy. This is harmless.
