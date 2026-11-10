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
| 1 seed | all | done | | | | 5 specs written |
| 2 execute | s1 | done | | | 1.2 | VALID (11 records); formula ~ time, no subject term; 79 DEG vs paper 214 |
| 2 execute | s2 | done | | | 0.6 | VALID (10); CTRL vs DA, log2FC corr -1.0 with the original run |
| 2 execute | s3 | done | | | 1.1 | VALID (12); padj < 0.05 stated; RE vs NE 5 vs paper 4423 |
| 2 execute | s4 | done | | | 1.6 | VALID (10); soleus vs EDL run, route paper_aligned |
| 2 execute | s5 | done | | | 1.2 | VALID (10); HM vs C primary, paper count 563 taken from HM vs H |
| 3 packets | all | done | | | | built twice: reviews/<name>/ and, for the reviewers, neutral copies from blind.py |
| 4 review | s1_GSE267512_unpaired | done (case_08) | sonnet (requested) | 92819 | 0.9 | OVERALL: fix; DISAGREE: pairing:blocking, model_fit:major, paper_match:major |
| 4 review | s2_GSE178262_reversed | done (case_04) | sonnet (requested) | 107910 | 1.1 | OVERALL: fix; DISAGREE: direction:major (model_fit:minor unsure) |
| 4 review | s3_GSE236613_threshold | done (case_01) | sonnet (requested) | 93949 | 1.1 | OVERALL: fix; DISAGREE: threshold:major, paper_match:major, direction:minor |
| 4 review | s4_GSE174785_forced_run | done (case_07) | sonnet (requested) | 97365 | 1.4 | OVERALL: fix; DISAGREE: run_or_refuse:major, matrix_method:major, paper_match:major (pairing:unsure minor) |
| 4 review | s5_GSE319603_wrong_control | done (case_06) | sonnet (requested) | 93152 | 0.9 | OVERALL: fix; DISAGREE: direction:blocking, paper_match:blocking (model_fit:unsure/minor) |
| 4 review | r1_GSE283493_pairing | done (case_05) | sonnet (requested) | 110899 | 1.5 | OVERALL: fix; DISAGREE: pairing:major, stop_reason:major |
| 4 review | c1_GSE164890 | done (case_11) | sonnet (requested) | 89898 | 0.4 | OVERALL: pass; DISAGREE: none |
| 4 review | c2_GSE344550 | done (case_09; first try stopped by quota before writing, rerun 2026-11-10) | sonnet (requested) | 86464 | 0.5 | OVERALL: pass; DISAGREE: none |
| 4 review | c3_GSE324100 | done (case_10; first try stopped by quota before writing, rerun 2026-11-10) | sonnet (requested) | 103932 | 0.8 | OVERALL: pass; DISAGREE: none (unsure only: model_fit:minor, confounding:minor) |
| 4 review | c4_GSE302867 | done (case_03) | sonnet (requested) | 109815 | 1.4 | OVERALL: human; DISAGREE: none (unsure: paper_match:major, WT_Ex vs WT_Sed Hallmark OXPHOS sign opposite to paper Fig 2e) |
| 4 review | c5_GSE230002 | done (case_02) | sonnet (requested) | 101879 | 1.1 | OVERALL: pass; DISAGREE: none (minor notes: threshold, paper_match, confounding, grouping) |
| 5 score | all | done | | mean 98917 | mean 1.0 | caught 6/6; clean blocking/major 0/5, 0 false alarms after adjudication (REPORT.md) |
