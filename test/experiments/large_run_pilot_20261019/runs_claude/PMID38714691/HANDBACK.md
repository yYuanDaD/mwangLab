# HANDBACK — PMID38714691 / GSE208615

## What ran
- `case_runner inspect GSE208615` → one matrix, `GSE208615_fpkm.csv.gz` (24,346 genes × 70 samples, Tuxedo/cuffnorm FPKM, gene symbols). Columns align exactly to metadata `title` (70/70).
- `case_runner execute case_spec.json` → status completed; the contract validator reported 15 records and 0 errors.
- Decisions:
  - **Samples:** 60 OLM-trained mice in 6 groups of n=10: SED (0-0-0), EX14 (14-0-0), RE2 (0-0-2), EX14D7 (14-7-0), EX14D7RE2 (14-7-2), EX14D14 (14-14-0). I excluded the 10 GEO "HC" samples (0-0-0 with no OLM). The paper's contrasts are all taken 1 h after OLM acquisition (S4.2.8.p1), so HC is not part of them.
  - **Matrix:** FPKM.
  - **Method:** limma-trend on log2(FPKM+1), one model `~ grp` with 5 contrasts vs SED. EX14 and EX14D7RE2 are primary (S2.2.p1); the other three are secondary.
  - **Sensitivity run:** the same model plus `cohort` (harvest day). Harvest day is balanced at 5 per group per day (S4.2.5.p1), so it is not confounded with exercise.
  - **Enrichment:** ORA on up-regulated genes plus Hallmark GSEA, for EX14 and EX14D7RE2.
- **Threshold:** the paper's own rule, uncorrected p < 0.05 with no fold-change cutoff (S4.2.8.p1). It is applied to limma p-values (`paper_on_deviation_route`). BH FDR < 0.05 is reported separately as an audit count.

## DEG counts (p < 0.05, no FC rule) — total (up/down) [audit FDR<0.05]
| Contrast | ours | with cohort covariate | paper |
|---|---|---|---|
| 14-0-0 vs SED | 1543 (1062/481) [8] | 1576 [9] | Fig. 2C/D only, no number in text |
| 14-7-2 vs SED | 1017 (522/495) [7] | 1025 [7] | Fig. 2C/D only |
| 14-7-0 vs SED | 866 (464/402) [0] | 873 | Fig. 2C only |
| 14-14-0 vs SED | 823 (607/216) [0] | 824 | Fig. 2C only |
| 0-0-2 vs SED | 482 (219/263) [0] | 490 | Fig. 2C only |

- **Genes up in both 14-0-0 and 14-7-2:** 273 in our run vs **21 in the paper** (Data Table S1). This is the only numeric paper result we can compare.
- **Named genes, which match the paper's direction:**
  - Acvr1c is up in 14-0-0 (log2FC 0.43, p=8e-4) and in 14-7-2 (log2FC 0.43, p=8e-4).
  - It is not significant in 14-7-0 (log2FC 0.19, p=0.12), as the paper reports.
  - Bdnf is up in 14-0-0 (log2FC 0.55, p=0.012) and in 14-7-2 (log2FC 0.44, p=0.044).
  - Both genes are in our 273-gene intersection.
  - Neither gene passes FDR; the paper's rule is raw p.
- **Enrichment (kept separate from the DE result):**
  - 14-0-0, up-regulated genes, GO cellular component ORA: Lysosome tops the list (adjusted p 4e-7).
  - 14-0-0, Hallmark GSEA: Protein secretion, Fatty-acid metabolism and EMT are enriched (FDR < 0.001).
  - 14-7-2 shows the same pattern more weakly: Protein secretion FDR 0.036, and ER tubular network leads the ORA.
  - The paper used DAVID GO/KEGG and IPA, so these are not directly comparable.

## Deviations
1. **Method:** limma-trend in one six-group model with a pooled variance, instead of the paper's pairwise Cyber-T Bayesian-regularized t. The repository has no Cyber-T executor. This likely accounts for much of the gap between our 273-gene intersection and the paper's 21: a pooled residual variance with 54 degrees of freedom gives more power than pairwise tests with 18.
2. **Low-expression filter:** genes kept at FPKM ≥ 1 in ≥ 10 samples, leaving 13,353 of 24,346. The paper states no filter.
3. **Transform:** log2(FPKM+1).
4. **Excluded samples:** the 10 HC samples (0-0-0 without OLM).
5. **Paper counts:** the per-group DEG counts appear only in figures, so no count-level comparison was possible.

## Tool problems
None blocking. The runner, enrichment and validator all completed without errors. One observation: `paper_counts` was left empty because the paper gives no counts in text, so the runner's `comparison` block is `{}`. The intersection count above was computed by hand from the result CSVs.
