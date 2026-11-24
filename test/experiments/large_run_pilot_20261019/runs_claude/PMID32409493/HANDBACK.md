# HANDBACK — PMID 32409493 / GSE137631

**The comparison with the paper rests on the abstract only.** No full text was available. The paper sources were the PubMed abstract (E-utilities efetch) and the GEO series title, summary, overall design and data_processing. Both are saved in `paper_abstract_and_geo.md`.

## What ran
- Design: women randomized to RYGB alone or RYGB plus combined aerobic and resistance exercise training (RYGB+ET). Vastus lateralis biopsies were taken before surgery (PRE) and 9 months after (POST9), from 6 patients per arm. 6 lean controls were sampled at baseline only. The 3-month biopsies mentioned in the abstract are not in GEO.
- Matrix: `GSE137631_raw_counts.txt.gz` (integer QuantSeq read counts). `prep_rename_columns.py` renamed its columns to GSM ids using an explicit name rule, never position; the map is in `GSE137631_raw_counts_gsm_column_map.csv`. All 30 samples aligned exactly. The DESeq2-normalized file was not used.
- Spec `case_spec.json` → `python -m tools.case_runner execute`. The run completed, suitability was analyzable (11/11 comparisons), and the validator reported 0 errors.
- Threshold: `workflow_default`, BH padj < 0.05 with no fold-change cutoff. The abstract states no DEG threshold.

| Table | Role | Method | DEGs (up/down) | Paper |
|---|---|---|---|---|
| ET_post9_vs_pre | primary (paper_aligned) | DESeq2 paired `~ subject + grp` | 148 (41/107) | count not in abstract |
| RYGB_post9_vs_pre | secondary | DESeq2 paired | 160 (68/92) | count not in abstract |
| exercise_x_time/RYGBET_vs_RYGB (difference in change) | secondary, declared deviation | limma paired_change, log2(CPM+1), CPM≥1 in ≥6 samples | 0 | — |
| ETpost_vs_LEAN | exploratory, associational | DESeq2 unpaired | 426 (244/182) | — |
| RYpost_vs_LEAN | exploratory, associational | DESeq2 unpaired | 1035 (456/579) | — |

The ordering of the lean comparisons (RYGB alone is further from lean than RYGB+ET) agrees with the GEO summary's claim that training restores a lean phenotype. Treat this as associational only; see the batch caveat below.

**Genes named in the abstract.** In the RYGB+ET arm, no named gene reached padj < 0.05:
- COL1A2: log2FC −0.66, padj 0.088
- COL1A1: −0.62, padj 0.68
- FST: +0.35, padj 0.84
- TGFB1: low expression, padj NA
- SMAD2 and SMAD3: unchanged

The directions for collagen I (down) and FST (up) match the abstract. None of these genes differ in the between-arm interaction (all padj > 0.9).

**Enrichment (GSEA, Hallmark, ranked by stat; separate from the DE result):**
- ET_post9_vs_pre: EPITHELIAL_MESENCHYMAL_TRANSITION (ECM/collagen set) NES −2.57, FDR < 0.001. TGF_BETA_SIGNALING NES −1.26, FDR 0.14.
- Difference in change (RYGB+ET minus RYGB): EMT NES −1.83, FDR 0.005. OXIDATIVE_PHOSPHORYLATION NES +2.04, FDR 0.002.

Both agree with the abstract: ECM remodeling is reduced more with exercise, and the effect adds to surgery. The interaction is null at the gene level but shows up at the pathway level.

## Deviations
- **Exercise-specific estimand.** The randomized exercise effect is the difference in pre-to-post change between arms. No DESeq2 executor handles an interaction with subject nested in arm, so I ran it with limma paired_change on log2(CPM+1) and declared it as a deviation. Within-arm POST9 vs PRE mixes training with surgery and weight loss.
- **Paper's exact DESeq2 design.** The abstract does not give it. I assumed pairing by patient; ages agree within each pair.
- **Threshold.** The workflow default was used because the paper's threshold is unknown.

## Caveats
- **Possible batch.** Matrix column names carry a `WD.` prefix for the lean and RYGB+ET samples but not for RYGB. This may mark a separate processing batch per arm. It cannot be tested here. Paired within-arm contrasts and the difference in change are protected from an additive per-subject batch. The lean comparisons are not.
- **Sample size.** n = 6 per arm, so the interaction has low power.

## Tool problems
- The paper sources had to be fetched by hand (curl efetch plus GEO SOFT grep). The runner has no input for "abstract + GEO only".
- Alignment required a prep script. Matrix columns (`WD.RYGB.ET.1.PRE`) and GEO titles (`RYGB + exercise training_1 PRE`) use different vocabularies, and `alignment.key_patterns` / `matrix_column_pattern` cannot map them when the prefix differs by arm. The inspect hint "title (case/separator differences)" matched only 12/30, so `normalize_keys` alone would have silently dropped 18 samples had it been trusted.
- pydeseq2 printed `RuntimeWarning: overflow encountered in exp` (`.venv-pdf/Lib/site-packages/pydeseq2/utils.py:1088`). The fit still completed and `deg_sanity` was ok.
- No executor exists for a DESeq2 interaction with a nested subject (`tools/deseq2_tools.py` takes additive `covariate_columns` plus `interaction_terms`, but not a nested-subject paired difference-in-change). This forced the limma route.
