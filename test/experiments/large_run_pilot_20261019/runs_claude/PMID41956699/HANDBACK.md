# HANDBACK — PMID41956699 / GSE315845

**Outcome: stopped at `ownership`, `manual_review` (missing file).** No differential expression was run.

**The comparison with the paper rests on the abstract only.** No full text was available. The study map comes from the PubMed abstract (`abstract_PMID41956699.txt`, fetched with E-utilities efetch) and the GEO series record (acc.cgi SOFT text).

## What ran
1. `python -m tools.case_runner inspect GSE315845 --data-root E:/agent/mwangLab_pdf/data` failed. GEOparse's SOFT download failed, and `download_supplementary_files` got HTTP 403.
2. I probed the download routes by hand. Every path under `ftp.ncbi.nlm.nih.gov/geo/` returned HTTP 403 over https and http, and FTP 550 over ftp. That included the series tar, the per-sample `GSM*_SED1.txt.gz` files, and an unrelated control series (GSE266241). The `www.ncbi.nlm.nih.gov/geo/download/?acc=...` endpoint redirects to the same blocked FTP path. The FTP root itself returned 200, so the block is on `/geo/` from this host.
3. The GEO web page (`acc.cgi ... form=text view=full`) was reachable. I parsed it with GEOparse into `data/GSE315845/GSE315845_metadata.csv` (9 samples × 37 columns).
4. The Zenodo record the series cites (10.5281/zenodo.19596784) holds only `Supplemental material.docx`, with no count matrix. I did not open it, because the brief limited paper evidence to the abstract and GEO.
5. I wrote `case_spec.json` with `paper_reconstruction` (valid) and `ownership` (owned=true, `manual_review`), then ran `execute`. Validator: 2 records, 0 errors.

## Study map (abstract + GEO)
- Mouse ventral hippocampus, bulk RNA-seq (NovaSeq, STAR on GRCm39 + salmon). GEO `data_processing` says per-sample files hold read counts, with TMM+CPM computed by conorm.
- Groups, n=3 each, single batch: SED (non-stressed, sedentary), SUS (chronic restraint stress, susceptible, sedentary) and SUSLE (susceptible + low-intensity treadmill exercise below the ventilatory threshold).
- Exercise estimand: **SUSLE vs SUS**. It is identifiable from the metadata; with the matrix it would be a DESeq2 `~ grp` model with planned contrasts SUSLE vs SUS (primary) and SUS vs SED (secondary).
- The abstract gives no DEG count, no method and no threshold. It names only "primary cilium-associated gene networks" and lower IL-1α (Il1a) and fractalkine (Cx3cl1) after exercise, without saying which assay measured them.

## DEG counts vs paper
None computed. The paper's count and threshold are unknown because the abstract states neither.

## Deviations
- The metadata CSV was built from acc.cgi SOFT text instead of the GEOparse FTP download. The content is the same GEO record.
- `inputs.matrix` points at `MISSING_MATRIX_GSE315845.txt`. It is a placeholder note, not data, and is never read as a matrix. I needed it only because of the runner limitation below.

## Tool problems
1. **The runner needs a real matrix before the first gate**, so a case cannot be stopped at `ownership` for a missing file.
   - `tools/case_runner.py:529-530` resolves and hashes `inputs.matrix` before `paper_reconstruction` and `ownership` are decided. With `raw_tar: true` it raises `NativeToolError` at `tools/native.py:551`.
   - The spec schema rejects `matrix: null` ("give exactly one of inputs.matrix or inputs.raw_tar").
   - Fix: allow a missing matrix when an early gate is not `valid`.
2. **`inspect` gives a misleading error** when GEO FTP is blocked. The GEOparse note says "No such file or directory: ...\Temp\tmpXXXX" (from `tools/geo_tools.py:13-39`, `download_geo_data`) instead of the HTTP 403. Nothing falls back to the acc.cgi SOFT text.
3. **Environment:** GEO FTP (`/geo/`) is blocked from this host. To unblock the case, put `GSE315845_RAW.tar` in `data/GSE315845/`, set `inputs.raw_tar: true`, and complete the gates from `alignment` onward (key = GSM id; grp from the `description` library name, `SED|SUSLE|SUSSED`).
