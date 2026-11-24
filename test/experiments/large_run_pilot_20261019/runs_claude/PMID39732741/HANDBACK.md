# HANDBACK: PMID39732741 / GSE273795

**Status: refused at the `design` gate.** The data cannot answer the exercise question.

## What ran
- `python -m tools.case_runner inspect GSE273795`: downloaded the series to `data/GSE273795`. The tar merged into 18,705 genes × 6 samples (`*_normalized_counts`).
- `python -m tools.case_runner execute case_spec.json`: the runner recorded paper_reconstruction, ownership, alignment (6/6 exact matches on GSM), matrix, and design (refused). The validator reported 0 errors.
- It ran twice. The first attempt is kept in `_previous/20261124T044942Z`. Its stop_reason called the mice "sedentary-housed", which the paper does not support, since the paper measures voluntary wheel running. I removed that wording and ran it again.

## Why it was refused
- The paper is about a drug: R159, a gp130 Y814 inhibitor, compared with vehicle in aged male mice on a high-fat diet (HFD).
- The only RNA-seq experiment is liver, HFD-R159 vs HFD-Veh, n = 3 per group (Fig. 3e,f; S9.p1).
- Voluntary wheel running appears only as a behavioural outcome (activity and motivation, Fig. legend at paper.md line 63; Discussion line 81). No group is defined by exercise.
- The GEO metadata has a single factor, treatment (HFD, R159 = 3; HFD, Vehicle = 3). With no exercise vs sedentary arm, the exercise estimand cannot be identified. The drug contrast is analyzable, but it does not answer the exercise request, so I did not run it.

## DEG counts vs paper
- None computed, because the case stopped before execution.
- The paper gives no DEG total either. It shows enriched terms and a heat map (Ccl2, Tlr5, Col1a1, Ctsk, Mmp2, Pdgfc, Apob, Lpl, Sele, Vcam1).
- The paper's threshold is raw p < 0.05 and fold change > 1.5, i.e. |log2FC| > 0.5849625 (Methods, RNA-seq paragraph). It was recorded in paper_reconstruction.

## Deviations
- None. No analysis was executed.
- Recorded discrepancy (not evaluated because the case stopped): GEO deposits only median-ratio-normalized EM estimates, not raw counts. I recorded the matrix as `estimated counts` with medium confidence.

## Tool problems
- None blocking.
- Minor: the matrix policy has no type word for already size-factor-normalized counts (a DESeq2 median-ratio matrix), so I used `estimated counts`. See `.claude/skills/bioinformatics-workflow/references/matrix-method-policy.md`, which has no "normalized counts" entry.
