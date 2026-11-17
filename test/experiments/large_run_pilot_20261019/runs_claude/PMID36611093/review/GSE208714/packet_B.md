# Review packet B (the analysis' decisions): GSE208714

## Mechanical flags

- none

## Stop reasons

- alignment (manual_review; claim type: other): Matrix columns are lab mouse IDs (NT6.303, TG9.1.3, ...) with no key to the GSM samples or their exercise/isolation/hemisphere labels in GEO, SRA or BioSample; aligning by position or by guessed prefix is forbidden. Needs the lab-ID to sample key (paper Supplementary Data or authors).
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE208714 (RNA-/TRAP-seq)", "GSE208633 (CUT&RUN, not analysed here)", "GSE208715 (SuperSeries)"], "assay": "TRAP-seq (translating mRNA, Emx1-NuTRAP excitatory neurons), polyA RNA-seq, NovaSeq 100 bp PE; separate bulk RNA-seq of wild-type dorsal hippocampus for the OLM experiment", "organism": "Mouse (male only, S4.1.3.p1)", "factors": {"exercise": ["sedentary", "ELE (voluntary wheel running P21-41)"], "isolation": ["SIT (bilateral hippocampus, one homogenate)", "separate (one hemisphere)"], "hemisphere": ["left", "right"], "wild_type_OLM_experiment": ["sedentary no OLM", "sedentary 3 min OLM", "sedentary 10 min OLM", "ELE P21-41 3 min OLM", "juvenile P21-27 / adolescent P35-41 exercise 3 min OLM"]}, "sample_inclusion": "SIT TRAP-seq: 4 ELE + 4 sedentary deposited; PCA outliers removed 2 sedentary and 1 ELE, leaving n = 2 sedentary and n = 3 ELE (FIG4 legend; S4.1.16.1.p2). Separate isolation: n = 3 mice per group (S4.1.7.p1, FIG2 legend f).", "primary_estimand": "Effect of early-life voluntary wheel running (P21-41) vs sedentary housing on translating mRNA in Emx1+ hippocampal neurons at P42, SIT isolation (S2.4.p1, FIG4a).", "planned_contrasts": ["SIT TRAP-seq ELE vs sedentary (S2.4.p1, FIG4a; paper: 297 up, 338 down; n = 3 ELE vs 2 sed after outlier removal)", "Separate-isolation TRAP-seq ELE vs sedentary (S2.2.p3, FIG2f-g; counts only in Supplementary Data 3)", "Separate isolation, ELE vs sedentary within left and within right hemisphere, plus hemisphere x ... [1028 more characters]

reasoning: Paper read in full (S2.1-S2.6, S4.1.3-S4.1.16, DA.p1). The primary RNA estimand is the SIT TRAP-seq ELE vs sedentary contrast in S2.4.p1/FIG4a with DESeq2 Wald, raw p < 0.05 and |log2FC| > log2(1.3). The paper excluded PCA outliers (2 sed, 1 ELE) without naming them, leaving 2 vs 3.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE208714\\GSE208714_countsNuTRAP.csv.gz", "owned": true, "checks": ["DA.p1 names GSE208714 as the RNA- and TRAP-seq series of this paper; GEO Series_pubmed_id = 36611093", "GSE208714_countsNuTRAP.csv.gz: 20 integer columns, Ensembl gene IDs, 55,335 features; metadata has exactly 20 Emx1-NuTRAP samples whose description field is 'countsNuTRAP.csv' (8 SIT, 12 separate)", "GSE208714_countswildtype.csv.gz: 24 columns for the 24 C57Bl/6J bulk samples (description 'countswildtype.csv'); belongs to the OLM experiment (S2.6), not the primary contrast"], "accession": "GSE208714", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE208714\\GSE208714_metadata.csv"}

reasoning: Both deposited count files belong to this paper and accession; the NuTRAP file holds the primary TRAP-seq samples (20 columns = 20 NuTRAP GSMs).

### alignment (manual_review, not_started)

