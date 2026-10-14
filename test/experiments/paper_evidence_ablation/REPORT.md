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

## Next

- Score the axis separately from the sample labels. Add an estimand field (acute bout, training, cross-sectional) to the gold, so a paper-aligned cross-sectional contrast is not counted as a reversal.
- Fill `covariance_annotations.csv` for the 24 frozen series to measure the pairing calls.
- Use title + abstract as the default paper evidence for contrast validation, and the structured sections for design, covariance, and threshold gates where locators are needed. Re-test with a larger set (all 39 eligible series) before changing production.
- 31 of 70 series with a PMCID have no Europe PMC full text; a PDF route (stage D) would cover them.

Files: `manifest.json` (frozen inputs and hashes), `calls.jsonl` (every call with prompt hash, evidence size, output, usage), `scored_calls.csv`, `summary.json`, `pilot_calls.jsonl` (4-series pilot, not part of the results).
