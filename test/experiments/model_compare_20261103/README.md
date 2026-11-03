# Model comparison on the case-spec route (2026-11-03)

Purpose: compare Sonnet, Haiku and Opus as the decision-maker on the bioinformatics-workflow case-spec route. Checkpoint 1 is the Sonnet batch only.

Pinned commit: 2621f3a204e972372d1c7552320f99bb1ab20cc1 (worktree E:\agent\mwangLab_mc, branch claude/project-thread-57ll9p). Python and GEO data come from E:\agent\mwangLab_pdf (.venv-pdf, data/).

Test set (rows of `large_run_pilot_20261019/queue_211.csv`):

| n | paper_id | GSE | expected |
|---|---|---|---|
| 24 | PMID41835150 | GSE319603 | run |
| 2 | PMID39393048 | GSE267512 | run |
| 27 | b06f79d81bb9463e3b902b4b8b96b865e96758a2 | GSE164890 | run |
| 18 | PMID34142717 | GSE178262 | run |
| 8 | PMID34358431 | GSE174785 | refuse |
| 13 | PMID42679010 | GSE344550 | refuse |

Reference: the Opus runs in `E:\agent\mwangLab_pdf\test\experiments\large_run_pilot_20261019\runs_claude\<paper_id>`.

Prompts: `build_prompts.py` applies the same edits to `prompt_for.py` output and saves `prompts/<paper_id>.txt`. `<model>` in a prompt is replaced by the model name at launch; nothing else differs between models.

Scoring: `score.py` (no LLM) writes `scores.csv` and `scores.md`: run vs refuse, per-comparison decisions (groups, direction, design, method, thresholds), DEG counts vs Opus and the paper, the decision-contract validator, and reads of forbidden paths in the subagent transcripts.

Agent metrics and three-line replies are in `results.csv`.

## Notes on checkpoint 1 (Sonnet)

- Row 18 was first launched with a title the coordinator typed from memory instead of the saved prompt. It was stopped before it wrote anything and rerun with the exact prompt; only the rerun is recorded. All six recorded runs match `prompts/`.
- Rows 27 and 8 did not use `case_runner` (no `case_spec.json`). `score.py` reads those from `decisions.json` and `summary.csv`, and reports the route. Up/down counts for row 27 come from its HANDBACK.
- Row 8 rewrote `data/GSE174785/GSE174785_merged_from_tar.csv` in the shared data root (git-ignored cache, tool behaviour during tar handling).
- Opus tokens and minutes come from `runs_claude/progress.csv`. Rows 2 and 18 were rerun there, so those figures may not cover the earlier passes. The Opus runs used earlier code than the pinned commit.
- `transcripts.csv` paths are local to this machine; the transcripts are not committed. `runs/.gitignore` keeps matrices and result tables out of git, so `score.py` needs the local run directories.
