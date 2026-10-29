# HANDBACK: paper 082a6f74bc23189c7e69bf6269a1995a3930db4f (PMC6616370, exRNA Atlas)

**Status: refused (both cases).** No DE analysis ran.

## What ran
- `case_runner inspect` on GSE121868 and GSE123865 (both cached under `E:/agent/mwangLab_pdf/data`).
- Read the paper's exercise sections (S2.11.p1-p3, S4.6.2.8.p1, FIG7) and its data-availability lists (S4.3.1.p1, S4.3.7.3.p1, the KRT).
- `case_runner execute case_spec.json`. The validator reported 7 records and 0 errors. The first attempt is kept in `_previous/20261029T040111Z`.

## Findings
- The paper's only exercise analysis uses the Exercise challenge study EXR-SADAS1EXER1-AN, which is **GEO GSE121874** (S4.3.1.p1). It compares Baseline (n=26) with post-Exercise (n=26). GSE121874 was **not** one of the assigned accessions.
- **GSE121868** is the subarachnoid hemorrhage dataset: 523 CSF and plasma samples from 30 donors, all patients, with no controls. The paper uses it only for cargo-type deconvolution. There is no exercise factor.
  - The matrices are exceRpt reads per million (RPM), not counts.
  - The matrix columns (`sample_B1010_ATGAGC_fastq`) match no metadata field. The only way to align them would be by position.
  - **Refused at `ownership`.** The files belong to the paper, but they contain none of the samples the exercise estimand needs. The ownership reasoning explains why the stop is not at the design gate (see the tool problem below).
- **GSE123865** is the RNA isolation kit study: 182 libraries made from 4 pools of healthy donors (female/male × serum/plasma), each run through 11 isolation kits.
  - Alignment worked by exact match on `description` (182/182).
  - The matrix is RPM.
  - **Refused at `design`.** There is no exercise contrast. The kit, biofluid and sex comparisons were rejected as answers to the exercise request. Suitability was also `not_analyzable` (data_type, sample_size).

## DEG counts vs paper
- Paper threshold: FDR < 0.05 and log2FC > 1 (S4.6.2.8.p1).
- The paper reports 53 DE miRNAs across 3 cargo profiles from deconvolution t-tests, 17 of which overlap its DESeq2 "Shah et al." set. All of these come from GSE121874.
- This run produced no DEG counts. 0 of 1 exercise contrasts can be reproduced from the assigned accessions.

## Deviations
- GSE121868 stops at `ownership` instead of the canonical `design` gate, because of the runner limitation below.

## Tool problems
- `tools/case_runner.py:503` calls `native.align_to_metadata(...)` unconditionally, before it checks whether the `alignment` gate has a non-valid `decision_status`.
  - A refused or unresolved alignment with no matching key therefore raises `NativeToolError` (`tools/native.py:304`) instead of being recorded as the stop.
  - The error message itself advises "record the alignment as unresolved", but that path cannot work.
  - The workaround was to stop at `ownership`.
- `inspect` gave no alignment key for GSE121868. This is correct, since none exists.
- Reading the inspect JSON with PowerShell `ConvertFrom-Json` fails on GSE123865, because the level keys `ExoRNeasy` and `Exorneasy` differ only by case. This is cosmetic: Python reads the file fine.
