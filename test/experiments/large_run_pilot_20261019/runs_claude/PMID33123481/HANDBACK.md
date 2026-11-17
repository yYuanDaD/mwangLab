# HANDBACK: PMID 33123481 / GSE150620

Status: **finished** (decision `valid`, execution `completed`, route `declared_deviation`; contract validator: 14 records, 0 errors).

## What the paper does with GSE150620
A perspective article. Its only analysis of GSE150620 is S3.p6 and FIG1 C. Mice ran on wheels for 2 weeks before EO771 engraftment, and their mammary tissue showed less expression of a Buffa et al. hypoxia gene set than sedentary controls (transcriptome representation analysis, P = 0.003). The paper reports **no gene-level DEG count, no DE threshold and no n**. It also never mentions that GEO holds a 2x2 design: activity (Control/Wheel) x liposome (PBS/Clodronate), with 6/6/5/5 mice.

## What ran
- Inspect, then `prep_merge_cpm.py`, which rebuilds the matrix from the 22 per-sample CPM files. Columns become GSM IDs. For duplicated symbols the row with the highest mean is kept, and 4 duplicated Excel-date IDs are dropped. Output: 52,528 genes x 22 samples.
- Matrix: linear CPM floored at 1. GEO data_processing says CPM; column sums are about 1.037e6. Transformed with log2(x+1). No raw counts were deposited, so count models do not apply.
- One limma cell-means model, `~ 0 + C(cell)`, fitted on all 22 mice. Contrasts:
  - primary: `wheel_vs_sed_pbs`
  - secondary: `wheel_vs_sed_avg` (activity effect averaged over liposome)
  - exploratory: `wheel_vs_sed_clo`, `interaction_act_x_lip`, `clo_vs_pbs_sed`, `clo_vs_pbs_wheel`
- Sensitivity: a separate two-group limma (`~ act_raw`, 11 vs 11) that ignores liposome. This is the pooled reading of the paper.
- No blocking. `replicate` is a within-group index, not a pairing key, and there is one experiment.
- Hallmark GSEA (prerank on the moderated t) for the primary, secondary and pooled tables.

## DEG counts vs paper (threshold: workflow_default, BH padj < 0.05, no FC cutoff; the paper has none)
| Table | n (up/down) | raw p < 0.05 audit | Paper |
|---|---|---|---|
| wheel_vs_sed_pbs (primary) | 0 | 871 | no DEG count reported |
| wheel_vs_sed_avg (secondary) | 1 (1/0), Gm7536 | 1286 | — |
| pooled_wheel_vs_sed (sensitivity) | 0 | 1018 | — |
| wheel_vs_sed_clo (exploratory) | 3 (3/0) | 1778 | — |
| interaction (exploratory) | 1 (1/0) | 1256 | — |
| clo_vs_pbs_sed / clo_vs_pbs_wheel (exploratory, not exercise) | 0 / 5 | 1216 / 1914 | — |

The comparable result is the paper's claim that hypoxia is lower in wheel runners:
- Hallmark HYPOXIA NES −1.68, FDR 0.005 (liposome-averaged)
- NES −1.68, FDR 0.007 (pooled 11 vs 11)
- NES −0.88, FDR 1.0 (PBS-only primary)

The direction is reproduced in every reading, but the result is significant only when all 22 mice are used. The paper therefore most likely pooled the clodronate mice. Hallmark GLYCOLYSIS shows the same pattern (avg NES −1.64, FDR 0.006). For individual hypoxia genes: Pgk1 is down in the all-mice readings (log2FC −0.59, raw p 0.048) and Adm is down but not significant; Vegfa, Slc2a1 and Ndrg1 do not change.

## Deviations (declared in the spec)
1. Gene-level limma DE plus Hallmark-hypoxia GSEA stand in for the paper's TRA of the Buffa set. Table_1.XLS was not available locally, and TRA is not an executor here.
2. Which mice the paper used is unknown. PBS-only is the primary; the liposome-averaged contrast and the pooled fit are run alongside it.
3. Duplicated gene symbols are collapsed in the prep script.
4. No low-expression filter. About 74% of entries sit at the CPM floor, which lowers BH power.

## Tool problems
- `tools/geo_tar.py:127`: the tar merge silently keeps the first row of each duplicated gene ID. Here that dropped 110 rows / 106 symbols, including Excel-date IDs, with no report. That is why I used the prep script.
- `.claude/skills/bioinformatics-workflow/references/case-spec.md:63` says the limma args are "as DESeq2", which includes `alpha`. But `run_limma_analysis` (`tools/limma_tools.py:17-28`) has no `alpha` parameter, so the execution failed with a TypeError until I removed it.
- Suitability comparison names for factorial designs (`act_raw_wheel_vs_sed_lip_raw-pbs`) are not documented; I only found them from the first run's "planned names not found" warning.
