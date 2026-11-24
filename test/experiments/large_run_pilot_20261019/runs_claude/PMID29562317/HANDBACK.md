# HANDBACK — PMID29562317 / GSE102284

**Status: finished** (case-spec route, validator 18 records, 0 errors). Route: `declared_deviation`.

## Estimand and the exercise question
The study has no exercise-training arm. The activity manipulation is 10 days of hind limb unloading (disuse, UN), then 10 days of unloading plus 3 days of reloading with voluntary cage ambulation (RL), compared with cage controls (CON), in adult (6 months, Y) and old (22–24 months, O) male mice; tissue is soleus (S1.1.p1, S2.1.p1). The paper intends a disuse/reloading analysis, so it was run with that label rather than refused. The caveat is in `study.caveats`: results describe disuse and early reloading, not exercise. RL vs UN, the effect of resuming loading and ambulation, was run as exploratory.

## What ran
- Matrix: deposited `GSE102284_Expression_profiling_analysis-Coen.csv`, `(Reads)` columns only. These are Partek E/M estimated counts on RefSeq transcripts, about 52% integers and about 35 M per library. They were summed to gene symbol (`feature_column: Gene`, sum; 21,154 genes), rounded, and filtered at CPM ≥ 1 in ≥ 4 samples, leaving 13,146 genes.
- Alignment: the key was derived from the title (`Y_C_1` matched to `YC_1`, normalized). 36 of 36 samples aligned exactly. Groups: YC 9, YU 4, YR 4, OC 9, OU 6, OR 4.
- Model: one pydeseq2 model on all 36 samples, cells age × cond (`tools.joint_contrasts:run_joint_deseq2`). The planned contrasts were UN vs CON and RL vs CON within each age. RL vs UN within each age was exploratory.
- Enrichment: ORA on down-regulated genes (Enrichr GO and KEGG) and Hallmark GSEA for the 4 planned contrasts.

## DEG counts (applied = paper rule: raw p < 0.05, no FC cutoff, FIG4B legend; audit = BH FDR < 0.05)
| contrast | n (p<0.05) | up | down | audit FDR<0.05 | paper |
|---|---|---|---|---|---|
| UN vs CON, adult | 6799 | 3343 | 3456 | 6029 | not reported |
| RL vs CON, adult | 7763 | 4059 | 3704 | 7109 | not reported |
| UN vs CON, old | 7098 | 3541 | 3557 | 6375 | not reported |
| RL vs CON, old | 6822 | 3435 | 3387 | 6043 | not reported |
| RL vs UN, adult (exploratory) | 7559 | 3933 | 3626 | 6902 | — |
| RL vs UN, old (exploratory) | 7842 | 4027 | 3815 | 7279 | — |

The paper gives no DEG counts. Comparison with the paper is qualitative and agrees with it:
- KEGG oxidative phosphorylation, TCA cycle and fatty acid degradation are enriched among down-regulated genes in all 4 planned contrasts (adjusted p from 1e-38 to 1e-2). Hallmark OXPHOS NES is between −3.2 and −3.5 (FDR 0). Both match FIG4A: down with UN and still down after RL.
- Ppargc1a, Esrra and Esrrg are down in all four contrasts (log2FC −0.36 to −2.08, all p < 0.05), with no recovery at RL. This matches FIG4C.
- Adult and old responses are similar, as S2.4.p2 says. In PCA, PC1 separates reloading and PC2 separates unloading, with age on PC3.

About 52% of filtered genes pass p < 0.05. The runner flags this (`deg_sanity: implausible_sig_fraction`). I checked it: within-group sample correlations are about 0.99 and samples cluster cleanly by condition, so this is a real, very large unloading/reloading effect with tight groups, not a mapping error. However, condition could be confounded with processing batch, and GEO records no batch information to test this.

## Deviations (declared)
1. DESeq2 (pydeseq2) instead of the original DESeq named in GEO `data_processing`. The paper route is blocked because original DESeq is not available and the supplementary methods are unavailable.
2. Analysis at gene level (summed transcripts) instead of Partek transcript level.
3. Estimated counts rounded.
4. The paper's "RPKM > 1" filter is approximated by CPM ≥ 1 in ≥ 4 samples on the read counts.
5. One joint model is used; the paper's per-comparison fitting is unknown.

## Tool problems
- Not a bug: `deg_sanity` (`tools/case_runner.py`, finish summary) reports only the first table's fraction (6799/13141) as a single case-level flag. It cannot be told that the effect is real.
- The low-count filter cannot use the deposited `(RPKM)` columns while the `(Reads)` columns are analyzed: `filter_low_counts` acts only on the analyzed matrix (`tools/case_runner.py`, `matrix_column_pattern` keeps one column kind). The paper's RPKM > 1 rule therefore had to be approximated.
- Minor: when the deposited CSV is read, pandas raises a DtypeWarning on the mixed-type `Chromosome` column. It is harmless.
- None blocking.
