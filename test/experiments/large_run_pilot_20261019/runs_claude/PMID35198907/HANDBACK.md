# HANDBACK: PMID35198907 / GSE194193

Paper: intravenous nicotinamide riboside (NR) x pterostilbene (PT) x voluntary wheel running (VWR), 2^3 factorial, male C57BL/6NTac mice on western diet, quadriceps mRNA-seq. Exercise factor = 4 weeks of VWR versus sedentary. Wheels were locked before the last dark phase, so this is a chronic training effect, not an acute exercise bout.

## What ran (case-spec route, `case_spec.json`)
- Ownership: GSE194193 is named in the key resources table. 62 samples = 64 mice minus the 2 the paper removed. Alignment: exact match on `title`, 62/62. Cells have 7-8 mice each.
- Matrix: featureCounts raw integer counts (GENCODE vM22, 55,487 genes). This is the paper's own input.
- Method: the paper's route. edgeR quasi-likelihood (QL) GLM in R (edgeR 4.10.7), TMM normalization, `~ 0 + grp + rin`, where grp is the 8 NR x PT x VWR cells and RIN is a continuous covariate (S4.4.10.p3). Low-count filter: filterByExpr, which kept 14,942 genes. The executor was `tools.r_de_tools:run_r_de` (engine edger_ql) with makeContrasts expressions.
- Primary: the VWR main effect, computed as the mean of the 4 VWR cells minus the mean of the 4 SED cells.
- Secondary: the NR and PT main effects from the same model.
- Exploratory: the VWR x NR, VWR x PT and VWR x NR x PT interactions, plus the 4 simple VWR effects.
- Sensitivity: a 4-group model (NR x VWR, PT pooled). The paper says its group variable has "4 (or 8)" levels.
- Threshold: the paper's own rule, FDR q < 0.05 with no fold-change cutoff (S2.6.p1, S2.6.p3).
- Enrichment: GSEA (Hallmark, ranked by log2FC) and Enrichr ORA on the primary table. The paper used camera on GO terms, so this is a substitute.

## DEG counts vs paper (FDR < 0.05)
The paper counts protein-coding genes only. Protein-coding status comes from a post-hoc MyGene `type_of_gene` lookup (scratchpad script, not a recorded gate).

| Contrast | ours, all genes | ours, protein-coding (up/down) | paper (protein-coding) |
|---|---|---|---|
| VWR main, 8-group (primary) | 1980 (1073/907) | 1911 (1032/879) | 2245 |
| VWR main, 4-group (sensitivity) | 2009 (1214/795) | 1937 (1167/770) | 2245 |
| NR main | 3 | 3 | 4 |
| PT main | 0 | 0 | 0 |
| VWR x NR, VWR x PT, 3-way interactions | 0 / 0 / 0 | 0 | none |

The primary count is about 85% of the paper's.

- **Paper VWR genes, all reproduced in direction and significance:** Art3 down (q=0.032; paper 0.019) and Mymk down (q=0.003; paper 0.006). Cd38, Sirt3 and Sirt5 are up (q=1e-4, 1e-4, 0.047). Nampt, Nmrk1 and Nmrk2 are unchanged, as the paper reports.
- **NR main effect, partly reproduced:** Nmrk2 is down (log2FC -1.11, which is about 54% lower; paper about 65%, q<0.001) and Mymk is up (q=0.015). Two paper genes miss the cutoff: Myh8 is up at q=0.053 and Art3 is up at q=0.19.
- **Enrichment agrees with Fig 6J** (top terms up with VWR): OXPHOS is the top Hallmark set (NES 2.06), and the leading GO BP terms are cellular respiration and the electron transport chain.
- **Exploratory simple effects:** VWR effects within single cells are much weaker (0, 62, 2 and 270 DEGs), with n = 7-8 per cell. This is consistent with the paper's finding of no interaction.

## Deviations
- edgeR 4.10.7 instead of 3.30.3.
- The paper states no low-count filter, so filterByExpr is our assumption. This is the most likely cause of the count gap.
- The paper does not state its main-effect contrast weights. We used equal cell weights.
- The paper does not say whether the 4- or 8-group model produced its VWR count. Both were run, and they give similar counts.
- The paper used camera GO enrichment. We used Hallmark GSEA plus ORA instead.

## Tool problems
- `tools/r_de.R:206-207` (edger_ql branch) writes `stat = F`, the QL F statistic, which is unsigned. The runner's default GSEA ranking (`ranking_metric: "stat"`) would therefore produce a meaningless unsigned ranking. We worked around it with `ranking_metric: log2FoldChange`. The same lines label `2^logCPM` as `baseMean`, which is not a mean count.
- Neither the runner nor suitability can express a factorial main effect averaged over the other factors. `joint_contrasts` only has simple effects and interactions. The planned VWR main effect therefore went through the generic R executor, and the main-effect contrast names do not match suitability names, so no `min_group_n` is recorded for them (`tools/case_runner.py:866-867`).
- No gene-biotype support: the paper's protein-coding counts needed an ad hoc MyGene lookup outside the runner.
