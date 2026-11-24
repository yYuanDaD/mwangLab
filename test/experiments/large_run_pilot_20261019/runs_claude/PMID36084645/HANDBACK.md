# HANDBACK: PMID36084645 / GSE205891

Decision maker: Claude Opus 5.5 (Claude Code session), case-spec route (`python -m tools.case_runner execute case_spec.json`). Preflight skipped as instructed. The first `execute` completed in one pass. After review it was re-run to add the unpaired sensitivity fits; earlier attempts are under `_previous/`. `validate_decision_contract.py` returned VALID for the run directory, including the `_previous/` copies.

## What ran

- **Paper**: an 8-month randomized trial in people with obesity and T2D. The intensive lifestyle therapy arm (ILT: energy restriction plus supervised exercise 4 x 60 min/week) was compared with standard care (SC). The paper reports muscle RNA-seq DEGs after vs before within each arm (S2.6.p1, FIG3A). Its threshold is log2|FC| > 0.3 and FDR < 0.05 using edgeR (S4.4.p1). For adipose tissue it reports selected genes only (S2.7.p1, FIG4).
- **Data**: GSE205891 has 62 samples: 28 muscle (SC 6 + ILT 8 subjects x pre/post) and 34 subcutaneous fat (SC 7 + ILT 10). These match FIG3 and FIG4. The only deposited matrix is `GSE205891_LID_all.gene_moderated_log2cpm.csv` (34,259 genes, log2 CPM; 2^x sums to about 1e6 per column). There are no raw counts.
- **Alignment**: exact match on `title` (62/62). `subject`, `tissue` and `visit` come from the title. `time` comes from the GEO sample type, and the A/B suffix agrees with it in every row. Sex inferred from X/Y genes gives one male (subject 026, ILT) in both tissues and at both timepoints. This matches the paper's "1 man in ILT".
- **Design**: tissue and arm are strata. `time` (post vs pre) is tested with subject blocking. Suitability verdict: analyzable.
- **Method**: limma (moderated t, eBayes), `~ C(subject) + Treatment`, on the deposited log2 CPM. Each execution has its own low-expression filter.

| Execution | Role | Pairs | Genes tested | DEGs (paper rule) | up / down | padj<0.05 only | Paper |
|---|---|---|---|---|---|---|---|
| muscle_ILT_post_vs_pre | primary | 8 | 13,285 | **1,382** | 906 / 476 | 1,997 | **1,540** |
| muscle_SC_post_vs_pre | secondary | 6 | 13,215 | **0** (min padj 0.24) | 0 / 0 | 0 | **65** |
| muscle_ILT_post_vs_pre_unpaired (`~ time`, no subject block) | sensitivity | 8 (not modelled) | 13,285 | 456 | 327 / 129 | 509 | 1,540 |
| muscle_SC_post_vs_pre_unpaired (`~ time`, no subject block) | sensitivity | 6 (not modelled) | 13,215 | 0 (min padj 1.0) | 0 / 0 | 0 | 65 |
| fat_ILT_post_vs_pre | secondary | 10 | 14,906 | 1,764 | 1,122 / 642 | 3,817 | not reported |
| fat_SC_post_vs_pre | secondary | 7 | 14,893 | 0 | 0 / 0 | 0 | not reported |
| muscle_change_ILT_vs_SC (paired change, ILT minus SC) | exploratory | 8 vs 6 | ~13.3k | 95 | 72 / 23 | 95 | not reported |

Threshold applied: padj < 0.05 and |log2FC| > 0.3, both strict. Source: `paper_on_deviation_route` (S4.4.p1).

**Named genes.**
- **ILT muscle**: all 10 genes the paper names are up and significant with the same sign: NAMPT, SIRT3, PPARGC1A, MT-ND1, MT-ND5, SOD2, COX4I1, CS, CYCS and VEGFA (log2FC 0.35 to 0.71, padj 0.0015 to 0.015).
- **ILT fat, ECM genes**: SPARC, LOX, LOXL1, TNMD and SEMA3C are down (padj < 0.02), as in the paper. PDGFA is also down (padj 0.024), but its log2FC of -0.28 falls just below the 0.3 cutoff.
- **ILT fat, inflammation genes**: TNF, CCL2, CCL5, CD68 and CD74 do not reach padj < 0.05, consistent with "unchanged". IL6 was removed by the expression filter.

**Enrichment** (muscle ILT; supporting only, because the paper used IPA):
- Hallmark GSEA: OXIDATIVE_PHOSPHORYLATION is the top term (NES 3.29).
- KEGG ORA: oxidative phosphorylation, thermogenesis and the TCA cycle are enriched.
- Both agree with the paper's IPA result (mitochondrial dysfunction / OXPHOS / TCA).

## Deviations (declared)

1. **edgeR on counts was blocked.** Only moderated log2 CPM was deposited, and library sizes are not available, so counts cannot be rebuilt. limma on log2 CPM ran instead.
2. **Low-expression filter added.** The rule was log2CPM >= 0 in at least the smaller group's number of samples (8, 6, 10, 7, and 12 for the change model). The paper does not describe a filter.
3. **Duplicated gene symbols.** 121 extra rows were collapsed by the executor to the highest-mean row (`tools/de_common.py:15`).
4. **Pairing modelled explicitly.** Pairing is by subject; the paper's edgeR design is not stated.
5. **Exploratory contrast added.** The randomized arm x time contrast (paired change) was added. The paper does not report DEGs for it.
6. **Per-sex analyses not run.** There is only one male, so no per-sex comparison has n >= 3.

**Scientific caveat:** ILT combines energy restriction (about 17% weight loss) with exercise training. These results describe lifestyle therapy, not exercise alone. The within-arm before/after changes are not randomized comparisons.

**SC muscle gap:** we found 0 DEGs, the paper reports 65.
- No gene reaches padj < 0.05 under the paired limma on log2 CPM. The minimum padj is 0.24, although 186 genes have p < 0.01 and |log2FC| > 0.3.
- Likely causes: the paper ran edgeR on counts, possibly with a different filter. A count model has more power at n = 6 pairs.
- This is a method or route difference, not a direction contradiction.

**Unpaired sensitivity (added after review).** Same samples, filter and threshold, fitted as `~ time` with no subject block.
- Muscle ILT drops from 1,382 to 456 DEGs (paper: 1,540).
- Muscle SC stays at 0 DEGs (min padj 1.0; paper: 65).
- So dropping the pairing does not explain the gap to the paper's counts. It moves ILT further from 1,540 and leaves SC at 0. The paired fit stays the primary result.
- The remaining gap most likely comes from the count-level edgeR route (counts were not deposited) and the paper's unstated filter.

## Tool problems

- **Suitability report gives a count-model route for a log-CPM matrix.** `tools/suitability.py:76-81`: `_TYPE_TO_KEY` matches substrings in order. My matrix-type string "log2 CPM (moderated, prior count; ...)" hit `"count"` before `"log"`, so the report printed "route: DESeq2 / edgeR / limma-voom" for a log2 CPM matrix. "CPM" has no key of its own. The method gate and the executor still used limma correctly. Only the suitability.md data-type line is wrong.
- **Leading zeros dropped from derived subject IDs.** Regex-derived `subject` values such as "003" came back as integers ("3") in `results/muscle_change_ILT_vs_SC/followup_post/paired_change_pairs.json`. Derived metadata is re-read without `dtype=str`. This is harmless here, but IDs like "03" and "3" would be merged.
- No executor failures and no LLM calls.
