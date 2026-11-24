# HANDBACK — PMID 32483463 / GSE128651

**Status: stopped. `manual_review` at the `ownership` gate.** No differential expression ran.

## What ran
- `python -m tools.case_runner inspect GSE128651 --data-root E:/agent/mwangLab_pdf/data` ran twice and failed both times. The second run had TMP/TEMP pointed at the scratchpad. The error was `no metadata ... GSE128651_metadata.csv`: the GEOparse SOFT download failed and the supplementary download got HTTP 403.
- Probes by hand (`evidence_geo/download_attempts.txt`):
  - every `https://ftp.ncbi.nlm.nih.gov/geo/...` path returns **403 Forbidden**, including unrelated series (GSE266241, GSE37525);
  - `ftp://` returns 550;
  - `geo/download/?acc=...` redirects (301) to the same FTP host.
  - `www.ncbi.nlm.nih.gov/geo/query/acc.cgi` does work. The series and sample text records are saved in `evidence_geo/`.
- The gates were recorded with the native recorder (`scripts/record_stop.py`), because the case-spec runner can't record this stop (see Tool problems).
  - `paper_reconstruction` is valid.
  - `ownership` is manual_review.
  - The decision contract validates (2 records). External-LLM attempts: 0.
- I removed the empty `data/GSE128651/` folder that the failed download created.

## Paper reconstruction (for resumption)
- **Design:** FACS-sorted muscle satellite cells (Lin⁻CD34⁺α7-integrin⁺). Con (untrained) n=4 vs Exe (4-week treadmill) n=4. GEO samples GSM3681653–60 are Con1–4 and Exe1–4. Two independent groups, no blocking.
- **Paper result** (S2.3.p1, FIG3B): 573 up and 1,326 down, 1,899 DEGs in total, at ">2-fold change, p<0.01".
  - Methods (S4.p10) instead say FDR < 0.05.
  - I took the Results rule as `paper_threshold`: pvalue < 0.01 and |log2FC| > 1. The FDR rule is recorded as the alternative.
  - Named genes: Igfbp7 up; Igfbp4, Igfbp5 and Igfbp6 down.
  - GSEA: OXPHOS, TCA, PI3K-Akt and mTOR down; ECM-receptor and S phase up.

## DEG counts vs paper
- Not computed: 0 of 1 contrasts ran. Paper: 573 up / 1,326 down (>2-fold, p<0.01).

## Deviations to expect once the file is available
- GEO deposits **only FPKM/RPKM** (`GSE128651_gene_fpkm.txt.gz`, made with Cufflinks per data_processing). The paper ran DESeq2 on HTSeq counts, so the paper's route is blocked.
- The runnable route would be log2(FPKM+1) + limma, as a declared deviation. The alternative is re-quantifying counts from SRA SRP189039.

## Tool problems
1. **Network:** NCBI GEO FTP (ftp.ncbi.nlm.nih.gov) returns HTTP 403 from this host. This blocks `download_geo_data` (GEOparse) and `download_supplementary_files` (`tools/geo_tools.py`).
2. **Misleading GEOparse error:** the failure is reported as `[Errno 2] No such file or directory: '...\\tmpXXXX'` instead of the 403 (it comes through `download_geo_data`, `tools/geo_tools.py`).
3. **Runner can't record a missing-matrix stop:** `tools/case_runner.py:529-530` calls `case.add_input(matrix_path)` (which needs `sha256`) before any gate. `_one_matrix` (`tools/case_runner.py:177-179`) also requires a matrix. So a case that stops at `ownership` because the file is missing can't be recorded through the runner.
4. **`inspect` needs metadata:** `inspect` has no fallback to the GEO `acc.cgi` text endpoint when the SOFT/FTP download fails. That endpoint was reachable here.

## To resume
Place `GSE128651_gene_fpkm.txt.gz` and `GSE128651_metadata.csv` in `data/GSE128651/`. Then rerun from inspect in a new run directory, or move this one to `_previous/`.
