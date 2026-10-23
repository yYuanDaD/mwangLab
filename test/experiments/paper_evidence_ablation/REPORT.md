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

## All eligible series (stage B2)

The draw was extended to every eligible series with the same seed and order (`manifest.json`; `stage_b_series` lists the original 24). Of the 15 new series, GSE158984 (single-cell) has no metadata sample in the gold, so 38 of 39 eligible series are scored. The 14 new series were annotated the same way (11 training, 3 acute bout; 5 with pairing required) and run in all four arms x 3 repeats: 168 new calls, all succeeded, about $0.64. The 288 earlier calls were reused because their prompts are unchanged. Totals below are over 38 series, 114 calls per arm.

One scorer gap surfaced: the sample-gold verdict calls a contrast correct when one arm has no labelled sample. In GSE217155 a metadata-arm call compared normal-diet controls (not in the gold) with exercise on the atherogenic diet, which confounds diet with exercise. The estimand scorer now marks such contrasts `one_arm_unlabelled` and does not count them as correct; the sample-gold column is left as it was for comparability.

| arm | correct (sample gold) | estimand-correct | refused | gold axis | other admissible axis | one arm unlabelled | pairing correct | pairing missed | pairing column right | mean input tokens | cost (114 calls) | identical triple across repeats |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| metadata | 71.1% | 75.4% | 22.8% | 71.1% | 6.1% | 1.8% | 88.2% (n = 85) | 10.6% | 50.0% | 1,711 | $0.11 | 92.1% |
| abstract | 80.7% | 88.6% | 11.4% | 83.3% | 5.3% | 0% | 95.9% (n = 98) | 3.1% | 70.0% | 2,151 | $0.14 | 84.2% |
| structured | 76.3% | 84.2% | 15.8% | 78.9% | 5.3% | 0% | 100% (n = 93) | 0% | 62.5% | 7,770 | $0.42 | 97.4% |
| flat | 74.6% | 85.1% | 14.9% | 77.2% | 7.9% | 0% | 100% (n = 94) | 0% | 57.1% | 18,214 | $0.93 | 94.7% |

Findings over 38 series:

1. The 24-series conclusions hold. Labels on the chosen axis are always correct except the one confounded metadata call; every remaining non-correct call is a refusal. Abstract is the most accurate arm (+13.2 points estimand-correct over metadata), structured and flat are close to each other (+8.8 and +9.7), and structured is the most stable across repeats.
2. Pairing: structured and flat text are 100% correct on 93–94 scorable calls. The metadata arm misses GSE144133, GSE24235 and GSE27536 (pre/post timepoints labelled 'Untrained'/'Trained' or 'Sedentary'/'Trained', and an exercised versus non-exercised limb). The abstract arm still misses GSE27536, where the pre/post design is stated only in Methods (S2.4.p1). Only one call over-calls pairing.
3. Pairing columns are often unnameable. The validator's metadata summary drops high-cardinality columns, so subject-ID columns with many subjects (GSE47881 `patientid`, GSE27536 `individual`, GSE156247 `subject id`) never reach the model, which then guesses a column. The model names the right column whenever the summary shows it.
4. Four series are refused in every arm: GSE1832, GSE53598, GSE92719 and GSE115645. Their arms exist only in per-sample titles or descriptions that the summary cannot group. GSE53598 and GSE156247 are the same article and subjects; GSE156247 exposes time point and subject as columns, and every arm gets it right. Paper text cannot fix this, because the contrast must name a metadata column and values.

What this means for production (not changed yet): pass title + abstract by default; add Methods (structured, with block IDs) when the design or pairing decision needs it, since it is what fixes GSE27536; and change the metadata summary to keep subject-like columns (name, number of subjects, whether IDs recur across groups) and to expose arm tokens embedded in per-sample titles. Those two summary changes target the remaining pairing-column and refusal errors, which paper text does not fix.

## Codex as the decision model (ultra paused)

