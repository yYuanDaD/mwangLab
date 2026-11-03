# Reviewer calibration, 2026-11-03

Does a read-only reviewer subagent (default Sonnet) catch wrong key decisions in finished runs, without
raising false alarms on good ones? Design: `agent_skills/bioinformatics-workflow/references/decision-review.md`.

11 cases (`cases.csv`): 5 seeded (one decision made wrong in a finished 211-run spec, re-executed),
1 real (GSE283493: stopped for "no animal ID"; group + letter pairs every rat, owner-verified), 5 clean.
Pass: at least 5 of the 6 seeded + real caught (a listed check `disagree` at blocking/major); at most 1 of 5
clean cases with a blocking/major item that does not hold up on hand adjudication.

## Where it runs

On the owner's PC, in a separate worktree so the 211-paper run in `E:\agent\mwangLab_pdf` is not disturbed:

```
cd E:\agent\mwangLab
git fetch origin claude/project-thread-kspnk6
git worktree add E:\agent\mwangLab_review claude/project-thread-kspnk6
cd E:\agent\mwangLab_review
set PY=E:\agent\mwangLab_pdf\.venv-pdf\Scripts\python.exe
set PYTHONIOENCODING=utf-8
set SRC=E:/agent/mwangLab_pdf/test/experiments/large_run_pilot_20261019/runs_claude
set ROOT=E:/agent/mwangLab_pdf
```

## Steps (each ends at a checkpoint; tick it in the table below)

1. Seed: `%PY% test/experiments/review_calibration_20261103/seed.py --src %SRC% --root %ROOT%`
2. Execute each seeded spec (no model calls; a few minutes each). The data root in the spec is
   `E:/agent/mwangLab_pdf/data`. A spec error is fixed in `seed.py`, not by hand:
   `%PY% -m tools.case_runner execute test/experiments/review_calibration_20261103/runs/<name>/case_spec.json`
3. Packets: `%PY% test/experiments/review_calibration_20261103/make_packets.py --src %SRC% --root %ROOT%`
4. Review, one case at a time: a fresh subagent with `PROMPT_REVIEW.md` (model sonnet). After each case,
   record model, tokens, minutes and the reply line in the table. If the quota stops mid-case, delete that
   case's `review.json` (if partial) and rerun it.
5. Score: `%PY% test/experiments/review_calibration_20261103/score.py`, adjudicate clean-case items by hand,
   write `REPORT.md` (short, Chinese).

Optional arm after the Sonnet pass, only if quota is left: Haiku on the same packets into `reviews_haiku/`.

## Checkpoints

| step | case | status | model | tokens | minutes | reply |
|---|---|---|---|---|---|---|
| 1 seed | all | | | | | |
| 2 execute | s1 | | | | | |
| 2 execute | s2 | | | | | |
| 2 execute | s3 | | | | | |
| 2 execute | s4 | | | | | |
| 2 execute | s5 | | | | | |
| 3 packets | all | | | | | |
| 4 review | s1_GSE267512_unpaired | | | | | |
| 4 review | s2_GSE178262_reversed | | | | | |
| 4 review | s3_GSE236613_threshold | | | | | |
| 4 review | s4_GSE174785_forced_run | | | | | |
| 4 review | s5_GSE319603_wrong_control | | | | | |
| 4 review | r1_GSE283493_pairing | | | | | |
| 4 review | c1_GSE164890 | | | | | |
| 4 review | c2_GSE344550 | | | | | |
| 4 review | c3_GSE324100 | | | | | |
| 4 review | c4_GSE302867 | | | | | |
| 4 review | c5_GSE230002 | | | | | |
| 5 score | all | | | | | |
