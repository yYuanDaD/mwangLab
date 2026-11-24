# HANDBACK — PMID 34880498 / GSE164401

Paper: *Exercise plasma boosts memory and dampens brain inflammation via clusterin* (PMC9721468).
Status: **finished**. The spec is `case_spec.json`, the records are written by `tools.case_runner execute`, and the contract validator reported 22 records with 0 errors.

## Estimand
This is a plasma-transfer design. Plasma was pooled from male mice that ran on a wheel for 28 d (runner plasma, RP) or from sedentary mice (control plasma, CP). It was infused into young recipients that did not exercise. The exercise comparison the paper intends is RP vs CP, measured in the recipients' hippocampus (S1.p3, Fig. 1h). The result is the effect of exercise-conditioned plasma, not of running itself. That caveat is recorded in the study gate.

## What ran
| Case | Matrix | Model | Contrast | Role |
|---|---|---|---|---|
| GSE164401_HC_RP_vs_CP | `GSE164401_HC_RNAseq_RP_vs_CP.csv` (16 samples, STAR GeneCounts raw counts) | pydeseq2 Wald `~ grp` | RP vs CP | primary, paper_aligned |
| GSE164401_HC_LPS | `GSE164401_HC_RNAseq_LPS_SAL_RP_CP.csv` (31 samples) | one pydeseq2 Wald model `~ grp`, 4 arms | LPS+RP vs LPS+CP | secondary (exercise plasma under LPS) |
| | | | LPS+SAL vs SAL+SAL | secondary (the paper's LPS reference, not an exercise effect) |

Enrichment: GSEA (MSigDB Hallmark, Wald stat ranking) on both RP contrasts. ORA was not run, because the paper's GO analysis used the top 250 or 500 DEGs, not a threshold list.

## Threshold
The paper's rule is DESeq2 Wald **raw P < 0.05 with no fold-change cutoff** (Fig. 1h and Fig. 2b legends), and that is what was applied. The audit rule, BH padj < 0.05, is reported separately. The padj < 0.1 rule in S6.10.p1 covers only the cortex clusterin experiment, so it was not used.

## DEG counts vs paper (raw P < 0.05)
| Contrast | Ours (up/down) | Paper | Audit padj<0.05 |
|---|---|---|---|
| RP vs CP (Fig. 1h) | **1,999** (759 up / 1,240 down = 38% / 62%) | **1,952** (39% / 61%) | 280 |
| LPS+SAL vs SAL+SAL | **4,709** | **4,936** | 2,940 |
| LPS+RP vs LPS+CP | 1,395 (533 / 862) | not stated in text (Supp. Table 4) | 3 |

Gene checks:
- **RP vs CP:** the genes the paper names all go in the stated direction. Tns4, Igsf5 and Ehf are down; Foxo6 and Fam19a2 are up (all P < 1e-4). The paper says Clu does not change with RP; here it has raw P = 0.0055 but padj = 0.14 and log2FC −0.13, so it is a marginal hit under the paper's raw-P rule.
- **LPS+RP vs LPS+CP:** all 9 qPCR-validated genes are down. 8 of 9 pass raw P < 0.05: Myd88, Tlr1, Tlr2, Irak3, Irf9, Stat1, Stat3 and Gfap. **Ifngr1** is the exception (P = 0.33, log2FC −0.06).
- **Reversal:** over the 739 genes with P < 0.05 in both the LPS and LPS+RP contrasts, the correlation of signed −log10 P is **r = −0.47**; the paper reports r = −0.78. The direction agrees, the magnitude is weaker, and the paper's exact gene selection is unknown.
- **GSEA:** in RP vs CP, interferon-γ and interferon-α response are negatively enriched (FDR < 0.001), as are IL6/JAK/STAT3 (FDR 0.002) and coagulation. Inflammatory response trends down but is not significant (FDR 0.13). In LPS+RP vs LPS+CP, IFN-γ, IFN-α, IL6/JAK/STAT3, TNFα/NF-κB and inflammatory response are all strongly negative (FDR ≈ 0). Both agree with the paper's claim that RP dampens inflammation.

## Deviations
- pydeseq2 was used instead of R DESeq2 1.32.
- 27 gene IDs mangled into dates by Excel (`2019-03-xx` / `2019-09-xx`, i.e. MARCH and SEPT genes, including 2 duplicated IDs) were dropped from both deposited matrices before analysis (`prep_drop_excel_dates.py`, outputs in `prepped/`). The original symbols cannot be recovered unambiguously (for example March1 vs Marc1).
- The LPS-experiment contrasts come from one joint 4-arm model. The paper does not say whether it fitted per-pair or joint models.
- The L index in the LPS sample titles (L1–L16, two mice per L) is nested within the arm, so it cannot be adjusted for. It was not modelled, as in the paper. The two columns per L are not technical replicates: on log-CPM Spearman, a column's nearest neighbour is usually a different L.

## Data and tool problems
- **GEO metadata error (data):** `characteristics_ch1.1.treatment` is "RP" for all 31 LPS-experiment hippocampus GSMs (GSM5625049–79), whatever their true arm. Groups were taken from the titles instead. This is recorded as a discrepancy.
- **case_runner, `key_patterns`:** the pattern must match every metadata row, including GSMs that are not in the matrix. A key pattern meant only for the 16 HC samples (`^HC_(...)$`) raised `NativeToolError` at `tools/native.py:392` (`derive_columns`). The workaround was a pass-through pattern, `^(?:HC_)?(.+)$`. A series with mixed sub-experiments needs either a match only over matrix-aligned rows or an "unmatched → null" option.
- **case_runner, `confounding_candidates`:** a free-text value (`"L index in titles"`) caused a bare `KeyError` instead of a spec error naming the field. The value has to be an existing metadata or derived column name.
- Inspect flagged `duplicated_feature_ids: 2` but did not point out that the rows are dates mangled by Excel. That needed a manual check, and there are 27 affected rows, not 2.