The same prompts, unchanged, sent to the local Codex CLI with `run_arms.py --backend codex-cli`. The CLI is signed in with a ChatGPT plan, so these calls use plan quota, not API billing. The model is `gpt-6.1-sol`, run with the Codex app's bundled CLI 0.162, because the PATH install (0.154) rejects that model on a ChatGPT account. Each call runs in a fresh, empty, read-only directory outside the repository with a strict output schema, so the model sees only the prompt. No call ran a shell command. Codex adds about 16k tokens of its own context to every call, so its token counts are not comparable with DeepSeek's. Two reasoning efforts were run: `low` (complete, 456 calls) and `ultra` (the user's Codex default; metadata arm complete, the three paper arms partial at the time of writing). Files: `calls_codex_<effort>.jsonl`, `scored_calls_codex_<effort>.csv`, `summary_codex_<effort>.json`.

All 38 series, 114 calls per arm (Codex ultra paper arms not yet run on all series):

| arm | estimand-correct: DeepSeek | Codex low | Codex ultra | refused: DeepSeek | Codex low | pairing correct: DeepSeek | Codex low | pairing abstained (unknown): Codex low |
|---|---|---|---|---|---|---|---|---|
| metadata | 75.4% | 86.0% | 86.8% | 22.8% | 13.2% | 88.2% | 74.0% | 22.9% |
| abstract | 88.6% | 89.5% | partial | 11.4% | 10.5% | 95.9% | 92.9% | 4.0% |
| structured | 84.2% | 89.5% | partial | 15.8% | 10.5% | 100% | 100% | 0% |
| flat | 85.1% | 89.5% | partial | 14.9% | 10.5% | 100% | 100% | 0% |

The 13 series that the paused ultra run finished in every arm (39 calls per arm), estimand-correct:

| arm | DeepSeek | Codex low | Codex ultra |
|---|---|---|---|
| metadata | 74.4% | 92.3% | 92.3% |
| abstract | 89.7% | 92.3% | 92.3% |
| structured | 84.6% | 92.3% | 92.3% |
| flat | 87.2% | 92.3% | 89.7% |

Cost and time per call: Codex low averages 18k–35k input tokens and 11–14 s; Codex ultra averages 47k input tokens and 31 s on metadata and 130k–184k input tokens and 76–101 s on the paper arms, against 1.7k–18k tokens and 2–3 s for DeepSeek.

Findings so far:

1. Codex low does better than DeepSeek on metadata alone: it refuses less (13.2% against 22.8%) at the same label accuracy. With any paper text, all Codex low arms reach the same 89.5%. The remaining 10.5% is the four series whose arms exist only in per-sample titles (GSE1832, GSE53598, GSE92719, GSE115645), refused in every arm. That is the same summary limitation as with DeepSeek.
2. On the chosen axis, Codex labels are always correct apart from one metadata-arm call that repeats DeepSeek's GSE217155 diet confound. Its other-axis picks are the paper-supported ones (GSE224310 training, GSE144627 and GSE51216 habitual).
3. On metadata, Codex answers pairing `unknown` far more often than DeepSeek (22.9% low, 30.2% ultra), rather than guessing. When it does commit to an answer it is rarely wrong (3.1% missed). With structured or flat text it is 100% right, as DeepSeek is.
4. Codex names the subject column a little more often than DeepSeek (metadata 76.9% against 50.0%), but it hits the same wall: high-cardinality subject columns are missing from the summary.
5. Ultra so far gives no accuracy gain over low on the matched series. It costs about 3–5 times the input tokens and 3–7 times the wall time.

**Resume mark (2026-10-14, paused at the user's request).** Ultra stopped at 239 of 456 calls, with none failed. Metadata is complete (114). The paper arms have abstract 42, structured 42 and flat 41 calls, covering the first 14 manifest series. The log resumes from completed calls; run this to finish it:

    python test/experiments/paper_evidence_ablation/run_arms.py --backend codex-cli --codex-effort ultra --arms abstract structured flat --workers 4

The remaining 217 calls take about 1 h 15 min at about 21 s per call with 4 workers. After they finish, refresh the ultra columns above.

## Next

- ~~Score the axis separately from the sample labels~~ and ~~fill the pairing gold~~: done in stage B2 above.
- Use title + abstract as the default paper evidence for contrast validation, and the structured sections for design, covariance, and threshold gates where locators are needed. ~~Re-test with all 39 eligible series~~: done above; the recommendation stands.
- Keep subject-like columns and per-sample arm tokens in `summarize_metadata_for_llm` (see the 38-series findings 3 and 4), then rerun this ablation.
- 31 of 70 series with a PMCID have no Europe PMC full text; a PDF route (stage D) would cover them.

Files: `manifest.json` (frozen inputs and hashes), `calls.jsonl` (every call with prompt hash, evidence size, output, usage), `scored_calls.csv`, `summary.json`, `pilot_calls.jsonl` (4-series pilot, not part of the results).
