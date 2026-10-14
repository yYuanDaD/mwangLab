# Paper-evidence ablation (2026-10-14)

Question: does giving the contrast validator the article text improve control/treatment decisions over GEO metadata alone, and does structure matter compared with the flat text?

## Setup

- Series: 24 ExerGeneDB GEO series with an open-access Europe PMC article and gold overlap, drawn round-robin over design classes with seed 20261014 (`manifest.json`): 8 simple, 8 multi_strata, 6 multi_time, 2 multi_time_and_strata. Funnel over the 110 GEO series: 21 had no PubMed link, 19 no PMCID, 31 a PMCID but no Europe PMC full text, 39 eligible.
- Model: DeepSeek V4 Pro (the configured provider), structured output, thinking off. 4 arms x 24 series x 3 repeats = 288 calls, all succeeded.
- Every arm gets the production validator inputs (metadata summary, keyword intent, Python proposal); only the paper block differs:
  - `metadata`: no paper text
  - `abstract`: title and abstract
  - `structured`: abstract, Methods, data availability, all tables and figure legends, with block IDs
  - `flat`: the historical flat `.txt` (same 100k-character cap)
- Scoring: `tools.contrast_gold.score_contrast_set` against ExerGeneDB sample roles, as in `exergenedb_gold_contrast_eval`.

## Results (per call, n = 72 per arm)

| arm | correct | wrong (reversed/mixed) | refused | not accepted (manual review) | pairing = required | locators that resolve | mean input tokens | cost (72 calls) | identical triple across repeats |
|---|---|---|---|---|---|---|---|---|---|
| metadata | 68.1% | 9.7% | 22.2% | 22.2% | 30.6% | n/a | 1,757 | $0.07 | 91.7% |
| abstract | 77.8% | 12.5% | 9.7% | 11.1% | 55.6% | 100% | 2,212 | $0.09 | 75.0% |
| structured | 70.8% | 12.5% | 16.7% | 16.7% | 55.6% | 100% | 6,890 | $0.24 | 95.8% |
| flat | 68.1% | 16.7% | 15.3% | 15.3% | 47.2% | 70.2% | 17,178 | $0.56 | 91.7% |

Majority verdict per series, structured versus metadata:

- Better with structured text: GSE140089 (refused to correct; the GEO labels "Basal" / "Post-Training" are only interpretable from the paper), GSE144627 (trained-vs-sedentary to the acute pre/post axis, 0/3 to 3/3 correct), GSE202295 (refused to Basal vs Post; see the gold note below).
- Worse with structured text: GSE117161 (correct to refused; the model read "Basal" as an intensity level, not the sedentary control), GSE51216 (pre/post to athlete vs control, which the paper emphasises).
- Abstract only: GSE195585 is correct only in this arm (0h vs 1h/4h); the other paper arms and metadata refuse.

## Findings

1. At n = 24, paper text does not clearly improve contrast accuracy. The abstract arm is best (+9.7 points correct, -12.5 points refusals) at almost no extra cost; the structured arm is +2.7 points; the flat arm is no better than metadata and has the highest wrong rate.
2. Structure matters for auditability. Structured locators all resolve; 30% of flat-arm locators are invented block IDs, because the flat text has none. The structured arm is also the most stable across repeats and uses 60% fewer tokens than the flat arm.
3. Paper evidence mainly reduces refusals on metadata-poor series and raises the pairing call from 31% to 56%. Where metadata has a subject column shared across arms, every structured call that chose a correct contrast also said pairing is required (15/15; metadata arm 10/14). Pairing has no gold yet, so over-calling is not measured.
4. Some "mixed" verdicts are gold-definition effects, not model errors:
   - ExerGeneDB defines the treatment axis as the acute bout (pre vs post). When a paper's primary comparison is cross-sectional (athletes vs controls, trained vs sedentary), following the paper is scored as mixed (purity about 0.5). This affects GSE51216 and GSE224310 in every arm.
   - GSE202295: 5 GEO "Post" samples are labelled Pre exercise in the gold, so the paper-correct Basal vs Post contrast scores mixed at purity 0.91.

## Estimand-aware rescoring (stage B2, zero new calls)

