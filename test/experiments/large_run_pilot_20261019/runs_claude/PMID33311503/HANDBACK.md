# HANDBACK — PMID33311503 / GSE153350

**Status: refused at `paper_reconstruction`.** The paper has no exercise estimand.

## What ran
1. `python -m tools.case_runner inspect GSE153350 --data-root E:/agent/mwangLab_pdf/data` failed twice. The SOFT file and the supplementary files return HTTP 403 from `ftp.ncbi.nlm.nih.gov`. See `inspect_GSE153350.json/.log`.
2. Manual checks on 2026-11-24:
   - `https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE153350&format=file` redirected to ftp.ncbi and returned 403.
   - The per-GSM `.tab.gz` files returned 403 over https.
   - `ftp://` returned 550.
   - The GEO web text endpoint (`acc.cgi ... form=text`) worked. I used it for the series and sample metadata.
3. `record_refusal.py` (scripted route, `native.RunRecorder`):
   - parsed the GSM text into `GSE153350_metadata_from_gsm_text.csv` (7 samples);
   - recorded the `paper_reconstruction` gate as `refused`.
   - `validate_decision_contract.py` reports VALID (1 record), with 0 external LLM attempts.

## Why it was refused
- **Paper topic:** estrogen-sensitive (ERα+) MPA neurons and torpor/thermoregulation. The experiments are chemogenetic activation, fasting-induced torpor, photometry and caspase ablation.
- **Sequencing:** the only sequencing is patch-seq of ERα+ MPA neurons (2 neurons pooled per sample). It compares temperature-responsive neurons (TR, n=4) with non-responsive ones (NR, n=3) after ex vivo 25→30 °C exposure (S2.3.p3, Fig. 3i, S4.3.1.p1, DA.p1).
- **GEO metadata:** the only varying factor is `temperature responsive: Yes/No`. Strain is Esr1-ZsGreen and tissue is Brain for every sample.
- **"Physical activity" in the paper:** S2.4.p1 and Supp. Fig. 4a–d mention it, but it is home-cage telemetry recorded as a phenotype. It is not an exercise intervention and has no RNA-seq.
- **Gate choice:** refusing at paper reconstruction is correct here, because no exercise contrast can be built from the paper. Using TR vs NR as a stand-in was rejected.

## DEG counts vs paper
- No analysis was run, so there are no DEG counts.
- The paper's own (non-exercise) contrast is TR vs NR, DESeq2 via Galaxy 2.11.40.6, BH-adjusted p < 0.05 with no fold-change cutoff (Fig. 3i legend). The paper shows only a volcano plot and states no DEG count.

## Deviations
- **Route:** the scripted route (RunRecorder) was used instead of `case_runner execute`, because the runner needs a matrix file even when the case stops at the first gate, and the matrix could not be downloaded.
- **Gate order:** the case stopped at `paper_reconstruction`, not `design`. The ownership, alignment and matrix gates could not be honestly recorded without the matrix. The refusal does not depend on them.
- **Metadata source:** the metadata CSV came from GEO's web text endpoint, not GEOparse, and has fewer columns. `data_processing` was not kept in the CSV; it states htseq-count gene counts.

## Tool problems
- `tools/case_runner.py:176-180` and `tools/case_runner.py:529-530`: `Inputs` requires a matrix (or raw_tar), and `CaseRun.run` registers it before the `paper_reconstruction` gate. A case that stops at the paper gate, or one whose matrix cannot be downloaded, cannot use the case-spec route.
- `tools/geo_tools.py:30`: `GEOparse.get_GEO` fails on the NCBI 403 with a misleading message, `[Errno 2] No such file or directory: ...\tmpXXXX` (seen at `geo_tools.py:42`). It has no fallback to the working `acc.cgi?...&form=text` endpoint.
- `tools/geo_tools.py:105`: the supplementary download uses ftp.ncbi over https only, so it fails with HTTP 403. This is an NCBI access block on this machine and network, not a code bug, but it has no retry or alternative path.