final: {"key_column": null, "matrix_columns": ["NT6.303", "NT6.304", "NT6.305", "NT6.306", "NT7.2.3", "NT7.2.4", "TG7.3.1", "TG7.3.2", "TG7.3.3", "TG7.3.4", "TG7.4.1", "TG7.4.2", "TG9.1.1", "TG9.1.2", "TG9.1.3", "TG9.1.4", "TG9.2.1", "TG9.2.2", "TG9.2.3", "TG9.2.4"], "metadata_ids": "GSM6365460-GSM6365479 (titles 'Brain, RNA, <exercised|sedentary>, <SIT|left/right separate>, biol rep<k>')", "searched_sources": ["GEO metadata CSV (all 39 columns): no field contains the lab IDs; inspect alignment_keys = []", "GSE208714 family SOFT: no lab IDs", "SRA RunInfo for PRJNA860786 (44 runs): LibraryName = GSM id", "BioSample records SAMN29862687.. (20 NuTRAP): attributes only repeat the GEO characteristics", "SRA full XML original file names: UCI facility names nR116-L4-P0xx-<index>, no lab IDs", "GSE208633 (CUT&RUN companion) sample text: facility file names only"], "wildtype_matrix_note": "countswildtype.csv columns (WT22.1.1 - RNA, ..., LBN21.1.1 - RNA, HC1-HC4) have the same problem; only HC1-HC4 plausibly correspond to the 4 'sedentary, biol rep' no-OLM samples, the other 20 cannot be keyed", "unblocking_fact": "a table mapping lab mouse IDs (NT6.303, TG9.1.3, ...) to GSM ids or to exercise/isolation/hemisphere labels, e.g. from the paper's Supplementary Data 2 (MOESM5/6 xlsx, sample RNA yields) or from the authors (araus@uci.edu / lead contact)"}

reasoning: The matrix column names are lab mouse IDs (NT6.303, TG9.1.3, ...) that appear nowhere in the GEO metadata, SOFT, BioSample, SRA run info, SRA original file names, or the CUT&RUN companion series. No metadata column or index equals or contains them, so no exact or named-key match exists. The prefixes NT (6 columns) and TG (14 columns) do not split into any metadata grouping (SIT 4+4, separate 6+6, exercised 10 / sedentary 10), so they cannot be decoded as group labels. The only alternatives are matching by column order or inferring labels from expression or library size, and both are forbidden: either would silently assign exercise labels to the wrong animals. The paper's outlier exclusion (2 ... [208 more characters]

rejected alternatives: [{"value": "align by column order to GSM6365460-79", "reason_rejected": "position alignment is forbidden; matrix order (NT6.303, TG7.4.1, NT7.2.3, ...) has no documented relation to GSM order"}, {"value": "NT = sedentary, TG = exercised", "reason_rejected": "6 NT vs 14 TG does not match 10 sedentary vs 10 exercised; label guess"}, {"value": "assign groups by clustering / library size vs SRA spot counts", "reason_rejected": "inferred labels, not provenance; counts are post-dedup fragments so they ... [34 more characters]


## Recorded paper-data discrepancies

[
  {
    "item": "fold-change cutoff",
    "paper": "S2.4.p1 '>30% expression increase' and FIG4 legend '|log2FC| > 0.3785' (= log2 1.3); S4.1.16.1.p2 prints 0.3875",
    "data": "not applicable (case stopped at alignment)",
    "disposition": "record_only: 0.3875 is read as a digit transposition of log2(1.3) = 0.3785116"
  },
  {
    "item": "sample inclusion",
    "paper": "PCA outliers removed: 2 sedentary and 1 ELE SIT samples (S4.1.16.1.p2), leaving 3 vs 2",
    "data": "GEO deposits all 4 + 4 SIT samples with no flag for which were excluded",
    "disposition": "blocks_paper_sample_set: the excluded samples are not identified"
  },
  {
    "item": "sample identifiers",
    "paper": "no sample key printed in the article text",
    "data": "matrix columns use lab IDs; metadata uses GSM ids with no link between them",
    "disposition": "blocks_alignment"
  }
]

## HANDBACK.md (start)

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
- **Paper's threshold** (S2.4.p1, FIG4 legend):  ... [798 more characters]
