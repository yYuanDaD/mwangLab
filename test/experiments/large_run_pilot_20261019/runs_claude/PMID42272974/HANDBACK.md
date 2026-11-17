# HANDBACK: PMID 42272974 (PMC13247415), GSE306842 + GSE306857

Optogenetic exercise of C2C12 ChR2(H134R) myotube monolayers. There are two separate experiments, both under SuperSeries GSE306860 (S10.p1):
- GSE306842 runs daily 30-min stimulation.
- GSE306857 runs daily 60-min stimulation.

Each experiment has an unstimulated control and 1, 4 and 10 Hz arms, with n = 6 wells per arm and 24 samples in all (S2.2.p2, Fig. 2).

## What ran

- **Route:** case spec, `python -m tools.case_runner execute case_spec.json`. Both cases ran to `completed`, with `decision_status` valid and `route: paper_aligned`. The contract validator returned 0 errors on 28 records.
- **Matrix:** `<GSE>_salmon.merged.gene_counts.tsv.gz`. These are Salmon estimated counts from nf-core/rnaseq 3.11.1 (GRCm39, Ensembl 110), 56,941 genes, about 91% integer values. They were rounded to integers, and the rounding is documented. The TPM file was rejected.
- **Alignment:** the key is the title suffix after `Muscle.<n>mins.`. Keys were matched with `normalize_keys`, so `x1Hz-1` matches `X1Hz.1`. 24/24 samples matched in each case, with exact matches and no positional matching. The group variable `grp` has levels CTRL, F1, F4 and F10, with 6 samples each.
- **Design:** one model `~ grp` per experiment on all 24 samples, with planned contrasts F1/F4/F10 vs CTRL. Suitability was `analyzable`. Covariance is `not_required`: wells are independent, and no batch or pairing is recorded.
- **Primary analysis:** R DESeq2 1.51 (Wald test) with `lfcShrink(type="apeglm")`, via `tools.r_de_tools:run_r_de` with `alpha` = 0.05. This is the paper's route (S5.6.p4). `log2FoldChange` holds the shrunken LFC, and `log2FoldChange_mle` keeps the MLE.
- **Sensitivity analysis:** pydeseq2 joint model with MLE LFC (`tools.joint_contrasts:run_joint_deseq2`).
- **Threshold:** the paper's rule, padj < 0.05 and |log2FC| > 0.5 on the shrunken LFC (Fig. 2d caption, S2.3.p1). The audit rule is padj < 0.05 alone.
- **Enrichment:** GSEA prerank on Hallmark (mouse `mh.all` 2024.1), ranked by Wald stat, for all 6 contrasts. All 6 runs completed. No ORA was run, because the paper did none at the DEG threshold.
- **Not compared:** 30 vs 60 min. Duration is aliased with experiment: separate cultures, harvest on day 14 vs day 16, and 0.6 vs 1.5 mL of media (S2.2.p3, S5.6.p1). The paper does not compare DE across the two experiments either.

## DEG counts vs the paper (padj < 0.05 and |shrunken log2FC| > 0.5)

The paper gives its counts only as a bar chart (Fig. 2d) and states no numbers in the text, so only the pattern can be compared.

| Contrast | Ours: total (up/down) | Ours: padj < 0.05 only | pydeseq2 MLE (sensitivity) | Paper |
|---|---|---|---|---|
| 30 min, 1 Hz vs ctrl | 2337 (1124/1213) | 5019 | 2739 | bar only |
| 30 min, 4 Hz vs ctrl | 2577 (1327/1250) | 5506 | 2980 | bar only |
| 30 min, 10 Hz vs ctrl | 197 (137/60) | 1034 | 285 | bar only, fewest |
| 60 min, 1 Hz vs ctrl | 1544 (650/894) | 5054 | 2039 | bar only |
| 60 min, 4 Hz vs ctrl | 2928 (1300/1628) | 6805 | 3425 | bar only |
| 60 min, 10 Hz vs ctrl | 13 (3/10) | 60 | 22 | bar only, fewest |

