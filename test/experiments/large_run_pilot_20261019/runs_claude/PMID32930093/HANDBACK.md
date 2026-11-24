# HANDBACK — PMID32930093 / GSE156667

**Outcome: refused at `paper_reconstruction`** (decision_status `refused`, execution `not_run`). Contract validator: 1 record, 0 errors.

## What ran
1. `python -m tools.case_runner inspect GSE156667 --data-root E:/agent/mwangLab_pdf/data`: failed (see Tool problems). GEO metadata was not cached.
2. Downloaded the full series SOFT through `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?...&targ=all&form=text&view=full` to `data/GSE156667/GSE156667_family.soft`. Wrote `data/GSE156667/GSE156667_metadata.csv` with `GEOparse.get_GEO(filepath=...).phenotype_data`, the same call `tools/geo_tools.py:30-36` uses.
3. Read the paper (`PMC7541086.paper.md`: ABS, S2.1–S2.3, S4.9, S4.12, S4.19, DA).
4. `python -m tools.case_runner execute case_spec.json`: the case stopped at `paper_reconstruction`.

## Why refused
- GSE156667 has 6 samples, all from the immortalized C2C12 mouse myoblast line, differentiated in culture: 3 WT and 3 CRISPR Lrrc8a KO under basal conditions. Genotype is the only field that varies (GEO characteristics and overall_design; paper S2.2.p1, S4.9.p1, FIG1 n=3 each).
- The paper's RNA-seq estimand is the effect of the Lrrc8a knockout in cells. It is not an exercise effect.
- Exercise appears only as a treadmill endurance test of skeletal-muscle KO mice (S4.19.p1), with no RNA sequenced. Stretch (S4.12.p1) was read out by western blot only.
- No sample subset or contrast in this accession can estimate how exercise affects gene expression. Relabelling KO vs WT as "exercise" would invent an estimand, so the case was refused.

## DEG counts vs paper
- 0/0 exercise contrasts: no exercise comparison exists.
- The paper's own genotype contrast (KO vs WT) was not run, because it is out of scope for the exercise request.
- The paper gives no total DEG count. It shows a top-17 heatmap and named genes (Mef2a, Myl2/3/4, Actc1, Tnnc2, Igf2, Akt2, Slc2a4, Foxo3/4/6 down; Ppargc1a, Pparg up).
- Paper threshold (S4.9.p1): Cuffdiff FDR < 0.05, fold change > 1.5 (FIG1 legend says ≥ 1.5), and FPKM > 1.5. Recorded in the paper_reconstruction gate; not applied.

## Deviations
- **Refused at `paper_reconstruction`, not at `design`.** The skill's usual gate for "no exercise arm" is `design`, after alignment and matrix. Here the deposited matrix (`GSE156667_merged.isoforms.fpkm_tracking.txt.gz`, isoform-level FPKM) could not be downloaded, so alignment and matrix could not run. The paper plus the GEO metadata alone settle that no exercise contrast exists, so the case stops at the first gate. With the matrix present, the outcome would be the same refusal at `design`.
- **The `inputs.matrix` slot points at `GSE156667_family.soft`.** This is only to pass the runner's file check; the runner hashes the file but never reads it as a matrix, because the case stops first. Declared in the spec's `discrepancies`.
- An `ownership` gate is in the spec (the schema requires it), but it is not recorded because the case stopped before it.

## Tool problems
1. **GEO download fails twice in `inspect`** (`tools/geo_tools.py:30`, `GEOparse.get_GEO(geo=...)`):
   - The SOFT download fails with `[Errno 2] No such file or directory: ...\Temp\tmpXXXX`. This happens inside and outside the sandbox, and with TMP/TEMP redirected to a scratch folder. GEOparse's FTP-based fetch seems to fail, leaving a missing temp file, and the error message hides the real cause.
   - `download_supplementary_files` fails with `HTTP Error 403: Forbidden`.
   - NCBI FTP (`ftp.ncbi.nlm.nih.gov`) returns 403 over https and http, and 550 over ftp, from this machine. `www.ncbi.nlm.nih.gov/geo/query/acc.cgi` works.
   - Suggested fix: fall back to acc.cgi `targ=all&form=text&view=full` for SOFT. This route has no way to get supplementary files.
2. **The runner needs a matrix file even for a case that stops before alignment.**
   - `tools/case_runner.py:529-530` calls `_matrix_input()` and `add_input(matrix)` before the first gate.
   - `tools/native.py:1049` then calls `sha256(path)`, which fails on a missing file.
   - So a paper-level refusal cannot be recorded when the data are unavailable.
3. **The spec schema requires `gates.ownership` even when `paper_reconstruction` stops the case** (`tools/case_runner.py` `Gates` model / `_complete`, around lines 205-218). Earlier gates are required fields, while later gates are optional after a stop.
