# HANDBACK — GSE71972 (Romero et al., J Physiol 2016, PMID 27061420)

**Outcome: stopped at the `ownership` gate with `manual_review` (route `stopped`). This is a missing file, not a scientific refusal.** No differential-expression model was fitted, so there are no DEG counts.

## Evidence basis
- **The comparison with the paper rests on the abstract only.** No full text was available. I read the PubMed abstracts of PMID 27061420, its 2018 update notice PMID 29455450, and the companion PMID 27493198, fetched with NCBI E-utilities efetch (`pubmed_abstracts.txt`). I also read the GEO series description (`geo_series_description.txt`).
- The abstract gives no DEG threshold, no DE method and no split by time point. It says only that exercise changed ">3000 protein-coding genes" and that 795 genes differed between control and H1/H2 blockade after exercise.

## What ran
1. `tools.case_runner inspect GSE71972` failed. GEOparse's SOFT download died with a temp-file error after the FTP fetch failed, and the supplementary download got HTTP 403.
2. I probed GEO directly (`download_attempts.txt`). Every path on `ftp.ncbi.nlm.nih.gov` returns HTTP 403, including the GEO root, with the sandbox both on and off. That covers the series supplementary files (`GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx`, `GSE71972_RAW.tar`, the DE tables), the per-sample `*.counts.txt.gz` files and NCBI's own generated counts. The block covers the whole GEO file host, not just this series. EBI BioStudies has no E-GEOD-71972. ENA has only FASTQs (about 3 GB × 48), and no aligner is available to rebuild the counts from them.
3. The full family SOFT did download through `acc.cgi`. It holds no count tables (`Sample_data_row_count = 0`). From it I built `data/GSE71972/GSE71972_metadata.csv` with GEOparse: 48 samples, 8 control + 8 blockade subjects, each sampled pre, immediately after and 3 h after exercise.
4. `case_spec.json` records the decisions. `tools.case_runner execute` crashed with `FileNotFoundError` on the absent matrix before it recorded any gate (that attempt is in `_previous/runner_attempt_missing_matrix/`). I therefore recorded the `paper_reconstruction` and `ownership` gates with the native recorder (`scripts/record_stop.py`), using the same content as the spec. `validate_decision_contract.py` reports VALID (2 records). No external LLM attempts were made.

## DEG counts vs paper
| Contrast | Ours | Paper (abstract) | Paper threshold |
|---|---|---|---|
| Exercise response (control; post vs pre) | not run | >3000 protein-coding genes | not stated in abstract |
| Control vs blockade, post-exercise | not run | 795 | not stated in abstract |

## Planned analysis once the matrix is available (not executed)
- **Matrix:** HTSeq-count raw counts, from `GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx` or from `RAW.tar` merged by GSM.
- **Model:** DESeq2 with time as a factor (pre / immediate / 3 h) and a subject key. In the control arm: immediate vs pre and 3 h vs pre, blocking on subject. Drug × time comparisons come from one model fitted on all 48 samples.
- **Subject key:** GEO reuses subject numbers 4 and 5 in both arms (CON_4 / HIST_4, CON_5 / HIST_5). The key must therefore be drug + subject, not the subject number alone.
- **Threshold:** the paper's threshold is unknown from the abstract, so it falls back to `workflow_default` (BH padj < 0.05).
- **Which analysis to compare against:** GEO says the alignments were re-run with updated software and that the updated counts and DE tables (dated 2016-08-30) are reported in the 2018 update (PMID 29455450). The abstract's numbers come from the original analysis. Compare against the updated deposited DE tables.

## Deviations
- Metadata comes from the `acc.cgi` SOFT, not from the standard GEOparse FTP download.
- The stop was recorded with the scripted route because the case runner cannot record one when the matrix is missing.

## Tool problems
- `tools/case_runner.py:529-530`: `_matrix_input()` / `case.add_input(matrix_path, "matrix")` hash the matrix (`tools/native.py:78`, `open(path)`) before any gate is recorded. A missing-matrix case therefore crashes with `FileNotFoundError` and leaves 0 records, so the runner cannot express an ownership `manual_review` stop.
- `tools/geo_tools.py:30`: `GEOparse.get_GEO(geo=...)` fails with a misleading `[Errno 2] ... tmpXXXX` temp-file error when the FTP host returns 403. The real cause, HTTP 403, is hidden. There is no fallback to `acc.cgi?targ=all&form=text&view=full`, which works.
- `tools/geo_tools.py:105`: supplementary download uses only `ftp.ncbi.nlm.nih.gov` (here HTTP 403) and has no alternative mirror.
- Environment: the GEO file host `ftp.ncbi.nlm.nih.gov` is fully blocked (HTTP 403) from this machine. E-utilities and `www.ncbi.nlm.nih.gov` work.

## To unblock
Put `GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx` (or `GSE71972_RAW.tar`) into `E:/agent/mwangLab_pdf/data/GSE71972/`. Then run `inspect`, extend `case_spec.json` past `ownership` and run `execute`.
