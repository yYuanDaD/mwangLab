# HANDBACK: PMID33513138 / GSE152347

STATUS: finished (route `declared_deviation`; validator 15 records, 0 errors; suitability `analyzable`)

## What ran
- Case-spec route (`tools.case_runner execute case_spec.json`). Preflight was skipped as instructed. No external LLM calls were made.
- Data: GSE152347 is the RNA-seq SubSeries of the paper's SuperSeries GSE152349 (S4.16.p1). The matrix is featureCounts raw fragment counts (52,636 GENCODE vM15 genes x 25 soleus samples). Alignment: exact match on the title minus `_RNA-seq`, 25/25 samples.
- Design (S4.3.p1, S4.17.p1): 12-week-old male and female WT and mD3AKO mice, at rest (`Bas`) or 60 min after a 30-min treadmill run (`60`). Cells: WT rest 5, WT ex60 7, KO rest 7, KO ex60 6. Independent animals, so no blocking term. Sex is an additive covariate, crossed with every cell. The X/Y sex check passed.
- Executions (DESeq2/pydeseq2):
  - **primary** `exercise_main`: `~ sex + geno + time`, ex60 vs rest (the paper's exercise main effect).
  - secondary `genotype_main`: KO vs WT with `~ sex + time + geno`.
  - secondary `joint`: cell-means `~ sex + cell` giving per-genotype exercise effects, genotype within time, and the genotype x exercise interaction.
  - sensitivity `exercise_main_cpmfilter`: CPM >= 1 in >= 3 samples.
  - exploratory `exercise_male` and `exercise_female` (`~ geno + time` within each sex).
- Threshold: paper rule, FDR < 0.05 with no fold-change cutoff (S4.17.p1, S2.2.p2). `threshold_source: paper`.
- No enrichment was run. The paper's only GO analysis is on the genotype DEGs (Fig 7F), and the request does not ask for pathways.

## DEG counts vs the paper (padj < 0.05, no FC cutoff)
| Table | Ours (up/down) | Paper |
|---|---|---|
| exercise_main (primary) | 2232 (1144/1088) | 1615 |
| genotype_main | 130 (89/41) | 56 (43 up / 13 down) |
| joint interaction time x geno | 0 | 0 |
| exercise_main_cpmfilter (sensitivity) | 2015 (999/1016) | 1615 |
| joint ex60 vs rest within WT / within KO | 859 / 1352 | not reported |
| exercise_male / exercise_female (exploratory) | 1350 / 752 | not reported |

The paper's named exercise genes all rise strongly in the primary table, in the paper's direction:
- Nr4a3: log2FC 3.16, padj 1e-31
- Ppargc1a: log2FC 1.11, padj 6e-19
- Hk2: log2FC 0.53, padj 2e-14
- Atf3: log2FC 3.98 (about 16-fold; the paper says about 15-fold), padj 2e-16

There is no genotype x exercise interaction, as in the paper. The direction of the result is reproduced, but the exercise and genotype DEG counts are higher than the paper's (+38% and 2.3x).

## Deviations (declared)
- **DE package:** the article does not name it ("processed as previously described [34]", S4.11.p1). DESeq2 was used with the paper's model structure (main effects plus interaction). If the paper used edgeR, its test may be more conservative, which could explain the higher counts.
- **Sex covariate:** added because sex separates the samples on the MDS plot (S2.2.p3). The article does not say whether its RNA-seq model included sex.
- **Expression filter:** the paper keeps 17,389 genes (S4.9.p1) but does not state the rule. The primary run uses DESeq2 independent filtering. The CPM >= 1 in >= 3 samples sensitivity run keeps 13,504 genes and finds 2,015 exercise DEGs.
- **Per-sex runs are exploratory:** the female WT rest cell has only n = 2.

## Tool problems
1. `tools/case_runner.py:825-828`: when `covariate_columns` is a comma string, the execution record writes the formula literally as `"~ sex,geno + time"`. The string is not split on commas. This is only cosmetic, because `tools/deseq2_tools.py:108-117` does split it and fits sex + geno + time.
2. `tools/case_runner.py:638-644`: the covariance `design_check` is built only from `design.factors` plus the blocking terms. It leaves out the included covariates, so it reports `formula_equivalent: ~ C(time) + C(geno)` without `sex`. Rank and df for the fitted model, which includes sex, are not checked.
3. Suitability (`tools/suitability.py`, comparison enumeration) lists only cell-level and interaction comparisons, not factorial main effects. Because of this, the paper's planned main-effect name `time_ex60_vs_rest` gave `planned names not found` and a `partially_analyzable` warning on the first attempt. The workaround was to list the interaction as the planned name; the first attempt is in `_previous/`.
4. On Windows, pydeseq2/joblib print a loky worker traceback at shutdown (`OSError: [WinError 6]` in `loky/process_executor.py:477`). It is harmless (exit 0, all outputs written) but looks like a crash in stderr.
