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
- **GEO data_processing:** states DESeq2 with q<=0.05 and |log2 ratio|>=1.
- **Ours:** none, because no contrast ran. This makes 0 of 2 exercise contrasts.

## Deviations and discrepancies (recorded, not reached)
- **DE method:** the paper names DEGseq, but GEO says HTSeq + DESeq2.
- **Raw counts:** GEO data_processing says a raw-count matrix was supplied, but only the FPKM file is deposited. The paper's count-based route would have been blocked even with a sample key, leaving limma on log2(FPKM+1) as a declared deviation.
- **Sequencing details:** the paper says NovaSeq 6000 / Nextera XT / PicoPure. GEO says HiSeq 4000 / NEBNext / Trizol.
- **Metadata typo:** GSM5720388 has source_name "PE+Vehicle-2", which duplicates GSM5720386 even though its title says rep4.

## Tool problems
1. **`tools/case_runner.py:582` cannot record this stop.** It calls `native.align_to_metadata` without first checking the alignment gate's `decision_status`. `tools/native.py:326` raises "no matrix column matched ... record the alignment as unresolved" when nothing matches exactly. The case spec therefore cannot record an alignment stop in the very situation that requires one. The failed attempt also left a case finished as `decided_not_executed`/`valid` (`_previous/attempt1_runner_error/summary.csv`) rather than as an error.
2. **`case_runner inspect` misses this matrix.** It returns `matrices: []` for `GSE190355_fpkm.anno.xls.gz`, a gzipped TSV with an `.xls.gz` name. Meanwhile `native.read_table` (`tools/native.py:205`) only treats names ending exactly in `.xls`/`.xlsx` as Excel, so the file does read correctly as gzipped TSV.
