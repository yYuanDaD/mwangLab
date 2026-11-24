# HANDBACK — PMID 41247792 / GSE305038

**Status: stopped at `ownership`, `manual_review` (missing expression matrix). No DE analysis ran.**

The comparison with the paper rests on the **PubMed abstract only** (efetch, saved as `PMID41247792_abstract.txt`) plus the GEO series and sample records. No full text was used.

## What ran
1. `python -m tools.case_runner inspect GSE305038 --data-root E:/agent/mwangLab_pdf/data` failed twice. The GEOparse metadata download hit `[Errno 2] No such file or directory: '...\AppData\Local\Temp\tmpXXXX'`, and the supplementary listing returned `HTTP Error 403`.
2. I fetched the full SOFT text by hand from `www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE305038&targ=all&form=text` and parsed it locally with GEOparse into `data/GSE305038/GSE305038_metadata.csv` (28 samples, 34 columns). The SOFT file is kept as `data/GSE305038/GSE305038_family.soft`.
3. Matrix download attempts all failed with HTTP 403:
   - the series `suppl/` folder;
   - `/geo/series/` and `/geo/`;
   - `geo/download/?acc=...`, which redirects to the FTP host;
   - the NCBI-generated `rnaseq_counts` file;
   - `ftp://` (550).
   - A 15-minute retry loop, one request per minute, got 15 × 403. `ftp.ncbi.nlm.nih.gov/pub/` returned 200, so the block covers the `/geo/` tree only.
4. `case_spec.json` records `paper_reconstruction` (valid) and `ownership` (manual_review). `execute` completed and the validator reported 0 errors (`summary.csv`, `case_runner.log`). `matrix_unavailable.txt` is a placeholder input I created only so the runner could record the stop. It holds no data.

## Study map (abstract + GEO)
- **Design:** human skeletal muscle RNA-seq, randomized crossover, n = 9 (7 M, 2 F).
  - Trials: A (normal activity) and IN (reduced activity, about 3.6k steps).
  - Biopsies before and 4 h after 60 min of exercise at 65% VO2max.
  - Processing: STAR + RSEM, then edgeR v4.0.16 GLM (GEO `data_processing`).
- **GEO samples:** 28 of the 36 possible. A-Pre 7, A-Post 7, IN-Pre 6, IN-Post 8.
  - I03 has no A-trial samples.
  - I05 has no pre biopsies in either trial.
  - I07 has no A-post sample.
  - I09 has no IN-pre sample.
- **Deposited data:** only two xlsx files, `edgeRglm_Counts_Inactive_Post-Inactive_Pre` and `..._Normal_Post-Normal_Pre`. There are no per-sample files.
- **Paper threshold:** not stated in the abstract.

## DEG counts vs paper
| Contrast | Paper (abstract) | Ours |
|---|---|---|
| A: Post vs Pre | 793 | not run |
| IN: Post vs Pre | 1,403 | not run |
| IN vs A at rest | 9 | not run |
| trial × exercise interaction | GSEA only | not run |

## Planned route (not executed)
I did not refuse on scientific grounds: the design supports the exercise estimand. Once the xlsx files are obtainable, the next step is to check whether they hold per-sample counts for all 28 samples. If they do, the plan is:
- one joint model on all samples: `~ subject + trial_time` (DESeq2 or edgeR GLM);
- within-trial Post vs Pre contrasts, with Post vs Pre as the paper-aligned primary contrast;
- the IN vs A contrast at Pre;
- the interaction, as exploratory.

If the files hold only results tables, the case stops at `matrix`.

## Deviations
- The metadata CSV was built from a hand-downloaded SOFT file, not by `download_geo_data`. Its content is equivalent (GEOparse `phenotype_data`).
- A placeholder matrix input was used to let the runner record a stop at `ownership`.

## Tool problems
- **NCBI GEO FTP blocks this machine:** HTTP 403 on everything under `https://ftp.ncbi.nlm.nih.gov/geo/`. This is environmental, not a code bug, but it stops every new download.
- **`tools/geo_tools.py:30`:** `GEOparse.get_GEO(geo=..., destdir=save_dir)` fails with `[Errno 2]` on a `%LOCALAPPDATA%\Temp\tmp*` path, even with TMP/TEMP pointed at the scratchpad. The error message says "ID could be incorrect", which is misleading because the series exists.
- **`tools/geo_tools.py:58-64`:** the supplementary listing reports only `HTTP Error 403: Forbidden`. It has no fallback and doesn't hint that the whole `/geo/` tree is blocked.
- **`tools/case_runner.py:529-530`** (`add_input`, which hashes via `tools/native.py:1049`): the runner needs an existing matrix file even for a case that stops at `ownership` because the matrix is missing. A stopped-at-ownership spec cannot omit `inputs.matrix`, so I used a placeholder.
