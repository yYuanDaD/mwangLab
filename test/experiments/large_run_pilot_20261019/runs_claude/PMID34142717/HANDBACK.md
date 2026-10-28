# HANDBACK: PMID34142717 / GSE178262

Paper: Maier et al., J Physiol 2022 (PMC9290843), "Transcriptomic, proteomic and phosphoproteomic underpinnings of daily exercise performance and zeitgeber activity of training in mouse muscle".

## What ran

- `prep_merge_lanes.py`: the GEO matrix has 80 columns, two lanes (L001/L002) for each of the 40 GSM libraries. The GSM descriptions say these are the same library. The script summed each library's two lanes into one GSM column. It matched L001 by the exact column name in the GSM description and L002 by the shared library suffix, and asserted that every GSM got exactly 2 of the 80 columns. It also mapped the Entrez row IDs to MyGene symbols (23601/23621 mapped, the 20 unmapped keep their Entrez ID, no duplicate symbols). Output: `GSE178262_lanes_merged_symbol.csv` plus `entrez_to_symbol.csv`.
- `case_spec.json` with two cases from the same series, one per experiment and muscle. Validator: 32 records, 0 errors.
  - **GSE178262_treadmill** (quadriceps, 24 samples, acute maximal treadmill run). Factors `trt` (Sed/Ex0/Ex3) and `zt` (sacrifice bin Z00/Z04/Z12/Z16). Each exercise group is compared with the sedentary group sacrificed at the matching time, as S2.2.p1 specifies: Ex+0h after a ZT0 run vs Sed ZT0, Ex+3h vs Sed ZT4, and the same for ZT12 against ZT12/ZT16. One joint pydeseq2 cell-means model (8 cells of n=3) was fitted, with the pseudo-counts rounded. The 4 planned contrasts are the paper route. The other 9 analyzable comparisons are exploratory (sedentary time-of-day differences, Ex at ZT12 vs ZT0, one trt x zt interaction).
  - **GSE178262_wheel** (gastrocnemius, 16 samples, 3 weeks of wheel training). DA mice (daytime wheel access, food restricted to the dark phase) vs CTRL mice (ad libitum night-time wheel access) at ZT4 and ZT16. One joint pydeseq2 model (4 cells of n=4). Both arms exercise, so the estimand is the timing of training (plus the feeding schedule), not exercise vs sedentary (S2.3.p1).
  - Enrichment: Enrichr ORA (GO plus KEGG) and Hallmark GSEA completed for the 6 planned tables. It is separate from the DE result. The paper itself used g:Profiler KEGG.

## Threshold

The paper's rule is FDR <= 0.05 with no fold-change cutoff (S3.3.p2). I applied it as padj <= 0.05, inclusive. A labelled audit rule (padj <= 0.05 and |log2FC| > log2(1.5)) is reported alongside.

## DEG counts vs paper (paper threshold)

| Table | Ours (up/down) | Paper |
|---|---|---|
| treadmill Ex+0h ZT0 vs Sed ZT0 | 1457 (909/548) | in Fig. 5A Venn only, not in the text |
| treadmill Ex+3h ZT0 vs Sed ZT4 | 2335 (1267/1068) | Fig. 5B only |
| treadmill Ex+0h ZT12 vs Sed ZT12 | 912 (589/323) | Fig. 5A only |
| treadmill Ex+3h ZT12 vs Sed ZT16 | 2904 (1449/1455) | Fig. 5B only |
| wheel DA vs CTRL at ZT4 | 2257 (1136/1121) | 2094 (S3.8.p1) |
| wheel DA vs CTRL at ZT16 | 369 (169/200) | 368 (S3.8.p1) |

Qualitative checks against S3.3.p2:
- Agree:
  - The response is larger at Ex+3h after the ZT12 run than at Ex+0h, and at ZT0 the Ex+0h response is larger than the ZT12 Ex+0h response.
  - Maff, Mafk, Mt1 and Mt2 are significant in all four treadmill contrasts.
  - Per1 is induced at ZT0 Ex+0h (log2FC 3.4) and not at ZT12 (padj 0.12).
- Partly disagree: Ciart is induced at ZT0 (log2FC 3.9). At ZT12 it reaches padj 0.004 with a smaller log2FC (1.6), while the paper calls it "not at ZT12".

Wheel experiment:
- Atf3, Per2, Ppargc1a and Ppara are strongly induced by daytime training at ZT4, as the paper reports.
- Klf4, Klf15, Maff and Nr4a3 are significant at both ZTs, but they go up at ZT4 and down at ZT16 for DA vs CTRL. That fits the paper's framing that CTRL mice are the active group at ZT16.
- Klf5 is not significant at either ZT (padj 0.10 and 0.82).

## Deviations (declared)

- pydeseq2 instead of R DESeq2 1.26.0. Fold changes are unshrunk (lfcShrink changes fold changes only, not padj).
- tximport lengthScaledTPM pseudo-counts were rounded to integers.
- Lanes were summed per library. The paper does not say how it handled lanes.
- One joint model per experiment. The paper does not state its model scope.
- Entrez IDs were mapped to symbols.
- The two experiments are separate cases by muscle and design. GEO gives the muscle per experiment, but the paper text does not.

## Tool problems

1. `tools/decision_contract.py:281-285` (`_same_threshold`) treats `effect_metric: null` and `effect_metric: "log2FoldChange"` as different rules, even when both have `effect_cutoff: null` (no fold-change rule). My first execute failed at finish with "applied threshold differs from paper_threshold" after every executor and enrichment had run, so the whole run had to be repeated. The validator should ignore `effect_metric` when `effect_cutoff` is null, or check this before execution.
2. `tools/case_runner.py:804`: `_finish` takes `n_deg` only from an execution with `role == "primary"`. The wheel case's only execution is `secondary`, so its `summary.csv` row has empty `n_deg` and `deg_sanity`, although the tables completed.
3. Interaction enumeration (`tools/suitability.py:214-227`) builds interactions only against the reference level of both factors. In an incomplete layout (Ex3 observed only at Z04/Z16, reference zt = Z00), the scientifically relevant interaction (Ex3:Z16 - Sed:Z16) - (Ex3:Z04 - Sed:Z04), which asks whether the +3h response depends on the time of day, is never listed. Only the Ex0 interaction was available.
4. `case_runner inspect` handles per-lane matrices poorly:
   - It reports `alignment_keys` matched 40/40 metadata vs 80 matrix columns, using the L001 names only. It does not flag that the other 40 columns are second lanes of the same libraries.
   - The L002 names in the GSM descriptions do not match the matrix (`..._1_1_1_..._L002` vs `..._2_1_1_..._L002`), so no key route recovers them.
   - Following the suggested `key_patterns` route would silently drop half the reads. A lane-merge prep script was needed.
5. Minor: the alignment summary prints `n_aligned 40/40` before `exclude_samples` is applied, so the counts do not show the 24 or 16 samples actually analysed per case. The levels table is correct.
