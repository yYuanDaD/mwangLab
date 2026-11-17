# HANDBACK: PMID29610328 / GSE101239

Run folder: `test/experiments/large_run_pilot_20261019/runs_claude/PMID29610328`. Spec: `case_spec.json`. The runner finished with status `completed`. The contract validator checked 13 records and found 0 errors. No external LLM calls were made.

## What ran
- **Paper.** Fig. 5 / S1.4.p2 sets the exercise question: 8 weeks of voluntary wheel running in prenatally VPA-exposed mice. The tissue is 12-week dentate-gyrus Nestin-EGFP+ NS/PCs, and the contrast is VPA+RW vs VPA. There is no Ctrl+RW arm. The exercise effect can therefore only be estimated within VPA mice, and a VPA x exercise interaction cannot be estimated.
- **Data.** GSE101239_RAW.tar holds per-sample Cufflinks FPKM files (the 12w file headers end in `_FPKM`). No counts were deposited. Samples were aligned exactly on the GSM index (21/21). The 12 E15 and P5 samples were excluded: those stages have no exercise arm, and the paper analysed each stage separately (S1.2.p1). Analysed: 9 samples at 12w, Ctrl 3 / VPA 3 / VPA+Run 3. Sex was inferred as all female; one sample (GSM2700549) had low confidence.
- **Method.** One limma model, `~ grp`, on log2(FPKM+1) (`run_joint_limma`). It produced three contrasts:
  - VPARun_vs_VPA (primary, exercise)
  - VPA_vs_Ctrl (secondary; the paper's 12w VPA-DEG set)
  - VPARun_vs_Ctrl (exploratory; checks normalisation back to Ctrl)
- **Sensitivity run.** The same model was refitted after keeping only genes with FPKM >= 1 in at least 3 samples.
- **Enrichment.** GSEA (Hallmark) completed on the primary contrast. ORA was attempted but did not run (only 4 DEGs).

## DEG counts vs paper
Paper threshold (S1.2.p1): q < 0.05 and FC >= 1.5. Applied exactly as padj < 0.05 and |log2FC| >= 0.5849625 (`paper_on_deviation_route`).

| Contrast | Ours (up/down) | Sensitivity, FPKM>=1 filter | Paper |
|---|---|---|---|
| VPA+RW vs VPA (exercise) | 4 (1/3): Gjc3, Gm14379, Arhgef4 down; Wipf3 up | 0 | no count reported; "mostly amended" VPA-distorted genes (Fig. 5B) |
| VPA vs Ctrl, 12w | 3 (2/1) | 0 | no 12w count in the text ("hundreds" per stage, S2.p2) |
| VPA+RW vs Ctrl | 1 | 0 | not reported |

Named genes:
- **Cxcr4.** Down in VPA vs Ctrl (log2FC -0.96, p = 0.029, padj 0.82). Up in RW vs VPA (+1.27, p = 0.0086, padj 0.35). The direction matches the paper; the change is significant only at nominal p, not after FDR correction.
- **Cntn2.** Down in VPA vs Ctrl (-0.73, p = 0.014). Up in RW vs VPA (+1.14, p = 0.0016, padj 0.23). The direction also matches.

GSEA, RW vs VPA: E2F targets, G2M checkpoint, MYC targets and mTORC1 are positively enriched (FDR < 0.05). This fits running increasing NS/PC proliferation. These are exploratory results and were not reported by the paper.

## Deviations
- **Method.** The paper's route is Cuffdiff on reads, which is blocked because only FPKM was deposited. limma on log2(FPKM+1) ran instead as a declared deviation. With n = 3 per group, limma is much more conservative than Cuffdiff, so the very small DEG counts are expected. The paper's "hundreds of DEGs" cannot be reproduced from the deposited FPKM.
- **Model.** All three 12w groups were fitted in one model with shared variance; the paper ran separate pairwise Cuffdiff tests.
- **Threshold scope.** The paper's DEG rule was defined for VPA vs Ctrl. The paper never counted VPA+RW vs VPA DEGs, so no count can be compared for the exercise contrast.
- **Fragile result.** The expression filter removes all 4 primary DEGs. One of them, Gm14379, is low-expressed (AveExpr 0.7). The FDR-level signal is therefore fragile and should not be read as a robust exercise signature.

## Tool problems
- `tools/enrichment_tools.py:250`: ORA refuses fewer than ~5 genes. This is expected behaviour but leaves no GO result for the 4-gene list.
- GSEA on the unfiltered table: gseapy warned that 18.96% of the ranking statistics are tied. The ties come from low or zero-expression genes. Building the ranking at `tools/enrichment_tools.py:348` does not filter low-expression genes first.
- limma printed "Zero sample variances detected" warnings on the unfiltered log2(FPKM+1) matrix. These are harmless.
- The data typo "Contol_P5" in the tar file names had no effect, because P5 was excluded.
