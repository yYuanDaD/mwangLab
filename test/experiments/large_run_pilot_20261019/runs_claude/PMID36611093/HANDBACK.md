# HANDBACK: PMID36611093 / GSE208714

**Status:** stopped at `alignment` with `manual_review`. No DE model was run.

## What ran
1. `python -m tools.case_runner inspect GSE208714 --data-root E:/agent/mwangLab_pdf/data` downloaded the series into `data/GSE208714`. It holds two count files, `GSE208714_countsNuTRAP.csv.gz` (20 columns, Ensembl IDs, integer counts) and `GSE208714_countswildtype.csv.gz` (24 columns, gene symbols). The inspect reported `alignment_keys: []` for both.
2. I read the paper (PMC9825372.paper.md), covering S2.1–S2.6, S4.1.3–S4.1.16 and DA.p1.
3. I searched for a key that links the matrix columns to the GSM samples, using read-only NCBI E-utilities queries.
   - The GEO metadata (all 39 columns) and the family SOFT do not contain the lab IDs.
   - In the SRA RunInfo for PRJNA860786 (44 runs), LibraryName is the GSM ID.
   - The BioSample records only repeat the GEO characteristics.
   - The original file names in the SRA XML are UCI facility names (`nR116-L4-P0xx-<index>`).
   - The GSE208633 (CUT&RUN) sample text has only facility file names.
4. `python -m tools.case_runner execute case_spec.json` recorded three gates: `paper_reconstruction`, `ownership`, and `alignment` (manual_review). The contract validator reported 3 records and 0 errors.

## Why it stopped
- The NuTRAP matrix columns are lab mouse IDs: NT6.303–306, NT7.2.3/4, TG7.3.1–4, TG7.4.1/2, TG9.1.1–4, TG9.2.1–4. They map to none of the 20 GSMs (GSM6365460–79) in any available source.
- The NT/TG prefixes (6 and 14 columns) do not match any grouping in the metadata:
  - SIT 4+4 versus separate 6+6;
  - exercised 10 versus sedentary 10.
- The only ways left to assign labels are column order, guessed prefixes, or labels inferred from expression or library size. All three are forbidden, so no exercise contrast can be built without silently mislabelling animals.
- The paper removed PCA outliers (2 sedentary and 1 ELE SIT sample) without naming them, so its 3-vs-2 sample set could not be rebuilt even with a key.
- The wild-type OLM matrix has the same problem. Its columns are WT…/LBN… IDs; only HC1–4 plausibly correspond to the 4 no-OLM sedentary samples.
- **What would unblock it:** a table mapping lab ID to GSM or to condition. Possible sources are the paper's Supplementary Data 2 (MOESM xlsx with per-sample RNA yields; not downloaded, because that file download was not authorised) or the authors.

## DEG counts versus the paper
- **Paper's threshold** (S2.4.p1, FIG4 legend): DESeq2 Wald raw p < 0.05 and |log2FC| > log2(1.3) = 0.3785116.
  - S4.1.16.1.p2 prints 0.3875, which I read as a digit transposition and recorded as a discrepancy.
- **Paper's result:** SIT ELE vs sedentary (n = 3 vs 2) gave 297 up and 338 down, 635 DEGs in total.
- **Ours:** none. 0 of 1 planned contrasts were run.

## Deviations
None. The case stopped before the design gate.

## Tool problems
- No bugs found. The runner stopped cleanly at alignment (`tools/case_runner.py:544-547`) and the validator passed.
- One gap: `case_runner inspect` only checks GEO metadata for alignment keys. It does not record that SRA, BioSample, and original file names were searched. I did that by hand with E-utilities, and that evidence lives only in the alignment `final.searched_sources` field of the spec.
