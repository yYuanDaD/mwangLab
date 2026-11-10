# Review packet B (the analysis' decisions): GSE190355

## Mechanical flags

- none

## Stop reasons

- alignment (manual_review; claim type: other): No exact key between matrix columns (MPST*/MST*/R*) and GEO samples; the 7 R* columns cannot be assigned to vehicle+PE vs vehicle, so the paper's exercise contrast (Fig 5A) is unidentifiable. Needs the authors' sample-code key or SRA re-quantification.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE190355"], "assay": "bulk RNA-seq of ipsilateral (ischemic) striatum, rat tMCAO model, day 35 (S4.16.p1, FIG5)", "factors": {"exercise": ["no PE (stationary wheel)", "PE (forced wheel running from day 7)"], "graft": ["vehicle (DMEM/F12)", "hNPC transplant"]}, "design": "2x2 factorial randomised groups: vehicle alone (n=3), vehicle plus PE (n=4), NPCs alone (n=3), NPCs plus PE (n=4) (S2.1.p1, FIG5 legend)", "sample_inclusion": "14 animals, one sample each; independent animals, no repeated measures", "primary_estimand": "Effect of postoperative physical exercise on striatal gene expression after stroke: vehicle plus PE vs vehicle alone (Fig 5A); exercise effect within grafted animals: NPCs plus PE vs NPCs alone (Fig 5D)", "planned_contrasts": ["vehicle+PE vs vehicle (FIG5 A; S2.4.p2; paper DEG count not stated, heatmap only)", "NPCs alone vs vehicle (FIG5 B; not an exercise contrast)", "NPCs+PE vs vehicle (FIG5 C; exercise confounded with graft)", "NPCs+PE vs NPCs alone (FIG5 D; exercise effect in grafted animals; DEG count not stated)"], "paper_method": "HISAT 2.0.5 alignment, DEGseq 1.18.0 pairwise DE (S4.16.p1); GEO data_processing instead says HTSeq counts + DESeq2", "paper_threshold": {"metric": null, "cutoff": null, "effect_metric": null, "effect_cutoff": null, "stated": false, "source_locator": "S4.16.p1 (no DEG cutoff stated); GEO data_processing states q<=0.05 and |log2 ratio|>=1 (DESeq2)"}, "paper_results": "Fig 5 heatmaps and top GO terms only: PE  ... [250 more characters]

reasoning: S2.1.p1 defines the four randomised groups; FIG5 legend gives the four RNA-seq comparisons and group sizes (4/4/3/3); S4.16.p1 gives HISAT2 + DEGseq with no threshold. The exercise estimands are Fig 5A (PE vs vehicle) and Fig 5D (NPCs+PE vs NPCs). Fig 5B is graft-only and 5C mixes graft and exercise.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE190355\\GSE190355_fpkm.anno.xls.gz", "owned": true, "checks": ["DA.p1 names GEO GSE190355; series pubmed_id = 35030322", "series has one supplementary file, GSE190355_fpkm.anno.xls.gz (gzipped TSV of FPKM plus annotation), 14 sample columns for 14 GSMs", "GEO data_processing mentions a raw-count matrix, but no count file is deposited (series SOFT lists only the FPKM file; sample supplementary_file_1 = NONE)"], "accession": "GSE190355", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE190355\\GSE190355_metadata.csv"}

reasoning: The matrix is the only supplementary file of the paper's own accession and has 14 sample columns, matching the 14 GSMs and the paper's 4+4+3+3 design. Ownership of the file is clear; per-sample identity is the alignment question.

### alignment (manual_review, not_started)

final: {"method": "none: no exact key", "n_aligned": 0, "n_metadata": 14, "coverage": 0.0, "unmatched_matrix_columns": ["MPST1", "MPST2", "MPST3", "MPST4", "MST1", "MST3", "MST4", "R11", "R20", "R23", "R26", "R29", "R2", "R4"], "unmatched_metadata_samples": ["GSM5720385", "GSM5720386", "GSM5720387", "GSM5720388", "GSM5720389", "GSM5720390", "GSM5720391", "GSM5720392", "GSM5720393", "GSM5720394", "GSM5720395", "GSM5720396", "GSM5720397", "GSM5720398"], "exact_matches_by_field": {"index": [], "title": [], "source_name_ch1": [], "characteristics_ch1.2.treatment": [], "relation": []}, "substring_matches_by_field": {"index": [], "title": [], "source_name_ch1": [], "characteristics_ch1.2.treatment": [], "relation": []}, "excluded_samples": {}}

reasoning: Matrix sample columns are MPST1, MPST2, MPST3, MPST4, MST1, MST3, MST4, R11, R20, R23, R26, R29, R2, R4. Metadata identifies samples only by GSM id, title ('Physical exercise group_rep1', 'Culture medium injection group rep1', ...), and source_name ('Ischemic striatum from PE+Vehicle-1', 'NPCs+PE-1', ...). No metadata field (index, title, source_name, description, relation) contains these lab codes, and the SRA records (SRX13339692-705, runinfo efetch) carry no LibraryName. So no exact key exists. A decoding guess is possible for 7 columns (MPST = MCAO+PE+Stem-cell Transplant, 4 columns = NPCs+PE n=4; MST = MCAO+Stem-cell Transplant, 3 columns = NPCs alone n=3) but the replicate numbers do n ... [561 more characters]

