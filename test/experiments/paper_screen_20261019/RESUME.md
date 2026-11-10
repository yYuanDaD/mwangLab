# Paper screen, 2026-10-19 (stage 3a): paused, how to resume

Paused at 2026-10-18 21:35 UTC because the PC was shutting down. No LLM calls were made.

## Done

- **Tests.** `tools/paper_screen.py` at 7603bcc; `test/unit/test_paper_screen.py` passes 19/19.
- **Collect.** `papers.csv` (committed) holds 1000 papers from six queries:
  - by source: 449 Semantic Scholar, 378 PubMed, 173 GEO-linked;
  - 800 have a PMCID, 553 a PDF URL, and 923 at least one;
  - 145 were also in the 200-paper run.
- **Full-text cache seeded.** `papers/` was seeded from `output/screen_20261018/papers/` and
  `_http_cache/` from `output/screen_20261018/_http_cache/`. The brief named
  `test/experiments/paper_screen_20261017/papers/`, but that folder does not exist.
- **Prefetch stopped partway.** It was stopped at paper 144/1000. 230 `*.paper.json` files
  are cached and all of them parse.
  - One PDF crashed its subprocess (Windows heap error 0xC0000374). Only that paper was lost;
    the batch continued.

Both `papers/` and `_http_cache/` stay on this machine and are not committed (see
`.gitignore`).

## Resume

Run from the repository root (`E:\agent\mwangLab_pdf`, with `.venv-pdf`), with
`PYTHONIOENCODING=utf-8`:

```bash
python -u test/experiments/paper_screen_20261017/prefetch_full_text.py test/experiments/paper_screen_20261019/papers.csv test/experiments/paper_screen_20261019 > test/experiments/paper_screen_20261019/prefetch_log.txt 2>&1
python -u -m tools.paper_screen screen test/experiments/paper_screen_20261019/papers.csv --out test/experiments/paper_screen_20261019 > test/experiments/paper_screen_20261019/screen_log.txt 2>&1
```

Prefetch skips papers that already have `papers/<stem>.paper.json`.

**Estimated time:**
- prefetch: about 3.5 h for the ~720 papers left, 109 of them PDF-only;
- screen: 30–60 min, mostly GEO queries and listing the contents of `_RAW.tar` files.

## Left

1. Finish the prefetch, then the screen.
2. Spot-check 10 papers fresh: up to 5 analyzable papers whose counts come from inside a
   `_RAW.tar`, plus random analyzable or needs_inspection papers.
3. Write REPORT.md: verdict, reason and source counts; yield compared with the 200-paper run;
   the spot-check table; bugs found. Do not change the screening code in this pass.
4. Commit and push (not `papers/` or `_http_cache/`).
