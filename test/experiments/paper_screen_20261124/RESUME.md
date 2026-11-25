# Next-batch paper screen, 2026-11-24: paused, how to resume

Goal: about 100 new analysable exercise papers for the next batch run, none of them collected,
screened or run before. The user asked for 100; data type defaults to the approved screener
(bulk RNA-seq, counts route plus TPM/FPKM on the limma route, no microarray). Do not start the
analysis until the user confirms the list. No LLM calls.

Paused by the user at 2026-11-25 01:37 UTC with 353 of 789 papers screened
(shard a 121/263, shard b 122/263, shard c 110/263).

## Done

- `build_exclude.py`: every papers/screen CSV of the 2026-10-17 to 2026-10-28 batches plus the
  211-run queue gives `exclude_papers.csv` (4283 PMIDs) and `exclude_gse.txt` (882 series).
- `harvest.py`: all GEO bulk RNA-seq series (human, mouse, rat) matching 39 exercise-type terms
  (6102), kept only when the GEO title or summary passes a strict exercise regex. 16 new
  GEO-linked papers and 53 papers found through Europe PMC for unlinked series. The GEO-linked
  pool is nearly used up: 105 of the 121 linked PMIDs were already in earlier batches.
- `harvest_epmc.py`: Europe PMC papers with an exercise term in title/abstract whose text
  mentions a GEO accession (`ACCESSION_TYPE:geo`), 720 new.
- `run1_loose/`: the first harvest used the screener's own topic regex. Its first 319 papers
  gave 42 analysable, of which about 38 were not exercise studies (pressure or iron overload,
  trained immunity, aerobic glycolysis). That regex is too loose for GEO records.

## Resume

The screener is the approved one (`git archive 94d6028 tools` extracted to a folder, run from
there) with `E:\agent\mwangLab_pdf\.venv-pdf` (it has docling). From that folder, for each of
`.`, `shard_b`, `shard_c` of this directory:

```bash
PYTHONIOENCODING=utf-8 python -u -m tools.paper_screen screen <dir>/papers_shard.csv --out <dir> > <dir>/screen_log_shard.txt 2>&1
```

Papers already screened replay from `_http_cache/` and `papers/` in seconds. About 1 hour is
left with the three shards in parallel. Then:

1. `python make_list.py` merges the shards, drops series seen before, and writes `new_batch.csv`.
2. Read the group labels and titles: drop papers that are not exercise studies, flag in-vitro
   "exercise mediator" designs (211-run PROBLEM_THEMES #18).
3. Give the user the list (GSE, PMID, species, data type, groups) and wait for the go-ahead.

If the list falls short of 100: the earlier pools excluded about 50 microarray-only and 32
scRNA-seq exercise papers at the data-type layer, and the GEO harvest here was RNA-seq only.
Adding microarray is the user's call.
