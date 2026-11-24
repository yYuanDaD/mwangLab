# HANDBACK — PMID35316212 / GSE184951

Paper: *Aerobic exercise elicits clinical adaptations in myotonic dystrophy type 1 patients independently of pathophysiological changes* (PMC9106360). Decision maker: Claude Opus 5.5 session (case-spec route). Status: **finished**. Contract validator: 17 records, 0 errors.

## What ran

- **Inputs:** per-sample HTSeq `*.geneCounts.txt.gz` from `GSE184951_RAW.tar` (63,677 Ensembl genes × 32 samples, all integers). The three `*.SE.MATS.JC.txt.gz` files are rMATS splicing tables and were not used as expression matrices.
- **Samples:** 11 DM1 patients sampled before and after training (S1–S9, S12, S13; P10 and P11 dropped out, S4.1.p1), plus 10 healthy controls (CON). Alignment was an exact match on the GSM ids.
- **Grouping and pairing:** `grp` (CON/PRE/POST) and `subject` come from the sample title. Each control gets its own subject id (`Control_N`), so a control matched to patient N is not counted as the same person.
- **Sex check:** sex inferred from Y-chromosome and XIST expression is consistent within every pre/post pair, and every control matches its patient's sex (DM1 5 M / 6 F; CON 5 M / 5 F). Metadata has no sex field, so `sex` was recoded from this check.
- **Method:** DESeq2 (pydeseq2 Wald), the paper's method (S4.16.p1).
  - Primary: `~ subject + grp`, POST vs PRE, 11 complete pairs.
  - Secondary: `~ grp`, PRE vs CON. This is a disease comparison (associational), not an exercise effect.
- **Threshold:** the paper's own rule from the Fig 4 legend: |log2FC| > 1.5 and raw P < 0.005, with no FDR. Source: `paper`. A separate audit rule is BH padj < 0.05 with no fold-change cutoff.
- **Enrichment:** ORA (Enrichr GO/KEGG) on POST vs PRE up-regulated genes, and Hallmark GSEA on the full POST vs PRE ranking.

## DEG counts vs the paper (|log2FC| > 1.5, P < 0.005)

| Table | Role | Ours (up/down) | Paper (up/down) | Audit padj<0.05 |
|---|---|---|---|---|
| grp_POST_vs_PRE | primary (paper_aligned) | 55 (46/9) | 19 (18/1) | 1066 |
| grp_PRE_vs_CON | secondary (associational) | 1471 (1156/315) | 640 (435/205) | 9745 |
| grp_POST_vs_PRE_filtered (mean count ≥ 10) | sensitivity | 27 (25/2) | 19 (18/1) | 1075 |
| grp_PRE_vs_CON_filtered (mean count ≥ 10) | sensitivity | 664 (440/224) | 640 (435/205) | 8589 |
| grp_POST_vs_PRE_male (5 pairs) | exploratory | 74 (58/16) | – | 12 |
| grp_POST_vs_PRE_female (6 pairs) | exploratory | 49 (37/12) | – | 36 |

- **Unfiltered runs:** the extra DEGs are mostly low-count genes (baseMean < 10), which pass a raw-P rule with a large fold change.
- **Filtered runs:** dropping genes with mean count < 10 (iDEP filters low-expressed genes by default; the paper names no filter) brings both contrasts close to the paper. Exercise gives 27 vs 19 and disease 664 vs 640, with up/down splits close to the paper's.
- **Named genes (PRE vs CON):** SNORD116-1, RNU5B-1, RNU6ATAC and SNORA38 are all strongly up in DM1-PRE, matching S2.8.p1.
- **Enrichment matches the paper (Fig 4E: ECM, angiogenesis, inflammation up with training):**
  - ORA on up-regulated genes: top terms are extracellular structure and matrix organization (COL1A1, COL3A1, ADAMTS14/16/18; adj P 3e-4).
  - GSEA: EMT, angiogenesis, IFN-α/γ, inflammatory response and IL6-JAK-STAT3 are up; MYC targets and DNA repair are down.

## Deviations

1. pydeseq2 instead of R DESeq2.
2. Each contrast is fitted on its own subset. A single model with subject blocking cannot estimate CON vs PRE, because each control is its own subject. The paper does not say whether it used one model.
3. The paper names no low-count filter. The filtered runs are a labelled sensitivity analysis, and the primary result stays unfiltered.
4. Extraction batches (S4.16.p1: a P6 pilot pair, then PRE, POST and CON "in individual batches") may coincide with group. No batch annotation is deposited, so batch could not be modelled; this is recorded as a caveat.
5. GEO has 10 controls, against 11 recruited (no control matched to patient 5). The paper's Fig 4 gives n = 10–11, so this was executable as is.
6. The paper's rule uses raw P with no FDR. It was applied as written, and the BH audit counts are reported next to it.

## Tool problems

- `tools/case_runner.py:387`: without `--merge-tar`, `inspect` profiles the rMATS `*.SE.MATS.JC.txt.gz` files as expression matrices. It treats exon coordinates as "sample columns" and IJC/SJC count columns as annotation, and it skips the real gene counts in `_RAW.tar`. I had to re-run inspect with `--merge-tar`.
- The suitability covariance line (`GSE184951/suitability/suitability.md`) gives conflicting dispositions for `subject` in one cell: "omit (identifier)", "candidate_covariate" and "omit (rank deficient)". It also reports `not_required`, although subject is a required block for the paired contrast.
- The sex check reports "per-sex analysis: yes", but `suitability.json` carries no `split_plan`. The per-sex runs had to be built by hand with a recoded `sex` column.
- A harmless pydeseq2 warning: `.venv-pdf/Lib/site-packages/pydeseq2/utils.py:1088` RuntimeWarning: overflow in exp.
