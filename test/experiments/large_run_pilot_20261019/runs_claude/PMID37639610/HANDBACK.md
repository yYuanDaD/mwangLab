# HANDBACK: PMID 37639610 / GSE233485

**Status: refused at `design`.** GSE233485 has no exercise contrast.

## What ran
1. `python -m tools.case_runner inspect GSE233485`: downloaded the series to `data/GSE233485`. It has one matrix, `GSE233485_WT_mKO_mTG_3-24mo_Count_Matrix_TPM.tsv.gz` (54,416 Ensembl genes x 35 samples).
2. `prep_metadata.py`: builds `sample_sheet_from_matrix_columns.csv`.
   - The matrix columns are animal IDs (`WT_1`, `MCK_3874`, `MKO_SO_23`, `WSO_13`, ...). None of them appear in any GEO sample field. The GEO descriptions are `WT_3mo_1`, `mTG_24mo_3`, and so on.
   - Genotype and age are encoded in the column prefixes: MCK = mTG, MKO = mKO, `_SO`/WSO = 24 mo.
   - The script decodes them and checks that the six group sizes equal the GEO counts (6/6/5/6/6/6). The unique n=5 group is mKO 3 mo, which matches the paper's FIG1 legend.
   - No GSM-level mapping is made, and nothing is matched by position.
3. `python -m tools.case_runner execute case_spec.json`: recorded these gates:
   - `paper_reconstruction`, `ownership`, `alignment` (35/35, exact on the sample sheet index) and `matrix` (TPM: column sums are 1e6 and `data_processing` says TPM) were all valid.
   - `design` was **refused**. The suitability report itself was `analyzable` for the genotype x age comparisons (11 comparisons).
   - The validator reported 0 errors on 5 records.

## Why refused
- All 35 samples are sedentary WT, PGC-1a mKO or PGC-1a mTG mouse gastrocnemius, at 3 or 24 months. The paper's RNA-seq estimand is aging x PGC-1a dosage (S1.1.p1, FIG1).
- The paper measures its exercise effects by **proteomics**, not in this series:
  - voluntary wheel endurance and resistance running, using previously published data (ref 21; FIG4C);
  - treadmill-trained vs sedentary 25 mo mice, TMT16plex with limma (FIG4D, S3.15), deposited in MassIVE MSV000092099 (DA.p1).
- mTG vs WT is a genetic model. The paper uses it only as a sedentary-state analogue (S1.4.p1, SI Fig S3H), so reporting it as an "exercise effect" would change the estimand. Both mTG vs WT and 24 vs 3 mo were rejected as candidates.

## DEG counts vs paper
- No contrasts were run, so there are no DEG counts.
- The paper's RNA-seq threshold is FDR < 0.01 with edgeR (S3.7.p1). It reports no DEG count for any contrast; it reports 860 PC-aligned genes.
- The paper has no RNA-seq exercise DEG count at all.

## Deviations
- The metadata input is a sample sheet derived from the matrix column names, not `GSE233485_metadata.csv`, because the two use different identifiers. Group labels are verified against the GEO counts. Individual GSM ids stay unassigned (alignment confidence: medium).
- Had the design been valid, the paper's edgeR-on-counts route would have been blocked: only TPM is deposited. limma on log2(TPM+1) would have run as a declared deviation.

## Tool problems
- `tools/case_runner.py` (alignment block, around lines 547-590): there is no way to declare **group-level labels decoded from matrix column names** when the GEO records do not carry the matrix's sample IDs.
  - I had to substitute a derived metadata file through `inputs.metadata`. `prep_scripts` is documented for matrix repair only.
  - `inspect` reported `alignment_keys: []` and gave no hint for this case.
- `tools/geo_tools.py:30`: `GEOparse.get_GEO` is called with no encoding.
  - On this Windows (GBK) host, `GSE233485_metadata.csv` has mojibake: "PGC-1伪" for PGC-1α in `title`, and "3鈥" in `data_processing`.
  - It is cosmetic here, because the genotype column uses `{alpha}`, but it could break regex patterns on titles.
- `inspect`: `integer_fraction` 0.607 comes entirely from zeros (only 0.016% of non-zero values are integers), and the type candidates say "linear_normalized ... or estimated_counts". Reporting the column-sum check (every column = 1e6, which means TPM) would settle the type directly.