The same 288 calls, rescored with `test/validation/exergenedb_gold/estimand_annotations.json`. For each series it names the axis the ExerGeneDB labels encode (`acute_bout`, `training`, or `habitual` for cross-sectional groups), the axes the paper itself analyses, pairing gold for each axis, and label corrections. The comparison axis a decision chose is scored separately from its sample labels on that axis (`tools.contrast_gold.score_estimand_decision`); pairing is scored against the gold for the chosen axis. The pairing gold is also copied into `covariance_annotations.csv`.

Annotation summary for the 24 series: gold axis acute_bout 14, training 10. Three papers analyse a second axis: GSE144627 and GSE51216 (habitual: trained or athletes versus sedentary), GSE224310 (training: before versus after 8 weeks, rested). GSE163356's paper analyses training while its GEO deposit and gold are per-session pre/post. Pairing gold: 15 required, 8 not required, 1 unknown (GSE218103 pools samples). GSE202295 has 8 samples whose GEO title and timepoint say post or recovery but which the gold labels control; they are corrected to treatment.

| arm | correct (sample gold) | estimand-correct | gold axis | other admissible axis | labels correct on chosen axis | pairing correct | pairing missed | pairing column right |
|---|---|---|---|---|---|---|---|---|
| metadata | 68.1% | 77.8% | 68.1% | 9.7% | 100% | 86.8% (n = 53) | 11.3% | 66.7% |
| abstract | 77.8% | 90.3% | 81.9% | 8.3% | 100% | 98.4% (n = 62) | 0% | 82.4% |
| structured | 70.8% | 83.3% | 75.0% | 8.3% | 100% | 100% (n = 57) | 0% | 83.3% |
| flat | 68.1% | 84.7% | 72.2% | 12.5% | 100% | 100% (n = 58) | 0% | 80.0% |

Estimand-correct means an admissible axis with correct labels; the rest of every arm is refusals. Pairing is scored on calls whose contrast fell on an annotated axis and whose series has pairing gold; the column check applies only when the subject ID is a metadata column (or its grouped form).

Findings:

1. Every "wrong" call in the first scoring was an axis choice, not a label error. On the axis it chose, every arm's labels are 100% correct: no reversed arms, no contrast that mixes groups on every axis. The wrong calls are GSE144627 and GSE51216 (habitual) and GSE224310 (training), all axes their papers analyse, plus GSE202295, which was a gold error.
2. With axis-aware scoring every paper arm beats metadata (abstract +12.5 points, flat +6.9, structured +5.6), and the abstract arm stays best. The remaining gap to 100% is refusals: GSE1832 and GSE53598 in every arm (the arms exist only in free-text titles), GSE117161 and GSE195585 in most.
3. Paper text fixes the pairing call. The metadata arm misses pairing on GSE144133 (GEO labels the pre/post timepoints 'Untrained'/'Trained', which reads as two groups) and GSE24235 (exercised versus non-exercised arm of the same person). Every paper arm gets both right, and no arm over-calls pairing on the 8 between-animal series; the only over-call is one abstract-arm call that marks the cross-sectional GSE51216 athlete-versus-control contrast as paired.
4. When pairing is required, the named subject column is right 67–83% of the time. The main miss is GSE47881, where the subject column (`patientid`, 45 values) is not in the validator's metadata summary and the model guesses a column name.

Scope: 24 series; the per-call table now also carries `axis`, `axis_admissible`, `label_verdict`, `estimand_correct`, `pairing_verdict`, `pairing_column_ok` (`scored_calls.csv`), and the arm summaries carry the matching rates (`summary.json`).

## Next

- ~~Score the axis separately from the sample labels~~ and ~~fill the pairing gold~~: done in stage B2 above.
- Use title + abstract as the default paper evidence for contrast validation, and the structured sections for design, covariance, and threshold gates where locators are needed. Re-test with a larger set (all 39 eligible series) before changing production.
- 31 of 70 series with a PMCID have no Europe PMC full text; a PDF route (stage D) would cover them.

Files: `manifest.json` (frozen inputs and hashes), `calls.jsonl` (every call with prompt hash, evidence size, output, usage), `scored_calls.csv`, `summary.json`, `pilot_calls.jsonl` (4-series pilot, not part of the results).
