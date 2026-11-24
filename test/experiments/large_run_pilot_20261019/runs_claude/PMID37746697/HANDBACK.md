# HANDBACK — PMID37746697 / GSE240814

**Outcome: refused at the `design` gate (both cases). No DE model was run.**

## Paper evidence: abstract only
No full text was available. The comparison with the paper rests on the PubMed abstract only
(`PMID37746697_abstract.txt`, fetched with NCBI efetch), plus the GEO series summary and overall design
and the authors' GEO supplementary DE files.

## What ran
1. `python -m tools.case_runner inspect GSE240814 --data-root E:/agent/mwangLab_pdf/data` downloaded the series
   to `data/GSE240814/`. It holds two per-sex matrices (`GSE240814_HU_male_total.csv`, 41 samples;
   `GSE240814_HU_female_total.csv`, 39 samples) and the authors' per-time DE/pathway tables.
2. `case_spec.json` (made by `make_spec.py`) has two cases, `GSE240814_male` and `GSE240814_female`.
   - The gates `paper_reconstruction`, `ownership`, `alignment` (exact match on `title`, 100% of matrix columns) and `matrix` are all `valid`.
   - `design` is `refused`.
   - Run result: `execute` completed and the validator reported 10 records with 0 errors.
   - The suitability report said "analyzable" (10 HU-time comparisons per sex), but that is a check on the data structure, not on the estimand.

## Why refused
- The study is **hindlimb unloading (HU), a disuse/atrophy model**. It compares 24/48/72/168 h of HU with 0 h ambulatory controls, separately in each sex.
- GEO treatment levels are only `Control` and `Hindlimb Unloading`. There is no exercise, training or loading arm in the paper or the data.
- The requested estimand ("how exercise affects gene expression") therefore cannot be identified.
- Running HU vs control and calling it an exercise effect would misstate the estimand. Reversing it (control vs HU as an "activity" proxy) would be a manufactured contrast. Both alternatives are recorded as rejected candidates.

## DEG counts vs paper
None computed (refused). For the record:
- The abstract states no DEG counts or threshold.
- The authors' GEO files (`*_Total_Up_and_Down_DE_*.csv`) report the counts below. Their DE tables all have FDR step-up < 0.05 and no fold-change cutoff.
- So the paper's threshold, inferred from the deposit rather than from the paper, is **FDR < 0.05**.

| Sex | 24h vs 0h | 48h vs 0h | 72h vs 0h | 168h vs 0h |
|---|---|---|---|---|
| Male | 3888 | 4133 | 1611 | 3053 |
| Female | 3173 | 4907 | 3647 | 1633 |

## Deviations / notes
- **Matrix:** the deposited matrices are DESeq2 median-ratio normalized counts from Partek Flow (non-integer; integer fraction about 0.03). Raw counts are not deposited. This would matter for any HU analysis but is moot here.
- **Group sizes:** the abstract says n=8/group. GEO has male control n=7, HU groups 8–9; female groups 8, except 168 h with n=7. This is recorded as a discrepancy.

## Tool problems
- `tools.case_runner inspect`: the `alignment_keys` `of_matrix` count (40 female / 42 male) does not match the actual sample columns (39 / 41; every sample column matched `title`). It looks like a non-sample annotation column is counted as a sample. This is cosmetic, but it suggests unmatched columns that do not exist.
- The PowerShell tool blocked `$env:` assignment and `Invoke-WebRequest` in this environment, so the Bash tool was used instead. This is a harness issue, not a repository issue.
