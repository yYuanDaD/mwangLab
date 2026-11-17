# HANDBACK: PMID 38157298 / GSE245760

Run directory: `test/experiments/large_run_pilot_20261019/runs_claude/PMID38157298`
Decision maker: Claude Opus 5.5 (Claude Code session), case-spec route (`tools.case_runner`).
Final status: **completed**, route `declared_deviation`. The decision-contract validator found 0 errors in 18 records.

## Study map (from the paper)
- 2x2 factorial in male C57BL/6 mice: WT vs CHCHD4 Tg (overexpression) x no training vs 4 weeks treadmill training. n = 4 per group, 16 samples. Muscle is tibialis anterior per the FIG1C legend; GEO says "skeletal muscles".
- Exercise estimand: trained vs untrained **within WT** (Table S4) and **within Tg** (Table S5) (S2.7.p5). The Tg vs WT contrasts (Tables S1-S3, FIG1C) are genotype effects, so I did not run them.
- Paper method: STAR/RSEM expected counts, then edgeR exactTest (S4.3.8.p1).
- Paper threshold: **none stated** for DEGs. FIG1C draws a p = 0.01 line on the Tg/WT volcano for display only.
- The paper's DEG counts are in supplementary Tables S4/S5, which are not in hand, so there is no DEG count to compare.

## What ran
- Input prep: `prep/prep_matrix.py` renamed the rows from `ENSMUSG.ver_Symbol` to the symbol. Symbols shared by several genes became `Symbol_ENSMUSG`; no values changed and no rows were summed.
- Alignment: exact match of GEO `description` (A1..D4) against the matrix column prefix; 16/16 samples aligned. The Tg labels are confirmed by Chchd4 at about 2.7x in B/D vs A/C.
- Matrix: RSEM estimated counts (87.5% integer, library sizes 41-62 M), rounded to integers (`rounding_documented`).
- Suitability: analyzable. Sex check passes (all male, consistent with S4.2.1.p1).
- Executions (BH padj < 0.05 is the applied rule; audit rule is raw p < 0.01; neither has a fold-change cutoff):

| Table | Role | DEGs padj<0.05 (up/down) | audit p<0.01 | Paper |
|---|---|---|---|---|
| edgeR_WT_EX_vs_SED (QL F-test, 8 WT samples) | primary | 17 (12/5) | 314 | Table S4, count n/a |
| edgeR_TG_EX_vs_SED (8 Tg samples) | secondary | 510 (124/386) | 1550 | Table S5, count n/a |
| DESeq2_WT_EX_vs_SED | sensitivity | 55 (27/28) | 310 | - |
| DESeq2_TG_EX_vs_SED | sensitivity | 635 (230/405) | 1217 | - |
| limma interaction (log2CPM, (WT_EX-WT_SED)-(TG_EX-TG_SED)) | exploratory | 8 (7/1) | 172 | not tested in paper |

- Named genes in WT trained vs untrained (edgeR). All are up, matching the paper's direction, but none reaches padj < 0.05:
  - mt-Nd3 +0.48
  - Atp1a3 +1.14 (p 0.07)
  - Rrad +0.90 (p 0.06)
  - Plac8 +0.73
  - Cidea +1.49 (p 0.0014)
  - Myh7 +1.16
- Named genes in Tg: mt-Nd3, Atp1a3, Rrad, Plac8 and Cidea show no meaningful change, consistent with "not in Tg".
  - Exception: Myh7 is log2FC -3.87 (padj 0.009) in Tg. Myh7 is barely expressed in this fast muscle (CPM about 1-3). Two untrained Tg samples (D2, D3) are outliers at 65 and 46 CPM and drive this result. It does not contradict the paper ("no increase in Tg"), but it is not robust.
- WT training signal is weak. The top hits are mostly predicted Gm genes and histone genes (Gm17167, Gm13301, Hist1h4m). The Tg training response is much larger (510 DEGs).
- Enrichment, kept separate from the DE result:
  - GSEA Hallmark: OXIDATIVE_PHOSPHORYLATION is up with training in both genotypes (WT NES 2.36, Tg NES 3.49; FDR about 0).
  - ORA in WT gives only 2 weak GO BP terms (purine catabolism).
  - ORA in Tg gives angiogenesis-regulation terms.
  - The paper's FIG S4B (muscle-contraction GO terms) concerns the Tg vs WT contrast in trained mice. That contrast was not run, so it was not compared.

## Deviations
1. edgeR glmQLFTest instead of exactTest. The repository has no exactTest executor (`tools/edger_tools.py:125`).
2. Estimated counts rounded before edgeR. The paper probably fed the RSEM expected counts to edgeR without rounding.
3. No low-count filter. The paper states none; the executor drops only all-zero genes.
4. The applied threshold is the workflow default (padj < 0.05) because the paper states none.

## Tool problems
- `tools/edger_tools.py:106`: `counts_sub.astype(int)` **truncates** non-integer counts instead of rounding them. It did not affect this run because the case-level `round` transform ran first. A direct call on RSEM counts would silently floor them.
- `tools/edger_tools.py:123-125`: only the QL GLM route exists, with no `exactTest` option. There is also no low-count filtering inside the executor, so tagwise dispersion runs on all ~40k nonzero genes. Each 8-sample edgeR call took about 5 minutes, and the full execute took about 25 minutes.
- `tools/case_runner.py:405` (inspect): `ENSMUSG.ver_Symbol` row IDs are typed as `other`, so enrichment would be refused without a prep script. A `feature_id_pattern` option, or Ensembl-prefix detection, would remove the need for the script.
- pydeseq2 prints `RuntimeWarning: overflow encountered in exp` (pydeseq2/utils.py:1088). The warnings are harmless.
