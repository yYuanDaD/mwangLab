# HANDBACK: GSE124819 (PMC6565704, PMID 31197156)

## What ran
- Case spec route (`case_spec.json`, `python -m tools.case_runner execute`); validator 11 records, 0 errors.
- Paper is a Scientific Data **data descriptor**: it deposits liver RNA-seq for two sample sets and only normalizes with DESeq2 RLE; it reports no DE test, DEG counts or threshold. The intended exercise comparisons (S1.p2, S1.p3, S2.2.p1) were reconstructed and run as **exploratory**.
- Matrix: HTSeq raw counts (`GSE124819_GeneMatrix_RawCounts_ALL_UpdatedSampleNames_UpdatedCounts.txt.gz`), 24,613 genes x 37 samples, exact alignment on `title` (37/37).
- Design: `arm` factor (reference CONT + tiny cage), stratified by sample `set` (SCI + Exercise vs SCI + In-Cage Activity; separate experiments with different depth). One DESeq2 (pydeseq2 Wald) cell-means model per set on all of that set's samples.
- Threshold: `workflow_default` BH padj < 0.05, no fold-change cutoff (paper states none).
- No enrichment (not requested by the paper).

## DEG counts (padj < 0.05)
| Contrast | Ours (up/down) | Paper |
|---|---|---|
| CONT+SWIM vs CONT (Exercise set) | 121 (62/59) | not reported |
| CONT+SWW vs CONT (Exercise set) | 184 (85/99) | not reported |
| CONT+Large vs CONT+Tiny cage (Activity set) | 0 | not reported |

## Deviations and caveats
- The DE test itself is our addition; the paper has no DE route to reproduce.
- Paper says exercised animals were collected at 13.5 wk post-SCI (S2.3.p1, S4.4.p1); GEO says 11.5 wk for all contusion arms. If the paper is right, exercise is inseparable from 2 extra weeks post-injury.
- Rats were doubly housed with same-group partners (S2.2.p1); no cage IDs, so cage effects cannot be modelled.
- GEO protocol names pentobarbital, paper ketamine/xylazine/acepromazine (recorded discrepancy, no effect on design).
- Paper notes large within-group variability and overlap of Large/Tiny samples in the Activity set (S4.3.p1), consistent with 0 DEGs there.

## Tool problems
- `tools/decision_contract.py:160` (and :191): `paper_threshold: null` is rejected ("must be an object") even with `threshold_source: workflow_default`; the case-spec docs do not say how to encode "paper states no threshold". Worked around with an object of nulls plus `"stated": false`.
- `tools/case_runner.py:873-875`: `finish.n_deg` / summary.csv `n_deg` holds only the first planned table (121) for a multi-contrast case; the other tables' counts appear only in the per-execution output.
