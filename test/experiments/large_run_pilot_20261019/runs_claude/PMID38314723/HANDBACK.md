# HANDBACK — PMID 38314723 (Arrdc2, mechanical load, aging)

**The paper comparison rests on the abstract only.** No full text was available. I used the PubMed abstract (fetched with E-utilities efetch) and the GEO series descriptions, saved under `paper/`. The abstract gives no DEG counts and no DEG threshold.

## What ran
Route: case spec (`case_spec.json`) run with `python -m tools.case_runner execute`. Validator: 25 records, 0 errors. Run status: completed.

| Case | Outcome |
|---|---|
| GSE248869: C2C12 myotubes, Arrdc2 vs GFP adenovirus, 5 vs 5 | **Refused at `alignment`.** The series has no exercise contrast (it is a cell-culture overexpression experiment). Also, the matrix columns (GFP3–7, Arrdc2-6/7/9/10/11) cannot be matched by name to the GSM titles (control 1–5, treatment 1–5). Only a positional mapping would work, and that is not allowed. |
| GSE269698_young_vehicle: young vehicle TA, contraction-stimulated vs contralateral non-stimulated leg, 6 vs 6 | Ran. limma on the deposited rlog values, `~ subject + stim`, plus an unpaired sensitivity run (`~ stim`). |
| GSE269698_aged_vehicle: aged vehicle TA, stimulated vs non-stimulated, 6 vs 6 | Ran. Same model as the young case. |

The exercise-like estimand is the acute response to high-force eccentric contractions, 4 h after electrical stimulation, compared within mouse. The DEX arms of GSE269698 belong to the later papers that the series also cites (PMIDs 39495237 and 40880111), so I left them out.

## DEG counts vs the paper
Threshold: `workflow_default`, BH padj < 0.05 with no fold-change rule. The abstract states no threshold; GEO only says "DESeq2 default, BH FDR".

| Contrast | Ours (paired, primary) | Ours (unpaired, sensitivity) | Paper |
|---|---|---|---|
| Young vehicle Stim vs Non-Stim | 0 | 0 | not given in abstract |
| Aged vehicle Stim vs Non-Stim | 1 (1 up) | 104 (95 up, 9 down) | not given in abstract |

The abstract's only gene-level claim is that increased load lowered Arrdc2 mRNA, but not Arrdc3, in young and aged muscle.
- **Young:** Arrdc2 log2FC −0.04 (p = 0.75). This does not reproduce the abstract's decrease. The young claim may come from qPCR or another cohort.
- **Aged:** Arrdc2 log2FC −0.45 (p = 0.024, padj = 0.20). The direction agrees but it is not significant after FDR.
- **Arrdc3:** not significant in either age (young +0.13, aged +0.21), consistent with "not Arrdc3".

## Deviations
- **Matrix:** only DESeq2 rlog matrices were deposited, with no count table. So I ran limma on the rlog values instead of the paper's DESeq2 on counts (`paper_route` is recorded as blocked). I used the per-pair rlog sheets (`Paired_YVNvsYVS`, `Paired_OVNvsOVS`). I also filtered genes to rlog ≥ 1 in at least 3 samples, which removes the all-zero rows.
- **Pairing is inferred.** The model treats replicate number k as the same mouse (YVNk with YVSk), based on the unilateral design and the "Paired" sheet names; no per-sample mouse ID is given.
  - Young: the residual correlations partly support this pairing.
  - Aged: they do not (OVNk with OVSk ranges from −0.49 to 0.26). GEO also says there were n = 4 aged-vehicle mice, yet 6 pairs are deposited. The aged pairing is therefore doubtful, and the 1-vs-104 gap between the paired and unpaired runs points to mispairing. Of the two aged results, the unpaired one is the more defensible.
- **Young non-stimulated legs** already have high and variable immediate-early genes (Atf3, Fos, Egr1), so the contraction contrast is weak in these data.
- No enrichment was run, since none was requested or described in the abstract.

## Tool problems
- `tools/limma_tools.py:26,115`: `covariate_columns` must be a comma-separated string. Passing a list (the form used for the joint executors) fails with an unhelpful `AttributeError: 'list' object has no attribute 'strip'`. The case runner does not normalise or validate this argument.
- The case runner requires `inputs.paper` entries to be existing files and fails with `FileNotFoundError` on a descriptive string. I fixed this by saving the abstract and GEO text under `paper/`.
- The refused case can only stop at `alignment`, because the runner gates in order. A study with no exercise arm and unmappable column labels cannot reach the `design` gate, which is where the refusal belongs.
