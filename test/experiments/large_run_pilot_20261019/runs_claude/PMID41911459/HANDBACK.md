# HANDBACK: PMID41911459 / GSE325919

## What ran
- Paper: old (23 mo) mice after 10 wk of high-intensity multicomponent interval training (HIMIT). RNA-seq of gastrocnemius (S2.24). The paper compares two groups against WT untrained: WT trained (the exercise effect, Fig. 2H) and G6PD-Tg untrained (a genotype effect, Fig. 2I).
- Data: GEO has 30 samples: WT untrained (SED), WT trained (TR) and G6PD-Tg untrained (G6PD), 5 per sex in each group. The `_RAW.tar` holds RSEM `*.genes.results.gz` files. `prep_merge_rsem.py` merged their `expected_count` column into `GSE325919_rsem_expected_counts.csv.gz` (53,465 genes x 30 samples, values not rounded).
- Spec: `case_spec.json`, run with `tools.case_runner execute`. The validator found 0 errors in 14 records. Alignment matched all 30/30 samples exactly. Suitability was `analyzable` and the sex check passed.
- Primary model: limma on log2(CPM+1) with `~ sex + grp` fitted on all 30 samples (`run_joint_limma`). Its planned contrasts are TR vs SED (the exercise contrast, primary) and G6PD vs SED (secondary, not exercise).
- Exploratory runs: TR vs SED within each sex (limma, 5 vs 5). The paper says "sexes were analyzed separately" (S2.26.p2).
- Enrichment: Hallmark GSEA (preranked on the moderated t) for both joint contrasts.

## DEG counts (threshold: workflow default BH padj < 0.05, no fold-change cutoff; the paper states no DEG threshold)
| Table | n (up/down) | raw p < 0.05 (audit) | Paper |
|---|---|---|---|
| joint/grp_TR_vs_SED (exercise) | 3 (0/3) | 1351 | not stated in text (Dataset S2 only, not available) |
| joint/grp_G6PD_vs_SED | 17 (7/10) | 1997 | not stated |
| TR_vs_SED_female (exploratory) | 1 (0/1) | 999 | - |
| TR_vs_SED_male (exploratory) | 0 | 1081 | - |

The paper reports RNA-seq only as GSEA (S1.p7): OxPhos, cristae, ROS detoxification and glutathione metabolism go up in the trained and G6PD-Tg groups. Our Hallmark GSEA agrees in direction:
- TR vs SED: OXIDATIVE_PHOSPHORYLATION NES 3.47 and FATTY_ACID_METABOLISM NES 2.71, both FDR ~0.
- G6PD vs SED: OXIDATIVE_PHOSPHORYLATION NES 3.84 (FDR ~0) and ROS_PATHWAY NES 1.49 (FDR 0.053).

## Deviations (declared)
- The paper's route (genes < 10 CPM removed, edgeR TMM, then limma) could not be run with the runner. We used library-size log2(CPM+1) with the preprocess_counts filter (count >= 10 in >= 3 samples), which kept 17,057 genes, and no TMM factors.
- Sex enters the pooled model as a covariate. The paper's RNA-seq handling of sex is not stated, so per-sex fits were added as exploratory runs.
- GSEA used MSigDB Hallmark sets; the paper used MitoCarta 3.0 (clusterProfiler/DOSE). This is a qualitative direction check only.
- No DEG count comparison was possible, because the paper's counts exist only in Dataset S2.

## Tool problems
1. `tools/geo_tar.py:59-60`: the tar merger only accepts members ending .txt/.tsv/.csv/.tab(.gz). RSEM `*.genes.results.gz` files are skipped, so `inspect` (via `tools/native.py:528`) said "no mergeable per-sample count files". A prep script was needed. `tools/paper_screen.py:525` already recognises RSEM `.genes.results`, so the two disagree.
2. `tools/case_runner.py:610-612`: the `log2(CPM+1)` transform calls `preprocess_counts` with fixed defaults (count >= 10 in >= 3 samples, no TMM). There is no way to give a CPM-based filter or TMM normalisation, so the common "edgeR TMM + limma" paper route cannot be run.
3. `tools/decision_contract.py:158-160`: `paper_threshold: null` is rejected ("must be an object"). There is no documented way to say "the paper states no threshold", so a placeholder object with null metric was used.
4. Minor: listing a covariate (sex) under design `factors` makes suitability name only per-sex and interaction comparisons, so the planned `grp_TR_vs_SED` was rejected. Moving sex to `covariate_candidates` fixed it. The case-spec docs do not say this.
