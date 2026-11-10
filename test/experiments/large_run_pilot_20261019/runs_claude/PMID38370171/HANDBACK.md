# HANDBACK: PMID38370171 / GSE240131

Paper: Low-intensity exercise training improves systolic function of heart during metastatic melanoma-induced cachexia in mice (PMC10874746).
Status: finished (case `completed`, decision `valid`, route `declared_deviation`, validator 16 records with 0 errors).

## What ran
- `case_runner inspect`, then `prep_matrix.py`. The prep script indexes the deposited `GSE240131_raw_counts.txt.gz` by gene symbol and drops the `st_gene_id` and `gene_id` columns. Six rows with duplicated symbols (Excel-mangled 1-Mar/2-Mar, Plin2) get their st_gene_id appended. Output: `GSE240131_counts_by_symbol.csv`, 17397 x 12.
- Spec: `case_spec.json`. Alignment is an exact match on a key taken from the GEO title (`Heart, C1` -> `C1`): 12/12 samples. Groups are grp = C/E/T/TE, 3 libraries each. Each library pools 2 mice (FIG3).
- Matrix: these are estimated counts. They come from featureCounts and about 7% of values are fractional. They were rounded (`transform: round`) and then analysed with edgeR (inmoose, TMM, QL F-test). Each pair was fitted on its own 6 samples, matching the paper's edgeR (S2.4.p1).
- Executions:
  - `grp_TE_vs_T`, primary: the exercise effect in tumor-bearing mice.
  - `grp_E_vs_C`, secondary: the exercise effect in tumor-free mice.
  - `grp_T_vs_C`, secondary: the tumor effect. This is the base set for the paper's reversal overlaps.
- Enrichment (ORA GO/KEGG and Hallmark GSEA) on TE_vs_T and E_vs_C: completed.
- Post-hoc overlap with `overlap_posthoc.py`, written to `overlap_posthoc.json`.

## Threshold
The paper's rule is in S2.4.p1: FC >= 1.5 and raw p < 0.05. Applied as p < 0.05 and |log2FC| >= 0.5849625, with source `paper`. Audit rule: BH FDR < 0.05, no FC cutoff.

## DEG counts vs paper (paper threshold)
| Table | Ours (up/down) | Paper |
|---|---|---|
| T vs C | 2629 (2028 / 601) | 2020 up / 741 down (S3.3.p1) |
| TE vs T | 2619 (675 / 1944) | no total stated |
| E vs C | 572 (351 / 221) | no count stated |
| tumor-down AND exercise-up (TE vs T) | 236 | 318 of 741 |
| tumor-up AND exercise-down (TE vs T) | 1389 | 1447 of 2020 |

Audit counts (FDR < 0.05): T vs C 3, TE vs T 2, E vs C 0. None of the contrasts holds up under FDR control at n=3.

Named genes: Myh7b, Pde4d, Rnf207, Tmem65, Kcnj5 and Cacnb2 all go down with tumor and up with exercise in TE vs T, matching the paper. Myh7b +2.37 (p=0.0018), Rnf207 +1.43, Tmem65 +1.24, Cacnb2 +1.23 (p=0.048). Kcnj5 just misses (p=0.051). All of them have padj around 0.25.

Pathways (kept separate from DE):
- TE vs T: the strongest ORA terms are cell cycle / DNA replication, consistent with FIG4F. GSEA puts oxidative phosphorylation (NES 3.0) and myogenesis (NES 1.2, n.s.) up with exercise, in line with the paper's aerobic-respiration and contraction clusters.
- E vs C: GSEA puts E2F/G2M up with exercise (FDR < 0.01). This is exploratory.

## Deviations
- Fractional featureCounts values were rounded to integers before edgeR. The paper ran edgeR on the deposited values.
- The paper does not state its edgeR test or its gene filtering. We used the QL F-test on all non-zero genes, with pairwise fits on 6 samples rather than one 4-group fit.
- The S3.3.p1 text says the tumor "upregulated 741 genes", but its named genes are tumor-decreased. We read 741 as tumor-down.
- Other GEO-vs-paper discrepancies:
  - GEO extract_protocol says "livers" while the paper says heart.
  - GEO says assembly mm10 while the paper says GRCm39.

## Key scientific caveat
Heart libraries T1 and T2 contain melanoma tumor tissue: Pmel, Tyrp1, Dct and Mlana (plus Mki67/Top2a) are 10^3-10^4-fold higher than in every other library. All TE libraries are free of it, and so is T3. The TE vs T and T vs C contrasts therefore mix cardiac change with tumor-cell content. The paper's "cell cycle/DNA replication up by tumor, reversed by exercise" set (FIG4E/F, 1447 genes) is very likely this contamination rather than a cardiac effect of exercise. The contamination also dilutes the cardiac genes, which may inflate the heart-contraction reversal signal. The contrast is still estimable, with no batch aliasing, so we ran it and did not refuse it. With n=3 we could not adjust for tumor content. E vs C is unaffected. This caveat is recorded in the study record.

## Tool problems
- `tools/native.py:240-246` (`profile_matrix`, used by `case_runner inspect`): the integer Entrez `gene_id` column and the text `gene_symbol` column were counted as samples. The profile then reported n_samples=14, max=108,169,201 (an Entrez ID) and missing_values=17390. Worked around with `prep_matrix.py`.
- `tools/edger_tools.py:106`: `counts_sub.astype(int)` truncates fractional estimated counts instead of rounding them. Avoided with the case-level `transform: round`.
- `tools/edger_tools.py:145-148`: the tool prints its own summary using padj < 0.05 and |log2FC| > 1. That summary is not the applied rule, so it is ignored. The counts above come from the runner's applied threshold.