rejected alternatives: [{"value": "decode MPST -> NPCs+PE and MST -> NPCs alone and run Fig 5D only", "reason_rejected": "abbreviation guess, not an exact key; replicate numbers disagree (MST1/3/4 vs NPCs-1/2/3); would silently corrupt the design if the code means something else"}, {"value": "split R columns into PE vs vehicle by order or number", "reason_rejected": "no evidence for any split of R2/R4/R11/R20/R23/R26/R29; position-based alignment is forbidden"}, {"value": "re-quantify from SRA FASTQ (SRP349620) with G ... [200 more characters]


## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "DEGseq 1.18.0 (S4.16.p1)",
    "data": "GEO data_processing: HTSeq counts + DESeq2, q<=0.05 and |log2 ratio|>=1",
    "disposition": "recorded; not reached because the case stops at alignment"
  },
  {
    "item": "Raw counts",
    "paper": "count-based DE (DEGseq)",
    "data": "data_processing says a raw-count matrix is supplied, but only the FPKM file is deposited",
    "disposition": "paper route would be blocked (FPKM only); recorded"
  },
  {
    "item": "Sequencer / library kit",
    "paper": "Novaseq 6000, Nextera XT, PicoPure (S4.16.p1)",
    "data": "GEO: HiSeq 4000, NEBNext Ultra, Trizol",
    "disposition": "recorded; does not change the estimand"
  },
  {
    "item": "Sample labels",
    "paper": "groups vehicle / vehicle+PE / NPCs / NPCs+PE",
    "data": "matrix columns MPST1-4, MST1/3/4, R2/R4/R11/R20/R23/R26/R29 with no key in metadata or SRA",
    "disposition": "stops the case at alignment (manual_review)"
  },
  {
    "item": "Source name",
    "paper": "vehicle+PE replicates 1-4",
    "data": "GSM5720388 source_name says 'PE+Vehicle-2' (duplicate of GSM5720386) while its title says rep4",
    "disposition": "recorded; metadata typo"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID35030322 / GSE190355

**Status: stopped at `alignment` with `manual_review`. No DE was run.**

## What ran
- `python -m tools.case_runner inspect GSE190355`: downloaded the series. The only supplementary file is `GSE190355_fpkm.anno.xls.gz` (a gzipped TSV of FPKM values plus annotation, 14 sample columns). Inspect listed **no candidate matrices** because it does not recognise the `.xls.gz` name.
- Read the paper (PMC8828662). It describes a randomised 2x2 design on day-35 ipsilateral striatum: vehicle (n=3), vehicle+PE (n=4), NPCs (n=3), NPCs+PE (n=4). There are four RNA-seq comparisons in Fig 5A-D. The exercise estimands are Fig 5A (vehicle+PE vs vehicle) and Fig 5D (NPCs+PE vs NPCs).
- Wrote `case_spec.json` with three gates: paper_reconstruction, ownership, and an alignment gate set to manual_review. `case_runner execute` then raised (see the tool problems below). That attempt was moved to `_previous/attempt1_runner_error/`.
- Recorded the same gates with the native recorder in `record_alignment_stop.py`, which only records decisions and computes no statistics. The alignment facts are in `GSE190355/aligned/alignment_facts.json`. The decision-contract validator reports VALID.

## Why it stopped
- **No key links the matrix columns to the samples.** The matrix columns are `MPST1-4`, `MST1/3/4`, `R2`, `R4`, `R11`, `R20`, `R23`, `R26` and `R29`. The metadata identifies samples only by GSM id, by title ("Physical exercise group_rep1", ...) and by source_name ("PE+Vehicle-1", "NPCs+PE-1", ...). None of these fields matches a matrix column, either exactly or as a substring. The SRA runinfo for SRX13339692-705 has an empty LibraryName.
- **The 7 `R*` columns cannot be split.** They hold the 4 vehicle+PE and 3 vehicle samples with no information on which is which. The paper's primary exercise contrast (Fig 5A) therefore cannot be identified.
- **Fig 5D would rest on a guess.** The codes suggest MPST = NPCs+PE (4 columns) and MST = NPCs (3 columns). This is an abbreviation guess, not a key, and the replicate numbers disagree (MST1/3/4 vs NPCs-1/2/3). I rejected it.
- **What would unblock it:** the authors' code-to-sample key, or re-quantifying the GSM-labelled SRA FASTQs (SRP349620). Re-quantifying would also supply the raw counts the paper's method needs.

## DEG counts vs the paper
- **Paper:** gives no DEG counts or named genes (Fig 5 shows heatmaps and GO terms only). It states no DEG threshold: S4.16.p1 names only DEGseq 1.18.0.
- **GEO data_p ... [1619 more characters]
