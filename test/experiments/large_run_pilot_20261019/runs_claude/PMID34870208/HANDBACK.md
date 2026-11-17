# HANDBACK: PMID34870208 / GSE180877

## What ran
- Case-spec route (`tools.case_runner execute case_spec.json`). There were three re-executions; earlier attempts are under `_previous/`. The contract validator passed with 15 records and 0 errors.
- Data: GSE180877 is whole-plantaris RNA-seq. The matrix is `GSE180877_Raw_gene_counts_matrix.txt.gz`: 20406 genes x 15 samples of Partek estimated counts, with feature IDs taken from `Gene Symbol`. The companion RRBS series GSE180433 was not analyzed because it is methylation, not expression.
- Alignment: each sample's key is its GEO title before the `[mouse id]`. Keys were matched to the matrix headers after normalization: 15/15 exact, no positional matching. Groups also come from the title.
- Method: DESeq2 (pydeseq2 Wald) on rounded estimated counts, with the paper's low-count filter (drop genes whose max count is <= 50). Threshold: padj < 0.05 with no fold-change cutoff, as the paper states (S2.5.p1, S4.1.p1).
- Enrichment ran on the primary contrast. ORA top terms are collagen-containing ECM and ECM organization. GSEA Hallmark top hits are EMT, coagulation and angiogenesis (up). Both agree with the paper's "ECM-related processes" (S2.5.p1).

## DEG counts vs paper (padj < 0.05, no FC cutoff)
| Table | Role | Ours (up/down) | Paper |
|---|---|---|---|
| pair_PoW6_vs_UT6 (6 PoW vs 3 UT) | primary | 298 (180/118) | 297 (179/118) |
| pair_DT9_vs_UT9 (3 vs 3) | secondary | 66 (11/55) | no total given; paper says no PoWeR gene persisted |
| joint_all/grp_PoW6_vs_UT6 (one model, 15 samples) | sensitivity | 386 (215/171) | - |
| joint_all/grp_DT9_vs_UT9 | sensitivity | 19 (2/17) | - |
| triplicate_PoW6_vs_UT6 (3 vs 3, July deposit only) | sensitivity | 95 (61/34) | - |

Persistence: of the 298 PoWeR DEGs, only Dusp7 is also DE after detraining, and its sign is opposite (-0.64 trained, +0.91 detrained). No gene persists in the same direction. This is recorded in the study caveats.

## Deviations and decisions
- The GEO `characteristics: treatment` field is unreliable. It calls 9M UT "Detrained", 9M PoW+DT "Sedentary", and 6M POW4-6 "Sedentary". Groups were taken from the titles, which agree with the matrix headers and with the paper.
- The 6M PoW arm has 6 samples: PoW1-3 plus POW4-6 [LD1-3], which were deposited on Sep 03 2021. The paper says "biological triplicate per group" (S4.p2). My first attempt excluded the LD samples, which gave 95 (61/34) DEGs. I revised the decision because the title and the matrix header both say PoW, the ECM markers in those samples look trained, and the 6-vs-3 fit reproduces 179/118 almost exactly. This revision was informed by the counts, and it is declared in the alignment and design candidates.
- Implementation differences from the paper:
  - pydeseq2 instead of Partek Flow DESeq2;
  - fractional counts rounded before DESeq2;
  - the max-count filter applied within each execution's samples;
  - pairwise fits are primary, and the all-sample joint model is a sensitivity run.

## Tool problems
- `case_runner inspect` returned `alignment_keys: []` (tools/case_runner.py:408, `_key_matches`). It missed that the matrix headers ("6M UT 1") equal the title prefix ("6M UT1 [PoW3]") once case and spaces are ignored; I derived the key by hand with `key_patterns` + `normalize_keys`.
- `inspect` reported `duplicated_feature_ids: 20384` (profile at tools/case_runner.py:399). That count is for the first column, `Chromosome`, not for any gene ID column. Using `feature_column: "Gene Symbol"` found 0 duplicates.
- pydeseq2 printed `RuntimeWarning: overflow encountered in exp` (pydeseq2/utils.py:1088) during fitting. It was not fatal.
