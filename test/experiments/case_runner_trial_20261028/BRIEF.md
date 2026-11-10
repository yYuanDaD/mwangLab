# Case-runner trial: one paper from the 45-paper run, redone with the case spec route

Goal: measure tokens and turns for one paper with the rewritten skill (`references/case-spec.md`,
`tools/case_runner.py`) against the same paper in the 2026-10 large run, where its subagent used
166,399 final-context tokens, 28 turns, 21,807 output tokens and 3.63 M cache-read tokens
(PMID42155766, GSE304653; result then: 79 / 281 DEGs for the two sorted fractions vs the paper's
87 / 293).

## How to run (Remote Control session on the PC)

1. Worktree `E:/agent/mwangLab_tokens` on branch `claude/project-thread-nnpggo`, pulled.
2. Launch **one subagent** (general-purpose, same model as the large run) with the prompt below,
   verbatim. Do not help it during the run; only wait for its handback. Record wall time.
3. After it finishes, from `E:/agent/mwangLab_tokens`:
   `python test/experiments/token_breakdown_20261028/extract_usage.py --match case_runner_trial_20261028 --out test/experiments/case_runner_trial_20261028`
   and report the subagent's row of `transcripts.csv` (turns, final_context, sum_output,
   sum_cache_read, sum_cache_creation) plus its tool-call count by tool. Do not commit
   `calls.csv` or `transcripts.csv` (they hold command text).
4. Commit the run folder (`test/experiments/case_runner_trial_20261028/PMID42155766`, csv/gz
   excluded by `.gitignore`) and push.

## Subagent prompt

```text
Environment: repository checkout E:\agent\mwangLab_tokens (do not commit, push or switch branches). Run every command from E:\agent\mwangLab_tokens with E:\agent\mwangLab_pdf\.venv-pdf\Scripts\python.exe and PYTHONIOENCODING=utf-8. Cached GEO data are in E:\agent\mwangLab_pdf\data (pass --data-root E:/agent/mwangLab_pdf/data to inspect; do not download into this checkout). Paper files: E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC13319373.paper.md and .paper.json. Do not open anything under test\experiments\large_run_pilot_20261019 or test\experiments\case_runner_validation_20261028 (earlier runs of this and other papers).

Task: load the bioinformatics-workflow skill (E:\agent\mwangLab_tokens\.claude\skills\bioinformatics-workflow\SKILL.md) and follow it. Analyze GSE304653 for PMID 42155766 (Exercise suppresses breast cancer and reprograms the immune tumor microenvironment, cancer cell intrinsic features, and their interaction): how exercise affects gene expression as the paper intends. Run directory: test/experiments/case_runner_trial_20261028/PMID42155766 (case_runner_trial_20261028). Skip the preflight. You make every scientific decision; when done, hand back a short summary: what ran, DEG counts vs the paper's, deviations, and anything in the tools that got in your way.
```
