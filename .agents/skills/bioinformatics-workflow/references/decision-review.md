# Decision review

A second, read-only pass over one finished case. The reviewer did not run the analysis and does not change it: it checks the key decisions against the paper and the data, and writes `review.json`. The analysis agent (or a person) acts on it.

## Before the reviewer starts

The orchestrator builds the packet (no model call):

```bash
python -m tools.case_review packet <run_dir>/<case_id> --out <review_dir> --paper <paper.md> [--spec <run_dir>/case_spec.json]
```

`<review_dir>` holds `packet_A.md` (facts only), `packet_B.md` (the analysis' decisions and mechanical flags) and `flags.json`.

## Order of work

1. **Blind answers.** Read `packet_A.md` and the paper (Methods, the figure legends and the results paragraphs that give DEG numbers; use the outline in packet A and search the paper, do not read it end to end). Answer, with paper locators:
   - B1 Should this series be analyzed for an exercise question at all? Which sequenced samples carry the exercise factor?
   - B2 The paper's main comparisons: which groups, how many samples each.
   - B3 Repeated measures: is any animal or person sampled more than once (time points, tissues, limbs, fractions)? Which data field could identify it? Use the candidate pairing keys in packet A.
   - B4 Model fit: one model on all samples, or each pair of groups fitted alone? Quote the sentence, or say the paper does not say.
   - B5 The paper's DEG rule, verbatim (FDR or raw p, fold-change cutoff and how it is written, inclusive or not), and the counts it reports.
   Write these into `blind` before you open packet B.
2. **Compare.** Open `packet_B.md`. For each check below, compare your blind answer and the paper with the decision. Open `case_spec.json`, `suitability/suitability.md` or result tables only to settle a specific point.
3. **Write** `review.json` and `review.md` in `<review_dir>`. Do not edit any other file.

## Checks

| id | Question | Typical error |
|---|---|---|
| `run_or_refuse` | Does the decision to run or refuse match B1? Are in-vitro "exercise mediator" designs labelled as such? | A series with no exercise arm analyzed; or refused although the metadata carry exercise groups |
| `grouping` | Are the samples in each level the paper's group, with the paper's n? Is every exclusion named with a reason? Is the control the paper's control for this contrast? | GEO field mislabelled or shifted by one sample; exclusion inferred without saying so; the exercise arm compared with the control of another condition (HFD + exercise vs chow instead of vs HFD), which confounds a second factor: report it under `grouping` |
| `direction` | Is each contrast exercise (or treatment) versus its control, as the paper reports it? | Non-reference pair ordered alphabetically, so signs flip |
| `pairing` | When B3 finds repeated samples, does the model block on the unit (or does the record say why it cannot)? Are numeric IDs treated as categories? | Subject left out; two tissues of one rat treated as independent; numeric IDs fitted as a slope |
| `model_fit` | Does the fit structure follow B4? When the paper is silent and counts differ a lot, are both fits reported? | Joint model where the paper fitted pairs, or the reverse |
| `confounding` | Is any batch, housing, sex or counting run aliased with the exercise factor, and is it recorded? | Exercise group singly housed; two counting runs split by group |
| `matrix_method` | Do the matrix values match the stated type (counts, estimated counts, RPKM)? Rounding, TMM, p-value histogram? | File named raw counts holds RPKM; voom without TMM piles p near 1 |
| `threshold` | Is the paper's rule transcribed exactly (B5)? If another rule fits the paper's numbers (packet B table), is that recorded as a discrepancy rather than silently used or ignored? | FDR written where the paper used raw p; FC 1.5 rounded |
| `paper_match` | Do "ours vs paper" pairs compare the same contrast at the same rule? Does HANDBACK claim more than the numbers show? | Paper count taken from a different comparison |
| `stop_reason` | For every stop or refusal: is the stated reason true, and was it established by a check wide enough to support it? | "No animal ID" after testing the replicate letter alone, while group + letter pairs every sample once |

### Stop reasons that say the data lack something

"No animal ID", "no exercise arm", "no raw counts", "n < 3" are claims that something is absent. They are often wrong because the search was narrow, not because the data lack it. For each such claim:

- Look at packet A's candidate pairing keys, exercise words per column, and the file list. A key with no duplicates in a level that links most samples is a candidate unit; the expression check (`tools/pairing_check.py`), when present, says whether same-key pairs correlate more than others. Support from the data does not prove the key; no support does not disprove it.
- Verdicts:
  - the reason holds: `agree`;
  - the reason is wrong but stopping is still right (the key is plausible but undocumented): `disagree`, severity `major`, `fix` = the corrected stop reason, the candidate key, and what would confirm it (a supplementary figure, the authors);
  - the candidate is well supported (the paper says the samples come from the same animals, the key pairs every sample once, the expression check supports it): `disagree`, severity `major`, `fix` = run the analysis with that key as a labelled assumption, as a sensitivity analysis next to the stopped primary record.

## Severity and the overall verdict

- `blocking`: the reported result answers a different question or is statistically invalid (wrong samples, reversed sign, no exercise arm, unpaired repeated measures).
  - A reversed sign of a reported contrast is blocking even when the DEG set and counts are unchanged: every direction-dependent statement (up, down, pathway sign) is wrong.
  - A series without an exercise arm reported as an exercise result is blocking; a caveat does not lower it.
- `major`: the result stands but a stated decision, reason or number is wrong and changes interpretation (threshold transcribed wrongly, wrong stop reason, missing confound note).
- `minor`: wording, a missing locator, a cosmetic mismatch.

`overall`:
- `pass`: no blocking or major item.
- `fix`: at least one blocking or major item with a concrete `fix` (a spec field and value, or an execution to add).
- `human`: a blocking or major item you cannot settle from the files, or an open policy question.

Open policy questions are not errors: report them under `human_items` unless the case contradicts a rule the skill states. Currently open: which threshold to report when the paper's numbers fit another rule than the one it states; whether in-vitro exercise-mediator series count as exercise studies; joint versus pairwise fits when the paper is silent.

## review.json

```json
{"case": "<case_id>", "reviewer": "<agent and model>",
 "blind": {"B1": "...", "B2": "...", "B3": "...", "B4": "...", "B5": "..."},
 "checks": [{"id": "pairing", "verdict": "agree|disagree|unsure|na", "severity": "blocking|major|minor|none",
             "evidence": "paper locator or file and value", "fix": "concrete change, or empty"}],
 "overall": "pass|fix|human",
 "human_items": ["..."],
 "summary": "two or three sentences in Chinese"}
```

All ten checks appear, in the order above. `review.md` is the same content in Chinese for a person: the overall verdict first, then only the `disagree` and `unsure` items.

## After the review

- `pass`: record and continue.
- `fix`: send the `fix` items to the analysis agent once. It applies them and runs `execute` again, or answers in writing why not. Do not loop: anything still disputed goes to the person.
- `human`: add the items to the run's review queue for the person.
