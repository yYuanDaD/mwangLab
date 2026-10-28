# HANDBACK: GSE195585 / PMC9037237 (collagen peptides + acute resistance exercise)

## What ran

- Case-spec route (`python -m tools.case_runner execute case_spec.json`). Validator: 17 records, 0 errors. Route `declared_deviation`.
- Matrix: `prep_matrix.py` builds `input/GSE195585_kallisto_est_counts_gsm.csv` (60,617 GENCODE genes x 119 GSM) from the tar's `-raw_counts` members only. The TPM members are dropped. For each file the script checks the name's arm, time and subject against the GEO record. The values are kallisto estimated counts and are not integers (74% of entries are whole numbers).
- Alignment: exact match on the GSM index, 119/119. grp: PLA 60, CP 59. time: t0 30, t1 30, t4 30, t24 29. subject ID01-ID30; ID17 has no 24 h sample.
- Suitability: analyzable, 19/19 comparisons, no warnings.
- Method: log2(CPM+1) from `preprocess_counts`, leaving 17,723 genes after the filter. Then `run_multigroup_analysis` `paired_change` with one fit per follow-up time: delta = follow-up minus baseline for each participant, modelled as `delta ~ 0 + C(grp)`. The fit is limma with moderated t. Contrasts: change in PLA, change in CP, CP minus PLA change, and the pooled change (exploratory). The 1 h and 4 h fits have 30 pairs each; the 24 h fit has 29 pairs (ID17 excluded).
- Enrichment: GSEA on MSigDB Hallmark for PLA 1 h, PLA 4 h, CP 4 h and CP-vs-PLA 4 h. ORA for CP-vs-PLA 4 h was recorded as failed because no gene passed the threshold.

## DEG counts (paper threshold: FDR < 0.05, no fold-change rule, S2.9.p1)

| Contrast | n (up/down) | audit: FDR<0.05 and abs(log2FC)>log2(1.5) |
|---|---|---|
| PLA 1h vs baseline (primary) | 2101 (1038/1063) | 319 |
| PLA 4h vs baseline (primary) | 4869 (1489/3380) | 561 |
| PLA 24h vs baseline (primary) | 3185 (2525/660) | 257 |
| CP 1h / 4h / 24h vs baseline | 2117 / 5675 / 2628 | 277 / 575 / 348 |
| CP minus PLA change, 1h / 4h / 24h | 0 / 0 / 0 | 0 / 0 / 0 |
| pooled change, 1h / 4h / 24h (exploratory) | 4272 / 8148 / 6264 | 292 / 549 / 329 |

The paper reports no DEG counts. Its results are KEGG GSEA NES values only, so no count comparison is possible.

How the paper's claims compare:
- Strong exercise response. NR4A3, ATF3, PPARGC1A and MYC are up at 4 h in PLA (all padj ~0). Hallmark GSEA: TNFa/NF-kB, hypoxia, p53, TGF-beta, IL6/JAK/STAT3, mTORC1 and UPR are up at 1 h and 4 h in both arms. This is consistent with the paper's report that PI3K-Akt and MAPK go up at 1 h and 4 h in both arms. No direct KEGG comparison was made because KEGG GSEA was not run.
- CP vs PLA. No gene-level difference in change at any time point. The paper's named genes at 4 h are ANGPT1 (log2FC -0.10, padj 0.995) and TGFB1 (+0.05, padj 0.995), so neither is supported. Hallmark GSEA on the 4 h difference shows IL6/JAK/STAT3 and inflammatory response up in CP (FDR 0.037) and OXPHOS and MYC targets down. The paper's CP > PLA claim for PI3K-Akt and MAPK is pathway-level only and was not tested with KEGG here.

## Deviations (declared)

- The paper's method is voom + limma, but the repository's voom executor can only fit two arms with no blocking or contrasts. It was replaced by limma on log2(CPM+1) of within-subject differences. The paper does not state how it modelled the repeated measures.
- Enrichment used Hallmark GSEA (and Enrichr ORA) instead of the paper's fgsea / EnrichmentBrowser on KEGG.
- Estimand caveat: there is no non-exercise control arm. The time contrasts therefore also include the effects of repeated biopsy, fasting, time of day and the drink. The PLA arm is treated as the primary exercise response.

## Tool problems

1. `tools/case_runner.py:569-571` (`_matrix_input`, raw_tar). When a GSM has two tar members (here `-TPM` and `-raw_counts`), the GSM rename is skipped without a message. The 238-column merge then mixes TPM and count columns. `inspect` reports the same mixed matrix with only the label "linear_normalized or estimated_counts". A prep script was needed.
2. `tools/decision_contract.py:281-285` (`_same_threshold`). `effect_metric` is compared even when `effect_cutoff` is null. A paper rule with `effect_metric: null` therefore fails against an applied rule with `effect_metric: "log2FoldChange", effect_cutoff: null`, which is the template's form. The check runs only in `native.py:1075` (`case.finish`), after every executor and GSEA has finished, and it exits with a traceback instead of the runner's JSON error.
3. A relative `inputs.matrix` path is resolved against `data_root` even when it points to the run directory. This is documented, but the error only appears as a FileNotFoundError at execute time.
4. An ORA run with zero DEGs is recorded as `failed` rather than `not_run`.
5. Minor: `inspect` shows mojibake in `extract_protocol_ch1` ("Bergstr枚m"), a metadata decoding issue.
