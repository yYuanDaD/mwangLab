# Paper screen, 2026-10-17: status and how to resume

Query `"exercise gene expression"`, up to 2026, 200 papers. Tool: `tools/paper_screen.py`.
No LLM calls were made.

## Done

1. **Collect.** 200 papers: 99 from Semantic Scholar, 101 from PubMed.
   - 154 have a PMCID, 101 have a PDF URL, and 178 have one or the other.
   - The file is `papers.csv`.
2. **Two collect bugs fixed**, with a regression test (`test/unit/test_paper_screen.py`, 9/9):
   - Semantic Scholar answered every anonymous request with HTTP 429, and `collect` dropped it
     silently. The first run was 100% PubMed. The tool now sends `S2_API_KEY` when it is set,
     backs off 20/40/60 s on a Semantic Scholar 429, and warns when the source fails.
   - `--max` was applied per source, which gave 381 rows. It is now the total. Sources alternate,
     and a duplicate fills in the kept row's missing PMCID or PDF URL.
   - The PubMed query now also honours `--end-year`.
3. **Screen.** All 200 rows are in `screen.csv` and `screen_summary.md`.

| Verdict | Papers |
|---|---:|
| analyzable | 7 |
| needs_inspection | 27 (23 of them are PDF download errors, see below) |
| excluded | 166 |

| Excluded because | Papers |
|---|---:|
| no_own_deposit | 81 |
| no_full_text | 50 |
| data_on_request | 14 |
| unsupported_data_type (mostly microarray) | 14 |
| non_geo_repository | 4 |
| normalized_only | 3 |

Full text came from Europe PMC JATS for 116 papers and from a PDF for 11. The other 73 had no
readable full text.

## Crash workaround used for this run

The in-process `screen` died twice at paper 99 with exit code 127 and no traceback, while
docling was converting a PDF. Converting that same PDF on its own works. I filled the
full-text cache with one subprocess per paper (`prefetch_full_text.py`), then reran `screen`,
which read every paper from the cache. `tools/paper_screen.py` itself was not changed for
this.

## Rerun or resume

Run from the repository root, with `PYTHONIOENCODING=utf-8`. Set `S2_API_KEY` for `collect`.

```bash
python -m tools.paper_screen collect "exercise gene expression" --out output/screen_20261017 --max 200 --end-year 2026
python -u test/experiments/paper_screen_20261017/prefetch_full_text.py output/screen_20261017/papers.csv output/screen_20261017
python -u -m tools.paper_screen screen output/screen_20261017/papers.csv --out output/screen_20261017
```

Both steps skip work that is already cached:
- prefetch skips papers that already have `papers/<stem>.paper.json`;
- `screen` reads GEO and E-utilities responses from `_http_cache/`.

A rerun on this machine takes minutes.

## Left for the next stage (not started)

1. **Spot-check** at least 12 rows by hand: at least 4 analyzable, 3 needs_inspection, and 5
   excluded with different reasons. Record whether each verdict and reason is right.
2. **Fixes**, with tests, for these leads I noticed but did not check:
   - **PDF 403s.** 23 of the 27 `needs_inspection` rows are
     `error:HTTPError: 403 Forbidden` from publisher or Europe PMC PDF links (Wiley, Cell,
     Science, eScholarship). `load_full_text` should treat a 403 as no full text
     (`no_full_text:pdf_forbidden`) rather than an error. `Http.get` raises on 403 and caches
     nothing.
   - **Own vs cited.** GSE97084 is called analyzable for three different papers
     (PMID31980607, PMID40613684, PMID37318869), so it is probably a reused public dataset.
     Only Results-only mentions are checked for "downloaded / publicly available" phrasing;
     Methods mentions are always counted as the paper's own.
   - **Prefetch failures.** 23 prefetch subprocesses exited with code 1, mostly the same 403s.
     Check that none of them is a parser crash.
   - **Several unsupported types.** When a paper has several unsupported data types, the
     reason names only one of them, for example `methylation` for a methylation +
     microarray paper.
3. **REPORT.md**, with the summary tables, the spot-check table and the known limitations.
