# HANDBACK — PMID34144055 / GSE168409

**Outcome:** stopped at the `ownership` gate with `manual_review`. No differential expression ran because the expression matrix could not be downloaded. This is not a refusal: the design does support an exercise comparison.

**Paper basis:** no full text was available. Everything said here about the paper rests on the **PubMed abstract only** (efetch, saved as `PMID34144055_abstract.txt`) plus the GEO series description and `data_processing` fields.

## What ran
1. `tools.case_runner inspect GSE168409` failed. GEOparse's SOFT download hit a temp-file error, and the supplementary download returned HTTP 403.
2. Manual checks:
   - `ftp.ncbi.nlm.nih.gov/geo/...` returns **HTTP 403** over both HTTPS and FTP (curl rc=9). This also happened for an unrelated directory (`GSE166nnn/`), so the block is environment-wide, not specific to this series.
   - `www.ncbi.nlm.nih.gov/geo/download/?...&format=file` returns a **reCAPTCHA** page.
   - `acc.cgi` text view worked. I saved the full SOFT as `data/GSE168409/GSE168409_family.soft` and built `data/GSE168409/GSE168409_metadata.csv` from it with GEOparse (117 samples × 34 columns).
3. The case spec (`case_spec.json`) recorded `paper_reconstruction` (valid) and `ownership` (manual_review). `execute` finished: 2 records, 0 validator errors, route `stopped`.

## The design the data would support (for the rerun)
- 117 PBMC RNA-seq samples (GPL21290, human). Two conditions, Gulf War Illness (GWI) patients and healthy controls (HC), each sampled at three time points: T0 (baseline), T1 (peak exercise, VO2max) and T2 (4 h recovery).
- Samples per condition and time: GWI 20/18/20, HC 19/20/20. Every cell has n ≥ 18.
- **Exercise estimand:** T1 vs T0 and T2 vs T0 (and T2 vs T1) within each condition, plus the condition × time interaction. The GWI vs HC comparison at each time point is a disease contrast, not an exercise effect.
- **Repeated measures:** GEO has no subject key. The per-sample file names carry consecutive tube numbers (2659hG0, 2660hG1, 2661hG2, 2662hH0, 2663hH1, 2664hH2, …). These look like GWI/HC triplets, but the pattern breaks where samples are missing. Confirm the pairing before using a subject block. Without it, the analysis would have to be unpaired and labelled as such.
- **Matrix:** the deposited `GSE168409_HISAT2_forDS.csv.gz` holds raw HISAT2 counts, already filtered (count ≥ 10 in all samples of at least one group). The `_RAW.tar` holds per-sample HTSeq counts. Either fits DESeq2.

## DEG counts vs the paper
- Ours: none (not run).
- Paper: the abstract gives no DEG counts or gene names.
- Paper threshold (GEO data_processing) is a consensus across three aligners (GSNAP, HISAT2, STAR). A gene counts as differentially expressed if either:
  - FC > |1.5| and FDR < 0.10 in one aligner, and FC > |1.4| and FDR < 0.15 in the other two; or
  - FC > |1.5| and FDR < 0.10 in two of the three.
- Only HISAT2 counts are deposited, so this rule cannot be reproduced exactly. The nearest single-aligner rule is FDR < 0.10 and |log2FC| > 0.5849625. That would be a declared deviation.

## Deviations
- The metadata CSV was built from the SOFT text fetched via `acc.cgi`, not from the usual FTP download.
- `inputs.matrix` points at a placeholder file, `GSE168409_matrix_UNAVAILABLE.txt`, that states the matrix is missing (see tool problem 2). It is not data.

## Tool problems
1. `tools.case_runner inspect` → `download_geo_data` (tools/geo_tools.py) failed with `[Errno 2] No such file or directory: ...\Temp\tmpXXXX` even with TMP/TEMP redirected. The underlying cause was probably the GEO FTP 403. The temp-file error hid it.
2. `tools/case_runner.py:529-530`: `run()` registers the matrix input (and hashes it via `tools/native.py:76`, `sha256`) before any gate is decided. A case that should stop at `ownership` because the matrix is missing therefore crashes with FileNotFoundError and records nothing. It should allow a missing matrix when the case stops at or before `ownership`.
3. Environment: GEO FTP (HTTP 403) and the GEO download page (reCAPTCHA) are blocked from this machine.

## To unblock
Place `GSE168409_HISAT2_forDS.csv.gz` (or `GSE168409_RAW.tar`) in `data/GSE168409/`. Restore `inputs.matrix`, then add the gates from alignment onward:
- condition × time factors;
- a confirmed subject key;
- `run_joint_deseq2` or a DESeq2 model `~ subject + time` within each condition, plus an interaction model.
