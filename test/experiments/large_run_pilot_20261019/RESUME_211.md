# Run of the remaining 211 analyzable papers (started 2026-10-28)

Branch `claude/project-thread-5415h4` = `claude/project-thread-s8u35g` + the case-spec route
(`claude/project-thread-nnpggo`, PR #6), checked out in `E:\agent\mwangLab_pdf`.

- Queue: `queue_211.csv` (built by `make_queue_211.py` from
  `../paper_screen_20261028/analyzable_combined.csv`, rows with `already_run` False).
  Papers with a local `paper_md` run first; the 21 without full text (Europe PMC has none,
  `fetch_missing_papers.py`) run last from the PubMed abstract and GEO description.
- Each paper is run by one fresh Claude subagent with the prompt in `PROMPT_211.md`, up to 3 at a
  time. Its outputs go to `runs_claude/<paper_id>/`, including `HANDBACK.md`.
- After each paper: `finish_paper.py` appends a row to `runs_claude/progress.csv` (with the
  decision-contract validator result) and a section to `runs_claude/PROBLEMS.md`.

## Resuming

A paper counts as done when its `paper_id` is in `runs_claude/progress.csv`. A paper whose folder
exists but is not in progress.csv was interrupted: move its folder to
`runs_claude/_interrupted/<paper_id>_<time>/` and rerun it.

## Paused 2026-10-28 after 16/211 (owner's request)

Done: queue rows 2–16 and 18 (see `runs_claude/progress.csv`). Next in `run_order_211.txt`: 19.
Nothing was interrupted. Problems seen in 2+ papers but not yet patched (candidates before resuming):
zero-DEG ORA recorded as failed and the ORA status key losing its direction (rows 3, 12, 14);
`alignment.key_patterns` limits (rows 4, 11); no low-count gene filter in the runner or edgeR
(rows 6, 11); `_RAW.tar` members of different types (FPKM + counts) merged into one matrix
(rows 10, 14); inspect not using GEO `data_processing` for the matrix type (rows 8, 13).

Resumed 2026-10-28 20:40 at row 19 (owner: "继续"), after patching the ORA status problem.

Owner 2026-10-28 20:57: "就跑5篇" — read as: this round runs rows 19–23 only, then stops. Row 24
(PMID41835150) had just started and was stopped; its partial folder is in
`runs_claude/_interrupted/` (not committed). Next time start at row 24.
Rows 19–23 finished 2026-10-28 (21/211 done). Next: row 24. Unpatched 2+-paper candidates now also
include `covariate_columns` given as a list crashing DESeq2 (`deseq2_tools.py:105`; rows 19, 23).

Round 3 started 2026-10-29 00:13 (owner: "继续跑5篇"): rows 24–28, after patching the list covariate crash.
Rows 24–28 finished 2026-10-29 (26/211, all VALID).

Owner 2026-10-29 03:35 (via the coordinator, verbatim "先继续用5h额度跑211篇吧"): run continuously, 5 at a
time, until the 5-hour quota runs out; short report after each batch of 5. Started at row 29.
