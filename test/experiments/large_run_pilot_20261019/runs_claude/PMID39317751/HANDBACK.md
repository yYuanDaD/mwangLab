# HANDBACK: PMID39317751 / GSE227516

## What ran
- Case spec route (`python -m tools.case_runner execute case_spec.json`). The run finished: decision `valid`, execution `completed`, and the contract validator reported 0 errors across 12 records. The previous attempt was moved to `_previous/20261110T173058Z`. The only change between attempts was the added study caveats.
- Data: `GSE227516_counts_table.csv.gz`, which holds kallisto + tximport estimated gene counts (Ensembl 104), 52,178 genes x 10 samples. It covers pancreatic islets from male C57BL/6 mice aged 6-9 months: 5 SEDENTARY and 5 EXERCISE (10-day treadmill training). This matches Fig. 2j,k and Fig. 4c,d (n = 5 per group).
- Alignment: matrix columns P1..P10 were matched to the first token of the GEO title (exact, 10/10). The group comes from the title and is recoded SED/EX.
- Design: two-group, `~ grp`, EX vs SED. Independent animals, no blocking. The suitability verdict was `analyzable`.
- Method: DESeq2 (pydeseq2 Wald) on rounded estimated counts (`transform: round`, `rounding_documented`). The paper does not name its RNA-seq method (S3.15.1.p1; the analysis was done by the Joslin core), so this route is a `declared_deviation`.
- Threshold: `workflow_default`, BH padj < 0.05 with no fold-change rule. The paper gives no RNA-seq threshold. Its P < 0.05 (S3.23.p1) applies to the Prism physiology and qPCR statistics. Raw p < 0.05 is reported only as a labelled audit count.
- Enrichment: ORA (GO BP/MF/CC and KEGG 2019 Mouse) and GSEA preranked on MSigDB mouse Hallmark. Both completed.

## DEG counts vs paper
| Contrast | Ours (padj<0.05) | up / down | audit raw p<0.05 | Paper |
|---|---|---|---|---|
| EX vs SED | 3798 | 980 / 2818 | 6481 | no DEG count reported (gene-set level only; "profound transcriptional changes", S1.3.p1) |

The direction is mostly down, which fits the paper's "exercise significantly downregulated the expression of several genes".

## Paper-claim checks
- **SenMayo set down (Fig. 2j,k):** not tested, because SenMayo is not among the workflow gene-set libraries. KEGG "Cellular senescence" is over-represented among the DEGs (adj P 0.001, 56/185 genes), but that test gives no direction.
- **Glucagon signalling up (S1.5.p2, Fig. 4c,d):** not reproduced. Gcgr has log2FC +0.97, the paper's direction, but padj is 0.24. KEGG "Glucagon signaling pathway" ORA has adj P 0.35.
- **Cdkn1a (p21Cip1):** contradicts the paper. It is UP in our results (log2FC +0.70, padj 0.042). The paper reports exercise lowering p21 by qPCR, though in other cohorts. This is recorded in the study caveats.
- **Cdkn2a:** down but not significant (log2FC -0.68, padj 0.33).
- **Trp53 and Hmgb1:** down at raw p (0.024 and 0.015), not significant at padj.
- **Hallmark GSEA:** the strongest sets go down with exercise: OXPHOS (NES -2.65), fatty-acid metabolism, interferon alpha/gamma response and E2F targets, all at FDR about 0. UPR and PANCREAS_BETA_CELLS go up (NES 1.34, FDR 0.07).

## Deviations
- The DE method and threshold were chosen by the workflow because the paper states neither.
- Estimated counts were rounded before DESeq2, following the standard tximport recipe.

## Tool problems
- No blocking problems.
- Minor: gseapy warned "Duplicated values found in preranked stats: 17.91% of genes" (`case_runner.log`). The ranking metric `stat` has many tied values, probably genes with near-zero counts or the same stat. GSEA ran anyway, but ties among those genes make their order arbitrary.