**Where we agree with the paper:**
- 1 and 4 Hz give comparable DEG numbers, and 10 Hz gives the fewest in both experiments (S2.3.p1).
- At 30 min, 1 and 4 Hz raise Myod1, Myh1, Myh2, Myh4, Myh7, Myh3, Myh8 and Pax7 (S2.3.p2).
- At 60 min, myogenic genes go down: Myog, Myod1 and Pax7 have shrunken LFC between -1.35 and -1.77 at 1 and 4 Hz (S2.3.p3).
- At 10 Hz, 60 min, Myh2 is the strongest down-regulated DEG by fold change (LFC -1.00, padj 4e-5).
- **GSEA:**
  - Myogenesis is the top set at 1 Hz 30 min (NES 2.73) and is significant in all 30-min conditions.
  - Myogenesis is not significant at 1 Hz 60 min (q 0.55).
  - Interferon alpha and gamma go down at 1 Hz 30 min and up at 1 Hz 60 min.
  - Hypoxia is enriched in both experiments.

**Where we differ** (these are also recorded in the study caveats):
- **10 Hz, 30 min:** the paper reports no significant effect on myogenic genes (S2.3.p3). We find Myog, Myod1 and Myh3 significant with small LFCs (0.53 to 0.74). The paper's Fig. 2e/f used two-way ANOVA in Prism, not DESeq2.
- **ROS pathway at 1 Hz, 30 min:** the paper reports it significantly down (S2.7.p1). We get NES +0.95, q 0.58.
- **Myog at 1 Hz, 30 min:** shrunken LFC is 0.41 (padj 0.010). That is below the 0.5 cutoff, so it is not a DEG under the paper's rule.
- **Myh2 at 10 Hz, 60 min:** it ranks 4th by p-value, not 1st.
- **OXPHOS:** it is not in the top five Hallmark sets at 1 Hz 60 min.

## Deviations (declared in the method gate)

- Salmon estimated counts were rounded to integers. The paper does not state how it imported them (for example tximport).
- Software versions differ: R 4.6 / DESeq2 1.51 here, vs R 4.2.0 in the paper.
- `alpha` was set to 0.05, the paper's FDR cutoff. The paper does not state it; R's default is 0.1.
- The DE model shares dispersion across all 4 arms of an experiment. The paper's wording ("averaged experimental vs averaged control") does not say whether it used one model or separate pairwise fits.
- **Not reproducible:**
  - ChR2 transgene expression (S2.8.p1): the deposited matrix contains only Ensembl mouse genes.
  - GO C5 GSEA and ClueGO: only Hallmark was run.
- QC alignment: GEO `data_processing` cites mm10 for QC, while the paper says mm39. The counts themselves are GRCm39. This does not affect the analysis.

## Tool problems

- **`tools/case_runner.py:454-458` (`_threshold_kwargs`):** `effect_metric` in a threshold is never passed to `native.apply_threshold` (whose `effect_column` defaults to `log2FoldChange`, `tools/native.py:805`). With `tools.deseq2_tools:run_deseq2_analysis`, the shrunken LFC sits in `log2FoldChange_shrunk` (`tools/deseq2_tools.py:183-185`). A paper rule on the shrunken LFC would then be applied silently to the MLE. I avoided this by using `run_r_de`, which writes the shrunken value into `log2FoldChange`.
- **`tools.joint_contrasts:run_joint_deseq2` (`tools/joint_contrasts.py:87`) has no LFC shrinkage option.** A one-model, multi-arm DESeq2 + apeglm route in Python is therefore unavailable; the R executor is needed for it.
- **gseapy duplicate-ranking warning (minor, `case_runner.log`).** gseapy warns "Duplicated values found in preranked stats" for about 19 to 23% of genes. These are mostly genes with zero counts in both compared arms, whose Wald stat is exactly 0 (4,021 of 31,566 in 30-min F1). This creates ties in the middle of the ranking only; I made no change.
- **Spec authoring:** a bash heredoc containing `''` inside an f-string broke the shell command. I wrote the spec generator with a file-write instead. This was not a repository issue.

## Files

- `case_spec.json` is the spec. The previous identical-decision attempt is in `_previous/`; the only change in the rerun was the added caveats.
- Per-case outputs are in `GSE306842/` and `GSE306857/`:
  - DE results: `results/deseq2_apeglm/DEG_results_grp_*_vs_CTRL.csv`
  - GSEA results: `results/enrichment_deseq2_apeglm_grp_*/gsea/`
  - suitability report: `suitability/suitability.md`
- Run records: `summary.csv`, `run_status.json`, `case_runner.log`.
